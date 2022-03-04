from .pcb import PCB

class MixedPcb(PCB):
    def __init__(self, id, memory):
        super().__init__(id, memory)
        self.type = "mixed"
    
    def getType():
        return self.__type