from typing import Union, Type
from os import system as osSystem, name as osName, get_terminal_size as terminalSize

# shell details
shellVersion = "1.0.0"
shellName = "lonnie 👨🏻"
shellShortFm = "ln"
successEmoji = "🎉"  # ✅
errorEmoji = "❗️"
commandHelp = "Run [COMMAND --help] for more information on a command."
shellStatus = {
    "isRunning": False,
    "emoji": "⚡️",
    "cmdHistory": [],
}

# for displaying colorful messages
shellTextColor = {
    "header": "\033[95m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "reset": "\033[0m",
    "bold": "\033[1m",
    "underline": "\033[4m",
}

# * ------------- SHELL UTILITY FUNCTIONS -------------
# These functions are used to get and show text input
# to and from the user through the shell.


def getRawArg(x)->Union[int, float, str]:
    # Returns the real datatype of a variable
    # returns a float, integer or string

    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return x.lower()

def getInput() -> str:
    # Returns the user input from the shell

    return input(f"\n{shellStatus['emoji']} : ").strip().lower()


def clearConsole() -> None:
    # clears the shell

    _ = osSystem("cls" if osName == "nt" else "clear")


def getArg(input: str, arg: str, argType: Union[Type[str], Type[int], Type[float]]):
    # ensures that the user enters the correct datatype for a shell command argument

    argTypes = [float, str, int]
    if argType not in argTypes:
        raise ValueError("argType must be float, int or str")

    args = input.split(" ")

    if any(string.startswith(f"{arg}=") for string in args):
        value = [x for x in args if arg in x][0].split("=")[1]
        raw_value = getRawArg(value)
        if not isinstance(raw_value, argType):
            if isinstance(raw_value, int) and argType == float:
                raw_value = float(raw_value)
            else:
                raw_value = None

        assert isinstance(raw_value, argType) or raw_value is None
        return raw_value
    else:
        return None


def displayMsg(msg: str) -> None:
    # Displays a message using the size of the shell,
    # asks the user for confirmation to print more messages if the
    # displayed message is the height of the shell

    w, h = terminalSize()

    lines = []
    breaks = msg.split("\n")
    for b in breaks:
        if b:
            lines.extend([b[i : i + w] for i in range(0, len(b), w)])
        else:
            lines.append(b)
    margin = 2
    numOfLines = len(lines)
    if numOfLines < h - margin:
        for l in lines:
            print(l)
    else:
        for l in lines[: h - margin]:
            print(l)
        _ = input(
            f"{shellTextColor['bold']}------- press ENTER to continue -------:{shellTextColor['reset']} "
        )
        displayMsg("\n".join(lines[h - margin :]))


def cpuMethodChoice(prompt: str, minNum: int, maxNum: int) -> int:
    # gets the user's choice for which cpu execution method to use

    prevEmoji = shellStatus["emoji"]
    shellStatus["emoji"] = f"{prompt} [{minNum}-{maxNum}]"
    userInput = "--value=" + getInput()
    value = getArg(userInput, "--value", int)

    while not value or (value > maxNum or value < minNum):  # type: ignore
        print("Error, invalid input!")
        userInput = "--value=" + getInput()
        value = getArg(userInput, "--value", int)

    shellStatus["emoji"] = prevEmoji
    assert isinstance(value, int)
    return value


def underlineMsg(msg: str) -> str:
    # prints an underlined message to the shell

    return f"\n{shellTextColor['underline']}{msg}{shellTextColor['reset']}\n"


def printErrorMsg(msg: str) -> None:
    # prints an error message to the shell

    print(f"\n{errorEmoji} {msg}\n")


def printSuccessMsg(msg: str) -> None:
    # prints a message with a success emoji to the shell

    print(f"\n{successEmoji} {msg}\n")


def printWarningMsg(msg: str) -> None:
    # prints a yellow message to the shell

    print(f"\n{shellTextColor['yellow']}{msg}{shellTextColor['reset']}\n")
