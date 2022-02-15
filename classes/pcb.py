class PCB:
    def __init__(self, id:int, memory:int):
        self.pid = id
        self.ioCycles = 0
        self.cpuCycles = 0
        self.waitCycles = 0
        self.memory = memory
    
    def getPid(self):
        return self.pid

    def getIoCycles(self):
        return self.ioCycles
    
    def updateIoCycles(self, value):
        if (not isinstance(value,int) and not isinstance(value,float) ):
            raise ValueError("Error increasing process I/O term, can only increase by an integer/float.")
        self.ioCycles += value

    def getCpuCycles(self):
        return self.cpuCycles

    def updateCpuCycles(self, value: int):
        if (not isinstance(value,int)):
            raise ValueError("Error increasing process cpu usage term, can only increase by an integer.")
        self.cpuCycles += value

    def getWaitCycles(self):
        return self.waitCycles

    def updateWaitCycles(self, value):
        if (not isinstance(value,int) and not isinstance(value,float) ):
            raise ValueError("Error increasing process waiting term, can only increase by an integer/float.")
        self.waitCycles += value
    
    def getMemory(self):
        return self.memory 
        
    def clear(self):
        self.ioCycles = 0
        self.cpuCycles = 0
        self.waitCycles = 0
        self.memory = 0

