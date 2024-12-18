# Verime

In the context of the side-channel analysis of hardware implementations, an evaluator usually requires to have access to the internal values of a target circuitry. For this purpose, a circuit oracle simulating these values is implemented, which may turn out to be time consuming to do manually (e.g., each probed internal value should be modeled and any modification of the original circuitry implies to rewrite the circuit oracle) and/or achieve poor performances (e.g., spawning a simulator process for each simulation).

The Verime tool is proposed to tackle these issues. In particular, it automatically generates a prediction library of a circuit (described in Verilog). More precisely, it performs behavioral verilog simulations during an arbitrary amount of clock cycles thanks to a Verilator backend. Verilator is a powerful tool, but requires some expertise and predicting certain internal states using the `\* verilator public *\` pragma can be challenging and time consuming to setup for a non-experienced user. Based on that, the Verime tools acts as a wrapper for verilator and aims to (significantly) reduce the evaluator work: it automatically generates the C++ Verilator backend code and generates a user friendly python package thant can be easily integrated and used.

The advantages over "raw" Verilator usage are:

- Easy integration with python: no bindings to write.
- Nultiple simulations in a single process, that can even run in parallel, achieving excellent performance (no process startup overhead).
- No need to handle complicated Verilator model interface to probe the value of wires.

In short, the workflow is as follows:

1. Annotate the targeted signal in the Verilog source(s) file(s) with the attribute `(* verime = "probed_sig_name" *)`.
1. Write a C++ simple simulation wrapper for the top-level module that indicates:
    - How the top-level module should be interfaced and how the input data is routed.
    - When the probed signals values should be stored (e.g., all clock cycles or some specific ones).
1. Run the Verime tool to build a python package (wheel) and install it as any other python package with pip.
1. Use the simulation package in python scirpts.

## Dependencies

In addition to Python (`>= 3.11`), Verime has the following native dependencies:

- [Yosys](https://yosyshq.net/yosys/) (versions 0.20 and 0.23 known to work)
- [Verilator](https://www.veripool.org/verilator/) (version 5.006 known to work)
- GNU Make

**CAUTION: Verilator dependency**:

- If a recent-enough version is available, we recommand to install Verilator using the packet manager of your OS.
- If you build from [source](https://github.com/verilator/verilator), we
  **highly recommend** using an in-place version of Verilator, as recommended
  in the official
  [documentation](https://veripool.org/guide/latest/install.html#run-in-place-from-verilator-root).
  Then, set the `VERILATOR_ROOT` environmnent variable appropriately (no `PATH`
  modification needed).
  Some versions of Verilator are known to not behave correctly when installed with `make install`.

## Installation

```
python3 -m pip install verime
```

You can also build it locally (it is a pure-python package).

## Usage example

This section demonstrates how Verime can be used for a simple example provided under the [tests](tests/example) directory. In particular, the later contains the Verilog file implementing a programmable delay counter (i.e., a module that counts up to an arbitrary value and indicates when it finishes). In particular, the following files can be found:

- [FA1bit.v](tests/example/srcs/FA1bit.v): a 1-bit full adder.
- [FANbits.v](tests/example/srcs/FANbits.v): a N-bit full adder.
- [counter.v](tests/example/srcs/counter.v): the top level counter.

These modules have been coded to use different coding styles (e.g., generate loop, multiple depth levels, generics and localparam, ... ). For the provided top level, `cnt_bound` is used to specify a delay (in terms of clock cycles), `start` is a control signal used to start a new count and `busy` is asserted when a count is in progress. An execution begins when `start` is asserted (and that `busy` is not). Then, the core will assert `busy` during `cnt_bound`+1 cycles.

### 1. Annotation of the HDL

 In this simple example, we use Verime to probe some internals signals accross the hierarchy of the counter. To do so, we first annotate the internal signals that we want to probe with the `verime` attribute. In particular, we annotate the signals `reg [N-1:0] counter_state` (in [counter.v](tests/example/srcs/counter.v)), `input a` (in [FA1bit.v](tests/example/srcs/FA1bit.v)) and `input b` (in [FA1bit.v](tests/example/srcs/FA1bit.v)) as depicted in the following code snippets

 ```verilog
 ...
 // Register to hold the value
(* verime = "counter_state" *)
reg [N-1:0] counter_state;
wire [N-1:0] counter_nextstate;
...
 ```

 and

 ```verilog
...
(* verime = "FA1_ina" *)
input a;
(* verime = "FA1_inb" *)
input b;
input cin;
...
 ```

### 2. Implementation of the C++ simulation wrapper

Once the HW design annotated, the file [test_counter.cpp](tests/example/test_counter.cpp) implements the C++ simulation wrapper of the top-level module.
This code follows the structure:

```c
// MUST be included, as is. 
#include "verime_lib.h"

// The simulation function. Only function that MUST be implemented
void run_simu(SimModel *sm, Prober *p, char* data, size_t data_size) {
   // See below for the content of this function.
}
```

For our simple example, the `run_simu` function only perfoms four basic steps:

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

2. Then, the programmable delay is fetched from the input buffer and the dedicated input bus of the core is set accordingly

```c
...
// Prepare the run with input data
// Set the cnt_bound value
memcpy(&sm->vtop->cnt_bound,data,BYTES_BOUND);
...
```

Where `BYTES_BOUND` is a macro derived from `GENERIC_N`, which is defined by
Verime as the value of the `N` generic parameter of the top-level module.
3. Afterwards, a core execution is started

```c
...
// Start the run
sm->vtop->start = 1;
sim_clock_cycle(sm);
sm->vtop->start = 0;
sm->vtop->eval();
...
```

4. Finally, we wait for the end of the execution. While waiting for the counter to reach the configuration, the value of the probed states are saved at every clock cycles. Their values are also saved the cycle after the completion of the counting process.

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

### 3. Building the python3 library package

It is now time to compile everything together in order to have our 'easy-to-use' simulation python package.
This is done in two steps: first generate the source files for the package using Verime, then running `make` with the generated `Makefile`.

The example [Makefile](tests/example/Makefile) follows this procedure to follow, you can simply run `make` in `tests/example`.
If the build is successful (otherwise check if you have installed all the required dependencies in correct versions), a wheel package should be created under the directory named after the `PACK_NAME` variable of the Makefile.

### 4. Use the simulation python package

Now that the package has been built for our simple design, the file [example_simu.py](tests/example/example_simu.py) demonstrates how the it can be used. In the example, we use it to validate the (functional) behavior of our HW module (i.e., by verifying the value of the internal counter after an execution). The following commands (under `tests/example`) can be used to verify that everything went well (here, we rely on a virtual environment which is recommanded but not stricly required):

```bash
python3 -m venv ve
source ve/bin/activate # change according to your OS and shell
pip install --upgrade pip
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

This section explains with more details the functions and parameters that can be used at the different steps of the flow when using the Verime tool.

### C++ Wrapper

The simulation wrapper is the only file that need to be written by as user. In in this file, the user only needs to implement to function `run_simu`:

```c
void run_simu(SimModel *sm, Prober *p, char *data, size_t data_size);
```

The following parameters are used:
- `SimModel *sm`: A Verime-specific structure holding the circuit model generated by the Verilator backend. It is typically used to simulate the stimuli at the top-level of the simulated hardware architecture.
- `Prober *p`: A Verime-specific structure used to easily to save the value of the probed (i.e., annotaded) signals at a given simulation time.
- `char *data`: An array of bytes, provided to the python API as the input data of a single simulation. These are the data required to perform a simulation.
- `size_t data_size`: The length of the `data` array.

The definitions of the structures `SimModel` and `Prober` depend on the hardware architecture as well as the annotated signals and are automatically generated by Verime. The directive `#include "verime_lib.h"` **must** be used in order to properly include the generated library code in the compilation flow. Besides, the Verilog top-level generic values can be recovered in the wrapper: Verime will define the macro `GENERIC_${PARAM}` for each generic defined at the Verilog top-level (where `PARAM` is the generic name).

To implement the top-level stimuli, the input/output of the core can be accessed through the `SimModel`. In particular `sm->vtop` references to an instance of the top module simulation object generated with Verilator. As an example, the statement `sm->vtop->sig_name = value;` can be used to set the value of the hardware top level I/O bus `sig_name`. The exact types of each data bus depends on its practical size, as summarized by the following table

| size $`s`$ (bits) | C++ type |
| --- | --- |
| $`s\leq 8`$ | `uint8_t` |
| $`8< s \leq 16`$ | `uint16_t` |
| $`16< s \leq 32`$ | `uint32_t` |
| $`32< s \leq 64`$ | `uint64_t` |
| $`64<s`$ | `uint32_t` [$`\lceil s/32 \rceil`$]|

In addition, the following functions are provided when including `verime_lib.h`:
- `sim_clock_cycle(SimModel * sm)`: simulates a posedge clock cycle. This function only works for a design that is synchronous to the positive edge of a top-level input clock.
- `save_state(Prober * p)`: save the value of the probed signal at the current simulation time.  
- `sm->vtop->eval()`: evaluates the circuit internal signals values at the current simulation time. This is a call to the `eval()` function of the generated Verilator object. This function should be used only if you cannot use `sim_clock_cycle`.

### Verime usage

The verime tool is used to build the front-end python package based on the HDL Verilog source and the C++ simulation wrapper. As shown by the tool helper, several parameter can be used.  

```
verime -h
usage: verime [-h] [-y YDIR [YDIR ...]] [-g GENERICS [GENERICS ...]] -t TOP [--yosys-exec YOSYS_EXEC] --pack PACK --simu SIMU [--build-dir BUILD_DIR] [--clock CLOCK]

options:
  -h, --help            show this help message and exit
  -y YDIR [YDIR ...], --ydir YDIR [YDIR ...]
                        Directory for the module search. (default: [])
  -g GENERICS [GENERICS ...], --generics GENERICS [GENERICS ...]
                        Verilog generic value, as -g<Id>=<Value>. (default: None)
  -t TOP, --top TOP     Path to the top module file, e.g. /home/user/top.v. (default: None)
  --yosys-exec YOSYS_EXEC
                        Yosys executable. (default: yosys)
  --pack PACK           The Verilator-me package name. (default: None)
  --simu SIMU           Path to the C++ file defining run_simu (default: None)
  --build-dir BUILD_DIR
                        The build directory. (default: .)
  --clock CLOCK         The clock signal to use. (default: clk)
```

The only required parameters are `-t`, `--pack` and `--simu`.

### Python Library

Once installed, the simulation library package can be used to simulate the probed internal state value by creating a `Simu` object, as shown next

```python
import generated_verime_lib as prediction_lib
...
predictions = prediction_lib.Simu(
   cases_inputs,
   am_probed_states
)
```

where `cases_inputs` is a 2D numpy array of bytes (i.e., `np.uint8`) that holds the input bytes for each simulation (each row will be used as the `data` argument of `run_simu` in the C++ code) and `am_probed_states` specifies the maximum amount of time that the probed states will be saved (i.e., the number of calls to `save_state` in `run_simu`).

The `Simu` object can be index with keys which are the Verime probed signals names, returning the corresponding simulation results. These are 3D numpy arrays, where the first dimension is the simulation index, the second dimension is the saving index (i.e., result of the i-th call to `save_state()` in `run_simu()`) and the third dimension is the byte index of the probed signal value. Putting all together, the following code snippet represents a generic template for the usage of the generated prediction library.

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

# Use Simu to predict the probed signals values. Here, we assume that no more
# than 100 saving of the probed state will be performed
predictions = plib.Simu(
   cases,
   100
)

# Use the predicted state for the signal "probed_state" for the "cid"-th case. Here, the 
# "sid"-th saving of the simulation is recovered  
useful_state = predictions["probed_state"][cid,sid,:]
... # do some stuff
```

Finally, some metadata are embedded in the library package and can be easily accessed for further usage. These are summarized here (use `help($VERIME_LIB)` to get detailled information):

| field | data |
| --- | --- |
| `GENERICS` | A dictionary holding the value of the Verilog top-level generics used. |
| `PROBED_STATE_BYTES` | Amount of bytes required to encode all the probed internal state values |
| `SIGNALS` | List containing the names of the signal generated by Verime |
| `SIG_BITS` | A dictionary holding the width (in bits) for each probed signals |
| `SIG_BYTES` | A dictionary holding the amount of bytes used to encode each probe signals |

#### Parallelization

The generated simulation library releases the python global interpreter lock
(GIL) when running the simulations, hence simulations can be parallelized on
multi-core CPUs using python's thread-based concurrency such as
`concurrent.futures.ThreadPoolExecutor`.
