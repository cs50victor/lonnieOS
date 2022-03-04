from .pcb import PCB

class OsPcb(PCB):
    def __init__(self, id, memory):
        super().__init__(id, memory)
        self.__type = "os"
    
    def getType():
        return self.__type


    