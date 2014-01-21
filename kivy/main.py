

from glob import glob
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.config import Config

from uno import *



Config.set( 'graphics', 'width', '1024' )
Config.set( 'graphics', 'height', '768' )

class Cardimg( Scatter ):
    '''Image widget to represent cards'''
    source = StringProperty(None)
    loc = ListProperty([0, 0])
    moving = BooleanProperty(True)
	
class HUD( BoxLayout ):
	pass
	
class JadnoApp(App):

    def build(self):
	root = self.root
	root.add_widget( HUD() )
	x_offset = 0
	for card in my_hand.card_list:
	    picture = Cardimg(source=card.image, loc=[(x_offset * 80) + 50, 150] )
	    root.add_widget(picture)
	    x_offset += 1
		
	start_card = Cardimg(
			    source=the_pile.discard[-1].image, 
					loc=[500, 450], moving=False 
					)
	root.add_widget(start_card)
		
    def on_pause(self):
	return True
		
		

my_deck = Deck(make_cards())
my_deck.shuffle()

the_pile = Discard()
the_pile.add_card(my_deck.deal_card())

my_hand = Hand()
	
for i in range( 7 ):
    newly_drawn_card = my_deck.deal_card()
    my_hand.add_card( newly_drawn_card )


if __name__ == '__main__':
    JadnoApp().run()

