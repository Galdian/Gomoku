from dataclasses import dataclass, field
import random
import copy

@dataclass
class Point:
	xcor: int
	ycor: int
	player: int
	coords_for_stone: tuple


def check_player_in_points_list(points_list, xcor, ycor):
	for point in points_list:
		if point[1].xcor == xcor and point[1].ycor == ycor:
			return point[1].player

def find_stone_coor(points_list, xcor, ycor):
	for point in points_list:
		if point[1].xcor == xcor and point[1].ycor == ycor:
			return point[1].coords_for_stone

def find_point_by_coor(points_list, xcor, ycor):
	index = next((i for i, point in enumerate(points_list) if (point[1].xcor == xcor and point[1].ycor == ycor)), -1)
	return index

def check_connected_stones(points_list, player, xcor, ycor):
	highest_points = 0
	# check horizontal
	factor = 1
	points = 0
	while (xcor + factor) < 16 and [xcor + factor, ycor] in points_list[player]:
		points += 1
		factor += 1
	factor = 1
	while (xcor - factor) > 0 and [xcor - factor, ycor] in points_list[player]:
		points += 1
		factor += 1
	if points > highest_points:
		highest_points = points
	# check vertical
	factor = 1
	points = 0
	while (ycor + factor) < 16 and [xcor, ycor + factor] in points_list[player]:
		points += 1
		factor += 1
	factor = 1
	while (ycor - factor) > 0 and [xcor, ycor - factor] in points_list[player]:
		points += 1
		factor += 1
	if points > highest_points:
		highest_points = points
	# check diagonal left up -> right down
	factor = 1
	points = 0
	while (ycor + factor) < 16 and (xcor + factor) < 16 and [xcor + factor, ycor + factor] in points_list[player]:
		points += 1
		factor += 1
	factor = 1
	while (ycor - factor) > 0 and (xcor - factor > 0) and [xcor - factor, ycor - factor] in points_list[player]:
		points += 1
		factor += 1
	if points > highest_points:
		highest_points = points
# check diagonal left down -> right up
	factor = 1
	points = 0
	while (ycor - factor) > 0 and (xcor + factor) < 16 and [xcor + factor, ycor - factor] in points_list[player]:
		points += 1
		factor += 1
	factor = 1
	while (ycor + factor) < 16 and (xcor - factor > 0) and [xcor - factor, ycor + factor] in points_list[player]:
		points += 1
		factor += 1
	if points > highest_points:
		highest_points = points
	return highest_points

def next_player(player):
	if player == 1:
		return 2
	if player == 2:
		return 1

def move_value(analyzed_points_list, x, y, player):
	connection_value = check_connected_stones(analyzed_points_list, player, x, y) * 1000
	if x > 8:
		xval = 16 - x
	if x < 8:
		xval = x
	if x == 8:
		xval = 8
	if y > 8:
		yval = 16 - y
	if y < 8:
		yval = y
	if y == 8:
		yval = 8
	positional_value = xval + yval
	return connection_value + positional_value

def find_strongest_move_in_given_position(analyzed_points_list, player):
	highest_move_value = 0
	moves_to_consider = []
	for move in analyzed_points_list[0]:
		analyzed_move_value = move_value(analyzed_points_list, move[0], move[1], player)
		if analyzed_move_value > highest_move_value:
			moves_to_consider = []
			moves_to_consider.append([move[0], move[1]])
			highest_move_value = analyzed_move_value
		elif analyzed_move_value == highest_move_value:
			moves_to_consider.append([move[0], move[1]])

	a = random.randint(0, len(moves_to_consider) - 1)
	x = moves_to_consider[a][0]
	y = moves_to_consider[a][1]
	return [highest_move_value, [x, y]]

def update_points(points_list, player, xcor, ycor):
	points_list[0].remove([xcor, ycor])
	points_list[player].append([xcor, ycor])

def AI_move(points_list, player, prev_move):
	x: int
	y: int
	# RANDOM MOVER
	# move_possible = False
	# while not move_possible:
	# 	x = random.randint(1, 15)
	# 	y = random.randint(1, 15)
	# 	a = check_player_in_points_list(points_list, x, y)
	# 	if a == 0:
	# 		move_possible = True

	if len(points_list[1]+points_list[2]) == 0:
		x = 8
		y = 8

	else:
		# potential_moves = []
		# for point in points_list[0]:
		# 	potential_moves.append(point)
			# if (point[0] <= prev_move[0]+4 and point[0] >= prev_move[0]-4) and (point[1] <= prev_move[1]+4 and point[1] >= prev_move[1]-4):
			# 	potential_moves.append(point)
		min = 10000
		mtc = []
		for potential_move in points_list[0]:
			new_list = copy.deepcopy(points_list)
			update_points(new_list, player, potential_move[0], potential_move[1])
			value = find_strongest_move_in_given_position(new_list, next_player(player))[0]
			xytoc = find_strongest_move_in_given_position(new_list, next_player(player))[1]
			if value < min:
				mtc = []
				min = value
				mtc.append(potential_move)
			elif value == min:
				mtc.append(potential_move)
		strongest_val = 0
		potential_strongest = []
		for move in mtc:
			move_to_consider = move_value(points_list, move[0], move[1], player)
			if move_to_consider > strongest_val:
				potential_strongest = []
				potential_strongest.append([move[0], move[1]])
				strongest_val = move_to_consider
			elif move_to_consider == strongest_val:
				potential_strongest.append([move[0], move[1]])
		a = random.randint(0, len(potential_strongest) - 1)
		x = potential_strongest[a][0]
		y = potential_strongest[a][1]



	return [x, y]