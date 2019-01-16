import pyaudio
import wave
import contextlib
import sys
from threading import *
import random
import time
import copy

# length of data to read.
#chunk = 1024

beats = [ 0.42956915,  0.85913831,  1.30031741,  1.71827662,  2.14784575,
        2.57741499,  2.9953742 ,  3.42494321,  3.85451245,  4.29569149,
        4.72526073,  5.15482998,  5.58439922,  6.01396799,  6.4319272 ]

bpm = 140
'''
************************************************************************
      This is the start of the "minimum needed to read a wave"
************************************************************************
'''

def get_duration(filename='download.wav'):
    with contextlib.closing(wave.open(filename,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration

def play_wav(filename='download.wav'):

    chunk = 1024
    # open the file for reading.
    wf = wave.open(filename, 'rb')

    # create an audio object
    p = pyaudio.PyAudio()

    # open stream based on the wave object which has been input.
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)


    def play():
        # read data (based on the chunk size)
        data = wf.readframes(chunk)

        # play stream (looping from beginning of file to the end)
        while len(data) > 0:
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            data = wf.readframes(chunk)

    def close():
        # cleanup stuff.
        stream.stop_stream()
        stream.close()    
        p.terminate()

    play()
    close()

def get_beat_diff(lst):
    beats = []
    for i in range(0,len(lst)):
        if (i == 0): continue
        else:
            prev_beat = lst[i-1]
            beat = lst[i]
            beats.append(round(beat,2)-round(prev_beat,2))
    return beats


def build_beats(patterns,filename='download.wav'):
    dur = get_duration(filename)
    bps = bpm/60
    bs = (.60/bps)

    beats_norm = []
    total = 0
    curr_patt = []
    beatnotes = []
    while total < dur:
        if (len(curr_patt) <= 0):
            r = random.randint(0,len(patterns)-1)
            curr_patt = copy.deepcopy(patterns[r])
        total += bs
        if (total < dur):
            beats_norm.append(total)
            beatnotes.append(curr_patt.pop(0))
    print(beatnotes)
    return (beatnotes,beats_norm)


def time_beats(lst,dirlist):
    global bts
    global dirs
    bts = lst
    dirs = dirlist
    def timer_handler():
        global bts
        global dirs
        print(dirs[0])
        if (len(bts) > 0):
            beat = bts[0]
            bts = bts[1:]
            dirs = dirs[1:]
            t = Timer(beat, timer_handler)
            t.start()

    if len(bts) != 0:
        beat = bts[0]
        t = Timer(beat, timer_handler)
        bts = bts[1:]
        t.start()

def build_patterns(num=15):
    dirs = ['up','down','left','right',None,None,None,None,None,None]
    patterns = []
    for i in range(0,num):
        r = random.randint(1,8)
        pattern = []
        if (i % 2 == 0): 
            for j in range(0,r):
                t = random.randint(0,9)
                pattern.append(dirs[t])
        else:
            for j in range(0,r):
                pattern.append(None)
        patterns.append(pattern)
    return patterns


patts = build_patterns()
bdirs,bts2 = build_beats(patts)
diffs = get_beat_diff(bts2)

print(get_duration())




t1 = Thread(target=play_wav)
t2 = Thread(target=time_beats, args=(diffs,bdirs))
t1.start()
t2.start()
t1.join()
t2.join()
print(bts2)