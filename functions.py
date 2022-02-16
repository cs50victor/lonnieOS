import os, platform, random, time
from datetime import datetime
from classes.pcb import PCB
from utils import *

#! -------  USER ACCESSIBLE FUNCTIONS -------
def exitShell(input: str):
    if "-y" in input:
        currStatus["isRunning"] = False
    else:
        print(f"Exit the {shellName} shell? Yes[y]/[No(n] :")
        cmd = getInput()
        while cmd not in ["yes", "no", "y", "n"]:
            print(f"Invalid input! Please enter Yes[y]/No[n] : ")
            cmd = getInput()
        if cmd in ["yes", "y"]:
            currStatus["isRunning"] = False

def showVersion():
    print(f"{shellName} 1.0.0 ({platform.platform().lower()})\n")

def showDate():
    print(f"⏳ {datetime.now().strftime('%m/%d/%Y, %H:%M:%S %p')}\n")

def listDirFiles():
    # "assume that there is only one directory for the OS"
    msg = "\n\nFiles in directory:\n"
    for f in os.listdir():
        msg += f"+++ {f}\n"
    displayMsg(msg)

def getCmdHistory():
    history = currStatus["cmdHistory"]
    msg = "\n\nLast 10 commands:\n"
    for i in range(len(history)):
        h = history[i]
        msg += f"{i+1}. {h['cmd']}\n"
    displayMsg(msg)

def showHelp():
    msg = "\nYou can:\n"
    i = 0
    for key in sorted(allCmds):
        msg += f'  + {key}    ({allCmds[key]["description"]})\n'
        i += 1

    msg += f"\n{commandHelp}.\n"
    displayMsg(msg)

def handleAliasing(input: str):
    try:
        oldCmd, newCmd = input.split("=")
        oldCmd, newCmd = oldCmd.split(" ")[1].strip(), newCmd.strip()

        if newCmd and (oldCmd in allCmds):
            allCmds[newCmd] = allCmds.pop(oldCmd)
            print(f"\n{successEmoji} Successfully aliased {oldCmd} to {newCmd}\n")
        else:
            print(f"\nInvalid command format!\n{commandHelp}\n")
    except:
        print(f"\nInvalid command format!\n{commandHelp}\n")

def handleScripts(input: str):
    commandsToDo = []
    try:
        fileName = input.split(" ")[1].strip()
        with open(fileName, "r") as f:
            commandsToDo = f.readlines()
        for c in commandsToDo:
            c = c.strip().lower()
            handleCmds(c)
    except IOError:
        print(f"\n{txtColor['yellow']}can't open file: {fileName}{txtColor['reset']}\n")

    except Exception as err:
        print(f"\nInvalid script command : {err}!\n{commandHelp}\n")

def setDate(cmd: str):
    try:
        print("\nThis process needs admin privileges.")
        date = cmd.replace("setdate", "").strip()
        os.system(f'date -s "${date}"')
    except Exception as err:
        print(f"\nError setting date!\n{err}\n{commandHelp}")

def changeEmoji(input: str):
    try:
        newEmoji = input.split(" ")[1]

        if newEmoji:
            currStatus["emoji"] = newEmoji
            print(f"\n{successEmoji} Successfully changed emoji to -> {newEmoji}\n")
        else:
            print(f"\nInvalid emoji command!\n{commandHelp}\n")
    except:
        print(f"\nInvalid emoji command!\n{commandHelp}\n")

#! --------- PCB FUNCTIONS --------------
def allPCBs():
    if currStatus["processes"]:
        msg = ""
        for pid in sorted(currStatus["processes"]):
            process, queueName = currStatus["processes"][pid]
            msg += f"\n PID: {pid} | Queue: {queueName} | CUT: {process.getCpuCycles()} cycles | IRT: {process.getIoCycles()} cycles | WT: {process.getWaitCycles()} cycles | Memory: {process.getMemory()} MB\n"
        displayMsg(msg)
    else:
        print("No PCBs available.")

def readyPCBs():
    if currStatus["readyQ"]:
        msg = ""
        for pid in currStatus["readyQ"]:
            process, queueName = currStatus["processes"][pid]
            msg += f"\n PID: {pid} | Queue: {queueName} | CUT: {process.getCpuCycles()} cycles | IRT: {process.getIoCycles()} cycles | WT: {process.getWaitCycles()} cycles | Memory: {process.getMemory()} MB\n"
        displayMsg(msg)
    else:
        print("No PCBs in the ready queue.")

def blockedPCBs():
    if currStatus["blockedQ"]:
        msg = ""
        for b in currStatus["blockedQ"]:
            pid = b
            if (isinstance(id, list)):
                pid = b[0]
            process, queueName = currStatus["processes"][pid]
            msg += f"\n PID: {pid} | Queue: {queueName} | CUT: {process.getCpuCycles()} cycles | IRT: {process.getIoCycles()} cycles | WT: {process.getWaitCycles()} cycles | Memory: {process.getMemory()} MB\n"
        displayMsg(msg)
    else:
        print("No PCBs in the blocked queue.")

def newPCB(input: str):
    pid, memory = getArg(input, "--id"), getArg(input, "--memory")

    if not pid:
        print(f"{errorEmoji}Error creating PCB, no id provided.\n{commandHelp}\n")
    elif not pid.isdigit():
        print(f"{errorEmoji}Error creating PCB, process id must be an integer.\n")
    elif int(pid) in currStatus["processes"]:
        print(f"{errorEmoji}Error creating PCB, process with id={pid} already exists.\n")
    elif not memory:
        print(f"{errorEmoji}Error creating PCB, no memory provided.\n{commandHelp}\n")
    elif not memory.isdigit():
        print(f"{errorEmoji}Error creating PCB, process memory must be an integer.\n")
    elif int(memory) > currStatus["memory"]:
        print(
            f"{errorEmoji}Error creating PCB [id:{pid}, memory:{memory}], not enough memory. Available Memory: {currStatus['memory']} MB\n"
        )
    else:
        pid, memory = int(pid), int(memory)
        process = PCB(pid, memory)
        currStatus["memory"] -= memory
        currStatus["readyQ"].append(pid)
        currStatus["processes"][pid] = [process, "readyQ"]
        print(f"{successEmoji} Successfully created PCB with id={pid}")

def deletePCB(input: str):
    pid = getArg(input, "--id")

    if not pid:
        print(f"{errorEmoji}Error deleting PCB, no id provided.\n{commandHelp}\n")
    elif not pid.isdigit():
        print(f"{errorEmoji}Error deleting PCB, process id must be an integer.\n")
    elif int(pid) not in currStatus["processes"]:
        print(f"{errorEmoji}Error deleting PCB, process with id={pid} doesn't exist.\n")
    else:
        pid = int(pid)
        process, queueName = currStatus["processes"][pid]
        currStatus[queueName].remove(pid)
        del currStatus["processes"][pid]
        currStatus["memory"] += process.getMemory()
        print(
            f"{successEmoji} Successfully deleted PCB with Pid={pid}| Queue: {queueName} | CUT: {process.getCpuCycles()} cycles | IRT: {process.getIoCycles()} cycles | WT: {process.getWaitCycles()} cycles | Memory: {process.getMemory()} MB\n"
        )
        process.clear()

def blockPCB(input: str):
    pid = getArg(input, "--id")

    if not pid:
        print(f"{errorEmoji}Error blocking PCB, no id provided.\n{commandHelp}\n")
    elif not pid.isdigit():
        print(f"{errorEmoji}Error blocking PCB, process id must be an integer.\n")
    elif int(pid) not in currStatus["processes"]:
        print(f"{errorEmoji}Error blocking PCB, process with id={pid} doesn't exist.\n")
    elif int(pid) in currStatus["blockedQ"]:
        print(f"{errorEmoji}Error unblocking PCB, process with id={pid} is already blocked.\n")
    else:
        pid = int(pid)
        process, queueName = currStatus["processes"][pid]
        currStatus[queueName].remove(pid)
        currStatus["blockedQ"].append(pid)
        currStatus["processes"][pid] = [process, "blockedQ"]

        print(
            f"{successEmoji} Successfully blocked PCB with PID={pid}| Queue: {queueName} | CUT: {process.getCpuCycles()} cycles | IRT: {process.getIoCycles()} cycles | WT: {process.getWaitCycles()} cycles | Memory: {process.getMemory()} MB\n"
        )

def unblockPCB(input: str):
    pid = getArg(input, "--id")

    if not pid:
        print(f"{errorEmoji}Error unblocking PCB, no id provided.\n{commandHelp}\n")
    elif not pid.isdigit():
        print(f"{errorEmoji}Error unblocking PCB, process id must be an integer.\n")
    elif int(pid) not in currStatus["processes"]:
        print(f"{errorEmoji}Error unblocking PCB, process with id={pid} doesn't exist.\n")
    elif int(pid) in currStatus["readyQ"]:
        print(f"{errorEmoji}Error unblocking PCB, process with id={pid} is already unblocked.\n")
    else:
        pid = int(pid)
        process, queueName = currStatus["processes"][pid]

        currStatus[queueName].remove(pid)
        currStatus["readyQ"].append(pid)
        currStatus["processes"][pid] = [process, "readyQ"]
        print(f"{successEmoji} Successfully unblocked PCB with id={pid}")

def showPCB(input: str):
    pid = getArg(input, "--id")

    if not pid:
        print(f"{errorEmoji}Error displaying PCB, no id provided.\n{commandHelp}\n")
    elif not pid.isdigit():
        print(f"{errorEmoji}Error displaying PCB, process id must be an integer.\n")
    elif int(pid) not in currStatus["processes"]:
        print(f"{errorEmoji}Error displaying PCB, process with id={pid} doesn't exist.\n")
    else:
        pid = int(pid)
        process, queueName = currStatus["processes"][pid]
        print(
            f"\n PID: {pid} | Queue: {queueName} | CUT: {process.getCpuCycles()} cycles | IRT: {process.getIoCycles()} cycles | WT: {process.getWaitCycles()} cycles | Memory: {process.getMemory()} MB"
        )

def randomPCBs(input: str):
    num = getArg(input, "--num")

    if not num:
        print(f"{errorEmoji}Error generating PCBs, no number provided.\n{commandHelp}\n")
    elif not num.isdigit():
        print(f"{errorEmoji}Error generating PCBs, number of PCBS must be an integer.\n")
    else:
        num = int(num)

        startingId = (
            sorted(currStatus["processes"].keys())[-1]+1
            if len(currStatus["processes"]) > 0 else 0
        )
        mem = currStatus["memory"] // (num * 2)

        if (mem <= 0):
            print(f"{errorEmoji} Not enough memory to create {num} PCBs. [ MAX # of PCBs - {currStatus['memory']} ]")
        else:
            for i in range(num):
                newPCB(f"--id={startingId} --memory={mem}")
                startingId += 1

            print(f"{successEmoji} Successfully generated {num} random PCBs.")

def updateBlockedQ():
    # not an optimal solution
    bNum, end = 0, len(currStatus["blockedQ"])
    if (bNum==end):return 
    currStatus["blockedQ"].sort(
        key=lambda x: isinstance(x, list) and x[2], reverse=True
    )
    waitingProcess = list(filter(lambda x: isinstance(x, list), currStatus['blockedQ']))
    if (not waitingProcess): return
    minBlockedT = waitingProcess[-1][2]
    currStatus["ioQ"] = sorted(list(filter(lambda x: (x[1] > minBlockedT), currStatus["ioQ"])),key=lambda e: e[1])

    while bNum < end:
        t1 = time.time()
        b = currStatus["blockedQ"][bNum]
        if not isinstance(b, list):
            break 
        pid = b[0]

        for e in currStatus["ioQ"]:
            if e[0]==b[1] and e[1] > b[2]:
                t2 = time.time()
                t = round(t2 - t1, 3)
                process = currStatus["processes"][pid][0]
                process.updateIoCycles(t)
                process.updateWaitCycles(t)
                currStatus["ioQ"].remove(e)
                currStatus["blockedQ"].remove(b)
                currStatus["readyQ"].append(pid)
                currStatus["processes"][pid] = [process, "readyQ"]
                end-=1
                break
        end-=1

def execute():

    start,end = 0, len(currStatus["readyQ"])
    while start < end:
        pid = currStatus["readyQ"][start]
        assert len(currStatus["cpu"]) < 2, "CPU can only hold one PCB."

        process = currStatus["processes"][pid][0]
        currStatus["cpu"].append(process)

        processingTime = random.randint(0, 10000)
        process.updateCpuCycles(processingTime)

        for p in currStatus["processes"].values():
            p = p[0]
            if pid != p.getPid():
                p.updateWaitCycles(processingTime)

        for t in range(0, processingTime, 10):
            r = random.randint(0, 10)
            if r == 4:
                currStatus["ioQ"].append(["u", t])
            elif r == 9:
                currStatus["ioQ"].append(["h", t])

        decision = random.randint(0,3)

        if decision == 0:
            deletePCB(f"--id={pid}")
        else:
            currStatus["readyQ"].pop(0)
            if decision == 1:
                currStatus["readyQ"].append(pid)
            elif decision == 2:
                currStatus["blockedQ"].append([pid, "u", processingTime])
                currStatus["processes"][pid] = [process, "blockedQ"]
            elif decision == 3:
                currStatus["blockedQ"].append([pid, "h", processingTime])
                currStatus["processes"][pid] = [process, "blockedQ"]

        updateBlockedQ()
        currStatus["cpu"].pop(0)
        end = len(currStatus["readyQ"])

def handleCmds(input: str):
    time = datetime.now().strftime("%I:%M:%S %p")
    if len(currStatus["cmdHistory"]) >= 10:
        currStatus["cmdHistory"].pop(0)
    currStatus["cmdHistory"].append({"time": time, "cmd": input})

    cmd = input.split(" ")[0].strip()
    
    if (len(cmd)<1):
        return 
    elif "--help" in input:
        specificCmd = allCmds.get(cmd)
        if specificCmd:
            print(f"+++ {allCmds[cmd]['help']}\n")
        else:
            showHelp()
    elif cmd in allCmds:
        if allCmds[cmd]["func"]["hasParams"]:
            allCmds[cmd]["func"]["name"](input)
        else:
            allCmds[cmd]["func"]["name"]()
    else:
        print(f"\n+++ no such command: {cmd}\n")


allCmds = {
    "alias": {
        "description": "allow the user to map different command names",
        "help": "Usage : [COMMAND] [old command name]=[new command name]",
        "func": {"hasParams": True, "name": handleAliasing},
    },
    "all-pcbs": {
        "description": "display information for all PCBs in all queues, in order of PID.",
        "help": "Usage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": allPCBs},
    },
    "blocked-q": {
        "description": "display PCBs in the blocked queue.",
        "help": "Usage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": blockedPCBs},
    },
    "block-pcb": {
        "description": "place a Process Control Block in the blocked queue.",
        "help": "Usage : [COMMAND] [--id]=[integer] | Required argument --id (PCB id).",
        "func": {"hasParams": True, "name": blockPCB},
    },
    "clear": {
        "description": "clear the shell.",
        "help": "Usage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": clearConsole},
    },
    "delete-pcb": {
        "description": "delete a Process Control Block from its queue and free its memory.",
        "help": "Usage : [COMMAND] [--id]=[integer] | Required argument --id (PCB id).",
        "func": {"hasParams": True, "name": deletePCB},
    },
    "emoji": {
        "description": "allow the user to change shell emoji.",
        "help": "Usage : [COMMAND] [new emoji] | this command doesn't take any other arguments.",
        "func": {"hasParams": True, "name": changeEmoji},
    },
    "exit": {
        "description": "exit the shell.",
        "help": "Usage : [COMMAND] [-y] | Optional argument -y to confirm intention to exit shell.",
        "func": {"hasParams": True, "name": exitShell},
    },
    "help": {
        "description": "display all current commands, and other help information.",
        "help": "Usage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": showHelp},
    },
    "history": {
        "description": "display a history of the last ten commands a user used.",
        "help": "Usage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": getCmdHistory},
    },
    "ls": {
        "description": "display a list of all the files in the current directory.",
        "help": "Usage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": listDirFiles},
    },
    "new-pcb": {
        "description": "create a new Process Control Block.",
        "help": "Usage : [COMMAND] [--id]=[integer] [--memory]=[integer] | Required arguments --id (unique PCB id) , and --memory (PCB memory allocation).",
        "func": {"hasParams": True, "name": newPCB},
    },
    "generate-pcbs": {
        "description": "generate a number of PCBs.",
        "help": "Usage : [COMMAND] [--num]=[integer] | Required argument --num (the number of PCBs you want generated).",
        "func": {"hasParams": True, "name": randomPCBs},
    },
    "ready-q": {
        "description": "display PCBs in the ready queue.",
        "help": "Usage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": readyPCBs},
    },
    "run-cpu": {
        "description": "run a cpu process simulation.",
        "help": "Usage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": execute},
    },
    "script": {
        "description": "run commands from a batch file or script.",
        "help": "Usage : [COMMAND] [file name]",
        "func": {"hasParams": True, "name": handleScripts},
    },
    "setdate": {
        "description": "allow the user to change the date.",
        "help": "Usage : [COMMAND] [new date]",
        "func": {"hasParams": True, "name": setDate},
    },
    "showdate": {
        "description": "display the current date.",
        "help": "Usage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": showDate},
    },
    "show-pcb": {
        "description": "display information about a Process Control Block.",
        "help": "Usage : [COMMAND] [--id]=[integer] | Required argument --id (PCB id).",
        "func": {"hasParams": True, "name": showPCB},
    },
    "unblock-pcb": {
        "description": "place a Process Control Block in the ready queue.",
        "help": "Usage : [COMMAND] [--id]=[integer] | Required argument --id (PCB id).",
        "func": {"hasParams": True, "name": unblockPCB},
    },
    "version": {
        "description": "display the version number of the shell.",
        "help": "Usage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": showVersion},
    },
}

# ready queue -> p