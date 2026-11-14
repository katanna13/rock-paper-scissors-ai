import random
from collections import defaultdict

loses = {
        "rock": "paper",
        "paper": "scissor",
        "scissor": "rock"
    }
def predict_move(history):
    if not history:
        return None
    count = defaultdict(int)
    for move in history:
        count[move] += 1
    return max(count, key=count.get)
def bot_move(history):
    if not history:
        return random.choice(["rock", "paper", "scissor"])
    predict = predict_move(history)
    return loses[predict]
def determine_winner(player,computer):
    if player == computer:
        return "draw"
    if loses[player] == computer:
        return "lose"
    return "win"

def play_game():
    wins = 0
    losses = 0
    draws = 0
    history = []
    print("=== ROCK PAPER SCISSOR ===")
    while True:
        choice = input("Choose: rock / paper / scissor / quit \n").strip().lower()
        if choice in ['rock', 'paper', 'scissor']:
            computer = bot_move(history)
            print("Computer chose:", computer)
            result = determine_winner(choice, computer)
            if result == "win":
                wins += 1
                print("You won!")
            elif result == "draw":
                draws += 1
                print("Draw")
            else:
                losses += 1
                print("You lost!")
            print("Score:")
            print(f"Player: {wins} | Computer: {losses} | Draw: {draws}")
            history.append(choice)
        elif choice == "quit":
            break
        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    play_game()
