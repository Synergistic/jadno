from random import randint
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

from kivy.properties import StringProperty, ListProperty
from kivy.config import Config

from uno import *



Config.set( 'graphics', 'width', '1024' )
Config.set( 'graphics', 'height', '768' )

  

#The main window that contains everything
class JadnoApp(App):
    def build(self):
	root = self.root
	
        player_cards = Widget()
        
        with player_cards.canvas:
	    x = 0
	    for card in player_hand.card_list:
		Color(1, 1, 1, 1)
	        c = Rectangle( pos=(64 * x, 40), size=(64, 96), source=card.image )
	        x += 1
	choices = BoxLayout(orientation='horizontal', 
	pos_hint={'bottom':1}, size_hint=(1, 0.05))
	
	for card in player_hand.card_list:
	    b = Button(text=str(card))
	    choices.add_widget(b)


        root.add_widget(choices)
        root.add_widget(player_cards)


	
###Game logic###
my_deck = Deck(make_cards())
my_deck.shuffle()

player_hand = Hand()
for i in range(16):
  player_hand.add_card( my_deck.deal_card() )
  print player_hand
  
	

#Start game loop
if __name__ == '__main__':
    JadnoApp().run()

