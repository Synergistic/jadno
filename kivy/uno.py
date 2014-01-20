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
	
	