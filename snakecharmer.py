import time
import os
import sys

import pyaudio
import numpy as np
import math
from matplotlib.mlab import find

chunk = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
RECORD_SECONDS = 0.2


def Pitch(signal):
    signal = np.fromstring(signal, 'Int16');
    crossing = [math.copysign(1.0, s) for s in signal]
    index = find(np.diff(crossing));
    f0=round(len(index) *RATE /(2*np.prod(len(signal))))
    return f0;


p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
channels = CHANNELS,
rate = RATE,
input = True,
output = True,
frames_per_buffer = chunk)



def main():

    # Initialization:
    print ("\n Initializing... \n")

    print("\n snakecharmer.io  H A S   B E E N   I N I T I A T E D \n")
    #os.system("say snakecharmer has been initiated")

    spinner = 0

    state = 0
    frequencies = []

    freq1 = 0
    freq2 = 0

    counter = 0

    while True:
        counter += 1

        data = stream.read(chunk, exception_on_overflow = False)
        frequency=Pitch(data)
        frequencies.append(frequency)
        #print(frequency)
        if len(frequencies) <= 10:
            continue

        frequencies.pop(0)
        #print (Frequency)
        avg = np.average(frequencies)
        std = np.std(frequencies)
        #print(avg, std)

        absoluteDifference1 = abs(freq2 - avg)
        absoluteDifference2 = abs(freq1 - avg)

        if std < 40:
            if state == 0 and absoluteDifference1 > 0.05 * freq2:
                frequencies = []
                counter = 0
                state = 1
                freq1 = avg
                #print("freq1", freq1, std)
            elif state == 1 and absoluteDifference2 > 0.05 * freq1:
                frequencies = []
                counter = 0
                state = 2
                freq2 = avg
                #print("freq2")
                print(freq1, freq2)
                state = 0
            #print(absoluteDifference1, biggestAllowedDiff)
        elif counter > 181:
            state = 0
            counter = 0
            #print("RESET")



        #time.sleep(RECORD_SECONDS)
        #sys.stdout.write("\r" )
        #sys.stdout.flush()



main()
