# verilator-me

In the context of hardware (HW) implementation, side-channel analysis (SCA) usually requires to have access to the value of internal signals of a target circuitry thanks to a so-called circuit oracle. The implementation of the latter  is usually time consuming (e.g., each probed internal value should be modeled and any modification of the original circuitry implies to rewrite the circuit oracle) and/or achieves poor performances. 

The Verime (for Verilator-me) tool is proposed to tackle this issues. In particular, the latter aims to automatically generate a prediction library of 
any arbitrary circuitry described in Verilog. It relies on the Verilator tools in order to achieve competitive simulation performances. More into the details, the computation of the internal states values if perfomed by simulating the circuit during an arbitrary amount of clock cycle thanks to a Verilator backend. Verilator is a powerful tool, but requires some expertise and predicting certain internal states using the `\* verilator public *\` pragma can be challenging and time consuming to setup for a non-experienced user. Based on that, the Verime tools acts as a wrapper and aims to (significantly) reduce the evaluator work: it automatically generates the C++ Verilator backend code and generates a user friendly python package. 

In short, the workflow is as follows:
1. Annotate the Verilog source files with the attribute (\* verilator\_me =
   "sig\_name" \*). Verime will then track the annotaded signals (based on a netlist obtained with Yosys) and generate the
   C++ Verilator code to simulate and keep track of their values during an execution. 
1. Write a C++ simulation wrapper for the top-level module. In practice, this is only required to indicates how your top-level module should be interfaced and how the input data are routed to the later. It is also used to indicate to Verime which cycle to probe (i.e., all, some, ...). The Verime wrapper generate top-level function to ease the integration. More info in the following Sections. 
1. Run the Verime tool to build the python package. The later can then be installed as any other python package with the pip utility.
1. Integrate the package in your custom flow. 


## Dependencies

* [Yosys](http://www.clifford.at/yosys/) (Yosys 0.20 (git sha1 4fcb95ed0, gcc 9.4.0-1ubuntu1~20.04.1 -fPIC -Os) tested)
* [Verilator](https://www.veripool.org/verilator/) (Verilator 4.220 2022-03-12 rev v4.220 tested)
* Python (Python 3.8.10 tested)
* GNU Make (v4.2.1 Built for x86_64-pc-linux-gnu tested)
* bash on Unix system (GNU bash, version 5.0.17(1)-release (x86_64-pc-linux-gnu) on Ubuntu 20.04.3 tested)

Currently, the package is not on Pypi and the user should install the following
tool in order to build and install Verilator-me.

* 'build' python packet.
* python3.8-venv 

## Installation
The Verime tools is written in python3 and can should be used as a python3 module. 
The following commands allow to install the Verime tool:

TODO
## Examplary run

The [test](test/) directory contains an example of use for the tool. The
exemplary HW circuit considered (under [test/src](https://git-crypto.elen.ucl.ac.be/cmomin/verilator-me/-/tree/README/test/srcs)) does not implement a particular functionality,
but tries to represent different Verilog coding styles such as bus handling,
generate and imbricated generate blocks or instanciation of submodules. Once in the [test](test/) directory, one may run 
```
make 
```
to run all the steps described below. 

Some signals in the architecture are annotaded with the *verilator\_me* attribute. These are the one
we would like to probe during a simulation of the circuit. The tool will look for such signals in the architecture 
and produce the high-level library code to easily probe these. The attribute annotation is of the form 
```
(* verilator_me = "verime_signal_name")
```
Where *verime\_signal\_name* is the name that will be used in the generated libraries to refer to the annotated signal.
For the test example, the library can be generate by running
```
python3 -m verime.verilator_me -y srcs -top srcs/top.v --pack my_funky_lib
```
This command creates a package for the top module defined in './srcs/top.v', specifying to look for Verilog modules in the directory './srcs'. The package created will be located at './my\_funky\_lib'. The building mecanism will first elaborate the HW design using the Yosys tool and create a .json file containing the architecture as well as the attributes of each signals. Based on this .json file, the tool builds the architecture path of each signal that the user aims to probe and creates the C++ library. The package created has the following architecture:

+ package_name/
   + hw-src/
      + *.v
   + sw-src/
      + package_name.h
      + package_name.cpp
   + config-verilator-me.json
   + config-dump.json

The *hw-src/* directory contains the HW sources files annotated as required for the Verilator compilation. The files *sw-src/package_name.h* and *sw-src/package_name.cpp* are respectively the declaration and the definition of the automatically generated functions. The *config-verilator-me.json* file contains the parameters used during the package creation that are required by the Verilator compilation (such as the values of the generics used for the top level module). Finally, the *config-dump.json* file contains the architecture of the data written by the auto-generated *write_probed_state* function (see next).

Once the library is built, the user should write the main function that will be used during the Verilator compilation. In the case case provided, the following function definition is provided in the file [test/test\_main.cpp](https://git-crypto.elen.ucl.ac.be/cmomin/verilator-me/-/blob/README/test/test_main.cpp):
```
#include "my_funky_lib.h"

int main(int argc, char** argv) {
    // Create Simulation model
    SimModel sm = create_new_model();

    // Create the probed state and link it the the model.
    ProbedState state; 
    link_state(sm,&state);

    // Open file to save
    FILE * fp;
    fp = fopen("test.save","w"); 

    // Set input 
    Vtop * top = sm.vtop;
    top->a = 0xff; // Set some inputs
    top->b = 0xf0; // Set some inputs
    top->valid_in = 1;

    // Run the simulation
    int cc = 0;
    while (!top->valid_out) {
        printf("Run clock cycle %d\n",cc);
        sim_clock_cycle(sm);
        write_probed_state(&state,fp);
        cc++;
    }

    // Close all
    delete_model(sm);
    fclose(fp);
    return 0;
}
```
Next are detailled the different steps in the main function definition.
+ The first step is to create the simulation model using the *create\_new\_model()* call. This call returns a specific structure containing a pointer to a VerilatedContext object (used by Verilator) as well as a pointer refering to an instance of the primary model header generated by Verilator for the HW sources provided in the specified verilator-me package (i.e., the *hw-src/* directory).
+ The second step is to create an instance of ProbedState, which is an automatically generated structure containing a pointer to the value of each of the probed signals. The call to the *link_state* function set the values of the ProbeState field to the actual reference in the Verilated modules.
+ Next, a file pointer is created in order to save the probed values.
+ Before running the simulation, the inputs values are set using the primary model header generated in the SimModel creation.
+ The simulation is run. Here, the calls to the *sim\_clock\_cycle* is used to evaluate the values across the hierarchy during a clock cycle. During each clock cycle, the value of each probed state are written sequentially in the save file by calling the *write_probed_state* function.
+ Finally, the used ressources are closed.

Finally, once the main function is defined, the user can compile any C++ code together with a package generated with verilator-me.
For the test example, this can be done with the following command
```
python3 -m verime.verilator_me --pack my_funky_lib -cpp test_main.cpp --exec my_funky_exec
```
where the argument 
+ **--pack** defines the package to use during the compilation.
+ **-cpp** defines a C++ file to add during the compilation (can be used multiple times).
+ **--exec** defines the path where the executable will be built. 

In more details, specifying a C++ file will run the verilator-me in the compilation mode. That is, is will take as input C++ files and Verilator-me packages to compile everything with Verilator in order to build a final executable. Finally, it has to be noted that the tool allows a user to tunes other parameters such as the workspaces of Verilator or Verilator-me. All the differents parameters can be found by running the following command
```
python3 -m verime.verilator_me --help
```

## File format

The configuration file generated (i.e., *config-verilator-me.json* and *config-dump.json*) are saved using the JSON format. The architecture of the *config-dump.json* file is of a particular interest, since it describes the way a call to the *write_probed_state* function is writting the value on the specified stream. In particular, each call is writting the ProbedState structure as a bytes stream, where all the words are written in little endian (byte per byte) consecutively. Taking this into consideration, the JSON file *config-dump.json* has the following architecture:

+ config-dump.json
   + **'bytes'**: Total amount of bytes in the probed state. 
   + **'sigs'**: 
      + **'verime_signal_name'**: 
         + **'bytes'**: The amount of bytes used by the signal in the saving file.
         + **'bits'**: the amount of valid bits in the saved data.


Put in an other way, every call to the *write_probed_state* function is writting *config-dump.json['bytes']* bytes to the specified stream following the architecture defined in *config-dump.json['sigs']*, where the signal order is following the order in the JSON file. An examplary code to parse the generated dump file can be found in the file [verime-utils.py](https://git-crypto.elen.ucl.ac.be/cmomin/verilator-me/-/blob/main/verime-utils.py).
