import os, platform, time
from datetime import datetime
from shellConfig import *
from classes.os import OS

# create an operating system instance
# provides an api for kernel level commands (PCB related commands)
lonnieOS = OS()

"""
  This file is divided into 3 major sections 
  and contains all the functions/commands that 
  a user can call in the shell.

  1 - SHELL ONLY FUNCTIONS [NON PCB/OS FUNCTIONS ]
  2 - PCB & OPERATING SYSTEM SHELL FUNCTIONS 
  3 - ALL SHELL COMMANDS MAPPED TO THEIR DESCRIPTION & FUNCTION
"""

# * --------- SHELL ONLY FUNCTIONS [AKA NON OS/PCB FUNCTIONS ]--------------


def exitShell(input: str) -> None:
    # Allows the user to exit the program

    if input.endswith(" -y"):
        shellStatus["isRunning"] = False
    else:
        prevEmoji = shellStatus["emoji"]
        shellStatus["emoji"] = f"Exit the {shellName} shell? "
        cmd = getInput()
        while cmd not in ["yes", "no", "y", "n"]:
            print(f"\nInvalid input! Please enter Yes[y]/No[n]")
            cmd = getInput()
        if cmd in ["yes", "y"]:
            shellStatus["isRunning"] = False
        else:
            shellStatus["emoji"] = prevEmoji


def showVersion() -> None:
    # Displays the current version of the shell to the user

    print(f"{shellName} {shellVersion} ({platform.platform().lower()})\n")


def showDate() -> None:
    # Displays the current date to the user

    print(f"⏳ {datetime.now().strftime('%m/%d/%Y, %H:%M:%S %p')}\n")


def listDirFiles() -> None:
    # Assumes that there is only one directory for this OS
    # & displays all the files in the current directory

    header = "Files in directory"
    msg = underlineMsg(f"{header}:")
    for i, file in enumerate(os.listdir()):
        msg += f"{i+1}. {file}\n"
    displayMsg(msg)


def getCmdHistory() -> None:
    # Displays the last 10 commands entered in the shell by the user

    history = shellStatus["cmdHistory"]
    msg = underlineMsg("Last 10 commands")

    for i, command in enumerate(history):
        msg += f"{command['time']} | ".ljust(10) + f"{i+1}. {command['cmd']}\n"
    displayMsg(msg)


def showHelp() -> None:
    # Displays helpful information on all the available shell commands to the user

    msg = underlineMsg("Available Commands:")

    for i, el in enumerate(sorted(allCmds.items())):
        key, value = el
        msg += f"{i+1}. {key}".ljust(20) + f'- {value["description"]}\n'

    msg += f"\n{commandHelp}.\n"
    print(msg)


def setDate(cmd: str) -> None:
    # Allows the user to set the date of the operating system

    try:
        print("\nThis command needs admin privileges.")
        date = cmd.replace("setdate", "").strip()
        os.system(f'date -s "${date}"')
    except:
        printErrorMsg(f"Error setting date!\n{commandHelp}")


def handleAliasing(input: str) -> None:
    # Changes a shell command's current name to a new name specified by the user

    try:
        oldCmd, newCmd = input.split("=")
        oldCmd, newCmd = oldCmd.split(" ")[1].strip(), newCmd.strip()

        allCmds[newCmd] = allCmds.pop(oldCmd)
        printSuccessMsg(f"Successfully aliased '{oldCmd}' to '{newCmd}'")
    except KeyError:
        printErrorMsg(
            f"Invalid alias command!You tried aliasing a command that doesn't exit.\n{commandHelp}"
        )
    except:
        printErrorMsg(f"Invalid alias command format!\n{commandHelp}")


def handleScripts(input: str) -> None:
    # Executes a sequence of shell commands from a script/batch file

    commandsToDo = []
    try:
        fileName = input.split(" ")[1].strip()
        # path
        with open(fileName, encoding="utf-8") as f:
            commandsToDo = f.readlines()
        for c in commandsToDo:
            if(len(c.strip())):
                header = underlineMsg('script cmd:').replace('\n','')
                print(f"{header} {c}")
                handleCmds(c)
    except IOError:
        printWarningMsg("can't open provided script/batch file.")
    except Exception as err:
        printErrorMsg(f"Invalid script command format!\n{commandHelp}\n{err}")


def changeEmoji(input: str) -> None:
    # Allows the user to change the emoji shown in the shell

    try:
        newEmoji = input.split(" ")[1]

        if newEmoji:
            shellStatus["emoji"] = newEmoji
            printSuccessMsg(f"Successfully changed emoji to -> {newEmoji}")
        else:
            printErrorMsg(
                f"Invalid emoji command! Did not enter a valid new emoji.\n{commandHelp}"
            )
    except:
        printErrorMsg(f"Invalid emoji command!\n{commandHelp}")


def handleCmds(input: str):
    # This handles mapping/connecting the commands entered in the shell to their functions

    input = input.strip().lower()

    if len(input):
        if len(shellStatus["cmdHistory"]) >= 10:
            shellStatus["cmdHistory"].pop(0)

        time = datetime.now().strftime("%I:%M:%S %p")
        shellStatus["cmdHistory"].append({"time": time, "cmd": input})

        cmd = input.split(" ")[0]

        if "--help" in input:
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
            print(f"++ command not found: {cmd}\nEnter 'help' to see all available commands.\n")


# * --------- PCB & OPERATING SYSTEM SHELL FUNCTIONS --------------


def allPCBs() -> None:
    # Displays a list of all Processes in the system.

    if lonnieOS.processes.isNotEmpty():
        msg = underlineMsg("ALL PCBS")
        for pid in lonnieOS.processes.getSortedIds():
            process = lonnieOS.processes.retreive(pid)
            msg += f"{process}\n"
        displayMsg(msg)
    else:
        print("No PCBs available.\n")


def readyPCBs() -> None:
    # Displays a list of all system processes in the ready queue.

    if lonnieOS.readyQ.isNotEmpty():
        msg = underlineMsg("PCBS IN READY QUEUE")
        for pid in lonnieOS.readyQ.getAllIdsUnsorted():
            process = lonnieOS.processes.retreive(pid)
            msg += f"{process}\n"
        displayMsg(msg)
    else:
        print("No PCBs in the ready queue.\n")


def blockedPCBs() -> None:
    # Displays a list of all currently blocked system processes.

    if lonnieOS.blockedQ.isNotEmpty():
        msg = underlineMsg("ALL BLOCKED PCBS")
        for b in lonnieOS.blockedQ.getAll():
            if isinstance(b, dict):
                pid = b["pid"]
            else:
                pid = b
            process = lonnieOS.processes.retreive(pid)
            msg += f"{process}\n"
        displayMsg(msg)
    else:
        print("No PCBs in the blocked queue.\n")


def showPCB(input: str) -> None:
    # Displays details of a specified system process.

    pid = getArg(input, "--id", int)

    if not isinstance(pid, int):
        printErrorMsg(
            f"Can't show PCB info. no id provided or id is not an integer.\n{commandHelp}"
        )
    else:
        try:
            process = lonnieOS.processes.retreive(pid)  # type: ignore
            print(process)
        except Exception as err:
            printErrorMsg(f"{err}")


def newPCB(input: str) -> None:
    # Allows the user to create a new process

    pid = getArg(input, "--id", int)
    memory = getArg(input, "--memory", float)
    pcbType = getArg(input, "--type", str)

    try:
        lonnieOS.createPCB(pid, memory, pcbType)  # type: ignore
        printSuccessMsg(
            f"Created PCB [ id={pid}, memory={memory}, type={pcbType}]. Memory left {lonnieOS.getSystemMemory()} MB"
        )
    except Exception as err:
        printErrorMsg(f"{err}")


def deletePCB(input: str) -> None:
    # Allows the user to delete a process

    pid = getArg(input, "--id", int)

    try:
        processInfo = lonnieOS.deletePCB(pid)  # type: ignore
        printSuccessMsg(f"Deleted PCB with {processInfo}")
    except Exception as err:
        printErrorMsg(f"{err}")


def blockPCB(input: str) -> None:
    # Allows the user to block a process

    pid = getArg(input, "--id", int)

    try:
        lonnieOS.blockPCB(pid)  # type: ignore
        printSuccessMsg(f"Blocked PCB with PID={pid}")
    except Exception as err:
        printErrorMsg(f"{err}")


def unblockPCB(input: str) -> None:
    # Allows the user to unblock a process

    pid = getArg(input, "--id", int)

    try:
        lonnieOS.unblockPCB(pid)  # type: ignore
        printSuccessMsg(f"Unblocked PCB with PID={pid}")
    except Exception as err:
        printErrorMsg(f"{err}")


def randomPCBs(input: str) -> None:
    # Allows the user to generate a number of random processes

    num = getArg(input, "--num", int)

    try:
        lonnieOS.generatePCBs(num)  # type: ignore
        printSuccessMsg(
            f"Generated {num} random PCBs. Memory left {lonnieOS.getSystemMemory()} MB"
        )
    except Exception as err:
        printErrorMsg(f"{err}")


def execute(input: str) -> None:
    # Allows the user to simulate different cpu scheduling algorithms

    method = getArg(input, "--scheduler", str)
    quantum = getArg(input, "--quantum", int)
    numOfQueues = getArg(input, "--queues", int)
    debug = getArg(input, "--debug", str)

    minQuantum = 1000
    maxQuantum = 5000
    minNumOfQueues = 1
    maxNumOfQueues = lonnieOS.readyQ.size()

    useDebug = debug in ["true", "yes", "y"]
    schedules = lonnieOS.getSchedulingPolicies()

    if method is None:
        printErrorMsg(
            f"Error running CPU simulation, no method provided or method is not a string.\n{commandHelp}"
        )
        return None
    elif method not in schedules:
        printErrorMsg(
            f"No valid scheduling policy chosen for cpu simulation!. Supported simulation methods {','.join(lonnieOS.getSchedulingPolicies())}.\n{commandHelp}"
        )
        return None
    elif method == schedules[1]:
        if not quantum or (quantum > maxQuantum or quantum < minQuantum):  # type: ignore
            quantum = cpuMethodChoice("time quantum ", minQuantum, maxQuantum)
    elif method == schedules[2]:
        if not numOfQueues or (numOfQueues > maxNumOfQueues or numOfQueues < minNumOfQueues):  # type: ignore
            numOfQueues = cpuMethodChoice("number of queues ", minNumOfQueues, maxNumOfQueues)
    elif method == schedules[3]:
        if not quantum or (quantum > maxQuantum or quantum < minQuantum):  # type: ignore
            quantum = cpuMethodChoice("time quantum ", minQuantum, maxQuantum)
        if not numOfQueues or (numOfQueues > maxNumOfQueues or numOfQueues < minNumOfQueues):  # type: ignore
            numOfQueues = cpuMethodChoice("number of queues ", minNumOfQueues, maxNumOfQueues)

    numOfPcbs = lonnieOS.processes.size() - 1
    startTime = time.time()
    cpuLog = ""

    # run differnet cpu schedulers based on the user's choice 
    if method == schedules[0]:
        try:
            details = lonnieOS.runFIFOScheduler(useDebug)
            cpuLog += details["log"]
            print(details["metrics"])
        except Exception as err:
            printErrorMsg(f"{err}")
            return

    elif method == schedules[1]:
        try:
            details = lonnieOS.runRRScheduler(quantum, useDebug)  # type: ignore
            cpuLog += details["log"]
            print(details["metrics"])
        except Exception as err:
            printErrorMsg(f"{err}")
            return
    elif method == schedules[2]:
        try:
            details = lonnieOS.runMLFQScheduler(numOfQueues, useDebug)  # type: ignore
            cpuLog += details["log"]
            print(details["metrics"])
        except Exception as err:
            printErrorMsg(f"{err}")
            return
    elif method == schedules[3]:
        try:
            details = lonnieOS.runAllSchedulers(quantum,numOfQueues, useDebug)  # type: ignore
            cpuLog += details["log"]
            print(details["metrics"])
        except Exception as err:
            printErrorMsg(f"{err}")
            return

    with open("cpu-log.txt", "w", encoding="utf-8") as cpuLogfile:
        cpuLogfile.write(f"CPU SIMULATION.\n")
        cpuLogfile.write(f"{cpuLog}.\n")
        cpuLogfile.write(f"CPU SIMULATION FINISHED.\n")
        endTime = round(time.time() - startTime, 4)
        avgTime = round(endTime / numOfPcbs, 4)

        cpuLogfile.write(
            f"Total number of processes in ready queue -> {lonnieOS.readyQ.size()}.\n"
        )
        cpuLogfile.write(
            f"Total number of processes in blocked queue -> {lonnieOS.blockedQ.size()}.\n"
        )
        cpuLogfile.write(
            f"Total number of processes in the system -> {lonnieOS.processes.size()}.\n"
        )
        cpuLogfile.write(
            f"Number of Pcbs: {numOfPcbs}. Time taken {endTime} seconds. Avg time: {avgTime}s\n"
        )

    # displayMsg(cpuLog)
    printSuccessMsg(
        f"""
        CPU simulation complete.\n
        Number of Pcbs: {numOfPcbs}. Time taken {endTime} s. Avg time: {avgTime}s\n
        View 'cpu-log.txt' for more details.
        """
    )


# * --------- ALL SHELL COMMANDS MAPPED TO THEIR DESCRIPTION & FUNCTION --------------

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
        "help": f"create a new Process Control Block.\nUsage : [COMMAND] [--id]=[integer] [--memory]=[integer] [--type]=[{' | '.join(lonnieOS.getPcbTypes())}] \nRequired arguments --id (unique PCB id) , and --memory (PCB memory allocation).",
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
    "cpu": {
        "description": "run a cpu process simulation.",
        "help": f"run a cpu process simulation.\nUsage : [COMMAND]  [--method]=[{' | '.join(lonnieOS.getSchedulingPolicies())}]  --quantum=[integer] --queues=[integer].\nRequired argument --method (scheduling algorithm for cpu simulation).\nOptional arguments --quantum (how many time cycles the process stays in the CPU before being kicked out) and --queues (number of queues for Multilevel Feedback Queue simulation.)",
        "func": {"hasParams": True, "name": execute},
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
