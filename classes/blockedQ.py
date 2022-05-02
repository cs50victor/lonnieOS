from typing import Union

# Manages all process entering and leaving the blocked queue.
# stores process id's and dict containing an id with the io details


class BlockedQ:
    def __init__(self) -> None:
        self.__queue = []

    def isEmpty(self) -> bool:
        # checks if there are no process in the blocked queue.

        return not self.__queue

    def isNotEmpty(self) -> bool:
        # checks if there are any process in the blocked queue.

        return not self.isEmpty()

    def peek(self) -> Union[int, dict, None]:
        # returns the first process in the process queue
        # if no process are in the blocked queue it returns None

        if self.isEmpty():
            return None
        return self.__queue[0]

    def enqueue(self, el: Union[int, dict]) -> None:
        # adds a process to the blocked queue

        # element validation
        if not isinstance(el, (int, dict)):
            raise ValueError(
                "Error blocking process. Must be a hashmap(dict) or integer."
            )
        elif isinstance(el, dict):
            if not isinstance(el.get("pid"), int):
                raise ValueError("Error blocking process. Processing id wasn't found.")
            elif el["pid"] in self.__queue:
                raise Exception("Error blocking process. PCB is already blocked.")
            elif not isinstance(el.get("time"), (int, float)):
                raise ValueError("Error blocking process. I/O time/burst wasn't found.")
            elif el["time"] < 0:
                raise ValueError(
                    "Error blocking process. I/O time/burst can't be lower than 0."
                )
        elif el in self.__queue:
            raise Exception("Error blocking process. PCB is already blocked.")

        self.__queue.append(el)

    def dequeue(self) -> Union[int, dict]:
        # removes the first process from the blocked queue

        if self.isEmpty():
            raise IndexError("Blocked queue is empty!")

        return self.__queue.pop(0)

    def remove(self, el: Union[int, dict]) -> None:
        #! breaks the FIFO rule of a queue
        # removes an element from the queue regardless of its position

        if not isinstance(el, (int, dict)):
            raise ValueError(
                "Error removing process from blocked queue. Must be a hashmap(dict) or integer."
            )

        try:
            self.__queue.remove(el)
        except ValueError as err:
            raise Exception(
                "Error removing process from blocked queue. Process is not in blocked queue."
            ) from err

    def getAll(self) -> list:
        # returns all processes in the blocked queue
        return self.__queue

    def size(self) -> int:
        # returns the number of processes in the blocked queue

        return len(self.__queue)
