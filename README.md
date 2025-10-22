# Blackjack AI Project

## **main.py**
### ⚠️ **MAY NOT WORK IN CURRENT VERSION**
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
I used LLMs to speed up writing code blocks, fix debugging issues, and experiment with how LLMs can benefit and hurt programming work flows.  
The biggest thing I noticed from this project was how LLMs were not always consistant with how they worded comments or code. ChatGPT was better than the integrated copilot model in vs code for with consistancy. Copilot was useful in quickly filing out for loops and if statements but not as helpful when working with repeating unique logic and lists as it would try to find patterns where there weren't any.  


# Models

## Initial Training
### V1 Notes
Trained the AI model on 10000 games. 
Gamma was 0.95, Epsilon started at 0.3 and followed "epsilon = epsilon_min + (epsilon_start - epsilon_min) * math.exp(-k * round)" until it reached 0.01 with k = 0.001
Training used 6 decks in the shoe.

### V2 Notes
Trained the model on another 10000 games. All settings stayed the same except for starting epsilon value being set to 0.1 instead of 0.3. Model reached a new peak win rate that was better than v1.

### V3 Notes
Kept setting the same as v2 and trained another 10000 games. Model didn't reach a higher win percentage but improved overall by winning more consistently. 

### V4 Notes
Kept setting the same and noticed that over 10000 games the win average began dropping.

### V5 Notes
Ran to see if v4 was just unlucky games and noticed stabilizing under worse conditions

## modified epsilon logic models
currently running to see how improvments in model are different

Noticed a drop off at performance improvements that never changed by model 8. Switched epsilon from .3 to .5 and continued the training with same epsilon decay equation. (may need to modify the model to have more than 2 layers to improve average win percentages)


## V2 Model
added neurons to initial layer (32 -> 64)
added another layer
v2_5 was trained over 60k games
v2_7 was trained over 100k games hust to see what would happen

# Note about win percentages
After various training methods and models I decided to program logic for basic strategy to compare the models to. 
After running it over 1 million games I found out that there was an error with the win logic that caused dealer busts to be counted as pushes instead of wins. Adjusting this logic I found that previous models I trained were performing at the same level as basic strategy which was the goal.

# Future Changes
I build out a python file to load ai models and provide AI recommended moves.
May build models for other Casino games with more variables and random actions.