import pandas as pd # type: ignore

rewrite = "Initial_training/vI_5_results_fixed.csv"
data = pd.read_csv("Initial_training/v5_results.csv")

def get_hand_value(hand):
    cards = hand.split(',')
    aces = cards.count('11')
    total = sum(int(v) for v in cards)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def get_reward(player, dealer):
    if player > 21:
        return -1
    elif dealer > 21:
        return 1
    elif player > dealer:
        return 1
    elif player < dealer:
        return -1
    else:
        return 0
    

#print(data.dtypes)
#print(data['player_hand'].head())
#recalculate player hand
data['player_hand_sum'] = data['player_hand'].apply(
    get_hand_value
)
#recalculate dealer hand as well
data['dealer_hand_sum'] = data['dealer_hand'].apply(
    get_hand_value
)

#print(data.head)

#recalculate result
data['reward'] = data.apply(lambda row: get_reward(row['player_hand_sum'], row['dealer_hand_sum']), axis=1)

data = data.drop(columns=['result', 'player_hand_sum', 'dealer_hand_sum'])
#print(data.head)
#save to new csv
data.to_csv(rewrite, index=False)