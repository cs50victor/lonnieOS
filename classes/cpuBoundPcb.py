from .pcb import PCB

class CpuPcb(PCB):
    def __init__(self, id, memory):
        super().__init__(id, memory)
        self.__type = "cpu"
    
    def getType():
        return self.__type