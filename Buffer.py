from MachineLine import MachineLineNode
from enum import Enum

class Buffer (MachineLineNode):
    
    class Type (Enum):
        MIDDLE = 0
        INPUT = 1
        OUTPUT = 2
        INPUT_COUNTER = 3
        OUTPUT_COUNTER = 4
    
    def __init__ (self, buffer_type, capacity, name):
        self.type = buffer_type
        if self.type == Buffer.Type.MIDDLE: self.capacity = capacity
        super(Buffer, self).__init__(name)  
        self.reset()
    
    def reset (self):
        if self.type in [Buffer.Type.MIDDLE, Buffer.Type.INPUT_COUNTER, Buffer.Type.OUTPUT_COUNTER]: self.current = 0
    
    def is_full (self):
        if self.type == Buffer.Type.MIDDLE:
            return self.current == self.capacity
        elif self.type in [Buffer.Type.OUTPUT, Buffer.Type.OUTPUT_COUNTER]:
            return False
    
    def is_empty (self):
        if self.type == Buffer.Type.MIDDLE:
            return self.current == 0
        elif self.type in [Buffer.Type.INPUT, Buffer.Type.INPUT_COUNTER]:
            return False
    
    def pop (self):
        if self.type in [Buffer.Type.MIDDLE, Buffer.Type.INPUT_COUNTER]:
            self.current -= 1

    def push (self):
        if self.type in [Buffer.Type.MIDDLE, Buffer.Type.OUTPUT_COUNTER]:
            self.current += 1

    def getCurrent(self):
        return self.current

    def getCapacity(self):
        return self.capacity
    
    def setCapacity(self, value):
        self.capacity = value
    
    def incrementCapacity(self):
        self.capacity += 1
    
    def __str__ (self):
        if self.type == Buffer.Type.MIDDLE:
            return f', {self.name}' + f' - {self.current}/{self.capacity}, '
        elif self.type in [Buffer.Type.INPUT, Buffer.Type.OUTPUT]:
            return f'{self.name}' + f' - {"INPUT" if self.type == Buffer.Type.INPUT else "OUTPUT"}'
        elif self.type in [Buffer.Type.INPUT_COUNTER, Buffer.Type.OUTPUT_COUNTER]:
            return f'{self.name}' + f' - {"INPUT " if self.type == Buffer.Type.INPUT_COUNTER else "OUTPUT "} {self.current}, '

INPUT_BUF = Buffer(Buffer.Type.INPUT, 0, "INPUT")                       # MUST BE USED AS INPUT BUFFER OF THE MACHINE LINE
INPUT_CNT_BUF = Buffer(Buffer.Type.INPUT_COUNTER, 0, "INPUT_CNT")       # MUST BE USED AS INPUT BUFFER OF THE MACHINE LINE
OUTPUT_BUF = Buffer(Buffer.Type.OUTPUT, 0, "OUTPUT")                    # MUST BE USED AS OUTPUT BUFFER OF THE MACHINE LINE
OUTPUT_CNT_BUF = Buffer(Buffer.Type.OUTPUT_COUNTER, 0, "OUTPUT_CNT")    # MUST BE USED AS OUTPUT BUFFER OF THE MACHINE LINE
