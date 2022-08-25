
# FIXME
PYTHON_INCLUDE=/usr/include/python3.8
VERILATOR_CFLAGS += -I$(PYTHON_INCLUDE)

VERILIB=$(BUILD_DIR)/V$(IMPLEM_NAME)__ALL.a

VERILATOR_CFLAGS += -fPIC

LDLIBS = -pthread -lpthread -latomic

VERIME_SRC_GEN = \
	     $(BUILD_DIR)/verime_lib \
	     $(BUILD_DIR)/simulation_runner \
	     $(BUILD_DIR)/simu

SIMU_O = $(addsuffix .o,$(VERIME_SRC_GEN)) $(BUILD_DIR)/verilated.o

CPP=g++

all: wheel

$(VERILIB):
	verilator \
	    --cc --build -Mdir $(BUILD_DIR) \
	    -Wno-WIDTH -Wno-PINMISSING \
	    $(addprefix -CFLAGS ,$(VERILATOR_CFLAGS)) \
	    $(addprefix -G,$(VERILOG_PARAMS)) \
	    --threads 1 \
	    -y $(HW_SRC) \
	    $(IMPLEM_NAME).v \

$(BUILD_DIR)/verilated.o: $(VERILIB)
	make -C $(BUILD_DIR) -f V$(IMPLEM_NAME).mk $(notdir $@)

$(BUILD_DIR)/%.o: $(BUILD_DIR)/%.cpp $(VERILIB)
	make -C $(BUILD_DIR) -f V$(IMPLEM_NAME).mk $(notdir $@)

simu.a: $(VERILIB) $(SIMU_O)
	cp $< $@
	ar rs $@ $(SIMU_O)

pywheel/%: %
	cp $< $@

wheel: pywheel/simu.a
	cd pywheel && python -m build . -o ..

.PHONY: all

