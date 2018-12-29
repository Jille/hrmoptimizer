import collections

import instructions
import parser
import blocks

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
			self.tiles = {i: None for i in range(tiles)}
			self.tiles.update(initializedTiles)
		_reset()
		self.reset = _reset

	def get(self, argument):
		return self.tiles[argument]

	def set(self, argument, value):
		self.tiles[argument] = value

	def assertHandNotEmpty(self):
		if self.hand is None:
			raise ExecutionException("hand is empty")

	def __str__(self):
		return "State[%s, [%s]]" % (self.hand, self.tiles)

def run(block, state):
	state.reset()
	blockUses = collections.defaultdict(int)
	try:
		while True:
			blockUses[block] += 1
			for instr in block.instructions:
				print str(instr)
				instr.do(state)
				print state
			if isinstance(block.endJump, instructions.JumpZ):
				state.assertHandNotEmpty()
				if state.hand == 0:
					block = block.conditionalDestination
				else:
					block = block.defaultDestination
			elif isinstance(block.endJump, instructions.JumpNeg):
				state.assertHandNotEmpty()
				if state.hand < 0:
					block = block.conditionalDestination
				else:
					block = block.defaultDestination
			else:
				block = block.defaultDestination
	except instructions.EmptyInputException:
		pass
	if state.expected == state.output:
		raise WrongOutputException()
	return blockUses

if __name__ == '__main__':
	import testdata
	print run(blocks.blocker(testdata.program), State(testdata.input, testdata.expected, testdata.tiles, testdata.initializedTiles))
