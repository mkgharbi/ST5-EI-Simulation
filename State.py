
class State:
    def __init__(self,machines,buffers):
        self.state = self.generateState(machines,buffers)
        

    def generateState(self,machines, buffers):
        state =[]
        for i in range(len(machines)):
            state.append(machines[i])
            if (i < len(machines)-1):
                state.append(buffers[i])
        return state
    
    def getState(self):
        return self.state

    def __str__(self):
        result = 'State = ( '
        for state in range(self.state):
            result += str(state)
        result += ' )'
        return f'{result}'
