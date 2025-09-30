import pandas as pd
import matplotlib.pyplot as plt

# Load your logged data
data = pd.read_csv("v1_results.csv")

# Moving average win rate
window = 1000
data['win'] = data['result'] == 1
data['win_ma'] = data['win'].rolling(window).mean()

plt.plot(data['round'], data['win_ma'])
plt.xlabel("Round")
plt.ylabel(f"{window}-round moving avg win rate")
plt.title("Blackjack AI Performance")
plt.show()
