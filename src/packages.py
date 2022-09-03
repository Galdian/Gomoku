from dataclasses import dataclass, field
import random

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
		potential_moves = []
		for point in points_list[0]:
			if (point[0] <= prev_move[0]+4 and point[0] >= prev_move[0]-4) and (point[1] <= prev_move[1]+4 and point[1] >= prev_move[1]-4):
				potential_moves.append(point)
		a = random.randint(0, len(potential_moves))
		x = potential_moves[a][0]
		y = potential_moves[a][1]



	return [x, y]