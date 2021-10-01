module and_g
#
(
    parameter W=8
)
(
    input [W-1:0] a,
    input [W-1:0] b,
    output [W-1:0] out
);

(* verilator_me = "tmp_andg" *)
wire [W-1:0] tmp;
assign tmp = a & b;
assign out = tmp;

endmodule
