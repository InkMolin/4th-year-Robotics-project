"""Contains functions used to control the movement of the robot

This module implements functions which tell the robot to start moving in a certain
direction as well as a command to stop. It also includes a test script if run directly.
"""
import serial
import time
import robotLocalization as rl

# Define serial communication port and baud rate
ser = serial.Serial("/dev/ttyACM1", 9600)

def forward():
    ser.write(b'1\r')
    print("Moving Forward")

def backward():
    ser.write(b'2\r')
    print("Moving Backward")

def left():
    ser.write(b'3\r')
    print("Moving Left")

def right():
    ser.write(b'4\r')
    print("Moving Right")

def anticlockwise():
    ser.write(b'5\r')
    print("Moving Anti-Clockwise")

def clockwise():
    ser.write(b'6\r')
    print("Moving Clockwise")

def stop():
    ser.write(b'7\r')
    print("Stopped")

def move_arm(target_pos):
    adj_pos = str(target_pos + 100) + '\r'
    ser.write(adj_pos)
    print('Moved arm to', target_pos, 'position')

def move_to_target(targets, angle=0, speed = [10,10], pos_threshold=0.3):
    at_position = False
    min_move_time = 0.2
    while True:
        current_loc = rl.get_position()
        x_diff = targets['x'] - float(current_loc['x'])
        y_diff = targets['y'] - float(current_loc['y'])
        print(x_diff, y_diff)
        if abs(x_diff) < pos_threshold and abs(y_diff) < pos_threshold:
            stop()
            break
        elif abs(x_diff) > pos_threshold:
            move_time = abs(x_diff)/speed[0]
            if x_diff > 0:
                left()
            elif x_diff < 0:
                right()
        else:
            stop()

        if abs(x_diff) < pos_threshold and abs(y_diff) > pos_threshold:
            move_time = abs(y_diff)/speed[1]
            if y_diff > 0:
                forward()
            elif y_diff < 0:
                backward()

        if move_time < min_move_time:
            move_time = min_move_time

        time.sleep(move_time)
    
    # Depending on x_diff and y_diff, if x and y diff increases stop program and see difference
    # DO BOTH SIMULTANEOUSLY
    # Move forward/backwards
    # Move left/right
    # every 0.5s get new location and check if within threshold


if __name__ == "__main__":
    print("Initializing")
    time.sleep(2)
    forward()
    time.sleep(3)
    stop()
    time.sleep(1)
    backward()
    time.sleep(3)
    stop()
    time.sleep(1)
    left()
    time.sleep(3)
    stop()
    time.sleep(1)
    right()
    time.sleep(3)
    stop()
    time.sleep(1)
    anticlockwise()
    time.sleep(4)
    stop()
    time.sleep(1)
    clockwise()
    time.sleep(4)
    stop()
    time.sleep(1)
