from blackjack import BlackjackGame

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
            tf.keras.layers.Dense(32, activation='relu', input_shape=(state_size,)),
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
#environment size
state_size = 3 #what the ai needs to analyze(dealer card, player's cards, bet)
num_actions = 3 #what the AI can do (hit, stand, double) add (split, bet) later
learning_rate = 0.001 # small number = slow but stable, big number = fast but overshoots frequently
#model file
filename = "test_model_v1.keras"
"""
#try using an existing model
if os.path.exists(filename):
    model = tf.keras.models.load_model(filename, compile = False)
    print("Loaded existing model")
#create new model if file not found
else:
    #create a model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(32, activation='relu', input_shape=(state_size,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(num_actions, activation='linear')
    ])
    print("Created a new model")

#compile model for training/running
learning_rate = 0.001 # small number = slow but stable, big number = fast but overshoots frequently
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate),loss='mse')
"""
#initialize model
model = initialize_model(state_size, num_actions, learning_rate, filename)

num_rounds = 1000 #test size (change to 1000+ after everything works)
gamma = 0.95 #discount factor (0 = cares about current reward, 1 = cares about future reward)
epsilon = 0.1 #exploration rate (0 = no exploration only follow model, 1 = always explores new options)

numDecks = 6
numPlayers = 1
game_data = []

#Begin game
game = BlackjackGame(numDecks, numPlayers)
dealerID = numPlayers #dealerID is always the last position in the initial list
#Allow agent to play rounds
for round in trange(num_rounds, desc = "AI Training Progress"):
    #print(f"Round #{round+1}")
    #check deck size and add cards if needed
    game.deck.reshuffle(numDecks)
    #start with bet (AI bet will be 1 until model can play reliably)
    bet = 1
    game.players[0]["hand"].bet = bet
    #deal table
    game.deal_cards()
    
    #get known values for AI to make a decision
    player_cards_val = game.players[0]["hand"].get_value()
    dealer_card_val = game.players[dealerID]["hand"].cards[0]["value"]#return value of first card in dealer hand

    state = np.array([player_cards_val, dealer_card_val, bet], dtype=float)#change this for environment(get_player_val, get_dealer_val, etc)
    done = False

    #check for dealer blackjack (no insurance for current game since betting not considered)
    dealer_cards_val = game.players[dealerID]["hand"].get_value()
    if dealer_cards_val == 21:
        done = True

        #check if player push or lose
        if player_cards_val == 21:
            reward = 0
        else:
            reward = -1

        #update the model with the loss or push
        """
        q_values = model.predict(state.reshape(1, -1), verbose = 0)
        q_values[0][0] = reward  #no actions taken so update first index
        model.fit(state.reshape(1, -1), q_values, verbose = 0)
        """
        update_model(model, state, state, 0, reward, gamma, done)
        continue #skip the rest of the round actions
    
    AI_moves = []
    #loops until AI model chooses to stand or busts
    while not done:
        #randomly choose an action to play if exploration condition is met (10% of moves are random)
        if np.random.rand() < epsilon:
            action = np.random.randint(num_actions)
        else:
            q_values = model.predict(state.reshape(1, -1), verbose = 0)
            action = np.argmax(q_values[0])
        
        #send action to game environment
        game.moves(0, action) #(player id, action id)
        #save AI move
        AI_moves.append(action)
        #end if AI stands or doubles
        if action in [0,2]:
            done = True
            break
        #check if hand causes bust(or stand)
        player_cards_val = game.players[0]["hand"].get_value()
        dealer_cards_val = game.players[dealerID]["hand"].get_value()
        if player_cards_val > 21:
            done = True
            reward = -1
        elif player_cards_val == 21:
            done = True
            reward = 1 #(final reward checks if lose to dealer 21)
        else:
            done = False
            reward = 0 
        #predict q_val for next action
        next_state = np.array([player_cards_val, dealer_card_val, bet], dtype=float) #pass the new state to the model
        """next_q_values = model.predict(next_state.reshape(1, -1), verbose = 0) #q_vals for new state
        #compute q_val for action
        q_values = model.predict(state.reshape(1, -1), verbose = 0) #updated q_vals for the original state
        #update model(training)
        if done:
            target = reward
        else:
            target = reward + gamma * np.max(next_q_values[0])
        #tell model what its reward was for its action (-  if it lost/busted, + if it finished without losing)
        q_values[0][action] = target
        model.fit(state.reshape(1, -1), q_values, verbose = 0)"""
        update_model(model, state, next_state, 0, reward, gamma, done)
        #go to next state
        state = next_state
    #dealer plays to finish round
    """
    while game.players[dealerID]["hand"].get_value() < 17:
        game.moves(dealerID, 1)
    """
    game.dealer_play(dealerID)
    #Determine if player won,lost,push
    player_cards_val = game.players[0]["hand"].get_value()
    dealer_cards_val = game.players[dealerID]["hand"].get_value()
    if player_cards_val > 21 or (player_cards_val < dealer_cards_val and dealer_cards_val <= 21):
        reward = -1
    elif (player_cards_val == 21 and dealer_cards_val != 21) or player_cards_val > dealer_cards_val:
        reward = 1
    else:
        reward = 0 

    #final q_val update
    target_q = q_values.copy()
    target_q[0][action] = reward + gamma * 0 #next_q is 0 since no more moves
    #update model
    model.fit(state.reshape(1, -1), target_q, verbose=0)
    #print(f"model reward was: {reward}")

    #add round_data to game_data
    round_data = {
        "player_hand": [card["value"] for card in game.players[0]["hand"].cards], 
        "dealer_hand": [card["value"] for card in game.players[dealerID]["hand"].cards],
        "actions": [move for move in AI_moves], 
        "result": reward
    }
    game_data.append(round_data)

    #clear table
    for player in game.players:
        player["hand"].clear()
        player["stood"] = 0

#save model
#filename = "test_model_v1.keras"
model.save(filename)
#print(game_data)
#save game results (stored in csv)
resultsFile = "blackjack_ai_results.csv"
with open(resultsFile, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["player_hand", "dealer_hand", "actions", "result"])
    writer.writeheader()

    for round_info in game_data:
        writer.writerow({
            "player_hand": ','.join(map(str, round_info["player_hand"])),
            "dealer_hand": ','.join(map(str, round_info["dealer_hand"])),
            "actions": ','.join(map(str, round_info["actions"])),
            "result": str(round_info["result"])
        })
