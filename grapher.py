import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Load your logged data
data = pd.read_csv("v2_7_results.csv")

# Moving average win rate
window = 1000
plt.figure(figsize=(10, 6))

data['win'] = data['result'] == 1
data['win_ma'] = data['win'].rolling(window).mean()
'''

# Find all *_results.csv files in the current directory
for file in glob.glob("*_1_results.csv"):
    data = pd.read_csv(file)
    if 'result' in data.columns and 'round' in data.columns:
        data['win'] = data['result'] == 1
        data['win_ma'] = data['win'].rolling(window).mean()
        label = os.path.splitext(os.path.basename(file))[0]
        plt.plot(data['round'], data['win_ma'], label=label)
'''

plt.plot(data['round'], data['win_ma'])
plt.xlabel("Round")
plt.ylabel(f"{window}-round moving avg win rate")
plt.title("Blackjack AI Performance")
plt.legend()
plt.tight_layout()
plt.show()
