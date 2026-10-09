// y = x * (wr + j wi), 1.15 fixed point.
module phase_shifter (
    input wire clk,
    input wire signed [15:0] i_in,
    input wire signed [15:0] q_in,
    input wire signed [15:0] w_re,
    input wire signed [15:0] w_im,
    output reg signed [15:0] i_out,
    output reg signed [15:0] q_out
);
    wire signed [31:0] ii = i_in * w_re;
    wire signed [31:0] qq = q_in * w_im;
    wire signed [31:0] iq = i_in * w_im;
    wire signed [31:0] qi = q_in * w_re;
    always @(posedge clk) begin
        i_out <= (ii - qq) >>> 15;
        q_out <= (iq + qi) >>> 15;
    end
endmodule
