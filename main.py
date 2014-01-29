from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.properties import StringProperty, BooleanProperty, \
			    ObjectProperty, NumericProperty
from kivy.core.window import Window

from random import randint, choice
from uno import *

Window.size = (1280, 720)

playing = False
last_touch = False
turn_change = 1
second_draw = False

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
		return True

class GameArea(FloatLayout):
	card_draw_list = []
	card_remove_list = []
	active_card_wids = []
	discard_wid = None
	
	def deal(self):
		'''shuffles, deals seven cards, puts a card on the discard pile,
		and makes widgets for everything'''
		
		my_deck.shuffle()
		x = 1 
		for i in range(7):
			c = my_deck.deal_card()
			player.add_card(c)
			self.make_card_wid(c, ((75 * x) - 50, 25))
			enemy.add_card(my_deck.deal_card())
			x += 1
		d =  my_deck.deal_card()
		if d.rank in ['w', 'wd4']: #if discard starts with wild
			d.color = choice(COLORS) #we need to give it a random color
		discard_pile.add_card(d)
		self.make_card_wid(d, (565, 400), move=False)

	def start_game(self):
		'''Initialize deck, discard pile, player hand objects
		and deal cards, flip the playing variable'''
		
		global my_deck, player, enemy, discard_pile, playing, last_touch, second_draw
		if playing: #if a game already is happening
			jadno.clear_gamearea() #clear the board
		self.active_card_wids = []

		my_deck = Deck(make_cards())
		discard_pile = Discard()
		player = Hand()
		enemy = Hand()
		self.deal()
		last_touch = False
		playing = True
		second_draw = False

	def make_card_wid(self, card, loc, move=True):
		'''Takes a card object and makes it into a CardImage widget.
		The new widget is added to an appropriate list for drawing/tracking.
		Discard pile will have move=False.'''
		
		i = CardImage(src_img = card.image,
				pos = loc,
				moving = move,
				card_obj = card)
		self.card_draw_list.append(i)
		if move:
			self.active_card_wids.append(i)
		if not move: #store the discard separately for easy identification
			self.discard_wid = i
	
	def add_a_card(self):
		'''Draws a card from the deck to the player's hand'''
		
		if len(my_deck.deck_list) > 0: 
			c = my_deck.deal_card()
			player.add_card(c)
			self.make_card_wid(c, (0, 0) )
			x = 1
			for card in self.active_card_wids: #This doesn't change the order, so cards can overlap, fix?
				if card != self.discard_wid:
					card.x = ((75 * x) - 50)
					card.y = 25
					x += 1
			
		else:
			print "Deck is empty bro"

	def remove_a_card(self):
		'''Method to remove a card object and it's corresponding widget.'''
		#make sure user has touched a card
		if not last_touch:
			jadno.h.message = "No recently touched cards"
			
		#make sure the last card touched isn't the discard pile
		elif last_touch == self.discard_wid.card_obj:
			jadno.h.message = "cannot remove discard pile"
			
		#make sure the player has cards to discard	
		if len(player.hand_list) == 0:
			jadno.h.message = 'No cards, start a new game!'
		
		#check if it's a legal move based on game rules
		elif is_valid_move(last_touch, self.discard_wid.card_obj):
			
			d = player.discard_card(last_touch) #discard the last touched card
			if d != None:
				for card in self.active_card_wids:
					if card.card_obj == d: #remove the played card from players hand
						self.active_card_wids.remove(card)
						self.card_remove_list.append(card)
				self.update_discard(d)
				if len(player.hand_list) == 0:
					jadno.h.message = 'You won!'
				else:
					jadno.h.message = 'Player just played a card.'
		else:
			jadno.h.message = "Not a valid move"
			
	def update_discard(self, new_card):
		'''Method to create a new widget for the discard pile after a player
		discards a card. Asks user about desired color of the played card is
		a wild'''
		

		#Need to know user's desired new color when playing wild
		if new_card.rank in ['w', 'wd4'] and jadno.h.turns % 2 == 0:
			#build a popup to ask which color to change to
			c = BoxLayout(orientation = 'vertical')
			c.add_widget(Label(text="Select your new color:"))
			s = Spinner(values=['r', 'g', 'b', 'y'])
			c.add_widget(s)
			b = Button(text='Okay')
			c.add_widget(b)
			p = Popup(title="Pick color", size_hint=(0.25, 0.4), content=c, auto_dismiss=False)
			
			def close_pop(b):
				if s.text in ['r', 'g', 'b', 'y']:
					p.dismiss()
					new_card.color = s.text
					self.game_rules(new_card)
					
			b.bind(on_release = close_pop)
			p.open()
			
		else:
			self.game_rules(new_card)

	def game_rules(self, new_card):
		global turn_change, second_draw	
			
		if new_card.rank == 's':
			jadno.h.turns += 2 * turn_change
		elif new_card.rank == 'r':
			turn_change *= -1
			
		elif new_card.rank == 'd2':
			jadno.h.turns += 2 * turn_change
			if jadno.h.turns % 2 == 0:
				for i in xrange(2):
					enemy.add_card(my_deck.deal_card())
			else:
				for i in xrange(2):
					self.add_a_card()			  
				
		elif new_card.rank == 'wd4':
			jadno.h.turns += 2 * turn_change
			if jadno.h.turns % 2 == 0:
				for i in xrange(4):
					enemy.add_card(my_deck.deal_card())
			else:
				for i in xrange(4):
					self.add_a_card()
		else:
			jadno.h.turns += turn_change
			
		second_draw = False
		jadno.root.remove_widget(self.discard_wid)
		discard_pile.add_card(new_card)
		self.make_card_wid(new_card, (565, 400), move=False)
		jadno.h.top_card = str(new_card)
		
class HUD(BoxLayout):
	'''This is what contains all the widgets for the interface'''
	turns = NumericProperty(100)
	message = StringProperty('Press New Game to begin.')
	top_card = StringProperty('')
	whose_turn = ['Player\'s', 'Computer\'s']
	
	def add_a_card(self):
	  global second_draw
	  if playing and jadno.h.turns % 2 == 0:
		if not second_draw:
			jadno.root.add_a_card()
			second_draw = not second_draw
		else:
		  jadno.h.turns += turn_change
		  jadno.h.message = 'You drew a card and still had no moves, lose a turn.'
		  second_draw = not second_draw
	
	def remove_a_card(self):
	  if playing and jadno.h.turns % 2 == 0:
		jadno.root.remove_a_card()

	def start_game(self):
	  jadno.root.start_game()
	  self.turns = 100
	  
class JadnoApp(App):

	def build(self):
		'''Builds a float layout as the base with holds the interface that
		contains buttons and cards. Handles adding/removing new widgets'''
		
		self.root = GameArea()
		self.h = HUD()
		self.root.add_widget(self.h)
		Clock.schedule_interval(self.update, 1.0 / 10.0)	
		return self.root
		
	def update(self, dt):
		'''Method called using the Clock for updating the card widgets.'''
		if playing:
			self.adding_cards()
			self.removing_cards()
			if self.h.turns % 2 == 1:
				Clock.schedule_once(jadno.computer_move, 4)

	def adding_cards(self):
		for card in self.root.card_draw_list:
			self.root.add_widget(card)
		self.root.card_draw_list = []
			
	def removing_cards(self):
		for card in self.root.card_remove_list:
			self.root.remove_widget(card)
		self.root.card_remove_list = []
		
	def clear_gamearea(self):
		self.root.clear_widgets()
		self.root.add_widget(self.h)

	def computer_move(self, dt):
		if playing and self.h.turns % 2 == 1: #cpu turn
			for card in enemy.hand_list:
				if is_valid_move(card, discard_pile.discard_list[-1]):
					if card.rank in ['w', 'wd4']:
						card.color = choice(COLORS)
					discard_pile.add_card(enemy.discard_card(card))
					self.root.update_discard(card)
					jadno.h.message = 'Computer played a card.'
					return None
					
			c = my_deck.deal_card()
			enemy.add_card(c)
	
			if is_valid_move(c, discard_pile.discard_list[-1]):
				if c.rank in ['w', 'wd4']:
					c.color = choice(COLORS)
				discard_pile.add_card(enemy.discard_card(c))
				self.root.update_discard(c)
				jadno.h.message = 'Computer played a card.'
				return None
			else:
				self.h.message = 'Computer drew a card and lost the turn.'
				self.h.turns += turn_change
					
#Start game loop
jadno = JadnoApp()
if __name__ == '__main__':

    jadno.run()

