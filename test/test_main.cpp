//#include "Vtop.h" // From Verilating "top.v"
//#include "Vtop_top.h" // From Verilating "top.v"
//#include "Vtop_andg.h" // From Verilating "top.v"
//#include "verilated.h"

#include "testlib.h"

void show(SimModel sm) {
    Vtop * top = sm.vtop;
    printf("Clk %d\n",top->clk);
    printf("a %d\n",top->a);
    printf("b %d\n",top->b);
    printf("out %d\n",top->out);
    printf("out_bis %x %x %x\n",top->out_bis[0],top->out_bis[1],0);
    printf("vout %d\n",top->valid_out);
    printf("tout %x\n",top->tddloop);
    printf("test %d\n",top->top->pipe_level__BRA__0__KET____DOT__in);
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
