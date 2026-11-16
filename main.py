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
def predict_move_recent(history,window_size=20):
    if window_size<=0:
        raise ValueError("window_size must be positive")
    return predict_move(history[-window_size:])
def predict_move_markov(history):
    if not history:
        return None
    count = {
        "rock": {"paper":0, "scissor":0,"rock":0},
        "paper": {"rock":0, "scissor":0,"paper":0},
        "scissor": {"paper":0, "rock":0, "scissor":0},
    }

    for i,move in enumerate(history[:-1]):
        count[move][history[i+1]] += 1
    max_value = 0
    for value in count[history[-1]]:
        if count[history[-1]][value]>max_value:
            max_value = count[history[-1]][value]
            winner = value
    if max_value==0:
        return None
    return winner
def bot_move(history,strategy="sliding_window",window_size=20):
    if not history:
        return random.choice(["rock", "paper", "scissor"])
    if strategy == "full_history":
        predict = predict_move(history)
    elif strategy == "sliding_window":
        predict = predict_move_recent(history,window_size)
    elif strategy == "markov":
        predict = predict_move_markov(history)
        if predict is None:
            return random.choice(["rock", "paper", "scissor"])
    else:
        raise ValueError(f"Unknown bot strategy: {strategy}")
    return loses[predict]
def determine_winner(player,computer):
    if player == computer:
        return "draw"
    if loses[player] == computer:
        return "lose"
    return "win"

def simulate_games(rounds,opponennt_strategy,bot_strategy,window_size = 20):
    wins = 0
    losses = 0
    draws = 0
    history = []
    for i in range(rounds):
        if opponennt_strategy == "always_rock":
            choice = "rock"
        elif opponennt_strategy == "random":
            choice = random.choice(["rock", "paper", "scissor"])
        elif opponennt_strategy == "switch":
            if i<rounds//2:
                choice = "rock"
            else:
                choice = "scissor"
        elif opponennt_strategy == "cycle":
            choices = ["rock", "paper", "scissor"]
            choice = choices[i%3]
        else:
            raise ValueError(f"Unknown strategy: {opponennt_strategy}")
        computer = bot_move(history,bot_strategy,window_size)
        result = determine_winner(computer,choice)
        if result == "lose":
            losses += 1
        elif result == "win":
            wins += 1
        else:
            draws += 1
        history.append(choice)
    return wins,draws,losses
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
    print("Random:", simulate_games(1000, "random", "markov"))
    print("Switch:", simulate_games(200, "switch", "markov"))