// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "verilated.h"
#include "verilated_dpi.h"

#include "Vtop__Syms.h"
#include "Vtop___024root.h"

VL_INLINE_OPT void Vtop___024root___sequent__TOP__2(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___sequent__TOP__2\n"); );
    // Body
    vlSelf->valid_out = (1U & vlSymsp->TOP__top.__PVT__pipe_level__BRA__2__KET____DOT__regin);
}

VL_INLINE_OPT void Vtop___024root___sequent__TOP__3(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___sequent__TOP__3\n"); );
    // Body
    vlSelf->out = vlSymsp->TOP__top__dut.tmp;
}

void Vtop_top___sequent__TOP__top__2(Vtop_top* vlSelf);
void Vtop_andg___sequent__TOP__top__dut__1(Vtop_andg* vlSelf);
void Vtop_top___combo__TOP__top__4(Vtop_top* vlSelf);

void Vtop___024root___eval(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval\n"); );
    // Body
    if (((IData)(vlSelf->clk) & (~ (IData)(vlSelf->__Vclklast__TOP__clk)))) {
        Vtop_top___sequent__TOP__top__2((&vlSymsp->TOP__top));
        Vtop___024root___sequent__TOP__2(vlSelf);
        Vtop_andg___sequent__TOP__top__dut__1((&vlSymsp->TOP__top__dut));
        Vtop___024root___sequent__TOP__3(vlSelf);
    }
    Vtop_top___combo__TOP__top__4((&vlSymsp->TOP__top));
    // Final
    vlSelf->__Vclklast__TOP__clk = vlSelf->clk;
}
