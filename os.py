from functions import *

def runShell():
    currStatus["isRunning"] = True
    clearConsole()
    welcomeMsg()
    # assert 8<4,"List is empty."

    while currStatus["isRunning"]:
        input = getInput()
        handleCmds(input)

# only execute shell when this file is being run directly
if __name__ == '__main__':
    runShell()

