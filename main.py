import audioop
import aifc
from itertools import repeat
from math import ceil
from functions import * # pylint: disable=unused-wildcard-import

Clear()

NORM = 0
INV = 1
CONV = 2
REV = 3

inFile = aifc.open("test.aif", 'r')
outFile = aifc.open("output.aif", 'w')
outFile.aiff()
outFile.setparams(inFile.getparams())

PrintInfo(inFile)

# bpm = input("BPM: ")
# chunkRate = input("chunk factor: ")
# logicMode = input("logic mode: ")
bpm = 120
chunkiness = .3
logicMode = CONV

chunkSize = int(bpm / 60 * outFile.getframerate() * chunkiness)

for _ in repeat(None, ceil(inFile.getnframes() / chunkSize)):
	chunk = inFile.readframes(chunkSize)
	outFile.writeframes(audioop.reverse(chunk, outFile.getsampwidth()))



inFile.close()
outFile.close()
print("END\n")