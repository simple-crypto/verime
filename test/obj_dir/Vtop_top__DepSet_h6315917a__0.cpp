// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "verilated.h"
#include "verilated_dpi.h"

#include "Vtop_top.h"

VL_INLINE_OPT void Vtop_top___sequent__TOP__top__2(Vtop_top* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vtop_top___sequent__TOP__top__2\n"); );
    // Body
    vlSelf->__PVT__pipe_level__BRA__1__KET____DOT__regin 
        = vlSelf->pipe_level__BRA__1__KET____DOT__in;
    vlSelf->__PVT__pipe_level__BRA__0__KET____DOT__regin 
        = vlSelf->pipe_level__BRA__0__KET____DOT__in;
    vlSelf->__PVT__pipe_level__BRA__2__KET____DOT__regin 
        = vlSelf->pipe_level__BRA__2__KET____DOT__in;
    vlSelf->pipe_level__BRA__2__KET____DOT__in = vlSelf->__PVT__pipe_level__BRA__1__KET____DOT__regin;
    vlSelf->pipe_level__BRA__1__KET____DOT__in = vlSelf->__PVT__pipe_level__BRA__0__KET____DOT__regin;
}
