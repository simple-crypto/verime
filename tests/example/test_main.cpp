#include "verime_lib.h"
#include <stdarg.h>
#include <stdlib.h>
#include <stddef.h>

// Fetch parameters L and W from the Verilog generic if no other specified.
#ifndef L
#define L GENERIC_L
#endif

#ifndef W
#define W GENERIC_W
#endif

// Some generation parameters
#define SIZE_BYTES W/8

struct Prober;
int save_state(Prober *p);

void run_simu(
        SimModel *sm,
        Prober *p,
        char* data,
        size_t data_size
        ) {

    // Data input is (arbitrarily) organised as  
    // 1) 

    // Initialise control signal at the top level
    sm->vtop->in_valid=0;
    sm->vtop->in_seed_valid=0;

    // Reset the AES core
    sm->vtop->rst = 1;
    sim_clock_cycle(sm);
    sm->vtop->rst = 0;
    sim_clock_cycle(sm);

    // Feed the seed
    memcpy(&sm->vtop->in_seed,data,SEED_PRNG_BYTES);
    sm->vtop->in_seed_valid = 1;
    sm->vtop->eval();
    
    while(sm->vtop->in_seed_ready!=1){
        sim_clock_cycle(sm);
    }
    sim_clock_cycle(sm);
    sm->vtop->in_seed_ready = 0;

    // Prepare the run with input data
    // Assign the plaintext with constant sharing
    memcpy(&sm->vtop->in_shares_plaintext,data+SEED_PRNG_BYTES,16); 
    memset(&sm->vtop->in_shares_plaintext+16,0,(D-1)*16);
    // Assign the key 
    memcpy(&sm->vtop->in_shares_key,data+SEED_PRNG_BYTES+16,16*D);

    // Start the run
    sm->vtop->in_valid = 1;
    sm->vtop->eval();
    while(sm->vtop->in_ready!=1){
        sim_clock_cycle(sm);
    }
    sim_clock_cycle(sm);
    sm->vtop->in_valid = 0;
    sm->vtop->eval();

    // Run until the end of the computation
    while(sm->vtop->out_valid!=1){
        save_state(p);
        sim_clock_cycle(sm);    
    }
    save_state(p);
}

