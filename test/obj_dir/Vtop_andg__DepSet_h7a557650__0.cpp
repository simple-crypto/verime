// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "verilated.h"
#include "verilated_dpi.h"

#include "Vtop__Syms.h"
#include "Vtop_andg.h"

VL_INLINE_OPT void Vtop_andg___sequent__TOP__top__dut__1(Vtop_andg* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vtop_andg___sequent__TOP__top__dut__1\n"); );
    // Body
    vlSelf->tmp = (0xffU & ((vlSymsp->TOP__top.__PVT__pipe_level__BRA__2__KET____DOT__regin 
                             >> 1U) & (vlSymsp->TOP__top.__PVT__pipe_level__BRA__2__KET____DOT__regin 
                                       >> 9U)));
}
