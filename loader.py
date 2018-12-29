import sys

def loadProgram():
	return sys.stdin.read()

def pickLevel():
	argv0, level = sys.argv
	return int(level)
