from MachineLine import Machine, Buffer, System, INPUT_CNT_BUF, OUTPUT_CNT_BUF

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

def generation(system):
    possibleNextStates = []
    for i in range(len(system.getMachines())-1):
        copySystem = system
        if (i == 0):
            copySystem.getMachines()[i].switchIs_Up()
            possibleNextStates.append(copySystem.getCurrentState())
        else: 
            if (copySystem.getBuffers()[i].is_empty()):
                copySystem.getMachines()[i+1].setIs_Up(True)
            else:
                copySystem.getMachines()[i+1].switchIs_Up()
            possibleNextStates.append(copySystem.getCurrentState())
    return possibleNextStates
    

def generatePossibleStatesFromCurrent(system):
    print(generateStringState(system))
    print("Possible states :")
    # Complete : facon de visualiser la liste des events franchissables : toutes combinaisons des events courants
    possibleStates = generation(system)
    print(possibleStates)
    # possibleNextStates.append(): 
def printSummarizedState(summarizedState):
    for element in summarizedState:
        print(element)

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

def main():
    print("------Simulation------")
    print("---Creating the System")
    numberMachine = int(input("Enter the number of machines: "))
    machine = []
    bufferTable = []
    for i in range(numberMachine-1) :
        sizei = bufferInput(i)
        bufferTable.append(Buffer(Buffer.Type.MIDDLE,sizei,'Buffer'+str(i+1)))
    machineTable = []
    for j in range(numberMachine):
        breakdown_prob = probabilityBreakdownInput(j)
        repair_prob = probabilityRepairInput(j)
        if (j == 0):
            machineTable.append(Machine(breakdown_prob,repair_prob,INPUT_CNT_BUF,bufferTable[j],"Machine1"))
        elif (j == numberMachine-1):
            machineTable.append(Machine(breakdown_prob,repair_prob,bufferTable[j-1],OUTPUT_CNT_BUF,"Machine"+str(j+1)))
        else:  
            machineTable.append(Machine(breakdown_prob,repair_prob,bufferTable[j-1],bufferTable[j],"Machine"+str(j+1)))
    system = System(numberMachine, machineTable, bufferTable)
    while(1):
        for buf in system.getBuffers():
            buf.reset()
        for machine in system.getMachines():
            machine.reset()
        system.resetHistoric()
        print("************************************")
        print("------Choosing simulation type------")
        print("--Click A: Automatic simulation")
        print("--Click B: 1-step simulation")
        print("--Click Q: Exit")
        choice = input("Pick your choice : ").upper()
        if (choice == "Q"):
            break
        else:
            timeUnit = int(input("Enter the time slot : "))
            instantT = 0
            print("T = 0")
            print(generateStringState(system))
            if (choice == "A"):
                while(instantT < timeUnit):
                    copyOutputValue = OUTPUT_CNT_BUF.getCurrent()
                    copyInputValue = abs(INPUT_CNT_BUF.getCurrent())
                    print("T = " + str(instantT+1))
                    for machine in system.getMachines():
                        machine.phase_1_rand()
                    for machine in system.getMachines():
                        machine.phase_2()
                    print(generateStringState(system))
                    differenceOutput = OUTPUT_CNT_BUF.getCurrent() - copyOutputValue
                    differenceInput = abs(INPUT_CNT_BUF.getCurrent()) - copyInputValue
                    summarizedState = generateSummarizedState(system,differenceOutput,differenceInput)
                    system.getHistoricState().append(summarizedState)
                    instantT +=1
            elif(choice == 'B'):
                while(instantT <= timeUnit):
                    print("T = " + str(instantT))
                    generatePossibleStatesFromCurrent(system)
                    choosenState = input("Choose possible state: ")
                    instantT +=1

if __name__ == "__main__":
    main()
