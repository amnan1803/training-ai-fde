"""
Week-00 Setup Readiness Diagnostic
Checks every item in the pre-Week-1 setup checklist.
Run:  python week-00/diagnostic.py
"""

import io
import os
import shutil
import subprocess
import sys
from pathlib import Path

# ensure UTF-8 output on Windows terminals
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PASS   = "✅ "
FAIL   = "❌ "
MANUAL = "⚠️  "


def _print(icon: str, status: str, label: str, detail: str = "") -> None:
    suffix = f"  ({detail})" if detail else ""
    print(f"  {icon}{status}  {label}{suffix}")


def auto(label: str, ok: bool, detail: str = "") -> bool:
    _print(PASS if ok else FAIL, "PASS" if ok else "FAIL", label, detail)
    return ok


def manual(label: str, hint: str = "") -> None:
    _print(MANUAL, "MANUAL", label, hint)


# ----------------------------------------------------------------
# Automated checks

def check_python() -> bool:
    v = sys.version_info
    ok = v >= (3, 10)
    return auto("Python ≥ 3.10", ok, f"found {v.major}.{v.minor}.{v.micro}")


def check_git_installed() -> bool:
    ok = shutil.which("git") is not None
    return auto("git is installed", ok)


def check_git_identity() -> bool:
    name  = subprocess.run(["git", "config", "user.name"],  capture_output=True, text=True).stdout.strip()
    email = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True).stdout.strip()
    ok = bool(name and email)
    detail = f"{name} <{email}>" if ok else "run: git config --global user.name / user.email"
    return auto("git identity configured", ok, detail)


def check_git_repo() -> bool:
    result = subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, text=True)
    ok = result.returncode == 0
    return auto("inside a git repository", ok)


def check_remote_origin() -> bool:
    result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
    url = result.stdout.strip()
    ok = result.returncode == 0 and "github.com" in url
    return auto("GitHub remote origin set", ok, url or "none found")


def check_repo_public_name() -> bool:
    result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
    url = result.stdout.strip()
    ok = "training-ai-fde" in url
    return auto("repo named training-ai-fde", ok, url)


def check_gitignore() -> bool:
    root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                               capture_output=True, text=True).stdout.strip())
    ok = (root / ".gitignore").exists()
    return auto(".gitignore present at repo root", ok)


def check_no_env_in_git() -> bool:
    result = subprocess.run(
        ["git", "ls-files", "*.env", ".env"],
        capture_output=True, text=True
    )
    tracked = result.stdout.strip()
    ok = not tracked
    return auto("no .env files tracked in git", ok, tracked if tracked else "clean")


def check_week00_folder() -> bool:
    root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                               capture_output=True, text=True).stdout.strip())
    ok = (root / "week-00").is_dir()
    return auto("week-00/ folder exists", ok)


def check_weekly_folders() -> bool:
    root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                               capture_output=True, text=True).stdout.strip())
    missing = [f"week-{i:02d}" for i in range(13) if not (root / f"week-{i:02d}").is_dir()]
    ok = not missing
    return auto("week-00 … week-12 folders present", ok,
                f"missing: {', '.join(missing)}" if missing else "all 13 present")


def check_readme_index() -> bool:
    root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                               capture_output=True, text=True).stdout.strip())
    readme = root / "README.md"
    ok = readme.exists() and "week-00" in readme.read_text(encoding="utf-8").lower()
    return auto("README.md exists and references week-00", ok)


def check_claude_md() -> bool:
    root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                               capture_output=True, text=True).stdout.strip())
    ok = (root / "CLAUDE.md").exists()
    return auto("CLAUDE.md stub present at repo root", ok)


def check_env_var_awareness() -> bool:
    # Just checks the user knows how to read one — we look for any non-empty var
    sample = os.environ.get("TRAINING_NAME", "")
    ok = bool(sample)
    detail = f"TRAINING_NAME={sample}" if ok else "set with: $env:TRAINING_NAME='yourname' (PowerShell)"
    return auto("TRAINING_NAME env var readable", ok, detail)


# ----------------------------------------------------------------
# Manual checks (cannot be auto-verified)

def manual_checks() -> None:
    manual("GitHub account is public",          "check: github.com/<you> — profile visible when logged out")
    manual("Repo is set to Public",             "Settings → Danger Zone → Change visibility")
    manual("VS Code (or editor) installed",     "code --version should print a version number")
    manual("Claude Code CLI installed",         "claude --version should print a version number")
    manual("Submission link sent to program",   "share your github.com/<you>/training-ai-fde URL")


# ----------------------------------------------------------------

def main() -> None:
    print("\nWeek-00 Setup Readiness Diagnostic")
    print("=" * 52)

    print("\n── Automated checks ──────────────────────────────")
    results = [
        check_python(),
        check_git_installed(),
        check_git_identity(),
        check_git_repo(),
        check_remote_origin(),
        check_repo_public_name(),
        check_gitignore(),
        check_no_env_in_git(),
        check_week00_folder(),
        check_weekly_folders(),
        check_readme_index(),
        check_claude_md(),
        check_env_var_awareness(),
    ]

    print("\n── Manual checks (verify yourself) ───────────────")
    manual_checks()

    passed = sum(results)
    total  = len(results)
    print(f"\n{'=' * 52}")
    print(f"  Automated: {passed}/{total} passed", end="")
    if passed == total:
        print("  — all green, you're ready for Week 1 ✅")
    else:
        print(f"  — fix the {total - passed} failing item(s) above, then re-run")
    print()


if __name__ == "__main__":
    main()
