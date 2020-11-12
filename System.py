from State import State

class System:
    def __init__(self, numberMachine, machines, buffers):
        self.numberMachine = numberMachine
        self.numberBuffer = numberMachine - 1
        self.historicState = []
        self.machines = machines
        self.buffers = buffers
        self.currentState = State(self.machines,self.buffers)
    
    def getMachines(self):
        return self.machines
    def getBuffers(self):
        return self.buffers
    def setCommonCapacity(self, value):
        for element in self.buffers:
            element.setCapacity(value)
        
    def getCurrentState(self):
        return self.currentState
    def getHistoricState(self):
        return self.historicState
    def resetHistoric(self):
        self.historicState.clear()
    def resetSystem(self):
        for element in self.buffers:
            element.reset()
    
        
