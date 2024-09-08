from machine import Pin, SPI
import st7789v2
# Usage example
spi = SPI(0, baudrate=40000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(19))
lcd = st7789v2.LCD_1inch69(spi, cs=17, dc=15, rst=14, bl=13)

# Clear screen
lcd.clear()

# Draw some text
lcd.draw_text(60, 60, "WITAM", 0xFFFF)

# Draw a rectangle
lcd.draw_rect(50, 50, 100, 100, 0xF800)  # Red rectangle
