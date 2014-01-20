

from glob import glob
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.config import Config

from uno import *



Config.set( 'graphics', 'width', '1280' )
Config.set( 'graphics', 'height', '720' )

class Cardimg(Scatter):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''

    source = StringProperty(None)


class JadnoApp(App):

    def build(self):

        # the root is created in pictures.kv
        root = self.root

        # get any files into images directory
        # curdir = dirname(__file__)
		
        for i in range( 10 ):
            card = my_deck.deck_list[randint(0, len(my_deck.deck_list)-1)]
            picture = Cardimg(source=card.image)
            root.add_widget(picture)
        # for card in my_deck.deck_list:
            # try:
                # load the image
                # picture = Cardimg(source=card.image)
                # add to the main field
                # root.add_widget(picture)
            # except Exception, e:
                # Logger.exception('Pictures: Unable to load <%s>' % filename)

    def on_pause(self):
        return True

my_deck = Deck(make_cards())
my_deck.shuffle()
if __name__ == '__main__':
    JadnoApp().run()

