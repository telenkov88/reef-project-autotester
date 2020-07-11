#!/usr/bin/python
# Import required libraries
import sys
import time
import RPi.GPIO as GPIO
import atexit
import logging
import logging.config
import socket
import multiprocessing
import signal
import os
import requests

# Steppers pins 1-2-3-4
pinsmap = [[13, 19, 26, 21],  # Channel 0
           [20, 16, 12, 1],   # Channel 1
           [17, 27, 22, 10],  # Channel 2
           [9, 11, 5, 6]]     # Channel 3


def init_gpio():
    # Use BCM GPIO references
    # instead of physical pin numbers
    GPIO.setmode(GPIO.BCM)
    for StepPins in pinsmap:
        for pin in StepPins:
            GPIO.output(pin, False)


def pump(channel, steps, StepPins, direction):
    GPIO.setmode(GPIO.BCM)
    print(f"Run {steps} steps")
    count = 0

    def exit_handler():
        print(">>>>>>>>>>>>>>>>>>>>> EXIT")
        for pin in StepPins:
            GPIO.output(pin, False)
        print(f"Count: {count}")
        pump_steps = count
        print("Exit handler")
        return count

    def signal_handler(signal, frame):
        print(">>>>>>>>>>>>>>>>>>>>> EXIT")
        for pin in StepPins:
            GPIO.output(pin, False)
        print(f"Count: {count}")

        try:
            print(requests.post('http://10.123.0.200:5000/get_count', json={f"channel_{channel}": count}))
        except:
            print("Exit error")
        print("Signal handler")
        sys.exit(0)

    atexit.register(exit_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Set all pins as output
    for pin in StepPins:
        print("Setup pins")
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

    # Define advanced sequence
    # as shown in manufacturers datasheet
    Seq = [[1, 0, 0, 1],
           [1, 0, 0, 0],
           [1, 1, 0, 0],
           [0, 1, 0, 0],
           [0, 1, 1, 0],
           [0, 0, 1, 0],
           [0, 0, 1, 1],
           [0, 0, 0, 1]]

    StepCount = len(Seq)
    StepDir = 1  # Set to 1 or 2 for clockwise
    # Set to -1 or -2 for anti-clockwise

    # Read wait time from command line
    WaitTime = 10 / float(1000)
    # Initialise variables
    StepCounter = 0

    # Start main loop
    for StepCounter in range(0, 7):
        count += 1
        # print(Seq[StepCounter])
        for pin in range(0, 4):
            xpin = StepPins[pin]  #
            if Seq[StepCounter][pin] != 0:
                # print(" Enable GPIO %i" % (xpin))
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)

        time.sleep(1 / 50)
    while count < steps:
        for StepCounter in range(0, 7):
            if count < steps:
                count += 1
            else:
                break
            # print(StepCounter)
            # print(Seq[StepCounter])
            for pin in range(0, 4):
                xpin = StepPins[pin]  #
                if Seq[StepCounter][pin] != 0:
                    # print(" Enable GPIO %i" % (xpin))
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)
            time.sleep(1 / 300)
    for pin in StepPins:
        GPIO.output(pin, False)

    print(f"Count: {count}")
    return count


class StepperPumps(object):
    def __init__(self, channel):
        self.logger = logging.getLogger("server")
        self.channel = channel
        self.StepPins = pinsmap[channel]

    def start(self, steps, direction=1):
        for child in multiprocessing.active_children():
            child.terminate()
        self.pump = multiprocessing.Process(target=pump, args=(self.channel, steps, self.StepPins, direction))
        print(f"Start pump No{self.channel}")
        self.pump.daemon = True
        self.pump.start()

    def stop(self):
        if self.pump.is_alive():
            print("Process alive, stopping")
            os.kill(self.pump.pid, signal.SIGINT)
            time.sleep(0.1)
            self.pump.terminate()

if __name__ == '__main__':
    print("hello")
    #pump(100, [20, 16, 12, 1], 1)

    pump1 = StepperPumps(1)
    pump1.start(10000, 1)
    time.sleep(0.3)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>.")
    pump1.start(10000, 1)
    time.sleep(0.3)
    pump1.stop()