'''
Strategy for hands in blackjack
3 tables with actions that are best given all available information the player has
'''
from blackjack import BlackjackGame, Hand
import csv
from tqdm import trange # type: ignore #for progress bar
# basic_strategy(game.hands[0], game.hands[dealerID]) #call until a stand is best


def basic_strategy(player_hand, player_hand_size, dealer_hand):
    # stand = 0, hit = 1, double = 2
    # Dealer upcard:2,3,4,5,6,7,8,9,T,A
    HARD_TOTALS = [[1,1,1,1,1,1,1,1,1,1], # 8-
                   [1,2,2,2,2,1,1,1,1,1], # 9
                   [2,2,2,2,2,2,2,2,1,1], # 10
                   [2,2,2,2,2,2,2,2,2,2], # 11
                   [1,1,0,0,0,1,1,1,1,1], # 12
                   [0,0,0,0,0,1,1,1,1,1], # 13
                   [0,0,0,0,0,1,1,1,1,1], # 14
                   [0,0,0,0,0,1,1,1,1,1], # 15
                   [0,0,0,0,0,1,1,1,1,1], # 16
                   [0,0,0,0,0,0,0,0,0,0]] # 17+
    # Dealer upcard:2,3,4,5,6,7,8,9,T,A
    SOFT_TOTALS = [[1,1,1,2,2,1,1,1,1,1], # A,2
                   [1,1,1,2,2,1,1,1,1,1], # A,3
                   [1,1,2,2,2,1,1,1,1,1], # A,4
                   [1,1,2,2,2,1,1,1,1,1], # A,5
                   [1,2,2,2,2,1,1,1,1,1], # A,6
                   [2,2,2,2,2,0,0,1,1,1], # A,7
                   [0,0,0,0,2,0,0,0,0,0], # A,8
                   [0,0,0,0,0,0,0,0,0,0]] # A,9
    # split = 1, keep = 0
    # Dealer upcard:2,3,4,5,6,7,8,9,T,A
    PAIR_SPLITS = [[1,1,1,1,1,0,0,0,0,0], # 2,2
                   [1,1,1,1,1,0,0,0,0,0], # 3,3
                   [0,0,0,1,1,0,0,0,0,0], # 4,4
                   [0,0,0,0,0,0,0,0,0,0], # 5,5
                   [1,1,1,1,1,0,0,0,0,0], # 6,6
                   [1,1,1,1,1,1,0,0,0,0], # 7,7
                   [1,1,1,1,1,1,1,1,1,1], # 8,8
                   [1,1,1,1,1,0,1,1,0,0], # 9,9
                   [0,0,0,0,0,0,0,0,0,0], # 10,10
                   [1,1,1,1,1,1,1,1,1,1]] # A,A
    
    
    player_hand_val = player_hand.get_value()
    dealer_hand_val = dealer_hand.get_value() # for determining dealer actions (not seen by player)
    dealer_upcard = dealer_hand.cards[0]["value"]
    #get the column needed for the strategy tables
    match dealer_upcard:
        case 2:
            upcard_index = 0
        case 3:
            upcard_index = 1
        case 4:
            upcard_index = 2
        case 5:
            upcard_index = 3
        case 6:
            upcard_index = 4
        case 7:
            upcard_index = 5
        case 8:
            upcard_index = 6
        case 9:
            upcard_index = 7
        case 10:
            upcard_index = 8
        case 11:
            upcard_index = 9
    row_index = -1
    #check for pair split first
    if player_hand_size == 2 and player_hand.cards[0]["value"] == player_hand.cards[1]["value"]:
        pair_value = player_hand.cards[0]["value"]
        match pair_value:
            case 2:
                row_index = 0
            case 3:
                row_index = 1
            case 4:
                row_index = 2
            case 5:
                row_index = 3
            case 6:
                row_index = 4
            case 7:
                row_index = 5
            case 8:
                row_index = 6
            case 9:
                row_index = 7
            case 10:
                row_index = 8
            case 11:
                row_index = 9
        split = PAIR_SPLITS[row_index][upcard_index]
        if split == 1:
            return 3 #split action
    #check for soft hand
    if player_hand_size == 2 and (player_hand.cards[0]["value"] == 11 or player_hand.cards[1]["value"] == 11):
        soft_total = player_hand_val
        match soft_total:
            case 13:
                row_index = 0
            case 14:
                row_index = 1
            case 15:
                row_index = 2
            case 16:
                row_index = 3
            case 17:
                row_index = 4
            case 18:
                row_index = 5
            case 19:
                row_index = 6
            case 20:
                row_index = 7
        action = SOFT_TOTALS[row_index][upcard_index]
    else:
        #hard hand
        hard_total = player_hand_val
        match hard_total:
            case _ if hard_total <= 8:
                row_index = 0
            case 9:
                row_index = 1
            case 10:
                row_index = 2
            case 11:
                row_index = 3
            case 12:
                row_index = 4
            case 13:
                row_index = 5
            case 14:
                row_index = 6
            case 15:
                row_index = 7
            case 16:
                row_index = 8
            case _ if hard_total >= 17:
                row_index = 9
        action = HARD_TOTALS[row_index][upcard_index]
    return action

#test running a game?
resultsFile = "BS_results.csv"
num_rounds = 1000000
numDecks = 1
numPlayers = 1
game_data = []

game = BlackjackGame(numDecks, numPlayers)
dealerID = numPlayers

for round in trange(num_rounds, desc="Basic Strategy Simulation"):
    #check deck size and add cards if needed
    game.deck.reshuffle(numDecks)
    #initialize hands
    bet = 1
    game.hands[0].bet = bet
    #deal table
    game.deal_cards()
    #player plays
    BS_moves = []
    #loop through each player hand
    playerHands = game.players[0]["hands"]
    playerStand = game.players[0]["stood"]
    i = 0
    done = False
    while i < len(playerHands):
        #get the handID from player hands
        handID = playerHands[i]
        stoodID = playerStand[i]
        while not done:
            action = basic_strategy(game.hands[handID], len(game.hands[handID].cards), game.hands[dealerID])
            game.moves(0, handID, stoodID, action)
            BS_moves.append(action)
            if action == 0:
                done = True
            else:
                done = False
        i += 1
    #dealer plays
    while game.hands[dealerID].get_value() < 17:
        game.dealer_play(dealerID, dealerID)
    #determine results
    rewards = []
    for i in game.players[0]["hands"]:
        player_cards_val = game.hands[i].get_value()
        dealer_cards_val = game.hands[dealerID].get_value()
        if player_cards_val > 21:
            rewards.append(-1)
        elif dealer_cards_val > 21:
            rewards.append(1)
        elif player_cards_val > dealer_cards_val:
            rewards.append(1)
        elif player_cards_val < dealer_cards_val:
            rewards.append(-1)
        else:
            rewards.append(0)
    
    #add round_data to game_data
    for j, i in enumerate(game.players[0]["hands"]):
        round_data = {
            "round": int(round),
            "player_hand": [card["value"] for card in game.hands[i].cards], 
            "dealer_hand": [card["value"] for card in game.hands[dealerID].cards],
            "actions": [move for move in BS_moves], 
            "result": rewards[j]
        }
        game_data.append(round_data)
    
    #reset the player hands trackers
    for i, player in enumerate(game.players):
        player["hands"] = [i]
        player["stood"] = [0]
    #clear the table
    for hand in game.hands:
        hand.clear()
    #clear the table completely and reset to just two hands
    game.hands = [Hand() for _ in range(numPlayers+1)]

    #save game results (stored in csv)
with open(resultsFile, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["round", "player_hand", "dealer_hand", "actions", "result"])
    writer.writeheader()

    for round_info in game_data:
        writer.writerow({
            "round": str(round_info["round"]),
            "player_hand": ','.join(map(str, round_info["player_hand"])),
            "dealer_hand": ','.join(map(str, round_info["dealer_hand"])),
            "actions": ','.join(map(str, round_info["actions"])),
            "result": str(round_info["result"])
        })