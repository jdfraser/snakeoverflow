import bottle
import json
import copy
from pathfinding import ShortestPath

name = 'Snakefront-test'

@bottle.get('/')
def index():
	return """
		<a href="https://github.com/sendwithus/battlesnake-python">
			gonna leave this default for now, don't want people spying :D
		</a>
	"""
@bottle.post('/start')
def start():
	data = bottle.request.json

	return json.dumps({
		'name': name,
		'color': '#1E90FF',
		'head_url': 'https://github.com/Nebual/snakefront/blob/master/snake.png?raw=true',
		'taunt': 'Online bookings for less!'
	})

def simulate(state):
	#modify state
	pass

def gen_heatmap(movedata):
	global ourSnakeName
	state = copy.deepcopy(movedata)
	heatmap = []
	width = len(state['board'])
	height = len(state['board'][0])
	for x in range(width):
		heatmap.append([1]*height)
	
	snakeOptions = {}
	for snake in state['snakes']:
		if snake['name'] != ourSnakeName:
			headpos = snake['coords'][0]
			neckpos = snake['coords'][1]
			for x,y in [[0,1],[0,-1],[1,0],[-1,0]]:
				movepos = [x + headpos[0], y + headpos[1]]
				if movepos[0] == neckpos[0] and movepos[1] == neckpos[1]: continue # Assume snake won't go backwards
				snakeOptions.setdefault(snake['name'], []).append(movepos)
		# todo: what if they ate food?
		snake['coords'].pop()
		for x,y in snake['coords']:
			heatmap[x][y] += 100
		for x,y in snakeOptions.get(snake['name'], []):
			heatmap[x][y] += 33 #repeating of course
	return heatmap


@bottle.post('/move')
def move():
	data = bottle.request.json # {'game_id': 'hairy-cheese', 'turn': 1, 'board': <boarddata>, 'snakes': <snakedatas>, 'food': [[1,2],[4,1]]} 
	# <boarddata>: 2d array [x][y] = {'state': 'empty' or 'food' or 'head' or 'body', 'snake': None or 'badsnake'}
	# <snakedata>: [{'url':'http://...', 'color': '#ffffff', 'headurl': 'http://....png', 'name': 'badsnake', 'taunt': 'Hey'}]
	# Do things here!!

	text = "heatmap:\n"
	heatmap = gen_heatmap(data)
	for y in range(len(heatmap[0])):
		for xs in heatmap:
			text += str(xs[y]) + ", "
		text += "\n"
	print text, "end heatmap"
	nextmove = ShortestPath(heatmap, headpos, [0,0])
	print "Recommend next move to " + str(next_move)

	for snake in data['snakes']:
		if snake['name'] == name:
			head = snake['coords'][0]

	#move = getpath()
	move = [head[0] +1, head[1]]
	if move[1] > head[1]:
		nextmove = 'down'
	elif move[1] < head[1]:
		nextmove = 'up'
	elif move[0] > head[0]:
		nextmove = 'right'
	elif move[0] < head[0]:
		nextmove = 'left'

	return json.dumps({
		'move': nextmove,
		'taunt': 'Booking in progress'
	})


@bottle.post('/end')
def end():
	data = bottle.request.json # {'game_id': 'hairy_cheese'}
	# Flush game state info    


	return json.dumps({}) # Server ignores our response


# Expose WSGI app
application = bottle.default_app()
