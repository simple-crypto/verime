//#include "Vtop.h" // From Verilating "top.v"
//#include "Vtop_top.h" // From Verilating "top.v"
//#include "Vtop_andg.h" // From Verilating "top.v"
//#include "verilated.h"

#include "my_funky_lib.h"

void showp(ProbedState * ps) {
    printf("testout_ps0 %08x\n",ps->outp[0][0]);
    printf("testout_ps1 %08x\n",ps->outp[0][1]);
    printf("testout_ps2 %08x\n",ps->outp[0][2]);
    printf("testout_ps3 %08x\n",ps->outp[0][3]);
}

int main(int argc, char** argv) {
    printf("Start main\n");
    SimModel sm = create_new_model();
    // Open file to save
    FILE * fp;
    fp = fopen("test.save","w"); 
    // Create the probed state and link it the the model
    ProbedState state; 
    link_state(sm,&state);
    // Set input 
    Vtop * top = sm.vtop;
    top->a = 0xff; // Set some inputs
    top->b = 0xf0; // Set some inputs
    top->valid_in = 1;
    // Run the simulation
    while (!top->valid_out) {
        sim_clock_cycle(sm);
        write_probed_state(&state,fp);
        printf("\n");
        showp(&state);
    }
    delete_model(sm);
    fclose(fp);
    return 0;
}
