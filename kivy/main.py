from random import randint
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter

from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.config import Config

from uno import *


Config.set( 'graphics', 'width', '1024' )
Config.set( 'graphics', 'height', '768' )
player = None
my_deck = None
discard_pile = None
playing = False
last = False

class CardImage(Scatter):
	moving = BooleanProperty(True)
	src_img = StringProperty(None)
	card_obj = ObjectProperty(None)
	
	def on_touch_down(self, touch):
		global last
		x, y = touch.x, touch.y

		# if the touch isnt on the widget we do nothing
		if not self.collide_point(x, y):
			return False
			
		touch.push()
		touch.apply_transform_2d(self.to_local)
		touch.pop()
		print 'touched', str(self.card_obj)
		last = self.card_obj
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
		if self.collide_point(450, 400):
			print "yes"
			
		return True

class GameArea(FloatLayout):
    pass
	
class HUD(BoxLayout):
	card_draw_list = []
	card_remove_list = []
	active_card_wids = []
	discard_wid = None
	
	def start_deal(self):
		my_deck.shuffle()
		x = 1 
		for i in range(7):
			c = my_deck.deal_card()
			player.add_card(c)
			self.make_card_wid(c, (100 * x, 25))
			x += 1
			
		d =  my_deck.deal_card()
		discard_pile.add_card(d)
		self.make_card_wid(d, (450, 400), move=False)

	def start_game(self):
		global my_deck, player, discard_pile, playing
		if playing:
			jadno.clear_gamearea()

		my_deck = Deck(make_cards())
		discard_pile = Discard()
		player = Hand()
		self.start_deal()
		
		last = False
		playing = True


	def make_card_wid(self, card, loc, move=True):
		i = CardImage(src_img = card.image,
				size = (150, 225),
				size_hint = (None, None),
				pos = loc,
				moving = move,
				card_obj = card)
		self.card_draw_list.append(i)
		self.active_card_wids.append(i)
		if not move:
			self.discard_wid = i
	
	def add_a_card(self):
		if len(my_deck.deck_list) > 0:
			c = my_deck.deal_card()
			player.add_card(c)
			self.make_card_wid(c, (100, 25))
		else:
			print "Deck is empty bro"

	def remove_a_card(self):
		if not last:
			print "No recently touched cards"
			return 0
			
		elif last == self.discard_wid.card_obj:
			print "cannot remove discard pile"
			return 0
			
		elif len(player.hand_list) > 0:
			d = player.discard_card(last)
			self.active_card_wids.remove(self.discard_wid)
			self.card_remove_list.append(self.discard_wid)
			
			for card in self.active_card_wids:
				if card.card_obj == d: #remove the card from the active widgets
					self.active_card_wids.remove(card)
					self.card_remove_list.append(card)
		else:
			print "No cards in your hand"
				
	def update_discard(self, new_card):
		self.make_card_wid(new_card, (450, 400), move=False)
		
#The main window that contains everything
class JadnoApp(App):

	def build(self):
		self.root = GameArea()
		self.h = HUD()
		self.root.add_widget(self.h)
		Clock.schedule_interval(self.update, 1.0 / 30.0)
		return self.root
		
	def update(self, dt):
		if playing:
			self.adding_cards()
			self.removing_cards()
		
	def adding_cards(self):
		for card in self.h.card_draw_list:
			self.root.add_widget(card)
		self.h.card_draw_list = []
			
	def removing_cards(self):
		for card in self.h.card_remove_list:
			self.root.remove_widget(card)
			if card != self.h.discard_wid:
				self.h.update_discard(card.card_obj)	
		self.h.card_remove_list = []
		
	def clear_gamearea(self):
		self.root.clear_widgets()
		self.root.add_widget(self.h)
		
#Start game loop
jadno = JadnoApp()
if __name__ == '__main__':
    jadno.run()

