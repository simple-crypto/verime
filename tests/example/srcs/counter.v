// Counter if N bits
module counter
#
(
    parameter N = 4
)
(
    input my_clk,
    input rst,
    input [N-1:0] cnt_bound,
    input start,
    output busy
);

// Register to hold the value
(* verime = "counter_state" *)
reg [N-1:0] counter_state;
wire [N-1:0] counter_nextstate;
reg inc_counter, rst_counter;
always@(posedge my_clk)
if(rst_counter) begin
    counter_state <= 0;
end else if(inc_counter) begin
    counter_state <= counter_nextstate;
end

// Instanciate the FA
wire [N-1:0] cst = 1;
FANbits #(.N(N))
fulladder(
    .a(counter_state),
    .b(cst),
    .cin(1'b0),
    .s(counter_nextstate)
);

// Register to hold the boundary value
reg [N-1:0] bound;
always@(posedge my_clk)
if(rst_counter) begin
    bound <= cnt_bound;
end 
wire end_cnt = counter_state == bound;

// FSM
localparam IDLE=0,
WAIT=1;

reg [1:0] state, nextstate;
always@(posedge my_clk)
if(rst) begin
    state <= IDLE;
end else begin
    state <= nextstate;
end

always@(*) begin
    inc_counter = 0;
    rst_counter = 0;

    nextstate = state;

    case(state)
        IDLE: begin
            if(start) begin
                rst_counter = 1;
                nextstate = WAIT;
            end
        end 
        WAIT: begin
            inc_counter = 1;
            if (end_cnt) begin
                nextstate = IDLE;
            end
        end
        default: nextstate = state;
    endcase
end

assign busy = state==WAIT;

endmodule
