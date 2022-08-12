import json
import ctypes
import os

from math import ceil
import numpy as np

# Load of the configuration file and return the cfg instance
def load_cfg_file(cfg_file_path):
    with open(cfg_file_path, "r") as f:
        cfg = json.load(f)
    return cfg

# Generate the configuration from the configuration strings
def load_cfgs(cfgs):
    return json.loads(cfgs)

# Return a specific sector in the file
def get_data_sector(data_filename, config, sec_idx):
    # Get the size of a sector in byte
    ss = config["bytes"]
    # Get the sector
    with open(data_filename, "rb") as df:
        offset = sec_idx * ss
        df.seek(offset)
        data_sector = df.read(ss)
    return data_sector

# Return the specific sector from a buffer
def get_data_sector_buffer(data_buffer, config, sec_idx):
    # Get the size of a sector (in amount of bytes)
    ss = config["bytes"]
    offset = sec_idx * ss
    return data_buffer[offset:offset+ss]

# Read a sector in the open file provided
def read_sector(open_file, size_byte_sector, offset_sector):
    offset = size_byte_sector*offset_sector
    open_file.seek(offset)
    data_sector = open_file.read(size_byte_sector)
    return data_sector


# Return a bunch of specific data sectors.
# The variable sec_idxes contains either (1) a list of indexes or (2) a list of list of indexes.
# In the first case, the return list contains each sectors read.
# In the second case, the return list contains a list of sectors read, where
# the sector read correspond to the list of indexes.
def get_data_sectors(data_filename, config, sec_idxes):
    # Get the size of a sector in byte
    ss = config["bytes"]
    # Generate the buffer
    buff = []
    # Get the sector(s)
    with open(data_filename, "rb") as df:
        if isinstance(sec_idxes[0],list):
            # Iterate over all the list of indexes
            for lidxes in sec_idxes:
                tmpb = []
                # Iterate over indexes
                for sidx in lidxes:
                    data_sector = read_sector(df,ss,sidx)
                    tmpb += [data_sector]
                buff += [tmpb]

        else:
            for sidx in sec_idxes:
                data_sector = read_sector(df,ss,sidx)
                buff += [data_sector]
    return buff

# Return the size in byte of the file
def get_bsize(data_filename):
    fstats = os.stat(data_filename)
    return fstats.st_size

# Return the sector information about the data file
# knowing the amount of runs.
# Returns:
#   - size_byte_file: The amount of bytes in the file
#   - am_bytes_run: The amount of byte in a run
#   - am_sector_run: The amount of clock cycle in a run (i.e., the mount of sectors per run)
#   - am_sectors_full: The global amount of sector in the file
def file_sectors_infos(data_filename,am_runs,config_probed_state):
    size_probed_state = config_probed_state['bytes']
    size_byte_file = get_bsize(data_filename)
    am_bytes_run = size_byte_file // am_runs
    am_sector_run = am_bytes_run // size_probed_state
    am_sectors_full = am_sector_run * am_runs
    return [am_sector_run,am_sectors_full]

# Generate the sectors indexes in the file related to a specific 
# sector index of a run. Put in other way, if one want to read a specific 
# sector of a run and to it for each run of the file, this function 
# generate the list of sector indexes.
def indexes_sector(relative_index, amount_sectors_file, amount_sector_run):
    if isinstance(relative_index,list):
        ret = []
        for ri in relative_index:
            assert ri<amount_sector_run
            ret += [list(range(ri,amount_sectors_file,amount_sector_run))]
        return ret
    else:
        assert relative_index<amount_sector_run
        return list(range(relative_index,amount_sectors_file,amount_sector_run))

# Get the bits representation of the bytestring
def byte2bits(bytestr, am_bits):
    bits_array = am_bits * [0]
    for idx in range(am_bits):
        by_idx = idx // 8
        bi_idx = idx % 8
        bits_array[idx] = (bytestr[by_idx] >> bi_idx) & 0x1
    return np.array(bits_array)

# Decode data_sector
def decode_data_sector(data_sec, config):
    # Create the empty dic for the obtained signal
    sigs_dic = {}
    # Iterate over each signals
    processed_bytes = 0
    for k in config["sigs"].keys():
        cu_data_bytes = config["sigs"][k]["bytes"]
        cu_data_bits = config["sigs"][k]["bits"]
        current_bytes = data_sec[processed_bytes : processed_bytes + cu_data_bytes]
        sigs_dic[k] = byte2bits(current_bytes, cu_data_bits)
        processed_bytes += cu_data_bytes
    return sigs_dic

# Decode data_sector and return byte
def decode_data_sector_bytes(data_sec, config):
    # Create the empty dic for the obtained signal
    sigs_dic = {}
    # Iterate over each signals
    processed_bytes = 0
    for k in config["sigs"].keys():
        cu_data_bytes = config["sigs"][k]["bytes"]
        current_bytes = data_sec[processed_bytes : processed_bytes + cu_data_bytes]
        sigs_dic[k] = current_bytes
        processed_bytes += cu_data_bytes
    return sigs_dic

# Decode multiple data sector, as obtained with the return 
# of get_data_sectors()
def decode_data_sectors(data_secs, config):
    if isinstance(data_secs,list):
        if isinstance(data_secs[0],list):
            buff = []
            for sl in data_secs:
                tmp_buff = []
                for s in sl:
                    tmp_buff += [decode_data_sector(s,config)]
                buff += [tmp_buff]
            return buff
        else:
            buff = []
            for s in data_secs:
                buff += [decode_data_sector(s,config)]
            return buff
    else:
        return decode_data_sector(data_secs,config)

# Return a vector of byte from a vector of bits. The bits 
# in the vector are ordered in little endian.
def bits2bytes(bvec):
    lb = len(bvec)
    am_bytes = ceil(lb / 8)
    # Padding
    am_bit_padding = 8*am_bytes-lb
    if am_bit_padding>0:
        vp = am_bit_padding*[0]
        p_bvec = bvec + vp
    else:
        p_bvec = bvec
    # Build the bytes vec
    byte_vec = am_bytes*[0]
    for b in range(am_bytes):
        tmp = 0
        for i in range(8):
            bit = p_bvec[8*b+i]
            tmp += (2**i)*bit
        byte_vec[b] = tmp
    return byte_vec

# Load and reload the ctypes library
def load_library(lib_path):
    return ctypes.CDLL(lib_path)

# Create a ctype string buffer with the provided String
def get_csb(string):
    sb = string.encode('utf-8')
    return ctypes.create_string_buffer(sb)

## Test
if __name__ == "__main__":
    import argparse
    # Parsing arguments
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
            )
    parser.add_argument(
            "-cf",
            "--config-file",
            default=None,
            help="Path to the config file."
            )
    parser.add_argument(
            "-df",
            "--data-file",
            default=None,
            help="Path to the data sampled."
            )
    parser.add_argument(
            "-c",
            "--clk",
            default=0,
            type=int,
            help="Clock cycle to probe"
            )

    args = parser.parse_args()

    # Config
    config_file = args.config_file
    data_file = args.data_file

    # Load config
    conf = load_cfg_file(config_file)

    # Get data sector
    data_sec = get_data_sector(data_file, conf, args.clk)

    print("Sector")
    print([hex(e) for e in data_sec])

    # Decode it
    dec_dic = decode_data_sector(data_sec, conf)

    for k in dec_dic.keys():
        print("Sig: {} ({} bits)\n-> {}\n".format(k, len(dec_dic[k]), dec_dic[k]))
