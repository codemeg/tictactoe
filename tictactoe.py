import pygame
import time
from random import randint, choice, shuffle

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)

pygame.init()
  
width = 346
height = 400
size = (width, height)
screen = pygame.display.set_mode(size)

margin = 20
line_width = 3
 
pygame.display.set_caption("Tic Tac Toe")
done = False
clock = pygame.time.Clock()

class Game():
	def __init__(self):
		self.keep_playing = True
		self.game_over = False
		self.stalemate = False
		self.win = False
	def game_end(self):
		if self.stalemate or self.win:
			self.game_over = True
	def stalemate(self):
		self.stalemate = True
	def win(self):
		self.win = True
	def ask_keep_playing(self):
		play_again = raw_input("Want to play again? (Y/N): ")
		play_again = play_again[0].lower()
		if play_again == "n":
			print "Thanks for playing! \n"
			self.keep_playing = False
		elif play_again == "y":
			print "Get ready!"
			positions = [0]*9
		else:
			print "YES OR NO."

def draw_x(screen, x, y):
	pygame.draw.line(screen, BLACK, [35+y*100,25+x*100], [105+y*100,115+x*100], line_width)
	pygame.draw.line(screen, BLACK, [105+y*100,25+x*100], [35+y*100,115+x*100], line_width)

def draw_o(screen, x, y):
	pygame.draw.ellipse(screen,BLACK,[35+y*100,25+x*100,70,90],line_width)

def draw_board(screen):
	pygame.draw.line(screen, BLACK, [margin+100, margin], [margin+100, margin+300+line_width], line_width)
	pygame.draw.line(screen, BLACK, [margin+200+line_width, margin], [margin+200+line_width, margin+300+line_width], line_width)
	pygame.draw.line(screen, BLACK, [margin, margin+100], [margin+300+line_width, margin+100], line_width)
	pygame.draw.line(screen, BLACK, [margin, margin+200+line_width], [margin+300+line_width, margin+200+line_width], line_width)

def draw_positions(positions):
	for i in range(9):
		x, y = i_to_xy(i)
		if positions[i] == 1:
			draw_x(screen,x,y)
		if positions[i] == 2:
			draw_o(screen,x,y)

def draw_text(text):
	font = pygame.font.Font(None, 32)
	text_to_draw = font.render(text,True,BLACK)
	screen.blit(text_to_draw, [20,340])

def draw_everything(screen,positions,text):
	screen.fill(WHITE)
	draw_board(screen)
	draw_positions(positions)
	draw_text(text)
	pygame.display.flip()
	clock.tick(60)

def xy_to_i(x, y):
	"""Converts x, y coordinates to index from 0-8"""
	return x * 3 + y

def i_to_xy(i):
	"""Converts index to x, y coordinates"""
	row = i / 3
	col = i % 3
	return (row, col)

def win(positions):
	"""Returns whether the game is won, which player won"""
	#Check rows
	for x in range(3):
		if positions[xy_to_i(x, 0)] == positions[xy_to_i(x, 1)] == positions[xy_to_i(x, 2)]:
			if positions[xy_to_i(x, 0)] == 1:
				return {"won":True, "winner":1}
			if positions[xy_to_i(x, 0)] == 2:
				return {"won":True, "winner":2}

	#Check columns
	for y in range(3):
		if positions[xy_to_i(0, y)] == positions[xy_to_i(1, y)] == positions[xy_to_i(2, y)]:
			if positions[xy_to_i(0, y)] == 1:
				return {"won":True, "winner":1}
			if positions[xy_to_i(0, y)] == 2:
				return {"won":True, "winner":2}

	#Check diagonals
	if positions[0] == positions[4] == positions[8]:
		if positions[4] == 1:
			return {"won":True, "winner":1}
		if positions[4] == 2:
			return {"won":True, "winner":2}
	if positions[2] == positions[4] == positions[6]:
		if positions[4] == 1:
			return {"won":True, "winner":1}
		if positions[4] == 2:
			return {"won":True, "winner":2}

	#If none of the above		
	return {"won":False, "winner":0}

def about_to_win(positions):
	"""Returns player about to win, position"""
	ones = 0
	twos = 0
	which_player = 0

	#Horizontal rows
	for x in range(3):
		for y in range(3):
			if positions[xy_to_i(x, y)] == 1:
				ones += 1
			if positions[xy_to_i(x, y)] == 2:
				twos += 1
			if ones == 2:
				which_player = 1
			if twos == 2:
				which_player = 2
		if which_player != 0:
			for j in range(3):
				if positions[xy_to_i(x, j)] == 0:
					print "%s is about to win horizontally so I'm going to go at position %d" % (str(which_player), xy_to_i(x,j)+1)
					return which_player, xy_to_i(x, j)
		ones = 0
		twos = 0
		which_player = 0

	#Vertical rows
	for y in range(3):
		for x in range(3):
			if positions[xy_to_i(x, y)] == 1:
				ones += 1
			if positions[xy_to_i(x, y)] == 2:
				twos += 1
			if ones == 2:
				which_player = 1
			if twos == 2:
				which_player = 2
		if which_player != 0:
			for j in range(3):
				if positions[xy_to_i(j, y)] == 0:
					print "%s is about to win vertically so I'm going to go at position %d" % (str(which_player), xy_to_i(j,y)+1)
					return which_player, xy_to_i(j, y)
		ones = 0
		twos = 0
		which_player = 0

	#Diagonal right
	for y in range(3):
		if positions[xy_to_i(y, y)] == 1:
			ones += 1
		if positions[xy_to_i(y, y)] == 2:
			twos += 1
		if ones == 2:
			which_player = 1
		if twos == 2:
			which_player = 2
	if which_player != 0:
		for j in range(3):
			if positions[xy_to_i(j, j)] == 0:
				print "%s is about to win diagonal right so I'm going to go at position %d" % (str(which_player), xy_to_i(j,j)+1)
				return which_player, xy_to_i(j, j)
	ones = 0
	twos = 0
	which_player = 0

	#Diagonal left
	for y in range(3):
		if positions[xy_to_i(2-y, y)] == 1:
			ones += 1
		if positions[xy_to_i(2-y, y)] == 2:
			twos += 1
		if ones == 2:
			which_player = 1
		if twos == 2:
			which_player = 2
	if which_player != 0:
		for j in range(3):
			if positions[xy_to_i(2-j, j)] == 0:
				print "%s is about to win diagonal left so I'm going to go at position %d" % (str(which_player), xy_to_i(2-j,j)+1)
				return which_player, xy_to_i(2-j, j)
	ones = 0
	twos = 0
	which_player = 0

	return 0, None

def stalemate(positions):
	count = 0
	for i in range(9):
		if positions[i] == 1 or positions[i] == 2:
			count += 1
	if count == 9 and not win(positions)["won"]:
		return True
	return False

def show_stats(player_one_name,player_one_wins,player_two_name,player_two_wins,stalemates):
	time.sleep(3)
	screen.fill(WHITE)
	starting_height = 100

	font = pygame.font.Font(None, 30)
	text_to_draw = font.render(player_one_name+" wins: "+str(player_one_wins),True,BLACK)
	screen.blit(text_to_draw, [20,starting_height])
	font = pygame.font.Font(None, 30)
	text_to_draw = font.render(player_two_name+" wins: "+str(player_two_wins),True,BLACK)
	screen.blit(text_to_draw, [20,starting_height+50])
	font = pygame.font.Font(None, 30)
	text_to_draw = font.render("Stalemates: "+str(stalemates),True,BLACK)
	screen.blit(text_to_draw, [20,starting_height+100])

	pygame.display.flip()
	clock.tick(60)
	time.sleep(2)

	text_to_draw = font.render(player_one_name+" wins: "+str(player_one_wins),True,BLACK)
	screen.blit(text_to_draw, [20,starting_height])
	text_to_draw = font.render(player_two_name+" wins: "+str(player_two_wins),True,BLACK)
	screen.blit(text_to_draw, [20,starting_height+50])
	text_to_draw = font.render("Stalemates: "+str(stalemates),True,BLACK)
	screen.blit(text_to_draw, [20,starting_height+100])
	font = pygame.font.Font(None, 30)
	text_to_draw = font.render("Want to play again? (Y or N)",True,GREEN)
	screen.blit(text_to_draw, [20,starting_height+200])

	pygame.display.flip()
	clock.tick(60)
	time.sleep(5)

def game_not_over(positions):
	is_game_won = win(positions)["won"]
	if not stalemate(positions) and not is_game_won:
		return True
	else:
		return False

def your_turn(positions,which_player):
	while True:
		pos = int(raw_input("Where do you want to go? (1-9): "))
		if positions[pos-1] == 0:
			positions[pos-1] = which_player
			return positions
		else:
			print "That space is taken already!"
			continue

def computer_turn(positions):
	print " "
	while True:
		time.sleep(1)
		# 1. If you can win then do it.
		player_about_to_win, place_about_to_win = about_to_win(positions)

		if player_about_to_win == 2 and positions[place_about_to_win] == 0:
			positions[place_about_to_win] = 2
			return positions

		# 2. If opponent is about to win then block them.
		if player_about_to_win == 1 and positions[place_about_to_win] == 0:
			positions[place_about_to_win] = 2
			return positions

		# 3. If center square is free then take it.
		if positions[4] == 0:
			positions[4] = 2
			return positions

		# 4. If corners are free then take them.
		corners = [0,2,6,8]
		shuffle(corners)
		for i in range(len(corners)):
			pos = corners[i]
			if positions[pos] == 0:
				positions[pos] = 2
				return positions
		pos = choice([1,3,5,7])
		if positions[pos] == 0:
			positions[pos] = 2
			return positions
		else:
			continue

def taking_turns(whose_turn,positions):
	if whose_turn %2 == 1:
		print "%s's turn" % (player_one_name)
		your_turn(positions,1)
	if whose_turn %2 == 0:
		print "%s's turn" % (player_two_name)
		if one_or_two == 1:
			computer_turn(positions)
		if one_or_two == 2:
			your_turn(positions,2)

g = Game()
positions = [0]*9
replay = 1
player_one_wins = 0
player_two_wins = 0
stalemates = 0

print "\nWelcome to TicTacToe! One player or two player?"

while True:
	one_or_two = raw_input("Please enter 1 or 2: ")
	if one_or_two == "1" or one_or_two == "2":
		one_or_two = int(one_or_two)
		break
	else:
		print "1 or 2. It's not that hard."

if one_or_two == 2:
	player_one_name = raw_input("What is Player 1's name? ")
	player_two_name = raw_input("What is Player 2's name? ")
else:
	player_one_name = raw_input("What is Player 1's name? ")
	player_two_name = "Computer"

whose_turn = 1
coin = randint(0,1)
if coin == 0:
	coin = "h"
else:
	coin = "t"
while True:
	guess = raw_input("Heads or Tails?: ")
	guess = guess[0].lower()
	if guess == "h" or guess == "t":
		break
	else:
		print "You didn't pick heads or tails!"
if guess == coin:
	print "%s gets to go first! \n" % (player_one_name)
else:
	whose_turn = 2
	print "Sorry! %s gets to go first! \n" % (player_two_name)

while not done:
	
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
	    if event.type == pygame.KEYDOWN:
	    	key = pygame.key.name(event.key)

	while g.keep_playing:
		while game_not_over(positions):
			draw_everything(screen,positions,"")

			#Main game play		
			taking_turns(whose_turn,positions)
			draw_everything(screen,positions,"")
			whose_turn += 1

		if stalemate(positions):
			stalemates += 1
			print "Stalemate! \n"

		if win(positions)["won"]:
			if win(positions)["winner"] == 1:
				player_one_wins += 1
				print "*****%s wins!***** \n" % (player_one_name)
			if win(positions)["winner"] == 2:
				player_two_wins += 1
				print "*****%s won.***** \n" % (player_two_name)
			
		show_stats(player_one_name,player_one_wins,player_two_name,player_two_wins,stalemates)

		#Checking if they want to play again
		g.ask_keep_playing()
		positions = [0]*9		

pygame.quit()