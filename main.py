import os, platform, random
from datetime import datetime
from classes.pcb import PCB
from utils import *

#! -------  USER ACCESSIBLE FUNCTIONS -------
def exitShell(input: str) -> None:
    if "-y" in input:
        currStatus["session"] = False
    else:
        prevEmoji = currStatus["emoji"]
        currStatus["emoji"] = f"Exit the {shellName} shell? "
        cmd = getInput()
        while cmd not in ["yes", "no", "y", "n"]:
            print(f"\nInvalid input! Please enter Yes[y]/No[n]")
            cmd = getInput()
        if cmd in ["yes", "y"]:
            currStatus["session"] = False
        else:
            currStatus["emoji"] = prevEmoji


def showVersion() -> None:
    print(f"{shellName} {shellVersion} ({platform.platform().lower()})\n")


def showDate() -> None:
    print(f"⏳ {datetime.now().strftime('%m/%d/%Y, %H:%M:%S %p')}\n")


def listDirFiles() -> None:
    # "assume that there is only one directory for the OS"
    msg = "\n\nFiles in directory:\n"
    for f in os.listdir():
        msg += f"+++ {f}\n"
    displayMsg(msg)


def getCmdHistory() -> None:
    history = currStatus["cmdHistory"]
    msg = "\n\nLast 10 commands:\n"
    for i in range(len(history)):
        h = history[i]
        msg += f"{i+1}. {h['cmd']}\n"
    displayMsg(msg)


def showHelp() -> None:
    msg = "\nYou can:\n\n"
    i = 1
    for key in sorted(allCmds):
        msg += f" {i}. {key}".ljust(20)
        msg += f'- {allCmds[key]["description"]}\n'
        i += 1

    msg += f"\n{commandHelp}.\n"
    print(msg)


def handleAliasing(input: str)  -> None:
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


def handleScripts(input: str)  -> None:
    commandsToDo = []
    try:
        fileName = input.split(" ")[1].strip()
        with open(fileName, encoding="utf-8") as f:
            commandsToDo = f.readlines()
        for c in commandsToDo:
            c = c.strip().lower()
            handleCmds(c)
    except IOError:
        print(f"\n{txtColor['yellow']}can't open file: {fileName}{txtColor['reset']}\n")
    except Exception as err:
        print(f"\nInvalid script command : {err}!\n{commandHelp}\n")


def setDate(cmd: str)  -> None:
    try:
        print("\nThis process needs admin privileges.")
        date = cmd.replace("setdate", "").strip()
        os.system(f'date -s "${date}"')
    except Exception as err:
        print(f"\nError setting date!\n{err}\n{commandHelp}")


def changeEmoji(input: str) -> None:
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
def allPCBs() -> None:
    if currStatus["processes"]:
        msg = ""
        for pid in sorted(currStatus["processes"]):
            process, queueName = currStatus["processes"][pid]
            msg += f"\n PID: {pid} | Queue: {queueName} | CUT: {process.getCpuT()} cycles | I/O-T: {process.getIot()} cycles | WT: {process.getWt()} cycles | Memory: {process.getMemory()} MB\n"
        displayMsg(msg)
    else:
        print("No PCBs available.")


def readyPCBs() -> None:
    if currStatus["readyQ"]:
        msg = ""
        for pid in currStatus["readyQ"]:
            process, queueName = currStatus["processes"][pid]
            msg += f"\n PID: {pid} | Queue: {queueName} | CUT: {process.getCpuT()} cycles | I/O-T: {process.getIot()} cycles | WT: {process.getWt()} cycles | Memory: {process.getMemory()} MB\n"
        displayMsg(msg)
    else:
        print("No PCBs in the ready queue.")


def blockedPCBs() -> None:
    if currStatus["blockedQ"]:
        msg = ""
        for b in currStatus["blockedQ"]:
            if isinstance(b, list):
                pid = b[0]
            else:
                pid = b
            process, queueName = currStatus["processes"][pid]
            msg += f"\n PID: {pid} | Queue: {queueName} | blocked time: {process.getBt()} | CUT: {process.getCpuT()} cycles | I/O-T: {process.getIot()} cycles | WT: {process.getWt()} cycles | Memory: {process.getMemory()} MB\n"
        displayMsg(msg)
    else:
        print("No PCBs in the blocked queue.")


def newPCB(input: str)  -> None:
    pid, memory = getArg(input, "--id",int), getArg(input, "--memory",int)

    if not pid:
        print(f"{errorEmoji}Error creating PCB, no id provided or id is not integer.\n{commandHelp}\n")
    elif pid in currStatus["processes"]:
        print(
            f"{errorEmoji}Error creating PCB, process with id={pid} already exists.\n"
        )
    elif not memory:
        print(f"{errorEmoji}Error creating PCB, no memory provided or memory is not an integer.\n{commandHelp}\n")
    elif memory > currStatus["memory"]:
        print(
            f"{errorEmoji}Error creating PCB [id:{pid}, memory:{memory}], not enough memory. Available Memory: {currStatus['memory']} MB\n"
        )
    else:
        process = PCB(pid, memory)
        currStatus["memory"] -= memory
        currStatus["readyQ"].append(pid)
        currStatus["processes"][pid] = [process, "readyQ"]
        print(f"{successEmoji} Successfully created PCB with id={pid}")


def deletePCB(input: str)  -> None:
    pid = getArg(input, "--id", int)

    if not pid:
        print(f"{errorEmoji}Error deleting PCB, no id provided or id is not an integer.\n{commandHelp}\n")
    elif pid not in currStatus["processes"]:
        print(f"{errorEmoji}Error deleting PCB, process with id={pid} doesn't exist.\n")
    else:
        process, queueName = currStatus["processes"][pid]
        currStatus[queueName].remove(pid)
        del currStatus["processes"][pid]
        currStatus["memory"] += process.getMemory()
        print(
            f"{successEmoji} Successfully deleted PCB with Pid={pid}| Queue: {queueName} | CUT: {process.getCpuT()} cycles | I/O-T: {process.getIot()} cycles | WT: {process.getWt()} cycles | Memory: {process.getMemory()} MB\n"
        )
        process.delete()


def blockPCB(input: str) -> None:
    pid = getArg(input, "--id", int)

    if not pid:
        print(f"{errorEmoji}Error blocking PCB, no id provided or id is not an integer.\n{commandHelp}\n")
    elif pid not in currStatus["processes"]:
        print(f"{errorEmoji}Error blocking PCB, process with id={pid} doesn't exist.\n")
    elif pid in currStatus["blockedQ"]:
        print(
            f"{errorEmoji}Error unblocking PCB, process with id={pid} is already blocked.\n"
        )
    else:
        process, queueName = currStatus["processes"][pid]
        currStatus[queueName].remove(pid)
        currStatus["blockedQ"].append(pid)
        currStatus["processes"][pid] = [process, "blockedQ"]

        print(
            f"{successEmoji} Successfully blocked PCB with PID={pid}| Queue: {queueName} | CUT: {process.getCpuT()} cycles | I/O-T: {process.getIot()} cycles | WT: {process.getWt()} cycles | Memory: {process.getMemory()} MB\n"
        )


def unblockPCB(input: str) -> None:
    pid = getArg(input, "--id", int)

    if not pid:
        print(f"{errorEmoji}Error unblocking PCB, no id provided or id is not an integer.\n{commandHelp}\n")
    elif pid not in currStatus["processes"]:
        print(
            f"{errorEmoji}Error unblocking PCB, process with id={pid} doesn't exist.\n"
        )
    elif pid in currStatus["readyQ"]:
        print(
            f"{errorEmoji}Error unblocking PCB, process with id={pid} is already unblocked.\n"
        )
    else:
        process, queueName = currStatus["processes"][pid]

        currStatus[queueName].remove(pid)
        currStatus["readyQ"].append(pid)
        currStatus["processes"][pid] = [process, "readyQ"]
        print(f"{successEmoji} Successfully unblocked PCB with id={pid}")


def showPCB(input: str) -> None:
    pid = getArg(input, "--id", int)

    if not pid:
        print(f"{errorEmoji}Error displaying PCB, no id provided is not an integer.\n{commandHelp}\n")
    elif pid not in currStatus["processes"]:
        print(
            f"{errorEmoji}Error displaying PCB, process with id={pid} doesn't exist.\n"
        )
    else:
        process, queueName = currStatus["processes"][pid]
        print(
            f"\n PID: {pid} | Queue: {queueName} | CUT: {process.getCpuT()} cycles | I/O-T: {process.getIot()} cycles | WT: {process.getWt()} cycles | Memory: {process.getMemory()} MB"
        )


def randomPCBs(input: str) -> None:
    num = getArg(input, "--num", int)

    if not num:
        print(
            f"{errorEmoji}Error generating PCBs, no number provided or number is not an integer.\n{commandHelp}\n"
        )
    else:

        startingId = (
            sorted(currStatus["processes"].keys())[-1] + 1
            if len(currStatus["processes"]) > 0
            else 0
        )
        mem = currStatus["memory"] // (num * 2)

        if mem <= 0:
            print(
                f"{errorEmoji} Not enough memory to create {num} PCBs. [ MAX # of PCBs - {currStatus['memory']} ]"
            )
        else:
            for i in range(num):
                newPCB(f"--id={startingId} --memory={mem}")
                startingId += 1

            print(f"{successEmoji} Successfully generated {num} random PCBs.")


def updateBlockedQ() -> None:
    # not an optimal solution
    bNum, end = 0, len(currStatus["blockedQ"])
    if bNum == end:
        return
    currStatus["blockedQ"].sort(
        key=lambda x: isinstance(x, list) and x[2], reverse=True
    )
    waitingProcess = list(filter(lambda x: isinstance(x, list), currStatus["blockedQ"]))
    if not waitingProcess:
        return
    minBlockedT = waitingProcess[-1][2]
    currStatus["ioQ"] = sorted(
        list(filter(lambda x: (x[1] > minBlockedT), currStatus["ioQ"])),
        key=lambda e: e[1],
    )
    spaces, numOfSpaces = " ", 3
    with open("cpu-log.txt", "w+",encoding="utf-8") as cpuLogfile:
        cpuLogfile.write(f"{spaces*numOfSpaces}- GOING THROUGH BLOCKED QUEUE TO SEE IF THE EVENT QUEUE SATISFIES ANY OF THE WAITING PROCESSES.\n")
        while bNum < end:
            b = currStatus["blockedQ"][bNum]
            if not isinstance(b, list):
                break
            pid = b[0]
            process = currStatus["processes"][pid][0]
            cpuLogfile.write(f"{spaces*(numOfSpaces+1)}- Blocked process [pid: {process.getPid()}, entered the blocked at : {process.getBt()}]\n")

            
            for e in currStatus["ioQ"]:
                bt = process.getBt()
                if e[0] == b[1] and e[1] > bt:
                    cpuLogfile.write(f"{spaces*(numOfSpaces+2)}- Found event [type: {e[0]}, timestamp:{e[1]}] to satisfy blocked process request [pid: {process.getPid()}, entered the blocked at : {process.getBt()}]\n")
                    t = e[1] - bt
                    process.setIot(t)
                    cpuLogfile.write(f"{spaces*(numOfSpaces+3)}- Updated the I/O usage time with how long it took the process to get the appropriate I/O - {t}.\n")
                    process.setBt(0)
                    cpuLogfile.write(f"{spaces*(numOfSpaces+3)}- Set process blocked time to 0.\n")
                    process.addWt(t)
                    cpuLogfile.write(f"{spaces*(numOfSpaces+3)}- Updated process waiting value by {t}.\n")
                    currStatus["ioQ"].remove(e)
                    cpuLogfile.write(f"{spaces*(numOfSpaces+3)}- Remove I/O event from I/O queue .\n")
                    currStatus["readyQ"].append(pid)
                    cpuLogfile.write(f"{spaces*(numOfSpaces+3)}- Added process to ready queue.\n")
                    currStatus["processes"][pid] = [process, "readyQ"]
                    currStatus["blockedQ"].remove(b)
                    cpuLogfile.write(f"{spaces*(numOfSpaces+3)}- Removed process from blocked queue.\n")
                    end -= 1
                    break
            bNum += 1


def execute() -> None:

    start, end = 0, len(currStatus["readyQ"])
    spaces, numOfSpaces = " ", 0
    with open("cpu-log.txt", "w+",encoding="utf-8") as cpuLogfile:
        cpuLogfile.write(f"{spaces*numOfSpaces}CPU SIMULATION.\n")
        while start < end:
            pid = currStatus["readyQ"][start]
            assert len(currStatus["cpu"]) < 2, "CPU can only hold one PCB."

            process = currStatus["processes"][pid][0]
            currStatus["cpu"].append(process)
            cpuLogfile.write(f"{spaces*(numOfSpaces+1)}Process [pid: {process.getPid()}] entered the CPU.\n")

            processingTime = random.randint(0, 10000)
            process.addCpuT(processingTime)
            cpuLogfile.write(f"{spaces*(numOfSpaces+1)}- Process time generated {processingTime}(s).\n")
            cpuLogfile.write(f"{spaces*(numOfSpaces+1)}- Process CPU Usage Term increased by {processingTime}.\n")

            for p in currStatus["processes"].values():
                p = p[0]
                if pid != p.getPid():
                    p.addWt(processingTime)
            cpuLogfile.write(f"{spaces*(numOfSpaces+1)}- Updated the Waiting Term in other processes by {processingTime}.\n")

            for t in range(0, processingTime, 10):
                r = random.randint(0, 10)
                cpuLogfile.write(f"{spaces*(numOfSpaces+2)}- Generated random number between 0 and 10 for ten time cycle- {r}.\n")
                if r == 4:
                    currStatus["ioQ"].append(["u", t])
                    cpuLogfile.write(f"{spaces*(numOfSpaces+3)}- Added a user input I/O event to the event queue with a timecycle stamp of {t}.\n")
                elif r == 9:
                    currStatus["ioQ"].append(["h", t])
                    cpuLogfile.write(f"{spaces*(numOfSpaces+3)}- Added a hard drive I/O event to the event queue with a timecycle stamp of {t}.\n")

            decision = random.randint(0, 3)
            cpuLogfile.write(f"{spaces*(numOfSpaces+1)}- Generated random number between 0 and 3 to determine what happens with the process - {decision}.\n")

            if decision == 0:
                deletePCB(f"--id={pid}")
                cpuLogfile.write(f"{spaces*(numOfSpaces+2)}- Process got terminated and removed from the system.\n")
            else:
                currStatus["readyQ"].pop(0)
                if decision == 1:
                    currStatus["readyQ"].append(pid)
                    cpuLogfile.write(f"{spaces*(numOfSpaces+2)}- Process returned to the ready queue to wait its turn.\n")
                elif decision == 2:
                    process.setBt(processingTime)
                    currStatus["blockedQ"].append([pid, "u",processingTime])
                    currStatus["processes"][pid] = [process, "blockedQ"]
                    cpuLogfile.write(f"{spaces*(numOfSpaces+2)}- Process required an I/O event and went into the blocked queue wanting an user I/O request.\n")
                elif decision == 3:
                    process.setBt(processingTime)
                    currStatus["blockedQ"].append([pid, "h",processingTime])
                    currStatus["processes"][pid] = [process, "blockedQ"]
                    cpuLogfile.write(f"{spaces*(numOfSpaces+2)}- Process required an I/O event and went into the blocked queue wanting a hard drive I/O request.\n")

            updateBlockedQ()
            currStatus["cpu"].pop(0)
            end = len(currStatus["readyQ"])
        cpuLogfile.write(f"{spaces*numOfSpaces}CPU SIMULATION FINISHED.\n")
        cpuLogfile.write(f"{spaces*numOfSpaces}Total Number of processes in ready queue - {len(currStatus['readyQ'])}.\n")
        cpuLogfile.write(f"{spaces*numOfSpaces}Total Number of processes in blocked queue - {len(currStatus['blockedQ'])}.\n")
        cpuLogfile.write(f"{spaces*numOfSpaces}Total Number of processes in the system - {len(currStatus['processes'])}.\n")
        


def handleCmds(input: str):
    time = datetime.now().strftime("%I:%M:%S %p")
    if len(currStatus["cmdHistory"]) >= 10:
        currStatus["cmdHistory"].pop(0)
    currStatus["cmdHistory"].append({"time": time, "cmd": input})

    cmd = input.split(" ")[0].strip()

    if len(cmd) < 1:
        return
    elif "--help" in input:
        if allCmds.get(cmd):
            print(f"\n{allCmds[cmd]['help']}\n")
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
        "description": "allow the user to map different command names.",
        "help": "allow the user to map different command names.\nUsage : [COMMAND] [old command name]=[new command name]",
        "func": {"hasParams": True, "name": handleAliasing},
    },
    "all-pcbs": {
        "description": "display information for all PCBs in all queues, in order of PID.",
        "help": "display information for all PCBs in all queues, in order of PID.\nUsage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": allPCBs},
    },
    "blocked-q": {
        "description": "display PCBs in the blocked queue.",
        "help": "display PCBs in the blocked queue.\nUsage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": blockedPCBs},
    },
    "block-pcb": {
        "description": "place a Process Control Block in the blocked queue.",
        "help": "place a Process Control Block in the blocked queue.\nUsage : [COMMAND] [--id]=[integer] \nRequired argument --id (PCB id).",
        "func": {"hasParams": True, "name": blockPCB},
    },
    "clear": {
        "description": "clear the shell.",
        "help": "clear the shell.\nUsage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": clearConsole},
    },
    "delete-pcb": {
        "description": "delete a Process Control Block from its queue and free its memory.",
        "help": "delete a Process Control Block from its queue and free its memory.\nUsage : [COMMAND] [--id]=[integer] \nRequired argument --id (PCB id).",
        "func": {"hasParams": True, "name": deletePCB},
    },
    "emoji": {
        "description": "allow the user to change shell emoji.",
        "help": "allow the user to change shell emoji.\nUsage : [COMMAND] [new emoji] | this command doesn't take any other arguments.",
        "func": {"hasParams": True, "name": changeEmoji},
    },
    "exit": {
        "description": "exit the shell.",
        "help": "exit the shell.\nUsage : [COMMAND] [-y] | Optional argument -y to confirm intention to exit shell.",
        "func": {"hasParams": True, "name": exitShell},
    },
    "help": {
        "description": "display all current commands, and other help information.",
        "help": "display all current commands, and other help information.\nUsage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": showHelp},
    },
    "history": {
        "description": "display a history of the last ten commands a user used.",
        "help": "display a history of the last ten commands a user used.\nUsage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": getCmdHistory},
    },
    "ls": {
        "description": "display a list of all the files in the current directory.",
        "help": "display a list of all the files in the current directory.\nUsage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": listDirFiles},
    },
    "new-pcb": {
        "description": "create a new Process Control Block.",
        "help": "create a new Process Control Block.\nUsage : [COMMAND] [--id]=[integer] [--memory]=[integer] \nRequired arguments --id (unique PCB id) , and --memory (PCB memory allocation).",
        "func": {"hasParams": True, "name": newPCB},
    },
    "generate-pcbs": {
        "description": "generate a number of PCBs.",
        "help": "generate a number of PCBs.\nUsage : [COMMAND] [--num]=[integer] \nRequired argument --num (the number of PCBs you want generated).",
        "func": {"hasParams": True, "name": randomPCBs},
    },
    "ready-q": {
        "description": "display PCBs in the ready queue.",
        "help": "display PCBs in the ready queue.\nUsage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": readyPCBs},
    },
    "run-cpu": {
        "description": "run a cpu process simulation.",
        "help": "run a cpu process simulation.\nUsage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": execute},
    },
    "script": {
        "description": "run commands from a batch file or script.",
        "help": "run commands from a batch file or script.\nUsage : [COMMAND] [file name]",
        "func": {"hasParams": True, "name": handleScripts},
    },
    "setdate": {
        "description": "allow the user to change the date.",
        "help": "allow the user to change the date.\nUsage : [COMMAND] [new date]",
        "func": {"hasParams": True, "name": setDate},
    },
    "showdate": {
        "description": "display the current date.",
        "help": "display the current date.\nUsage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": showDate},
    },
    "show-pcb": {
        "description": "display information about a Process Control Block.",
        "help": "display information about a Process Control Block.\nUsage : [COMMAND] [--id]=[integer] \nRequired argument --id (PCB id).",
        "func": {"hasParams": True, "name": showPCB},
    },
    "unblock-pcb": {
        "description": "place a Process Control Block in the ready queue.",
        "help": "place a Process Control Block in the ready queue.\nUsage : [COMMAND] [--id]=[integer] \nRequired argument --id (PCB id).",
        "func": {"hasParams": True, "name": unblockPCB},
    },
    "version": {
        "description": "display the version number of the shell.",
        "help": "display the version number of the shell.\nUsage : [COMMAND] | this command doesn't take any other arguments.",
        "func": {"hasParams": False, "name": showVersion},
    },
}
