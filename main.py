from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.core.window import Window

from random import randint, choice
from uno import *

Window.size = (1280, 720)

playing = False
last_touch = False

class CardImage(Scatter):
	moving = BooleanProperty(True)
	src_img = StringProperty(None)
	card_obj = ObjectProperty(None)
	
	def on_touch_down(self, touch):
		global last_touch
		x, y = touch.x, touch.y

		# if the touch isnt on the widget we do nothing
		if not self.collide_point(x, y):
			return False
			
		touch.push()
		touch.apply_transform_2d(self.to_local)
		touch.pop()
		print 'touched', str(self.card_obj)
		last_touch = self.card_obj
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
	card_draw_list = []
	card_remove_list = []
	active_card_wids = []
	discard_wid = None
	
	def start_deal(self):
		'''shuffles, deals seven cards, puts a card on the discard pile,
		and makes widgets for everything'''
		
		my_deck.shuffle()
		x = 1 
		for i in range(7):
			c = my_deck.deal_card()
			player.add_card(c)
			self.make_card_wid(c, (100 * x, 25))
			x += 1
			
		d =  my_deck.deal_card()
		if d.rank in ['w', 'wd4']: #if discard starts with wild
			d.color = choice(COLORS) #we need to give it a random color
		discard_pile.add_card(d)
		self.make_card_wid(d, (450, 400), move=False)

	def start_game(self):
		'''Initialize deck, discard pile, player hand objects
		and deal cards, flip the playing variable'''
		
		global my_deck, player, discard_pile, playing
		if playing: #if a game already is happening
			jadno.clear_gamearea() #clear the board

		my_deck = Deck(make_cards())
		discard_pile = Discard()
		player = Hand()
		self.start_deal()
		last_touch = False
		playing = True

	def make_card_wid(self, card, loc, move=True):
		'''Takes a card object and makes it into a CardImage widget.
		The new widget is added to an appropriate list for drawing/tracking.
		Discard pile will have move=False.'''
		
		i = CardImage(src_img = card.image,
				pos = loc,
				moving = move,
				card_obj = card)
		self.card_draw_list.append(i)
		self.active_card_wids.append(i)
		if not move: #store the discard separately for easy identification
			self.discard_wid = i
	
	def add_a_card(self):
		'''Draws a card from the deck to the player's hand'''
		
		if len(my_deck.deck_list) > 0:
			c = my_deck.deal_card()
			player.add_card(c)
			self.make_card_wid(c, (100, 25))
		else:
			print "Deck is empty bro"

	def remove_a_card(self):
		'''Method to remove a card object and it's corresponding widget.'''
		
		#make sure user has touched a card
		if not last_touch:
			print "No recently touched cards"
			
		#make sure the last card touched isn't the discard pile
		elif last_touch == self.discard_wid.card_obj:
			print "cannot remove discard pile"
			
		#make sure the player has cards to discard	
		elif len(player.hand_list) <= 0:
			print "You Win"	
		
		#check if it's a legal move based on game rules
		elif is_valid_move(last_touch, self.discard_wid.card_obj):
			d = player.discard_card(last_touch)
			self.active_card_wids.remove(self.discard_wid) #current discard widget no longer needed
			self.card_remove_list.append(self.discard_wid) #to be deleted from parent widget
			
			for card in self.active_card_wids:
				if card.card_obj == d: #remove the played card from the active widgets and parent
					self.active_card_wids.remove(card)
					self.card_remove_list.append(card)

		else:
			print "Not a valid move"
			
	def update_discard(self, new_card):
		'''Method to create a new widget for the discard pile after a player
		discards a card. Asks user about desired color of the played card is
		a wild'''

		#Need to know user's desired new color when playing wild
		if str(new_card) in ['w', 'wd4']:
			c = BoxLayout(orientation = 'vertical')
			c.add_widget(Label(text="Select your new color:"))
			s = Spinner(values=['r', 'g', 'b', 'y'])
			c.add_widget(s)
			b = Button(text='Okay')
			c.add_widget(b)
			p = Popup(title="Enter color", size_hint=(0.25, 0.4), content=c, auto_dismiss=False)
			
			def close_pop(b):
				if s.text in ['r', 'g', 'b', 'y']:
					p.dismiss()
					new_card.color = s.text
			b.bind(on_release = close_pop)
			p.open()
		
		#replace the old discard pile widget with a new one
		self.make_card_wid(new_card, (450, 400), move=False)
	
class HUD(BoxLayout):
	'''This is what contains all the widgets for the interface'''
	
	def add_a_card(self):
	  jadno.root.add_a_card()
	
	def remove_a_card(self):
	  jadno.root.remove_a_card()
	
	def start_game(self):
	  jadno.root.start_game()
	
#The main window that contains everything
class JadnoApp(App):

	def build(self):
		'''Builds a float layout as the base with holds the interface that
		contains buttons and cards. Handles adding/removing new widgets'''
		
		self.root = GameArea()
		self.h = HUD()
		self.root.add_widget(self.h)
		Clock.schedule_interval(self.update, 1.0 / 30.0)
		return self.root
		
	def update(self, dt):
		'''Handles the adding/removing widgets'''
		if playing:
			self.adding_cards()
			self.removing_cards()
		
	def adding_cards(self):
		for card in self.root.card_draw_list:
			self.root.add_widget(card)
		self.root.card_draw_list = []
			
	def removing_cards(self):
		for card in self.root.card_remove_list:
			self.root.remove_widget(card)
			#add that card to the discard pile
			if card != self.root.discard_wid: 
				self.root.update_discard(card.card_obj)	
		self.root.card_remove_list = []
		
	def clear_gamearea(self):
		self.root.clear_widgets()
		self.root.add_widget(self.h)


	
#Start game loop
jadno = JadnoApp()
if __name__ == '__main__':

    jadno.run()

