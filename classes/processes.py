from typing import List, Dict, Union
from classes.osPcb import OsPcb
from classes.mixedPcb import MixedPcb
from classes.cpuBoundPcb import CpuPcb
from classes.interactivePcb import InteractivePcb

#* Manages all process in the operating system

class Processes:
    def __init__(self) -> None:
        self.__processes:Dict = {}
        self.__processIds:list[int] = []

    def isNotEmpty(self)-> bool:
        #* Checks if operating system has any running processes 
        return self.size()>0

    def getUniqueId(self)->int:
        # returns a unique id 
        maxPid = sorted(self.__processes.keys())[-1]
        return maxPid+1

    def getAllIds(self) -> List[int]:
        return self.__processIds

    def getSortedIds(self) -> List[int]:
        return sorted(self.__processIds)
    
    def retreive(self, id:int) -> Union[MixedPcb,CpuPcb,InteractivePcb]:
        # get the details of a process

        if id not in self.__processIds:
            raise Exception("Error retreiving process. Process with id doesn't exist.")
        return self.__processes[id]

    def add(self, id:int, process:Union[OsPcb,MixedPcb,CpuPcb,InteractivePcb]) -> None:
        if id in self.__processIds:
            raise Exception(f"Error creating process. Process with id {id} already exist.")
        
        if (not isinstance(process,(OsPcb,MixedPcb,CpuPcb,InteractivePcb))):
            raise Exception("Error creating process. Invalid Process type.")

        self.__processes[id] = process
        self.__processIds.append(id)

    def remove(self, id:int) -> Union[MixedPcb,CpuPcb,InteractivePcb]:
        # removes a process 

        try:
            process = self.__processes.pop(id)
            self.__processIds.remove(id)
        except KeyError as err:
            raise Exception(f"Can't remove process. Process with id {id} doesn't exist.") from err
        
        return process
    
    def size(self) -> int:
        # returns the number of processes in the system
        
        return len(self.__processIds)

    