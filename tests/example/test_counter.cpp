#include "verime_lib.h"
#include <stdarg.h>
#include <stdlib.h>
#include <stddef.h>

// Fetch parameters N from the Verilog generic (exported as GENERIC_*) if no other specified.
#ifndef N
#define N GENERIC_N
#endif

// Some generation parameters
#define BYTES_BOUND N/8

struct Prober;
int save_state(Prober *p);

void run_simu(
        SimModel *sm,
        Prober *p,
        char* data,
        size_t data_size
        ) {

    // Data input is (arbitrarily) organised as  
    // 1 byte taking the counter bound value 

    // Initialise control signal at the top level
    sm->vtop->start=0;
    sm->vtop->rst=0;

    // Reset the top module core
    sm->vtop->rst = 1;
    sim_clock_cycle(sm);
    sm->vtop->rst = 0;
    sim_clock_cycle(sm);

    // Prepare the run with input data
    // Set the cnt_bound value
    memcpy(&sm->vtop->cnt_bound,data,BYTES_BOUND);

    // Start the run
    sm->vtop->start = 1;
    sim_clock_cycle(sm);
    sm->vtop->start = 0;
    sm->vtop->eval();

    // Run until the end of the computation
    while(sm->vtop->busy==1){
        // Save all the probed values
        save_state(p);
        // Simulate a single clock cycle
        sim_clock_cycle(sm);    
    }
    // Save the probed value once the operation is over
    save_state(p);
}

