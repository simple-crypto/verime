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
from .simu import json_description, simu_batch
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
