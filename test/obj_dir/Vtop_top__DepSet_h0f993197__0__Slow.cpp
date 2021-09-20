// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "verilated.h"
#include "verilated_dpi.h"

#include "Vtop__Syms.h"
#include "Vtop_top.h"

VL_ATTR_COLD void Vtop_top___settle__TOP__top__3(Vtop_top* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vtop_top___settle__TOP__top__3\n"); );
    // Body
    vlSelf->pipe_level__BRA__0__KET____DOT__in = (((IData)(vlSymsp->TOP.a) 
                                                   << 9U) 
                                                  | (((IData)(vlSymsp->TOP.b) 
                                                      << 1U) 
                                                     | (IData)(vlSymsp->TOP.valid_in)));
    vlSelf->pipe_level__BRA__1__KET____DOT__in = vlSelf->__PVT__pipe_level__BRA__0__KET____DOT__regin;
    vlSelf->pipe_level__BRA__2__KET____DOT__in = vlSelf->__PVT__pipe_level__BRA__1__KET____DOT__regin;
    vlSelf->tddloop = ((0xfff0U & (IData)(vlSelf->tddloop)) 
                       | (((IData)(vlSelf->li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp) 
                           << 3U) | (((IData)(vlSelf->li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp) 
                                      << 2U) | (((IData)(vlSelf->li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp) 
                                                 << 1U) 
                                                | (IData)(vlSelf->li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp)))));
    vlSelf->tddloop = ((0xff0fU & (IData)(vlSelf->tddloop)) 
                       | (((IData)(vlSelf->li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp) 
                           << 7U) | (((IData)(vlSelf->li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp) 
                                      << 6U) | (((IData)(vlSelf->li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp) 
                                                 << 5U) 
                                                | ((IData)(vlSelf->li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp) 
                                                   << 4U)))));
    vlSelf->tddloop = ((0xf0ffU & (IData)(vlSelf->tddloop)) 
                       | (((IData)(vlSelf->li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp) 
                           << 0xbU) | (((IData)(vlSelf->li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp) 
                                        << 0xaU) | 
                                       (((IData)(vlSelf->li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp) 
                                         << 9U) | ((IData)(vlSelf->li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp) 
                                                   << 8U)))));
    vlSelf->tddloop = ((0xfffU & (IData)(vlSelf->tddloop)) 
                       | (((IData)(vlSelf->li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp) 
                           << 0xfU) | (((IData)(vlSelf->li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp) 
                                        << 0xeU) | 
                                       (((IData)(vlSelf->li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp) 
                                         << 0xdU) | 
                                        ((IData)(vlSelf->li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp) 
                                         << 0xcU)))));
}
