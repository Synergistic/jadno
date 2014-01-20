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
	#19 each of Blue, Green, Red, Yellow (0-9)
	#8 each Draw Two, Reverse, Skip; 2 of each color
	#4 Wild cards
	#4 Wild Draw Four
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
	    
					