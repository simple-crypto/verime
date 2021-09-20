// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "verilated.h"
#include "verilated_dpi.h"

#include "Vtop_top.h"

VL_ATTR_COLD void Vtop_top___initial__TOP__top__1(Vtop_top* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vtop_top___initial__TOP__top__1\n"); );
    // Body
    vlSelf->li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp = 0U;
    vlSelf->li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp = 1U;
    vlSelf->li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp = 0U;
    vlSelf->li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp = 1U;
    vlSelf->li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp = 0U;
    vlSelf->li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp = 1U;
    vlSelf->li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp = 0U;
    vlSelf->li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp = 1U;
    vlSelf->li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp = 0U;
    vlSelf->li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp = 1U;
    vlSelf->li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp = 0U;
    vlSelf->li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp = 1U;
    vlSelf->li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp = 0U;
    vlSelf->li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp = 1U;
    vlSelf->li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp = 0U;
    vlSelf->li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp = 1U;
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

VL_ATTR_COLD void Vtop_top___ctor_var_reset(Vtop_top* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vtop_top___ctor_var_reset\n"); );
    // Body
    vlSelf->clk = VL_RAND_RESET_I(1);
    vlSelf->valid_in = VL_RAND_RESET_I(1);
    vlSelf->a = VL_RAND_RESET_I(8);
    vlSelf->b = VL_RAND_RESET_I(8);
    vlSelf->out = VL_RAND_RESET_I(8);
    vlSelf->__PVT__out_bis[0] = 2522092080U;
    vlSelf->__PVT__out_bis[1] = 2882382797U;
    vlSelf->__PVT__out_bis[2] = 1122867U;
    vlSelf->__PVT__out_bis[3] = 16909060U;
    vlSelf->tddloop = VL_RAND_RESET_I(16);
    vlSelf->valid_out = VL_RAND_RESET_I(1);
    vlSelf->pipe_level__BRA__0__KET____DOT__in = VL_RAND_RESET_I(17);
    vlSelf->__PVT__pipe_level__BRA__0__KET____DOT__regin = VL_RAND_RESET_I(17);
    vlSelf->pipe_level__BRA__1__KET____DOT__in = VL_RAND_RESET_I(17);
    vlSelf->__PVT__pipe_level__BRA__1__KET____DOT__regin = VL_RAND_RESET_I(17);
    vlSelf->pipe_level__BRA__2__KET____DOT__in = VL_RAND_RESET_I(17);
    vlSelf->__PVT__pipe_level__BRA__2__KET____DOT__regin = VL_RAND_RESET_I(17);
    vlSelf->li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp = VL_RAND_RESET_I(1);
    vlSelf->li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp = VL_RAND_RESET_I(1);
    vlSelf->li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp = VL_RAND_RESET_I(1);
    vlSelf->li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp = VL_RAND_RESET_I(1);
    vlSelf->li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp = VL_RAND_RESET_I(1);
    vlSelf->li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp = VL_RAND_RESET_I(1);
    vlSelf->li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp = VL_RAND_RESET_I(1);
    vlSelf->li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp = VL_RAND_RESET_I(1);
    vlSelf->li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp = VL_RAND_RESET_I(1);
    vlSelf->li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp = VL_RAND_RESET_I(1);
    vlSelf->li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp = VL_RAND_RESET_I(1);
    vlSelf->li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp = VL_RAND_RESET_I(1);
    vlSelf->li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp = VL_RAND_RESET_I(1);
    vlSelf->li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp = VL_RAND_RESET_I(1);
    vlSelf->li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp = VL_RAND_RESET_I(1);
    vlSelf->li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp = VL_RAND_RESET_I(1);
}
