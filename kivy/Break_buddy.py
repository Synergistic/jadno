import time
from uno import *
import sys
import kivy	
from kivy.app import App
from kivy.config import Config
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, OptionProperty
from kivy.clock import Clock

from kivy.uix.floatlayout import FloatLayout

Config.set( 'graphics', 'width', '800' )
Config.set( 'graphics', 'height', '600' )

class Itamz( FloatLayout ):
  pass

class JadnoApp(App):
  def build(self):
    return Itamz()
	
do_this = JadnoApp()
do_this.run()





#def player_has_move( player_name, player, top_card ):
	#global turn

	##if the player has no playable cards
	#if not player.has_valid_move( top_card ):

		
		#new_card_drawn = the_deck.deal_card()
		#print player_name, 'has no valid moves, drawing a card.', new_card_drawn
		#player.add_card( new_card_drawn )

		##if the card is not playable, skip the turn
		#if not player.is_valid_move( new_card_drawn, top_card ): 
	  
			#print 'Still none, {0}  lose a turn.'.format( player_name )
			#turn += 1
			#return False
	#return True
  
#def player_discards_card( player, discard_card, top_card ):

  ##check if its a legal move based on current discard card
  #if player.is_valid_move( discard_card, top_card ):

    ##move the card from players hand to discard pile
    #discard_pile.add_card( player.discard_card( discard_card ) )
		
    #player.check_for_uno()

#def game_rules( current_player, cur_string, other_player, oth_string):
	#'''Handles special cards and their functions'''
	
	#global turn, turn_change, message, playing

	##if it is a skip card, skip the next players turn
	#if choosen_Card.rank == 's':
		#message = '{0} was skipped'.format( oth_string )
		#turn += turn_change * 2
		
	##if the card is a wild card	
	#elif choosen_Card.rank in [ 'w', 'wd4' ]:
	
		##prompt user for a new color & set the wild card to that color
		#new_color = raw_input( 'Pick a color to continue play: ' )
		#discard_pile.discard[ -1 ].color = new_color
	
		#turn += turn_change
		
		##if its a wd4, make the other player draw cards and skip them
		#if choosen_Card.rank == 'wd4':
		
			#message = '{0} had the draw four!'.format( oth_string )
			#turn += turn_change
			
			#for i in range(4):
				#other_player.add_card( the_deck.deal_card() )
	
	##if it is a draw 2, make the other player draw and skip them
	#elif choosen_Card.rank == 'd2':
	
		#message = '{0} had to draw two!'.format( oth_string )
		#turn += turn_change * 2
		
		#for i in range(2):
			#other_player.add_card( the_deck.deal_card() )				
	
	##if its a reverse card, change the direction of turns
	#elif choosen_Card.rank == 'r':
	
		#message = 'The turn order was reversed'
		#turn_change *= -1
	
	##otherwise its a plain number, nothing happens
	#else:
		#turn += turn_change

	##check if the player has uno
	#if current_player.uno:
		#print '{0} has uno!!'.format( cur_string )

#def check_for_win( player, player_string ):
	#if len( player.cards ) == 0:
		#print '{0} Wins!!'.format( player_string )
		#playing = False
		#return True


##initialize player hands, the deck, and discard pile		

#player1 = Hand()
#player2 = Hand()

#the_deck = Deck()
#discard_pile = Discard()

#the_deck.shuffle()

##start each player with 7 cards
#for i in range( 7 ):
	#player1.add_card( the_deck.deal_card() )
	#player2.add_card( the_deck.deal_card() )

##put one card on the discard pile to get started
#discard_pile.add_card( the_deck.deal_card() )

##if the first card is a wild, pick a random color to start
#if discard_pile.discard[ - 1 ] in [ 'w', 'wd4' ]:
	#discard_pile.discard[ -1 ].color = random.choice(COLORS)

##initalize turn clock, turn direction, the message, and start the loop
#turn = 0
#turn_change = 1
