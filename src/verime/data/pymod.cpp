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

#define VERIME_PORTABLE

#ifdef VERIME_PORTABLE
#define Py_LIMITED_API 0x03080000 // Build compatible with python3.8
#endif

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Defined in simu.a
extern "C" int simulate_execution_buffer_batch(char *buffer, size_t buffer_size,
                                               char *data, size_t data_size,
                                               size_t size_batch,
                                               size_t cycles_alloc);

// Defined in simu.a
extern "C" const char *dump_json();

// Defined in simu.a
extern "C" uint32_t get_probed_state_bytes();

#define PYMODULE_NAME "$package.simu"
#define PYMODULE_INIT PyInit_simu

#ifdef VERIME_PORTABLE
// Force inclusion of the symbol: since the symbol if from a library, if we
// don't use it, maybe we won't get it.
extern "C" void (*export_simulate_execution_buffer_batch)();
void (*export_simulate_execution_buffer_batch)() =
    (void (*)())&simulate_execution_buffer_batch;
extern "C" uint32_t (*export_get_probed_state_bytes)();
uint32_t (*export_get_probed_state_bytes)() = &get_probed_state_bytes;

#else
static PyObject *simu_batch(PyObject *self, PyObject *args) {
  PyObject *states_obj, *indata_obj;
  Py_buffer states_buf, indata_buf;
  Py_ssize_t batch_size, max_n_saves, indata_size;
  int err = 0;
  uint32_t probed_state_bytes = get_probed_state_bytes();

  if (!PyArg_ParseTuple(args, "OO", &states_obj, &indata_obj))
    return NULL;

  if (PyObject_GetBuffer(states_obj, &states_buf,
                         PyBUF_CONTIG | PyBUF_FORMAT) == -1) {
    return NULL;
  }
  if (states_buf.ndim != 3) {
    PyErr_SetString(PyExc_ValueError, "probes_buf must have three dimensions.");
    err = 1;
    goto free_states;
  }
  if (strcmp(states_buf.format, "B")) {
    PyErr_SetString(PyExc_ValueError, "probes_buf must be an array of bytes.");
    err = 1;
    goto free_states;
  }
  if (states_buf.shape[2] != probed_state_bytes) {
    PyErr_SetString(
        PyExc_ValueError,
        "Third dimension of probes_buf must be probed_state_bytes.");
    err = 1;
    goto free_states;
  }
  batch_size = states_buf.shape[0];
  max_n_saves = states_buf.shape[1];

  if (PyObject_GetBuffer(indata_obj, &indata_buf,
                         PyBUF_CONTIG_RO | PyBUF_FORMAT) == -1) {
    err = 1;
    goto free_states;
  }
  if (indata_buf.ndim != 2) {
    PyErr_SetString(PyExc_ValueError, "indata must have two dimensions");
    err = 1;
    goto free_all;
  }
  if (strcmp(indata_buf.format, "B")) {
    PyErr_SetString(PyExc_ValueError, "indata must be an array of bytes.");
    err = 1;
    goto free_all;
  }
  if (indata_buf.shape[0] != batch_size) {
    PyErr_SetString(PyExc_ValueError,
                    "probes_buf and indata must have equal first dimension.");
    err = 1;
    goto free_all;
  }
  indata_size = indata_buf.shape[1];

  Py_BEGIN_ALLOW_THREADS err = simulate_execution_buffer_batch(
      (char *)states_buf.buf, batch_size * max_n_saves * probed_state_bytes,
      (char *)indata_buf.buf, batch_size * indata_size, batch_size,
      max_n_saves);
  Py_END_ALLOW_THREADS if (err) {
    PyErr_SetString(PyExc_ValueError, "Simulation failed.");
    err = 1;
    goto free_all;
  }

free_all:
  PyBuffer_Release(&indata_buf);
free_states:
  PyBuffer_Release(&states_buf);

  if (err) {
    return NULL;
  } else {
    Py_INCREF(Py_None);
    return Py_None;
  }
}

PyDoc_STRVAR(
    simu_batch_doc,
    "simu_batch(probes_buf, indata, /)\n"
    "--\n"
    "\n"
    "Simulate batch_size times the circuit and store probed wires.\n"
    "Arguments:\n"
    "probes_buf: array-like, (batch_size, np, probed_state_bytes), uint8\n"
    "\tBuffer to store probed values,\n"
    "\tprobed_state_bytes is the space needed to save the probed values.\n"
    "\tnp is the maximum number of times the probes can be saved in an "
    "execution,\n"
    "indata: array-like, (batch_size, indata_length), uint8\n"
    "\tInput data bytes for each execution (indata_length is arbitrary).");
#endif // VERIME_PORTABLE

static PyObject *json_description(PyObject *self, PyObject *args) {
  return Py_BuildValue("s", dump_json());
}

static PyMethodDef methods[] = {
#ifndef VERIME_PORTABLE
    {"simu_batch", simu_batch, METH_VARARGS, simu_batch_doc},
#endif // VERIME_PORTABLE
    {"json_description", json_description, METH_VARARGS,
     "JSON description of the simulated code."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef pymodule = {
    PyModuleDef_HEAD_INIT, PYMODULE_NAME, /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,   /* size of per-interpreter state of the module,
             or -1 if the module keeps state in global variables. */
    methods};

PyMODINIT_FUNC PYMODULE_INIT(void) { return PyModule_Create(&pymodule); }
