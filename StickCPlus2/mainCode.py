from m5stack import *
from m5ui import *
from uiflow import *
import os
import imu
import hat
import time

setScreenColor(0xffffff)

# Initialize the IMU and Heart Rate Hat
imu0 = imu.IMU()
hat_heartrate_2 = hat.get(hat.HEART_RATE)

# Initialize variables
is_recording = False
csv_file_path = '/flash/data.csv'
data = []

# UI elements
flashing_circle = M5Circle(60, 70, 10, 0x000000, 0x000000)  # Flashing circle between label0 and readings

label0 = M5TextBox(7, 100, "IR:", lcd.FONT_Default, 0xff0000, rotate=0)
label4 = M5TextBox(7, 120, "Xacc", lcd.FONT_Default, 0xf50000, rotate=0)
label5 = M5TextBox(7, 140, "yAcc", lcd.FONT_Default, 0xc71111, rotate=0)
label6 = M5TextBox(7, 160, "zAcc", lcd.FONT_Default, 0xf50000, rotate=0)
label7 = M5TextBox(7, 180, "Gyro X", lcd.FONT_Default, 0xf50000, rotate=0)
label8 = M5TextBox(7, 200, "Gyro Y", lcd.FONT_Default, 0xf50000, rotate=0)
label9 = M5TextBox(7, 220, "Gyro Z", lcd.FONT_Default, 0xf50000, rotate=0)
label0_val = M5TextBox(84, 100, "0", lcd.FONT_Default, 0xff0000, rotate=0)
label4_val = M5TextBox(84, 120, "0", lcd.FONT_Default, 0xff0000, rotate=0)
label5_val = M5TextBox(84, 140, "0", lcd.FONT_Default, 0xff0000, rotate=0)
label6_val = M5TextBox(84, 160, "0", lcd.FONT_Default, 0xff0000, rotate=0)
label7_val = M5TextBox(84, 180, "0", lcd.FONT_Default, 0xff0000, rotate=0)
label8_val = M5TextBox(84, 200, "0", lcd.FONT_Default, 0xff0000, rotate=0)
label9_val = M5TextBox(84, 220, "0", lcd.FONT_Default, 0xff0000, rotate=0)
title0 = M5Title(title="HEALTH MONITOR", x=8, fgcolor=0xFFFFFF, bgcolor=0xff7300)
label0_status = M5TextBox(7, 20, "M5 to Record", lcd.FONT_Default, 0x000000, rotate=0)
label1_status = M5TextBox(20, 60, "", lcd.FONT_Default, 0x000000, rotate=0)

# Function to start recording data
def start_recording():
    global is_recording, data
    is_recording = True
    data.clear()  # Clear previous data if starting a new recording session
    label0_status.setText("Recording")

# Function to stop recording and save data to CSV
def stop_recording_and_save():
    global is_recording
    is_recording = False
    
    # Save data to the CSV file
    with open(csv_file_path, 'w') as file:
        file.write("IR,Xacc,Yacc,Zacc,GyroX,GyroY,GyroZ\n")
        file.write("\n".join(data) + "\n")
    
    label0_status.setText("CSV Saved")

# Function to record a data point (using IR, accelerometer, and gyroscope data)
def record_data():
    if is_recording:
        ir_value = hat_heartrate_2.getIr()
        x_acc, y_acc, z_acc = imu0.acceleration  # Get x, y, z acceleration
        gyro_x, gyro_y, gyro_z = imu0.gyro  # Get x, y, z gyroscope data
        
        if ir_value:  # Log only if IR value is available (could indicate valid reading)
            # Append data to the list
            data.append("{},{},{},{},{},{},{}".format(ir_value, x_acc, y_acc, z_acc, gyro_x, gyro_y, gyro_z))
            label0_val.setText(str(ir_value))
            label4_val.setText(str(x_acc))
            label5_val.setText(str(y_acc))
            label6_val.setText(str(z_acc))
            label7_val.setText(str(gyro_x))
            label8_val.setText(str(gyro_y))
            label9_val.setText(str(gyro_z))
            heartbeat()

# Function to send CSV data over serial
def send_data_as_csv():
    with open(csv_file_path, 'r') as file:
        csv_data = file.read()
        print(csv_data)  # Send the CSV data over serial
    label0_status.setText("CSV Sent")

# Function to simulate heartbeat visual effect with a flashing circle
# Function to simulate heartbeat visual effect with a flashing circle
def heartbeat():
    flashing_circle.setBgColor(0x000000)  # Turn off the circle (black) by default
    wait(0.2)
    flashing_circle.setBgColor(0xff0000)  # Flash the circle to white
    wait(0.2)
    flashing_circle.setBgColor(0x000000)  # Return to black after flashing

# Set up button callbacks
btnA.wasPressed(start_recording)     # Button A starts recording
btnB.wasPressed(stop_recording_and_save)  # Button B stops recording and saves data
btnC.wasPressed(send_data_as_csv)    # Button C sends data as CSV over serial

# Main loop
while True:
    if is_recording:
        record_data()
    wait_ms(100)  # Adjust the recording frequency as needed
