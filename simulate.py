#!/usr/bin/python

import random
import netCDF4
import numpy as n
from netCDF4 import Dataset
from numpy import arange, dtype

# The story is: There is a factory with two assembly lines.
# The assembly lines share a gate.
# The parallel sequences of two assembly lines are:
# FRAME_A_IN ->(2s) GATE ->(1.3s) ASSEMBLE_A ->(3.2s) PRODUCT_A_OUT
# FRAME_B_IN ->(1.5s) GATE ->(0.9s) ASSEMBLE_B ->(3.4s) PRODUCT_B_OUT
# There are multiple of above processes executing simultaneously.
# We expect any anomaly detection algorithm to learn the two sequences mixed together,
# and still detect the following anomalies:
# FRAME_A_IN -> GATE -> ASSEMBLE_B

eventIds = dict(
    FRAME_A_IN = 0,
    FRAME_B_IN = 1,
    GATE = 2,
    ASSEMBLE_A = 3,
    ASSEMBLE_B = 4,
    PRODUCT_A_OUT = 5,
    PRODUCT_B_OUT = 6
)
eventNames = [
    "FRAME_A_IN",
    "FRAME_B_IN",
    "GATE",
    "ASSEMBLE_A",
    "ASSEMBLE_B",
    "PRODUCT_A_OUT",
    "PRODUCT_B_OUT"
]

eventsA = []
eventsB = []

def nextEventFrameA(time_now):
    # FRAME_A_IN -> GATE -> ASSEMBLE_A -> PRODUCT_A_OUT
    delay = random.randint(0,100)
    time_now = time_now + delay
    eventsA.append(dict(
        event = "FRAME_A_IN",
        time = time_now
    ))
    delay = 2000 + random.randint(0,100)
    time_now = time_now + delay
    eventsA.append(dict(
        event = "GATE",
        time = time_now
    ))
    delay = 1300 + random.randint(0,100)
    time_now = time_now + delay
    eventsA.append(dict(
        event = "ASSEMBLE_A",
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
    delay = random.randint(0,100)
    time_now = time_now + delay
    eventsB.append(dict(
        event = "FRAME_B_IN",
        time = time_now
    ))
    delay = 1500 + random.randint(0,100)
    time_now = time_now + delay
    eventsB.append(dict(
        event = "GATE",
        time = time_now
    ))
    delay = 900 + random.randint(0,100)
    time_now = time_now + delay
    eventsA.append(dict(
        event = "ASSEMBLE_B",
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

rootgrp = Dataset("test.nc", "w", format="NETCDF4")

# Dimensions
#    numSeqs = Number of sequences
#    numTimesteps = Total number of timesteps
#    inputPattSize = Size of each input pattern (= number of input neurons)
#    maxSeqTagLength = Maximum length of a sequence tag

numSeqs = 1
numTimesteps = len(sortedEvents)-1
# Number of states
inputPattSize = len(eventNames)
maxSeqTagLength = 1

rootgrp.createDimension("numSeqs", numSeqs)
rootgrp.createDimension("numTimesteps", numTimesteps)
rootgrp.createDimension("inputPattSize", inputPattSize)
rootgrp.createDimension("maxSeqTagLength", maxSeqTagLength)

# For classification:
# dimensions:
#    numLabels = Number of target classes

# Outputs are just next inputs.
numLabels = inputPattSize
rootgrp.createDimension("numLabels", numLabels)

# Variables

#    char seqTags(numSeqs, maxSeqTagLength) = Tag (name) for each sequence
#    int seqLengths(numSeqs) = Length of each sequence
#    float inputs(numTimesteps, inputPattSize) = Input Patterns

# For classification:
# variables:
#    int targetClasses(numTimesteps) = Target classes (one for each timestep)

seqTagsVar = rootgrp.createVariable("seqTags", dtype("S1").char,
    ("numSeqs", "maxSeqTagLength"))

seqTagsVar[0] = n.array("a")

seqLengths = [numTimesteps]
seqLengthsVar = rootgrp.createVariable("seqLengths", dtype("int").char, ("numSeqs"))
seqLengthsVar[:] = n.array(seqLengths)

inputs = []
# Removing the last input, because it doesn't have a defined next state.
inputEvents = sortedEvents[:-1]
# Removing the first output, because it doesn't have a defined previous state.
outputEvents = sortedEvents[1:]

for event in inputEvents:
    pattern = [0.0 for x in range(inputPattSize)]
    pattern[eventIds[event["event"]]] = 1.0
    inputs.append(pattern)

inputsVar = rootgrp.createVariable("inputs", dtype("float").char,
    ("numTimesteps", "inputPattSize"))
inputsVar[:] = n.array(inputs)

targetClasses = []
for event in outputEvents:
    targetClasses.append(eventIds[event["event"]])

targetClassesVar = rootgrp.createVariable("targetClasses", dtype("int").char, ("numTimesteps"))
targetClassesVar[:] = n.array(targetClasses)

rootgrp.close()

