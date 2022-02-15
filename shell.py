import json
from functions import handleCmds
from utils import shellName,currStatus,txtColor,clearConsole, getInput

def loadMemory():
    try:
        with open('memory.json') as json_file:
            data = json.load(json_file)
            if( isinstance(data["memory"], int) or isinstance(data["memory"], float)):
                currStatus["memory"] = round(data["memory"])
            else:
                print(f"{txtColor['yellow']}Memory value must be a number (memory.json). Using fallback memory allocation.{txtColor['reset']}")
    except FileNotFoundError:
        print(f"{txtColor['yellow']}Memory file (memory.json) not found. Using fallback memory allocation.{txtColor['reset']}")
    except Exception as err:
        print(f"{txtColor['yellow']}Error reading memory file (memory.json). Using fallback memory allocation - [{err}]{txtColor['reset']}")

def welcomeMsg():
    print(f"\nWelcome to the {shellName.lower()} shell 🥳🎉🥳🎉🥳🎉🥳🎉\n--------------------------------------------\nMemory: {currStatus['memory']} MB | For more details enter 'help'.\n")

def runShell():
    currStatus["isRunning"] = True
    clearConsole() 
    loadMemory()
    welcomeMsg() 

    while currStatus["isRunning"]:
        input = getInput()
        handleCmds(input)

# only execute shell when this file is being run directly
if __name__ == '__main__':
    runShell()

