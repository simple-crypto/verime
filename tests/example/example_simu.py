#! /bin/env python3 

# Import the library generated
import counter_example_16_lib as plib

# Some usefull package 
import numpy as np
import datetime as dt

### Print the generics used to generate the library
print("List of generic used to compile the library:")
for i,g in enumerate(plib.GENERICS):
    print("({}) '{}':{}".format(i,g,plib.GENERICS[g]))

### Print the names of the signals probed. The practical names of the signals are
### expected to be the ones specified into the Verilog file. However, in the case
### of a generate loop, the duplication of the same signal is avoided by rather
### using the signal SIGNAME__i, where i is the index of the generated instance.
names = plib.SIGNALS 
sigbits = plib.SIG_BITS
sigbytes = plib.SIG_BYTES
print("\nList of signals probed:")
for i,n in enumerate(names):
    print("({}) '{}' ({} bits encoded on {} bytes)".format(i,n,sigbits[n],sigbytes[n]))

### Run some examplary run of predictions
# Fetch the amounf of byte the generate as bound
N = plib.GENERICS["N"]
Nbytes = int(N/8)

# Amount of runs to perform
I = 100

# Set to True to print all verification log
verbose = False

# Generate the inputs of the top level Verilog module. In this examplary case, each
# input case is encoded on N bytes that are used as the bounds of the counter.
# The input is as numpy array of size [Nc,BytesCase] where Nc is the amount of case to simulate
# and BytesCase is the amount of bytes used by a case simulation. In particular, each row of the 
# data is processed by the library such that 'data' and 'data_size' in the C++ wrapper
# correspond to a row array and the length of the latter. 
data_in = np.random.randint(0,256,[I,Nbytes],dtype=np.uint8)

# Use the library to simulate each run.
# In order to simulate, a maximum amount of simulation clock cycles (per simulation case) is provided and used
# by the lib to allocated the buffer used by the 'save_state' function called by the C++ wrapper. 

# Since the counter simulation could take up to 2**N cycles, and we arbitrarily choose
# to allocate a bit more here
MAX_CYCLES = 2**N+5 
dt_start = dt.datetime.now()
predictions = plib.Simu(
        data_in,
        MAX_CYCLES
        )
dt_end = dt.datetime.now()

# The predicted/probed values can then be recovered per signal, per case and per save index. 
# In particular, the returned value is a dictionary with the probed signals names from 
# plib.SIGNALS as keys and 3D numpy array as values. The 3D arrays stored the simulation results 
# obtained from the backend simulation (i.e., the call to the 'save_state' function store the current values
# of each probed signals into this array).
#
# In particular, the value 
#
#       predictions[signame][case_id,save_id,:]
#
# return the value of the signal 'signame' for the case with index 'case_id' and for the 'save_id'-th call
# to the function 'save_state'. In this example, the 'save_state' function is called every clock cycle in the C++
# wrapper, so the 'save_id' is equivalent to the clock cycle index. More fancy save mechanism could be implemented.
# 


# We use the predictions results to verify the good functionality of our core. In particular, we check the value 
# of the internal register 'counter_state' at the end of the simulation (so, once the signal 'busy' is deasserted). 
# The value should be equal to ('counter_bound'+1) % 2**N. Let's check that for each case
print("\nCheck the prediction results for the {} cases:".format(I))
total_cycles = 0
for i in range(I):
    # Compute the value of the bound used for the case
    bound_bytes = data_in[i,:]
    bound_int= sum([e<<(8*i) for i,e in enumerate(bound_bytes)])

    # Compute expected last 'counter_state' value
    exp_last_counter_state = (bound_int + 1) % 2**N

    # Fetch the value of the prediction at clock cycle index 'bound+1'
    last_counter_bytes = predictions['counter_state'][i,bound_int+1,:]
    last_counter_int = sum([e<<(8*i) for i,e in enumerate(last_counter_bytes)])
    
    if verbose:
        # Some printing
        print("#### Case {}".format(i))
        print("Bound value used: {}".format(bound_int))
        print("Expected last counter_state value: {}".format(exp_last_counter_state))
        print("Last counter_state value simulated: {}".format(last_counter_int))
        print("[{} cycles simulated]".format(bound_int+1))
        print("")

    # To keep track of the amount of cycles simulated
    total_cycles += bound_int+1

    # Verifiy value
    assert last_counter_int == (bound_int + 1)%(2**N)

print("All simulated cases where successfully verified!")
print("[{} elapsed ({} pred. cases ; {} clock cycles simulated)]".format(dt_end-dt_start,I,total_cycles))

