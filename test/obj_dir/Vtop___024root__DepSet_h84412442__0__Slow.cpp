// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "verilated.h"
#include "verilated_dpi.h"

#include "Vtop__Syms.h"
#include "Vtop___024root.h"

VL_ATTR_COLD void Vtop___024root___settle__TOP__4(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___settle__TOP__4\n"); );
    // Body
    vlSelf->valid_out = (1U & vlSymsp->TOP__top.__PVT__pipe_level__BRA__2__KET____DOT__regin);
    vlSelf->tddloop = vlSymsp->TOP__top.tddloop;
    vlSelf->tddloop = vlSymsp->TOP__top.tddloop;
}

VL_ATTR_COLD void Vtop___024root___initial__TOP__1(Vtop___024root* vlSelf);
VL_ATTR_COLD void Vtop_top___initial__TOP__top__1(Vtop_top* vlSelf);

VL_ATTR_COLD void Vtop___024root___eval_initial(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_initial\n"); );
    // Body
    Vtop___024root___initial__TOP__1(vlSelf);
    Vtop_top___initial__TOP__top__1((&vlSymsp->TOP__top));
    vlSelf->__Vclklast__TOP__clk = vlSelf->clk;
}

VL_ATTR_COLD void Vtop_top___settle__TOP__top__3(Vtop_top* vlSelf);
void Vtop_andg___sequent__TOP__top__dut__1(Vtop_andg* vlSelf);
void Vtop___024root___sequent__TOP__3(Vtop___024root* vlSelf);

VL_ATTR_COLD void Vtop___024root___eval_settle(Vtop___024root* vlSelf) {
    if (false && vlSelf) {}  // Prevent unused
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_settle\n"); );
    // Body
    Vtop_top___settle__TOP__top__3((&vlSymsp->TOP__top));
    Vtop___024root___settle__TOP__4(vlSelf);
    Vtop_andg___sequent__TOP__top__dut__1((&vlSymsp->TOP__top__dut));
    Vtop___024root___sequent__TOP__3(vlSelf);
}
