import logging, re
from rich.logging import RichHandler
from prompt_toolkit import prompt
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles import Style
from prompt_toolkit.history import InMemoryHistory

PROMPT_STYLE = None
FLAG_MAP = None
STYLE_COMMANDS = None
args = []
flags = {}

def setup_cli(PROMPT_STYLE_, FLAG_MAP_, STYLE_COMMANDS_):
    setup_logger()
    global FLAG_MAP, STYLE_COMMANDS, PROMPT_STYLE
    PROMPT_STYLE = Style.from_dict(PROMPT_STYLE_)
    FLAG_MAP = FLAG_MAP_
    STYLE_COMMANDS = STYLE_COMMANDS_
    return logger
    


def setup_logger():
    global logger

    logger = logging.getLogger("g4f_cli")
    logger.setLevel(logging.DEBUG)
    rich_handler = RichHandler(markup=True, show_time=False, show_path=False)
    rich_handler.setFormatter(logging.Formatter("%(message)s"))

    logger.handlers = [rich_handler]
    logger.propagate = False

    logging.getLogger("g4f").disabled = True
    logging.getLogger("undetected_chromedriver").disabled = True
    logging.getLogger("urllib3").disabled = True
    logging.getLogger("asyncio").disabled = True
    logging.getLogger("websockets").disabled = True
    logging.getLogger("nodriver").disabled = True
    logging.getLogger("selenium").disabled = True
    return logger


class CommandLexer(Lexer):
    def lex_document(self, document):
        def get_tokens(_):
            text = document.text
            tokens = []

            for cmd in STYLE_COMMANDS:
                if text.startswith(cmd):
                    tokens.append(("class:command", cmd))
                    text = text[len(cmd) :]
                    break

            last_pos = 0
            for match in re.finditer(r"--\S+", text):
                start, end = match.span()
                if start > last_pos:
                    tokens.append(("", text[last_pos:start]))
                tokens.append(("class:flag", text[start:end]))
                last_pos = end

            if last_pos < len(text):
                tokens.append(("", text[last_pos:]))

            return tokens

        return get_tokens


def prompt_processArg(arg, cmd):
    if arg.startswith("--"):
        if "=" in arg:
            flag, value = arg.split("=")
            flags[flag[2:]] = value
        else:
            flags[arg[2:]] = True
    elif arg.startswith("-"):
        mapping = FLAG_MAP.get(cmd, {}).get(arg[1])
        if mapping:
            if "=" in mapping:
                flag, value = mapping.split("=")
                flags[flag[2:]] = value
            else:
                flags[mapping[2:]] = True
        else:
            args.append(arg)
    else:
        args.append(arg)



def prompt_processRequest(request):
    quotes = False
    current_arg = ""

    cmd = request.split(" ")[0]

    for char in request:
        if char == " " and not quotes:
            if current_arg:
                prompt_processArg(current_arg, cmd)
                current_arg = ""
        elif char == '"':
            quotes = not quotes
        else:
            current_arg += char
    if current_arg:
        prompt_processArg(current_arg, cmd)

prompt_history = InMemoryHistory()

def cli_prompt(promt_value):
    global args, flags
    request = prompt(
        promt_value, lexer=CommandLexer(), style=PROMPT_STYLE, history=prompt_history
    )
    args = []
    flags = {}
    prompt_processRequest(request=request)
    command = args[0]
    return [args, flags, command]
