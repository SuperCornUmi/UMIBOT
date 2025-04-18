import RPi.GPIO as GPIO
import time
import random

# GPIO Setup
GPIO.setmode(GPIO.BOARD)
PIN_LEFT = 33     # key_left
PIN_RIGHT = 38    # key_right
PIN_X = 22        # Board_X

GPIO.setup(PIN_LEFT, GPIO.OUT)
GPIO.setup(PIN_RIGHT, GPIO.OUT)
GPIO.setup(PIN_X, GPIO.OUT)

# Ensure all keys are released
GPIO.output(PIN_LEFT, GPIO.HIGH)
GPIO.output(PIN_RIGHT, GPIO.HIGH)
GPIO.output(PIN_X, GPIO.HIGH)

def press_key(pin, duration):
    """Simulate key press for the given duration (in seconds)"""
    GPIO.output(pin, GPIO.LOW)    # Press down
    time.sleep(duration)
    GPIO.output(pin, GPIO.HIGH)   # Release

try:
    # One-time startup delay
    print("? Starting in 2 seconds...")
    time.sleep(2)

    while True:
        print("?? Step 1: Press LEFT key")
        press_key(PIN_LEFT, random.uniform(0.4, 0.8))

        print("?? Step 2: Hold X key")
        press_key(PIN_X, random.uniform(2.5, 5.0))

        print("?? Step 3: Press RIGHT key")
        press_key(PIN_RIGHT, random.uniform(0.4, 0.8))

        print("?? Step 4: Hold X key again")
        press_key(PIN_X, random.uniform(2.5, 5.0))

        # No delay between cycles now

except KeyboardInterrupt:
    print("?? Interrupted by user. Cleaning up GPIO...")

finally:
    GPIO.cleanup()
