import json

class Level(object):
	def __init__(self, input):
		self.number = input['number']
		self.name = input['name']
		self.commands = input['commands']
		self.initializedTiles = {}
		if 'floor' not in input:
			self.tiles = 0
		else:
			self.tiles = input['floor']['columns'] * input['floor']['rows']
			if 'tiles' in input['floor']:
				if isinstance(input['floor']['tiles'], list):
					for k, v in enumerate(input['floor']['tiles']):
						self.initializedTiles[int(k)] = v
				else:
					for k, v in input['floor']['tiles'].items():
						self.initializedTiles[int(k)] = v
		self.examples = []
		for ex in input['examples']:
			self.examples.append((ex['inbox'], ex['outbox']))

levels = {}

with open('hrm-level-data/index.json') as fh:
	data = json.load(fh)
	for l in data:
		if 'cutscene' in l and l['cutscene']:
			continue
		levels[l['number']] = Level(l)
