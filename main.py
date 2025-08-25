from blackjack import BlackjackGame, Hand, Deck

def main():
    game = BlackjackGame(numDecks = 2, numPlayers = 1)
    quit = False
    while not quit:
        #user places bet
        print(f"You have ${game.players[0]["money"]}")
        bet = input("Enter bet amount (q to quit): ").lower()#force lowercase to prevent Q from failing
        if bet == "q":
            #end game
            quit = True
            break
        elif int(bet) > 0 and int(bet) <= game.players[0]["money"]:
            #set players bet amount
            game.players[0]["hand"].bet = int(bet)
            game.players[0]["money"] -= game.players[0]["hand"].bet#remove bet amount from your money 
        else:
            bet = -1
            print("Invalid input")
        #Fail safe incase player entered invalid bet amount 
        if int(bet) > 0 and not quit:
            #play hand since bet is valid
            game.deal_cards()
            #print("Dealer shows: ", game.dealer[0]["hand"].cards[0])
            print("Dealer shows: ", game.players[-1]["hand"].cards[0])
            print("Your hand: ", game.players[0]["hand"].cards)

            while not int(game.players[0]["stood"]) and game.players[0]["hand"].get_value() < 21:
                action = int(input("Choose action (stand/hit/double/split): "))
                game.moves(0, action)
                print("Your hand:", game.players[0]["hand"].cards)

            while game.players[-1]["hand"].get_value() < 17:
                game.moves(-1, 1)
            print("\nDealer hand:", game.players[-1]["hand"].cards)

            # Decide winner
            player_val = game.players[0]["hand"].get_value()
            dealer_val = game.players[-1]["hand"].get_value()

            if player_val > 21:
                print("You bust! Dealer wins.")
            elif dealer_val > 21 or player_val > dealer_val:
                print("You win!")
                game.players[0]["money"] += (game.players[0]["hand"].bet) * 2 #give you winnings + initial bet
            elif dealer_val > player_val:
                print("Dealer wins!")
            else:
                print("Push (tie).")
                game.players[0]["money"] += game.players[0]["hand"].bet #you get initial bet back
            #clear table
            for player in game.players:
                player["hand"].clear()
                player["stood"] = 0
    print(f"Thanks for playing! You finished with ${game.players[0]["money"]}")

if __name__ == "__main__":
    main()
