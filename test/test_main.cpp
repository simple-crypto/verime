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
    printf("testout0 %08x\n",get_outp(sm)[0]);
    printf("testout1 %08x\n",get_outp(sm)[1]);
    printf("testout2 %08x\n",get_outp(sm)[2]);
    printf("testout3 %08x\n",get_outp(sm)[3]);
    printf("\n");
}

void show_outbis_ptr(SimModel sm) {
    printf("Pointer Ref: %08x\n",sm.vtop->top->out_bis);
}

void show_ps_ptr(ProbedState * ps){
    printf("Pointer Ps: %08x\n",ps->outp[0]);
}

void showp(ProbedState * ps) {
    printf("testout_ps0 %08x\n",ps->outp[0][0]);
    printf("testout_ps1 %08x\n",ps->outp[0][1]);
    printf("testout_ps2 %08x\n",ps->outp[0][2]);
    printf("testout_ps3 %08x\n",ps->outp[0][3]);
}

int main(int argc, char** argv) {
    printf("Start main\n");
    SimModel sm = create_new_model();
    // Create the probed state and link it the the model
    ProbedState state; 
    link_state(sm,&state);
    Vtop * top = sm.vtop;
    top->a = 0xff; // Set some inputs
    top->b = 0xf0; // Set some inputs
    top->valid_in = 1;
    while (!top->valid_out) {
        sim_clock_cycle(sm);
        show(sm);
        printf("\n");
        show_outbis_ptr(sm);
        showp(&state);
        show_ps_ptr(&state);
    }
    delete_model(sm);
    return 0;
}
