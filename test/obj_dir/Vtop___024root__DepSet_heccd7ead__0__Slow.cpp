// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "verilated.h"
#include "verilated_dpi.h"

#include "Vtop___024root.h"

VL_ATTR_COLD void Vtop___024root___initial__TOP__1(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___initial__TOP__1\n"); );
    // Body
    vlSelf->out_bis[0U] = 0x96541230U;
    vlSelf->out_bis[1U] = 0xabcdabcdU;
    vlSelf->out_bis[2U] = 0x112233U;
    vlSelf->out_bis[3U] = 0x1020304U;
}

VL_ATTR_COLD void Vtop___024root___final(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___final\n"); );
}

VL_ATTR_COLD void Vtop___024root___ctor_var_reset(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ctor_var_reset\n"); );
    // Body
    vlSelf->clk = VL_RAND_RESET_I(1);
    vlSelf->valid_in = VL_RAND_RESET_I(1);
    vlSelf->a = VL_RAND_RESET_I(8);
    vlSelf->b = VL_RAND_RESET_I(8);
    vlSelf->out = VL_RAND_RESET_I(8);
    vlSelf->out_bis[0] = 2522092080U;
    vlSelf->out_bis[1] = 2882382797U;
    vlSelf->out_bis[2] = 1122867U;
    vlSelf->out_bis[3] = 16909060U;
    vlSelf->tddloop = VL_RAND_RESET_I(16);
    vlSelf->valid_out = VL_RAND_RESET_I(1);
}
