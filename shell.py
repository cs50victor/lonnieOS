import json, os, subprocess
from main import handleCmds
from utils import shellName, currStatus, txtColor, clearConsole, getInput, shellVersion


def loadMemory():
    try:
        with open("memory.json") as json_file:
            data = json.load(json_file)
            if isinstance(data["memory"], int) or isinstance(data["memory"], float):
                currStatus["memory"] = round(data["memory"])
            else:
                print(
                    f"{txtColor['yellow']}Memory value must be a number (memory.json). Using fallback memory allocation.{txtColor['reset']}"
                )
    except FileNotFoundError:
        print(
            f"{txtColor['yellow']}Memory file (memory.json) not found. Using fallback memory allocation.{txtColor['reset']}"
        )
    except Exception as err:
        print(
            f"{txtColor['yellow']}Error reading memory file (memory.json). Using fallback memory allocation - [{err}]{txtColor['reset']}"
        )


def welcomeMsg():
    w = (os.get_terminal_size().columns) - 10
    leftMargin = " " * 10
    border = f"-|------------------------------------------------------|-"
    lines = [
        " ",
        f"{shellName.upper()} v{shellVersion}",
        f"Memory: {currStatus['memory']} MB. for more details enter 'help'.",
        " ",
    ]
    print(f"{leftMargin}{border}")
    for line in lines:
        print(f"{leftMargin} |{line.center(len(border)-4)}|")
    print(f"{leftMargin}{border}")


def runShell():
    currStatus["session"] = True
    clearConsole()
    os.system("python -m unittest discover -s tests -t tests")
    loadMemory()
    welcomeMsg()

    while currStatus["session"]:
        input = getInput()
        handleCmds(input)


# only execute shell when this file is being run directly
if __name__ == "__main__":
    runShell()
