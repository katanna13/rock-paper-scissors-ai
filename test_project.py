import pytest

from main import determine_winner, predict_move,bot_move,predict_move_recent,simulate_games,predict_move_markov
@pytest.mark.parametrize(
    "player, computer, expected",[
        ("rock", "rock", "draw"),
        ("paper", "paper", "draw"),
        ("scissor", "scissor", "draw"),
        ("rock", "scissor", "win"),
        ("rock", "paper", "lose"),
        ("paper", "rock", "win"),
        ("paper", "scissor", "lose"),
        ("scissor", "rock", "lose"),
        ("scissor", "paper", "win"),
    ]
)

def test_determine_winner(player, computer, expected):
    assert determine_winner(player,computer) == expected

@pytest.mark.parametrize(
    "history, expected",[
        ([],None),
        (["rock", "paper", "scissor", "rock"],"rock"),
        (["rock", "paper", "scissor", "paper"],"paper"),
        (["rock", "paper", "scissor", "scissor"],"scissor"),
    ]
)

def test_predict_move(history, expected):
    assert predict_move(history) == expected

@pytest.mark.parametrize(
    "history,strategy,window_size, expected",[
        (["rock","rock","paper"],"full_history",0,"paper"),
        (["rock","paper","paper","rock","rock","scissor"],"sliding_window",3,"paper"),
        (["rock","scissor","scissor"],"full_history",0,"rock"),
    ]
)

def test_bot_move(history,strategy,window_size, expected):
    assert bot_move(history,strategy,window_size) == expected

def test_bot_move_empty_history(monkeypatch):
    monkeypatch.setattr(
        "main.random.choice",
        lambda choises: "paper"
    )
    assert bot_move([]) == "paper"

def test_predict_move_recent():
    history = ["rock"] * 5 + ["scissor"] * 3
    assert predict_move(history) == "rock"
    assert predict_move_recent(history, 5) == "scissor"

def test_window_size():
    with pytest.raises(ValueError):
        predict_move_recent([],-1)

def test_simulate_games():
    wins,draws,losses = simulate_games(
        100, "random", "sliding_window"
    )
    assert wins+draws+losses == 100

    wins,draws,losses = simulate_games(
        100, "always_rock","sliding_window"
    )
    assert wins>=99 and draws+losses<=1

def test_unknown_strategy():
    with pytest.raises(ValueError):
        bot_move([],"unknown_strategy")
        simulate_games(100,"unknown","sliding_window")

def test_predict_move_markov():
    assert predict_move_markov([]) is None
    assert predict_move_markov(["rock"]) is None
    assert predict_move_markov(["rock","scissor"]) is None
    assert predict_move_markov(["rock","paper","rock"]) == "paper"

def test_move_markov(monkeypatch):
    monkeypatch.setattr(
        "main.random.choice",
        lambda choises: "rock"
    )
    assert bot_move([],"markov") == "rock"
    assert bot_move(["rock","scissor"],"markov") == "rock"
    assert bot_move(["rock","paper","rock"],"markov") == "scissor"