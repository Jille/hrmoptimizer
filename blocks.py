import instructions
import parser

nextBlockId = 0

class Block(object):
	def __init__(self):
		global nextBlockId
		self.blockId = nextBlockId
		nextBlockId += 1
		self.instructions = []
		self.endJump = None
		self.conditionalDestination = None
		self.defaultDestination = None

def blocker(s):
	program, labels, tileLabels = parser.parse(s)
	start = Block()
	current = start
	labelToBlocks = {idx: Block() for idx in set(labels.values())}
	print labelToBlocks
	for p, instr in enumerate(program):
		print "At %d: %s" % (p, instr)
		if p in labelToBlocks and labelToBlocks[p] != current:
			assert current.defaultDestination is None
			current.defaultDestination = labelToBlocks[p]
			current = current.defaultDestination
		if isinstance(instr, instructions.BaseJumpInstruction):
			current.endJump = type(instr)
			targetBlock = labelToBlocks[labels[instr.argument]]
			if isinstance(instr, instructions.JumpZ) or isinstance(instr, instructions.JumpN):
				current.conditionalDestination = targetBlock
				if p+1 in labelToBlocks:
					current.defaultDestination = labelToBlocks[p+1]
				else:
					current.defaultDestination = Block()
				current = current.defaultDestination
			else:
				current.defaultDestination = targetBlock
				current = Block()  # empty block that'll be garbage collected
		else:
			current.instructions.append(instr)
	return start, tileLabels

def printBlock(b):
	print "==> Block %d" % b.blockId
	for instr in b.instructions:
		print "---> %s" % instr
	if b.conditionalDestination:
		print "---> %s %s" % (b.endJump.keyword(), b.conditionalDestination.blockId)
	print "---> JUMP %s" % b.defaultDestination.blockId

if __name__ == '__main__':
	import loader
	start, tileLabels = blocker(loader.loadProgram())
	todo = [start]
	seen = set()
	while todo:
		b = todo.pop()
		if b in seen:
			continue
		seen.add(b)
		todo.append(b.defaultDestination)
		if b.conditionalDestination is not None:
			todo.append(b.conditionalDestination)
		printBlock(b)
