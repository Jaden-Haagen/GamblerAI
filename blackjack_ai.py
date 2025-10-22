from blackjack import BlackjackGame, Hand

import math
import tensorflow as tf
import numpy as np
import csv
import os
from tqdm import trange #for progress bar


#function for AI model 
def initialize_model(state_size, num_actions, learning_rate, filename):
    #try using an existing model if filename is an existing file
    if os.path.exists(filename):
        model = tf.keras.models.load_model(filename, compile = False)
        print("Loaded existing model")
    #create new model if file not found
    else:
        #create a model
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(state_size,)),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(num_actions, activation='linear')
        ])
        print("Created a new model")

    #compile model to train
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate),loss='mse')
    return model

#function to update model (q_values, target, etc)
def update_model(model, state, next_state, action, reward, gamma, done):
    q_values = model.predict(state.reshape(1, -1), verbose = 0)
    if done:
        target = reward
    else:
        next_q_values = model.predict(next_state.reshape(1, -1), verbose = 0)
        target = reward + gamma * np.max(next_q_values[0])
    q_values[0][action] = target
    model.fit(state.reshape(1, -1), q_values, verbose = 0)

#Update these parts to change models, training, storage location, etc.
#File names for model, new model, and game results
filename = "model_v2_7.keras"
filesavename = "model_v2_8.keras"
resultsFile = "v2_8_results.csv"

#environment size
state_size = 3 #what the ai needs to analyze (dealer card, player's cards, bet)
num_actions = 4 #what the AI can do (hit, stand, double, split) add bet later
learning_rate = 0.001 # small number = slow but stable, big number = fast but overshoots frequently

num_rounds = 10000 #test size (change to 1000+ after everything works)
gamma = 0.95 #discount factor (0 = cares about current reward, 1 = cares about future reward)
epsilon = 0.1 #exploration rate (0 = no exploration only follow model, 1 = always explores new options)
#updated for epsilon update at each round (ubove is just a back up value)
epsilon_start = 0.5 #change if using a pretrained model
epsilon_min = 0.01
k = 0.001  # decay speed
rounds_trained = num_rounds * 10 #to keep epsilon consistent between training sessions


numDecks = 1
numPlayers = 1
game_data = []

"""
#compile model for training/running
learning_rate = 0.001 # small number = slow but stable, big number = fast but overshoots frequently
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate),loss='mse')
"""
#initialize model
model = initialize_model(state_size, num_actions, learning_rate, filename)

#Begin game
game = BlackjackGame(numDecks, numPlayers)
dealerID = numPlayers #dealerID is always the last position in the initial list (doubles as dealer hand ID)
#Allow agent to play rounds
for round in trange(num_rounds, desc = "AI Training Progress"):
    #update epsilon for model training
    epsilon = epsilon_min + (epsilon_start - epsilon_min) * math.exp(-k * (round + rounds_trained))
    
    #check deck size and add cards if needed
    game.deck.reshuffle(numDecks)
    #start with bet (AI bet will bet 1 until model can play reliably)
    bet = 1
    game.hands[0].bet = bet
    #deal table
    game.deal_cards()
    
    #get known values for AI to make a decision
    player_cards_val = game.hands[0].get_value()
    dealer_card_val = game.hands[dealerID].cards[0]["value"]#return value of first card in dealer hand

    state = np.array([player_cards_val, dealer_card_val, bet], dtype=float)#change this for environment(get_player_val, get_dealer_val, etc)
    #variables for tracking if player is finished playing and if dealer is dealt a blackjack (natural)
    done = False
    natural = False
    #check for dealer blackjack (no insurance for current game since betting not considered)
    dealer_cards_val = game.hands[dealerID].get_value()
    if dealer_cards_val == 21:
        #player and dealer are done playing
        done = True
        natural = True
        #check if player push or lose
        if player_cards_val == 21:
            reward = 0
        else:
            reward = -1

        #update the model with the loss or push
        update_model(model, state, state, 0, reward, gamma, done)
    
    AI_moves = []
    #loop through each player hand
    playerHands = game.players[0]["hands"]
    playerStand = game.players[0]["stood"]
    i = 0
    while i < len(playerHands):
        #get the handID from player hands
        handID = playerHands[i]
        stoodID = playerStand[i]
        #loops until AI model chooses to stand or busts
        while not done:
            #list all valid moves for hand
            valid_moves = [0, 1]
            if game.players[0]["money"] >= game.hands[handID].bet and len(game.hands[handID].cards) == 2:
                valid_moves.append(2)
            if game.players[0]["money"] >= game.hands[handID].bet and len(game.hands[handID].cards) == 2 and game.hands[handID].cards[0]["value"] == game.hands[handID].cards[1]["value"]:
                valid_moves.append(3)
            #randomly choose an action to play if exploration condition is met (10% of moves are random)
            if np.random.rand() < epsilon:
                action = np.random.choice(valid_moves)
            else:
                q_values = model.predict(state.reshape(1, -1), verbose = 0)[0]
                # Mask invalid actions (set to very negative so argmax won't pick them)
                masked_q = np.full_like(q_values, -np.inf)
                # Only copy the valid moves
                for a in valid_moves:
                    if a < len(q_values):  # safety check
                        masked_q[a] = q_values[a]
                action = np.argmax(masked_q)
            
            #send action to game environment
            success = game.moves(0, handID, stoodID, action) #(player id, hand id, stood id, action id)
            #check if hand causes bust(or stand)
            player_cards_val = game.hands[handID].get_value()
            dealer_cards_val = game.hands[dealerID].get_value()
            #small penalty for trying illegal move
            if success:
                #save AI move
                AI_moves.append(action)
                #check if player is winning/losing after turn
                if player_cards_val > 21:
                    done = True
                    reward = -1
                elif player_cards_val == 21:
                    done = True
                    reward = 1 #(final reward checks if lose to dealer 21)
                else:
                    done = False
                    reward = 0 
            else:
                reward = -0.1
                #save AI move
                AI_moves.append(action)
            #end if AI stands or doubles
            if action in [0,2]:
                done = True
                break
            
            #predict q_val for next action
            next_state = np.array([player_cards_val, dealer_card_val, bet], dtype=float) #pass the new state to the model
            update_model(model, state, next_state, 0, reward, gamma, done)
            #go to next state
            state = next_state
        #update i since hand is done
        i += 1
    #dealer plays to finish round if not dealt blackjack
    """
    while game.players[dealerID]["hand"].get_value() < 17:
        game.moves(dealerID, 1)
    """
    rewards = []
    if not natural:
        #dealer plays their hand
        game.dealer_play(dealerID, dealerID)
        #go through each hand and determine win/loss/push
        for i in game.players[0]["hands"]:
            #update player cards total
            player_cards_val = game.hands[i].get_value()
            #Determine if player won,lost,push
            dealer_cards_val = game.hands[dealerID].get_value()
            if player_cards_val > 21 or (player_cards_val < dealer_cards_val and dealer_cards_val <= 21):
                reward = -1
                rewards.append(-1)
            elif (player_cards_val == 21 and dealer_cards_val != 21) or player_cards_val > dealer_cards_val:
                reward = 1
                rewards.append(1)
            else:
                reward = 0 
                rewards.append(0)
    else:
        rewards = [-1]#loss on a natural
    #final q_val update
    q_values = model.predict(state.reshape(1, -1), verbose = 0)
    target_q = q_values.copy()
    target_q[0][action] = reward + gamma * 0 #next_q is 0 since no more moves
    #update model
    model.fit(state.reshape(1, -1), target_q, verbose=0)
    #print(f"model reward was: {reward}")

    #add round_data to game_data
    for j, i in enumerate(game.players[0]["hands"]):
        round_data = {
            "round": int(round),
            "player_hand": [card["value"] for card in game.hands[i].cards], 
            "dealer_hand": [card["value"] for card in game.hands[dealerID].cards],
            "actions": [move for move in AI_moves], 
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
#save model as a file
model.save(filesavename)
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
