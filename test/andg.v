module andg
#
(
    parameter W=8
)
(
    input [W-1:0] a,
    input [W-1:0] b,
    output [W-1:0] out
);

(* verilator_me = "test3" *)
wire [W-1:0] tmp/* verilator public */;
assign tmp = a & b;
assign out = tmp;

endmodule
