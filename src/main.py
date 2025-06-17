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
from abc import ABC, abstractmethod


g4f = None
logger = None

#
# Setup varaibles
#

STYLE_COMMANDS = []
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
    logger = setup_cli(PROMPT_STYLE, FLAG_MAP, STYLE_COMMANDS, DEBUG)
    setup_g4f(g4f, logger, print_toCopy, DEBUG)


def setup_checkUpdate():
    pass


def print_toCopy(arr):
    if len(arr) < 1:
        return
    global general_toCopy
    for i, val in enumerate(arr):
        print(f"[\033[93m{i}\033[0m]: {val}\033[0m")
    general_toCopy = []
    general_toCopy = arr
    logger.info('To copy some, type "copy <number>"')


def ensure_g4f():
    global g4f
    if g4f is None:
        import g4f as _g4f

        g4f = _g4f


#
# CommandsFactory
#


class Command(ABC):
    @abstractmethod
    def execute(self, args, flags, command):
        pass


class CommandsFactory:
    def __init__(self):
        self.commands = {}

    def get(self, name):
        return self.commands.get(name)

    # Decorator
    def register(self, name):
        def decorator(func):
            self.commands[name] = func
            return func

        return decorator


commandFactory = CommandsFactory()


@commandFactory.register("help")
class CommandHelp:
    name = "help"

    def execute(args, flags):
        type = flags.get("type", "py")
        if type == "html":
            webbrowser.open("https://thisSasha.github.io/g4f_cli")
        elif type == "py":
            print(open(FILES["help"], "r").read())


@commandFactory.register("exit")
class CommandExit:
    name = "exit"

    def execute(args, flags):
        sys.exit(0)


@commandFactory.register("find")
class CommandFind:
    name = "find"

    def execute(args, flags):
        typeToFind = "provider" if flags.get("provider") else "model"
        keysRule = "or" if flags.get("or") else "and"
        g4f_find(typeToFind, keysRule, args[1:])


@commandFactory.register("copy")
class CommandCopy:
    name = "copy"

    def execute(args, flags):
        if len(args) < 2 or not args[1].isdigit():
            logger.error("Invalid command format. Type 'help' for usage.")
            return

        index = int(args[1])
        if 0 <= index < len(general_toCopy):
            logger.info("Copied: " + general_toCopy[index])
            pyperclip.copy(general_toCopy[index])
        else:
            logger.error("Invalid index")


@commandFactory.register("use")
class CommandUse:
    name = "use"

    def execute(args, flags):
        if len(args) < 2:
            logger.error("Invalid command format. Type 'help' for usage.")
            return

        useModel = flags.get("model", "default")
        useProvider = flags.get("provider", "BaseProvider")
        useText = args[1]
        g4f_call(useModel, useProvider, useText)


@commandFactory.register("echo")
class CommandEcho:
    name = "echo"

    def execute(args, flags):
        logger.info(" ".join(args[1:]))


@commandFactory.register("get")
class CommandGet:
    name = "get"

    def execute(args, flags):
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
        elif entity_type and len(args) > 1:
            g4f_get(entity_type, args[1])
        else:
            logger.error("Invalid command format. Type 'help' for usage.")


@commandFactory.register("update")
class CommandUpdate:
    name = "update"

    def execute(args, flags):
        if flags.get("only-cli", False):
            logger.info("Updating g4f_cli...")
            process = subprocess.Popen(
                [sys.executable, "-m", "pip", "install", "-U", "."],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.dirname(os.path.dirname(__file__)),
            )
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                logger.info("g4f_cli updated successfully. Please restart the CLI.")
            else:
                logger.error(f"Failed to update g4f_cli: {stderr.decode()}")
            return

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


@commandFactory.register("version")
class CommandVersion:
    name = "version"

    def execute(args, flags):
        logger.info(f"G4F_CLI v{VERSION}")
        logger.info("Author: thisDevSasha")
        logger.info("Source code: https://github.com/thisSasha/g4f_cli")


#
# Main
#


print(open(FILES["logo"], "r").read())
if DEBUG:  # print
    print("\033[93mLoading g4f...\033[0m")
ensure_g4f()
if DEBUG:  # print
    print("\033[93mSuccessfully loaded\033[0m")
STYLE_COMMANDS = commandFactory.commands.keys()
setup_modules()
general_allModels = g4f_setAllModels()
interrupt_counter = 0

while True:
    try:
        [args, flags, command] = cli_prompt("g4f > ")
        interrupt_counter = 0
        if command.strip() == "":
            continue
        cmd = commandFactory.get(command)
        if cmd:
            cmd.execute(args, flags)
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
