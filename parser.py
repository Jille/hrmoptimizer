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
	for line in lines[1:]:
		line = line.strip()
		if not line:
			continue
		if line.endswith(':'):
			label = line[:-1]
			labels[label] = len(program)
		else:
			sp = line.split()
			instr = instr_map[sp[0]]
			arg = None
			if instr.argumentType:
				arg = sp[1]
				if instr.argumentType == instructions.FloorArgument:
					arg = int(arg)
			program.append(instr(arg))
	return [program, labels]

if __name__ == '__main__':
	import loader
	print parse(loader.loadProgram())
