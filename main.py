from src.packages import Point, check_connected_stones, AI_move, find_point_by_coor, find_stone_coor
from tkinter import messagebox
import pygame
from pygame.locals import *

pygame.init()

# CONSTANTS

NUM_OF_LINES = 15
WINCON = 5

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
BOARD_SQUARE_LENGTH = 600

BOARD_COLOR = (205, 170, 125)
LINE_COLOR = (0, 0, 0)
LINE_WIDTH = 5

STONE_RADIUS = ((BOARD_SQUARE_LENGTH / NUM_OF_LINES) * 0.49)
P1_STONE_COLOR = (0, 0, 0)
P2_STONE_COLOR = (255, 255, 255)

FPSCLOCK = pygame.time.Clock()



# DRAW BOARD

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill(BOARD_COLOR)

# CREATE POINTS
square_border = (BOARD_SQUARE_LENGTH / (NUM_OF_LINES) * 0.9)
vertical = 32
point_xcoor = 1
points_list_for_drawing = []
ai_points_list = [[], [], []]
for a in range(0, NUM_OF_LINES):
	horizontal = 32
	point_ycoor = 1
	for b in range(0, NUM_OF_LINES):
		point_in_space = pygame.draw.rect(background, BOARD_COLOR, (vertical, horizontal, square_border, square_border))
		horizontal += BOARD_SQUARE_LENGTH / (NUM_OF_LINES - 1)
		points_list_for_drawing.append([point_in_space, Point(point_xcoor, point_ycoor, 0, (
			point_in_space.left + square_border / 2, point_in_space.top + square_border / 2))])
		ai_points_list[0].append([point_xcoor, point_ycoor])
		point_ycoor += 1

	vertical += BOARD_SQUARE_LENGTH / (NUM_OF_LINES - 1)
	point_xcoor += 1

# LINES

vertical_lines_start_point = (SCREEN_WIDTH - BOARD_SQUARE_LENGTH) / 2
horizontal_lines_start_point = (SCREEN_HEIGHT - BOARD_SQUARE_LENGTH) / 2
line_coor = 0
for a in range(0, NUM_OF_LINES):
	pygame.draw.line(background, LINE_COLOR, (vertical_lines_start_point, horizontal_lines_start_point + line_coor),
					 ((vertical_lines_start_point + BOARD_SQUARE_LENGTH), horizontal_lines_start_point + line_coor),
					 LINE_WIDTH)
	pygame.draw.line(background, LINE_COLOR, (vertical_lines_start_point + line_coor, horizontal_lines_start_point),
					 (vertical_lines_start_point + line_coor, (horizontal_lines_start_point + BOARD_SQUARE_LENGTH)),
					 LINE_WIDTH)
	line_coor += BOARD_SQUARE_LENGTH / (NUM_OF_LINES - 1)

screen.blit(background, (0, 0))


def ai_set_points_lists(player, xcor, ycor):
	ai_points_list[0].remove([xcor, ycor])
	ai_points_list[player].append([xcor, ycor])

# DRAW STONE


def draw_stone(player, xcor, ycor):
	if player == 1:
		scolor = P1_STONE_COLOR
	if player == 2:
		scolor = P2_STONE_COLOR
	pygame.draw.circle(background, scolor, (xcor, ycor), STONE_RADIUS)
	screen.blit(background, (0, 0))


# NEXT TURN

current_player = 1


def next_turn():
	global current_player
	if current_player == 1:
		current_player = 2
	else:
		current_player = 1


# CPU MOVE
prev_move = []
def cpu_move(ai_list, draw_list, player):
	global prev_move
	movecords = AI_move(ai_list, player, prev_move)
	drawcords = find_stone_coor(draw_list, movecords[0], movecords[1])
	draw_stone(player, drawcords[0], drawcords[1])
	prev_move = [movecords[0], movecords[1]]
	ai_set_points_lists(player, movecords[0], movecords[1])
	if check_connected_stones(ai_points_list, player, movecords[0], movecords[1]) == 4:
		pygame.display.update()
		finish()
	next_turn()


# MAIN LOOP

answer = messagebox.askyesno("Let's start the game!", "Would you like to go first?")
if answer:
	cpu_player = 2
else:
	cpu_player = 1

def finish():
	messagebox.showinfo(title="Game finished!", message=f"Player {current_player} has won!")
	pygame.quit()


pygame.display.flip()

mouse_pos = (0, 0)
running = True
while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if not running:
			pygame.quit()
		elif current_player == cpu_player:
			cpu_move(ai_points_list, points_list_for_drawing, current_player)
		# elif current_player != cpu_player:
		# 	cpu_move(ai_points_list, points_list_for_drawing, current_player)
		elif event.type == MOUSEBUTTONUP:
			mouse_pos = pygame.mouse.get_pos()
			for point in points_list_for_drawing:
				point_in_space = point[0]
				if point_in_space.collidepoint(mouse_pos) and pygame.MOUSEBUTTONUP and point[1].player == 0:
					draw_stone(current_player, point[1].coords_for_stone[0], point[1].coords_for_stone[1])
					point[1].player = current_player
					ai_set_points_lists(current_player, point[1].xcor, point[1].ycor)
					prev_move = [point[1].xcor, point[1].ycor]
					if check_connected_stones(ai_points_list, current_player, point[1].xcor, point[1].ycor) == 4:
						pygame.display.update()
						finish()
					next_turn()

		pygame.display.update()

		FPSCLOCK.tick(30)
