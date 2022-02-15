from os import system as osSystem, name as osName, get_terminal_size as terminalSize

shellName = "lonnie"
shellShortFm = "ln"
successEmoji = "🎉"
errorEmoji = "❗️"
commandHelp = "Run COMMAND --help for more information on a command."

currStatus = {
    "isRunning": False,
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


def clearConsole():
    _ = osSystem("cls") if osName == "nt" else osSystem("clear")


def getArg(input, arg):
    input = input.split(" ")

    if any(arg in string for string in input):
        return [x for x in input if arg in x][0].split("=")[1]
    else:
        return None


def displayMsg(msg):
    w, h = terminalSize()
    shellArea = w * h

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
            f"{txtColor['bold']}------- press any key to continue -------:{txtColor['reset']} "
        )
        displayMsg("\n".join(lines[h - margin :]))


def getInput():
    return input(f"{currStatus['emoji']}: ").strip().lower()
