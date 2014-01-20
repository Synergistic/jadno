#UNO the game "Jadno"
import os
import random

RANKS = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 's', 'r', 'd2', 'wd4', 'w' ]
COLORS = [ 'R', 'G', 'B', 'Y' ]

class Card( object ):
	''' A Card object that represents UNO cards.
	It  has a rank; 0-9, skip, reverse, draw two,
	wild, wild draw four. As well as a color; blue, green, red
	yellow'''


	def __init__( self, color, rank):
		self.rank = rank
		self.color = color

	def __str__( self ):
		if self.color == None:
		  return str( self.rank )
		  
		else:
		  card_rep = self.color + str( self.rank )
		  return card_rep

class Hand( object ):
	'''a Hand is made up of 1+ Uno cards. Cards
	can be added, or removed (i.e. playing a card)
	'''

	def __init__( self ):
		self.cards = []
		self.uno = False
		
	def __str__( self ):
		hand_rep = " "
		for card in self.cards:
			hand_rep += str( card ) + ' '
		return hand_rep

	def add_card( self, card ):
		self.cards.append( card )


	def discard_card( self, card ):
		if card in self.cards:
			return self.cards.pop( self.cards.index( card ) )


	def check_for_uno( self ):
	#Checks if a player has 'uno'
		if len( self.cards ) == 1:
			self.uno = True
		  
		else:
			self.uno = False

	def is_valid_move( self, card, top_card ):

		#if the played card has the same color as discard pile
		if card.color == top_card.color:
		  return True
		  
		#if the played card has the same rank as the discard
		elif card.rank == top_card.rank or card.rank in [ 'w', 'wd4' ]:
		  return True
		  
		else:
		  return False
		  
	def has_valid_move( self, top_card ):
		for card in self.cards:
		  if self.is_valid_move( card, top_card ):
			return True
		return False
		  
class Deck( object ):
	'''Jadno deck, made up of Jadno Card objects;
	19 each of Blue, Green, Red, Yellow (0-9)
	8 each Draw Two, Reverse, Skip; 2 of each color
	4 Wild cards
	4 Wild Draw Four'''
	def __init__( self ):
		self.deck = []
		for color in COLORS:
		  for rank in RANKS:
			if rank == 0:
			  self.deck.append( Card( color, rank ) )
			  
			elif rank in [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]:
			  self.deck.append( Card( color, rank ) )
			  self.deck.append( Card( color, rank ) )
			  
			elif rank in [ 'wd4', 'w' ]:
			  self.deck.append( Card( None, rank ) )
			  
			elif rank in [ 's', 'r', 'd2' ]:
			  self.deck.append( Card( color, rank) )
			  self.deck.append( Card( color, rank) )
		  
	def __str__( self ):
		deck_rep = " "
		for card in self.deck:
			deck_rep += str( card ) + " "
		return deck_rep

	def shuffle( self ):
		random.shuffle( self.deck )

	def deal_card( self ):
	  return self.deck.pop()
	
class Discard( object ):
	'''The pile where players discard their Cards'''

	def __init__( self ):
		self.discard = []
	 
	def __str__( self ):
		discard_rep = str( len( self.discard ) ) + ' ' + str( self.discard[ -1 ] )
		return discard_rep

	def add_card( self, card ):
		self.discard.append( card )
	    
def player_has_move( player_name, player, top_card ):
	'''Does the player have any possible moves? If not, then
	draw a card and check again. If they still don't have any
	moves after drawing, then skip their current turn.'''
	
	global turn

	#if the player has no playable cards
	if not player.has_valid_move( top_card ):

		
		new_card_drawn = the_deck.deal_card()
		print player_name, 'has no valid moves, drawing a card.', new_card_drawn
		player.add_card( new_card_drawn )

		#if the card is not playable, skip the turn
		if not player.is_valid_move( new_card_drawn, top_card ): 
	  
			print 'Still none, {0}  lose a turn.'.format( player_name )
			turn += 1
			return False
	return True
  
def player_discards_card( player, discard_card, top_card ):
	'''makes sure the players choosen card can legally be discarded.
	Adds the card to the discard pile and then checks for uno (1 card)'''
	
	#check if its a legal move based on current discard card
	if player.is_valid_move( discard_card, top_card ):

		#move the card from players hand to discard pile
		discard_pile.add_card( player.discard_card( discard_card ) )
		
		player.check_for_uno()
		
def match_string_to_card( card_string, player ):
	''' converts the users entered string to the correct card in hand'''

	if card_string.isalnum():
	#if the string contains a color

		if card_string[ 0 ] in COLORS:
			#the color is the first item
			color = card_string[ 0 ]
	  
			# the rank is everything after that
			rank = card_string[ 1: ]

		#if it does not contain a color
		elif card_string[ 0: ] in RANKS:
			color = None
			rank = card_string[ 0: ]

		else:
			return False
	else:
		return False

  #check for a card with matching color/rank in players hand
	for card in player.cards:
		if color == None:
		  if card.rank == rank:
			return card

		elif card.rank == rank and card.color == color:
			return card
	return False

def game_rules( current_player, cur_string, other_player, oth_string):
	'''Handles special cards and their functions'''
	
	global turn, turn_change, message, playing

	#if it is a skip card, skip the next players turn
	if choosen_Card.rank == 's':
		message = '{0} was skipped'.format( oth_string )
		turn += turn_change * 2
		
	#if the card is a wild card	
	elif choosen_Card.rank in [ 'w', 'wd4' ]:
	
		#prompt user for a new color & set the wild card to that color
		new_color = raw_input( 'Enter the first letter of your desired color: ' ).capitalize()
		discard_pile.discard[ -1 ].color = new_color
	
		turn += turn_change
		
		#if its a wd4, make the other player draw cards and skip them
		if choosen_Card.rank == 'wd4':
		
			message = '{0} had the draw four!'.format( oth_string )
			turn += turn_change
			
			for i in range(4):
				other_player.add_card( the_deck.deal_card() )
	
	#if it is a draw 2, make the other player draw and skip them
	elif choosen_Card.rank == 'd2':
	
		message = '{0} had to draw two!'.format( oth_string )
		turn += turn_change * 2
		
		for i in range(2):
			other_player.add_card( the_deck.deal_card() )				
	
	#if its a reverse card, change the direction of turns
	elif choosen_Card.rank == 'r':
	
		message = 'The turn order was reversed'
		turn_change *= -1
	
	#otherwise its a plain number, nothing happens
	else:
		turn += turn_change

	#check if the player has uno
	if current_player.uno:
		print '''===============
={0} has Jadno!!=
==============='''.format( cur_string )

def check_for_win( player, player_string ):
	'''Check to see if a player has no remaining cards'''
	
	if len( player.cards ) == 0:
		print '{0} Wins!!'.format( player_string )
		playing = False
		return True

def prompt_user_for_card( player, player_string):
	'''Display the hand, discard pile, and ask user what they want to play'''
	
	discard_card = raw_input( 
	'\n' + player_string + ' Turn\n' + 'Hand: ' + str( player ) + '\nDiscard Pile: ' + str( top_card ) + '\nWhat card would you like to play? ' )
	  
	return match_string_to_card( discard_card, player )		
	
	
#initialize player hands, the deck, and discard pile		
player1 = Hand()
player2 = Hand()

the_deck = Deck()
discard_pile = Discard()

the_deck.shuffle()

#start each player with 7 cards
for i in range( 7 ):
	player1.add_card( the_deck.deal_card() )
	player2.add_card( the_deck.deal_card() )

#pick the first card to start the discard pile
discard_pile.add_card( the_deck.deal_card() )

#if the first card is a wild, pick a random color for it
if discard_pile.discard[ -1 ].rank in [ 'w', 'wd4' ]:
	discard_pile.discard[ -1 ].color = random.choice(COLORS)
	

	
#initalize turn clock, turn direction, the message, and start the loop
turn = 0
turn_change = 1 #for reverse cards
playing = True


print '''\nWelcome to Jadno, an Uno clone!\n
Cards are representated as such; COLORcardtype
For example, a red 2 would be R2.
===============================\n
Colors: Red, Yellow, Blue, Green
w = Wild, wd4 = Wild Draw 4, 
d2 = Draw 2, r = Reverse, s = Skip\n
To play a card, simply type in the 
matching string, it is case sensitive.
==============================='''

#start game loop
while playing:

	if turn % 2 == 0: #player 1 turn

	#store the card on top of the discard pile
		top_card = discard_pile.discard[-1]
		# os.system('cls' if os.name=='nt' else 'clear')
		#if the player can make a move
		if player_has_move( 'Player 1', player1, top_card ):
		
			choosen_Card = prompt_user_for_card( player1, 'Player 1' )
			
			#if its in the players hand
			if choosen_Card:

				#the player discards a card to the pile
				player_discards_card( player1, choosen_Card, top_card )
				
				#checks for special cards and takes appropriate action
				game_rules( player1, 'Player 1', player2, 'Player 2')
				
				#sees if that was the players last card, for the win
				if check_for_win( player1, 'Player 1' ):
					break
					
	if turn % 2 == 1: #player 2 turn
		# os.system('cls' if os.name=='nt' else 'clear')
		#store the card on top of the discard pile
		top_card = discard_pile.discard[-1]

		#if the player can make a move
		if player_has_move( 'Player 2', player2, top_card ):
	  
			choosen_Card = prompt_user_for_card( player2, 'Player 2')
			
			#if the chosen card is in the player's hand
			if choosen_Card:

				#the player discards a card to the pile
				player_discards_card( player2, choosen_Card, top_card )
			
				game_rules( player2, 'Player 2', player1, 'Player 1')
				
				if check_for_win( player2, 'Player 2' ):
					break
					