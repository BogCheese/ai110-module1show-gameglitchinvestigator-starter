# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [X] Describe the game's purpose.
- [X] Detail which bugs you found.
- [X] Explain what fixes you applied.

## 📸 Demo Walkthrough

A sample game on **Normal** difficulty (range 1-100, 8 attempts). Suppose the secret number is **55**.

1. The game starts with score 0 and shows "Guess a number between 1 and 100. Attempts left: 8".
2. User enters `40`. Game shows "📈 Go HIGHER!" (Too Low). Score: -5. Attempts left: 7.
3. User enters `70`. Game shows "📉 Go LOWER!" (Too High). Score: -10. Attempts left: 6.
4. User enters `abc`. Game shows "Invalid input: only whole numbers are accepted (e.g. 42)." The guess is not counted: attempts left stays 6 and the score is unchanged.
5. User enters `7.5`. Game shows the same whole-number error, and nothing changes.
6. User enters `150`. Game shows "150 is out of range. Guess a number between 1 and 100." The guess is rejected and nothing changes.
7. User enters `55`. Game shows "🎉 Correct!", balloons appear, and the game ends with "You won! The secret was 55. Final score: 70". The score is the 100-point first-guess base minus 10 for each earlier valid guess (80 for winning on guess 3), plus the two -5 penalties (80 - 10 = 70).
8. Any further guess shows "You already won. Start a new game to play again."
9. User clicks on New Game. Score, history and attempts reset, and a new secret is chosen from the current difficulty's range.
10. User switches the difficulty to Easy. A fresh game starts with the range 1-20 and 6 attempts, and the hint text shows "Guess a number between 1 and 20".

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================

tests/test_game_logic.py::test_winning_guess PASSED                                     [  3%]
tests/test_game_logic.py::test_guess_too_high PASSED                                    [  6%]
tests/test_game_logic.py::test_guess_too_low PASSED                                     [  9%]
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED                       [ 12%]
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED                       [ 15%]
tests/test_game_logic.py::test_numeric_not_text_comparison PASSED                       [ 18%]
tests/test_game_logic.py::test_difficulty_ranges PASSED                                 [ 21%]
tests/test_game_logic.py::test_first_guess_win_scores_90 PASSED                         [ 24%]
tests/test_game_logic.py::test_win_points_have_floor PASSED                             [ 27%]
tests/test_game_logic.py::test_wrong_guess_always_costs_5[1-Too High] PASSED            [ 30%]
tests/test_game_logic.py::test_wrong_guess_always_costs_5[1-Too Low] PASSED             [ 33%]
tests/test_game_logic.py::test_wrong_guess_always_costs_5[2-Too High] PASSED            [ 36%]
tests/test_game_logic.py::test_wrong_guess_always_costs_5[2-Too Low] PASSED             [ 39%]
tests/test_game_logic.py::test_wrong_guess_always_costs_5[3-Too High] PASSED            [ 42%]
tests/test_game_logic.py::test_wrong_guess_always_costs_5[3-Too Low] PASSED             [ 45%]
tests/test_game_logic.py::test_wrong_guess_always_costs_5[4-Too High] PASSED            [ 48%]
tests/test_game_logic.py::test_wrong_guess_always_costs_5[4-Too Low] PASSED             [ 51%]
tests/test_game_logic.py::test_app_loads_without_exception PASSED                       [ 54%]
tests/test_game_logic.py::test_secret_matches_selected_difficulty[Easy] PASSED          [ 57%]
tests/test_game_logic.py::test_secret_matches_selected_difficulty[Normal] PASSED        [ 60%]
tests/test_game_logic.py::test_secret_matches_selected_difficulty[Hard] PASSED          [ 63%]
tests/test_game_logic.py::test_new_game_resets_state[Easy] PASSED                       [ 66%]
tests/test_game_logic.py::test_new_game_resets_state[Normal] PASSED                     [ 69%]
tests/test_game_logic.py::test_new_game_resets_state[Hard] PASSED                       [ 72%]
tests/test_game_logic.py::test_can_play_again_after_new_game[Easy] PASSED               [ 75%]
tests/test_game_logic.py::test_can_play_again_after_new_game[Normal] PASSED             [ 78%]
tests/test_game_logic.py::test_can_play_again_after_new_game[Hard] PASSED               [ 81%]
tests/test_game_logic.py::test_guess_above_range_rejected PASSED                        [ 84%]
tests/test_game_logic.py::test_guess_below_range_rejected PASSED                        [ 87%]
tests/test_game_logic.py::test_guess_at_range_edges_accepted PASSED                     [ 90%]
tests/test_game_logic.py::test_non_numeric_guess_rejected PASSED                        [ 93%]
tests/test_game_logic.py::test_decimal_guess_rejected PASSED                            [ 96%]
tests/test_game_logic.py::test_app_rejected_guess_does_not_use_attempt PASSED           [100%]

===================================== 33 passed in 5.38s =====================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
