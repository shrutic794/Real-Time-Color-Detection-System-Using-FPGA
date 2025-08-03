#  FPGA-Based Color Detection Using RGB565

This Verilog project implements a simple image-based color detection system using an FPGA. It reads pixel data in **RGB565** format from memory, detects red, green, and blue dominance using ratio-based logic, and activates the corresponding LED based on the dominant color across all pixels.

---

##  Modules Overview

###  `image_memory.v`
- Stores 256 RGB565 pixel values in a memory array.
- Loads image data from a `.hex` file during simulation or synthesis.
- Outputs pixel data based on the current address.

###  `color_detection.v`
- Extracts 5-bit Red, 6-bit Green, and 5-bit Blue components from RGB565.
- Uses **ratio-based thresholding** to detect dominance of red, green, or blue.
- Outputs flags: `red_detected`, `green_detected`, and `blue_detected`.

###  `top_color_detection.v`
- Integrates memory and detection modules.
- Cycles through all 256 pixel addresses.
- Counts how many times each color was dominant.
- Sets one of the `red_led`, `green_led`, or `blue_led` outputs based on the most frequently detected color.

---

##  How It Works

1. The `image_memory` module loads pixel data from a `.hex` file.
2. On every clock cycle, one pixel is processed by `color_detection`.
3. A counter increments for red, green, or blue based on detection.
4. After scanning all 256 pixels, the module activates the LED corresponding to the dominant color.

---

##  RGB565 Format

- Red:   5 bits (`[15:11]`)
- Green: 6 bits (`[10:5]`)
- Blue:  5 bits (`[4:0]`)

Ratio-based detection avoids strict thresholds and works on **relative dominance**.

---

##  Output LEDs

| Output Signal | Meaning                    |
|---------------|----------------------------|
| `red_led`     | Red is the most dominant   |
| `green_led`   | Green is the most dominant |
| `blue_led`    | Blue is the most dominant  |

> Note: All three LED lines may momentarily show logic high due to initial behavior; this can be enhanced with a final comparison stage or FSM logic.

---


