// DDS NCO. freq_word / 2^32 * clk.
module nco (
    input wire clk,
    input wire rst,
    input wire [31:0] freq_word,
    input wire [15:0] phase_offset,
    output reg signed [15:0] sample
);
    reg [31:0] acc;
    always @(posedge clk) begin
        if (rst) begin
            acc <= 0;
            sample <= 0;
        end else begin
            acc <= acc + freq_word;
            sample <= acc[31] ? -16'sd32767 : 16'sd32767;
        end
    end
endmodule
