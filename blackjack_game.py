''' Game of Black Jack

Instructions/gameplay:
1. Create a deck of 52 cards
2. Shuffle the deck
3. Ask the player for their bet
4. Make sure that the player's bet does not exceed their available chips
5. Deal two cards to the Dealer and two cards to the player
6. Show only one of the dealers cards, the other remains hidden
7. Show both of the Player's cards
8. Ask the player's hand doesnt Bust (go over 21), ask if they'd like to Hit again.
9. If the player stands, play the dealers hand. The dealer will always hit until Dealers value meets or exceeds 17
10. Determine the winner and adjust the player's chips aaccordingly
11. Ask the Player if they'd like to play again. 
''' 

''' Step 1: Imort the random module. This will be used to shuffle the deck prior to dealing. Then, declare 
variables to store suits, ranks and values. You can develop your own system, or copy ours below. Finally,
declare a boolen value to be used to control while loops. This is a common practice used to control the
flow of the game. ''' 

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True


''' 
Step 2: Class Definitions
- Create a card class
''' 

class Card():
    

    def __init__(self,suit,rank):
        
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)


''' Step 3: Create a deck class:

- Store 52 card objects in a list that can shuffled later. 
- Firstly, instantiate all  52 unique card objects and add them to our list.
-  So long as the Card class definition appears in our code, we can build Card objects inside our Deck __init__ method. Consider iterating over sequences of suits and ranks to build out each card. This might appear inside a Deck class __init__ method:

for suit in suits:
for rank in ranks:

In addition to an __init__ method we'll want to add methods to shuffle our deck, and to deal out cards during gameplay.

OPTIONAL: We may never need to print the contents of the deck during gameplay, but having the ability to see the cards inside it may help troubleshoot any problems that occur during development. With this in mind, consider adding a __str__ method to the class definition. ''' 

class Deck:

	def __init__(self):

		self.deck = [] # start with an empty list
		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(suit,rank))

	def __str__(self):
		deck_comp = ''
		for card in self.deck:
			deck_comp += '\n' + card.__str__()
		return " The deck has: "+ deck_comp

	def shuffle(self):
		# Shuffling the deck
		random.shuffle(self.deck)
	
	def deal(self):
		# Should called to deal card to player.
		deal_card = self.deck.pop()
		return deal_card
		


# Testing: Just to see that everything works so far.
test_deck = Deck()
print(test_deck)
print(test_deck.shuffle())
print(test_deck.deal())
print(test_deck)


''' Step 4: Create a Hand class:
In addition to holding Card objects dealt from the Deck, the hand calss may be used to calculate the value of those cards using the values dictionary defined above. It may also need to adjust for the value of Aces when appropriate. '''

class Hand:

	def __init__(self):

		self.cards = [] # Start with an empty list as we did in the Deck class
		self.value = 0  # Start with zero value
		self.aces = 0   # Add an attribute to keep track of aces

	
	def add_card(self,card):
		# card passed in
		# from deck.deal() ---> dealcard()
		self.cards.append(card)
		self.value += values[card.rank]

		# Track aces
		if card.rank == 'Ace':
			self.aces += 1
		
	def adjust_for_ace(self):
		
		''' If the total > 21 and i still have an ace
		then change ace to be 1 instead of 11 '''
		while self.value > 21 and self.aces:
			self.value -= 10
			self.aces -= 1


test_deck = Deck()
test_deck.shuffle()

# player
test_player = Hand()

# deal card from deck
pulled_card = test_deck.deal()
print(pulled_card)
test_player.add_card(pulled_card)
print(test_player.value)

print(test_player.add_card(test_deck.deal()))
print(test_player.value)


''' Step 5: Create a Chips Class
In addition to decks of cards and hands, we need to keep track of a player's starting chips, bets, and ongoing winnings. This could be done using global variables, but in the spirit of object orientated programming, lets make a chips class instead! '''

class Chips:

	def __init__(self, total= 100):
		self.total = total # This can be set to a default value or supplied by a user input
		self.bet = 0

	def win_bet(self):
		self.total += self.bet

	def lose_bet(self):
		self.total -= self.bet



''' Function Definitions:
A lot of steps are going to be repetitive. That's where functions come in! The following steps are guidelines - add or remove functions as needed in your own programme. '''

''' Step 6: Write a function for taking bets
Since we're asking the user for an integer value, this would be a good place to use a try/except. Remember to check that a player's bet can be covered by their available chips. '''

def take_bet(chips):

	while True:

		try:
			chips.bet = int(input("How many chips would you like to bet? "))
		except ValueError:
			print(" Sorry, a bet must be a number!")
		else:
			if chips.bet > chips.total:
				print("Sorry, you is too broke! current balance: {}".format(chips.total))
			else:
				break


''' Step 7: Write a function for taking hits
Either player can take hits until they bust. This function will be called during gameplay anytime a Player requests a hit, or a Dealer's hand is less than 17. It should take in Deck and Hand objects as arguments, and deal one card off the deck and add it to the Hand. You may want it to check for aces in the event that a player's hand exceeds 21. '''

def hit(deck, hand):

	deal_card= deck.deal()
	hand.add_card(deal_card)
	hand.adjust_for_ace()


''' 
Step 8: Write a function prompting the Player to Hit or Stand
This function should accept the deck and the player's hand as arguments, and assign playing as a global variable.
If the Player Hits, employ the hit() function above. If the Player Stands, set the playing variable to False - this will control the behavior of a while loop later on in our code. '''


def hit_or_stand(deck, hand):
	global playing # to control an upcoming while loop

	while True:
		x = input('Hit or Stand? Enter h or s ')

		if x[0].lower() == 'h':
			hit(deck,hand)

		elif x[0].lower() == 's':
			print("Player stands. Dealer's turn.")
			playing = False

		else:
			print("Sorry, I did not understand, please enter h or s only!")
			continue

		break


''' Step 9: Write functions to display cards
When the game starts, and after each time Player takes a card, the dealer's first card is hidden and all of Player's cards are visible. At the end of the hand all cards are shown, and you may want to show each hand's total value. Write a function for each of these scenarios. ''' 


def show_some(player, dealer):

    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    
def show_all(player, dealer):

    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


''' step 10 Write functions to handle end of game scenarios
Remember to pass player's hand, dealer's hand and chips as needed. '''

def player_busts(player, dealer, chips):
    print("Player busts!")
    chips.lose_bet()
def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()
def dealer_busts(player, dealer, chips):
    print("Dealer busts!")
    chips.win_bet()
def dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips.lose_bet()
def push(player, dealer):
	print("Dealer and player tie! PUSH!")




''' GAME ON '''

while True:
    # Print an opening statement
    print("Welcome To Blackjack!")

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())    

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    try:
        chip_input = int(input("How many chips do you have?: "))
    except ValueError:
     	print("Sorry, input must be a number! please put in chips")
           
    player_chips = Chips(chip_input)


    # Prompt the Player for their bet
    take_bet(player_chips)
   
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
   
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        while dealer_hand.value < 17: #Soft 17 rule - dealer stops hitting at minimum of 17.
        	hit(deck, dealer_hand)
    
        # Show all cards
        show_all(player_hand, dealer_hand)
    
        # Run different winning scenarios
        if dealer_hand.value > 21:
        	dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
        	dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
        	player_wins(player_hand, dealer_hand, player_chips)
        else:
        	push(player_hand, dealer_hand)

    # Inform Player of their chips total
    print('\n player total chips are at {}'.format(player_chips.total))
    
    # Ask to play again
    new_game = input("would you like to play a new game? yes/no: ")

    if new_game[0].lower() == 'y':
    	playing = True
    	continue
    else:
        print("Thank you for playing!")
        break