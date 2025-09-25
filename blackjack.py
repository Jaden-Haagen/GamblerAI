import random

class Deck:
    def __init__(self, numDecks = 2):
        self.cards = self.generate_deck(numDecks)
        self.shuffle_deck()

    #Generate a shoe with x number of decks 
    def generate_deck(self, numDecks = 1):
        #H = Hearts, D = Diamonds, C = Clubs, S = Spades
        suits = ["H", "D", "C", "S"]
        #dictionary for card values (Ace is stored as 11 until bust(reevaluated as a 1))
        values = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
            "J": 10, "Q": 10, "K": 10, "A": 11
        }
        #Generate all cards needed for the desired number of decks
        deck = [{"card": v, "suit": s, "value": values[v]} for _ in range(numDecks) for s in suits for v in values]
        return deck

    #Shuffles the shoe/deck of cards for game
    def shuffle_deck(self):
        random.shuffle(self.cards)
    
    #remove a card from the shoe 
    def deal(self):
        return self.cards.pop()
    
    def reshuffle(self, numDecks):
        threshold = (numDecks * 52) * 0.25 #adds cards to shoe when cards get below 25%
        if len(self.cards) < threshold:
            self.cards = self.generate_deck(numDecks)
            self.shuffle_deck()

class Hand:
    def __init__(self, bet=1):
        self.cards = [] #Player hand
        self.bet = bet #Player bet amount
        self.active = True #Player hasn't busted/stood

    def get_value(self):
        value = sum(card["value"] for card in self.cards)
        #Find aces in hand
        aces = sum(1 for card in self.cards if card["card"] == "A")
        #If aces cause bust then make them worth 1 point instead of 11
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value
    
    #End turn
    def stand(self):
        self.active = False

    #Add card to hand
    def add_card(self, card):
        self.cards.append(card)
    
    #Add card to hand (after initial deal)
    def hit(self, deck):
        self.add_card(deck.deal())#add card that was removed from shoe
    
    #Double bet, hit, and end turn
    def double(self, deck):
        self.bet *= 2
        self.hit(deck)
        self.stand()
    
    #might change this
    def split(self):
        pass

    #Clear hand for a new round
    def clear(self):
        self.cards = []
        self.bet = 0
        self.active = True

class BlackjackGame:
    def __init__(self, numDecks, numPlayers, startingMoney = 1000):
        self.deck = Deck(numDecks)
        #self.players = [{"hand": Hand(), "money": startingMoney, "stood": 0} for _ in range(numPlayers+1)]
        self.players = [{"hands": [i], "money": startingMoney, "stood": [0]} for i in range(numPlayers+1)] #hands holds hand IDs  
        self.hands = [Hand() for _ in range(numPlayers+1)] #List of all hands on the table (accessed with player hand IDs)
        #self.dealer = [{"hand": Hand(), "stood": 0}]

    def deal_cards(self):
        #Deal 2 cards to each player hand and the dealer
        for _ in range(2):
            '''for player in self.players:
                player["hand"].add_card(self.deck.deal())'''
            for hand in self.hands:
                hand.add_card(self.deck.deal())
            #self.dealer[0]["hand"].add_card(self.deck.deal())

    #all action codes
    STAND = 0
    HIT = 1
    DOUBLE = 2
    SPLIT = 3
    #returns true or false if move was valid and executed
    def moves(self, player, handID, stoodID, action):#pass hand ID as well
        match action:
            case self.STAND:
                self.players[player]["stood"][stoodID] = 1
                return True
            case self.HIT:
                #self.players[player]["hand"].add_card(self.deck.deal())
                self.hands[handID].add_card(self.deck.deal())
                return True
            case self.DOUBLE:
                #if self.players[player]["money"] >= self.players[player]["hand"].bet:
                if self.players[player]["money"] >= self.hands[handID].bet:
                    #self.players[player]["hand"].double(self.deck)
                    self.hands[handID].double(self.deck)
                    #self.players[player]["stood"] = 1
                    self.players[player]["stood"][stoodID] = 1
                    return True
                else:
                    return False
            case self.SPLIT:
                #must have at least the amount of money for new bet and two cards with same number
                #if self.players[player]["money"] >= self.players[player]["hand"].bet and self.players[player]["hand"].cards[0]["value"] == self.players[player]["hand"].cards[1]["value"]:
                if self.players[player]["money"] >= self.hands[handID].bet and self.hands[handID].cards[0]["value"] == self.hands[handID].cards[1]["value"]:
                    #create 2 hands for the player (requries rewrite of the hand in players)
                    #remove card to create new hand
                    moveCard = self.hands[handID].cards.pop()
                    #create new hand 
                    self.hands.append(Hand([moveCard])) #new hand with the second card from original hand
                    self.players[player]["hands"].append(len(self.hands)-1) #add hand ID to list of player hands
                    #deal cards to hands
                    self.hands[handID].add_card(self.deck.deal())
                    self.hands[len(self.hands)-1].add_card(self.deck.deal())
                    #update stood list
                    self.players[player]["stood"].append(0)
                    #play hands
                    return True
                else:
                    return False
            case _:
                raise ValueError("Invalid action")
            
    def dealer_play(self, dealerID, handID):
        while self.hands[handID].get_value() < 17:
            self.moves(dealerID, handID, 0, 1)