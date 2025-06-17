# Gpt4Free CLI (g4f\_cli)

[**G4F Repository**](https://github.com/techwithanirudh/g4f?tab=readme-ov-file)

![Gpt4Free CLI Banner](/public/banner.svg)

## ✨ Overview

Gpt4Free CLI is a lightweight Python-based command-line interface for the [g4f](https://pypi.org/project/g4f/) library.
It simplifies browsing models and providers, sending requests, and receiving responses, while offering concise logging. Perfect for exploring the g4f library.

## 🚀 Features

Gpt4Free CLI supports all current models and providers from the `g4f` library. The `get` and `find` commands let you conveniently retrieve available options and search by keywords.

Stream support and real-time log capture allow you to monitor browser launch delays, failures, and hangs. In `DEBUG` mode, a log file `.log` is created (capturing nodriver, urllib3, and other logs).

Colorized output is implemented via `rich.logging`. You can also quickly copy results to the clipboard by index using the `copy` command.

The project is lightweight and free of unnecessary dependencies. Command history is retained within the current session. All commands have a well-thought-out structure and are easy to extend.

## ⚙️ Installation

```bash
git clone https://github.com/thisSasha/g4f_cli.git
cd g4f_cli
python3 -m venv .venv
source .venv/bin/activate      # Linux & macOS
.\.venv\Scripts\activate       # Windows PowerShell
pip install -r requirements.txt
```

> [Dependencies](https://github.com/thisSasha/g4f_cli/blob/main/requirements.txt)
> [Entry Point](https://github.com/thisSasha/g4f_cli/blob/main/src/main.py)
> [Source](https://github.com/thisSasha/g4f_cli/tree/main/src)

## ▶️ Usage

Launch the CLI:

```bash
chmod +x ./run.sh
./run.sh     # Linux & macOS
.\run.bat    # Windows
```

You'll see the prompt:

```text
g4f > 
```

> **Example Commands**
>
> ```bash
> g4f > find --provider open ai
> g4f > use --model=gpt_4 --provider=BaseProvider "Hello, world"
> g4f > get --all models
> g4f > copy 2
> g4f > version
> ```

---

## 🏗️ Architecture

```
.
├── public/
│   ├── help.txt          # (optional HTML help page)
│   └── logo.txt          # ASCII logo
├── requirements.txt
├── VERSION               # Current CLI version
├── src/
│   ├── main.py           # Entry point and REPL loop
│   ├── cli.py            # prompt-toolkit logic, flag parsing
│   └── g4f_execute.py    # Core actions: find, call, get, update
└── run.{sh|bat}      # Launch scripts
```

* `main.py` initializes the environment and handles commands
* `cli.py` implements command parsing, flags, and history
* `g4f_execute.py` calls `g4f.ChatCompletion` and processes output

## 📄 Info

> **Author:** thisDevSasha  <br/>
> **Repository:** [https://github.com/thisSasha/g4f\_cli](https://github.com/thisSasha/g4f_cli)  <br/>
> **Report an Issue:** [https://github.com/thisSasha/g4f\_cli/issues](https://github.com/thisSasha/g4f_cli/issues)  <br/>
> **License:** [GPL v3](https://github.com/thisSasha/g4f\_cli/blob/main/LICENSE)  <br/>
