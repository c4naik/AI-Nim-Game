import pygame
import pygame_menu
import sys


class Button():
	def __init__(self, label, xpos, ypos, screen):
		self.xpos = xpos  			# x-position on screen
		self.ypos = ypos			# y-position on screen
		self.surf = pygame.surface.Surface((100, 50))   		# width, height of surface for button
		self.screen = screen
		self.font = pygame.font.SysFont("Verdana", 20)				# font size
		self.label = label
		self.txtSurf = self.font.render(self.label, True, (0, 0, 0))

	def draw(self, color = (0, 0, 0)):
		surf = self.surf.copy()
		self.button = self.txtSurf.get_rect(center = (self.surf.get_width() // 2, self.surf.get_height() // 2))		# center of surface
		self.surf.fill(color)
		self.surf.blit(self.txtSurf, self.button)
		self.button.move_ip(self.xpos - self.surf.get_width() // 2, self.ypos + self.surf.get_height())		# move button box to correct screen position

		# screen
		self.screen.blit(self.surf, (self.xpos - self.surf.get_width() // 2, self.ypos + self.surf.get_height()))

class TextBox():
	def __init__(self, xpos, ypos, screen):
		self.xpos = xpos			# x-position on screen
		self.ypos = ypos			# y-position on screen
		self.screen = screen
		self.font = pygame.font.SysFont("Verdana", 20)				# font size
		self.box = pygame.Rect(xpos - 75, ypos, 150, 40)				# width, height

	def textBox(self, text, color = (0, 0, 0), textColor = (0, 0, 0)):
		pygame.draw.rect(self.screen, color, self.box, 3)
		self.txtSurf = self.font.render(text, True, (255,255,255))
		self.screen.blit(self.txtSurf, (self.box.x + 5, self.box.y + 10))			# start text after leaving some padding
		self.box.w = max(150, self.txtSurf.get_width() + 10)						# if text overflows out of text box

class GUI():
	def __init__(self, height = 800, width =800):
		pygame.init()
		self.height = height
		self.width = width

		# create the screen
		self.screen = pygame.display.set_mode((width, height))

		# title, icon and background
		pygame.display.set_caption("NIM")
		self.icon = pygame.image.load("pile.png")
		pygame.display.set_icon(self.icon)
		self.background = pygame.image.load("background.jpg")

		# piles of objects
		self.objImg = pygame.image.load("coin.png")

		self.font = pygame.font.SysFont(None, 40)				# font size

	def bgcolor(self):
		self.screen.fill((0, 0, 0))
		self.screen.blit(self.background, (0, 0))

	def quitgame(self):
		pygame.quit()
		sys.exit()

	def pile(self, pileX, pileY):
		(self.screen).blit(self.objImg, (pileX, pileY))

	def write(self, x, y, text, textColor = (255, 0,255 )):
		self.txtSurf = self.font.render(text, True, textColor)
		self.txtRect = self.txtSurf.get_rect(center = (x, y))
		self.screen.blit(self.txtSurf, self.txtRect)
