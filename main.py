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

def generateStringState(system):
    result = 'State = ( '
    for i in range(len(system.getCurrentState())):
        result += str(system.getCurrentState()[i])
    result += ' )'
    return result

def generatePossibleStatesFromCurrent(system):
    possibleNextStates = []
    print(generateStringState(system, possibleNextStates))
    print("Possible states :")
    
    #possibleNextStates.append()

def main():
    print("------Simulation------")
    print("---Creating the System")
    numberMachine = int(input("Enter the number of machines: "))
    machine = []
    bufferTable = []
    for i in range(numberMachine-1) :
        sizei = input("Enter the buffer size of Buffer" + str(i+1) + " : ")
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
            if (choice == "A"):
                while(instantT <= timeUnit):
                    print("T = " + str(instantT))
                    for machine in system.getMachines():
                        machine.phase_1_rand()
                    for machine in system.getMachines():
                        machine.phase_2()
                    print(generateStringState(system))
                    instantT +=1
            elif(choice == 'B'):
                while(instantT <= timeUnit):
                    print("T = " + str(instantT))
                    generatePossibleStatesFromCurrent(system)
                    choosenState = input("Choose possible state: ")
                    instantT +=1


if __name__ == "__main__":
    main()
