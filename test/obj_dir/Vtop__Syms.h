// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VTOP__SYMS_H_
#define VERILATED_VTOP__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vtop.h"

// INCLUDE MODULE CLASSES
#include "Vtop___024root.h"
#include "Vtop_top.h"
#include "Vtop_andg.h"

// DPI TYPES for DPI Export callbacks (Internal use)

// SYMS CLASS (contains all model state)
class Vtop__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vtop* const __Vm_modelp;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vtop___024root                 TOP;
    Vtop_top                       TOP__top;
    Vtop_andg                      TOP__top__dut;

    // SCOPE NAMES
    VerilatedScope __Vscope_top__dut;
    VerilatedScope __Vscope_top__li_pipe__BRA__0__KET____lj_pipe__BRA__0__KET__;
    VerilatedScope __Vscope_top__li_pipe__BRA__0__KET____lj_pipe__BRA__1__KET__;
    VerilatedScope __Vscope_top__li_pipe__BRA__0__KET____lj_pipe__BRA__2__KET__;
    VerilatedScope __Vscope_top__li_pipe__BRA__0__KET____lj_pipe__BRA__3__KET__;
    VerilatedScope __Vscope_top__li_pipe__BRA__1__KET____lj_pipe__BRA__0__KET__;
    VerilatedScope __Vscope_top__li_pipe__BRA__1__KET____lj_pipe__BRA__1__KET__;
    VerilatedScope __Vscope_top__li_pipe__BRA__1__KET____lj_pipe__BRA__2__KET__;
    VerilatedScope __Vscope_top__li_pipe__BRA__1__KET____lj_pipe__BRA__3__KET__;
    VerilatedScope __Vscope_top__li_pipe__BRA__2__KET____lj_pipe__BRA__0__KET__;
    VerilatedScope __Vscope_top__li_pipe__BRA__2__KET____lj_pipe__BRA__1__KET__;
    VerilatedScope __Vscope_top__li_pipe__BRA__2__KET____lj_pipe__BRA__2__KET__;
    VerilatedScope __Vscope_top__li_pipe__BRA__2__KET____lj_pipe__BRA__3__KET__;
    VerilatedScope __Vscope_top__li_pipe__BRA__3__KET____lj_pipe__BRA__0__KET__;
    VerilatedScope __Vscope_top__li_pipe__BRA__3__KET____lj_pipe__BRA__1__KET__;
    VerilatedScope __Vscope_top__li_pipe__BRA__3__KET____lj_pipe__BRA__2__KET__;
    VerilatedScope __Vscope_top__li_pipe__BRA__3__KET____lj_pipe__BRA__3__KET__;
    VerilatedScope __Vscope_top__pipe_level__BRA__0__KET__;
    VerilatedScope __Vscope_top__pipe_level__BRA__1__KET__;
    VerilatedScope __Vscope_top__pipe_level__BRA__2__KET__;

    // CONSTRUCTORS
    Vtop__Syms(VerilatedContext* contextp, const char* namep, Vtop* modelp);
    ~Vtop__Syms();

    // METHODS
    const char* name() { return TOP.name(); }
} VL_ATTR_ALIGNED(VL_CACHE_LINE_BYTES);

#endif  // guard
