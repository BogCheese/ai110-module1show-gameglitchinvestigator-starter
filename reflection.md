# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?
Answer: When I started I realized the hints were broken, or rather they were completely wrong. When it said to go lower value when I input -10000, and the actual number was -35, I could see something in the code was flawed regarding hints at least. But otherwise if you guess the secret number it functions as expected. I dont really understand what the score stands for as I got -25 in the developer debug info section but thats there for now. I can look more into that after. Another thing that was broken was the difficulty system. Hard is 1-50 whilst Normal difficulty is 1-100, this is flawed as guessing a number 1-50 is vastly easier than guessing a number 1-100.

- What did the game look like the first time you ran it?
Answer: The game looked like a simple number guesser between 1 and 100, displayed updated attempts at each area. Had a simple text box to take in answers and a Submit button and a new game button that didn't work correctly.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
Answer: The hints are completely incorrect, having -1000 while saying its lower when the secret number is -35 was completely wrong. Another bug I noticed was starting a new game was impossible.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|

| Guess `-10000` when the secret is `-35` | Hint says "Go HIGHER" | Hint says "Go LOWER" | No error; wrong hint shown (`check_guess`, app.py 37-40: messages swapped) |

| Any valid guess on an even attempt (first guess counts as attempt 2) | Guess is compared to the integer secret | Secret is converted to `str`, so results can be wrong (e.g. "9" > "10") | No error shown; `TypeError` is caught silently in `check_guess` (app.py 158-161, 41-47) |

| Win or lose a game, then click **New Game** | New round with fresh score, history and status | "Game over. Start a new game" appears and play stops; score/history persist; secret ignores difficulty | No error; `st.stop()` at app.py 145 (New Game block, app.py 134-138) |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Answer: I used Claude Code (agent mode) inside VS Code. I gave it multi-step instructions, such as moving `check_guess` into `logic_utils.py`, fixing the hint bug and updating the import in `app.py`, and it edited the files and ran pytest itself.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
Answer: Correct suggestion: a `reset_game()` function for the New Game bug. The AI traced the bug to the New Game block only resetting `attempts` and picking the secret from a hardcoded 1-100. Because status was never reset to "playing", `st.stop()` blocked all play after a win or loss. It suggested one `reset_game()` that resets attempts, score, status and history and picks the secret from the current difficulty's `low`/`high`, and it also calls it when the difficulty changes. This was correct because it fixed the actual cause (stale `status` in `st.session_state`) instead of patching the symptom. I verified it by checking that a won/lost game can be restarted, and with a test that forces `status="won"` with leftover score and history, clicks New Game, and asserts everything is reset and the secret is inside the range for Easy, Normal and Hard (`test_new_game_resets_state`).

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
Answer: Changed suggestion: Hard range 1-200. The FIXME said Hard (1-50) was easier than Normal (1-100), and the AI fixed it by changing Hard to 1-200 without touching the attempt limit. When I asked it to review the code for anything out of scope or a poor fit, it caught its own mistake: 200 numbers need about 8 guesses even with perfect halving, but Hard only allows 5 attempts, so Hard is nearly unwinnable (Easy needs about 5 of 6 attempts, Normal about 7 of 8, so those are fair). The range fix was right, but leaving the attempt limit alone made it a poor fit for how the game plays. I am treating the attempt limit as part of the same fix: either raise Hard's attempts or shrink its range. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
Answer: I treated a bug as fixed only when a test that targets that exact behaviour passed, not just when the app looked right. Each bug got a simple test: for the hints, `check_guess(60, 50)` must return "Too High" and its message must say "LOWER". For the string-comparison bug, `check_guess(9, 10)` must be "Too Low". For scoring, `update_score(0, "Win", 1)` must be 100 (it was 90 before I reported it). For input handling, `parse_guess("abc", 1, 100)`, `"7.5"`, `"150"` and `"0"` must all be rejected, and `"1"` and `"100"` must be accepted.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
Answer: I ran `python -m pytest -v` from the project folder; the final run was 34 passed. The three starter tests were actually failing at first because `check_guess` returns `(outcome, message)` but they compared the whole result to a string, which showed the tests were out of date, not the game. I also added an app-level test with Streamlit's `AppTest` that submits `abc`, `7.5`, `9999` and `0` and checks an error is shown and that `attempts` stays 0 and `history` stays empty, which proved rejected guesses no longer use up an attempt. Separately, I started the app with `streamlit run app.py --server.headless true` and its health check returned 200 with no errors in the log.

- Did AI help you design or understand any tests? How?
Answer: Yes. The AI wrote the pytest cases and explained why the starter tests failed, and it used `streamlit.testing.v1.AppTest` to test the New Game and difficulty bugs that live in `app.py` rather than in `logic_utils.py`. I steered it toward simpler tests ("a guess of 60 against a secret of 50 returns Too High"), since a short test that names one bug is easier to trust than a long one.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
