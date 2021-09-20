// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "verilated.h"
#include "verilated_dpi.h"

#include "Vtop__Syms.h"
#include "Vtop_top.h"

VL_INLINE_OPT void Vtop_top___combo__TOP__top__4(Vtop_top* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vtop_top___combo__TOP__top__4\n"); );
    // Body
    vlSelf->pipe_level__BRA__0__KET____DOT__in = (((IData)(vlSymsp->TOP.a) 
                                                   << 9U) 
                                                  | (((IData)(vlSymsp->TOP.b) 
                                                      << 1U) 
                                                     | (IData)(vlSymsp->TOP.valid_in)));
}
