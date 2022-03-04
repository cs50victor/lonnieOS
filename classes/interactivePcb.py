from .pcb import PCB

class InteractivePcb(PCB):
    def __init__(self, id, memory):
        super().__init__(id, memory)
        self.__type = "interactive"
    
    def getType():
        return self.__type