# Wordle Solver

> Every guess is a question. This solver asks the best one.

Built on a single idea from information theory: the best move is the one that
reduces uncertainty the most. Each turn, the solver computes the entropy of
every candidate's feedback distribution and plays the word that maximizes
expected information gain — no frequency tables, no heuristics, just bits.

## How It Works

At its core, the solver reframes Wordle as a communication problem: the answer
is a hidden message, each guess is a query, and feedback is the channel's reply.
A good guess is one that makes the reply as unpredictable as possible.

Concretely:

1. Every guess/target pair is mapped to one of 243 feedback patterns and stored
   in a precomputed **pattern matrix** using base-3 encoding (`r=0, y=1, g=2`).
2. For each remaining guess, candidates are grouped by the pattern they'd
   produce — a partition of the current search space.
3. The entropy of that partition measures how informative the guess is:
   ```
   H(Y) = -Σ p(pattern) · log₂(p(pattern))
   ```
5. Play the guess with the highest entropy — the one expected to reveal the most information.
6. Filter the candidate list using the actual feedback and repeat.

4. The highest-entropy guess is played, feedback is collected, and the candidate
list is filtered to matching patterns. Repeat.

The solver surfaces the full information-theoretic picture each turn:

- **H(W)** — prior uncertainty over candidates
- **H(Y)** — entropy of the guess's feedback
- **H(W|Y)** — posterior uncertainty after the guess
- **I(W;Y)** — mutual information, i.e. the bits the guess is expected to reveal)

## Features

- Entropy-maximizing guess selection
- Fast — vectorized with NumPy, pattern matrix is cached to disk
- Shows entropy metrics and the top-20 ranked guesses each turn
- Prioritizes actual candidate answers as tiebreakers
- Interactive — you enter the feedback Wordle gives you
- Automatically builds and caches the pattern matrix on first run

## Requirements

- **Python 3.8+**
- **NumPy**

Install NumPy if you don't have it:

```bash
pip install numpy
```

## Files

```
wordle-solver/
├── main.py                    # The solver
├── dictionary_5_letter.json   # All valid 5-letter guesses
├── targets_5_letter.json      # Possible Wordle answers
└── pattern_matrix.npy         # Auto-generated cache (created on first run)
```

- `dictionary_5_letter.json` — a JSON array of every 5-letter English word allowed as a guess.
- `targets_5_letter.json` — a JSON array of the words that can actually be the answer.
- `pattern_matrix.npy` — generated automatically the first time you run the solver. Delete it to force a rebuild.

## Usage

Run the solver:

```bash
python main.py
```

The solver prints its best guess along with entropy metrics and a ranked list of the top 20 words. You then:

1. Enter the guess it recommends (or any valid guess) when prompted.
2. Enter the feedback Wordle gave you as a 5-character string of `r` (red/gray), `y` (yellow), `g` (green), in order.

Example session:

```
remaining candidates:  2315
H(W) (prior entropy) =  11.177 bits
H(Y) (best guess's entropy) =  5.886 bits
H(W|Y) (posterior entropy) =  5.291 bits
I(W;Y) information gain =  5.886 bits
  soare — H(Y)=5.886 bits
  roate — H(Y)=5.885 bits
  ...
BEST=soare
soare
rryrg

remaining candidates:  98
H(W) (prior entropy) =  6.614 bits
...
BEST=...
```

When only one candidate remains, the solver prints it directly:

```
BEST=point
```

Enter the guess and its feedback, and it will confirm `solved`.

Feedback legend:

| Char | Meaning |
|------|---------|
| `g`  | Green — correct letter, correct position |
| `y`  | Yellow — correct letter, wrong position |
| `r`  | Gray — letter not in the word |

## Customization

Want to use your own word lists? Just replace the two JSON files with your own arrays of 5-letter words:

- `dictionary_5_letter.json` — words the solver is allowed to guess.
- `targets_5_letter.json` — words that can be the answer.

Then delete the cached `pattern_matrix.npy` and run the solver again — it will rebuild the matrix against your new lists automatically.

## License

This project is licensed under the **MIT License** — you are free to use,
copy, modify, and distribute it, as long as the original copyright notice
and this permission notice are included.

See the [LICENSE](LICENSE) file for the full text.

Copyright (c) 2026 Shams Ghobashy, Shahd Khaled
