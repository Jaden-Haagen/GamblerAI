from blackjack import BlackjackGame, Hand

import math
import tensorflow as tf # type: ignore
import numpy as np # type: ignore
import csv
import os
from tqdm import trange # type: ignore #for progress bar

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
    return model

#function to train model
def train_model(filename,
                state_size,
                num_actions,
                learning_rate,
                num_rounds,
                gamma,
                epsilon,
                epsilon_start,
                epsilon_min,
                k,
                rounds_trained,
                numDecks,
                numPlayers,
                game_data):

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
        
        #setup state variables
        player_cards_val = 0 #unknown
        dealer_card_val = 0 #unknown
        bet = 0 #need to determine
        balance_norm = game.money[0]/1000 #normalized balance
        bet_norm = 0 #normalized bet
        last_result = 0 #outcome of last hand
        #(player's cards, dealer card, bet, balance(normalized), bet(normalized), last_result)
        state = np.array([player_cards_val, dealer_card_val, bet, balance_norm, bet_norm, last_result], dtype=float)
        #AI makes bet
        chip_values = [1, 5, 10, 25, 50, 100, 500, 1000]
        if np.random.rand() < epsilon:
            bet = np.random.choice(chip_values)
        else:
            q_values = model.predict(state.reshape(1, -1), verbose = 0)[0]
            # Mask invalid actions (set to very negative so argmax won't pick them)
            masked_q = np.full_like(q_values, -np.inf)
        bet = 1
        game.hands[0].bet = bet
        #deal table
        game.deal_cards()

        #get known values for AI to make a decision
        player_cards_val = game.hands[0].get_value()
        dealer_card_val = game.hands[dealerID].cards[0]["value"]#return value of first card in dealer hand

        state = np.array([player_cards_val, dealer_card_val, bet, balance_norm, bet_norm, last_result], dtype=float)
        



#Update these parts to change models, training, storage location, etc.
#File names for model, new model, and game results
filename = "model_v3_0.keras"
filesavename = "model_v3_0.keras"
resultsFile = "v3_0_results.csv"

#environment size
state_size = 6 #what the ai needs to analyze (dealer card, player's cards, bet, balance(normalized), bet(normalized), last_result)
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

train_model(filename,
            state_size,
            num_actions,
            learning_rate,
            num_rounds,
            gamma,
            epsilon,
            epsilon_start,
            epsilon_min,
            k,
            rounds_trained,
            numDecks,
            numPlayers,
            game_data)