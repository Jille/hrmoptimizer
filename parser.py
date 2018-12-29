import collections

import instructions

class ParseException(Exception):
	pass

instr_map = {x.keyword(): x for x in instructions.all}

print instr_map

def parse(s):
	lines = s.splitlines()
	if lines[0] != "-- HUMAN RESOURCE MACHINE PROGRAM --":
		raise ParseException("Not a HRM program?")
	program = []
	labels = {}
	tileLabels = collections.defaultdict(str)
	eatLabel = None
	for line in lines[1:]:
		line = line.strip()
		if not line:
			continue
		if eatLabel is not None:
			tileLabels[eatLabel] += line + "\n"
			if ';' in line:
				eatLabel = None
		elif line.endswith(':'):
			label = line[:-1]
			labels[label] = len(program)
		elif line.startswith('DEFINE LABEL '):
			eatLabel = int(line[len('DEFINE LABEL '):])
		else:
			sp = line.split()
			instr = instr_map[sp[0]]
			arg = None
			if instr.argumentType:
				arg = sp[1]
				if instr.argumentType == instructions.FloorArgument:
					arg = int(arg)
			program.append(instr(arg))
	return [program, labels, tileLabels]

if __name__ == '__main__':
	import loader
	print parse(loader.loadProgram())
