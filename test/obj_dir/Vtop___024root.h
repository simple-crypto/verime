// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtop.h for the primary calling header

#ifndef VERILATED_VTOP___024ROOT_H_
#define VERILATED_VTOP___024ROOT_H_  // guard

#include "verilated.h"

class Vtop__Syms;
class Vtop_top;

VL_MODULE(Vtop___024root) {
  public:
    // CELLS
    Vtop_top* top;

    // DESIGN SPECIFIC STATE
    VL_IN8(clk,0,0);
    VL_IN8(valid_in,0,0);
    VL_IN8(a,7,0);
    VL_IN8(b,7,0);
    VL_OUT8(out,7,0);
    VL_OUT8(valid_out,0,0);
    CData/*0:0*/ __Vclklast__TOP__clk;
    VL_OUT16(tddloop,15,0);
    VL_OUTW(out_bis,127,0,4);

    // INTERNAL VARIABLES
    Vtop__Syms* vlSymsp;  // Symbol table

    // CONSTRUCTORS
    Vtop___024root(const char* name);
    ~Vtop___024root();
    VL_UNCOPYABLE(Vtop___024root);

    // INTERNAL METHODS
    void __Vconfigure(Vtop__Syms* symsp, bool first);
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);


#endif  // guard
