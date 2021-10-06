#! /bin/env python3
import json
import re
import os
import argparse

# Constant attribute to look for.
# Attributed signal will be considered in the file
# generation
verime_attr = "verilator_me"

# Check the validity of a signal
def __check_netn_validity(nn):
    return nn[0] != "$"


# Check the validity of a cell
def __check_celn_validity(cn):
    return cn[0] != "$"


def __create_mod_path(mod_path, mod_name):
    if mod_path == "":
        return mod_name
    else:
        return "{}.{}".format(mod_path, mod_name)


def __create_entry_path_name(mod_path, mod_name, net_name):
    return "{}.{}".format(__create_mod_path(mod_path, mod_name), net_name)


# Parse signal resulting of generation block
def __parse_generate_index(netpath):
    idxes = re.findall(r"\[([^]]*)\]", netpath)
    vidx = ""
    for i, e in enumerate(idxes):
        if i == len(idxes) - 1:
            vidx += "{}".format(e)
        else:
            vidx += "{}_".format(e)
    return vidx


def __create_match_entry(mod_path, mod_name, net_name, verime_name, width):
    # Create the netpath
    np = __create_entry_path_name(mod_path, mod_name, net_name)
    # Create the potential idx string (for Verilog generate blocks)
    idx_str = __parse_generate_index(np)
    if idx_str != "":
        verime_name_ret = verime_name + "__{}".format(idx_str)
    else:
        verime_name_ret = verime_name
    # Keep the width of the signal
    return [np, verime_name_ret, width]


def __recur_search_verime_attr(mod_jtree, mod_name, mod_inst, mod_path):
    matches = []
    # Iterate over each netname
    for netn in mod_jtree[mod_name]["netnames"].keys():
        # If the signal is valid (i.e., not for yosys purpose), proceed
        if __check_netn_validity(netn):
            # Search for the target attribute
            if (
                verime_attr
                in mod_jtree[mod_name]["netnames"][netn]["attributes"].keys()
            ):
                # Create a new match entry
                ment = __create_match_entry(
                    mod_path,
                    mod_inst,
                    netn,
                    mod_jtree[mod_name]["netnames"][netn]["attributes"][verime_attr],
                    len(mod_jtree[mod_name]["netnames"][netn]["bits"]),
                )
                matches += [ment]

    # Dig into the module cells for other signals in the architecture
    for cn in mod_jtree[mod_name]["cells"].keys():
        if __check_celn_validity(cn):
            matches += __recur_search_verime_attr(
                mod_jtree,
                mod_jtree[mod_name]["cells"][cn]["type"],
                cn,
                __create_mod_path(mod_path, mod_name),
            )
    # Return
    return matches


def search_verime_attr(ld_json_netlist, mod_name, mod_inst):
    return __recur_search_verime_attr(
        ld_json_netlist["modules"], mod_name, mod_inst, ""
    )


# Format the name as generated by Verilator
def __format_cpp_name(netname):
    # Check if the name is from a generated block
    if "[" in netname:
        # Get the signal name
        splitv = netname.split("[")
        sn = splitv[0]
        sn_idx = splitv[1].split("]")[0]
        return "{}__BRA__{}__KET____DOT__".format(sn, sn_idx)
    else:
        return netname


# Create the name of a variable generated by Verilator.
def __create_cpp_cw_name(net_list):
    cw_name = ""
    for e in net_list:
        cw_name += __format_cpp_name(e)
    return cw_name


# Create the list of variables to access a specific signal accross
# the architecture
def __create_cpp_model_var(netpath):
    # Split path with dot chars
    sp_string = netpath.split(".")
    # Generate the list of variable name
    var_names = []
    idx_runner = 0
    end = True
    while idx_runner < len(sp_string):
        # Create empty net_list and fill it
        netlist = []
        runi = 0
        if "[" in sp_string[idx_runner + runi]:
            while "[" in sp_string[idx_runner + runi]:
                runi += 1
            # Final addition
            runi += 1
        netlist = sp_string[idx_runner : idx_runner + runi + 1]
        # Create name
        var_names += [__create_cpp_cw_name(netlist)]
        idx_runner += runi + 1
    return var_names


# Create Verilator path from the list of variables
def __create_cpp_model_path(netpath):
    # Create the model header
    mhead_p = ""
    # Create the global path that should be called from Verilator
    for i, e in enumerate(netpath):
        if i == 0:
            mhead_p = e
        else:
            mhead_p += "->{}".format(e)
    return mhead_p


# Search top module
def __search_top_module(modules_list):
    for e in modules_list.keys():
        if "top" in modules_list[e]["attributes"].keys():
            return e


# Create a list of verilator header required for the cpp library.
def __create_cpp_header_list(modules_list):
    # Create an empty list of header
    head_list = []
    # Search for top module
    topm = __search_top_module(modules_list)
    head_list += ["V{}.h".format(topm)]
    for mn in modules_list.keys():
        head_name = "V{}_{}.h".format(topm, mn)
        head_list += [head_name]
    # Add the Verilated.h header
    head_list += ["verilated.h"]
    return head_list


# Return the corresponding Verilator cpp type based on the width of the signal
def __get_cpp_verilator_type(l):
    if l <= 8:
        return "uint8_t"
    elif 8 < l and l <= 16:
        return "uint16_t"
    elif 16 < l and l <= 32:
        return "uint32_t"
    elif 32 < l and l <= 64:
        return "uint64_t"
    else:
        return "uint32_t *"


# Build Header include based on header list
def __code_include_header(head_list):
    header_code = ""
    for e in head_list:
        inc_code = '#include "{}"\n'.format(e)
        header_code += inc_code
    return header_code


# Build SimModel Structure cpp code.
def __code_SimModel(sim_top_module):
    struct_code = ""
    return """struct SimModel{{ 
    VerilatedContext * contextp;
    V{} * vtop;
}};\n""".format(
        sim_top_module
    )


# Build the code for the create_new_model() function
def __code_h_create_new_model():
    h_code = "SimModel create_new_model();\n"
    return h_code


def __code_cpp_create_new_model(sim_top_module):
    cpp_code = """SimModel create_new_model() {{
    VerilatedContext * contextp = new VerilatedContext;
    V{} * top;
    top = new V{}(contextp);
    SimModel sm;
    sm.contextp = contextp;
    sm.vtop = top;
    return sm;
}}\n""".format(
        sim_top_module, sim_top_module
    )
    return cpp_code


# Build the code for the sim_clock_cycle() function
def __code_h_sim_clock_cycle():
    h_code = "void sim_clock_cycle(SimModel sm);\n"
    return h_code


def __code_cpp_sim_clock_cycle(sim_top_module):
    cpp_code = """void sim_clock_cycle(SimModel sm){{
    V{} * top = sm.vtop;
    top->clk=0;
    top->eval();
    top->clk=1;
    top->eval();
}}\n""".format(
        sim_top_module
    )
    return cpp_code


# Build the code for the delete_model() function
def __code_h_delete_model():
    h_code = "void delete_model(SimModel mod);\n"
    return h_code


def __code_cpp_delete_model():
    cpp_code = """void delete_model(SimModel mod) {
    delete mod.vtop;
    delete mod.contextp;
};\n"""
    return cpp_code


# Build the include barrier code to add on top of the library header file
def __code_inc_barrier(code, libname):
    header_variable = "LIB_{}_H_".format(libname.upper())
    barried_code = "#ifndef {}\n#define {}\n{}\n#endif".format(
        header_variable, header_variable, code
    )
    return barried_code


# Create the accessor definition and code for the given
# match entry (obtained by parsing the Yosys json netlist)
def __code_accessor_declaration(entry):
    # Get the type of the return value
    return_type = __get_cpp_verilator_type(entry[2])
    # Generate the accessor function name
    fname = "get_{}".format(entry[1])
    # Generate the global declaration
    fdec = "{} {}(SimModel sm)".format(return_type, fname)
    return fdec


def __code_accessor_definition(entry):
    fdef = "    return sm.vtop->{};".format(
        __create_cpp_model_path(__create_cpp_model_var(entry[0]))
    )
    return fdef


def __code_h_accessor(entry):
    # Build the declaration
    fdec = __code_accessor_declaration(entry)
    ret_h_f = "{};\n".format(fdec)
    return ret_h_f


def __code_cpp_accessor(entry):
    # Build the definition
    fdec = __code_accessor_declaration(entry)
    fdef = __code_accessor_definition(entry)
    ret_cpp_f = "{}{{\n{}\n}}\n".format(fdec, fdef)
    return ret_cpp_f


# Create the code for the ProbedState structure
def __code_ProbedState_element(entry):
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
        am_32w = l // 32
        if l % 32 != 0:
            am_32w += 1
        return "uint32_t (* {})[{}];".format(entry[1], am_32w)


def __code_ProbedState(entries):
    struct_code = ""
    struct_code += "typedef struct {\n"
    for e in entries:
        struct_code += "    {}\n".format(__code_ProbedState_element(e))
    struct_code += "} ProbedState;\n"
    return struct_code


# Code for the link_state() function
def __code_link_state_declaration():
    def_code = "void link_state(SimModel sm, ProbedState * state)"
    return def_code


def __code_link_state_definition(entries):
    def_code = "{} {{\n".format(__code_link_state_declaration())
    # For each entry write the bounding
    for e in entries:
        if e[2] > 64:
            code_e = "state->{} = &sm.vtop->{}".format(
                e[1], __create_cpp_model_path(__create_cpp_model_var(e[0]))
            )
        else:
            code_e = "state->{} = &sm.vtop->{}".format(
                e[1], __create_cpp_model_path(__create_cpp_model_var(e[0]))
            )

        def_code += "    {};\n".format(code_e)
    # Close bracket
    def_code += "}"
    return def_code


def __code_h_link_state():
    dec_code = __code_link_state_declaration()
    return "{};\n".format(dec_code)


def __code_cpp_link_state(entries):
    def_code = __code_link_state_definition(entries)
    return "{}\n".format(def_code)


# Code for the write_probed_state
def __code_declaration_write_probed_state():
    dec_code = "void write_probed_state(ProbedState * state, FILE * stream)"
    return dec_code


def __code_fwrite_probed_state_elem(entry):
    l = entry[2]
    longword = False
    if l <= 8:
        sizew = 1
        amw = 1
    elif 8 < l and l <= 16:
        sizew = 2
        amw = 1
    elif 16 < l and l <= 32:
        sizew = 4
        amw = 1
    elif 32 < l and l <= 64:
        sizew = 16
        amw = 1
    else:
        longword = True
        sizew = 4
        amw = l // 32
        if l % 32 != 0:
            amw += 1
    if longword:
        return "fwrite(state->{}[0],{},{},stream)".format(entry[1], sizew, amw)
    else:
        return "fwrite(state->{},{},{},stream)".format(entry[1], sizew, amw)


def __code_definition_write_probed_state(entries):
    def_code = "{} {{\n".format(__code_declaration_write_probed_state())
    # For each entry
    for e in entries:
        def_code += "    {};\n".format(__code_fwrite_probed_state_elem(e))
    # Close final bracket
    def_code += "}"
    return def_code


def __code_h_write_probed_state():
    return "{};\n".format(__code_declaration_write_probed_state())


def __code_cpp_write_probed_state(entries):
    return "{}\n".format(__code_definition_write_probed_state(entries))


# Build the library header file based on the list
# of probed signals
def __code_lib_declaration(libname, psgis_entries, header_list, topm):
    # Create the header inclusion list
    hinc = __code_include_header(header_list)
    # Create the functions declarations
    fdec_code = ""
    fdec_code += __code_SimModel(topm) + "\n"
    fdec_code += __code_ProbedState(psgis_entries) + "\n"
    fdec_code += __code_h_create_new_model() + "\n"
    fdec_code += __code_h_sim_clock_cycle() + "\n"
    fdec_code += __code_h_delete_model() + "\n"
    fdec_code += __code_h_link_state() + "\n"
    fdec_code += __code_h_write_probed_state() + "\n"
    # Create the accessor declaration
    fdec_code += "// Individualss accessors.\n"
    for e in psgis_entries:
        fdec_code += __code_h_accessor(e)
    # Create global code
    head_code = "{}\n{}".format(hinc, fdec_code)
    # Add the include barrier
    return __code_inc_barrier(head_code, libname)


# Build the library definition file based on the list
# of probed signals
def __code_lib_definition(libname, psgis_entries, topm):
    # Add the include of the library header
    hinc = '#include  "{}.h"\n'.format(libname)
    # Create the functions definitions
    fdef_code = ""
    fdef_code += __code_cpp_create_new_model(topm) + "\n"
    fdef_code += __code_cpp_sim_clock_cycle(topm) + "\n"
    fdef_code += __code_cpp_delete_model() + "\n"
    fdef_code += __code_cpp_link_state(psgis_entries) + "\n"
    fdef_code += __code_cpp_write_probed_state(psgis_entries) + "\n"
    # Create accessors definition
    fdef_code += "// Individualss accessors.\n"
    for e in psgis_entries:
        fdef_code += __code_cpp_accessor(e) + "\n"
    # Create global code
    def_code = "{}\n{}".format(hinc, fdef_code)
    return def_code


# Create the library files
def build_verilator_library(netjson_fname, libname, out_dir):
    print("#########################################")
    print("# Generating the Verilator library '{}' #".format(libname))
    print("#########################################\n")
    # Load the netlist file
    with open(netjson_fname) as json_netlist:
        netlist = json.load(json_netlist)

    # Search the top module
    tm = __search_top_module(netlist["modules"])
    print("Top module identified in the hierarchy: {}\n".format(tm))

    # Search for the signal to probe
    print("Identified signals paths:")
    sigsp = search_verime_attr(netlist, tm, tm)
    for i, e in enumerate(sigsp):
        print("({}) {} ({})".format(i, e[0], e[2]))
    print("")

    # Build the header list
    head_list = __create_cpp_header_list(netlist["modules"])

    # Build the declaration code
    lib_dec_code = __code_lib_declaration(libname, sigsp, head_list, tm)
    lib_dec_file = out_dir + "/{}.h".format(libname)
    with open(lib_dec_file, "w") as f:
        f.write(lib_dec_code)

    # Build the definition code
    lib_def_code = __code_lib_definition(libname, sigsp, tm)
    lib_def_file = out_dir + "/{}.cpp".format(libname)
    with open(lib_def_file, "w") as f:
        f.write(lib_def_code)

    # Return the list of design files used
    return [__get_elab_list_files(netlist["modules"]), sigsp]


# Create the list of file used in the architecture elaboration
def __get_pathfile(src_attr):
    return src_attr.split(":")[0]


def __get_elab_list_files(modules_list):
    file_list = []
    print("Building design files list...")
    for e in modules_list.keys():
        df_module = __get_pathfile(modules_list[e]["attributes"]["src"])
        print("Module '{}' -> {}".format(e, df_module))
        file_list += [df_module]
    print("")
    return file_list


# Generate the Yosys elaboration script
def __code_yosys_elab_json_script(inc_dirs, top_mod_path, json_out_path, generics_dic):
    script_code = ""
    # Create the include default options for the read_verilog command
    def_rv_options = ""
    hier_libdir_options = ""
    for i, idr in enumerate(inc_dirs):
        if i == len(inc_dirs) - 1:
            def_rv_options += "-I{}".format(idr)
            hier_libdir_options += "-libdir {}".format(idr)
        else:
            def_rv_options += "-I{} ".format(idr)
            hier_libdir_options += "-libdir {} ".format(idr)
    script_code += "verilog_defaults -add {}\n".format(def_rv_options)
    # Add the reading of the initial verilog top module
    script_code += "read_verilog {}\n".format(top_mod_path)
    # Generate the generics options for the hierarchy commands
    gen_options = ""
    for i, gene in enumerate(generics_dic.keys()):
        if i == len(generics_dic.keys()) - 1:
            gen_options += "-chparam {} {}".format(gene, generics_dic[gene])
        else:
            gen_options += "-chparam {} {} ".format(gene, generics_dic[gene])
    # Add the elaboration commands
    top_basename = os.path.basename(top_mod_path)
    top_mn = top_basename.split(".")[0]
    script_code += "hierarchy -top {} {} {}\n".format(
        top_mn, hier_libdir_options, gen_options
    )
    script_code += "proc\n"
    script_code += "write_json {}\n".format(json_out_path)
    return script_code


def __build_yosys_elab_script(
    inc_dirs, top_mod_path, json_out_path, generics_dic, script_path
):
    # Build the code
    code2write = __code_yosys_elab_json_script(
        inc_dirs, top_mod_path, json_out_path, generics_dic
    )
    # Write the file
    with open(script_path, "w") as f:
        f.write(code2write)
    os.system("chmod 766 {}".format(script_path))


def __run_yosys_script(yosys_exec_path, script_path):
    print("Run yosys elaboration")
    cmd = "{} -q -s {}".format(yosys_exec_path, script_path)
    print("RUNNING: {}".format(cmd))
    os.system(cmd)


# Workspace related
def __reset_and_create_dir(workspace_dir):
    # Delete existing workspace
    if os.path.exists(workspace_dir):
        print("")
        print("### WARNING #######################################")
        print("Directory {} found -> the directory will be deleted.".format(workspace_dir))
        print("###################################################")
        print("")
        os.system("rm -rf {}".format(workspace_dir))
    # Create new workspace
    os.system("mkdir -p {}".format(workspace_dir))


def __create_dir(dir_name):
    os.system("mkdir -p {}".format(dir_name))


# Parsing for verilator annotation
def __parse_verilated_me_signs(file_content):
    # Search for verime attribute found in the file
    verime_attr_found = re.findall(r"\(\*.*{}.*\*\)".format(verime_attr), file_content)
    # Search for the verime signal assignation
    verime_sigs = []
    for att_match in verime_attr_found:
        sig_name = att_match.split("{}".format(verime_attr))[1].split('"')[1].split('"')[0]
        verime_sigs += [sig_name]
    # Search for annotated signal declaration
    sig_dec_annot = []
    for vme_sig in verime_sigs:
        sig_dec = re.findall(
            r"\(\*.*{}.*=.*\"{}\".*\*\).*\n.*;".format(verime_attr, vme_sig),
            file_content,
        )
        sig_dec_annot += sig_dec
    # Recover signal declaration only;
    sig_dec_only = []
    for an_sig_dec in sig_dec_annot:
        sig_dec_only += [an_sig_dec.split("\n")[1].lstrip()]
    # Format signal declaration with /* verilator public */
    # annotation
    formated_sig_dec = []
    for sd in sig_dec_only:
        formated_sig_dec += [sd[:-1] + " /* verilator public */;"]
    # Replace attribute with annotated declaration
    ret_content = file_content
    for sd_an, f_sd in zip(sig_dec_annot, formated_sig_dec):
        ret_content = ret_content.replace(sd_an, f_sd)
    return ret_content


# Create the parsed Verilog design files
def __parse_design_files(src_files_list, out_dir):
    # For each design file considered, parse the attribute
    # an annotate target signals before rewritting it
    print("Start annotated files generation...")
    for df in src_files_list:
        print("Processing of '{}'...".format(df), end="")
        # Read file content
        with open(df, "r") as f:
            fcontent = f.read()
        # Parse
        new_fcontent = __parse_verilated_me_signs(fcontent)
        # Rewrite to new location
        filename = os.path.basename(df)
        new_filename = out_dir + "/{}".format(filename)
        with open(new_filename, "w") as f:
            f.write(new_fcontent)
        print(" Done.")
    print("")

# Copy the .vh files from the include directory to the target directory
def __copy_vh_files(inc_dir_list, target_dir):
    # For each include dir in the provided list, copy all the '.vh' files
    # to the target directory
    for idr in inc_dir_list:
        # Check all the file to check if it has the correct extension
        for fname in os.listdir('{}'.format(idr)):
            if fname.endswith('.vh'):
                pathname = '{}/{}'.format(idr,fname)
                cmd = "cp {} {}/".format(pathname,target_dir)
                os.system(cmd)


## Create verilator config
# Create Verilator top-level parameter
def __verilator_param_verilog_generics(generic_dict):
    param_string = ""
    for i, k in enumerate(generic_dict.keys()):
        if i == len(generic_dict.keys()) - 1:
            param_string += "-G{}={}".format(k, generic_dict[k])
        else:
            param_string += "-G{}={} ".format(k, generic_dict[k])
    return param_string


# Create the configuration file for verilator
def __verilator_gen_config_file(config_file, generic_dict, top_module_path):
    # Save the generics
    dic_cfg = {}
    dic_cfg["GENERIC_TOP"] = __verilator_param_verilog_generics(generic_dict)
    # Save the top level filename
    tl_fn = os.path.basename(top_module_path)
    dic_cfg["TOP"] = tl_fn
    # Save the file
    with open(config_file, "w") as cf:
        json.dump(dic_cfg, cf)


#### Argument parsing
## Parse te generics arguments
def __args_parse_generics(argparse_generics):
    dic = {}
    for e in argparse_generics:
        ee = e[0]
        sp_arg = ee.split("=")
        if sp_arg[1].isnumeric():
            dic[sp_arg[0]] = int(sp_arg[1])
        else:
            dic[sp_arg[0]] = sp_arg[1]
    return dic


#### JSON for the format
def __am_bytes(size_bits):
    if size_bits <= 8:
        return 1
    elif 8 < size_bits and size_bits <= 16:
        return 2
    elif 16 < size_bits and size_bits <= 32:
        return 4
    elif 32 < size_bits and size_bits <= 64:
        return 8
    else:
        am_w32 = size_bits // 32
        if size_bits % 32:
            am_w32 + 1
        return 4 * am_w32


def __jsoncfg_sigs_dict(psgis_entries):
    glob_dict = {}
    bytes_total = 0
    for e in psgis_entries:
        e_dict = {}
        e_dict["bytes"] = __am_bytes(e[2])
        e_dict["bits"] = e[2]
        bytes_total += e_dict["bytes"]
        glob_dict[e[1]] = e_dict
    return [glob_dict, bytes_total]


def __jsoncfg_globalcfg_dict(psgis_entries):
    [sig_dict, bytes_am] = __jsoncfg_sigs_dict(psgis_entries)
    ret_dict = {"bytes": bytes_am, "sigs": sig_dict}
    return ret_dict


def __jsoncfg_create(psgis_entries, filename):
    # Create the config dic
    cfg_dic = __jsoncfg_globalcfg_dict(psgis_entries)
    # Write to file
    with open(filename, "w") as f:
        json.dump(cfg_dic, f)


#### Main functions
## Generate the verilator-me package
def __create_verime_package(
    pckg_name,
    build_dir,
    work_dir,
    inc_dir_list,
    generics_dict,
    top_module_path,
    yosys_exec_path,
):
    # Create the different paths
    json_out_path = "{}/net.json".format(work_dir)
    yosys_script_path = "{}/make_yosys.yo".format(work_dir)

    pckg_dir = "{}/{}".format(build_dir, pckg_name)

    pckg_hw_dir = "{}/hw-src".format(pckg_dir)
    pckg_sw_dir = "{}/sw-src".format(pckg_dir)
    pckg_cfg_file = "{}/config-verilator-me.json".format(pckg_dir)
    pckg_data_format_file = "{}/config-dump.json".format(pckg_dir)

    ##########################
    # Create workspace
    __reset_and_create_dir(work_dir)

    # Create build dir
    __reset_and_create_dir(pckg_dir)

    # Create sw dir
    __create_dir(pckg_sw_dir)

    #### Verilator-me run
    # build yosys script
    __build_yosys_elab_script(
        inc_dir_list, top_module_path, json_out_path, generics_dict, yosys_script_path
    )

    # Run yosys script
    __run_yosys_script(yosys_exec_path, yosys_script_path)

    # Build the library files
    [design_files_used, sigsp] = build_verilator_library(
        json_out_path, pckg_name, pckg_sw_dir
    )

    #### Generation of the files for Verilator
    # Generate parsed file to annotate the signal
    # With /* verilator public */ signals
    __create_dir(pckg_hw_dir)
    __parse_design_files(design_files_used, pckg_hw_dir)
    __verilator_gen_config_file(pckg_cfg_file, generics_dict, top_module_path)
    __copy_vh_files(inc_dir_list,pckg_hw_dir)

    # Create the config file for the dumping
    __jsoncfg_create(sigsp, pckg_data_format_file)


## Compile with verilator for the verime package
def __compile_verime_package(
    cpp_files,
    verime_pack_path,
    inc_dirs_list,
    exec_name,
    verilator_dir,
    verilator_exec_path,
):
    ## Reset the Verilator workspace directory
    __reset_and_create_dir(verilator_dir)
    ## -I not working with verilator -> pass by setting CPATH value before
    ## executing verilator. Creation of the new value.
    cpath_new_value = ""
    for i, d in enumerate(inc_dirs_list):
        if i == len(inc_dirs_list) - 1:
            cpath_new_value += "{}:$CPATH".format(os.path.abspath(d))
        else:
            cpath_new_value += "{}:".format(os.path.abspath(d))
    # Add the path of the verime_library
    vpack_abs_path = os.path.abspath(verime_pack_path)
    cpath_new_value = "{}/sw-src:{}".format(vpack_abs_path, cpath_new_value)
    # Create the list of cpp files
    str_cpp_files = ""
    for i, d in enumerate(cpp_files):
        if i == len(cpp_files) - 1:
            str_cpp_files += "{}".format(os.path.abspath(d))
        else:
            str_cpp_files += "{} ".format(os.path.abspath(d))
    libname = os.path.basename(verime_pack_path)
    str_cpp_files += " {}/sw-src/{}.cpp".format(vpack_abs_path, libname)
    # Read the verime package to get the generics and top module
    with open("{}/config-verilator-me.json".format(vpack_abs_path), "r") as f:
        cfg = json.load(f)
    # Build parameters for verilator
    top_mod_path = "{}/hw-src/{}".format(vpack_abs_path, cfg["TOP"])
    srcs_path = "{}/hw-src".format(vpack_abs_path)
    generics_params = cfg["GENERIC_TOP"]
    # Build the executable name
    used_exec_name = os.path.abspath(exec_name)
    # Create global command
    cmd = "CPATH={} {} --cc --exe --build -y {} -Mdir {} -o {} {} {} {}".format(
        cpath_new_value,
        verilator_exec_path,
        srcs_path,
        verilator_dir,
        used_exec_name,
        generics_params,
        top_mod_path,
        str_cpp_files,
    )
    # Run the build command
    print("RUNNING VERILATOR BUILD COMMAND:")
    print(cmd)
    print("\n\n")
    os.system(cmd)


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
        action="append",
        nargs="+",
        help="Directory for the module search.",
    )
    parser.add_argument(
        "-I",
        "--Idir",
        default=[],
        action="append",
        nargs="+",
        help="Directory to search for include.",
    )
    parser.add_argument(
        "-g",
        "--generics",
        default=[],
        action="append",
        nargs="+",
        help="Generic value, as -g<Id>=<Value>.",
    )
    parser.add_argument(
        "-top",
        "--top",
        default=None,
        help="Path to the top module file, e.g. /home/user/top.v.",
    )
    parser.add_argument("--yosys-exec", default="yosys", help="Yosys executable.")
    parser.add_argument(
        "--verime-work", default="/tmp/verime-work", help="Verilator-me workspace."
    )
    parser.add_argument(
        "--pack",
        default=None,
        help="The path to the Verilator-me package used. Path represented as <dirname>/<packname>.",
    )
    parser.add_argument(
        "-cpp",
        "--cpp-files",
        default=[],
        action="append",
        nargs="+",
        help="C++ file to use in the compilation process. If specified, the compilation mode is used.",
    )
    parser.add_argument(
        "--exec",
        default="exec",
        help="Path of the binary produced by the compilation process.",
    )
    parser.add_argument(
        "--verilator-work",
        default="/tmp/verime-verilator-work",
        help="Verilator-me workspace for verilator.",
    )
    parser.add_argument(
        "--verilator-exec", default="verilator", help="Verilator executable."
    )

    args = parser.parse_args()

    ## Check args
    if len(args.cpp_files) == 0:
        if args.top == None:
            print("ERROR: A top module should be provided.")
            quit()
    if args.pack == None:
        print("ERROR: A package should be provided.")
        quit()

    # Create list of arguments
    list_y = []
    for e in args.ydir:
        list_y += [e[0]]

    list_I = []
    for e in args.Idir:
        list_I += [e[0]]

    list_cpp = []
    for e in args.cpp_files:
        list_cpp += [e[0]]

    dic_gen = __args_parse_generics(args.generics)

    # Check if it is compilation of building
    if len(args.cpp_files) == 0:
        # Building package
        __create_verime_package(
            os.path.basename(os.path.abspath(args.pack)),
            os.path.dirname(os.path.abspath(args.pack)),
            args.verime_work,
            list_y,
            dic_gen,
            args.top,
            "yosys",
        )
    else:
        # Compile package
        __compile_verime_package(
            list_cpp,
            os.path.abspath(args.pack),
            list_I,
            args.exec,
            args.verilator_work,
            args.verilator_exec,
        )
