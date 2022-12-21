# Verilator-me (a.k.a. Verime)

In the context of hardware (HW) implementation, side-channel analysis (SCA) usually requires to have access to the value of internal signals of a target circuitry thanks to a so-called circuit oracle. The implementation of the latter  is usually time consuming (e.g., each probed internal value should be modeled and any modification of the original circuitry implies to rewrite the circuit oracle) and/or achieves poor performances. 

The Verime (for Verilator-me) tool is proposed to tackle this issues. In particular, the latter aims to automatically generate a prediction library of 
any arbitrary circuitry described in Verilog. It relies on the Verilator tools in order to achieve competitive simulation performances. More into the details, the computation of the internal states values if perfomed by simulating the circuit during an arbitrary amount of clock cycle thanks to a Verilator backend. Verilator is a powerful tool, but requires some expertise and predicting certain internal states using the `\* verilator public *\` pragma can be challenging and time consuming to setup for a non-experienced user. Based on that, the Verime tools acts as a wrapper and aims to (significantly) reduce the evaluator work: it automatically generates the C++ Verilator backend code and generates a user friendly python package. 

In short, the workflow is as follows:
1. Annotate the Verilog source files with the attribute `(\* verilator_me =
   "probed_sig_name" \*)`. Verime will then track the annotaded signals (based on a netlist obtained with Yosys) and generate the
   C++ Verilator code to simulate and keep track of their values during an execution. 
1. Write a C++ simulation wrapper for the top-level module. In practice, this is only required to indicates how your top-level module should be interfaced and how the input data are routed to the later. It is also used to indicate to Verime which cycle to probe (i.e., all, some, ...). The Verime wrapper generate top-level function to ease the integration. More info in the following Sections. 
1. Run the Verime tool to build the python package. The later can then be installed as any other python package with the pip utility.
1. Integrate the package in your custom flow. 


## Dependencies

* [Yosys](https://yosyshq.net/yosys/) (Yosys 0.20 (git sha1 4fcb95ed0, gcc 9.4.0-1ubuntu1~20.04.1 -fPIC -Os) tested)
* [Verilator](https://www.veripool.org/verilator/) (Verilator 4.220 2022-03-12 rev v4.220 tested)
* Python (Python 3.8.10 tested)
* GNU Make (v4.2.1 Built for x86_64-pc-linux-gnu tested)
* bash on Unix system (GNU bash, version 5.0.17(1)-release (x86_64-pc-linux-gnu) on Ubuntu 20.04.3 tested)

In addition, the following package are required

* build.
* python3.8-venv 

## Installation
The Verime tools is written in python3 and should be used as a python3 module. 
The following commands allow to install the Verime tool:
```
python3 -m build
python3 -m pip install dist/*.whl
```
In summary, the first command build the python package of the tool and the second one install the `.whl` file generated. 

## User guide or User To-do list



## Example

The [tests](tests/example) directory contains an example of use for the tool. In particular, the directory [srcs](tests/example/srcs) contains the Verilog file implementing a programmable delay counter (i.e., a module that counts up to an arbitrary value and indicates when it finishes). In particular, the following files can be found:

* [FA1bit.v](tests/example/srcs/FA1bit.v): a 1-bit full adder. 
* [FANbits.v](tests/example/srcs/FANbits.v): a N-bit full adder. 
* [counter.v](tests/example/srcs/counter.v): the top level counter.

These modules are not necessarily optimal and have been coded to explicitly use different coding styles (e.g., generate loop, multiple depth levels, generics and localparam, ... ). For the provided top level, `cnt_bound` is used to specify a delay (in clock cycle), `start` is a control signal used to start a new count and `busy` is asserted when a count is in progress. An execution begins when `start` is asserted (and that `busy` is not). Then, the core will assert `busy` during `cnt_bound`+1 cycles.

### 1. Annotation of the HDL
 In this simple example, we use Verime to probe some internals signals accross the hierarchy of the counter. To do so, we first annotate the internal signals that we want to probe with the `verilator_me` attribute. In particular, we annotate the signals `reg [N-1:0] counter_state` (in [counter.v](tests/example/srcs/counter.v)), `input a` (in [FA1bit.v](tests/example/srcs/FA1bit.v)) and `input b` (in [FA1bit.v](tests/example/srcs/FA1bit.v)) as depicted in the following code snippets

 ```verilog
 ...
 // Register to hold the value
(* verilator_me = "counter_state" *)
reg [N-1:0] counter_state;
wire [N-1:0] counter_nextstate;
...
 ```
 and 
 ```verilog
...
(* verilator_me = "FA1_ina" *)
input a;
(* verilator_me = "FA1_inb" *)
input b;
input cin;
...
 ```
### 2. Implementation of the C++ simulation wrapper
Once the HW design annotated, the file [test_counter.cpp](tests/example/test_counter.cpp) implements the C++ simulation wrapper of the top-level module. For our simple example, the latter only perfoms four basic steps:
1. First, the core is reset
```c
...
// Reset the top module core
sm->vtop->rst = 1;
sim_clock_cycle(sm);
sm->vtop->rst = 0;
sim_clock_cycle(sm);
...
```
1. Then, the programmable delay is fetched from the input buffer and the dedicated input of the core is set accordingly
```c
...
// Prepare the run with input data
// Set the cnt_bound value
memcpy(&sm->vtop->cnt_bound,data,BYTES_BOUND);
...
```
1. Afterwards, a core execution is started
```c
...
// Start the run
sm->vtop->start = 1;
sim_clock_cycle(sm);
sm->vtop->start = 0;
sm->vtop->eval();
...
```
1. Finally, we wait for the end of the execution. While waiting for the counter to reach the configuration, the value of the probed states are saved at every clock cycles. Their values are also saved the cycle after the completion of the counting. 
```c
...
// Run until the end of the computation
while(sm->vtop->busy==1){
   // Save all the probed values for the current clock cycle.
   save_state(p);
   // Simulate a single clock cycle
   sim_clock_cycle(sm);    
}
// Save the probed value once the operation is over
save_state(p);
...
```
### 3. Building the python3 library package. 
It is now time to compile everything together in order to have our 'easy-to-use' python package. To do so, the (simple) [Makefile](tests/example/Makefile) provided is a good example of the procedure to follow. The latter is basically a wrapper for the verime tool. 
For our exmaple, calling `make` under `tests/example` allows to execute the building process. If no problem arises during the later (which should be the case, otherwise please check if you've installed all the required dependencies), a wheel library should be created under the directory named after the `PACK_NAME` variable of the Makefile. 

### 4. Use the front-end generated library package. 
Now that the library has been (automatically) built for our simple design, the file [example_simu.py](tests/example/example_simu.py) demonstrates how the latter can be used to easily simulate the targeted internal values. In particular, it is use in our example to
validate the behavior of our HW module (i.e., by verifying the value of the internal counter after an execution). The following commands (under `tests/example`) can be used to verify that everything went well (here, we rely on a virtual environment which is not stricly required in practice):
```
python3 -m venv ve
source ve/bin/activate # change according to your OS and shell
pip install --upgrade pip
pip install numpy # Required for our test script
pip install counter_example_16_lib/*.whl # default value
python3 example_simu.py
```
At the end, a message similar to the following should be displayed
```
...
Check the prediction results for the 100 cases:
All simulated cases where successfully verified!
[0:00:00.583404 elapsed (100 pred. cases ; 3387683 clock cycles simulated)]
```

## Verime API
### C++ Wrapper

### Python Wrapper
