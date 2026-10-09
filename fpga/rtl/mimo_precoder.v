module mimo_precoder (
    input wire clk,
    input wire signed [15:0] i_in,
    input wire signed [15:0] q_in,
    input wire signed [15:0] w_re0, input wire signed [15:0] w_im0,
    input wire signed [15:0] w_re1, input wire signed [15:0] w_im1,
    input wire signed [15:0] w_re2, input wire signed [15:0] w_im2,
    input wire signed [15:0] w_re3, input wire signed [15:0] w_im3,
    output wire signed [15:0] i0, output wire signed [15:0] q0,
    output wire signed [15:0] i1, output wire signed [15:0] q1,
    output wire signed [15:0] i2, output wire signed [15:0] q2,
    output wire signed [15:0] i3, output wire signed [15:0] q3
);
    phase_shifter u0 (.clk(clk), .i_in(i_in), .q_in(q_in), .w_re(w_re0), .w_im(w_im0), .i_out(i0), .q_out(q0));
    phase_shifter u1 (.clk(clk), .i_in(i_in), .q_in(q_in), .w_re(w_re1), .w_im(w_im1), .i_out(i1), .q_out(q1));
    phase_shifter u2 (.clk(clk), .i_in(i_in), .q_in(q_in), .w_re(w_re2), .w_im(w_im2), .i_out(i2), .q_out(q2));
    phase_shifter u3 (.clk(clk), .i_in(i_in), .q_in(q_in), .w_re(w_re3), .w_im(w_im3), .i_out(i3), .q_out(q3));
endmodule
