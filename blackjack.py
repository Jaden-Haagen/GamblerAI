import random

class Deck:
    def __init__(self, numDecks = 1):
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
        deck = [{"card": v + s, "value": values[v]} for _ in range(numDecks) for s in suits for v in values]
        return deck

    #Shuffles the shoe/deck of cards for game
    def shuffle_deck(self):
        random.shuffle(self.cards)
    
    #remove a card from the shoe 
    def deal(self):
        return self.cards.pop()

class Hand:
    def __init__(self, bet=1):
        self.cards = [] #Player hand
        self.bet = bet #Player bet amount
        self.active = True #Player hasn't busted/stood

    def get_value(self):
        value = sum(card["value"] for card in self.cards)
        #Find aces in hand
        aces = sum(1 for card in self.cards if card["card"][:-1] == "A")
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
        self.players = [{"hand": Hand(), "money": startingMoney, "stood": 0} for _ in range(numPlayers+1)]
        #self.dealer = [{"hand": Hand(), "stood": 0}]

    def deal_cards(self):
        #Deal 2 cards to each player and the dealer
        for _ in range(2):
            for player in self.players:
                player["hand"].add_card(self.deck.deal())
            #self.dealer[0]["hand"].add_card(self.deck.deal())

    #all action codes
    STAND = 0
    HIT = 1
    DOUBLE = 2
    SPLIT = 3
    def moves(self, player, action):
        match action:
            case self.STAND:
                self.players[player]["stood"] = 1
            case self.HIT:
                self.players[player]["hand"].add_card(self.deck.deal())
            case self.DOUBLE:
                if self.players[player]["money"] >= self.players[player]["hand"].bet:
                    self.players[player]["hand"].double(self.deck)
                    self.players[player]["stood"] = 1
            case self.SPLIT:
                pass
            case _:
                raise ValueError("Invalid action")