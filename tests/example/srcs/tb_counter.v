`timescale 1ns/1ps
module tb_counter ();

localparam T = 2.0;
localparam Td = T/2.0;

localparam N = 4;

reg clk;
reg rst;

reg [N-1:0] cnt_bound;

reg start;
wire busy;

// Clock
always@(*) #Td clk<=~clk;

// Dut
counter #(.N(N))
dut(
    .clk(clk),
    .rst(rst),
    .cnt_bound(cnt_bound),
    .start(start),
    .busy(busy)
);

initial begin
    $dumpfile("log.vcd");
    $dumpvars(0,tb_counter);

    clk = 1;
    rst = 0;
    start = 0;

    #(0.01*T);
    rst = 1;
    #T;
    rst = 0;

    cnt_bound = 4'd12;

    #T;
    start = 1;
    #T;
    start = 0;

    while(busy) begin
        #T;
    end

    #T;
    #T;

    $finish();
end

endmodule
