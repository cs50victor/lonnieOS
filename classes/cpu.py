# Stores the id of the PCB being processed by the CPU
#* Manages processes entering and leaving the cpu

class CPU():
    def __init__(self):
        self.currProcess:list[int] = []
    
    def process(self, processId:int)->None:
        # add a process to the CPU
        
        # ensures that only one PCB is being processed 
        # by the CPU at any given time

        if self.currProcess:
            self.currProcess.pop(0)
        self.currProcess.append(processId)
    