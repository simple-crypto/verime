// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vtop__Syms.h"
#include "Vtop.h"
#include "Vtop___024root.h"
#include "Vtop_top.h"
#include "Vtop_andg.h"

// FUNCTIONS
Vtop__Syms::~Vtop__Syms()
{
}

Vtop__Syms::Vtop__Syms(VerilatedContext* contextp, const char* namep,Vtop* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP(namep)
    , TOP__top(Verilated::catName(namep, "top"))
    , TOP__top__dut(Verilated::catName(namep, "top.dut"))
{
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-12);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    TOP.top = &TOP__top;
    TOP__top.dut = &TOP__top__dut;
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(this, true);
    TOP__top.__Vconfigure(this, true);
    TOP__top__dut.__Vconfigure(this, true);
    // Setup scopes
    __Vscope_top__dut.configure(this, name(), "top.dut", "dut", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__0__KET____lj_pipe__BRA__0__KET__.configure(this, name(), "top.li_pipe[0].lj_pipe[0]", "lj_pipe[0]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__0__KET____lj_pipe__BRA__1__KET__.configure(this, name(), "top.li_pipe[0].lj_pipe[1]", "lj_pipe[1]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__0__KET____lj_pipe__BRA__2__KET__.configure(this, name(), "top.li_pipe[0].lj_pipe[2]", "lj_pipe[2]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__0__KET____lj_pipe__BRA__3__KET__.configure(this, name(), "top.li_pipe[0].lj_pipe[3]", "lj_pipe[3]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__1__KET____lj_pipe__BRA__0__KET__.configure(this, name(), "top.li_pipe[1].lj_pipe[0]", "lj_pipe[0]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__1__KET____lj_pipe__BRA__1__KET__.configure(this, name(), "top.li_pipe[1].lj_pipe[1]", "lj_pipe[1]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__1__KET____lj_pipe__BRA__2__KET__.configure(this, name(), "top.li_pipe[1].lj_pipe[2]", "lj_pipe[2]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__1__KET____lj_pipe__BRA__3__KET__.configure(this, name(), "top.li_pipe[1].lj_pipe[3]", "lj_pipe[3]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__2__KET____lj_pipe__BRA__0__KET__.configure(this, name(), "top.li_pipe[2].lj_pipe[0]", "lj_pipe[0]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__2__KET____lj_pipe__BRA__1__KET__.configure(this, name(), "top.li_pipe[2].lj_pipe[1]", "lj_pipe[1]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__2__KET____lj_pipe__BRA__2__KET__.configure(this, name(), "top.li_pipe[2].lj_pipe[2]", "lj_pipe[2]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__2__KET____lj_pipe__BRA__3__KET__.configure(this, name(), "top.li_pipe[2].lj_pipe[3]", "lj_pipe[3]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__3__KET____lj_pipe__BRA__0__KET__.configure(this, name(), "top.li_pipe[3].lj_pipe[0]", "lj_pipe[0]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__3__KET____lj_pipe__BRA__1__KET__.configure(this, name(), "top.li_pipe[3].lj_pipe[1]", "lj_pipe[1]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__3__KET____lj_pipe__BRA__2__KET__.configure(this, name(), "top.li_pipe[3].lj_pipe[2]", "lj_pipe[2]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__li_pipe__BRA__3__KET____lj_pipe__BRA__3__KET__.configure(this, name(), "top.li_pipe[3].lj_pipe[3]", "lj_pipe[3]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__pipe_level__BRA__0__KET__.configure(this, name(), "top.pipe_level[0]", "pipe_level[0]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__pipe_level__BRA__1__KET__.configure(this, name(), "top.pipe_level[1]", "pipe_level[1]", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_top__pipe_level__BRA__2__KET__.configure(this, name(), "top.pipe_level[2]", "pipe_level[2]", 0, VerilatedScope::SCOPE_OTHER);
    // Setup export functions
    for (int __Vfinal=0; __Vfinal<2; __Vfinal++) {
        __Vscope_top__dut.varInsert(__Vfinal,"tmp", &(TOP__top__dut.tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,1 ,7,0);
        __Vscope_top__li_pipe__BRA__0__KET____lj_pipe__BRA__0__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__li_pipe__BRA__0__KET____lj_pipe__BRA__1__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__li_pipe__BRA__0__KET____lj_pipe__BRA__2__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__li_pipe__BRA__0__KET____lj_pipe__BRA__3__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__0__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__li_pipe__BRA__1__KET____lj_pipe__BRA__0__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__li_pipe__BRA__1__KET____lj_pipe__BRA__1__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__li_pipe__BRA__1__KET____lj_pipe__BRA__2__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__li_pipe__BRA__1__KET____lj_pipe__BRA__3__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__1__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__li_pipe__BRA__2__KET____lj_pipe__BRA__0__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__li_pipe__BRA__2__KET____lj_pipe__BRA__1__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__li_pipe__BRA__2__KET____lj_pipe__BRA__2__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__li_pipe__BRA__2__KET____lj_pipe__BRA__3__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__2__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__li_pipe__BRA__3__KET____lj_pipe__BRA__0__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__0__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__li_pipe__BRA__3__KET____lj_pipe__BRA__1__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__1__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__li_pipe__BRA__3__KET____lj_pipe__BRA__2__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__2__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__li_pipe__BRA__3__KET____lj_pipe__BRA__3__KET__.varInsert(__Vfinal,"tmp", &(TOP__top.li_pipe__BRA__3__KET____DOT__lj_pipe__BRA__3__KET____DOT__tmp), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0);
        __Vscope_top__pipe_level__BRA__0__KET__.varInsert(__Vfinal,"in", &(TOP__top.pipe_level__BRA__0__KET____DOT__in), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,16,0);
        __Vscope_top__pipe_level__BRA__1__KET__.varInsert(__Vfinal,"in", &(TOP__top.pipe_level__BRA__1__KET____DOT__in), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,16,0);
        __Vscope_top__pipe_level__BRA__2__KET__.varInsert(__Vfinal,"in", &(TOP__top.pipe_level__BRA__2__KET____DOT__in), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1 ,16,0);
    }
}
