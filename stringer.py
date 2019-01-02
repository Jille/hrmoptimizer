import collections

import instructions
import parser
import blocks
import runner

def restring(block, metadata, state):
	blockUses = runner.run(block, state)
	buckets = collections.defaultdict(list)
	for b, uses in blockUses.items():
		buckets[uses].append(b)
	todo = []
	for _, equalBlocks in sorted(buckets.items(), key=lambda x: x[0]):
		entries = {b: 0 for b in equalBlocks}
		for b, num in blockUses.items():
			if b.defaultDestination in entries:
				entries[b.defaultDestination] += num
		todo.extend([x[0] for x in sorted(entries.items(), key=lambda x: x[1])])
	before = {}
	after = {}
	allBlocks = set(blockUses.keys())
	while todo:
		b = todo.pop()
		# chainHead is to avoid creating cycles.
		chainHead = b
		while chainHead in before:
			chainHead = before[chainHead]
		if b.defaultDestination not in before and chainHead != b.defaultDestination:
			before[b.defaultDestination] = b
			after[b] = b.defaultDestination
		allBlocks.add(b.defaultDestination)
		if b.conditionalDestination is not None:
			allBlocks.add(b.conditionalDestination)

	order = []
	todo = {block}
	while todo:
		b = todo.pop()  # get random element
		while b in before:
			b = before[b]
		chain = [b]
		while b in after:
			b = after[b]
			chain.append(b)
		order.extend(chain)
		print "After appending %s, order is now %s" % ([tb.blockId for tb in chain], [tb.blockId for tb in order])
		todo = allBlocks - set(order)

	explicitJumps = set()
	labledBlocks = set()
	for i, b in enumerate(order):
		print "At position %d" % i
		blocks.printBlock(b)
		if len(order) <= i+1 or order[i+1] != b.defaultDestination:
			explicitJumps.add(b)
			labledBlocks.add(b.defaultDestination)
		if b.conditionalDestination is not None:
			labledBlocks.add(b.conditionalDestination)

	nextLabel = 97
	blockLabels = {}
	for b in order:
		if b in labledBlocks:
			blockLabels[b] = chr(nextLabel)
			nextLabel += 1

	program = ["-- HUMAN RESOURCE MACHINE PROGRAM --", ""]
	for b in order:
		if b in labledBlocks:
			program.append(blockLabels[b] +":")
		for instr in b.instructions:
			program.append("\t" + str(instr))
		if b.conditionalDestination is not None:
			program.append("\t%s %s" % (b.endJump.keyword(), blockLabels[b.conditionalDestination]))
		if b in explicitJumps:
			program.append("\tJUMP " + blockLabels[b.defaultDestination])
	for i, comment in metadata.comments.items():
		program.append('DEFINE LABEL %d' % i)
		program.append(comment)
	for tl, label in metadata.tileLabels.items():
		program.append('DEFINE LABEL %d' % tl)
		program.append(label)
	return '\n'.join(program)

if __name__ == '__main__':
	import loader
	start, metadata = blocks.blocker(loader.loadProgram())
	print restring(start, metadata, runner.State.fromLevel(loader.pickLevel()))
