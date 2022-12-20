## Some arbitrary top-level generic
MYGEN_L=10
MYOTHERGEN_W=16

# Name of the python package that will be generated
PACK_NAME?=verilogcstyle_test_lib_${MYGEN_L}_${MYOTHERGEN_W}
# Directory where the package will be generated
PACKAGE_DIR = $(abspath $(PACK_NAME))

# Path to the top level Verilog Module
VERILOG_TOP = srcs/top.v

# Definition of the top level generics (used by Yosys and Verilator)
VERILOG_PARAMS = \
	    L=${MYGEN_L} \
	    W=${MYOTHERGEN_W}

# Directory where to look for `.v`and `.vh` files
VERILOG_SRC_DIRS = \
	    ../../hdl/aes_32bits \
	    ../../hdl/glob_MSKaes \
	    ../../hdl/masked_gadgets \
	    ../../hdl/rnd_gen \
	    ../../hdl/sbox

# C++ wrapper for the top level
SIMU_FILE = test_main.cpp

all: verime

verime:
	verime \
	    $(addprefix -y ,$(VERILOG_SRC_DIRS)) \
	    -g $(VERILOG_PARAMS) \
	    --top $(VERILOG_TOP) \
	    --pack $(PACK_NAME) \
	    --build-dir $(PACKAGE_DIR) \
	    --simu $(SIMU_FILE)
	make -C $(PACKAGE_DIR)

clean:
	rm -rf $(PACKAGE_DIR)

.PHONY: verime clean all

