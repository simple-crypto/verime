## Some arbitrary top-level generic
MYGEN_N=16

# Name of the python package that will be generated
PACK_NAME?=counter_example_${MYGEN_N}_lib
# Directory where the package will be generated
PACKAGE_DIR = $(abspath $(PACK_NAME))

# Path to the top level Verilog Module
VERILOG_TOP = srcs/counter.v

# Definition of the top level generics (used by Yosys and Verilator)
VERILOG_PARAMS = \
	    N=${MYGEN_N} 

# Directory where to look for `.v`and `.vh` files
VERILOG_SRC_DIRS = \
	    ./srcs

# C++ wrapper for the top level
SIMU_FILE = test_counter.cpp

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

