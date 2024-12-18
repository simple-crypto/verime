# Copyright SIMPLE-Crypto contributors <info@simple-crypto.org>
#
# This file is part of verime <https://github.com/simple-crypto/verime>.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from . import simu
from .simu import json_description
import concurrent.futures
import numpy as np
import json
import itertools as it

_desc = json.loads(json_description())
PROBED_STATE_BYTES = _desc["bytes"]
_list_bytes = list(desc["bytes"] for desc in _desc["sigs"].values())
# SIG_BYTES = list(desc["bytes"] for desc in _desc["sigs"].values())
SIG_BYTES = {
    sig: desc["bytes"] for sig, desc in json.loads(json_description())["sigs"].items()
}
SIGNALS = list(_desc["sigs"].keys())
SIG_BITS = {
    sig: desc["bits"] for sig, desc in json.loads(json_description())["sigs"].items()
}
GENERICS = _desc["GENERIC_TOP"]

## Begin hack section
if "simu_batch" in dir(simu):
    from .simu import simu_batch
else:
    # simu is build as a python module and features a PyBuffer-based API. However,
    # this API is not available in PY_LIMITED_API before 3.11, and we want to
    # support at least 3.10.
    # As a result, we do ctypes-based wrappers here.

    import ctypes

    numpy_ctypeslib_flags = ["C_CONTIGUOUS", "ALIGNED"]

    array_2d_bytes = np.ctypeslib.ndpointer(
        dtype=np.uint8,
        ndim=2,
        flags=numpy_ctypeslib_flags,
    )
    array_3d_bytes = np.ctypeslib.ndpointer(
        dtype=np.uint8,
        ndim=3,
        flags=numpy_ctypeslib_flags,
    )

    simu_raw = np.ctypeslib.load_library(simu.__file__, ".")
    # The commented code below comes from pymod.cpp, we mirror it in python.
    # extern "C" int simulate_execution_buffer_batch(
    #         char * buffer,
    #         size_t buffer_size,
    #         char* data,
    #         size_t data_size,
    #         size_t size_batch,
    #         size_t cycles_alloc
    #         );
    simu_raw.simulate_execution_buffer_batch.argtypes = [
        array_3d_bytes,
        ctypes.c_size_t,
        array_2d_bytes,
        ctypes.c_size_t,
        ctypes.c_size_t,
        ctypes.c_size_t,
    ]
    simu_raw.simulate_execution_buffer_batch.restype = ctypes.c_int
    # extern "C" uint32_t get_probed_state_bytes();
    simu_raw.get_probed_state_bytes.argtypes = []
    simu_raw.get_probed_state_bytes.restype = ctypes.c_uint32

    def simu_batch(probes_buf, indata, /):
        # uint32_t probed_state_bytes = get_probed_state_bytes();
        probed_state_bytes = simu_raw.get_probed_state_bytes()
        assert probes_buf.shape[2] == probed_state_bytes
        # batch_size = states_buf.shape[0];
        batch_size = probes_buf.shape[0]
        # max_n_saves = states_buf.shape[1];
        max_n_saves = probes_buf.shape[1]
        assert indata.shape[0] == batch_size
        # indata_size = indata_buf.shape[1];
        indata_size = indata.shape[1]
        # err = simulate_execution_buffer_batch(
        #         (char *) states_buf.buf,
        #         batch_size * max_n_saves * probed_state_bytes,
        #         (char *) indata_buf.buf,
        #         batch_size * indata_size,
        #         batch_size,
        #         max_n_saves
        #         );
        err = simu_raw.simulate_execution_buffer_batch(
            probes_buf,
            batch_size * max_n_saves * probed_state_bytes,
            indata,
            batch_size * indata_size,
            batch_size,
            max_n_saves,
        )
        assert err == 0


## End hack section


class Simu:
    sig_slices = {
        sig: slice(offset - desc["bytes"], offset)
        for offset, (sig, desc) in zip(
            it.accumulate(_list_bytes), json.loads(json_description())["sigs"].items()
        )
    }

    def __init__(self, indata, max_cycle, nthreads=None):
        self.trace_buff = np.zeros(
            [indata.shape[0], max_cycle, PROBED_STATE_BYTES], dtype=np.uint8
        )
        if nthreads is None:
            simu_batch(self.trace_buff, indata)
        else:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=nthreads
            ) as executor:
                list(
                    executor.map(
                        lambda args: simu_batch(*args),
                        zip(
                            np.array_split(self.trace_buff, nthreads),
                            np.array_split(indata, nthreads),
                        ),
                    )
                )

    def __getitem__(self, idx):
        return self.trace_buff[:, :, self.sig_slices[idx]]
