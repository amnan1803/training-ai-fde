# Week 0 Diagnostic

## 1. Coding warm-up

**Function:** `run_length_encode(s)` in `solution.py`  
Compresses a string into `(character, count)` pairs. Example: `"aabbbcc"` → `[("a",2),("b",3),("c",2)]`.

**Tests:** `test_solution.py` (5 cases — basic, empty, no repeats, all-same, single char)

```
python -m pytest week-00/test_solution.py -v
# 5 passed in 0.05s
```

---

## 2. GitHub operation — branch and commit

Work for this diagnostic was done on a dedicated branch and merged back to `main`:

```bash
git checkout -b week-00/diagnostic      # create branch
# ... write files ...
git add week-00/
git commit -m "Add week-00 diagnostic"
git checkout main
git merge week-00/diagnostic --no-ff
git push origin main
```

Verification: `git log --oneline -3` shows the merge commit on `main`.

---

## 3. Command-line task — navigate, run a script, read an env var

```bash
# navigate
cd training-ai-fde/week-00

# run a script
python -m pytest test_solution.py -v

# set and read an environment variable
export TRAINING_NAME=amnansani          # bash
$env:TRAINING_NAME = "amnansani"        # PowerShell

python env_check.py
# TRAINING_NAME=amnansani
```

`env_check.py` reads `TRAINING_NAME` via `os.environ.get()` and prints it.

---

## 4. Function read — what does this do, what would break it?

```python
def mystery(n):
    seen = set()
    x = n
    while x not in seen:
        seen.add(x)
        x = sum(int(d) ** 2 for d in str(x))
    return x == 1
```

**What it does:**  
Checks whether `n` is a *happy number*. Starting from `n`, it repeatedly replaces the value with the sum of the squares of its digits. If that sequence eventually reaches `1`, the number is happy and the function returns `True`. If the sequence enters a cycle that never reaches `1`, the `seen` set catches the repeated value and the function returns `False`. The `while` loop always terminates for positive integers because every cycle is finite.

**What would break it:**

- **Negative input** — `str(-5)` is `"-5"`, so the generator tries `int("-")` and raises `ValueError`.
- **Non-integer input** — `str(3.14)` is `"3.14"`; `int(".")` raises `ValueError`.
- **Zero** — `str(0)` is `"0"`, which works mechanically (`0² = 0`), but the sequence immediately cycles (`0 → 0`), so the function returns `False`. That may or may not be the intended behaviour depending on the caller's contract.
