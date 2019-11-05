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
	mode = input("1 inverse\n2 converse\n3 reverse\nSelect mode: ")
	if mode == '1':
		modeStr = "-inverse"
		badMode = False
	elif mode == '2':
		modeStr = "-converse"
		badMode = False
	elif mode == '3':
		modeStr = "-reverse"
		badMode = False
	else:
		badMode = True

outfilePath = inFilePath.replace(".aif", modeStr + ".aif")
outFile = aifc.open(outfilePath, 'w')
outFile.aiff()
outFile.setparams(inFile.getparams())


# PrintInfo(inFile)

Clear()
bpm = int(input("Tempo BPM: "))
chunkiness = int(input("chunkiness (chunk per beat): "))
# bpm = 120
# chunkiness = .125
# logicMode = CONV

chunkSize = int((bpm / 60 * outFile.getframerate()) / chunkiness)

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
else:
	#REVERSE
	for position in reversed(range(0, inFile.getnframes(), chunkSize)):
		inFile.setpos(position)
		chunk = inFile.readframes(chunkSize)
		outFile.writeframes(audioop.reverse(chunk, outFile.getsampwidth()))

inFile.close()
outFile.close()
print("OUTPUT at " + outfilePath)