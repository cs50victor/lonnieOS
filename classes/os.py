import random, json, copy
from classes.cpu import CPU
from classes.ioQ import IOQ
from classes.osPcb import OsPcb
from classes.mixedPcb import MixedPcb
from classes.cpuBoundPcb import CpuPcb
from classes.blockedQ import BlockedQ
from classes.readyQ import ReadyQ
from classes.processes import Processes
from classes.interactivePcb import InteractivePcb
from typing import List, Dict, Union

# * operating system
# * Provides an API for the user to perform OS/kernel functionalities through the shell

# note to self: need to fix turn around time, and response time calculations

class OS:
    def __init__(self) -> None:
        """
         the operating system class aggregates almost all 
         other classes.
        """
        # manages all system I/O events
        self.__ioQ = IOQ()
        # cpu processing
        self.__cpu = CPU()
        # manages all blocked processes
        self.blockedQ = BlockedQ()
        # manages all ready processes
        self.readyQ = ReadyQ()
        # main data structure that stores details and states of all processes
        self.processes = Processes()
        # minimum amount of memory needed to run OS
        self.__minSystemMem = 100
        # current system memory
        self.__systemMemory: float = 1001
        # all CPU execution methods
        self.__cpuExecMethods: list[str] = ["fifo", "round-robin", "mlfq", "all"]
        # types of pcbs
        self.__pcbTypes: list[str] = ["interactive", "cpu", "mixed"]
        # available pcb queues 
        self.__PCBQueues: list[str] = ["readyQ", "blockedQ"]
        # highest possible burst of a system process
        self.__maxCpuBurst = 10000
        # creates an OS process upon OS object creation
        self.__createOsPCB()

    def __createOsPCB(self) -> None:
        # Creates a reserved process for the operating system
        # OS uses id=0 as a reserved id for the OS PCB
        osPid, osMem = 0, 1
        osProcess = OsPcb(osPid, osMem)
        osProcess.setQueue(self.__PCBQueues[0])
        self.processes.add(osPid, osProcess)
        self.__systemMemory -= 1
        self.readyQ.enqueue(osPid, 0)

    def __roundMemory(self, mem) -> float:
        return round(mem, 1)

    def getPcbTypes(self) -> List[str]:
        # returns available OS pcb types
        return self.__pcbTypes

    def getSchedulingPolicies(self) -> List[str]:
        # returns available CPU execution methods
        return self.__cpuExecMethods

    def getMinMemory(self) -> float:
        # returns the minimum amount of memory needed to run the OS
        return self.__minSystemMem

    def getSystemMemory(self) -> float:
        # returns the system's current memoery
        return self.__roundMemory(self.__systemMemory - 1)

    def setSystemMemoryFromFile(self) -> None:
        # * Sets the system's memory by reading the memory.json file. Uses a fallback value if unsuccessful.
        fallBackMemMsg = (
            f"\nUsing fallback memory allocation - [{self.__systemMemory} MB]."
        )

        try:
            with open("memory.json") as json_file:
                data = json.load(json_file)
                mem = data["memory"]
                if isinstance(mem, int):
                    minMemoryRequired: float = self.getMinMemory()
                    if mem > minMemoryRequired:
                        self.__systemMemory = self.__roundMemory(mem)
                    else:
                        raise Exception(
                            f"Memory value must be > {minMemoryRequired}.{fallBackMemMsg}"
                        )
                else:
                    raise Exception(
                        f"Memory value in memory.json file must be an integer.{fallBackMemMsg}"
                    )
        except FileNotFoundError as err:
            raise FileNotFoundError(
                f"Memory file (memory.json) not found.{fallBackMemMsg}"
            ) from err
        except KeyError as err:
            raise Exception(
                f"Error reading memory file (memory.json). 'memory' key not found.{fallBackMemMsg}"
            ) from err

    def createPCB(
        self,
        pid: Union[int, None],
        memory: Union[float, None],
        pcbType: Union[str, None],
    ) -> None:
        # OS API: ALLOWS THE CREATION OF A NEW SYSTEM PROCESS
        # no memory provided or memory is not an integer.\n{commandHelp}\n

        if pid is None:
            raise ValueError(f"no PCB id provided or id is not an integer - pid={pid}.")
        elif pcbType is None or pcbType not in self.__pcbTypes:
            raise ValueError(
                f"no PCB type provided or type is not one of the following: {', '.join(self.__pcbTypes)} ."
            )
        elif memory is None:
            raise ValueError("no memory provided or memory is not an integer.")
        elif memory > self.getSystemMemory():
            raise ValueError(
                f"not enough memory to create PCB. Available Memory: {self.getSystemMemory()} MB"
            )

        memory = self.__roundMemory(memory)
        if pcbType == self.__pcbTypes[0]:
            process = InteractivePcb(pid, memory)
            self.processes.add(pid, process)
        elif pcbType == self.__pcbTypes[1]:
            process = CpuPcb(pid, memory)
            self.processes.add(pid, process)
        elif pcbType == self.__pcbTypes[2]:
            process = MixedPcb(pid, memory)
            self.processes.add(pid, process)

        self.__systemMemory -= memory
        self.readyQ.enqueue(pid, 0)

    def deletePCB(self, pid: Union[int, None]) -> str:
        # OS API: ALLOWS THE TERMINATION OF A SYSTEM PROCESS

        if pid is None:
            raise ValueError(f"no PCB id provided or id is not an integer - pid={pid}.")

        process = self.processes.retreive(pid)
        if process.getType() == "os":
            raise Exception("Can't delete PCB. PCB is a system process.")

        self.processes.remove(pid)
        self.__systemMemory += process.getMemory()
        q = process.getQueue()
        if q == self.__PCBQueues[0]:
            self.readyQ.remove(pid)
        elif q == self.__PCBQueues[1]:
            self.blockedQ.remove(pid)
        else:
            raise Exception("Can't delete PCB. PCB is in an invalid queue.")
        processInfo = f"{process}"
        process.delete()
        return processInfo

    def generatePCBs(self, num: Union[int, None]) -> None:
        # OS API: ALLOWS THE USER TO GENERATE A NUMBER OF RANDOM SYSTEM PROCESSES

        if num is None:
            raise ValueError(
                f"Error generating PCBs, no number provided or --num value is not an integer."
            )

        memory: float = 0.5
        maxProcess: int = int(self.getSystemMemory() / memory)

        if num > maxProcess:
            raise Exception(
                f"Not enough memory to create {num} PCBs. [ MAX # of PCBs - {maxProcess} ]"
            )

        startingPcbId = self.processes.getUniqueId()
        for _ in range(num):
            self.createPCB(startingPcbId, memory, random.choice(self.__pcbTypes))
            startingPcbId += 1

    def blockPCB(self, pid: Union[int, None]) -> str:
        # OS API: MOVES A SYSTEM PROCESS FROM THE READY QUEUE TO THE BLOCKED QUEUE
        # block a PCB by it's id
        # this function is to be only called from the shell command

        if pid is None:
            raise ValueError(f"no PCB id provided or id is not an integer - pid={pid}.")
        elif pid not in self.processes.getAllIds():
            raise ValueError(
                f"Error blocking PCB, process with id={pid} doesn't exist."
            )
        elif not self.readyQ.contains(pid):
            raise ValueError(
                f"Error blocking PCB, process with id={pid} isn't in ready queue."
            )
        process = self.processes.retreive(pid)
        if process.getType() == "os":
            raise Exception("Can't block PCB. PCB is a system process.")

        self.readyQ.remove(pid)
        self.blockedQ.enqueue(pid)
        process.setQueue(self.__PCBQueues[1])
        return f"{process}"

    def unblockPCB(self, el: Union[int, dict, None]) -> str:
        # OS API: MOVES A SYSTEM PROCESS FROM THE BLOCKED QUEUE TO THE READY QUEUE

        assert isinstance(el, (int, dict)) or (
            el == None
        ), "unblockPCB: Invalid parameter"

        pid = None
        if isinstance(el, int):
            pid = el
        elif isinstance(el, dict):
            pid = el["pid"]
        else:
            raise ValueError("Error unblocking PCB, invalid parameter.")
        # el has been validated

        if not isinstance(pid, int):
            raise ValueError(
                f"Error unblocking PCB, id wasn't provided or found in parameter. pid={pid}"
            )
        elif pid not in self.processes.getAllIds():
            raise ValueError(
                f"Error unblocking PCB, process with id={pid} doesn't exist."
            )
        elif self.readyQ.contains(pid):
            raise ValueError(
                f"Error unblocking PCB, process with id={pid} is in ready queue."
            )

        self.blockedQ.remove(el)
        process = self.processes.retreive(pid)
        priority = process.getPriority()
        self.readyQ.enqueue(pid, priority)
        process.setQueue(self.__PCBQueues[0])
        process.clearWT()
        return f"{process}"

    def __updateOtherPcbsWaitTime(self, pid: int) -> str:
        # private method used by CPU schedulers to
        # update the waiting time of system processes

        process = self.processes.retreive(pid)
        cpuBurst = process.getCpuBurst()
        contextSwitchTime = cpuBurst + 10
        for id in self.readyQ.getAll():
            if id != pid and process.getType() != "os":
                process.addWt(round(contextSwitchTime))
        return f"\tUpdated the Waiting Time of processes in the ready queue by {contextSwitchTime}.\n"

    def __makePcbNextDecision(self, pid: int, decision: int) -> str:
        # private method used by CPU schedulers to
        # make the next decision for a process exiting the CPU

        assert decision in [0, 1, 2, 3], "Invalid pcb decision value. 0<=decision>=3"

        log = ""
        process = self.processes.retreive(pid)
        cpuBurst = process.getCpuBurst()

        if decision == 0:
            print(f"PCB terminated - {process}")
            self.deletePCB(pid)
            log += (
                f"\tProcess id={pid} got terminated and was removed from the system.\n"
            )
        else:
            self.readyQ.dequeue()
            priority = process.getPriority()
            if decision == 1:
                self.readyQ.enqueue(pid, priority)
                log += "\tProcess returned to the ready queue to wait its turn.\n"
            elif decision == 2:

                process.setQueue(self.__PCBQueues[1])
                process.setBt(round(cpuBurst))
                process.setIot(round(cpuBurst))
                self.blockedQ.enqueue({"pid": pid, "type": "user", "time": cpuBurst})
                log += "\tProcess required a user I/O event and went into the blocked queue.\n"
            elif decision == 3:

                process.setQueue(self.__PCBQueues[1])
                process.setBt(round(cpuBurst))
                process.setIot(round(cpuBurst))
                self.blockedQ.enqueue(
                    {"pid": pid, "type": "hard-drive", "time": cpuBurst}
                )
                log += "\tProcess required a hard drive I/O event and went into the blocked queue.\n"
        return log

    def __generateIoEvents(self, pid: int, maxPossibleBurst: int) -> str:
        """"
            private method used by CPU schedulers to
            create a random number of I/O events.
            simulates I/O events created by the user using a system process
            (i.e user is typing while using a microsoft word process)
        """
        

        process = self.processes.retreive(pid)
        cpuBurst = round(process.getCpuBurst())
        numOfCreatedEvents = 0
        # print("\t...I/O events being generated.")
        for t in range(0, cpuBurst, 10):
            r = random.randint(0, 10)
            if r == 4:
                self.__ioQ.add({"type": "user", "time": t})
                numOfCreatedEvents += 1
            elif r == 9:
                self.__ioQ.add({"type": "hard-drive", "time": t})
                numOfCreatedEvents += 1

        # print("blocked queue", self.blockedQ.getAll())
        topBlockedPcb: Union[int, dict, None] = self.blockedQ.peek()
        if isinstance(topBlockedPcb, dict) and topBlockedPcb["time"] >= (
            maxPossibleBurst - 10
        ):
            self.__ioQ.add({"type": topBlockedPcb["type"], "time": maxPossibleBurst})

        return f"\tProcess generated {numOfCreatedEvents} I/O events.\n"

    def __satisfyIoRequests(self) -> str:
        """
            goes through the blocked queue and tries to find
            an I/O event created after the process is 
            sent to the blocked queue
        """

        # print("\t...Processes being unblocked.")
        satisfiedIoRequests = 0
        allBlockedPcbs = self.blockedQ.getAll()

        i = 0
        while i < len(allBlockedPcbs):
            blockedPdata = allBlockedPcbs[i]
            if isinstance(blockedPdata, dict):
                if self.__ioQ.satisfy(blockedPdata):
                    self.unblockPCB(blockedPdata)
                    satisfiedIoRequests += 1
                    i -= 1
            else:
                self.unblockPCB(blockedPdata)
            i += 1

        assert len(allBlockedPcbs) == i
        return f"\t satisfied {satisfiedIoRequests}/{self.blockedQ.size()} blocked processes."

    def runFIFOScheduler(self, debug: bool = False) -> Dict:
        # OS API: FIFO scheduling policy [default]
        """
            goes through the ready queue and 
            executes processes to completion in a First In First Out method
        """

        log = ""
        turnAroundT: float = 0
        responseT: float = 0
        cpuUtilization: float = 0
        pcbsProcessed: int = 0
        nonOsPCBs:int = 0

        while self.readyQ.size() != 1 or self.blockedQ.isNotEmpty():
            pcbsProcessed += 1

            pid = self.readyQ.peek()

            if debug:
                print(
                    f"\t|-Process [id={pid}] in CPU - readyQ-process:{self.readyQ.size()} blockedQ-process:{self.blockedQ.size()} i/o-events:{self.__ioQ.size()}"
                )

            self.__cpu.process(pid)
            log += f"\tPCB [pid: {pid}] is being processed by the CPU.\n"
            process = self.processes.retreive(pid)

            cpuBurst = random.randint(0, self.__maxCpuBurst - 1)
            process.setCpuBurst(cpuBurst)
            process.setMaxCpuBurst(cpuBurst)
            log += f"\tProcess [pid: {pid}]'s CPU burst time {cpuBurst} cycles.\n"

            log += self.__updateOtherPcbsWaitTime(pid)
            log += self.__generateIoEvents(pid, self.__maxCpuBurst)
            if debug:
                print(f"\t\tburst: {cpuBurst}, max I/O {round((cpuBurst/10)*0.2)+1}")
                print(
                    f"\t|-Process [id={pid}] exiting CPU - readyQ-process:{self.readyQ.size()} blockedQ-process:{self.blockedQ.size()} i/o-events:{self.__ioQ.size()}"
                )

            if process.getType() == "os":
                decision = 1
            else:
                decision = random.randint(0, 3)
            log += self.__makePcbNextDecision(pid, decision)
            log += self.__satisfyIoRequests()

            if process.getType() != "os":
                nonOsPCBs += 1
                # time spent in the cpu
                cpuUtilization += cpuBurst

            # T(response) = T(first) - T(arrival)
            responseT += process.getWt()
            # T(turnaround) = T(completion) - T(arrival)
            turnAroundT += cpuBurst

            log += f"\tProcess [pid: {pid}] left the CPU.\n"

        if pcbsProcessed == 0:
            raise Exception(
                "CPU can't run FIFO scheduler. Please create pcbs and try again."
            )
        avgTurnAround: float = round(turnAroundT / pcbsProcessed, 3)
        avgResponse: float = round(responseT / pcbsProcessed, 3)
        avgCpuUtil: float = round(cpuUtilization / nonOsPCBs, 3)

        metrics = f"\tAverages : Turn around-time {avgTurnAround} | Response time {avgResponse} | CPU utilization: 100% - {avgCpuUtil} burst].\n"
        log += metrics

        return {"log": log, "metrics": metrics}

    def runRRScheduler(self, quantum: Union[int, None], debug: bool = False) -> Dict:
        # OS API:  Round Robin scheduling policy
        """
            goes through the ready queue and 
            executes processes for a specified amount of time (quantum).
            terminates a process if the burst left is less than the specified quantum.
        """

        if quantum is None or quantum < 1:
            raise ValueError(f"Round Robin scheduler error. No time quantum provided.")

        log = ""
        turnAroundT: float = 0
        responseT: float = 0
        cpuUtilization: float = 0
        pcbsProcessed: int = 0
        nonOsPCBs:int = 0

        while self.readyQ.size() != 1 or self.blockedQ.isNotEmpty():
            pcbsProcessed += 1
            pid = self.readyQ.peek()

            shouldExit = False

            if debug:
                print(
                    f"\t|-Process [id={pid}] in CPU - readyQ-process:{self.readyQ.size()} blockedQ-process:{self.blockedQ.size()} i/o-events:{self.__ioQ.size()}"
                )

            self.__cpu.process(pid)
            log += f"\tPCB [pid: {pid}] is being processed by the CPU.\n"
            process = self.processes.retreive(pid)

            currQuantum = quantum

            if process.getType() != "os":
                cpuBurstLeft = process.getMaxCpuBurst()
                if cpuBurstLeft < 0:
                    raise ValueError(
                        f"PCB [pid: {pid}] is shouldn't no longer be in the system. Negative burst time.\n"
                    )
                elif cpuBurstLeft == 0:
                    # First arrival in CPU
                    cpuBurstLeft = random.randint(1, self.__maxCpuBurst - 1)

                if cpuBurstLeft > quantum:
                    cpuBurstLeft -= quantum
                    process.setMaxCpuBurst(cpuBurstLeft)
                elif cpuBurstLeft <= currQuantum:
                    currQuantum = cpuBurstLeft
                    process.setMaxCpuBurst(currQuantum)
                    shouldExit = True

            process.setCpuBurst(currQuantum - 1)
            log += f"\tProcess [pid: {pid}]'s CPU burst time {currQuantum} cycles.\n"

            log += self.__updateOtherPcbsWaitTime(pid)
            log += self.__generateIoEvents(pid, quantum)
            if debug:
                print(
                    f"\t\tburst: {currQuantum}, max I/O {round((currQuantum/10)*0.2)+1}"
                )
                print(
                    f"\t|-Process [id={pid}] exiting CPU - readyQ-process:{self.readyQ.size()} blockedQ-process:{self.blockedQ.size()} i/o-events:{self.__ioQ.size()}"
                )

            if process.getType() == "os":
                decision = 1
            elif shouldExit:
                decision = 0
            else:
                decision = random.randint(1, 3)
            log += self.__makePcbNextDecision(pid, decision)

            if pcbsProcessed % 2 == 0:
                log += self.__satisfyIoRequests()

            if process.getType() != "os":
                nonOsPCBs += 1
                # time spent in the cpu
                cpuUtilization += currQuantum

            # T(response) = T(first) - T(arrival)
            responseT += process.getWt()
            # T(turnaround) = T(completion) - T(arrival)
            turnAroundT += currQuantum

            log += f"\tProcess [pid: {pid}] left the CPU.\n"

        if pcbsProcessed == 0:
            raise Exception(
                "CPU can't run Round-Robin scheduler. Please create pcbs and try again."
            )
        avgTurnAround: float = round(turnAroundT / pcbsProcessed, 3)
        avgResponse: float = round(responseT / pcbsProcessed, 3)
        avgCpuUtil: float = round(cpuUtilization / nonOsPCBs, 3)

        metrics = f"\tAverages : Turn around-time {avgTurnAround} | Response time {avgResponse} | CPU utilization: 100% - {avgCpuUtil} burst].\n"
        log += metrics

        return {"log": log, "metrics": metrics}

    def runMLFQScheduler(
        self, numOfQueues: Union[int, None], debug: bool = False
    ) -> Dict:
        # OS API:  MLFQ scheduling policy
        """
            goes through the ready queue and 
            executes processes for a specified amount of time (quantum).
            terminates a process if the burst left is less than the specified quantum.
        """
        

        if numOfQueues is None or numOfQueues < 1:
            raise ValueError(
                f"Multi level feedback scheduler error. Invalid number of queues provided."
            )

        log = ""
        turnAroundT: float = 0
        responseT: float = 0
        cpuUtilization: float = 0
        pcbsProcessed: int = 0
        nonOsPCBs:int = 0

        maxReadyQueueSize = self.readyQ.size()

        baseQuantum = self.__maxCpuBurst / numOfQueues
        queues = {}
        for queue in range(numOfQueues):
            # maxQuantum = n+1 * baseQuantum
            # level: maxQuantum
            queues[queue] = (queue + 1) * baseQuantum

        while self.readyQ.size() != 1 or self.blockedQ.isNotEmpty():
            pcbsProcessed += 1
            pid = self.readyQ.peek()
            shouldExit, lowerPriority = False, False
            self.__cpu.process(pid)

            process = self.processes.retreive(pid)
            currPCBPriority = process.getPriority()
            quantum = queues[currPCBPriority]
            log += f"\tPCB [pid: {pid} , priority queue: {currPCBPriority}] is being processed by the CPU.\n"
            if debug:
                print(
                    f"\t|-Process [id={pid}, priority queue: {currPCBPriority}] in CPU - readyQ-process:{self.readyQ.size()} blockedQ-process:{self.blockedQ.size()} i/o-events:{self.__ioQ.size()}"
                )

            currQuantum = quantum

            cpuBurstLeft = process.getMaxCpuBurst()
            if cpuBurstLeft < 0:
                raise ValueError(
                    f"PCB [pid: {pid}] is shouldn't no longer be in the system. Negative burst time.\n"
                )
            elif cpuBurstLeft == 0:
                #  MLFQ RULE 3
                # First arrival in CPU
                cpuBurstLeft = random.randint(1, self.__maxCpuBurst - 1)

            if cpuBurstLeft > quantum:
                cpuBurstLeft -= quantum
                process.setMaxCpuBurst(cpuBurstLeft)
                #  MLFQ RULE 4
                # reduce priority fo current process
                lowerPriority = currPCBPriority + 1
                process.setPriority(lowerPriority)
                log += f"\tPCB [pid: {pid} , priority queue: {currPCBPriority}] has been downgraded to queue {lowerPriority}.\n"

                if debug:
                    print(log)

            elif cpuBurstLeft <= currQuantum:
                if process.getType() != "os":
                    currQuantum = cpuBurstLeft
                    process.setMaxCpuBurst(currQuantum)
                    shouldExit = True
                else:
                    # reset os pcb
                    osNewBurst = random.randint(1, self.__maxCpuBurst - 1)
                    process.setMaxCpuBurst(osNewBurst)

            process.setCpuBurst(currQuantum - 1)
            log += f"\tProcess [pid: {pid}]'s CPU burst time {currQuantum} cycles.\n"

            log += self.__updateOtherPcbsWaitTime(pid)
            log += self.__generateIoEvents(pid, quantum)
            if debug:
                print(
                    f"\t\tburst: {currQuantum}, max I/O {round((currQuantum/10)*0.2)+1}"
                )
                print(
                    f"\t|-Process [id={pid}] exiting CPU - readyQ-process:{self.readyQ.size()} blockedQ-process:{self.blockedQ.size()} i/o-events:{self.__ioQ.size()}"
                )

            if process.getType() == "os":
                decision = 1
            elif shouldExit:
                decision = 0
            else:
                decision = random.randint(1, 3)
            log += self.__makePcbNextDecision(pid, decision)

            if pcbsProcessed % 2 == 0:
                log += self.__satisfyIoRequests()

            if process.getType() != "os":
                nonOsPCBs += 1
                # time spent in the cpu
                cpuUtilization += currQuantum
            
            # T(response) = T(first) - T(arrival)
            responseT += process.getWt()
            # T(turnaround) = T(completion) - T(arrival)
            turnAroundT += currQuantum

            if maxReadyQueueSize % (pcbsProcessed * 0.9) == 0:
                # MLFQ RULE 4
                # moves all processes to the topmost queue when all processes might have had a chance to get processed
                for id in self.processes.getAllIds():
                    pcb = self.processes.retreive(id)
                    if pcb.getPriority() != 0:
                        pcb.setPriority(0)

            log += f"\tProcess [pid: {pid}] left the CPU.\n"

        if pcbsProcessed == 0:
            raise Exception(
                "CPU can't run MLFQ scheduler. Please create pcbs and try again."
            )
        avgTurnAround: float = round(turnAroundT / pcbsProcessed, 3)
        avgResponse: float = round(responseT / pcbsProcessed, 3)
        avgCpuUtil: float = round(cpuUtilization / nonOsPCBs, 3)

        metrics = f"\tAverages : Turn around-time {avgTurnAround} | Response time {avgResponse} | CPU utilization: 100% - {avgCpuUtil} burst].\n"
        log += metrics

        return {"log": log, "metrics": metrics}

    def runAllSchedulers(
        self,
        quantum: Union[int, None],
        numOfQueues: Union[int, None],
        debug: bool = False,
    ) -> Dict:
        # OS API:  RUN and Compare all CPU scheduling policies  
        """
            runs all CPU schedulers and  displays a summary.
            returns a combination of all scheduling metrics 
        """

        # Verify parameter
        assert (
            isinstance(quantum, int) or quantum is None
        ), "Invalid runAllSchedulers parameters"
        assert (
            isinstance(numOfQueues, int) or numOfQueues is None
        ), "Invalid runAllSchedulers parameters"

        #* THIS SAVES THE CURRENT STATE OF THE OPERATING SYSTEM
        #* by making a copy of the essential datastructures
        pcbCopy = copy.deepcopy(self.processes)
        readyQCopy = copy.deepcopy(self.readyQ)
        memoryCopy = self.__systemMemory

        #* Runs the FIFO scheduler
        schedulerType: str = "FIFO SCHEDULER"
        log: str = f"\n\t_____{schedulerType} LOG_____\n"
        m1: str = f"\n\t_____{schedulerType} METRICS_____\n"
        schedulerData: dict = self.runFIFOScheduler(debug)
        m1 += schedulerData["metrics"]
        log += schedulerData["log"] + m1
        
        #* restores the operating system's previous state
        #* needed to run the next scheduler
        self.processes = copy.deepcopy(pcbCopy)
        self.readyQ = copy.deepcopy(readyQCopy)
        self.__ioQ.clear()
        self.__systemMemory = memoryCopy

        #* Runs the ROUND ROBIN scheduler
        schedulerType = "ROUND ROBIN SCHEDULER"
        log += f"\n\t_____{schedulerType} LOG_____\n"
        m2 = f"\n\t_____{schedulerType} METRICS_____\n"
        schedulerData: dict = self.runRRScheduler(quantum, debug)
        m2 += schedulerData["metrics"]
        log += schedulerData["log"] + m2

        #* restores the operating system's previous state
        #* needed to run the next scheduler
        self.processes = copy.deepcopy(pcbCopy)
        self.readyQ = copy.deepcopy(readyQCopy)
        self.__ioQ.clear()
        self.__systemMemory = memoryCopy

        #* Runs the MULTI-LEVEL FEEDBACK QUEUE SCHEDULER
        schedulerType = "MULTI-LEVEL FEEDBACK QUEUE SCHEDULER"
        log += f"\n\t_____{schedulerType} LOG_____\n"
        m3  = f"\n\t_____{schedulerType} METRICS_____\n"
        schedulerData: dict = self.runMLFQScheduler(numOfQueues, debug)
        m3 += schedulerData["metrics"]
        log += schedulerData["log"] + m3

        metrics = m1+m2+m3
        log += f"\n\tALL SCHEDULER METRICS:\n{metrics}"
        
        # returns a combination of all metrics
        return {"log": log, "metrics": metrics}
