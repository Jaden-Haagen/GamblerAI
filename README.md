# Blackjack AI Project

## **main.py**
Run this file to play a game of blackjack in the terminal.  
- Enter `q` to quit the game when prompted.  
- To make different moves, follow the list:  
  - **stand** = 0  
  - **hit** = 1  
  - **double** = 2  
  - **split** = *Currently does nothing*  

---

## **blackjack_ai.py**
This file holds all the code to run and train an AI model.  
- Running this file will create a new model stored under the assigned file name.  
- A CSV of results will also be saved.  

---

## **blackjack.py**
This file contains all the classes and functions for various parts of a blackjack game:  
- **Deck** → Generates decks, shuffles cards, and deals cards.  
- **Hand** → Adds cards to a player's hand and performs actions (hit, stand, etc.).  
- **BlackjackGame** → Creates players, manages their moves, and controls the dealer's hand.  

---

## Notes
I used ChatGPT to speed up writing code blocks and fix debugging issues.  
This caused some things to be less than ideal in terms of coding style, but they still work well enough for the project.  

A proper **split function** will be implemented later once the codebase is cleaned up further.

# Models

## V1 Notes
Trained the AI model on 10000 games. 
Gamma was 0.95, Epsilon started at 0.3 and followed "epsilon = epsilon_min + (epsilon_start - epsilon_min) * math.exp(-k * round)" until it reached 0.01 with k = 0.001
Training used 6 decks in the shoe.

## V2 Notes
Trained the model on another 10000 games. All settings stayed the same except for starting epsilon value being set to 0.1 instead of 0.3. Model reached a new peak win rate that was better than v1.

## V3 Notes
Kept setting the same as v2 and trained another 10000 games. Model didn't reach a higher win percentage but improved overall by winning more consistently. 

## V4 Notes
Kept setting the same and noticed that over 10000 games the win average began dropping.

## V5 Notes
Ran to see if v4 was just unlucky games and noticed stabilizing under worse conditions

# modified epsilon logic models
currently running to see how improvments in model are different