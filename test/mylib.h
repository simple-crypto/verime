#ifndef LIB_H_
#define LIB_H_
#include "Vtop.h"
#include "Vtop_top.h" // From Verilating "top.v"
#include "Vtop_andg.h" // From Verilating "top.v"
#include "verilated.h"

struct SimModel{
    VerilatedContext * contextp;
    Vtop * vtop;
};

SimModel create_new_model();

void delete_model(SimModel mod);

#endif
