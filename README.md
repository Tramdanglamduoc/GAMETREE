# 🎮 GAMETREE — Number Multiplication Game with AI

A two-player number game where you compete against an AI powered by **Minimax** and **Alpha-Beta Pruning** algorithms. Built with Python and Kivy for a graphical interface.

This project was developed as part of the *Fundamentals of Artificial Intelligence* course at Riga Technical University (Team 26).

---

## What Is This Game?

You and the AI take turns multiplying a number. The goal is to reach **1200 or more** while scoring more points than your opponent. Simple rules, but the AI thinks 5 moves ahead — so every choice matters.

### Scoring Rules

| Situation | Effect |
|---|---|
| Result is **even** | Current player loses **1 point** |
| Result is **odd** | Current player gains **1 point** |
| Result ends in **0 or 5** | **+1 point added to the Bank** |
| Game ends (≥ 1200) | Last player **claims all Bank points** |

The player with the highest score at the end wins. In case of a tie, it's a draw.

---

## Requirements

- Python 3.x
- [Kivy](https://kivy.org/) library

Install Kivy with:

```bash
pip install kivy
```

Make sure `seguiemj.ttf` (included in the repo) is in the **same directory** as `final-draft.py` — it's needed for emoji rendering in the UI.

---

## How to Run

```bash
python final-draft.py
```

---

## How to Play

**Step 1 — Enter a starting number**  
Type any integer between **8 and 18** in the input field.

**Step 2 — Choose an AI algorithm**  
- 🧠 **Minimax** — explores all possible game paths (slower but exhaustive)  
- ⚡ **Alpha-Beta Pruning** — same result as Minimax, but skips irrelevant branches (faster)

**Step 3 — Choose who goes first**  
- 🙋 **You Start** — you make the first move  
- 🤖 **AI Starts** — the AI moves first

**Step 4 — Take turns multiplying**  
Each turn, click ×2, ×3, or ×4 to multiply the current number. The AI responds automatically after your move.

**Step 5 — Game ends when the number hits 1200+**  
The player who made that final move collects the Bank. Scores are compared and the winner is announced.

**To play again**, click the 🔄 **Retry** button at any point after the starting number is entered.

---

## Game Stats

At the end of each game, the UI shows:

- **Total Nodes Explored** — how many game states the AI evaluated
- **Alpha Cuts** *(Alpha-Beta only)* — branches pruned at MAX levels
- **Beta Cuts** *(Alpha-Beta only)* — branches pruned at MIN levels

These stats let you directly compare the efficiency of the two algorithms.

---

## How the AI Works

The AI searches 5 moves ahead using a game tree. At each node, it simulates all possible multiplications (×2, ×3, ×4) and evaluates the resulting game state with this heuristic:

```
If game ends (≥ 1200):
  h(s) = scoreP2 + bank − scoreP1   (if AI ends the game)
  h(s) = scoreP2 − (scoreP1 + bank) (if human ends the game)

Otherwise:
  h(s) = scoreP2 − scoreP1
```

**Minimax** explores every node in the tree. **Alpha-Beta Pruning** cuts branches where the result can't possibly affect the final decision — achieving the same move choice with significantly fewer computations. In our experiments, Alpha-Beta was roughly 1.75× faster than plain Minimax.

---

## Project Structure

```
GAMETREE/
├── final-draft.py     # Main game (GUI version using Kivy)
├── seguiemj.ttf       # Emoji font required by Kivy
└── Report/            # Assignment report (PDF)
```

---

## Team

Developed by Team 26 — Riga Technical University, 2024/2025  
Course: Fundamentals of Artificial Intelligence  
Instructor: Alla Anohina-Naumeca
