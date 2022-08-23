PACK_NAME?=testverime_lib
PACKAGE_DIR = $(abspath $(PACK_NAME))
BUILD_DIR = $(PACKAGE_DIR)/build
VERILATOR_DIR = $(PACKAGE_DIR)/verilator

VERILOG_TOP = srcs/top.v

VERILOG_PARAMS = W=7
VERILOG_SRC_DIRS = \
	    ./srcs
IMPLEM_NAME = $(basename $(notdir $(VERILOG_TOP)))
VERILATED_NAME=V$(IMPLEM_NAME)
VERILIB=$(VERILATOR_DIR)/$(VERILATED_NAME)__ALL.a

MAKEFILE_PATH = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

CPP_WRAPPER=test_main

SWIG_WRAPPER = $(VERILATOR_DIR)/$(CPP_WRAPPER)_wrap.cpp

# FIXME find python
LDLIBS = -pthread -lpthread -latomic

# FIXME
PYTHON_INCLUDE=/usr/include/python3.8

VERIME_DIR = $(PACKAGE_DIR)/verime
VERIME_TOUCH = $(VERIME_DIR)/.verime

VERILATOR_CFLAGS += -fPIC
VERILATOR_CFLAGS += -I$(PYTHON_INCLUDE)

CPP=g++

all: default

$(BUILD_DIR) $(VERILATOR_DIR):
	mkdir -p $@

$(VERIME_TOUCH) $(VERILATOR_DIR)/$(PACK_NAME).cpp &: $(VERILATOR_DIR)
	python3 -m verime.verilator_me \
	    $(addprefix -y ,$(VERILOG_SRC_DIRS)) \
	    -g $(VERILOG_PARAMS) \
	    --top $(VERILOG_TOP) \
	    --pack $(PACK_NAME) \
	    --build-dir $(VERIME_DIR) \
	    --sw-dir $(VERILATOR_DIR)
	touch $@

$(SWIG_WRAPPER): $(MAKEFILE_PATH)/$(CPP_WRAPPER).i | $(VERILATOR_DIR)
	cp $< $(VERILATOR_DIR)/$(CPP_WRAPPER).i
	swig -c++ -python -outdir $(PACKAGE_DIR) $(VERILATOR_DIR)/$(CPP_WRAPPER).i
	mv $(subst .cpp,.cxx,$@) $@

$(VERILIB): $(VERIME_TOUCH)
	verilator \
	    --cc --build -Mdir $(VERILATOR_DIR) \
	    -Wno-WIDTH -Wno-PINMISSING \
	    $(addprefix -G,$(VERILOG_PARAMS)) \
	    $(addprefix -CFLAGS ,$(VERILATOR_CFLAGS)) \
	    --threads 1 \
	    -y $(VERIME_DIR)/hw-src \
	    $(IMPLEM_NAME).v

$(VERILATOR_DIR)/verilated.o: $(VERILIB)
	make -C $(VERILATOR_DIR) -f V$(IMPLEM_NAME).mk $(notdir $@)

$(VERILATOR_DIR)/$(CPP_WRAPPER).cpp: $(MAKEFILE_PATH)/$(CPP_WRAPPER).cpp | $(VERILATOR_DIR)
	cp $< $@

$(VERILATOR_DIR)/%.o: $(VERILATOR_DIR)/%.cpp $(VERIME_TOUCH) $(VERILIB)
	make -C $(VERILATOR_DIR) -f V$(IMPLEM_NAME).mk $(notdir $@)

$(BUILD_DIR)/%.o: $(BUILD_DIR)/%.cpp $(VERIME_TOUCH) $(VERILIB)
	ccache $(CPP) -I. -MMD $(CFLAGS) -std=gnu++14 -c $< -o $@


$(PACKAGE_DIR)/_$(CPP_WRAPPER).so: \
    $(VERILATOR_DIR)/$(CPP_WRAPPER)_wrap.o \
    $(VERILATOR_DIR)/$(CPP_WRAPPER).o \
    $(VERILATOR_DIR)/verilated.o \
    $(VERILATOR_DIR)/$(notdir $(PACKAGE_DIR)).o \
    $(VERILIB)
	$(CPP) -shared $(LDLIBS) $^ -o $@

default: $(PACKAGE_DIR)/_$(CPP_WRAPPER).so

clean:
	rm -rf $(PACKAGE_DIR)

.PHONY: default clean all

