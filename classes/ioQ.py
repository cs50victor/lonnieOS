"""
    Every process generates an I/O event,
    it would be useless if a program doesn't 
    accept input or display output to the user 
"""
import heapq


# This class manages all I/O events created and deleted by a 'USER' 
# when using the operating system
# saves the I/O times in two min-heap datastructures

class IOQ:
    def __init__(self) -> None:
        self.__uIo = []
        self.__hdIo = []
        heapq.heapify(self.__uIo)
        heapq.heapify(self.__hdIo)

    def add(self, io:dict)->None:
        # adds a created I/O event to 
        # one of two min-heap based on it's type
        if io["type"] == "user":
            heapq.heappush(self.__uIo,io["time"])
        else:
            heapq.heappush(self.__hdIo,io["time"])
    
    def satisfy(self, io:dict)->bool:
        # this removes the io event at the top of the min-heap
        # until an one with a higher time than a
        # processes' I/O is seen in the heap

        if io["type"] == "user":
            while self.__uIo:
                currIOTime = heapq.heappop(self.__uIo)
                if currIOTime > io["time"]:
                    return True
            return False
        else:
            while self.__hdIo:
                currIOTime = heapq.heappop(self.__hdIo)
                if currIOTime > io["time"]:
                    return True
            return False
    
    def size(self)->int:
        # returns the total number of I/O events are in the system
        return len(self.__uIo) + len(self.__hdIo)
    
    def clear(self)->None:
        # deletes all I/O events 

        self.__uIo.clear()
        self.__hdIo.clear()



        


 