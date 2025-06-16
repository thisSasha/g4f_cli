import webbrowser, pyperclip, sys, subprocess, os
from g4f_execute import (
    g4f_find,
    g4f_call,
    g4f_get,
    g4f_getAll,
    setup_g4f,
    g4f_setAllModels,
)
from cli import setup_cli, cli_prompt


g4f = None
logger = None

#
# Setup varaibles
#

STYLE_COMMANDS = [
    "help",
    "exit",
    "find",
    "copy",
    "use",
    "echo",
    "get",
    "update",
    "version",
]
DEBUG = False
FILES = {
    "logo": "public/logo.txt",
    "version": "VERSION",
    "help": "public/help.txt",
}
VERSION = open(FILES["version"], "r").read()
FLAG_MAP = {
    "help": {"p": "--type=py", "h": "--type=html"},
    "find": {"p": "--provider", "m": "--model", "a": "--and", "o": "--or"},
    "get": {"p": "--providers", "m": "--models", "a": "--all"},
}
PROMPT_STYLE = {
    "command": "bold",
    "flag": "grey",
}


general_toCopy = []


#
# Setup functions
#


def setup_modules():
    global logger
    logger = setup_cli(PROMPT_STYLE, FLAG_MAP, STYLE_COMMANDS)
    setup_g4f(g4f, logger, print_toCopy, DEBUG)


def setup_checkUpdate():
    pass


def print_toCopy(arr):
    if len(arr) < 1:
        return
    global general_toCopy
    for i, val in enumerate(arr):
        print(f"[{i}]: {val}")
    general_toCopy = []
    general_toCopy = arr
    logger.info('To copy some, type "copy <number>"')


def ensure_g4f():
    global g4f
    if g4f is None:
        import g4f as _g4f

        g4f = _g4f


def command_help(type):
    if type == "html":
        webbrowser.open("https://thisSasha.github.io/g4f_cli")
    elif type == "py":
        print(open(FILES["help"], "r").read())


#
# Main
#


print(open(FILES["logo"], "r").read())
if DEBUG:  # print
    print("\033[93mLoading g4f...\033[0m")
ensure_g4f()
setup_modules()
if DEBUG:  # print
    print("\033[93mSuccessfully loaded\033[0m")
general_allModels = g4f_setAllModels()
interrupt_counter = 0

while True:
    try:
        [args, flags, command] = cli_prompt("g4f > ")
        interrupt_counter = 0
        if command.strip() == "":
            continue
        elif command == "help":
            command_help(flags.get("type", "py"))
        elif command == "echo":
            logger.info(" ".join(args[1:]))
        elif command == "find":
            typeToFind = "provider" if flags.get("provider") else "model"
            keysRule = "or" if flags.get("or") else "and"
            g4f_find(typeToFind, keysRule, args[1:])
        elif command == "copy":
            if args[1].isdigit():
                index = int(args[1])
                if 0 <= index < len(general_toCopy):
                    logger.info("Copied: " + general_toCopy[index])
                    pyperclip.copy(general_toCopy[index])
                else:
                    logger.error("Invalid index")
            else:
                logger.error("Index must be a number")
        elif command == "use":
            useModel = flags.get("model", "default")
            useProvider = flags.get("provider", "BaseProvider")
            useText = args[1]
            g4f_call(useModel, useProvider, useText)
        elif command == "exit":
            break
        elif command == "version":
            logger.info(f"G4F_CLI v{VERSION}")
            logger.info("Author: thisDevSasha")
            logger.info("Source code: https://github.com/thisSasha/g4f_cli")
        elif command == "get":
            entity_type = (
                "providers"
                if flags.get("providers")
                else "models" if flags.get("models") else False
            )
            if flags.get("all", False):
                if entity_type:
                    g4f_getAll(entity_type)
                else:
                    print_toCopy([general_allModels])
            elif entity_type:
                g4f_get(entity_type, args[1])
            else:
                logger.error("Invalid command format. Type 'help' for usage.")
        elif command == "update":
            if flags.get("--only-cli", False):

                continue
            logger.info("Trying to update g4f...")
            process = subprocess.Popen(
                [sys.executable, "-m", "pip", "install", "-U", "g4f"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = process.communicate()
            if "installing packages" in stdout.decode():
                logger.info("g4f updated successfully")
            else:
                logger.info("The latest version of g4f is installed")
        else:
            logger.error('Command not found. Type "help" for a list of commands.')
    except KeyboardInterrupt:
        interrupt_counter += 1
        if interrupt_counter > 1:
            logger.info("For exit, type 'exit'")
    except IndexError as e:
        logger.error("Invalid command format. Type 'help' for usage.")
        logger.debug(str(e))
        logger.debug(
            f"{e.__traceback__.tb_frame.f_code.co_filename.split(os.sep)[-1]}:{e.__traceback__.tb_lineno}"
        )
        continue
    except Exception as e:
        interrupt_counter = 0
        if not DEBUG:
            logger.error(f"Unexpected error: {e}")
        logger.debug(str(e))
        logger.debug(
            f"{e.__traceback__.tb_frame.f_code.co_filename.split(os.sep)[-1]}:{e.__traceback__.tb_lineno}"
        )
