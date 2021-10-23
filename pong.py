import pygame
from pygame.locals import *
from random import random
from random import randint

pygame.init()

SS = (1200, 720)
GAME = True

screen = pygame.display.set_mode(SS)

game_clock = pygame.time.Clock()

score_font = pygame.font.SysFont("Liberation mono", 50, True)
P_SCORE = 0
E_SCORE = 0

#player stuff
class player():
	def __init__(s, initial_xy, initial_wh):
		s.player_xy = initial_xy
		s.player_xy_v = [10, 10]
		s.player_wh = initial_wh
		
	def update(s):
		key = pygame.key.get_pressed()
		if key[pygame.K_UP] and s.player_xy[1] > 0:
			s.player_xy[1] -= s.player_xy_v[1]
		if key[pygame.K_DOWN] and s.player_xy[1] < SS[1] - s.player_wh[1]:
			s.player_xy[1] += s.player_xy_v[1]
		
	def draw(s):
		global screen
		pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(s.player_xy, s.player_wh))
		
	def get_xy(s):
		return s.player_xy
	def get_wh(s):
		return s.player_wh

#enemy
class enemy():
	def __init__(s, xy, wh):
		s.xy = xy
		s.xy_v = [3.5, 3.5]
		s.wh = wh
		
	def update(s, ball_xy):
		global SS
		if s.xy[1] + s.wh[1]/2 == ball_xy[1]:
			s.xy[1] = s.xy[1]
		elif s.xy[1] + s.wh[1]/2 > ball_xy[1]:
			s.xy[1] -= s.xy_v[1]
		elif s.xy[1] + s.wh[1]/2 < ball_xy[1]:
			s.xy[1] += s.xy_v[1]
		
	def draw(s):
		global screen
		pygame.draw.rect(screen, (255,255,255), pygame.Rect(s.xy, s.wh))
	
	def get_xy(s):
		return s.xy
		
	def get_wh(s):
		return s.wh

#ball
class ball():
	def __init__(s, initial_xy):
		s.ball_xy = initial_xy
		s.ball_r = 50
		s.ball_x_v_inc = 0.0
		s.ball_xy_vel = [8*random() + 2, random()]
		s.dir = 0
		s.colliding = 0
		s.state = 0
		s.time_scored = 0
		
		s.color = [255, 255, 0]
		
		if randint(0, 1) == 0: s.dir = 1
		if randint(0, 1) == 0: s.ball_xy_vel[1] *= -1
		
	def update(s, player_xy, player_wh, enemy_xy, enemy_wh):
		global SS, P_SCORE, E_SCORE
		
		time_now = pygame.time.get_ticks()
		
		if s.state == 0:
		#punktowanie 	
			if s.ball_xy[0] > SS[0] + 300:
				s.state = 1
				P_SCORE += 1
				s.time_scored = pygame.time.get_ticks()
			elif s.ball_xy[0] < -300:
				s.state = 1
				E_SCORE += 1
				s.time_scored = pygame.time.get_ticks()
				
			#kolizja z sufitem/podlogom
			if s.ball_xy[1] <= s.ball_r or s.ball_xy[1] >= SS[1] - s.ball_r:
				s.ball_xy_vel[1] *= -1
			
			if s.colliding == 1:
				s.ball_xy_vel[0] += 1
				if s.ball_r > 1:
					s.ball_r -= 0.5
				s.color = [randint(128, 255),randint(128, 255), 0]
				s.colliding = 0
				
			#kolizja z paletka gracza
			# delta = abs(pozycja paletki) - (abs(obecna pozycja) + abs(premdkosc)
			# jak delta <= 0 to odbicie
			delta_p = (abs(s.ball_xy[0]) + abs(s.ball_xy_vel[0])) - abs(player_xy[0])
			
			if (delta_p <= s.ball_r + player_wh[0] and
				s.dir == 1 and
				s.ball_xy[1] <= player_xy[1] + player_wh[1] and
				s.ball_xy[1] > player_xy[1]):
				
				s.ball_xy[0] = player_xy[0] + s.ball_r + player_wh[0] + 5
				
				s.colliding = 1
				
				#odbicie po x
				s.dir = 0
				
				#kalkulacja odbicia po 
				s.ball_xy_vel[1] = (s.ball_xy[1] - (player_xy[1] + player_wh[1]/1.5))/10
				
			delta_e =  abs(enemy_xy[0]) - (abs(s.ball_xy[0]) + abs(s.ball_xy_vel[0]))
			
			#kolizja z paletka przeciwnika
			if (delta_e <= s.ball_r and
				s.dir == 0 and 
				s.ball_xy[1] <= enemy_xy[1] + enemy_wh[1] and
				s.ball_xy[1] > enemy_xy[1]):
				
				s.ball_xy[0] = enemy_xy[0] - s.ball_r - 5
				
				s.colliding = 1
				
				#odbicie po x
				s.dir = 1
				
				#kalkulacja odbicia po 
				s.ball_xy_vel[1] = (s.ball_xy[1] - (enemy_xy[1] + enemy_wh[1]/1.5))/10
			
			if s.dir == 0:
				s.ball_xy[0] += s.ball_xy_vel[0]
			elif s.dir == 1:
				s.ball_xy[0] -= s.ball_xy_vel[0]
			
			s.ball_xy[1] += s.ball_xy_vel[1]
			
		elif s.state == 1:
			if time_now - s.time_scored > 3000:
				s.__init__([600,360])
				s.state = 0
			
	def draw(s):
		global screen
		pygame.draw.circle(screen, s.color, s.ball_xy, s.ball_r)
		
	def get_xy(s):
		return s.ball_xy
		
ball = ball([600, 360])
player = player([50, 360], [20, 100])
enemy = enemy([1150 - 20, 360], [20, 100])

Line = [pygame.Rect((600-5, 0), (10, 100)),
		pygame.Rect((600-5, 100), (10, 100)),
		pygame.Rect((600-5, 200), (10, 100)),
		pygame.Rect((600-5, 300), (10, 100)),
		pygame.Rect((600-5, 400), (10, 100)),
		pygame.Rect((600-5, 500), (10, 100)),
		pygame.Rect((600-5, 600), (10, 100)),]
		
Line_colors = [[0,0,0],
			   [128,128,128],
			   [0,0,0],
			   [128,128,128],
			   [0,0,0],
			   [128,128,128],
			   [0,0,0]]

while GAME:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME = False
	
	game_clock.tick(58)
	
	ball.update(player.get_xy(), player.get_wh(), enemy.get_xy(), enemy.get_wh())
	player.update()
	enemy.update(ball.get_xy())
	
	pygame.draw.rect(screen, (0,0,0), pygame.Rect((0, 0), SS))
	for x in range(0, len(Line)):
		pygame.draw.rect(screen, Line_colors[x], Line[x])
		
	TEXT_P_SCORE = score_font.render(str(P_SCORE), False, 0xffffffff)
	TEXT_E_SCORE = score_font.render(str(E_SCORE), False, 0xffffffff)
	screen.blit(TEXT_P_SCORE, (10, 0))
	screen.blit(TEXT_E_SCORE, (SS[0] - 50, 0))
	ball.draw()
	player.draw()	
	enemy.draw()
	
	pygame.display.update()
	
pygame.quit()
