// 0x00 control, 0x04 freq_word, 0x10+8i weights.
module beamform_top (
    input wire clk, input wire rst_n, input wire sclk, input wire cs_n, input wire mosi, output wire miso,
    output wire signed [15:0] dac0, output wire signed [15:0] dac1,
    output wire signed [15:0] dac2, output wire signed [15:0] dac3, output wire dac_strobe
);
    reg [31:0] regfile [0:31];
    reg [4:0] bitcnt;
    reg [39:0] shifter;
    reg miso_r;
    integer k;
    initial for (k = 0; k < 32; k = k + 1) regfile[k] = 0;
    assign miso = miso_r;
    always @(posedge sclk or posedge cs_n) begin
        if (cs_n) bitcnt <= 0;
        else begin
            shifter <= {shifter[38:0], mosi};
            bitcnt <= bitcnt + 1;
            if (bitcnt == 5'd39) regfile[shifter[38:32]] <= {shifter[31:0], mosi};
            miso_r <= regfile[shifter[38:32]][31 - bitcnt[4:0]];
        end
    end
    wire rst = ~rst_n | regfile[0][0];
    wire enable = regfile[0][1];
    wire signed [15:0] nco_i;
    nco u_nco (.clk(clk), .rst(rst), .freq_word(regfile[1]), .phase_offset(16'd0), .sample(nco_i));
    wire signed [15:0] i0, q0, i1, q1, i2, q2, i3, q3;
    mimo_precoder u_mimo (
        .clk(clk), .i_in(nco_i), .q_in(16'sd0),
        .w_re0(regfile[4][15:0]), .w_im0(regfile[5][15:0]),
        .w_re1(regfile[6][15:0]), .w_im1(regfile[7][15:0]),
        .w_re2(regfile[8][15:0]), .w_im2(regfile[9][15:0]),
        .w_re3(regfile[10][15:0]), .w_im3(regfile[11][15:0]),
        .i0(i0), .q0(q0), .i1(i1), .q1(q1), .i2(i2), .q2(q2), .i3(i3), .q3(q3)
    );
    assign dac0 = enable ? i0 : 16'sd0;
    assign dac1 = enable ? i1 : 16'sd0;
    assign dac2 = enable ? i2 : 16'sd0;
    assign dac3 = enable ? i3 : 16'sd0;
    assign dac_strobe = enable;
endmodule
