# Verilator-me (a.k.a. Verime)

In the context of hardware (HW) implementation, side-channel analysis (SCA) usually requires to have access to the value of internal signals of a target circuitry thanks to a so-called circuit oracle. The implementation of the latter  is usually time consuming (e.g., each probed internal value should be modeled and any modification of the original circuitry implies to rewrite the circuit oracle) and/or achieves poor performances. 

The Verime (for Verilator-me) tool is proposed to tackle this issues. In particular, the latter aims to automatically generate a prediction library of 
any arbitrary circuitry described in Verilog. It relies on the Verilator tools in order to achieve competitive simulation performances. More into the details, the computation of the internal states values if perfomed by simulating (behavioral simulation) the circuit during an arbitrary amount of clock cycles thanks to a Verilator backend. Verilator is a powerful tool, but requires some expertise and predicting certain internal states using the `\* verilator public *\` pragma can be challenging and time consuming to setup for a non-experienced user. Based on that, the Verime tools acts as a wrapper and aims to (significantly) reduce the evaluator work: it automatically generates the C++ Verilator backend code and generates a user friendly python package. 

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

## Verime API and detailed usage
This section explain with more details the different function that can be used at the different steps of the flow when using the Verime tool. 

### C++ Wrapper
The simulation wrapper is the only file that need to be written by as user. In particular, the user only needs to implement to function `run_simu` with the following declaration
```c
void run_simu(SimModel *sm, Prober *p, char *data, size_t data_size);
```
The following parameters are used:
* `SimModel *sm`: a Verime specific structure holding the circuit model generated by the Verilator backend. It is typically used to simulate the stimuli at the top-level of the simulated hardware architecture. 
* `Prober *p`: a Verime specific structure used to easily to save the value of the probed (i.e., annotaded) signals at a given simulation time. 
* `char *data`: an array of bytes, provided by the front end as the input case data. These are the data required to perform a simulation. 
* `size_t data_size`: the amount of input bytes provided. 

The definition of the structures `SimModel` and `Prober` depends on the hardware architecture as well as the annotated signals and are automatically generated by Verime. The directive `#include "verime_lib.h"` MUST be used in order to properly include the generated structure in the compilation flow. Putting all together, a typical wrapper template is as follows:
```c
// MUST be included, as is. 
#include "verime_lib.h"

// Define some macros, possibly using the generic value used at the top-level Verilog module
#ifndef FANCYGENERIC
#define FANCYGENERIC GENERIC_P
#endif
...
// The simulation function. Only function that MUST be implemented
void run_simu(SimModel *sm, Prober *p, char* data, size_t data_size) {
   // TODO: implements top-level stimulis to perform an execution with the HW module.
   // The user also has to specify which when the probed signals values are saved.
}
```

To implement the top-level stimuli, the input/output of the core can be accessed through the `SimModel`. In particular `sm->vtop` references to an instance of the top module simulation object generated with Verilator. It follows that `sm->vtop->sig_name = value;` set the value of the hardware top level I/O bus `sig_name`. The exact types of each data bus depends on its practical size, as summarized by the following table

| size (bits) | C++ type |
| --- | --- |
| $`s\leq 8`$ | uint8_t |
| $`8< s \leq 16`$ | uint16_t | 
| $`16< s \leq 32`$ | uint32_t |
| $`32< s \leq 64`$ | uint64_t |
| $`64<s`$ | uint32_t [$`\lceil s/32 \rceil`$]| 

In addition, the following (limited) set of functions are provided when including `verime_lib.h`:
* `sm->vtop->eval()`: evaluates the circuit internal signals values at the current simulation time.
* `sim_clock_cycle(SimModel * sm)`: simulate a posedge clock cycle. E. **Caution:** this function only works for a top module fed with a single clock denoted `clk` at the top level.
* `save_state(Prober * p)`: save the value of the probed signal at the current simulation time.  

Finally, the values of the generics used at the top-level module can be recover in the wrapper. In particular, Verime will define the macro `GENERIC_${PARAM}` for each generic defined at the Verilog top-level (where `PARAM` is the generic name). 

### Python Wrapper

Once installed, the generated library package can be used to simulate the probed internal state value by calling the `Simul` function, as shown next
```python
prediction_lib.Simul(
   cases_inputs,
   am_probed_states
)
```
where `cases_inputs` is a 2D numpy array of bytes (i.e., np.uint8) holds the input byte for each case and `am_probed_states` specifies the maximum amount of time that the probed states will be saved. In practice, each row of `cases_inputs` holds the bytes that will be sent to `run_simu` function in the C++ wrapper for a single execution (i.e., `data` array). The value of `am_probed_states` must be 
at least equal to the amount of time that the function `save_state` is called in the simulation wrapper. 

Consider the following generic template
```python
# Import the generated lib
import generated_verime_lib as plib
# Import numpy, used to generate the input byte for each simulated cases
import numpy as numpy

# Amount of cases to simulate and amount of input bytes per cases
Ncases = 100
Nbytes_per_case = 7

# Generate the input bytes value. In practice, the cases are represented as a
# numpy array where each row contains the input bytes to be used as `data` in
# C++ simulation wrapper.  
cases = np.random.randint(0,256,[Ncases,Nbytes_per_case],dtype=np.uint8)

# Use the Simul function to predict the probed signals values. Here, we assume that no more
# than 100 saving of the probed state will be performed
predictions = plib.Simul(
   cases,
   100
)

# Use the predicted state for the signal "probed_state" for the "cid"-th case. Here, the 
# "sid"-th saving of the simulation is recovered  
useful_state = predictions["probed_state"][cid,sid,:]
... # do some stuff

```

### Cautionary note
clock
