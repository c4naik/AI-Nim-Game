import os
import re
import random
from gui import *

class Nim():
	def __init__(self, board = [9, 6, 6, 5, 3, 2]):
		self.board = board
		self.mode = 2
		self.player1 = 1
		self.player2 = 2
		self.winner = None
		self.playerMovesHistory = list()
		self.aiMovesHistory = list()
		self.gameDisplay = GUI()
		self.menuHeight = 500
		self.menuWidth = 500
		self.Player1Name = "Player 1"
		self.Player2Name = "Player 2"

	def setMode1(self, PvsAIMenu):
		global endGame
		endGame = False
		self.mode = 1
		self.saveNames(PvsAIMenu)
		play(game)
		endGame = True

	def setMode2(self, PvsPMenu):
		global endGame
		endGame = False
		self.mode = 2
		self.saveNames(PvsPMenu)
		play(game)
		endGame = True

	def saveNames(self, menu):
		names = menu.get_input_data()
		for key in names.keys():
			if key == "playerName":
				self.Player1Name = names[key]
				self.Player2Name = "AI"
			elif key == "player1":
				self.Player1Name = names[key]
			elif key == "player2":
				self.Player2Name = names[key]

	def playAgain(self):
		global playAgain
		playAgain = True

	def menuSetup(self):
		global endGame
		global playAgain

		# Create Player vs AI menu
		PvsAIMenu = pygame_menu.Menu(
			height = self.menuHeight,
			width = self.menuWidth,
			title = "Enter Player Name",
			enabled = True,
			theme = mainTheme
		)

		PvsAIMenu.add.text_input(
			"Player Name : ",
			default = "Human",
			textinput_id = "playerName"
			)

		PvsAIMenu.add.button("Play", self.setMode1, PvsAIMenu)

		PvsAIMenu.add.button("Back", pygame_menu.events.BACK)

		PvsAIMenu.add.button("Quit", pygame_menu.events.EXIT)

		# Create Player vs Player Menu
		PvsPMenu = pygame_menu.Menu(
			height = self.menuHeight,
			width = self.menuWidth,
			title = "Enter Player Names",
			enabled = True,
			theme = mainTheme
		)

		PvsPMenu.add.text_input(
			"Player 1 : ",
			default = "Player 1",
			textinput_id = "player1"
			)


		PvsPMenu.add.text_input(
			"Player 2 : ",
			default = "Player 2",
			textinput_id = "player2"
			)

		PvsPMenu.add.button("Play", self.setMode2, PvsPMenu)

		PvsPMenu.add.button("Back", pygame_menu.events.BACK)

		PvsPMenu.add.button("Quit", pygame_menu.events.EXIT)

		# Create MODE menu
		modeMenu = pygame_menu.Menu(
			height = self.menuHeight,
			width = self.menuWidth,
			title = "Select Mode",
			enabled = True,
			theme = mainTheme,
		)

		modeMenu.add.button("Against AI", PvsAIMenu)

		modeMenu.add.button("Against another Player", PvsPMenu)

		modeMenu.add.button("Quit", pygame_menu.events.EXIT)

		# Create play again menu
		againMenu = pygame_menu.Menu(
			height = self.menuHeight,
			width = self.menuWidth,
			title = "Play Again?",
			enabled = True,
			theme = mainTheme,
		)

		againMenu.add.button("Yes", self.playAgain)

		againMenu.add.button("No", pygame_menu.events.EXIT)

		while True:
			self.gameDisplay.bgcolor()
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					self.gameDisplay.quitgame()

			if not endGame and modeMenu.is_enabled():
				modeMenu.update(events)
				modeMenu.draw(self.gameDisplay.screen)

			elif againMenu.is_enabled():
				if(self.winner == self.player1):
					self.gameDisplay.write(self.gameDisplay.width // 2, 100, "{} won!".format(self.Player1Name))
				else:
					self.gameDisplay.write(self.gameDisplay.width // 2, 100, "{} won!".format(self.Player2Name))

				againMenu.update(events)
				againMenu.draw(self.gameDisplay.screen)

			if playAgain:
				break

			pygame.display.flip()


	def drawGame(self):
		count = 1
		pileX = 5	# Start after leaving 5 px margin on the left
		pileY = self.gameDisplay.height - (self.gameDisplay.font.get_height() * 2) - (self.gameDisplay.objImg).get_height()	 # Start after leaving 32px margin at the bottom, therefore total 64 + 32 px; 64 px height for the object in pile, 32px for the pile number since font size is 32

		next = ((self.gameDisplay.width - (2 * pileX) - ((self.gameDisplay.objImg).get_width()) * len(self.board)) / (len(self.board) - 1)) + (self.gameDisplay.objImg).get_width()		# {[width - (2 * space left on the left side) - (width of object * number of rows)] / number of rows - 1} + width of object; eg. {[800 - (2 * 5) - (64 * 6)] / 5} + 64

		self.gameDisplay.bgcolor()
		labelY = self.gameDisplay.height - self.gameDisplay.font.get_height()			# since font height = 22

		# Draw the board
		for pile in self.board:
			labelX = pileX + (self.gameDisplay.objImg).get_width() / 2		# since have to get center of pile
			self.gameDisplay.write(labelX, labelY, str(count), (255, 200, 200))
			count = count + 1

			for _ in range(pile):
				self.gameDisplay.pile(pileX, pileY)
				pileY -= (self.gameDisplay.objImg).get_height() / 2

			pileY = self.gameDisplay.height - (self.gameDisplay.font.get_height() * 2) - (self.gameDisplay.objImg).get_height()	 # Start after leaving 32px margin at the bottom, therefore total 64 + 32 px; 64 px height for the object in pile, 32px for the pile number since font size is 32
			pileX += next


	def getCorrectRow(self, row):
		try:
			row = int(row)
			if not 1 <= row <= len(self.board):
				return "Error! There are {} rows!".format(len(self.board))

			else:
				if(self.board[row-1] < 1):
					return "Error! That row is empty!"
				else:
					return row - 1
		except:
			return "Please enter a valid move!"


	def getCorrectAmount(self, amount, row):
		try:
			amount = int(amount)
			if amount < 1 or amount > self.board[row]:
				return "Error! Illegal amount!"
			else:
				return amount
		except:
			return "Please enter a valid move!"


	def remove(self, currentPlayer):
		rowbox = TextBox(self.gameDisplay.width // 3, (self.gameDisplay.font.get_height() * 2) + 40, self.gameDisplay.screen)
		row = ''
		amountbox = TextBox((self.gameDisplay.width // 3) * 2, (self.gameDisplay.font.get_height() * 2) + 40, self.gameDisplay.screen)
		amount = ''
		submit = Button("Submit", self.gameDisplay.width // 2, (self.gameDisplay.font.get_height() * 2) + rowbox.box.h + 10, self.gameDisplay.screen)
		colorActive = (255, 0, 0)
		colorPassive = (204, 204, 204)
		rowcolor = colorPassive
		amountcolor = colorPassive
		rowboxActive = False
		amountboxActive = False
		finalrow = None
		finalamount = None

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.gameDisplay.quitgame()

				elif event.type == pygame.MOUSEBUTTONDOWN:
					position = pygame.mouse.get_pos()
					if rowbox.box.collidepoint(position):
						rowboxActive = True
						amountboxActive = False

					else:
						rowboxActive = False

					if amountbox.box.collidepoint(position):
						amountboxActive = True
						rowboxActive = False

					else:
						amountboxActive = False

					if submit.button.collidepoint(position):
						finalrow = self.getCorrectRow(row)

						if not isinstance(finalrow, str):
							finalamount = self.getCorrectAmount(amount, finalrow)
						else:
							continue
						if not isinstance(finalamount, str):
							self.board[finalrow] -= finalamount
							playerMovemessage = "{} removed : {} from row : {}".format(currentPlayer, finalamount, finalrow + 1)
							(self.playerMovesHistory).append(playerMovemessage)
							self.displayPreviousmove()
							return
						else:
							continue

				elif event.type == pygame.KEYDOWN:
					if rowboxActive:
						if event.key == pygame.K_BACKSPACE:
							row = row[:-1]
						else:
							row += event.unicode

					elif amountboxActive:
						if event.key == pygame.K_BACKSPACE:
							amount = amount[:-1]
						else:
							amount += event.unicode

			self.drawGame()

			self.gameDisplay.write(self.gameDisplay.height // 3, self.gameDisplay.font.get_height() * 3, "Row", (255, 255, 0))

			self.gameDisplay.write((self.gameDisplay.height // 3) * 2, self.gameDisplay.font.get_height() * 3, "Amount", (255, 255, 0))

			self.gameDisplay.write(self.gameDisplay.height // 2, self.gameDisplay.font.get_height(), currentPlayer + '\'s turn!', (255, 255, 0))

			submit.draw((153, 204, 255))

			position = pygame.mouse.get_pos()
			if submit.button.collidepoint(position):
				submit.draw((153, 204, 255))

			else:
				submit.draw((51, 153, 255))

			if rowboxActive:
				rowcolor = colorActive
			else:
				rowcolor = colorPassive

			if amountboxActive:
				amountcolor = colorActive
			else:
				amountcolor = colorPassive

			rowbox.textBox(row, rowcolor)
			amountbox.textBox(amount, amountcolor)

			if finalrow is not None and finalamount == None:
				self.gameDisplay.write((self.gameDisplay.height // 2), self.gameDisplay.font.get_height() * 2, finalrow, (204, 0, 0))
			elif finalamount is not None:
				self.gameDisplay.write((self.gameDisplay.height // 2), self.gameDisplay.font.get_height() * 2, finalamount, (204, 0, 0))

			pygame.display.update()


	def changePlayer(self):
		if self.player1 == 1:
			self.player1 = 2
		else:
			self.player1 = 1


	def checkWin(self, currentPlayer):

		for value in range(len(self.board)):
			if self.board[value] > 0:
				self.changePlayer()
				return

		self.winner = currentPlayer


	def isBalanced(self, tempBoard):
		balanced = 0
		for row in range(len(self.board)):
			balanced = balanced ^ (tempBoard[row])

		if balanced == 0:
			return True
		else:
			return False


	def AImove(self):
		boardBalanced = False
		rowTraversed = 0
		tempBoard = (self.board).copy()

		if(self.isBalanced(tempBoard)):
			for row in range(len(self.board)):
				if(tempBoard[row] > 0):
					tempBoard[row] -= 1
					aiMovemessage = "AI removed : 1 from row : {}".format(row + 1)
					(self.aiMovesHistory).append(aiMovemessage)
					self.board = tempBoard.copy()
					break

		else:
			for row in range(len(self.board)):
				amount = 0
				rowTraversed += 1
				if(tempBoard[row] > 0):
					for object in range(tempBoard[row]):
						tempBoard[row] -= 1
						amount += 1

						if(self.isBalanced(tempBoard)):
							boardBalanced = True
							aiMovemessage = "AI removed : {} from row : {}".format(amount, row + 1, rowTraversed)
							(self.aiMovesHistory).append(aiMovemessage)
							self.board = tempBoard.copy()
							break

						if(tempBoard[row] == 0):
							tempBoard = self.board.copy()

					if(boardBalanced):
						break

		self.displayPreviousmove(player = 'ai')


	def displayPreviousmove(self, player = ''):
		if(player == 'ai'):
			if(len(self.aiMovesHistory) > 0):
				print(self.aiMovesHistory[-1])
		else:
			if(len(self.playerMovesHistory) > 0):
				print(self.playerMovesHistory[-1])


def play(game, currentPlayer = None):
	game.drawGame()

	if currentPlayer is None:
		currentPlayer = random.randint(1, 2)

	if(game.mode == 1):
		# vs AI setup
		while not game.winner:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game.gameDisplay.quitgame()

			if(currentPlayer == game.player1):
				print(game.player1)
				game.remove(game.Player1Name)
			else:
				game.AImove()

			game.checkWin(currentPlayer)

	else:
		# 2 player mode setup
		while not game.winner:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game.gameDisplay.quitgame()

			if(currentPlayer == game.player1):
				game.remove(game.Player1Name)
			else:
				game.remove(game.Player2Name)

			game.checkWin(currentPlayer)

while True:
	mainTheme = pygame_menu.themes.THEME_SOLARIZED.copy()
	mainTheme.background_color = (255, 244, 153, 100)
	mainTheme.title_background_color = (0, 0, 0, 100)
	mainTheme.title_font_color = (255, 255, 255)
	mainTheme.widget_font_color = (200, 200, 200)
	mainTheme.selection_color = (0, 0, 0)
	mainTheme.menubar_close_button = False
	game = Nim()
	game.gameDisplay.bgcolor()
	endGame = False
	playAgain = False

	# Choose the mode
	game.menuSetup()
	os.execl(sys.executable, sys.executable, *sys.argv)
