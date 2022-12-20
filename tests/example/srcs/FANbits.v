// N-bits full adder
module FANbits
#
(
    parameter N=4
)
(
    input [N-1:0] a,
    input [N-1:0] b,
    input cin,
    output [N-1:0] s,
    output cout
);

// Generate the N single bit FA instance
genvar i;
generate
for(i=0;i<N;i=i+1) begin: FAinst
    // Carry signals propagated
    wire inst_cin, inst_cout;
    
    // Instances
    FA1bit adder1bit(
        .a(a[i]),
        .b(b[i]),
        .cin(inst_cin),
        .s(s[i]),
        .cout(inst_cout)
    );

    // Route carry input 
    if (i==0) begin
        assign inst_cin = cin;
    end else begin
        assign inst_cin = FAinst[i-1].inst_cout;
    end
end
endgenerate

// Propagate the carry out signal
assign cout = FAinst[N-1].inst_cout;

endmodule
