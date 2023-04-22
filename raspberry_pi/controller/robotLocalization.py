"""Contains functions used to determine the location of the robot

This module implements functions which tell the robot to start moving in a certain
direction as well as a command to stop. It also includes a test script if run directly.
"""
import serial
import time

# Initial connection setup
DWM = serial.Serial(port="/dev/ttyACM0", baudrate=115200)
# print("Connected to " + DWM.name)
DWM.write("\r\r".encode())
# print("Encode")
time.sleep(1)

# Returns (x,y,z) position of robot when called
def get_position(debug = False):
    DWM.write("lep\r".encode())
    time.sleep(1)
    # Keep reading until position returned
    while True:
        data = DWM.readline()
        if(data):
            if debug: print(data)
            try:
                data_list = data.decode().split(',')
                if debug: print(data_list)
                if data_list[0] == 'POS':
                    DWM.write("\r".encode())
                    current_loc = {
                        'x': data_list[1],
                        'y': data_list[2],
                        'z': data_list[3],
                    }
                    return current_loc
            except:
                print('No position')

def remap_target(angle, target_loc):
    pass
    # return remap_target_loc

# Some function that calculates the current robot angle
def get_current_angle():
    pass

if __name__ == "__main__":
    print("Initializing")
    location = get_position()
    print(location)
