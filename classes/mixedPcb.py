from .pcb import PCB

#* The default process create by a process. 
# kind of a mix between CPU and I/O bound processes.
 
class MixedPcb(PCB):
    def __init__(self, id:int, memory:float):
        super().__init__(id, memory)
        self.__type = "mixed"
    
    def getType(self)->str:
        return self.__type
    
    def __str__(self) -> str:
        # returns details of this PCB when printed in the shell
        return f"{super().__str__()}, Type: {self.__type}"