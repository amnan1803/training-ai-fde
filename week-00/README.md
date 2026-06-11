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
