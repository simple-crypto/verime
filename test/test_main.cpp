//#include "Vtop.h" // From Verilating "top.v"
//#include "Vtop_top.h" // From Verilating "top.v"
//#include "Vtop_andg.h" // From Verilating "top.v"
//#include "verilated.h"

#include "mylib.h"

vluint64_t main_time = 0; // Current simulation time
// This is a 64-bit integer to reduce wrap over issues and
// allow modulus. This is in units of the timeprecision
// used in Verilog (or from --timescale-override)
double sc_time_stamp() { // Called by $time in Verilog
    return main_time; // converts to double, to match
    // what SystemC does
}
int main(int argc, char** argv) {
    printf("Start main\n");
    SimModel sm = create_new_model();
    Vtop * top = sm.vtop;
    top->a = 0xff; // Set some inputs
    top->b = 0xf0; // Set some inputs
    top->valid_in = 1;
    while (!top->valid_out) {
        if ((main_time % 2) == 0) {
            top->clk = 0; // Toggle clock
        }
        if ((main_time % 2) == 1) {
            top->clk = 1;
        }
        top->eval(); // Evaluate model
        printf("Clk %d\n",top->clk);
        printf("a %d\n",top->a);
        printf("b %d\n",top->b);
        printf("out %d\n",top->out);
        printf("out_bis %x %x %x\n",top->out_bis[0],top->out_bis[1],0);
        printf("vout %d\n",top->valid_out);
        printf("tout %x\n",top->tddloop);
        printf("test %d\n",top->top->pipe_level__BRA__0__KET____DOT__in);
        printf("\n");
        //cout << top->out << endl; // Read a output
        main_time++; // Time passes...
    }
    top->final();
    delete_model(sm);
    return 0;
}
