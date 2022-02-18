class PCB:
    def __init__(self, id: int, memory: int):
        self.__pid = id
        self.__ioCycles = 0
        self.__cpuCycles = 0
        self.__waitCycles = 0
        self.__blockedTime = 0
        self.__memory = memory

    def getPid(self) -> int:
        return self.__pid

    def getIot(self) -> int:
        return self.__ioCycles

    def getCpuT(self) -> int:
        return self.__cpuCycles

    def getWt(self) -> int:
        return self.__waitCycles

    def getBt(self) -> int:
        return self.__blockedTime

    def getMemory(self) -> int:
        return self.__memory

    def setIot(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError(
                "Error setting process I/O term, can only set to an integer."
            )
        self.__ioCycles = value

    def setBt(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError(
                "Error setting process blocked time, can only set to an integer."
            )
        self.__blockedTime = value

    def addCpuT(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError(
                "Error increasing process cpu usage term, can only increase by an integer."
            )
        self.__cpuCycles += value

    def addWt(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError(
                "Error increasing process waiting term, can only increase by an integer."
            )
        self.__waitCycles += value

    def delete(self) -> None:
        self.__ioCycles = 0
        self.__cpuCycles = 0
        self.__waitCycles = 0
        self.__memory = 0


"""
@property
def name(self):

@name.setter
def name(self,newname):
"""
