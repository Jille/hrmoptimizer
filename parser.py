import collections

import instructions

class ParseException(Exception):
	pass

instr_map = {x.keyword(): x for x in instructions.all}

print instr_map

Metadata = collections.namedtuple('Metadata', ['tileLabels', 'comments'])

def parse(s):
	lines = s.splitlines()
	if lines[0] != "-- HUMAN RESOURCE MACHINE PROGRAM --":
		raise ParseException("Not a HRM program?")
	program = []
	labels = {}
	tileLabels = collections.defaultdict(str)
	comments = collections.defaultdict(str)
	eatLabel = None
	eatComment = None
	for line in lines:
		if '--' in line:
			line = line.split('--', 1)[0]
		line = line.strip()
		if not line:
			continue
		if eatLabel is not None:
			tileLabels[eatLabel] += line + "\n"
			if ';' in line:
				eatLabel = None
		elif eatComment is not None:
			comments[eatComment] += line + "\n"
			if ';' in line:
				eatComment = None
		elif line.endswith(':'):
			label = line[:-1]
			labels[label] = len(program)
		elif line.startswith('DEFINE LABEL '):
			eatLabel = int(line[len('DEFINE LABEL '):])
		elif line.startswith('DEFINE COMMENT '):
			eatComment = int(line[len('DEFINE COMMENT '):])
		else:
			sp = line.split()
			instr = instr_map[sp[0]]
			arg = None
			if instr.argumentType:
				arg = sp[1]
				if instr.argumentType == instructions.FloorArgument:
					if not (arg.startswith('[') and arg.endswith(']')):
						arg = int(arg)
			program.append(instr(arg))
	return [program, labels, Metadata(tileLabels=tileLabels, comments=comments)]

if __name__ == '__main__':
	import loader
	print parse(loader.loadProgram())
