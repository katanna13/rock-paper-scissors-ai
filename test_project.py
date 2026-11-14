import pytest
from _pytest import monkeypatch

from main import determine_winner, predict_move,bot_move

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
    "history, expected",[
        (["rock","rock","paper"],"paper"),
        (["rock","paper","paper"],"scissor"),
        (["rock","scissor","scissor"],"rock"),
    ]
)

def test_bot_move(history, expected):
    assert bot_move(history) == expected

def test_bot_move_empty_history(monkeypatch):
    monkeypatch.setattr(
        "main.random.choice",
        lambda choises: "paper"
    )
    assert bot_move([]) == "paper"