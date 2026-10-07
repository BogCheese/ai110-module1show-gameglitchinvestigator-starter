import pytest
from streamlit.testing.v1 import AppTest

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

DIFFICULTIES = ["Easy", "Normal", "Hard"]


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Regression: hint messages were swapped ---

def test_too_high_hint_says_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message


def test_too_low_hint_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message


# --- Regression: secret was turned into a str, so comparison was textual ---

def test_numeric_not_text_comparison():
    assert check_guess(9, 10)[0] == "Too Low"      # "9" > "10" as text
    assert check_guess(100, 42)[0] == "Too High"
    assert check_guess(-10000, 42)[0] == "Too Low"  # "-10000" < "42" happened to work; keep it pinned


# --- Regression: difficulty ranges ---

def test_difficulty_ranges():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard")[1] > get_range_for_difficulty("Normal")[1]
    assert get_range_for_difficulty("Unknown") == (1, 100)


# --- Regression: scoring ---

def test_first_guess_win_scores_100():
    assert update_score(0, "Win", 1) == 100


def test_second_guess_win_scores_90():
    assert update_score(0, "Win", 2) == 90


def test_win_points_have_floor():
    assert update_score(0, "Win", 50) == 10


@pytest.mark.parametrize("outcome", ["Too High", "Too Low"])
@pytest.mark.parametrize("attempt", [1, 2, 3, 4])
def test_wrong_guess_always_costs_5(outcome, attempt):
    assert update_score(20, outcome, attempt) == 15


# --- Regression: New Game did not reset state / ignored difficulty ---

def _app():
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()
    return at


def _button(at, label_part):
    return next(b for b in at.button if label_part in b.label)


def test_app_loads_without_exception():
    at = _app()
    assert not at.exception


@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_secret_matches_selected_difficulty(difficulty):
    at = _app()
    at.sidebar.selectbox[0].select(difficulty).run()
    low, high = get_range_for_difficulty(difficulty)
    assert not at.exception
    assert low <= at.session_state.secret <= high


@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_new_game_resets_state(difficulty):
    at = _app()
    at.sidebar.selectbox[0].select(difficulty).run()

    # Simulate a finished game with leftover state.
    at.session_state.status = "won"
    at.session_state.score = 70
    at.session_state.attempts = 3
    at.session_state.history = [1, 2, 3]
    at.run()

    _button(at, "New Game").click().run()

    low, high = get_range_for_difficulty(difficulty)
    assert not at.exception
    assert at.session_state.status == "playing"
    assert at.session_state.score == 0
    assert at.session_state.attempts == 0
    assert at.session_state.history == []
    assert low <= at.session_state.secret <= high


@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_can_play_again_after_new_game(difficulty):
    # After a loss the game is blocked by st.stop(); New Game must unblock it.
    at = _app()
    at.sidebar.selectbox[0].select(difficulty).run()
    at.session_state.status = "lost"
    at.run()
    _button(at, "New Game").click().run()

    at.text_input[0].input("1").run()
    _button(at, "Submit").click().run()

    assert not at.exception
    assert at.session_state.attempts == 1
    assert at.session_state.history == [1]


# --- Invalid / out-of-range guesses are rejected ---

def test_guess_above_range_rejected():
    ok, value, err = parse_guess("150", 1, 100)
    assert ok is False and value is None
    assert "out of range" in err and "1" in err and "100" in err


def test_guess_below_range_rejected():
    ok, _, err = parse_guess("0", 1, 100)
    assert ok is False
    assert "out of range" in err


def test_guess_at_range_edges_accepted():
    assert parse_guess("1", 1, 100) == (True, 1, None)
    assert parse_guess("100", 1, 100) == (True, 100, None)


def test_non_numeric_guess_rejected():
    ok, value, err = parse_guess("abc", 1, 100)
    assert ok is False and value is None
    assert "only whole numbers" in err


def test_decimal_guess_rejected():
    ok, value, err = parse_guess("7.5", 1, 100)
    assert ok is False and value is None
    assert "only whole numbers" in err


def test_app_rejected_guess_does_not_use_attempt():
    at = _app()
    for bad in ["abc", "7.5", "9999", "0"]:
        at.text_input[0].input(bad).run()
        _button(at, "Submit").click().run()
        assert at.error  # an error message is shown
        assert at.session_state.attempts == 0
        assert at.session_state.history == []
