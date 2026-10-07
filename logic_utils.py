# FIX: Moved from app.py into logic_utils.py via agent mode; I (the user) asked for the refactor and the AI did the move.
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # FIX: Hard was 1-50 (easier than Normal); AI flagged it from the FIXME and I approved making it 1-200.
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


# FIX: Moved to logic_utils.py by the AI; I then asked for out-of-range and non-numeric guesses to be rejected, and the AI implemented it.
def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess.

    If low and high are given, guesses outside [low, high] are rejected.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    raw = raw.strip()

    # FIX: Only whole numbers allowed; I decided decimals should be rejected and the AI removed the float() truncation.
    try:
        value = int(raw)
    except ValueError:
        return False, None, "Invalid input: only whole numbers are accepted (e.g. 42)."

    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"{value} is out of range. Guess a number between {low} and {high}."

    return True, value, None


# FIX: Moved to logic_utils.py by the AI (per my multi-step instruction); it also swapped the reversed high/low hints and dropped the str-comparison fallback.
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


# FIX: AI rewrote scoring after I reported a first-guess win gave 90 instead of 100; wrong guesses now always cost 5.
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
