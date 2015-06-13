#!/usr/bin/python

import random

# The story is: There is a factory with two assembly lines.
# The assembly lines share a gate.
# The parallel sequences of two assembly lines are:
# FRAME_A_IN ->(2s) GATE ->(1.3s) ASSEMBLE_A ->(3.2s) PRODUCT_A_OUT
# FRAME_B_IN ->(1.5s) GATE ->(0.9s) ASSEMBLE_B ->(3.4s) PRODUCT_B_OUT
# There are multiple of above processes executing simultaneously.
# We expect any anomaly detection algorithm to learn the two sequences mixed together,
# and still detect the following anomalies:
# FRAME_A_IN -> GATE -> ASSEMBLE_B

eventsA = []
eventsB = []

def nextEventFrameA(time_now):
    # FRAME_A_IN -> GATE -> ASSEMBLE_A -> PRODUCT_A_OUT
    delay = 2000 + random.randint(0,100)
    time_now = time_now + delay
    eventsA.append(dict(
        event = "FRAME_A_IN",
        time = time_now
    ))
    delay = 1300 + random.randint(0,100)
    time_now = time_now + delay
    eventsA.append(dict(
        event = "GATE",
        time = time_now
    ))
    delay = 3200 + random.randint(0,100)
    time_now = time_now + delay
    eventsA.append(dict(
        event = "PRODUCT_A_OUT",
        time = time_now
    ))
    return time_now;

def nextEventFrameB(time_now):
    # FRAME_B_IN ->(1.5s) GATE ->(0.9s) ASSEMBLE_B ->(3.4s) PRODUCT_B_OUT
    delay = 1500 + random.randint(0,100)
    time_now = time_now + delay
    eventsB.append(dict(
        event = "FRAME_B_IN",
        time = time_now
    ))
    delay = 900 + random.randint(0,100)
    time_now = time_now + delay
    eventsB.append(dict(
        event = "GATE",
        time = time_now
    ))
    delay = 3400 + random.randint(0,100)
    time_now = time_now + delay
    eventsB.append(dict(
        event = "PRODUCT_B_OUT",
        time = time_now
    ))
    return time_now


RUNNING_TIME = 10000000
# 10000 s
time_now = 0

while (time_now <= RUNNING_TIME):
    time_now = nextEventFrameA(time_now)

time_now = 0

while (time_now <= RUNNING_TIME):
    time_now = nextEventFrameB(time_now)


# Joining together.
sortedEvents = eventsA + eventsB

sortedEvents = sorted(sortedEvents, key=lambda e: e['time'])

print sortedEvents
# TODO: NetCDF output for CURRENNT
