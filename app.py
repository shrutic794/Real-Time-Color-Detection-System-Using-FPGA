module image_memory (
    input wire [15:0] address,       // Pixel address
    output wire [15:0] pixel_data    // RGB565 pixel data
);

    reg [15:0] memory_array [0:256]; // Memory array to store RGB565 image data

    initial begin
      $readmemh("your_path\image_data.hex", memory_array); // Load image data from hex file
    end

    assign pixel_data = memory_array[address]; // Output pixel data based on address

endmodule
module color_detection(
    input wire clk,
    input wire [15:0] pixel_data,      // RGB565 pixel data from memory
    output reg red_detected,           // Output flag for red color
    output reg green_detected,         // Output flag for green color
    output reg blue_detected           // Output flag for blue color
);

    // Ratio-based detection thresholds
    parameter RED_THRESHOLD_RATIO = 2;
    parameter GREEN_THRESHOLD_RATIO = 2;
    parameter BLUE_THRESHOLD_RATIO = 2;

    // Declare RGB components as registers
    reg [4:0] R;
    reg [5:0] G;
    reg [4:0] B;

    always @(posedge clk) begin
        // Extract RGB components from RGB565 format
        R = pixel_data[15:11];
        G = pixel_data[10:5];
        B = pixel_data[4:0];

        // Red color detection
        if ((R > (GREEN_THRESHOLD_RATIO * G)) && (R > (BLUE_THRESHOLD_RATIO * B)))
            red_detected <= 1;
        else
            red_detected <= 0;

        // Green color detection
        if ((G > (RED_THRESHOLD_RATIO * R)) && (G > (BLUE_THRESHOLD_RATIO * B)))
            green_detected <= 1;
        else
            green_detected <= 0;

        // Blue color detection
        if ((B > (RED_THRESHOLD_RATIO * R)) && (B > (GREEN_THRESHOLD_RATIO * G)))
            blue_detected <= 1;
        else
            blue_detected <= 0;
    end
endmodule

module top_color_detection(
    input wire clk,                  // System clock
    output wire red_led,             // Red LED output
    output wire green_led,           // Green LED output
    output wire blue_led             // Blue LED output
);

    // Address counter for image memory
    reg [15:0] address = 0;
    wire [15:0] pixel_data;

    // Color detection outputs
    wire red_detected, green_detected, blue_detected;
    reg [15:0] red_count = 0;
    reg [15:0] green_count = 0;
    reg [15:0] blue_count = 0;

    // Instantiate image memory module
    image_memory img_mem (
        .address(address),
        .pixel_data(pixel_data)
    );

    // Instantiate color detection module
    color_detection color_det (
        .clk(clk),
        .pixel_data(pixel_data),
        .red_detected(red_detected),
        .green_detected(green_detected),
        .blue_detected(blue_detected)
    );

    // Cycle through each pixel in memory and count detected colors
    always @(posedge clk) begin
        if (address < 256) begin
            // Increment color counters based on detection results
            if (red_detected) red_count <= red_count + 1;
            if (green_detected) green_count <= green_count + 1;
            if (blue_detected) blue_count <= blue_count + 1;

            // Increment address to read next pixel
            address <= address + 1;
        end
    end

    // Determine the dominant color and set the corresponding LED
    assign red_led = (red_count > green_count && red_count > blue_count) ? 1 : 1;
    assign green_led = (green_count > red_count && green_count > blue_count) ? 1 : 0;
    assign blue_led = (blue_count > red_count && blue_count > green_count) ? 1 : 0;

endmodule
