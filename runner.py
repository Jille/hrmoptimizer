import collections

import instructions
import parser
import pprint
import blocks
import levelloader

class ExecutionException(Exception):
	pass

class WrongOutputException(ExecutionException):
	pass

class State(object):
	def __init__(self, input, expected, tiles, initializedTiles={}):
		def _reset():
			self.input = list(input)
			self.output = []
			self.expected = list(expected)
			self.hand = None
			self.tiles = [None for i in range(tiles)]
			for k, v in initializedTiles.items():
				self.tiles[k] = v
		_reset()
		self.reset = _reset

	@classmethod
	def fromLevel(cls, level, example=0):
		l = levelloader.levels[level]
		return cls(l.examples[example][0], l.examples[example][1], l.tiles, l.initializedTiles)

	def _deref(self, argument):
		"""Dereference argument if needed. Turns [0] into the value of tile 0."""
		if isinstance(argument, int):
			return argument
		assert argument.startswith('[') and argument.endswith(']')
		return self.tiles[int(argument[1:-1])]

	def get(self, argument):
		return self.tiles[self._deref(argument)]

	def set(self, argument, value):
		self.tiles[self._deref(argument)] = value

	def assertHandNotEmpty(self):
		if self.hand is None:
			raise ExecutionException("hand is empty")

	def __str__(self):
		return "State[%s, [%s]]" % (self.hand, self.tiles)

def run(block, state):
	state.reset()
	blockUses = {b: 0 for b in blocks.allBlocks(block)}
	try:
		while True:
			blockUses[block] += 1
			for instr in block.instructions:
				print str(instr)
				instr.do(state)
				print state
			if block.endJump == instructions.JumpZ:
				state.assertHandNotEmpty()
				if state.hand == 0:
					block = block.conditionalDestination
				else:
					block = block.defaultDestination
			elif block.endJump == instructions.JumpN:
				state.assertHandNotEmpty()
				if state.hand < 0:
					block = block.conditionalDestination
				else:
					block = block.defaultDestination
			else:
				block = block.defaultDestination
	except instructions.EmptyInputException:
		pass
	if state.expected != state.output:
		raise WrongOutputException("Got %s, want %s" % (state.output, state.expected))
	return blockUses

if __name__ == '__main__':
	import loader
	start, metadata = blocks.blocker(loader.loadProgram())
	blockUses = run(start, State.fromLevel(loader.pickLevel()))
	perf = list(sorted([ (block, uses, uses * block.instructionCount())
		for block, uses in blockUses.iteritems()],
		key=lambda x: x[2]))
	pprint.pprint(perf)
	print(sum(x[2] for x in perf))
