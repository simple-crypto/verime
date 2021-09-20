#include "Vtop.h"
#include "Vtop_top.h" // From Verilating "top.v"
#include "Vtop_andg.h" // From Verilating "top.v"
#include "verilated.h"
#include "mylib.h"

SimModel create_new_model() {
    VerilatedContext * contextp = new VerilatedContext;
    Vtop * top;
    top = new Vtop(contextp);
    SimModel sm;
    sm.contextp = contextp;
    sm.vtop = top;
    return sm;
}

void delete_model(SimModel mod) {
    delete mod.vtop;
    delete mod.contextp;
}
