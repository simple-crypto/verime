module top
#
(
    parameter L = 5,
    parameter W = 8
)
(
    clk,
    valid_in,
    a,
    b,
    out,
    out_bis,
    tddloop,
    valid_out
);

input clk;
input valid_in;
input [W-1:0] a;
input [W-1:0] b;
output [W-1:0] out;
(* verilator_me = "out_bis"*)
output [127:0] out_bis;
output [15:0] tddloop;
output valid_out;


genvar i;
generate
for(i=0;i<L;i=i+1) begin: pipe_level
    wire [2*W+1-1:0] in;
    wire [2*W+1-1:0] out;

    (* verilator_me = "reg_in_pipeline" *)
    reg [2*W+1-1:0] regin;
    always@(posedge clk)
    begin
        regin <= in;
    end
    assign out = regin;

    if(i==0) begin
        assign in = {a,b,valid_in};
    end else begin
        assign in = pipe_level[i-1].out;
    end
end
endgenerate

// Test of imbricated loop
genvar j;
generate
for(i=0;i<4;i=i+1) begin: li_pipe
    for(j=0;j<4;j=j+1) begin: lj_pipe
        (* verilator_me = "tmp_double_loops" *)
        wire tmp;
        assign tmp = 1'b0;
        assign tddloop[4*i+j] = tmp;
    end
end
endgenerate

assign valid_out = pipe_level[L-1].out[0];
andg dut(
    .a(pipe_level[L-1].out[1 +: W]),
    .b(pipe_level[L-1].out[1+W +: W]),
    .out(out)
);


assign out_bis = {32'h01020304,32'h00112233,32'habcdabcd,32'h96541230};

endmodule
