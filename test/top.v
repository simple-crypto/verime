module top
#
(
    parameter L = 4,
    parameter W = 8
)
(
    input clk,
    input valid_in,
    input [W-1:0] a,
    input [W-1:0] b,
    output [W-1:0] out,
    output [127:0] out_bis,
    output [15:0] tddloop,
    (* verilator_me = "test" *)
    output valid_out
);

genvar i;
generate
for(i=0;i<L;i=i+1) begin: pipe_level
    wire [2*W+1-1:0] in /* verilator public */;
    wire [2*W+1-1:0] out;

    (* verilator_me = "test2" *)
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
        (* verilator_me = "testd" *)
        wire tmp /* verilator public */;
        /* verilator lint_off WIDTH */
        assign tmp = (((4*i+j) % 2) & 1'b1) ;
        /* verilator lint_on WIDTH */
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
