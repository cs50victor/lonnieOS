from .pcb import PCB

# * A process reserved by the Operating System..
# Very important PCB as it is used in all CPU scheduling methods


class OsPcb(PCB):
    def __init__(self, id: int, memory: float):
        super().__init__(id, memory)
        self.__type = "os"

    def getType(self) -> str:
        return self.__type

    def __str__(self) -> str:
        # returns details of this PCB when printed in the shell
        return f"{super().__str__()}, Type: {self.__type}"
