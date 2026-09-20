#!/usr/bin/env python3
"""
Codebreaker - a terminal version of the classic Mastermind game.

The computer hides a secret code made of digits. You guess the code, and
after each guess the computer tells you two things:

    exact  - how many digits are the right digit in the right place
    close  - how many are the right digit in the wrong place

You are not told which ones. Working out the code from those two numbers
is the whole game.

Run it with:  python3 codebreaker.py
"""

import json
import os
import random
import sys
from pathlib import Path

# Look for settings.json next to this script, so the game works no matter
# which folder you happen to run it from.
SETTINGS_PATH = Path(__file__).resolve().parent / "settings.json"

# Used only if settings.json is missing or unreadable, so the game still runs.
FALLBACK = {
    "default": "standard",
    "levels": {
        "gentle": {"length": 3, "symbols": 6, "attempts": 10, "repeats": False},
        "standard": {"length": 4, "symbols": 6, "attempts": 10, "repeats": True},
        "hard": {"length": 5, "symbols": 8, "attempts": 12, "repeats": True},
    },
}


# ----------------------------------------------------------------------
# Terminal colour
# ----------------------------------------------------------------------

if sys.platform == "win32":
    os.system("")          # switches on colour support in Windows terminals

USE_COLOUR = sys.stdout.isatty()

CODES = {
    "bold": "\033[1m", "dim": "\033[2m", "green": "\033[32m",
    "yellow": "\033[33m", "cyan": "\033[36m", "red": "\033[31m",
}


def paint(text, *styles):
    """Wrap text in colour codes, unless output isn't a real terminal."""
    if not USE_COLOUR:
        return str(text)
    prefix = "".join(CODES[s] for s in styles)
    return f"{prefix}{text}\033[0m"


# ----------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------

def load_settings():
    """Read the difficulty levels from settings.json."""
    try:
        with open(SETTINGS_PATH, encoding="utf-8") as fh:
            data = json.load(fh)
        levels = data["levels"]
        if not levels:
            raise KeyError("levels")
        return levels, data.get("default", next(iter(levels)))
    except (OSError, json.JSONDecodeError, KeyError, StopIteration):
        print(paint("Could not read settings.json - using built-in defaults.\n", "dim"))
        return FALLBACK["levels"], FALLBACK["default"]


def choose_level(levels, default):
    """Ask which difficulty to play. Enter alone accepts the default."""
    names = list(levels)

    print(paint("Difficulty", "bold"))
    for number, name in enumerate(names, 1):
        s = levels[name]
        repeats = "repeats allowed" if s.get("repeats", True) else "no repeats"
        print(f"  {number}. {name:<9} {s['length']} digits from 1-{s['symbols']}, "
              f"{s['attempts']} guesses, {repeats}")

    prompt = f"\nPick 1-{len(names)}, or press Enter for {default}: "
    while True:
        answer = input(prompt).strip().lower()
        if not answer and default in levels:
            return default, levels[default]
        if answer.isdigit() and 1 <= int(answer) <= len(names):
            name = names[int(answer) - 1]
            return name, levels[name]
        if answer in levels:
            return answer, levels[answer]
        print(paint("  Not one of the options - try again.", "red"))


# ----------------------------------------------------------------------
# Game logic
# ----------------------------------------------------------------------

def make_code(setting):
    """Build a random secret code as a list of digit characters."""
    digits = [str(d) for d in range(1, setting["symbols"] + 1)]
    if setting.get("repeats", True):
        return [random.choice(digits) for _ in range(setting["length"])]
    return random.sample(digits, setting["length"])


def score(secret, guess):
    """Compare a guess against the secret.

    Returns (exact, close). A digit counted as exact is never also counted
    as close, which is what makes repeated digits score correctly.
    """
    exact = sum(s == g for s, g in zip(secret, guess))
    shared = sum(min(secret.count(d), guess.count(d)) for d in set(guess))
    return exact, shared - exact


def read_guess(setting):
    """Ask for one guess and check it before returning it.

    Returns a list of digits, or None if the player wants to give up.
    """
    length, symbols = setting["length"], setting["symbols"]

    while True:
        raw = input(paint("  your guess: ", "cyan")).strip().lower()

        if raw in ("q", "quit", "exit"):
            return None
        # Spaces are allowed, so both "1234" and "1 2 3 4" work.
        cleaned = raw.replace(" ", "")

        if len(cleaned) != length:
            print(paint(f"  Needs to be exactly {length} digits.", "red"))
            continue
        if not cleaned.isdigit():
            print(paint("  Digits only.", "red"))
            continue
        if any(not 1 <= int(d) <= symbols for d in cleaned):
            print(paint(f"  Use digits from 1 to {symbols} only.", "red"))
            continue

        return list(cleaned)


def show_row(number, guess, exact, close):
    """Print one line of the scoreboard."""
    spaced = " ".join(guess)
    print(f"   {number:>2}    {spaced:<12}"
          f"{paint(exact, 'green', 'bold'):>10}"
          f"{paint(close, 'yellow'):>13}")


def play_round(setting):
    """Play a single game. Returns the number of guesses used, or None if lost."""
    secret = make_code(setting)
    attempts = setting["attempts"]

    print()
    print(f"  A {setting['length']}-digit code is hidden. "
          f"You have {attempts} guesses.")
    print(paint("  Type q at any time to give up.\n", "dim"))
    print(paint("    #    guess          exact        close", "bold"))
    print(paint("   ---  -----------   ---------    ---------", "dim"))

    for turn in range(1, attempts + 1):
        guess = read_guess(setting)
        if guess is None:
            print(f"\n  The code was {paint(' '.join(secret), 'bold')}.\n")
            return None

        exact, close = score(secret, guess)
        show_row(turn, guess, exact, close)

        if exact == setting["length"]:
            print()
            print(paint(f"  Cracked it in {turn} "
                        f"{'guess' if turn == 1 else 'guesses'}.", "green", "bold"))
            print()
            return turn

    print()
    print(paint("  Out of guesses.", "red"))
    print(f"  The code was {paint(' '.join(secret), 'bold')}.\n")
    return None


def ask_again():
    answer = input("  Play again? [Y/n] ").strip().lower()
    return answer in ("", "y", "yes")


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    levels, default = load_settings()

    print()
    print(paint("  CODEBREAKER", "bold", "cyan"))
    print(paint("  Guess the hidden code. After each guess you are told how many", "dim"))
    print(paint("  digits are exactly right, and how many are the right digit in", "dim"))
    print(paint("  the wrong place. You are not told which.\n", "dim"))

    name, setting = choose_level(levels, default)

    played = 0
    won = 0
    best = None

    while True:
        result = play_round(setting)
        played += 1
        if result is not None:
            won += 1
            if best is None or result < best:
                best = result

        if not ask_again():
            break

    print()
    print(f"  {won} solved out of {played} on {name}.", end="")
    if best:
        print(f"  Best: {best} {'guess' if best == 1 else 'guesses'}.")
    else:
        print()
    print()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n  Stopped.\n")
