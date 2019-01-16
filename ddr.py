# External module imports
import RPi.GPIO as GPIO
import time
from evdev import InputDevice, categorize, ecodes

import pyaudio
import wave
import sys

import random
import contextlib
import threading


from essentia.standard import *

import copy
import os




# Pin Definitons:
green = [18, 19, 20, 21, 22]	# RIGHT
red = [23, 24, 25, 26, 27]		# UP
blue = [17, 16, 13, 12, 6] 		# DOWN
yellow = [5, 4, 7, 8, 10]  		# LEFT

song_cache = dict()

# ROW-COL COORDINATES TO GPIO PINS MAPPING
cor_map = {
	(0, 0) : 5,
	(0, 1) : 4,
	(0, 2) : 7,
	(0, 3) : 8,
	(0, 4) : 10,
	(1, 0) : 17,
	(1, 1) : 16,
	(1, 2) : 13,
	(1, 3) : 12,
	(1, 4) : 6,
	(2, 0) : 23,
	(2, 1) : 24,
	(2, 2) : 25,
	(2, 3) : 26,
	(2, 4) : 27,
	(3, 0) : 18,
	(3, 1) : 19,
	(3, 2) : 20,
	(3, 3) : 21,
	(3, 4) : 22
}

board = [
			[False, False, False, False, False],  # LEFT ARROW
			[False, False, False, False, False],  # DOWN ARROW
			[False, False, False, False, False],  # UP ARROW
			[False, False, False, False, False]   # RIGHT ARROW
		]
	

test = ["Up", "Down", None, None, "Right", "Right", "Left"]

def update_board(move):
	if move == "Left":
		i = 0
	elif move == "Down":
		i = 1
	elif move == "Up":
		i = 2
	elif move == "Right":
		i = 3
	else:
		i = -1

	for (j, row) in enumerate(board):
		board[j] = row[1:] + [i == j]

def display_board():
	for i in range(len(board)):
		for j in range(len(board[i])):
			val = board[i][j]
			pin = cor_map[(i, j)]
			if val:
				GPIO.output(pin, GPIO.HIGH)
			else:
				GPIO.output(pin, GPIO.LOW)


def get_mat_input(mat):
	event = mat.read_one()
	move = None
	while (event != None):
		if event.type == ecodes.EV_KEY and event.value:
			if event.code == 290:
				move = "Up"
			elif event.code == 291:
				move = "Right"
			elif event.code == 288:
				move = "Left"
			elif event.code == 289:
				move = "Down"
		event = mat.read_one()
	return move



# print('Import Completed')

# loader = MonoLoader(filename=audiofile)


# audio = loader()



# rhythm_extractor = RhythmExtractor2013(method="multifeature")
# bpm, beats, beats_conf, _, beats_intervals = rhythm_extractor(audio)

# print('BPM:', bpm)

# print('Audio Loaded')

def get_duration(filename):
	with contextlib.closing(wave.open(filename,'r')) as f:
		frames = f.getnframes()
		rate = f.getframerate()
		duration = frames / float(rate)
		return duration

def build_patterns(num=15):
	dirs = ['Up','Down','Left','Right',None,None]
	patterns = []
	for i in range(0,num):
		r = random.randint(1,8)
		pattern = []
		for j in range(0,r):
			t =  random.randint(0,5)
			pattern.append(dirs[t])
		patterns.append(pattern)
	return patterns


def build_beats(patterns, bpm, filename='audiofiles/download.wav'):
	dur = get_duration(filename)
	bps = bpm/60
	bs = (1/bps)

	print("Seconds per beat:", bs)

	beats_norm = []
	total = 0
	curr_patt = []
	beatnotes = []
	while total < dur:
		if (len(curr_patt) <= 0):
			if (random.randint(0,6) != 0):
			    r = random.randint(0,len(patterns)-1)
			    curr_patt = copy.deepcopy(patterns[r])
			else:
				r = random.randint(1,8)
				curr_patt = copy.deepcopy([None]*r)
		total += bs
		if (total < dur):
			#beats_norm.append(total)
			beatnotes.append(curr_patt.pop(0))
	print(beatnotes)
	return (beatnotes,bs)

def play_wav(filename='audiofiles/download.wav'):
	wf = wave.open(filename,'rb')

	p = pyaudio.PyAudio()

	chunk = 1024

	stream = p.open(format =
		            p.get_format_from_width(wf.getsampwidth()),
		            channels = wf.getnchannels(),
		            rate = wf.getframerate(),
		            output = True)

	data = wf.readframes(chunk)

	while len(data) > 0:

		stream.write(data)
		data = wf.readframes(chunk)

	stream.close()
	p.terminate()

# print('Building Patterns')
# patts = build_patterns()
# print('Building Beats')
# bdirs,bs = build_beats(patts,audiofile)

def select_song():
	print("Select a song number from the following list and press enter")
	songs = []
	for file_name in os.listdir("audiofiles"):
		if file_name.endswith(".wav"):
			songs.append(file_name)

	for (i, song_name) in enumerate(songs):
		print "%d. %s" % (i + 1, song_name)
	i = input("Song Number: ")
	song_name = songs[i-1]
	print "Processing: %s" % song_name
	return song_name

def get_bpm(file_name):
	loader = MonoLoader(filename=file_name)
	audio = loader()
	rhythm_extractor = RhythmExtractor2013(method="multifeature")
	bpm, beats, beats_conf, _, beats_intervals = rhythm_extractor(audio)
	return bpm

def play_game(arrows, sec_per_beat):

    # Pin Setup:
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
    # LED pin set as output
    GPIO.setup(yellow + blue + red + green, GPIO.OUT, initial=GPIO.LOW)
    device = InputDevice("/dev/input/event0")

    for i in range(4):
    	new_arrow = arrows[i]
    	update_board(new_arrow)
    	display_board()
    	time.sleep(sec_per_beat)

    for i in range(4, len(arrows)):
    	new_arrow = arrows[i]
    	cur_arrow = arrows[i - 4]
    	update_board(new_arrow)
    	display_board()
    	time.sleep(sec_per_beat)
    	if cur_arrow == get_mat_input(device) and cur_arrow != None:
    		print "Yay!"

    for i in range(len(arrows) - 3, len(arrows)):
    	cur_arrow = arrows[i]
    	update_board(None)
    	display_board()
    	time.sleep(sec_per_beat)
    	if cur_arrow == get_mat_input(device) and cur_arrow != None:
    		print "Yay!"

    time.sleep(sec_per_beat)
    GPIO.cleanup()

def main():
	print("Import complete")
	while True:
		song_name = "audiofiles/" + select_song()
		if not song_name in song_cache:
			bpm = get_bpm(song_name)
			(arrows, sec_per_beat) = build_beats(build_patterns(), bpm, song_name)
			song_cache[song_name] = (arrows, sec_per_beat)
		else:
			(arrows, sec_per_beat) = song_cache[song_name]
		t1 = threading.Thread(target=play_wav,args=(song_name,))
		t1.daemon = True
		t1.start()
		play_game(arrows, sec_per_beat)
		t1.join()
try:
	main()
except KeyboardInterrupt:
	GPIO.cleanup()



# print('Starting Threads')
# t1 = threading.Thread(target=play_wav,args=(audiofile,))
# t1.start()
# main(bdirs,bs)
# print('Finished')
    


