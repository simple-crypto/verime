# verilator-me

Tool to ease the generation of oracle for HW circuit analysis.

The tool automatically generates a C++ library with top level function to access the signals specified by the user in the Verilog code.
The goal of the tool is to ease the prbing of specific signals values inside a complex HW architecture. 

In short, the workflow works as follows:
1. Annotate the Verilog source files with the attribute (\* verilator\_me =
   "sig\_name" \*). Each annotated signals will then be used in the library
   generation.
1. Run the verilator-me tool to generate the top level library to be used with
   Verilator.
1. Write the main function to be used by the Verilator compilation. For this
   function, the user should specify the input/output behavior of the HW module
   considered. For this, he can directly set the value of the input and use the
   top level functions provided by the generated library.  
1. Compile the design with Verilator and run the built executable.


## Dependencies

Test 
