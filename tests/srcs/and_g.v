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


(* verilator_me = "test_big_matrix_imbricated" *)
wire [127:0] mat_big [3:0];
assign mat_big[0] = 128'd120;
assign mat_big[1] = 128'd121;
assign mat_big[2] = 128'd122;
assign mat_big[3] = 128'd123;




(* verilator_me = "tmp_andg" *)
wire [W-1:0] tmp;
assign tmp = a & b;
assign out = tmp;

endmodule
