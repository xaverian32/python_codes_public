from machine import I2C, Pin
import time

# LSM6DSRTR default I2C address
LSM6DSRTR_ADDR = 0x6A

# LSM6DSRTR registers
CTRL2_G = 0x11  # Control register for gyroscope
OUTX_L_G = 0x22  # Gyroscope X-axis low byte
OUTX_H_G = 0x23  # Gyroscope X-axis high byte
OUTY_L_G = 0x24  # Gyroscope Y-axis low byte
OUTY_H_G = 0x25  # Gyroscope Y-axis high byte
OUTZ_L_G = 0x26  # Gyroscope Z-axis low byte
OUTZ_H_G = 0x27  # Gyroscope Z-axis high byte

# Initialize I2C interface
# Modify Pin numbers (e.g., 21 and 22) based on your wiring
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

def write_register(register, value):
    i2c.writeto_mem(LSM6DSRTR_ADDR, register, bytes([value]))

def read_register(register, num_bytes):
    return i2c.readfrom_mem(LSM6DSRTR_ADDR, register, num_bytes)

def initialize_gyroscope():
    # Set gyroscope to 208 Hz, 500 dps range
    write_register(CTRL2_G, 0b01101000)

def read_gyroscope():
    # Read X, Y, Z gyroscope data (2 bytes each)
    gx_l = read_register(OUTX_L_G, 1)[0]
    gx_h = read_register(OUTX_H_G, 1)[0]
    gy_l = read_register(OUTY_L_G, 1)[0]
    gy_h = read_register(OUTY_H_G, 1)[0]
    gz_l = read_register(OUTZ_L_G, 1)[0]
    gz_h = read_register(OUTZ_H_G, 1)[0]

    # Combine high and low bytes (2's complement for signed values)
    gx = (gx_h << 8 | gx_l)
    if gx > 32767:
        gx -= 65536

    gy = (gy_h << 8 | gy_l)
    if gy > 32767:
        gy -= 65536

    gz = (gz_h << 8 | gz_l)
    if gz > 32767:
        gz -= 65536

    return gx, gy, gz

# Main program
initialize_gyroscope()

while True:
    gx, gy, gz = read_gyroscope()
    print(f"Gyroscope: X={gx}, Y={gy}, Z={gz}")
    time.sleep(0.1)
