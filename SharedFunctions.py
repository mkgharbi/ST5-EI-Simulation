def probabilityBreakdownInput(j):
    while True:
        try:
            firstInput = float(input("Enter the breakdown probability of machine " + str(j+1) + " : "))
            if 0 <= firstInput <= 1:
                return (firstInput)
            print("Please try again, it must be a number between 0 and 1")
        except ValueError:
            print("Input must be numeric.")

def probabilityRepairInput(j):
    while True:
        try:
            firstInput = float(input("Enter the repair probability of machine " + str(j+1) + " : "))
            if 0 <= firstInput <= 1:
                return (firstInput)
            print("Please try again, it must be a number between 0 and 1")
        except ValueError:
            print("Input must be numeric.")

def bufferInput(j):
    while True:
        try:
            firstInput = int(input("Enter the buffer size of buffer " + str(j+1) + " : "))
            if 1 <= firstInput:
                return (firstInput)
            print("Please try again, it must be equal or greater to 1")
        except ValueError:
            print("Input must be integer.")

def generateStringState(system):
    result = 'State = ( '
    for i in range(len(system.getCurrentState().getState())):
        result += str(system.getCurrentState().getState()[i])
    result += ' )'
    return result


def generateSummarizedState(system, differenceOutput, differenceInput):
    summarizedState = []
    for index in range(len(system.getCurrentState().getState())):
        if (index % 2 == 0): # Machine case 
            summarizedState.append(system.getCurrentState().getState()[index].getIs_Up())
        else: # buffer case 
            summarizedState.append(system.getCurrentState().getState()[index].getCurrent())
            summarizedState.append(system.getCurrentState().getState()[index].getCapacity())
    summarizedState.append(differenceOutput)
    summarizedState.append(differenceInput)
    return summarizedState


def simulatingAStep(system):
    for machine in system.getMachines():
        machine.phase_1_rand()
    for machine in system.getMachines():
        machine.phase_2()

def resetTables(system):
    for buf in system.getBuffers():
        buf.reset()
    for machine in system.getMachines():
        machine.reset()
    system.resetHistoric()