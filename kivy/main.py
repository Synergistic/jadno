from random import randint
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter

from kivy.properties import StringProperty, ListProperty
from kivy.config import Config

from uno import *


Config.set( 'graphics', 'width', '1024' )
Config.set( 'graphics', 'height', '768' )
FIRST = True
player_hand = None
my_deck = None
class CardImage(Scatter):
    src_img = StringProperty(None)
    identity = StringProperty(None)

    def on_touch_down(self, touch):
        x, y = touch.x, touch.y

        # if the touch isnt on the widget we do nothing
        if not self.collide_point(x, y):
            return False
			
        touch.push()
        touch.apply_transform_2d(self.to_local)
        touch.pop()
        print 'touched', self.identity
        # if we don't have any active controls, then don't accept the touch
        if not self.do_translation_x and \
            not self.do_translation_y and \
            not self.do_rotation and \
            not self.do_scale:
            return False

        # grab the touch to track later events
        self._bring_to_front()
        touch.grab(self)
        self._touches.append(touch)
        self._last_touch_pos[touch] = touch.pos

        return True

class GameArea(FloatLayout):
    pass
	
class HUD(BoxLayout):
    card_draw_list = []
	
    def start_deal(self):
        
        for i in range(7):
            player_hand.add_card( my_deck.deal_card() )
			
        for card in player_hand.card_list:
            i = CardImage(src_img = card.image,
                        identity = str(card),
                        size = (200, 300),
                        size_hint = (None, None)
                        )
            i.top = 300
            self.card_draw_list.append(i)
             

    def start_game(self):
        global my_deck, player_hand, FIRST
        if not FIRST:
            jadno.clear_gamearea()
        my_deck = Deck(make_cards())
        my_deck.shuffle()

        player_hand = Hand()
        self.start_deal()
        FIRST = False

		
		
#The main window that contains everything
class JadnoApp(App):

    def build(self):
        self.root = GameArea()
        self.h = HUD()
        self.root.add_widget(self.h)
        Clock.schedule_interval(self.update, 1.0 / 10.0)
        return self.root
		
    def update(self, dt):
        for card in self.h.card_draw_list:
            self.root.add_widget(card)
        self.h.card_draw_list = []

    def clear_gamearea(self):
        self.root.clear_widgets()
        self.root.add_widget(self.h)
#Start game loop
jadno = JadnoApp()
if __name__ == '__main__':
    jadno.run()

