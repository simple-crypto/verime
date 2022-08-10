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
(* my_other_attr = "other", verilator_me = "out_bis", my_second_other = "test"*)
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
        and_g dutb(
            .a(8'b0),
            .b(8'b1),
            .out()
        );
    end
end
endgenerate

assign valid_out = pipe_level[L-1].out[0];
and_g dut(
    .a(pipe_level[L-1].out[1 +: W]),
    .b(pipe_level[L-1].out[1+W +: W]),
    .out(out)
);

(* verilator_me = "test_mat_bytes" *)
wire [7:0] test_mat_bytes [3:0];
assign test_mat_bytes[0] = 8'd3;
assign test_mat_bytes[1] = 8'd5;
assign test_mat_bytes[2] = 8'd4;
assign test_mat_bytes[3] = 8'd6;

(* verilator_me = "test_big_matrix" *)
wire [127:0] mat_big [3:0];
assign mat_big[0] = 128'd120;
assign mat_big[1] = 128'd121;
assign mat_big[2] = 128'd122;
assign mat_big[3] = 128'd123;

(* verilator_me = "test_wire_u8" *)
wire test_wire_uint8;
assign test_wire_uint8 = 1'b1;

(* verilator_me = "test_bus_u8" *)
wire [6:0] test_bus_uint8;
assign test_bus_uint8 = 7'd5;

(* verilator_me = "test_bus_u16" *)
wire [11:0] test_bus_uint16;
assign test_bus_uint16 = 12'd301;

(* verilator_me = "test_bus_u32" *)
wire [24:0] test_bus_uint32;
assign test_bus_uint32 = 25'd1234;

(* verilator_me = "test_long_bus_u32" *)
wire [71:0] test_long_bus_u32;
assign test_long_bus_u32 = 72'd125365;



assign out_bis = {32'h01020304,32'h00112233,32'habcdabcd,32'h96541230};

endmodule
