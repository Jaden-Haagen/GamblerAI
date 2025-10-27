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
### Notes
- AI was trained in 10000 game increments to ensure randomness of cards and smoothen out any unlucky hand results.

- Gamma was 0.95, Epsilon started at 0.3 and followed "epsilon = epsilon_min + (epsilon_start - epsilon_min) * math.exp(-k * round)" until it reached 0.01 with k = 0.001
- Training used 6 decks in the shoe.
- In training 1 there was great initial success. With a peak win rate of about 40 percent after learning from 3000 hands. After about 5000 games it appeared to suffer from slight over training or epsilon values as the win precentage dropped slightly and gradually continue to fall. 
Through the next 20000 games (training 2 and 3) it reached 40 percent win rates but never had the same success. 
By 40000 and 50000 games (training 4 and 5) it was clearly suffering from overtraining and was becoming more unstable.


## V1 Training
Designed to see the affects of using a constant epsilon equation through trainings by adding previous rounds trained to the rounds variable in the epsilon equation.

With the first training run the model achieved better peak win percentages than the initial model but was slightly less stable. This wasn't as big of an issue though as the model still had plenty of time to learn.
In the second training the epsilon logic modification proved to work as the model improved its peak win rate to around 44 percent. 
After training over many more sessions I noticed that while it did suffer from worse performance it didn't just drop and stay low but instead fluctuated and would sometimes return to 40 percent.


## V2 Model
- added neurons to initial layer (32 -> 64)
- added another layer
- v2_5 was trained over 60k games
- v2_6 was a quick training due to a typo trying to run 100k games
- v2_7 was trained over 100k games hust to see what would happen
The added neurons and layers caused training to be less stable initially. After hitting about 40 percent win rate it dropped and stayed below 38 percent for about 64k games.
With the large number of games trained over the model had started to play with worse win percentages than previous models but would spike up to around 45 percent before dropping again. I think this was more due to overtraining than the changes in the model since the random drastic changes only appear later in training.

# Note about win percentages
After various training methods and models I decided to program logic for basic strategy to compare the models to. 
After running it over 1 million games I found out that there was an error with the win logic that caused dealer busts to be counted as pushes instead of wins.
This lead to the win percentages being lower than they should've been. After adjusting the logic and recalculating the results for all saved game data I found the percentages increased by around 5 to 10 percent.
When I compared the basic strategy to the AI models I found they performed about the same at their peak win rates but over all still performed worse than the basic strategy. Now that I am more familiar with training models and making modifications I will see if I can train a model to achieve a peak win rate similar to basic strategy.

# Future Changes
I plan to load ai models and provide AI recommended moves to players during their games.

Design and train AI models that can play other games like roulette and poker.