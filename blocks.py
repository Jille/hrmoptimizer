import instructions
import parser

nextBlockId = 0

class Block(object):
	def __init__(self, line, label=None):
		global nextBlockId
		self.blockId = nextBlockId
		nextBlockId += 1
		self.instructions = []
		self.line = line
		self.label = label
		self.endJump = None
		self.conditionalDestination = None
		self.defaultDestination = None

	def __repr__(self):
		if self.label:
		        return 'Block %s @%s' % (self.label, self.line)
		return 'Block @%s' % self.line

	def instructionCount(self):
		if self.endJump:
		    return len(self.instructions) + 1
		return len(self.instructions)
	

def blocker(s):
	program, labels, metadata = parser.parse(s)
	start = Block(0)
	current = start
	lineToLabel = {line: label for label, line in labels.iteritems()}
	labelToBlocks = {}
	for label, line in labels.iteritems():
	    labelToBlocks[line] = Block(line, label)
	print labelToBlocks
	lastLabelLine = 0
	for p, instr in enumerate(program):
		print "At %d: %s" % (p, instr)
		if p in labelToBlocks and labelToBlocks[p] != current:
			lastLabelLine = p
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
					current.defaultDestination = Block(
						p+1,
						'%s+%s' % (lineToLabel[lastLabelLine],
							   p - lastLabelLine))
				current = current.defaultDestination
			else:
				current.defaultDestination = targetBlock
				current = Block(p)  # empty block that'll be garbage collected
		else:
			current.instructions.append(instr)
	return start, metadata

def allBlocks(start):
	ret = set()
	todo = [start]
	while todo:
		b = todo.pop()
		if b in ret:
			continue
		ret.add(b)
		todo.append(b.defaultDestination)
		if b.conditionalDestination is not None:
			todo.append(b.conditionalDestination)
	return ret

def printBlock(b):
	print "==> Block %d" % b.blockId
	for instr in b.instructions:
		print "---> %s" % instr
	if b.conditionalDestination:
		print "---> %s %s" % (b.endJump.keyword(), b.conditionalDestination.blockId)
	print "---> JUMP %s" % b.defaultDestination.blockId

if __name__ == '__main__':
	import loader
	start, metadata = blocker(loader.loadProgram())
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
