# Simple Library for Implementing Robot Control

# Import Library for GPIO Control
import RPi.GPIO as GPIO
import time

upPin = 13
downPin = 15
leftPin = 16
rightPin = 18
RRotPin = 29
LRotPin = 31

GPIO.setmode(GPIO.BOARD)

GPIO.setup(upPin, GPIO.OUT)
GPIO.setup(downPin, GPIO.OUT)
GPIO.setup(leftPin, GPIO.OUT)
GPIO.setup(rightPin, GPIO.OUT)

def move_left_time(duration = 1):
    GPIO.output(leftPin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(leftPin, GPIO.LOW)

def move_right_time(duration = 1):
    GPIO.output(rightPin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(rightPin, GPIO.LOW)

def move_up_time(duration = 1):
    GPIO.output(upPin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(upPin, GPIO.LOW)

def move_down_time(duration = 1):
    GPIO.output(downPin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(downPin, GPIO.LOW)

def rotate_right_time(duration = 1):
    GPIO.output(RRotPin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(RRotPin, GPIO.LOW)

def force_stop():
    GPIO.output(downPin, GPIO.LOW)
    GPIO.output(upPin, GPIO.LOW)
    GPIO.output(rightPin, GPIO.LOW)
    GPIO.output(leftPin, GPIO.LOW)

# Code to test the libary
if __name__ == "__main__":
    move_left_time()
    move_right_time()
    move_up_time()
    move_down_time()
    rotate_right_time()
    GPIO.cleanup()
    