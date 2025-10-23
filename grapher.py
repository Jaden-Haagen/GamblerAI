import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import glob
import os

def plot_win_rate(i: int, show: bool):
    # Load your logged data
    data = pd.read_csv(f"model_v1/v1_{i}_results_fixed.csv")
    filename = (f"model_v1/v1_{i}_Win_Percent.png")
    # Moving average win rate
    window = 1000
    plt.figure(figsize=(10, 6))
    #data['win'] = data['result'] == 1
    data['win'] = data['reward'] == 1
    data['win_ma'] = data['win'].rolling(window).mean()
    '''

    # Find all *_results.csv files in the current directory
    #for file in glob.glob("*_1_results.csv"):
    for file in glob.glob("*_results_fixed.csv"):
        data = pd.read_csv(file)
        if 'reward' in data.columns and 'round' in data.columns:
            #data['win'] = data['result'] == 1
            data['win'] = data['reward'] == 1
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
    plt.savefig(filename)
    if show:
        plt.show()

for i in range(14, 15):
    plot_win_rate(i, show=False)