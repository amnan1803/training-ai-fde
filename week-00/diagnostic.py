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

def check_repo_layout() -> bool:
    root = Path(subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True
    ).stdout.strip())
    missing = [f for f in ["README.md", "CLAUDE.md", "week-00"] if not (root / f).exists()]
    ok = not missing
    return auto(
        "Repo layout",
        ok,
        "README.md, CLAUDE.md, and week-00/ all exist" if ok
        else f"missing: {', '.join(missing)}",
    )


def check_python() -> bool:
    v = sys.version_info
    ok = v >= (3, 12)
    return auto("Python 3.12+", ok, f"sys.version_info >= (3, 12)  —  found {v.major}.{v.minor}.{v.micro}")


def check_pip() -> bool:
    ok = shutil.which("pip") is not None or shutil.which("pip3") is not None
    found = "pip" if shutil.which("pip") else ("pip3" if shutil.which("pip3") else "not found")
    return auto("pip", ok, f"pip or pip3 found in PATH  —  {found}")


def check_node() -> bool:
    node = shutil.which("node")
    if not node:
        return auto("Node.js LTS v20+", False, "node not found in PATH")
    result = subprocess.run(["node", "--version"], capture_output=True, text=True)
    version_str = result.stdout.strip().lstrip("v")
    try:
        major = int(version_str.split(".")[0])
        ok = major >= 20
    except ValueError:
        ok = False
    return auto("Node.js LTS v20+", ok, f"node --version major >= 20  —  found v{version_str}")


def check_npm() -> bool:
    ok = shutil.which("npm") is not None
    return auto("npm", ok, "npm --version found in PATH")


def check_git_installed() -> bool:
    ok = shutil.which("git") is not None
    return auto("Git installed", ok, "git --version found in PATH")


def check_git_config() -> bool:
    name  = subprocess.run(["git", "config", "user.name"],  capture_output=True, text=True).stdout.strip()
    email = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True).stdout.strip()
    ok = bool(name and email)
    detail = (
        f"user.name and user.email both set  —  {name} <{email}>"
        if ok
        else "run: git config --global user.name 'Name' && git config --global user.email 'you@example.com'"
    )
    return auto("Git global config", ok, detail)


def check_vscode_cli() -> bool:
    ok = shutil.which("code") is not None
    return auto("VS Code CLI", ok, "code binary found in PATH")


def check_anthropic_key() -> bool:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    ok = bool(key)
    detail = (
        "Env var present  —  set"
        if ok
        else "optional — deferred to a later week"
    )
    return auto("Anthropic API key", ok, detail)


# ----------------------------------------------------------------
# Manual checks (cannot be automated)

def manual_checks() -> None:
    manual("GitHub repo is set to Public",       "Settings -> Danger Zone -> Change visibility")
    manual("Repo URL shared with the program",   "share your github.com/<you>/training-ai-fde link")
    manual("Claude Code CLI installed",          "claude --version should print a version number")


# ----------------------------------------------------------------

def main() -> None:
    print("\nWeek-00 Setup Readiness Diagnostic")
    print("=" * 52)

    print("\n── Automated checks ──────────────────────────────")
    results = [
        check_repo_layout(),
        check_python(),
        check_pip(),
        check_node(),
        check_npm(),
        check_git_installed(),
        check_git_config(),
        check_vscode_cli(),
        check_anthropic_key(),
    ]

    print("\n── Manual checks (cannot be automated) ───────────")
    manual_checks()

    passed = sum(results)
    total  = len(results)
    print(f"\n{'=' * 52}")
    if passed == total:
        print(f"  Automated: {passed}/{total} passed  — all green, you're ready for Week 1 ✅")
    else:
        print(f"  Automated: {passed}/{total} passed  — fix the {total - passed} failing item(s) above, then re-run")
    print()

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
