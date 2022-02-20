from os import system as osSystem, name as osName, get_terminal_size as terminalSize
import subprocess

shellVersion = "1.0.0"
shellName = "lonnie"
shellShortFm = "ln"
successEmoji = "✅" # 🎉
errorEmoji = "❗️"
commandHelp = "Run [COMMAND --help] for more information on a command."

currStatus = {
    "session": False,
    "emoji": "💫",
    "memory": 2228,
    "cmdHistory": [],
    "processes": {},
    "readyQ": [],
    "blockedQ": [],
    "ioQ": [],
    "cpu": [],
}

txtColor = {
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
def getRawArg(x):
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return x

def clearConsole():
    _ = osSystem("cls" if osName == "nt" else "clear")

def displayMsg(msg:str):
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
        clr = "\n" * h
        for l in lines:
            print(l)
    else:
        for l in lines[: h - margin]:
            print(l)
        _ = input(
            f"{txtColor['bold']}------- press ENTER to continue -------:{txtColor['reset']} "
        )
        displayMsg("\n".join(lines[h - margin :]))

def getArg(input:str, arg:str, argType:str):
    argTypes = [float, str, int]
    if argType not in argTypes:
        raise ValueError("argType must be float, int or str")

    input = input.split(" ")
    # str in float
    if any(string.startswith(arg) for string in input):
        value = [x for x in input if arg in x][0].split("=")[1]
        raw_value = getRawArg(value)
        return raw_value if isinstance(raw_value, argType) else None
    else:
        return None

def getInput():
    return input(f"{currStatus['emoji']}: ").strip().lower()
