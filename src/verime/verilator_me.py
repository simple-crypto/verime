#! /bin/env python3
import math
import json
import re
import os
import argparse
import shutil
import subprocess
import itertools as it

# Constant attribute to look for.
# Attributed signal will be considered in the file
# generation
VERIME_ATTR = "verilator_me"
PROBED_STATE_C_VAR = "probed_state_bytes"

def list_all_instances(netlist, top_module):
    """Walk the tree of instances reprensented by the netlist and for each
    instance, yield the path as a list of strings and the module type.
    """
    yield ([], top_module)
    for cell_name, cell in netlist["modules"][top_module]["cells"].items():
        # skip yosys internal names
        if '$' not in cell_name:
            for path, mod in list_all_instances(netlist, cell["type"]):
                yield ([cell_name]+path, mod)

def list_verime_nets(module):
    """In a module, list all nets with the verilator_me attribute, and for
    each one, yield its name, its width, and the value of the verilator_me
    attribute.
    """
    for netn, net in module['netnames'].items():
        if not netn.startswith('$') and VERIME_ATTR in net['attributes']:
            width = len(net['bits'])
            yield (netn, width, net['attributes'][VERIME_ATTR])

def find_verime_nets(netlist, top_module):
    """In the architecture, list all signals with a verilator_me attribute.
    For each such signal, yield its path, the value of the verilator_me
    attribute (suffixed to be unique) and its with.
    """
    for path, module in list_all_instances(netlist, top_module):
        mod_path = '.'.join([top_module] + path)
        for (net_name, width, verime_name) in list_verime_nets(netlist['modules'][module]):
            net_path = mod_path + '.' + net_name
            # Parse signal resulting of generation block
            idx_str = '_'.join(re.findall(r"\[([^]]*)\]", net_path))
            if idx_str != "":
                verime_name += "__" + idx_str
            yield (net_path, verime_name, width)


# Format the name as generated by Verilator
def __format_cpp_name(netname, last_in_path):
    # Check if the name is from a generated block
    if "[" in netname:
        # Get the signal name
        splitv = netname.split("[")
        sn = splitv[0]
        sn_idx = splitv[1].split("]")[0]
        if last_in_path:
            return "{}[{}]".format(sn, sn_idx)
        else:
            return "{}__BRA__{}__KET____DOT__".format(sn, sn_idx)
    else:
        return netname


# Create the name of a variable generated by Verilator.
def __create_cpp_cw_name(net_list, last_in_path):
    return ''.join(__format_cpp_name(e, last_in_path) for e in net_list)


# Create the list of variables to access a specific signal accross
# the architecture
def __create_cpp_model_var(net_path):
    # Split path with dot chars
    sp_string = net_path.split(".")
    # Generate the list of variable name
    var_names = []
    idx_runner = 0
    end = True
    while idx_runner < len(sp_string):
        # Create empty net_list and fill it
        net_list = []
        runi = 0
        if "[" in sp_string[idx_runner + runi]:
            while (idx_runner + runi < len(sp_string)) and "[" in sp_string[
                idx_runner + runi
            ]:
                runi += 1
        net_list = sp_string[idx_runner : idx_runner + runi + 1]
        # Create name
        last_in_path = idx_runner + runi + 1 > len(sp_string)
        var_names += [__create_cpp_cw_name(net_list, last_in_path)]
        idx_runner += runi + 1
    return '->'.join(var_names)


def width2storage(l):
    """From the width in bits of a signal, return a description of the encoding
    of the signal as (word_size, is_array, array_length)."""
    if l <= 8:
        return (1, False, 1)
    elif 8 < l and l <= 16:
        return (2, False, 1)
    elif 16 < l and l <= 32:
        return (4, False, 1)
    elif 32 < l and l <= 64:
        return (8, False, 1)
    else:
        return (4, True, math.ceil(l / 32))


def storage_size(l):
    word_size, _, array_length = width2storage(l)
    return word_size * array_length


def size_probed_state(psig_entries):
   return sum(storage_size(entry[2]) for entry in psig_entries)


def code_SimModel(sim_top_module):
    return fn_def((
        'struct SimModel',
        ['VerilatedContext * contextp;', f'V{sim_top_module} * vtop;']
        )) + ';'

def code_new_model_ptr(sim_top_module):
    return (
            'extern "C" SimModel * new_model_ptr()',
            [
                f'VerilatedContext * contextp = new VerilatedContext;',
                f'V{sim_top_module} * top = new V{sim_top_module}(contextp);',
                f'SimModel * sm_ptr = (struct SimModel *) malloc(sizeof(struct SimModel));',
                f'sm_ptr->contextp = contextp;',
                f'sm_ptr->vtop = top;',
                f'return sm_ptr;',
                ]
            )


def code_delete_model_ptr():
    return (
            'extern "C" void delete_model_ptr(SimModel * sm)',
            [
                'delete(sm->vtop);',
                'delete(sm->contextp);',
                'free(sm);',
                ]
            )


def code_sim_clock_cycle(sim_top_module):
    return (
            "void sim_clock_cycle(SimModel * sm)",
            [
                f'V{sim_top_module} * top = sm->vtop;',
                f'top->clk=0;',
                f'top->eval();',
                f'top->clk=1;',
                f'top->eval();',
                ]
            )


def code_inc_barrier(code, libname):
    """Build the include barrier code to add on top of the library header
    file."""
    header_variable = "LIB_{}_H_".format(libname.upper())
    barried_code = "#ifndef {}\n#define {}\n{}\n#endif".format(
        header_variable, header_variable, code
    )
    return barried_code


def code_accessor(entry):
    # Get the type of the return value
    word_size, is_array, _ = width2storage(entry[2])
    return_type = {
        (1, False): "uint8_t",
        (2, False): "uint16_t",
        (4, False): "uint32_t",
        (8, False): "uint64_t",
        (4, True): "uint32_t *",
    }[(word_size, is_array)]
    # Accessor function name
    fname = "get_{}".format(entry[1])
    return (
            "{} {}(SimModel * sm)".format(return_type, fname),
            ["return sm->vtop->{};".format(__create_cpp_model_var(entry[0]))],
            )

def code_ProbedState_element(entry):
    """Create the code for the ProbedState structure."""
    l = entry[2]
    if l <= 8:
        return "uint8_t * {};".format(entry[1])
    elif 8 < l and l <= 16:
        return "uint16_t * {};".format(entry[1])
    elif 16 < l and l <= 32:
        return "uint32_t * {};".format(entry[1])
    elif 32 < l and l <= 64:
        return "uint64_t * {};".format(entry[1])
    else:
        return "uint32_t (* {})[{}];".format(entry[1], math.ceil(l/32))


def code_ProbedState(entries):
    return '\n'.join([
        "typedef struct {",
        *("    " + code_ProbedState_element(e) for e in entries),
        "} ProbedState;"
        ])


def code_new_probed_state_ptr():
    return (
            'extern "C" ProbedState * new_probed_state_ptr()',
            [
                'ProbedState prb_st;',
                'ProbedState * prb_st_ptr = (ProbedState *) malloc(sizeof(ProbedState));',
                'memcpy(prb_st_ptr,&prb_st,sizeof(ProbedState));',
                'return prb_st_ptr;',
                ]
            )

def state_typecast(width):
    return f'(uint32_t (*)[{math.ceil(width / 32)}])' if width > 64 else ''

def code_link_state(entries):
    return (
            "void link_state(SimModel * sm, ProbedState * state)",
            [
                "state->{} = {} &sm->vtop->{};".format(
                    e[1], state_typecast(e[2]), __create_cpp_model_var(e[0])
                    )
                for e in entries
                ]
            )


def code_fwrite_probed_state_elem(entry):
    sizew, longword, amw  = width2storage(entry[2])
    return f'fwrite(state->{entry[1]}{[0] if longword else ""},{sizew},{amw},stream);'


def code_write_probed_state(entries):
    return (
            "void write_probed_state(ProbedState * state, FILE * stream)",
            [code_fwrite_probed_state_elem(e) for e in entries]
            )


def code_dump_json(psig_entries, generics_dict, top_module):
    sig_dict = {
            e[1]: { "bytes": storage_size(e[2]), "bits": e[2] }
            for e in psig_entries
    }
    cfg_dic = {
            "bytes": size_probed_state(psig_entries),
            "sigs": sig_dict,
            "GENERIC_TOP": ' '.join(f'-G{gn}={gv}' for gn, gv in generics_dict.items()),
            "TOP": top_module
            }
    # Create the JSON string and replace the quote for C formatting
    json_str = json.dumps(cfg_dic).replace('"', '\\"')
    return (
            "const char * dump_json()",
            [f'return "{json_str}";']
            )


# Code to generate the code for the ProbedStateBuffer
def code_memcpy_probed_state_elem(entry, offset_bytes, target_ptr):
    sizew, longword, amw  = width2storage(entry[2])
    # Generate the format with target
    target_format = target_ptr.format(offset_bytes)
    source_format = f'ps->{entry[1]}{[0] if longword else ""}'
    size_format = sizew * amw
    memcpy_format = "memcpy({},{},{})".format(target_format, source_format, size_format)
    return memcpy_format


def code_core_write_probed_state_to_buffer(entries, target_ptr):
    def_core_code = []
    offset_bytes = 0
    for e in entries:
        def_core_code.append(
                '    ' + code_memcpy_probed_state_elem(e, offset_bytes, target_ptr) + ';'
                )
        offset_bytes += storage_size(e[2])
    return '\n'.join(def_core_code)


def code_ProbedStateBuffer(psig_entries):
    return fn_def(('typedef struct', [
        f'char (* buffer)[{size_probed_state(psig_entries)}];',
        'uint32_t am_ps;',
    ])) + ' ProbedStateBuffer;'


def code_new_ProbedStateBuffer_ptr(psig_entries):
    size_ps = size_probed_state(psig_entries)
    return (
            'extern "C" ProbedStateBuffer * new_probed_state_buffer_ptr(uint32_t n)',
            [
                f'char (* buffer)[{size_ps}] = (char (*) [{size_ps}]) malloc(n*{size_ps});',
                'ProbedStateBuffer * psb_ptr = (ProbedStateBuffer *) malloc(sizeof(ProbedStateBuffer));',
                'psb_ptr->buffer = buffer;',
                'psb_ptr->am_ps = 0;',
                'return psb_ptr;',
                ]
            )


def code_delete_ProbedStateBuffer_ptr():
    return (
            'extern "C" void delete_probed_state_buffer_ptr(ProbedStateBuffer * ptr)',
            [
                'free(ptr->buffer);',
                'free(ptr);',
                ]
            )


def code_write_probed_state_to_buffer(psig_entries):
    core_copy_code = code_core_write_probed_state_to_buffer(
        psig_entries, "&psb->buffer[psb->am_ps][{}]"
    )
    return (
            "void write_probed_state_to_buffer(ProbedState * ps, ProbedStateBuffer * psb)",
            [
                core_copy_code,
                'psb->am_ps += 1;'
                ]
            )


def code_write_probed_state_to_charbuffer(psig_entries):
    core_copy_code = code_core_write_probed_state_to_buffer(psig_entries, "&cb[{}]")
    return (
            "void write_probed_state_to_charbuffer(char * cb, ProbedState * ps)",
            [ core_copy_code, ]
            )


def code_reset_ProbedStateBuffer():
    return (
            "void reset_probed_state_buffer(ProbedStateBuffer * psb)",
            [ 'psb->am_ps = 0;', ]
            )


def code_flush_probed_state_buffer(psig_entries):
    sizebyte_ps = size_probed_state(psig_entries)
    return (
            'extern "C" void flush_probed_state_buffer(ProbedStateBuffer * psb, FILE * stream)',
            [
                f'for(uint32_t i=0; i<psb->am_ps; i++) {{',
                f'    fwrite(&psb->buffer[i],{sizebyte_ps},1,stream);',
                f'}}',
                f'reset_probed_state_buffer(psb);',
                ]
            )


def code_probed_state_bytes(psig_entries):
    sizebyte_ps = size_probed_state(psig_entries)
    return "const uint32_t {} = {};\n".format(PROBED_STATE_C_VAR, sizebyte_ps)

def fn_decl(code):
    return code[0]+';'

def fn_def(code):
    return '{} {{\n{}\n}}'.format(
            code[0],
            '\n'.join('    '+l for l in code[1])
            )


def code_verilator_lib(libname, psgis_entries, header_list, topm, generics_dict):
    functions = [
            code_new_model_ptr(topm),
            code_delete_model_ptr(),
            code_new_probed_state_ptr(),
            code_new_ProbedStateBuffer_ptr(psgis_entries),
            code_delete_ProbedStateBuffer_ptr(),
            code_write_probed_state_to_buffer(psgis_entries),
            code_write_probed_state_to_charbuffer(psgis_entries),
            code_reset_ProbedStateBuffer(),
            code_flush_probed_state_buffer(psgis_entries),
            code_sim_clock_cycle(topm),
            code_link_state(psgis_entries),
            code_write_probed_state(psgis_entries),
            *[code_accessor(e) for e in psgis_entries],
            code_dump_json(psgis_entries, generics_dict, topm),
    ]
    datastructs = [
            code_probed_state_bytes(psgis_entries),
            code_SimModel(topm),
            code_ProbedState(psgis_entries),
            code_ProbedStateBuffer(psgis_entries),
    ]
    header_decls = '\n'.join(
            [f'#include "{header}"' for header in header_list] +
            datastructs +
            [fn_decl(fn) for fn in functions]
            )
    header_code = code_inc_barrier(header_decls, libname)
    cpp_code = '\n'.join(
            # Include the library header
            ['#include  "{}.h"'.format(libname)] +
            [fn_def(fn) for fn in functions]
    )
    return (header_code, cpp_code)

# Create the library files
def build_verilator_library(netlist, libname, out_dir, generics_dict):
    print("# Generating the Verilator library '{}' #".format(libname))

    # Search the top module
    tm = next(mname for mname, mod in netlist["modules"].items() if "top" in mod["attributes"])
    print("Top module identified in the hierarchy: {}\n".format(tm))

    # Search for the signal to probe
    print("Identified signals paths:")
    sigsp = list(find_verime_nets(netlist, tm))
    for i, e in enumerate(sigsp):
        print("({}) {} ({})".format(i, e[0], e[2]))

    # Header list
    head_list = ["V{}__Syms.h".format(tm)]

    # Write verilator library (.cpp and .h)
    lib = code_verilator_lib(libname, sigsp, head_list, tm, generics_dict)
    for code, suffix in zip(lib, ('.h', '.cpp')):
        with open(os.path.join(out_dir, libname+suffix), "w") as f:
            f.write(code)

    # Return the list of design files used
    return (
            [
            module["attributes"]["src"].split(':')[0]
            for module in netlist['modules'].values()
            ],
            sigsp
            )


# Generate the Yosys elaboration script
def gen_yosys_commands(inc_dirs, top_mod_path, json_out_path, generics_dic):
    yosys_commands = []
    # Create the include default options for the read_verilog command
    def_rv_options = ' '.join(f'-I{idr}' for idr in inc_dirs)
    yosys_commands.append(f'verilog_defaults -add {def_rv_options}')
    # Add the reading of the initial verilog top module
    yosys_commands.append(f'read_verilog {top_mod_path}')
    # Generate the generics options for the hierarchy commands
    gen_options = ' '.join(f'-chparam {gene} {gval}' for gene, gval in generics_dic.items())
    # Add the elaboration commands
    top_mn = os.path.splitext(os.path.basename(top_mod_path))[0]
    hier_libdir_options = ' '.join(f'-libdir {idr}' for idr in inc_dirs)
    yosys_commands.append("hierarchy -top {} {} {}".format(
        top_mn, hier_libdir_options, gen_options
    ))
    yosys_commands.append('proc')
    yosys_commands.append(f'write_json {json_out_path}')
    return yosys_commands


def run_yosys(yosys_exec_path, yosys_commands):
    args = [yosys_exec_path, '-q'] + list(
            it.chain.from_iterable(('-p', cmd) for cmd in yosys_commands)
            )
    print("Yosys command", args)
    subprocess.run(args, check=True)


class StringLines:
    def __init__(self, s):
        lines = s.splitlines()
        if s.endswith('\n'):
            lines.append('') # Preserve end-of-file '\n'
        self.s = '\n'.join(lines)
        self.line_lengths = [len(l) for l in lines]
        # +1 stands for the '\n'
        self.line_offsets = [0] + list(it.accumulate(l+1 for l in self.line_lengths))[:-1]
        assert self.s == s

    def line_offset2position(self, line, offset):
        """Line and offset start at 1."""
        assert offset <= self.line_lengths[line-1]
        return self.line_offsets[line-1] + offset - 1


def create_annotated_design(netlist, out_dir):
    """Create a copy of all design files in out_dir, with a /* verilator public
    */ comment appended to every wire declaration with a VERIME_ATTR
    attribute."""
    # Do not open twice a file if it contains multiple module declarations.
    design_files = dict()
    # There might be multiple module objects per module declaration (due to
    # parameters), avoid to treat one multiple times.
    module_srcs = set()
    for mname, module in netlist['modules'].items():
        src = module['attributes']['src']
        if src not in module_srcs:
            module_srcs.add(src)
            fname = ':'.join(src.split(':')[:-1])
            if fname not in design_files:
                with open(fname, "r") as f:
                    design_files[fname] = (StringLines(f.read()), [])
            file_lines, inserts = design_files[fname]
            # There might be multiple netname objects per wire declaration (due to
            # generate blocks), avoid to treat one multiple times.
            net_srcs = set()
            for net_name, net in module["netnames"].items():
                if VERIME_ATTR in net["attributes"] and net["attributes"]["src"] not in net_srcs:
                    net_srcs.add(net["attributes"]["src"])
                    decl = net["attributes"]["src"].split(':')[-1]
                    start_pos, end_pos = [pos.split('.') for pos in decl.split('-')]
                    end_line, end_offset = [int(x) for x in end_pos]
                    pos = file_lines.line_offset2position(end_line, end_offset)
                    # Insert the /* verilator public */ before the ';'
                    # that follows the declaration.
                    inserts.append(file_lines.s.index(';', pos))
    # Write back the files with the comments inserted.
    for fname, (fl, inserts) in design_files.items():
        inserts.sort()
        new_content = ' /* verilator public */ '.join(
                fl.s[start:end] for start, end in zip([0] + inserts, inserts + [len(fl.s)])
                )
        with open(os.path.join(out_dir, os.path.basename(fname)), "w") as f:
            f.write(new_content)

def copy_vh_files(inc_dir_list, target_dir):
    """Copy the .vh files from the include directory to the target directory."""
    for idr in inc_dir_list:
        for fname in os.listdir(idr):
            if fname.endswith(".vh"):
                shutil.copy(os.path.join(idr, fname), os.path.join(target_dir, fname))


def gen_config_file(config_file, generic_dict, top_module_path):
    with open(config_file, "w") as cf:
        json.dump(dic_cfg, cf)


#### Main functions
## Generate the verilator-me package
def create_verime_package(
    pckg_name,
    build_dir,
    inc_dir_list,
    generics_dict,
    top_module_path,
    yosys_exec,
    pckg_sw_dir=None,
    pckg_hw_dir=None,
):
    json_out_path = os.path.join(build_dir, 'net.json')
    if pckg_sw_dir is None:
        pckg_sw_dir = os.path.join(build_dir, 'sw-src')
    if pckg_hw_dir is None:
        pckg_hw_dir = os.path.join(build_dir, 'hw-src')

    # Create workspace
    for d in [build_dir, pckg_sw_dir, pckg_hw_dir]:
        os.makedirs(d, exist_ok=True)

    # Yosys
    yosys_commands = gen_yosys_commands(
        inc_dir_list, top_module_path, json_out_path, generics_dict
    )
    run_yosys(yosys_exec, yosys_commands)
    with open(json_out_path) as json_netlist:
        netlist = json.load(json_netlist)

    # Build the library files (.h and .cpp)
    [design_files_used, sigsp] = build_verilator_library(
        netlist, pckg_name, pckg_sw_dir, generics_dict
    )

    #### Generation of the files for Verilator
    # Generate parsed file to annotate the signal
    # With /* verilator public */ signals
    create_annotated_design(netlist, pckg_hw_dir)
    copy_vh_files(inc_dir_list, pckg_hw_dir)


# Main program
if __name__ == "__main__":
    # Parsing arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-y",
        "--ydir",
        default=[],
        action="extend",
        nargs='+',
        type=str,
        help="Directory for the module search.",
    )
    parser.add_argument(
        "-g",
        "--generics",
        action="extend",
        nargs='+',
        type=str,
        help="Verilog generic value, as -g<Id>=<Value>.",
    )
    parser.add_argument(
        "-t",
        "--top",
        required=True,
        help="Path to the top module file, e.g. /home/user/top.v.",
    )
    parser.add_argument("--yosys-exec", default="yosys", help="Yosys executable.")
    parser.add_argument(
        "--pack",
        required=True,
        help="The Verilator-me package name.",
    )
    parser.add_argument(
        "--build-dir",
        default=".",
        help="The build directory.",
    )
    parser.add_argument(
        "--sw-dir",
        help="Directory to store generated .cpp and .h files.",
    )
    parser.add_argument(
        "--hw-dir",
        help="Directory to store generated verilog files.",
    )
    args = parser.parse_args()

    dic_gen = {}
    for e in args.generics:
        name, val = e.split('=')
        dic_gen[name] = int(val) if val.isnumeric() else val

    # Building package
    create_verime_package(
        args.pack,
        os.path.abspath(args.build_dir),
        args.ydir,
        dic_gen,
        args.top,
        "yosys",
        pckg_sw_dir=args.sw_dir,
        pckg_hw_dir=args.hw_dir,
    )
