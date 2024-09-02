from m5stack import *
from m5ui import *
from uiflow import *
import os

setScreenColor(0xffffff)

# Example data headers and values
header = "Time,Temperature,Humidity\n"
data = [
    "2024-09-02 12:00:00,25.5,60",
    "2024-09-02 12:05:00,25.7,61",
    "2024-09-02 12:10:00,25.9,59"
]

# Save data to a CSV file on the device
with open('/flash/data.csv', 'w') as file:
    # Write the header first
    file.write(header)
    # Write each data row
    for entry in data:
        file.write(entry + "\n")

# Display a confirmation message on the screen
label0 = M5TextBox(20, 20, "CSV Data Saved", lcd.FONT_DejaVu18, 0x000000, rotate=0)
