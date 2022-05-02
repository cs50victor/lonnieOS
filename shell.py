"""
    A Command Line Interface (CLI) connects a user to a computer program or operating system. 
    Through the CLI, users interact with a system or application by typing in text (commands). 
"""
import os
from main import (
    lonnieOS,
    getInput,
    shellName,
    handleCmds,
    shellStatus,
    clearConsole,
    shellVersion,
    shellTextColor,
    printWarningMsg,
)


def loadMemory() -> None:
    # * Sets the system's memory by reading the memory.json file.
    # * Uses a fallback value if unsuccessful.
    try:
        lonnieOS.setSystemMemoryFromFile()
    except Exception as err:
        printWarningMsg(f"{err}")


def welcomeMsg() -> None:
    # * Displays a welcome message containing the
    # * system memory, shell name and shell version.

    print(
        f"""
                     █  
     ▄█▄ █▀█▀█ ▄█▄   █  {shellTextColor["bold"]}{shellName.upper()} v{shellVersion}{shellTextColor["reset"]}
     ▀▀███▄█▄████▀   █  RAM: {lonnieOS.getSystemMemory()} MB.
         ▀█▀█▀       █  for more details enter 'help'.
    """
    )


def runShell() -> None:
    # * Receives and handles all shell commands until the program is exited.

    shellStatus["isRunning"] = True
    clearConsole()
    # run all tests
    os.system("python -m unittest discover -s tests -t tests")
    loadMemory()
    # display welcome message
    welcomeMsg()

    while shellStatus["isRunning"]:
        input = getInput()
        handleCmds(input)


# only execute shell when this file is being run directly
if __name__ == "__main__":
    runShell()
