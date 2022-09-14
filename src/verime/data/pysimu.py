from .simu import simu_batch, json_description 
import concurrent.futures
import numpy as np 
import json
import itertools as it

_desc = json.loads(json_description())
PROBED_STATE_BYTES =_desc["bytes"]
_list_bytes = list(desc["bytes"] for desc in _desc["sigs"].values())
#SIG_BYTES = list(desc["bytes"] for desc in _desc["sigs"].values())
SIG_BYTES = {sig: desc["bytes"] for sig, desc in json.loads(json_description())["sigs"].items()}
SIGNALS = list(_desc["sigs"].keys())
SIG_BITS = {sig: desc["bits"] for sig, desc in json.loads(json_description())["sigs"].items()}
GENERICS = _desc["GENERIC_TOP"] 

class Simu:
    sig_slices = {
            sig: slice(offset-desc["bytes"], offset)
            for offset, (sig, desc) in zip(
                it.accumulate(_list_bytes),
                json.loads(json_description())["sigs"].items()
                )
            }

    def __init__(self,indata,max_cycle,nthreads=None):
        self.trace_buff = np.zeros([indata.shape[0],max_cycle,PROBED_STATE_BYTES],dtype=np.uint8)
        if nthreads is None:
            simu_batch(
                    self.trace_buff,
                    indata
                    )
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=nthreads) as executor:
                list(executor.map(
                    lambda args: simu_batch(*args),
                    zip(
                        np.array_split(self.trace_buff, nthreads),
                        np.array_split(indata, nthreads),
                        )
                    ))

    def __getitem__(self, idx):
        return self.trace_buff[:,:,self.sig_slices[idx]]
