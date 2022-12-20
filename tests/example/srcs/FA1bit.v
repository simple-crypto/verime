// 1-bit full adder
module FA1bit
(
    input a,
    input b,
    input cin,
    output s,
    output cout
);


wire s_tmp;
assign s_tmp = a ^ b ^ cin;

wire cout_tmp;
assign cout_tmp = (cin & (a ^ b)) + (a & b);

// Generate out
assign s = s_tmp;
assign cout = cout_tmp;

endmodule
