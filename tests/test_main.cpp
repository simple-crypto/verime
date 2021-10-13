#include "my_funky_lib.h"

int main(int argc, char** argv) {
    // Create Simulation model
    SimModel * sm = new_model_ptr();

    // Create the probed state and link it the the model.
    ProbedState * state = new_probed_state_ptr(); 
    link_state(sm,state);

    // Open file to save
    FILE * fp;
    fp = fopen("test.save","w"); 

    // Set input 
    Vtop * top = sm->vtop;
    top->a = 0xff; // Set some inputs
    top->b = 0xf0; // Set some inputs
    top->valid_in = 1;

    // Run the simulation
    int cc = 0;
    while (!top->valid_out) {
        printf("Run clock cycle %d\n",cc);
        sim_clock_cycle(sm);
        write_probed_state(state,fp);
        cc++;
    }

    // Close all
    fclose(fp);
    return 0;
}
