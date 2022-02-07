import os, platform
from datetime import datetime

shellName = "Hendrix"
shellShortFm = "hn"
emoji = "🎸"
cmdHistory = []

# change data structure in next version
allCmds = {
    "alias": {"cname": "alias", "description": "exit the shell"},
    "clear": {"cname": "clear", "description": "exit the shell"},
    "dir-files": {"cname": "ls", "description": "exit the shell"},
    "exit": {"cname": "exit", "description": "exit the shell"},
    "get-date": {"cname": "showdate", "description": "exit the shell"},
    "help": {"cname": "help", "description": "exit the shell"},
    "history": {"cname": "--history", "description": "exit the shell"},
    "script": {"cname": "script", "description": "exit the shell"},
    "set-date": {"cname": "setdate", "description": "exit the shell"},
    "version": {"cname": "--version", "description": "exit the shell"},
}

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

def getVersion():
    return f"{shellName} 1.0.0 ({platform.platform().lower()})"

def getDate():
    return datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p")

def getCmd():
    cmd = input(f"{emoji}: ").strip().lower()
    time = getDate()
    if len(cmdHistory) >= 10:
        cmdHistory.pop(0)
    cmdHistory.append({"time": time, "cmd": cmd})
    return cmd

def listDirFiles():
    # "assume that there is only one directory for the OS"
    msg = "\n\nFiles in directory\n"
    for f in os.listdir():
        msg += f"+++ {f}\n"
    displayMsg(msg)

def getCmdHistory():
    msg = "\n\nLast 10 commands\n"
    for i in range(len(cmdHistory)):
        h = cmdHistory[i]
        msg += f"+++ ({i}) - {h['time']} -> {h['cmd']}\n"
    displayMsg(msg)

def showHelp():
    msg = "\nYou can:\n"
    for c in sorted(allCmds):
        cmd = allCmds[c]
        msg += f'+++ ({cmd["cname"]})  {cmd["description"]}\n'
    msg += "\n"
    displayMsg(msg)

def handleAliasing(cmd):
    cmd = cmd.replace("alias", "")
    try:
        oldCmd, newCmd = cmd.split('=')
        oldCmd, newCmd = oldCmd.strip(), newCmd.strip()
    except:
        print("\n+++ Invalid alias command!\n-----alias 'old command name' = 'new command name'  \n")

    oldCmdArr = [y for x, y in allCmds.items()]
    oldCmdArr = [c["cname"] for c in oldCmdArr]
    if ((oldCmd and newCmd) and oldCmd in oldCmdArr):
        # not an optimal solution
        for name, detail in allCmds.items():
            if oldCmd == detail["cname"]:
                detail["cname"] = newCmd
        print(f"\n🎉 Successfully aliased {oldCmd} to {newCmd}")
    else:
        print("\n+++ Invalid alias old command name!\n-----alias 'old command name' = 'new command name'  \n")
        print("\nCurrent commands. Enter help for more help")
        for i in range(len(oldCmdArr)):
            print(f"({i}) {oldCmdArr[i]}")

def handleScripts(cmd):
    commandsToDo = []

    try:
        fileName = cmd.split(' ')[1].strip()
        with open(fileName, "r") as f:
            commandsToDo = f.readlines()
    except:
        print("\n+++ Invalid script command!\n-----script scriptFileName.extension \n")

    print("\n")
    for c in commandsToDo:
        c = c.strip().lower()
        handleCmd(c)
    print("\n")

def setDate(cmd):
    commandsToDo = []

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

def handleCmd(cmd):
    if "--help" in cmd or cmd == allCmds["help"]["cname"]:
        showHelp()
    elif "alias" in cmd:
        handleAliasing(cmd)

    elif cmd == allCmds["version"]["cname"]:
        print(getVersion())

    elif cmd == allCmds["get-date"]["cname"]:
        print(getDate())

    elif cmd == allCmds["dir-files"]["cname"]:
        listDirFiles()

    elif cmd == allCmds["history"]["cname"]:
        getCmdHistory()

    elif allCmds["script"]["cname"] in cmd:
        handleScripts(cmd)

    elif allCmds["set-date"]["cname"] in cmd:
        setDate(cmd)
    
    elif cmd == allCmds["clear"]["cname"]:
        clearConsole()
    else:
        print(f"\n+++ no such command: {cmd}\n")

def runShell():
    
    clearConsole()
    welcomeMsg()
    # assert 8<4,"List is empty."

    while True:
        cmd = getCmd()
        if(cmd == allCmds["exit"]["cname"]):
            print(f"\nExit the {shellName} shell? Yes(y)/No(n) :")
            cmd = getCmd()
            while (cmd not in ["yes", "no", "y", "n"]):
                print("Invalid input! Please enter Yes(y)/No(n)")
                cmd = getCmd()
            if (cmd in ["yes", "y"]):
                return
        else:
            handleCmd(cmd)

# only execute shell when this file is being run directly
if __name__ == '__main__':
    runShell()