from dataclasses import dataclass, field

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
	else:
		return -1

def check_victory_conditions(points_list, player, xcor, ycor):
	victory = False
	# check horizontal
	factor = 1
	points = 0
	while (xcor + factor) < 16 and check_player_in_points_list(points_list, xcor + factor, ycor) == player:
		points += 1
		factor += 1
	factor = 1
	while (xcor - factor) > 0 and check_player_in_points_list(points_list, xcor - factor, ycor) == player:
		points += 1
		factor += 1
	if points >= 4:
		victory = True
	# check vertical
	factor = 1
	points = 0
	while (ycor + factor) < 16 and check_player_in_points_list(points_list, xcor, ycor + factor) == player:
		points += 1
		factor += 1
	factor = 1
	while (ycor - factor) > 0 and check_player_in_points_list(points_list, xcor, ycor - factor) == player:
		points += 1
		factor += 1
	if points >= 4:
		victory = True
	# check diagonal left up -> right down
	factor = 1
	points = 0
	while (ycor + factor) < 16 and (xcor + factor) < 16 and check_player_in_points_list(points_list, xcor + factor, ycor + factor) == player:
		points += 1
		factor += 1
	factor = 1
	while (ycor - factor) > 0 and (xcor - factor > 0) and check_player_in_points_list(points_list, xcor - factor, ycor - factor) == player:
		points += 1
		factor += 1
	if points >= 4:
		victory = True
# check diagonal left down -> right up
	factor = 1
	points = 0
	while (ycor - factor) > 0 and (xcor + factor) < 16 and check_player_in_points_list(points_list, xcor + factor, ycor - factor) == player:
		points += 1
		factor += 1
	factor = 1
	while (ycor + factor) < 16 and (xcor - factor > 0) and check_player_in_points_list(points_list, xcor - factor, ycor + factor) == player:
		points += 1
		factor += 1
	if points >= 4:
		victory = True
	return victory
	