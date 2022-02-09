import os, platform
from datetime import datetime

shellName = "lonnie"
shellShortFm =  "ln"

currStatus = {
    "isRunning": False,
    "emoji": "⚡️",
    "cmdHistory": [],
}

def exitShell():
    print(f"\nExit the {shellName} shell? Yes(y)/No(n) :")
    cmd = getInput()
    while (cmd not in ["yes", "no", "y", "n"]):
        print("Invalid input! Please enter Yes(y)/No(n)")
        cmd = getInput()
    if (cmd in ["yes", "y"]):
        currStatus["isRunning"] = False

def displayMsg(msg):
    w, h = os.get_terminal_size()
    shellArea= w*h

    lines = []
    breaks = msg.split("\n")
    for b in breaks:
        if(b):
            lines.extend([ b[i:i+w] for i in range(0, len(b), w) ])
        else:
            lines.append(b)
    margin = 2
    numOfLines = len(lines)
    if(numOfLines < h-margin):
        for l in lines:print(l)
    else:
        for l in lines[:h-margin]:print(l)
        _ = input("------- press any key to continue -------: ")
        displayMsg("".join(lines[h-margin:]))

def welcomeMsg():
    displayMsg("\nWelcome lonnie 🥳🎉🥳🎉🥳🎉🥳🎉\n")

def clearConsole():
    _ = os.system('cls') if os.name=="nt" else os.system('clear')

def showVersion():
    print(f"{shellName} 1.0.0 ({platform.platform().lower()})\n")

def showDate():
    print(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S %p')}\n")

def getInput():
    cmd = input(f"{currStatus['emoji']}: ").strip().lower()
    time = datetime.now().strftime("%I:%M:%S %p")
    if len(currStatus["cmdHistory"]) >= 10:
        currStatus["cmdHistory"].pop(0)
    currStatus["cmdHistory"].append({"time": time, "cmd": cmd})
    return cmd

def listDirFiles():
    # "assume that there is only one directory for the OS"
    msg = "\n\nFiles in directory\n"
    for f in os.listdir():
        msg += f"+++ {f}\n"
    displayMsg(msg)

def getCmdHistory():
    history = currStatus["cmdHistory"]
    msg = "\n\nLast 10 commands\n"
    for i in range(len(history)):
        h = history[i]
        msg += f"({i+1}) - {h['time']} -> {h['cmd']}\n"
    displayMsg(msg)

def showHelp():
    msg = "\nYou can:\n"
    i=0
    for key in sorted(allCmds):
        msg += f'+++ ({key})  {allCmds[key]["description"]}\n'
        i+=1

    msg += "\n"
    displayMsg(msg)

def handleCmds(input):
    cmd = input.split(" ")[0].strip()

    if "--help" in input:
        specificCmd = allCmds.get(cmd)
        if (specificCmd):
            print(f"+++ {allCmds[cmd]['description']}\n")
        else:
            showHelp()
    elif cmd in allCmds:
        if (allCmds[cmd]["func"]["hasParams"]):
            allCmds[cmd]["func"]["name"](input)
        else:
            allCmds[cmd]["func"]["name"]()
    else:
        print(f"\n+++ no such command: {cmd}\n")

def handleAliasing(cmd):
    cmd = cmd.replace("alias", "")
    try:
        oldCmd, newCmd = cmd.split('=')
        oldCmd, newCmd = oldCmd.strip(), newCmd.strip()

        if (newCmd and (oldCmd in allCmds)):
            allCmds[newCmd] = allCmds.pop(oldCmd)
            print(f"\n🎉 Successfully aliased {oldCmd} to {newCmd}\n")
        else:
            print("\n+++ Invalid alias old command name!\n-----alias 'old command name' = 'new command name'  \n")
            print("\nCurrent commands. Enter help for more help")
            showHelp()
    except:
        print("\n+++ Invalid alias command!\n-----alias 'old command name' = 'new command name'  \n")

def handleScripts(cmd):
    commandsToDo = []

    try:
        fileName = cmd.split(' ')[1].strip()
        with open(fileName, "r") as f:
            commandsToDo = f.readlines()
        
        print("\n")
        for c in commandsToDo:
            c = c.strip().lower()
            handleCmds(c)
    except IOError:
        print(f"\ncan't open file: {fileName}\n")

    except Exception as err:
        print(f"\n+++ Invalid script command : {err}!\n-----script scriptFileName.extension \n")

def setDate(cmd):
    try:
        date =  cmd.replace("setdate", "").strip()
    except:
        print("\n+++ Invalid setdate command!\n-----setdate date \n")

    try:
        print("\nThis process needs admin privileges.")
        os.system(f'date -s "${date}"')
    except err:
        print("Run this shell in with administrator privileges.\n")
        print(f"\n+++ Error setting date!\n-----{err}\n")

allCmds = {
    "alias": {"description": "exit the shell", "func":{"hasParams": True, "name": handleAliasing},},
    "clear": {"description": "exit the shell", "func":{"hasParams": False, "name": clearConsole }},
    "exit": {"description": "exit the shell","func":{"hasParams": False, "name": exitShell} },
    "help": {"description": "exit the shell","func":{"hasParams": False, "name": showHelp} },
    "history": { "description": "exit the shell","func":{"hasParams": False, "name": getCmdHistory}},
    "ls": {"description": "exit the shell","func":{"hasParams": False, "name": listDirFiles} },
    "script": {"description": "exit the shell","func":{"hasParams": True, "name": handleScripts}},
    "setdate": { "description": "exit the shell","func":{"hasParams": True, "name": setDate} },
    "showdate": {"description": "exit the shell","func":{"hasParams": False, "name": showDate} },
    "version": {"description": "exit the shell","func":{"hasParams": False, "name": showVersion} },
}