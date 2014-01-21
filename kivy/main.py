

from glob import glob
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter

from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.config import Config

from uno import *



Config.set( 'graphics', 'width', '1280' )
Config.set( 'graphics', 'height', '960' )

class Cardimg( Scatter ):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''

    source = StringProperty(None)
    loc = ListProperty([0, 0])

class JadnoApp(App):

    def build(self):

        # the root is created in pictures.kv
        root = self.root

        x_offset = 0
        for card in my_hand.card_list:
            picture = Cardimg(source=card.image, loc=[(x_offset * 80) + 50, 150] )
            root.add_widget(picture)
            x_offset += 1

    def on_pause(self):
        return True
		
		

my_deck = Deck(make_cards())
my_deck.shuffle()

my_hand = Hand()
	
for i in range( 7 ):
	newly_drawn_card = my_deck.deal_card()
	my_hand.add_card( newly_drawn_card )


if __name__ == '__main__':
    JadnoApp().run()

