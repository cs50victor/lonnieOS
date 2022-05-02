from typing import Union


# * Parent class inherited by all other PCB classes
# Not used directly by the Operating System

class PCB:
    def __init__(self, id: int, memory: float):
        # the unique id of the PCB
        self.__pid = id
        # the amount of time needed by the process for a created I/O
        self.__ioCycles: int = 0
        # amount of time the process is currently using the CPU
        self.__cpuBurst: float = 0
        # amount of time the process will use the CPU
        self.__maxCpuBurst: float = 0
        # amount of time the PCB is waiting to be processed by the CPU
        self.__waitCycles: int = 0
        # time spent by the process in the blocked Queue
        self.__blockedTime: int = 0
        # the memory used by the process
        self.__memory = memory
        # the current queue of the process
        self.__queue: str = "readyQ"
        # the current priority of the process
        self.__priority = 0

    
    # Setters and Gettera

    # Getters
    def getPid(self) -> int:
        return self.__pid

    def getIot(self) -> int:
        return self.__ioCycles

    def getCpuBurst(self) -> float:
        return self.__cpuBurst
    
    def getMaxCpuBurst(self) -> float:
        return self.__maxCpuBurst

    def getWt(self) -> int:
        return self.__waitCycles

    def getBt(self) -> int:
        return self.__blockedTime

    def getMemory(self) -> float:
        return self.__memory

    def getQueue(self) -> str:
        return self.__queue

    def getPriority(self)->int:
        return self.__priority

    # Setters with parameter validation


    def setPriority(self, priority: int) -> None:
        if not isinstance(priority, int):
            raise ValueError(
                "Error changing process's priority, can only change to an integer."
            )
        self.__priority = priority

    def setIot(self, time: int) -> None:
        if not isinstance(time, int):
            raise ValueError(
                "Error setting process I/O term, can only set to an integer."
            )
        self.__ioCycles = time

    def setBt(self, time: int) -> None:
        if not isinstance(time, int):
            raise ValueError(
                "Error setting process blocked time, can only set to an integer."
            )
        self.__blockedTime = time

    def setQueue(self, queue) -> None:
        if queue not in ["readyQ", "blockedQ"]:
            raise ValueError("Error updating process queue. Invalid queue name.")
        self.__queue = queue

    def setCpuBurst(self, time: Union[int,float]) -> None:
        if not isinstance(time, (int,float)):
            raise ValueError(
                "Error increasing process cpu usage term, can only increase by an integer/float."
            )
        self.__cpuBurst = float(time)
    
    def setMaxCpuBurst(self, time: Union[int,float]) -> None:
        if not isinstance(time, (int, float)):
            raise ValueError(
                "Error increasing process's max cpu usage term, can only set value to an integer/float."
            )
        self.__maxCpuBurst = float(time)

    def addWt(self, time: int) -> None:
        if not isinstance(time, int):
            raise ValueError(
                "Error increasing process waiting term, can only increase by an integer."
            )
        self.__waitCycles += time

    def clearWT(self):
        self.__waitCycles = 0

    def delete(self) -> None:
        # 'deletes' the pcb 
        self.__ioCycles = 0
        self.__cpuBurst = 0
        self.__waitCycles = 0
        self.__memory = 0

    def __str__(self) -> str:
        # returns details of this PCB when printed in the shell
        id = self.__pid
        cpu = round(self.__maxCpuBurst,4)
        io = self.__ioCycles
        wt = self.__waitCycles
        mem = self.__memory
        q = self.__queue
        p = self.__priority
        return f"PID: {id}, Priority {p}, {mem} MB, Burst/Times [CPU: {cpu}, I/O: {io}, Waiting: {wt}], {q}"
