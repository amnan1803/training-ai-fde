# Week 0 — Setup and Diagnostic

Submission for the Phase 0 calibration diagnostic.

## 1. Coding warm-up

**File:** `diagnostic.py`

A setup readiness checker that validates every item in the pre-Week-1 checklist and exits non-zero if any automated check fails.

**Automated checks:**

| Check | What it verifies |
| --- | --- |
| Repo layout | `README.md`, `CLAUDE.md`, and `week-00/` all exist |
| Python 3.12+ | `sys.version_info >= (3, 12)` |
| pip | `pip` or `pip3` found in PATH |
| Node.js LTS v20+ | `node --version` major ≥ 20 |
| npm | `npm --version` found in PATH |
| Git installed | `git --version` found in PATH |
| Git global config | `user.name` and `user.email` both set |
| VS Code CLI | `code` binary found in PATH |
| Anthropic API key | Env var present (optional — deferred to a later week) |

**Manual checks listed (cannot be automated):**

- GitHub repo is set to Public
- Repo URL shared with the program
- Claude Code CLI installed

**Run:**

```bash
python week-00/diagnostic.py
```

---

## 2. GitHub operation — branch and commit

Created a feature branch, committed the diagnostic work, then merged back to `main`:

```bash
git checkout -b week-00/diagnostic   # create branch
# ... write files ...
git add week-00/
git commit -m "Add week-00 diagnostic"
git checkout main
git merge week-00/diagnostic --no-ff
git push origin main
```

Verification: `git log --oneline -5` shows the merge commit on `main`.

---

## 3. Command-line task

Navigate to the repo, run the diagnostic script, and read an environment variable:

```bash
# navigate
cd training-ai-fde

# run the script
python week-00/diagnostic.py

# set and read an environment variable
export ANTHROPIC_API_KEY=your_key_here        # bash / zsh
$env:ANTHROPIC_API_KEY = "your_key_here"      # PowerShell

echo $ANTHROPIC_API_KEY                       # bash
$env:ANTHROPIC_API_KEY                        # PowerShell
```

The diagnostic reads `ANTHROPIC_API_KEY` via `os.environ.get()` and reports PASS if it is set.

---

## 4. Function read — `shutil.which`

```python
shutil.which("git")
```

**What it does:**
Searches the directories listed in the `PATH` environment variable for an executable named `"git"` (or whatever name is passed). Returns the full absolute path to the executable if found (e.g. `"/usr/bin/git"` on Linux or `"C:\Program Files\Git\cmd\git.exe"` on Windows), or `None` if no matching executable exists in PATH. It also checks that the file is actually executable, not just present.

**Used in `diagnostic.py`** to auto-detect installed tools — e.g. `shutil.which("git") is not None` is the check behind the *Git installed* row.

**What would break it:**

- `PATH` is empty or unset — `which` has nowhere to search and returns `None` for everything.
- The executable exists on disk but lacks execute permission — `which` skips it and returns `None`.
- `None` is passed as the name — raises `TypeError`.
