# Codebreaker

A terminal version of the classic code-breaking game Mastermind, written in
Python.

The computer hides a secret code made of digits. You guess it, and after each
guess you are told two numbers:

- **exact** — how many digits are the right digit in the right place
- **close** — how many are the right digit, but in the wrong place

You are never told *which* ones. Narrowing the code down from those two numbers
is the whole game. It takes seconds to learn and is hard to put down.

```
    #    guess          exact        close
   ---  -----------   ---------    ---------
    1    1 2 3 4              1            1
    2    5 6 1 2              0            2
    3    6 1 3 3              4            0

  Cracked it in 3 guesses.
```

## Prerequisites

Python 3. Nothing to install — the game uses only the Python standard library.

macOS and most Linux systems already have Python 3. On Windows you may need to
install it from [python.org](https://www.python.org/downloads/).

To check:

```
python3 --version
```

Any version starting with `3.` will work.

## Getting the code

**Download (no tools needed):** click the green **Code** button at the top of
this page, choose **Download ZIP**, then unzip it.

**Clone (requires Git):**

```
git clone https://github.com/YOUR-USERNAME/Codebreaker.git
```

## How to run the game

### macOS

Open Terminal, move into the project folder, then start the game:

```
cd ~/Downloads/Codebreaker-main
python3 codebreaker.py
```

Adjust the first line if the folder is somewhere else or unzipped under a
different name. A shortcut that avoids typing the path: right-click the folder
in Finder and choose **Services → New Terminal at Folder**. The terminal opens
already inside it, so you can go straight to `python3 codebreaker.py`.

The command is `python3`, not `python`. macOS no longer ships a plain `python`
command, so `python` gives you `command not found`.

The first time you run it, macOS may offer to install the command line
developer tools. Click **Install**, wait for it to finish, then run the command
again.

### Windows

Open Command Prompt or PowerShell:

```
cd %USERPROFILE%\Downloads\Codebreaker-main
py codebreaker.py
```

Use `py` on Windows. If that isn't recognised, try `python codebreaker.py`.

A shortcut: open the folder in File Explorer, click the address bar, type
`cmd`, and press Enter. The terminal opens in that folder.

### Linux

```
cd ~/Downloads/Codebreaker-main
python3 codebreaker.py
```

## How to play

Pick a difficulty at the start, or press Enter to take the default.

| Level | Code length | Digits | Guesses | Repeated digits |
| --- | --- | --- | --- | --- |
| gentle | 3 | 1–6 | 10 | not used |
| standard | 4 | 1–6 | 10 | possible |
| hard | 5 | 1–8 | 12 | possible |

Type your guess as digits and press Enter. Both `1234` and `1 2 3 4` are
accepted. Type `q` to give up and reveal the code.

A useful opening on *standard* is something like `1 1 2 2` — it tells you how
many 1s and 2s are in the code before you worry about position. From there,
change one digit at a time and watch how the two numbers move. On levels where
digits can repeat, remember that a code may contain the same digit more than
once.
