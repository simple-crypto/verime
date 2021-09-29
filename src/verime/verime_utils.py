import json

# Load of the configuration file and return the cfg instance
def load_cfg_file(cfg_file_path):
    with open(cfg_file_path, "r") as f:
        cfg = json.load(f)
    return cfg


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


# Get the bits representation of the bytestring
def byte2bits(bytestr, am_bits):
    bits_array = am_bits * [0]
    for idx in range(am_bits):
        by_idx = idx // 8
        bi_idx = idx % 8
        bits_array[idx] = (bytestr[by_idx] >> bi_idx) & 0x1
    return bits_array


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


## Test
if __name__ == "__main__":
    print("Test of verime-utils")

    # Config
    config_file = "test/my_funky_lib/config-dump.json"
    data_file = "test/test.save"

    # Load config
    conf = load_cfg_file(config_file)

    with open(data_file, "rb") as f:
        print([hex(e) for e in f.read()])

    # Get data sector
    data_sec = get_data_sector(data_file, conf, 1)

    print("Sector")
    print([hex(e) for e in data_sec])

    # Decode it
    dec_dic = decode_data_sector(data_sec, conf)

    for k in dec_dic.keys():
        print("Sig: {} ({} bits)\n-> {}\n".format(k, len(dec_dic[k]), dec_dic[k]))
