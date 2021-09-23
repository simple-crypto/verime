//#include "Vtop.h" // From Verilating "top.v"
//#include "Vtop_top.h" // From Verilating "top.v"
//#include "Vtop_andg.h" // From Verilating "top.v"
//#include "verilated.h"

#include "my_funky_lib.h"

void show(SimModel sm) {
    Vtop * top = sm.vtop;
    printf("Clk %d\n",top->clk);
    printf("a %d\n",top->a);
    printf("b %d\n",top->b);
    printf("testout %08x\n",get_outp(sm)[0]);
    printf("testout %08x\n",get_outp(sm)[1]);
    printf("testout %08x\n",get_outp(sm)[2]);
    printf("testout %08x\n",get_outp(sm)[3]);
    printf("\n");
}

int main(int argc, char** argv) {
    printf("Start main\n");
    SimModel sm = create_new_model();
    Vtop * top = sm.vtop;
    top->a = 0xff; // Set some inputs
    top->b = 0xf0; // Set some inputs
    top->valid_in = 1;
    while (!top->valid_out) {
        sim_clock_cycle(sm);
        show(sm);
    }
    delete_model(sm);
    return 0;
}
