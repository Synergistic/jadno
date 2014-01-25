#UNO the game "Jadno"
import os
import random

RANKS = [ '0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', 
        '6', '6', '7', '7', '8', '8', '9', '9', 's', 's', 'r', 'r', 
		'd2', 'd2', 'wd4', 'w' ]
		
COLORS = [ 'b', 'g', 'r', 'y' ]

class Card( object ):
    ''' A Card object that represents UNO cards.
    It  has a rank; 0-9, skip, reverse, draw two,
    wild, wild draw four. As well as a color; blue, green, red
    yellow'''


    def __init__( self, color, rank, image ):
	    self.rank = rank
	    self.color = color
	    self.image = image

    def __str__( self ):
        if self.color == None:
            return str( self.rank )
	  
        else:
            card_rep = self.color + str( self.rank )
            return card_rep

class Deck( object ):
    '''Jadno deck, made up of Jadno Card objects;
    19 each of Blue, Green, Red, Yellow (0-9)
	1 zero, 2 of each number 1-9 per color
    8 each Draw Two, Reverse, Skip; 2 of each color
    4 Wild cards
    4 Wild Draw Four'''
    def __init__( self, card_list ):
        self.deck_list = card_list

    def __str__( self ):
        deck_rep = " "
        for card in self.deck_list:
            deck_rep += str( card ) + " "
        return deck_rep

    def shuffle( self ):
        random.shuffle( self.deck_list )

    def deal_card( self ):
        return self.deck_list.pop()

class Hand( object ):
    '''a Hand is made up of 1+ Uno cards. Cards
    can be added, or removed (i.e. playing a card)
    '''

    def __init__( self ):
        self.hand_list = []
        self.uno = False

    def __str__( self ):
        hand_rep = " "
        for card in self.hand_list:
            hand_rep += str( card ) + ' '
        return hand_rep

    def add_card( self, card ):
        self.hand_list.append( card )


    def discard_card( self, card ):
        if card in self.hand_list:
            return self.hand_list.pop( self.hand_list.index( card ) )
		
class Discard( object ):
    '''The pile where players discard their Cards'''

    def __init__( self ):
        self.discard_list = []
	 
    def __str__( self ):
        discard_rep = str( len( self.discard_list ) ) + ' ' + str( self.discard_list[ -1 ] )
        return discard_rep

    def add_card( self, card ):
        self.discard_list.append( card )
	    
		
def make_cards():
    cards = []
    for color in COLORS:
        for rank in RANKS:
            if rank in [ 'wd4', 'w' ]:
                image = 'images/' + rank + '.png'
                cards.append( Card( None, rank, image ) )
            else:
                image = 'images/' + color + rank + '.png'
                cards.append( Card( color, rank, image ) )
			
    return cards
	
def is_valid_move(card, top_card):

	#if the played card has the same color as discard pile
	if card.color == top_card.color:
	  return True
	  
	#if the played card has the same rank as the discard
	elif card.rank == top_card.rank or card.rank in [ 'w', 'wd4' ]:
	  return True
	  
	else:
	  return False