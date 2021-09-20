// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtop.h for the primary calling header

#ifndef VERILATED_VTOP_ANDG_H_
#define VERILATED_VTOP_ANDG_H_  // guard

#include "verilated.h"

class Vtop__Syms;
VL_MODULE(Vtop_andg) {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(__PVT__a,7,0);
    VL_IN8(__PVT__b,7,0);
    VL_OUT8(__PVT__out,7,0);
    CData/*7:0*/ tmp;

    // INTERNAL VARIABLES
    Vtop__Syms* vlSymsp;  // Symbol table

    // CONSTRUCTORS
    Vtop_andg(const char* name);
    ~Vtop_andg();
    VL_UNCOPYABLE(Vtop_andg);

    // INTERNAL METHODS
    void __Vconfigure(Vtop__Syms* symsp, bool first);
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);


#endif  // guard
