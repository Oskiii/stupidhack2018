import time
import os
import sys

import pyaudio
import numpy as np
from numpy import genfromtxt
import math
from matplotlib.mlab import find
import csv
import curses

scsv = open("alphabet.csv", "r").read()
alphabetReader = csv.reader(scsv.split('\n'), delimiter=',')
alphabet = []

pythonLogo = open("pythonLogo.txt", "r").readlines()

#for line in pythonLogo:
#    print(line)

#time.sleep(1)

i = 0
for row in alphabetReader:
    alphabet.append(row)
    i += 1

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
RECORD_SECONDS = 0.2
init = False

currentFrequency = 0
currentNote = ""
codeString = ""


def Pitch(signal):
    signal = np.fromstring(signal, 'Int16');
    crossing = [math.copysign(1.0, s) for s in signal]

    index = find(np.diff(crossing))
    f0=round(len(index) *RATE /(2*np.prod(len(signal))))
    return f0;


p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
channels = CHANNELS,
rate = RATE,
input = True,
output = True,
frames_per_buffer = chunk)

notes = [
1219,
516,
580,
646,
703,
797,
891,
967,
1031
]

noteLetters = [
"Blank",
"C1",
"D",
"E",
"F",
"G",
"A",
"B",
"C2"
]

def freqToNote(freq):
    noteError = 40
    i = 0
    for note in notes:
        if abs(freq - note) < noteError:
            return i
        i += 1
    return -1

def printFromFrequencies(freq1, freq2):
    #print(freq1, freq2)


    firstIndex = freqToNote(freq1)
    secondIndex = freqToNote(freq2)

    if firstIndex == -1 or secondIndex == -1 or firstIndex == secondIndex:
        return

    global codeString
    character = ""
    try:
        character = str(alphabet[secondIndex][firstIndex])
    except:
        print("Error: ", str(firstIndex), str(secondIndex))
        exit()


    if character == "Back" and len(codeString) > 0:
        codeString = codeString[:-1]
    elif character == "Enter":
        character = "\n"
    elif character == "Tab":
        character = "\t"
    elif character == "Run":
        print("\n")
        exec(codeString)
        codeString = ""
        time.sleep(10)
    else:
        codeString += character




def main():

    # Initialization:
    print ("\n Initializing... \n")

    screen = curses.initscr()


    spinner = 0

    state = 0
    frequencies = []

    freq1 = 0
    freq2 = 0

    counter = 0

    while True:
        global currentFrequency
        global currentNote
        global init

        counter += 1

        data = stream.read(chunk, exception_on_overflow = False)
        frequency=Pitch(data)
        frequencies.append(frequency)
        #print(frequency)
        if len(frequencies) <= 30:
            continue

        frequencies.pop(0)
        #print (Frequency)
        avg = np.average(frequencies)
        std = np.std(frequencies)
        #print(avg, std)

        absoluteDifference1 = abs(freq2 - avg)
        absoluteDifference2 = abs(freq1 - avg)

        if std < 100:

            if state == 0:
                frequencies = []
                counter = -100
                state = 1
                freq1 = avg
                if freq1 > 1300:
                    freq1 = freq1 / 2
                currentFrequency = str(freq1)
                currentNote = str(noteLetters[freqToNote(freq1)])
                #print("freq1: ", freq1)
                time.sleep(0.3)
            elif state == 1 and absoluteDifference2 > 0.05 * freq1:
                frequencies = []
                counter = 0
                state = 2
                freq2 = avg
                if freq2 > 1300:
                    freq2 = freq1 / 2
                #print("freq2: ", freq2)
                printFromFrequencies(freq1, freq2)
                state = 0
                currentFrequency = 0
                currentNote = ""
                time.sleep(0.3)
            #print(absoluteDifference1, biggestAllowedDiff)
        elif counter > 181:
            state = 0
            counter = 0
            currentFrequency = ""
            currentNote = ""
            #print("RESET")


        #sys.stdout.write( "\r    ")
        printString = currentNote + " " + codeString
        #sys.stdout.write( "\r " + printString)
        #sys.stdout.flush()

        screen.clear()
        lineNum = 0

        for line in pythonLogo:
            screen.addstr(int(lineNum), 2, line)
            lineNum += 1

        screen.addstr(int(lineNum+2), 0, "\tBlank\tC1\tD\tE\tF\tG\tA\tB\tC2", curses.A_STANDOUT)
        screen.addstr(int(lineNum+3), 0, "Blank\t" + "\t".join(alphabet[0]))
        screen.addstr(int(lineNum+4), 0, "C1\t" + "\t".join(alphabet[1]))
        screen.addstr(int(lineNum+5), 0, "D\t" + "\t".join(alphabet[2]))
        screen.addstr(int(lineNum+6), 0, "E\t" + "\t".join(alphabet[3]))
        screen.addstr(int(lineNum+7), 0, "F\t" + "\t".join(alphabet[4]))
        screen.addstr(int(lineNum+8), 0, "G\t" + "\t".join(alphabet[5]))
        screen.addstr(int(lineNum+9), 0, "A\t" + "\t".join(alphabet[6]))
        screen.addstr(int(lineNum+10), 0, "B\t" + "\t".join(alphabet[7]))
        screen.addstr(int(lineNum+11), 0, "C2\t" + "\t".join(alphabet[8]))



        screen.addstr(int(lineNum+13), 0, "snakecharmer.io  H A S   B E E N   I N I T I A T E D")
        screen.addstr(int(lineNum+15), 0, "Freq\tStd")
        screen.addstr(int(lineNum+16),0,str(frequency) + "\t" + str(std))
        screen.addstr(int(lineNum+17), 0, "Note: " + currentNote)
        screen.addstr(int(lineNum+18), 0, codeString)
        screen.refresh()

        if not init:
            os.system("say snakecharmer has been initiated")
            init = True



curses.wrapper(main())
