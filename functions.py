import os

def Clear():
	"""Clear terminal"""
	os.system('clear')

def PrintInfo(audiofile):
	print("  " + str(audiofile.getnchannels()) + " channel(s)\n  " + str(audiofile.getsampwidth() * 8) + "-bit samples\n  " + str(audiofile.getframerate()) + " samples per second\n  " + str(audiofile.getnframes()) + " total samples")
