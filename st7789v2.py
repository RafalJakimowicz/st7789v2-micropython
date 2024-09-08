from machine import Pin, SPI
import framebuf
import time

class LCD_1inch69:
    def __init__(self, spi, cs, dc, rst, bl):
        # Pins
        self.cs = Pin(cs, Pin.OUT)
        self.dc = Pin(dc, Pin.OUT)
        self.rst = Pin(rst, Pin.OUT)
        self.bl = Pin(bl, Pin.OUT)

        # SPI setup
        self.spi = spi

        # Display resolution
        self.width = 240
        self.height = 280
        self.x_offset = 0    # Offset for correcting position
        self.y_offset = 20   # Adjust vertical offset by 20 pixels

        # Framebuffer for graphics
        self.buffer = bytearray(self.width * self.height * 2)
        self.fb = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.RGB565)

        self.init_display()

    def init_display(self):
        # Reset the display
        self.rst.value(0)
        time.sleep(0.1)
        self.rst.value(1)
        time.sleep(0.1)

        self.send_command(0x11)  # Sleep out
        time.sleep(0.12)

        # Initialization commands based on ST7789V2 datasheet
        self.send_command(0x36)
        self.send_data(0x00)  # Set scan direction

        self.send_command(0x3A)
        self.send_data(0x05)  # Set color format to 16-bit

        self.send_command(0x21)  # Inversion ON
        self.send_command(0x13)  # Normal display mode ON

        # Adjust memory access window with x/y offset correction
        self.set_window(0, 0, self.width - 1, self.height - 1)

        self.send_command(0x29)  # Display ON
        time.sleep(0.12)

    def set_window(self, x0, y0, x1, y1):
        """Set the display window with offset correction."""
        x0 += self.x_offset
        x1 += self.x_offset
        y0 += self.y_offset
        y1 += self.y_offset

        # Column address set (X)
        self.send_command(0x2A)
        self.send_data(x0 >> 8)
        self.send_data(x0 & 0xFF)
        self.send_data(x1 >> 8)
        self.send_data(x1 & 0xFF)

        # Row address set (Y)
        self.send_command(0x2B)
        self.send_data(y0 >> 8)
        self.send_data(y0 & 0xFF)
        self.send_data(y1 >> 8)
        self.send_data(y1 & 0xFF)

        # Write to RAM
        self.send_command(0x2C)

    def send_command(self, command):
        self.cs.value(0)
        self.dc.value(0)  # Command mode
        self.spi.write(bytearray([command]))
        self.cs.value(1)

    def send_data(self, data):
        self.cs.value(0)
        self.dc.value(1)  # Data mode
        if isinstance(data, int):
            self.spi.write(bytearray([data]))
        else:
            self.spi.write(data)
        self.cs.value(1)

    def clear(self, color=0x0000):
        """Clear the screen with the given color."""
        self.fb.fill(color)
        self.show()

    def show(self):
        """Update the display with the framebuffer content."""
        self.set_window(0, 0, self.width - 1, self.height - 1)
        self.cs.value(0)
        self.dc.value(1)
        self.spi.write(self.buffer)
        self.cs.value(1)

    def draw_text(self, x, y, text, color=0xFFFF):
        """Draw text at a given position."""
        self.fb.text(text, x, y, color)
        self.show()

    def draw_pixel(self, x, y, color):
        """Draw a pixel at (x, y)."""
        self.fb.pixel(x, y, color)
        self.show()

    def draw_line(self, x1, y1, x2, y2, color):
        """Draw a line between two points."""
        self.fb.line(x1, y1, x2, y2, color)
        self.show()

    def draw_rect(self, x, y, w, h, color):
        """Draw a rectangle."""
        self.fb.rect(x, y, w, h, color)
        self.show()