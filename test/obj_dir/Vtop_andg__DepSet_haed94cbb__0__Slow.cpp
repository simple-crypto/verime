// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "verilated.h"
#include "verilated_dpi.h"

#include "Vtop_andg.h"

VL_ATTR_COLD void Vtop_andg___ctor_var_reset(Vtop_andg* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vtop_andg___ctor_var_reset\n"); );
    // Body
    vlSelf->__PVT__a = VL_RAND_RESET_I(8);
    vlSelf->__PVT__b = VL_RAND_RESET_I(8);
    vlSelf->__PVT__out = VL_RAND_RESET_I(8);
    vlSelf->tmp = VL_RAND_RESET_I(8);
}
