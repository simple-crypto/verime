// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "verilated.h"
#include "verilated_dpi.h"

#include "Vtop__Syms.h"
#include "Vtop_andg.h"

void Vtop_andg___ctor_var_reset(Vtop_andg* vlSelf);

Vtop_andg::Vtop_andg(const char* _vcname__)
    : VerilatedModule(_vcname__)
 {
    // Reset structure values
    Vtop_andg___ctor_var_reset(this);
}

void Vtop_andg::__Vconfigure(Vtop__Syms* _vlSymsp, bool first) {
    if (false && first) {}  // Prevent unused
    this->vlSymsp = _vlSymsp;
}

Vtop_andg::~Vtop_andg() {
}
