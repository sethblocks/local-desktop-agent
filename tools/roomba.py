#
# Irobot Roomba Support
#
import serial
import time
from langchain_core.tools import tool
@tool
def drive(distance: int, radius: int):
    """Drives the robot as far as distance, with a turn radius of radius. Lower turn radius makes a tighter turn and can be from -200 (right) to 200 (left). The distance is how far to drive, a tighter turn radius such as 1 will turn in place.
    For example: velocity 200 and radius 0 will drive forward 200mm
    distance 200 and radius 1 will turn left in place 200mm
    distance 100 and radius -1 will turn right in place 100mm"""
    try:
        ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
    except:
        return "There is no Roomba Robot Vacuum Available"
    

    ser.write(bytes(bytes([137]) + (500).to_bytes(2, 'big', signed=True) + (radius).to_bytes(2, 'big', signed=True))) #Forward Drive Command
    time.sleep(distance/500)
    ser.write(bytes([137,0,0,0,0]))

    ser.close()
    return "Drive successfull"


if __name__ == "__main__":
    print("start")
    drive(-200, 0)
    
    