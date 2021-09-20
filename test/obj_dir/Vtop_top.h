// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtop.h for the primary calling header

#ifndef VERILATED_VTOP_TOP_H_
#define VERILATED_VTOP_TOP_H_  // guard

#include "verilated.h"

class Vtop__Syms;
class Vtop_andg;

VL_MODULE(Vtop_top) {
  public:
    // CELLS
    Vtop_andg* dut;

    // DESIGN SPECIFIC STATE
    VL_IN8(clk,0,0);
    VL_IN8(valid_in,0,0);
    VL_IN8(a,7,0);
    VL_IN8(b,7,0);
    VL_OUT8(out,7,0);
    VL_OUT8(valid_out,0,0);
    CData/*0:0*/ li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp;
    CData/*0:0*/ li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp;
    CData/*0:0*/ li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp;
    CData/*0:0*/ li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp;
    CData/*0:0*/ li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp;
    CData/*0:0*/ li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp;
    CData/*0:0*/ li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp;
    CData/*0:0*/ li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp;
    CData/*0:0*/ li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp;
    CData/*0:0*/ li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp;
    CData/*0:0*/ li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp;
    CData/*0:0*/ li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp;
    CData/*0:0*/ li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp;
    CData/*0:0*/ li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp;
    CData/*0:0*/ li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp;
    CData/*0:0*/ li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp;
    VL_OUT16(tddloop,15,0);
    VL_OUTW(__PVT__out_bis,127,0,4);
    IData/*16:0*/ pipe_level__BRA__0__KET____DOT__in;
    IData/*16:0*/ __PVT__pipe_level__BRA__0__KET____DOT__regin;
    IData/*16:0*/ pipe_level__BRA__1__KET____DOT__in;
    IData/*16:0*/ __PVT__pipe_level__BRA__1__KET____DOT__regin;
    IData/*16:0*/ pipe_level__BRA__2__KET____DOT__in;
    IData/*16:0*/ __PVT__pipe_level__BRA__2__KET____DOT__regin;

    // INTERNAL VARIABLES
    Vtop__Syms* vlSymsp;  // Symbol table

    // CONSTRUCTORS
    Vtop_top(const char* name);
    ~Vtop_top();
    VL_UNCOPYABLE(Vtop_top);

    // INTERNAL METHODS
    void __Vconfigure(Vtop__Syms* symsp, bool first);
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);


#endif  // guard
