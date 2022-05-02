from .pcb import PCB

#* This process is 3x MORE likely to need user I/O during execution.

class InteractivePcb(PCB):
    def __init__(self, id:int, memory:float):
        super().__init__(id, memory)
        self.__type = "interactive"
    
    def getType(self)->str:
        return self.__type
    
    def __str__(self) -> str:
        # returns details of this PCB when printed in the shell
        return f"{super().__str__()}, Type: {self.__type}"