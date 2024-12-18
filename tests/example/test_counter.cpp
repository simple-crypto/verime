#include "verime_lib.h"

// Fetch parameters N from the Verilog generic if no other specified (exported
// as 'GENERIC_${GENERIC_NAME)' at compilation time by Verime)
#ifndef N
#define N GENERIC_N
#endif

// Some generation parameters
#define BYTES_BOUND N / 8

// The C++ Verilator-like wrapper for the top module.
// That is the only mandatory function that a user should write.
// In particular, this function should simulate the top level behavior
// of the top module by generating the top-level stimuli for a single case.
//
// SimModel and Prober are specific Verime structure included with
// the (generated file) 'verime_lib.h'.
//
// The array 'data' is a vector of byte (of length 'data_size') passed from the
// front end python script. It contains the useful data required to performed a
// single simulation with the core (arbitrarily chosen by the user).
//
void run_simu(SimModel *sm, Prober *p, char *data, size_t data_size,
              size_t max_n_cycles) {

  // Data input is (arbitrarily) organised as
  // BYTES_BOUND taking the counter bound value

  // Initialise control signal at the top level
  sm->vtop->start = 0;
  sm->vtop->rst = 0;

  // Reset the top module core
  sm->vtop->rst = 1;
  sim_clock_cycle(sm);
  sm->vtop->rst = 0;
  sim_clock_cycle(sm);

  // Prepare the run with input data
  // Set the cnt_bound value
  memcpy(&sm->vtop->cnt_bound, data, BYTES_BOUND);

  // Start the run
  sm->vtop->start = 1;
  sim_clock_cycle(sm);
  sm->vtop->start = 0;
  sm->vtop->eval();

  // Run until the end of the computation
  for (size_t n_cycles = 0; n_cycles < max_n_cycles; n_cycles++) {
    // Save all the probed values for the current clock cycle.
    save_state(p);
    // Stop if computation is over.
    if (sm->vtop->busy != 1) {
      break;
    }
    // Simulate a single clock cycle
    sim_clock_cycle(sm);
  }
}
