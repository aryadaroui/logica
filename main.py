import audioop
import aifc
from itertools import repeat
from math import ceil
from numpy import linspace
from functions import * # pylint: disable=unused-wildcard-import

INTRO = "logica v0.5 -- written by Arya Daroui\n\nlogica applies offline audio effects to an input .aif file:\ninverse: reverse chunks but preserve order\nconverse: chunks not reversed, but their order is\nreverse (contrapositive): reversed chunks and reversed order, effectively reversing the entire audio file\n"
INV = 1
CONV = 2
REV = 3
TRIV = 4

Clear()
print(INTRO)
inFilePath = input("please drag and drop the input .aif file: ")
inFilePath = inFilePath.rstrip()	# removes whitespace
inFilePath = inFilePath.rstrip('/')	# removes extra / at end
inFilePath = inFilePath.replace(r'\ ', ' ')	# removes extra escape character prefix
inFile = aifc.open(inFilePath, 'r')


Clear()
badMode = True
while badMode:
	mode = input("1 inverse\n2 converse\n3 reverse\n4 triverse\n5 diverse\nSelect mode: ")
	if mode == '1':
		modeStr = "-inverse"
		badMode = False
	elif mode == '2':
		modeStr = "-converse"
		badMode = False
	elif mode == '3':
		modeStr = "-reverse"
		badMode = False
	elif mode == '4':
		modeStr = "-triverse"
		badMode = False
	elif mode == '5':
		modeStr = "-diverse"
		badMode = False
	else:
		Clear()
		badMode = True

# PrintInfo(inFile)

Clear()
bpm = int(input("Tempo BPM: "))
chunkiness = float(input("chunkiness (chunk per beat): "))
# input if diverse and triverse should start on reverse

# if mode = '5':
# 	startRev = input
# bpm = 120
# chunkiness = .125
# logicMode = CONV

outfilePath = inFilePath.replace(".aif", modeStr + "-" + str(bpm) + "-" + str(chunkiness) + ".aif")
outFile = aifc.open(outfilePath, 'w')
outFile.aiff()
outFile.setparams(inFile.getparams())

# chunkSize = int((bpm / 60 * outFile.getframerate()) )

chunkSize = int(outFile.getframerate() * 60 * (1/bpm) * (1/chunkiness))

if mode == '1':
	# CONVERSE
	for _ in repeat(None, ceil(inFile.getnframes() / chunkSize)):
		chunk = inFile.readframes(chunkSize)
		outFile.writeframes(audioop.reverse(chunk, outFile.getsampwidth()))
elif mode == '2':
	#INVERSE
	for position in reversed(range(0, inFile.getnframes(), chunkSize)):
		inFile.setpos(position)
		chunk = inFile.readframes(chunkSize)
		outFile.writeframes(chunk)
	# could have also just reversed (contrapositiv-ed) the converse
elif mode == '3':
	#REVERSE
	for position in reversed(range(0, inFile.getnframes(), chunkSize)):
		inFile.setpos(position)
		chunk = inFile.readframes(chunkSize)
		outFile.writeframes(audioop.reverse(chunk, outFile.getsampwidth()))
elif mode == '4':
	#TRIVERSE
	for _ in repeat(None, ceil(inFile.getnframes() / chunkSize)):
		chunk = inFile.readframes(chunkSize)
		outFile.writeframes(chunk)
		outFile.writeframes(audioop.reverse(chunk, outFile.getsampwidth()))
		outFile.writeframes(chunk)
elif mode == '5':
	#DIVERSE
	for count in range(0, ceil(inFile.getnframes() / chunkSize)):
		chunk = inFile.readframes(chunkSize)
		if count % 2 == 1:
			# print(str(count) + "RN")
			outFile.writeframes(audioop.reverse(chunk, outFile.getsampwidth()))
			outFile.writeframes(chunk)
		else:
			# print(str(count) + "NR")
			outFile.writeframes(chunk)
			outFile.writeframes(audioop.reverse(chunk, outFile.getsampwidth()))


inFile.close()
outFile.close()
Clear()
print("OUTPUT at " + outfilePath)