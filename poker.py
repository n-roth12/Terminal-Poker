import random as r
import numpy as np
import time

RANKS = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
SUITS = ['D', 'S', 'H', 'C']
cardsInGame = []
communityCards = [] 

class Card:
	"""
	A class used to represent a Card in the Game
	
	Attributes:
		rank : str
		the number, also called rank, on the card

		suit : str
		the suit, which can be one of four options
		'D' = Diamonds, 'S' = Spades, 'H' = Hearts, 'C' = Clubs
	"""
	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit
	def getRank(self):
		return self.rank
	def getSuit(self):
		return self.suit
	def display(self):
		if self.rank > 10:
			if self.rank == 11:
				faceCard = 'J'
			elif self.rank == 12:
				faceCard = 'Q'
			elif self.rank == 13:
				faceCard = 'K'
			else:
				faceCard = 'A'
			return '|' + faceCard + str(self.suit) + '|'
		else:
			return '|' + str(self.rank) + str(self.suit) + '|'

class Player:
	"""
	A class used to represent a player in the Game
	A player can be either the user or an automated player

	Attributes:
		card1, card2 : Card, Card
		The two pocket Cards that the player is dealt

		hand_strength : int
		A numerical representation of the strength of the players hand
		Ranges from 11 to 1, with 11 being the worst and 1 being the best

		hand : Cards[]
		The total list of Cards at the Players disposal, including the 
		community cards

		id : int
		The unique identifier for the player

		hand_name : str
		Name of the type of hand that a player has
		Can be 'Pair', 'Two-Pair', 'Flush', etc.

		best_hand : Cards[]
		The strongest five cards that the player has

		current_bet : int
		The amount that the player current has placed in the pot during 
		the active betting phase
	"""
	def __init__(self, card1, card2, id):
		self.card1 = card1
		self.card2 = card2
		self.hand_strength = 11
		self.hand = [card1, card2]
		self.id = id
		self.hand_name = 'none'
		self.best_hand = [card1, card2]
		self.current_bet = -1
	def getPocket(self):
		return [self.card1, self.card2]
	def getHand(self):
		return self.hand
	def setHand(self, hand):
		self.hand = hand
	def display(self):
		string = ''
		for card in self.hand:
			string = string + card.display() + '  '
		return string
	def setHandStrength(self, strength):
		self.hand_strength = strength
	def getHandStrength(self):
		return self.hand_strength
	def getId(self):
		return self.id
	def getHandName(self):
		return self.hand_name
	def getBestHand(self):
		return self.best_hand
	def updateHand(self):
		all_cards = [self.card1, self.card2] + communityCards
		self.hand = all_cards
		hand_result = checkHand(sort(self.hand))
		self.hand_name = hand_result[0]
		self.best_hand = hand_result[1]
		self.hand_strength = hand_result[2]
	def getCurrentBet(self):
		return self.current_bet
	def setCurrentBet(self, bet):
		self.current_bet = bet

class Game:
	"""
	A class to represent a Game of poker

	Attributes:
		players : Player[]
		The list of players in the current Game

		pot : int
		The total amount bet by all the players in the current Game

		phase : int
		The current phase of the Game
		1 for pre-flop, 2 for flop, etc.

		current_bet : int
		The current bet of the active phase of the Game
		The bet that any player must make to not fold
	"""
	def __init__(self, players):
		self.players = players
		self.pot = 0
		self.phase = 1
		self.current_bet = 0
	def getBet(self):
		return self.current_bet
	def setBet(self, bet):
		self.current_bet = bet
	def advancePhase(self):
		self.phase = self.phase + 1
		self.current_bet = 0
	def getPhase(self):
		return self.phase
	def getPot(self):
		return self.pot
	def setPot(self, pot):
		self.pot = pot

def makeBet(player, game):
	strength = player.getHandStrength()
	phase = game.getPhase()
	if phase == 1:
		return 11 - strength
	elif phase == 2:
		return 11 - strength
	else:
		return 10 - strength

def checkSame(card1, card2):
	if (card1.getRank() == card2.getRank()) and (card1.getSuit() == card2.getSuit()):
		return True
	else: 
		return False

def checkForRepeat(new_card):
	for card in cardsInGame:
		if checkSame(new_card, card):
			return True
	return False

def generateCard():
	rank = r.randint(0, len(RANKS)-1)
	suit = r.randint(0, len(SUITS)-1)
	new_card = Card(RANKS[rank], SUITS[suit])
	if len(cardsInGame) > 0:
		if checkForRepeat(new_card):
			return generateCard()
		else:
			cardsInGame.append(new_card)
			return new_card
	else:
		cardsInGame.append(new_card)
		return new_card

def generateFlop():
	for i in range(0, 3):
		communityCards.append(generateCard())
	print('\n')
	print('Flop: ', displayHand(communityCards))
	print('\n')

def generateTurn():
	communityCards.append(generateCard())
	print('\n')
	print('Turn: ', displayHand(communityCards))
	print('\n')

def generateRiver():
	communityCards.append(generateCard())
	print('\n')
	print('River: ', displayHand(communityCards))
	print('\n')

def updateAllHands(players):
	for player in players:
		player.updateHand()

def displayHand(hand):
	string = hand[0].display()
	for i in range(1, len(hand)):
		string = string + ' ' + hand[i].display()
	return string

def sort(hand):
	for i in range(0, len(hand)):
		min_index = i
		for j in range(i+1, len(hand)):
			if hand[j].getRank() > hand[min_index].getRank():
				min_index = j
		hand[i], hand[min_index] = hand[min_index], hand[i]
	return hand

def checkHand(hand):
	counts = [0] * len(RANKS)
	for card in hand:
		rank_index = RANKS.index(card.getRank())
		counts[rank_index] = counts[rank_index] + 1		
	straight_flush_result = checkStraightFlush(hand)
	if len(straight_flush_result) > 1:
		return straight_flush_result
	elif 4 in counts:
		return getFourOfAKind(hand, counts)
	elif (3 in counts) and (2 in counts):
		return getFullHouse(hand, counts)
	flush_result = checkFlush(hand)
	if len(flush_result) > 1:
		return flush_result
	straight_result = checkStraight(hand)
	if len(straight_result) > 1:
		return straight_result
	elif 3 in counts:
		return getThreeOfAKind(hand, counts)
	elif counts.count(2) >= 2:
		return getTwoPair(hand, counts)
	elif 2 in counts:
		return getPair(hand, counts)
	else:
		return ['High Card', findHighs(hand, [], 5), 10]

def checkStraightFlush(hand):
	flush_result = checkFlush(hand)
	if len(flush_result) > 1:
		straight_result = checkStraight(flush_result[1])
		if len(straight_result) > 1:
			straight_flush_hand = straight_result[1]
			if straight_flush_hand[0].getRank() == 14:
				return ['Royal Flush', straight_flush_hand, 1]
			else:
				return ['Straight Flush', straight_flush_hand, 2]
		else:
			return ['You do not have a straight flush']
	else:
		return ['You do not have a straight flush']

def checkFlush(hand):
	counts = [0, 0, 0, 0]
	for i in range(0, len(hand)):
		count_index = SUITS.index(hand[i].getSuit())
		counts[count_index] = counts[count_index] + 1
	if any(count >= 5 for count in counts):
		flush_suit = SUITS[counts.index(max(counts))]
		flush_hand = []
		index = 0
		while(len(flush_hand)) < max(counts):
			if hand[index].getSuit() == flush_suit:
				flush_hand.append(hand[index])
			index = index + 1
		return ['Flush', flush_hand, 5]
	else:
		return ['You do not have a flush']

def checkStraight(hand):
	for i in range(0, len(hand)-4):
		first_rank = hand[i].getRank()
		if first_rank == 5:
			if first_rank == hand[i+1].getRank()+1 == hand[i+2].getRank()+2 == hand[i+3].getRank()+3 == hand[0].getRank()-9:
				straight_hand = [hand[i], hand[i+1], hand[i+2], hand[i+3], hand[0]]
				return ['Straight', straight_hand, 6]
		if first_rank == hand[i+1].getRank()+1 == hand[i+2].getRank()+2 == hand[i+3].getRank()+3 == hand[i+4].getRank()+4:
			straight_hand = [hand[i], hand[i+1], hand[i+2], hand[i+3], hand[i+4]]
			return ['Straight', straight_hand, 6]
	return ['You do not have a straight']

def getFourOfAKind(hand, counts):
	best_hand = []
	for card in hand:
		if card.getRank() == RANKS[counts.index(4)]:
			best_hand.append(card) 
	best_hand.append(findHighs(hand, [RANKS[counts.index(4)]], 1)[0])
	return ['Four-of-a-Kind', best_hand, 3]

def getFullHouse(hand, counts):
	best_hand = []
	for card in hand:
		if card.getRank() == RANKS[counts.index(3)]:
			best_hand.append(card)
	for card in hand:
		if card.getRank() == RANKS[counts.index(2)]:
			best_hand.append(card)
	return ['Full House', best_hand, 4]

def getThreeOfAKind(hand, counts):
	best_hand = []
	for card in hand:
		if card.getRank() == RANKS[counts.index(3)]:
			best_hand.append(card)
	highs = findHighs(hand, [RANKS[counts.index(3)]], 2)
	for card in highs:
		best_hand.append(card)
	return ['Three-of-a-Kind: ', best_hand, 7]

def getTwoPair(hand, counts):
	best_hand = []
	indices = [i for i, count in enumerate(counts) if count == 2]
	for card in hand:
		if card.getRank() == RANKS[indices[0]]:
			best_hand.append(card)
	for card in hand:
		if card.getRank() == RANKS[indices[1]]:
			best_hand.append(card)
	best_hand.append(findHighs(hand, [RANKS[indices[0]], RANKS[indices[1]]], 1)[0])
	return ['Two-Pair', best_hand, 8]

def getPair(hand, counts):
	best_hand = []
	for card in hand:
		if card.getRank() == RANKS[counts.index(2)]:
			best_hand.append(card)
	highs = findHighs(hand, [RANKS[counts.index(2)]], 3)
	for card in highs:
		best_hand.append(card)
	return ['Pair', best_hand, 9]

def findHighs(hand, values, cards_needed):
	highest_cards = []
	index = 0
	while len(highest_cards) < cards_needed:
		if hand[index].getRank() not in values:
			highest_cards.append(hand[index])
		index = index + 1
	return highest_cards

def advance(game, players):
	for player in players:
		player.setCurrentBet(-1)
	game.advancePhase()

def userBet(player, game):
	print('\n')
	print('Your hand is: ' + player.display())
	print('Place your bet: ')
	if game.getBet() > 0 :
		print('(Enter less than ' + str(game.getBet()) + ' to fold)')
	return(int(input()))

def betPhase(game, players):
	"""
	Carries out the betting for each phase of the game.
	Each player gets the chance to raise, call, or flop. Then the betting
	continues until all players have called the last raise or folded.
	:type game: Game
	:type players: List[Player]
	"""
	index = 0
	count = 0
	last_raiser_id = players[0].id
	curr_player = players[0]

	print('Current pot: ' + str(game.getPot()))
	print('\n')

	while not (curr_player.id == last_raiser_id and count > 0):
		time.sleep(0.5)

		if curr_player.id == -1:
			bet = userBet(players[index], game)
		else:
			bet = makeBet(players[index], game)

		if bet < game.getBet():
			if curr_player.id != -1:
				print('Player ' + str(curr_player.id) + ' folds')
			else:
				print('You folded')
			players.remove(curr_player)
			index = index - 1

		elif bet == game.getBet():
			if curr_player.id != -1:
				print('Player ' + str(curr_player.id) + ' calls ' + str(bet))
			else:
				print('You called ' + str(bet))
			game.setPot(game.getPot() + bet)

		elif bet > game.getBet():
			game.setBet(bet)
			game.setPot(game.getPot() + bet)
			last_raiser_id = curr_player.id
			if curr_player.id != -1:
				print('Player ' + str(curr_player.id) + ' raises ' + str(bet))
			else:
				print('You raised ' + str(bet))

		count += 1
		index = (index + 1) % len(players)
		curr_player = players[index]


def playGame(num_players):
	"""
	:type num_players: int
	Plays a full game of poker. Players are initialized with two Cards
	then added to the Game. All Cards are generated then added to the 
	CardInGame list.
	"""
	print(' \n\n\n----------------------------')
	print('STARTING GAME WITH ' + str(num_players) + ' PLAYERS')
	print('----------------------------\n')
	time.sleep(1)

	players = []
	cardsInGame = []
	for i in range(0, num_players):
		player = Player(generateCard(), generateCard(), i + 1)
		players.append(player)
	user = Player(generateCard(), generateCard(), 0)
	game = Game(players + [user])

	user_player = Player(generateCard(), generateCard(), -1)	# Player.id = -1 for user 
	players.append(user_player)

	# Pre-flop betting phase
	betPhase(game, players)
	if len(players) == 1:
		if players[0].id != -1:
			print('Player ' + str(players[0].getId()) + ' wins before showdown!')
		else:
			print('You win before showdown!')
		return

	time.sleep(0.5)
	generateFlop()
	advance(game, players)
	updateAllHands(players)

	# Flop betting phase
	betPhase(game, players)
	if len(players) == 1:
		if players[0].id != -1: 
			print('Player ' + str(players[0].getId()) + ' wins before showdown!')
		else:
			print('You win before showdown!')
		return

	time.sleep(0.5)
	generateTurn()
	advance(game, players)
	updateAllHands(players)

	# Turn betting phase
	betPhase(game, players)
	if len(players) == 1:
		if players[0].id != -1:
			print('Player ' + str(players[0].getId()) + ' wins before showdown!')
		else:
			print('You win before showdown!')
		return

	time.sleep(0.5)
	generateRiver()
	advance(game, players)
	updateAllHands(players)

	# River betting phase
	betPhase(game, players)
	if len(players) == 1:
		if players[0].id != -1:
			print('Player ' + str(players[0].getId()) + ' wins before showdown!')
		else:
			print('You win before showdown!')
		return

	print('\n')
	index = 1
	for player in players:
		print('Player ' + str(player.getId()) + ' pocket: ', displayHand(player.getPocket()))
		print('Player ' + str(player.getId()) + ' hand result: ', displayHand(player.getBestHand()))
		print('Player ' + str(player.getId()) + ' final hand: ', player.getHandName())
		print('Player ' + str(player.getId()) + ' hand strength: ', player.getHandStrength())
		print('\n')
		index = index + 1

	for winner in getWinner(players):
		if winner.id != -1:
			print('Player ' + str(winner.getId()) + ' Wins with ' + winner.getHandName() + ': ' +  displayHand(winner.getBestHand()))
		else:
			print('You Win with ' + winner.getHandName() + ': ' + displayHand(winner.getBestHand()))

def getWinner(players):
	"""
	:type players: List[Player]
	:rtype: List[Player]
	Returns the players that had the best hand in the game.
	This will usually be one player.
	"""
	strengths = [player.getHandStrength() for player in players]
	winners = []
	for i in range(0, len(players)):
		if strengths[i] == min(strengths):
			winners.append(players[i])
	if len(winners) == 1:
		return winners
	else: 
		for i in range(0, 5):
			next_card = [player.getHand()[i].getRank() for player in winners]
			high = max(next_card)
			winners = [player for player in winners if player.getHand()[i].getRank() == high]
			if len(winners) == 1:
				return winners
	return winners

def checkPlayAgain():
	print('Would you like to play again? (Y/N): ')
	given_answer = False
	while not given_answer:
		answer = input().lower()
		if answer == 'y':
			return True
		elif answer == 'n':
			return False
		else:
			print('Please enter Y to play again and N to stop playing: ')

if __name__ == '__main__':
	print('Enter number of opponents: ')
	num_players = int(input())
	keep_playing = True

	while keep_playing:
		playGame(num_players)
		keep_playing = checkPlayAgain()

	print('Thanks for playing!')
	print('\n')





