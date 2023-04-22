"""Contains functions used to control the arm movement of the robot

This module implements functions which tell the robot to start moving in a certain
direction as well as a command to stop. It also includes a test script if run directly.
"""
import serial
import time

def move_arm(target_pos):
    with serial.Serial("/dev/ttyACM1", 9600) as ser:
        time.sleep(3)
        adj_pos = str(target_pos + 100)
        ser.write(adj_pos.encode('utf-8'))
        print('Moved arm to', target_pos, 'position')
        time.sleep(3)

if __name__ == "__main__":
    sleep_time = 3
    print("Initializing")
    time.sleep(sleep_time)
    move_arm(5)
    time.sleep(sleep_time)
    move_arm(10)
    time.sleep(sleep_time)
    move_arm(15)
    time.sleep(sleep_time)
    move_arm(5)
    time.sleep(sleep_time)
    move_arm(17)
    time.sleep(sleep_time)
    move_arm(0)
    print('Ended')
