# only supported in Python versions >= 3.6
from collections import OrderedDict
from operator import itemgetter

# Manages all process entering and leaving the ready queue.
# stores all the process ids and their priority in a dictionary 
# but is used as to a queue and heap - ish

class ReadyQ:
    def __init__(self) -> None:
        # {"id": priority:int }
        # using OrderedDict to preserve key insertion order
        self.__queue: dict[int, int] = OrderedDict()

    def __getAllIds(self):
        # return a sorted list of process id's. in order of priority
        return [
            sortedDict[0]
            for sortedDict in sorted(self.__queue.items(), key=itemgetter(1))
        ]

    def isEmpty(self) -> bool:
        # checks if there are no process in the ready queue.

        return not self.__queue

    def isNotEmpty(self) -> bool:
        # checks if there are any process in the ready queue.
        return not self.isEmpty()

    def peek(self) -> int:
        # returns the first process in the process queue

        if self.isEmpty():
            raise KeyError("Can't peek into Ready queue. Currently empty!")

        return self.__getAllIds()[0]

    def enqueue(self, pid: int, priority: int) -> None:
        # adds a process to the ready queue

        if not isinstance(pid, int):
            raise ValueError(
                "Error enqueueing process. Please provide the PCB pid [integer]."
            )
        elif not isinstance(priority, int):
            raise ValueError(
                "Error enqueueing process. Please provide the PCB priority [integer]."
            )
        elif pid in self.__queue:
            raise Exception("Error enqueueing process. PCB is already in ready queue.")

        #  sets the default priority of all
        self.__queue[pid] = priority

    def dequeue(self) -> None:
        # removes the first process from the ready queue
        try:
            firstIndex = self.peek()
            self.remove(firstIndex)
        except Exception as err:
            raise Exception(
                f"Error performing Dequeue on Ready Queue .more details - {err}"
            ) from err

    def remove(self, pid: int) -> None:
        # remove a process from the ready queue
        # this function breaks the FIFO rule of a queue

        if not isinstance(pid, int):
            raise ValueError(
                "Error removing process from ready queue. Must be a hashmap or integer."
            )

        try:
            del self.__queue[pid]
        except KeyError as err:
            raise Exception(
                "Error removing process from ready queue. Process is not in ready queue."
            ) from err

    def contains(self, pid: int) -> bool:
        # checks if a process is in the ready queue  

        value = self.__queue.get(pid)
        # using None because a pid could be 0
        # and 0 is a falsy value

        if value == None:
            return False
        else:
            return True

    def getAll(self) -> list:
        # get all processes in the ready queue

        return self.__getAllIds()

    def getAllIdsUnsorted(self) -> list:
        # returns all the keys in their unsorted order
        return list(self.__queue.keys())

    def size(self) -> int:
        # returns the number of processes in the ready queue

        return len(self.__queue)
