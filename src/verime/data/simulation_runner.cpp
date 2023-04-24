// Copyright SIMPLE-Crypto contributors <info@simple-crypto.org>
// 
// This file is part of verime <https://github.com/simple-crypto/verime>.
// 
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the “Software”), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#include "verime_lib.h"
#include "simulation_runner.h"

// To be defined in the file supplied by the user of verime.
// (stored as simu.cpp in the build directory).
void run_simu(
        SimModel *sm,
        Prober *p,
        char* data,
        size_t data_size
        );

// Similute multiple execution for a ful run and 
// write the probed internal state for each clock cycle 
// in the buffer
extern "C" int simulate_execution_buffer_batch(
        char * buffer,
        size_t buffer_size,
        char* data,
        size_t data_size,
        size_t size_batch,
        size_t cycles_alloc
        ){
    // Create the simulation model
    SimModel * sm = new_model_ptr();
    // Create the probe model
    ProbedState * state = new_probed_state_ptr(); 
    // Link the model
    link_state(sm,state);
    size_t max_n_saves = cycles_alloc;
    size_t data_call_size = data_size / size_batch;

    if (buffer_size < probed_state_bytes * cycles_alloc * size_batch) {
        return 1;
    }

    for (size_t r=0; r<size_batch; r++) {
        Prober p = Prober { buffer + r * max_n_saves * probed_state_bytes, 0, max_n_saves, state };
        run_simu(
                sm,
                &p,
                data + r*data_call_size,
                data_call_size
                );
    }

    // Close stuff
    delete_model_ptr(sm);
    free(state);
    return 0;
}
