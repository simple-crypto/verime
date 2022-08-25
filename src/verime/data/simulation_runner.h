#ifndef SIMULATION_RUNNER_H_
#define SIMULATION_RUNNER_H_

#include <stddef.h>


extern "C" int simulate_execution_buffer_batch(
        char * buffer,
        size_t buffer_size,
        char* data,
        size_t data_size,
        size_t size_batch,
        size_t cycles_alloc
        );

#endif //SIMULATION_RUNNER_H_
