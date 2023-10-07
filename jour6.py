# Jour 6: Creer le jeu pong
import pygame
from math import cos, sin, radians, degrees
from random import randint, choice

pygame.init()
pygame.mixer.init()

WIDTH = 1000
HEIGHT = 600
score=0 # player score
couches = 15 # number of ball layers
offset=5 # offset before the beginning of the game (anti-lag)

ambiance = pygame.mixer.Sound("ambiance.mp3")
ambiance.set_volume(0.1)
bounce = pygame.mixer.Sound("bump.ogg")
bounce.set_volume(0.3)


class Player():
    def __init__(self, WIDTH, HEIGHT):
        self.width=20
        self.height=150
        self.max_x = WIDTH - self.width
        self.max_y = HEIGHT - self.height
        self.x1 = 0
        self.x2 = self.max_x
        self.y = 0
        self.velocity = 550
        self.color = (255, 255, 255)

    def move_up(self, dt):
        self.y = round(max(0, self.y-self.velocity*dt))

    def move_down(self, dt):
        self.y = round(min(self.y+self.velocity*dt, self.max_y))


class Ball():
	def __init__(self, WIDTH, HEIGHT, player):
		self.r = 20
		self.player = player
		self.max_x = WIDTH
		self.max_y = HEIGHT
		self.x = self.max_x//2
		self.y = self.max_y//2
		self.velocity = 300
		angles=[randint(-160,-105),randint(-75,-15),randint(15,75),randint(105,160)]
		self.angle = choice(angles)
		self.color = (0, 255, 0)

	def move(self, dt):
		self.x += cos(radians(self.angle)) * self.velocity * dt
		self.y += sin(radians(self.angle)) * self.velocity * dt

		if self.y < self.r:
			if not (0 <= self.angle <= 180):
				self.angle *= -1
				bounce.play(1)
		elif self.y > self.max_y - self.r:
			if 0 <= self.angle <= 180:
				self.angle *= -1
				bounce.play(1)

		# Left side colision
		if (self.player.width//2 <= self.x - self.r <= self.player.width):
			if self.player.y <= self.y <= self.player.y + self.player.height:
				if not (-90<= self.angle <= 90):
					if self.angle < 0: self.angle = -180 - self.angle
					else: self.angle = 180 - self.angle 
					bounce.play(1)
														
		# Right side colision
		if self.max_x-self.player.width<=self.x+self.r<=self.max_x-self.player.width//2:
			if self.player.y <= self.y <= self.player.y + self.player.height:
				if -90<= self.angle <= 90:
					if self.angle < 0: self.angle = -180 - self.angle
					else: self.angle = 180 - self.angle
					bounce.play(1)

	# verifying if the ball is out screen
	def is_out(self):
		return self.x + self.r//2 <= 0 or self.max_x  <= self.x +self.r//2


# Game variables
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

player = Player(WIDTH, HEIGHT)
ball = Ball(WIDTH, HEIGHT, player)
balls = []

ambiance.play(-1)

# Game loop
Running=True
while Running:
	dt = clock.tick(60)/1000
	score+=dt

	# Updating the screen display
	screen.fill("black")
	pygame.draw.line(screen,(200, 200, 200),(WIDTH//2, 0),(WIDTH//2,HEIGHT),width=1)
	pygame.draw.rect(screen, (0, 0, 0), (WIDTH//2-160//2, 0, 160, 40))
	pygame.draw.rect(screen, (255,255, 255), (WIDTH//2-160//2, 0, 160, 40), 2)

	font = pygame.font.Font(None, 36)
	score_text = font.render(f"Score: {round(score)}", True, (255, 255, 255))
	screen.blit(score_text, (WIDTH//2 - 160//2 + 14, 10))

	# displaying the ball layers
	for i, b in enumerate(balls):
		color = tuple(c*i/len(balls) for c in ball.color)
		r = ball.r/2 + ball.r/2*i/len(balls)
		pygame.draw.circle(screen, color, (b[0], b[1]), r)
	pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.r)

	# defining the new ball layers
	if len(balls) > couches: balls = balls[1:]
	balls.append((ball.x, ball.y))

	#displaying the player
	pos1 = (player.x1, player.y, player.width, player.height)
	pos2 = (player.x2, player.y, player.width, player.height)
	pygame.draw.rect(screen, player.color, pos2)
	pygame.draw.rect(screen, player.color, pos1)

	# accelerating the ball
	ball.velocity += 7*dt

	# Handling movements and events
	if score >offset: ball.move(dt)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Running=False

	keys = pygame.key.get_pressed()
	if keys[pygame.K_UP]:
		player.move_up(dt)
	if keys[pygame.K_DOWN]:
		player.move_down(dt)

	if ball.is_out():
		Running=False
	pygame.display.flip()

print(f"Votre score est de : {round(score)}")
ambiance.stop()
pygame.quit()