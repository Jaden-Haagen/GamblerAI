import csv
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

def convert_strings(cards):
    if isinstance(cards, str):
        cardList = cards.split(",") #split the string at the commas
        converted = [] #temp storage of values
        #take the strings and make them ints
        for c in cardList:
            converted.append(int(c))
        return converted
    else:
        return [cards]

def calculate_hand(hand):
    aces = hand.count(11)
    total = sum(hand)
    #Aces count as 1 if hand busts until it no longer busts or no more aces present
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total
def plot_progress(x, y):
    plt.scatter(x, y)
    plt.xlabel("player hand value")
    plt.ylabel("dealer hand value")
    plt.title("AI results")
    #plt.show
    plt.savefig("test.png")

def main():
    filename = "blackjack_ai_results.csv"
    df = pd.read_csv(filename) #create a dataframe of the csv data
    #convert strings to integers for graphs and calculations
    df["player_hand"] = df["player_hand"].apply(convert_strings)
    df["dealer_hand"] = df["dealer_hand"].apply(convert_strings)
    df["actions"] = df["actions"].apply(convert_strings)
    #generate columns containing the value of player and dealer hands
    df["player_total"] = df["player_hand"].apply(calculate_hand)
    df["dealer_total"] = df["dealer_hand"].apply(calculate_hand)
    #checking data to ensure everything was working properly
    #"""print(df.head())
    for _, row in df.iterrows():
        if row["player_total"] == 22 and row["result"] in [0]: #should be physically impossible to get a hand value higher than 30 hand since you can't hit a 21
            print(f"hand: {row['player_hand']}, total: {row['player_total']}")
    #"""
    plot_progress(df["player_total"], df["dealer_total"])
    plt.clf() #clear the graph
    #How frequent hand values appear
    plt.hist(df["player_total"], bins=range(0, 32))  # 0–21
    plt.xlabel("Player Hand Total")
    plt.ylabel("Frequency")
    plt.title("Distribution of Player Hand Totals")
    plt.savefig("value_dist.png")
    plt.clf() #clear the graph
    #heatmap of win/loss/draw vs hand value
    sns.histplot(data=df, x="player_total", hue="result", multiple="stack", bins=range(0,31))
    plt.xlabel("Player Hand Value")
    plt.ylabel("Number of Occurances")
    plt.title("Frequency of Hand Values w/ win/loss/draw per Occurance")
    plt.xticks(range(0, 31), rotation=270)
    plt.savefig("handvwin.png")
    plt.clf() #clear the graph


    #first 100 game training
    filename = "blackjack_ai_results_v1.csv"
    df2 = pd.read_csv(filename)
    
    counts = df2["result"].value_counts()
    total = len(df2)
    percentages = (counts / total) * 100
    print("Percentages for 1000 games trained")
    for result, pct in percentages.items():
        print(f"{result}: {pct:.2f}%")
    
    #percentages for all results
    counts = df["result"].value_counts()
    total = len(df)
    percentages = (counts / total) * 100
    print("Percentages for 10000 games trained")
    for result, pct in percentages.items():
        print(f"{result}: {pct:.2f}%")



if __name__ == "__main__":
    main()