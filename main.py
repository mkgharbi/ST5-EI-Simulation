from MachineLine import Machine, Buffer, System, INPUT_BUF, OUTPUT_BUF

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


def main():
    print("------Simulation------")
    print("---Creating the System")
    numberMachine = int(input("Enter the number of machines: "))
    machine = []
    bufferTable = []
    for i in range(numberMachine-1) :
        sizei = input("Enter the buffer size of buffer" + str(i+1) + " : ")
        bufferTable.append(Buffer(0,sizei,'buffer'+str(i+1)))
    print(bufferTable)
    machineTable = []
    for j in range(numberMachine):
        breakdown_prob = probabilityBreakdownInput(j)
        repair_prob = probabilityRepairInput(j)
        if (j == 0):
            machineTable.append(Machine(breakdown_prob,repair_prob,INPUT_BUF,bufferTable[j],"Machine"+str(j+1)))
        if ( j == numberMachine-1):
            machineTable.append(Machine(breakdown_prob,repair_prob,bufferTable[j-1],OUTPUT_BUF,"Machine"+str(j+1)))
        else:  
            machineTable.append(Machine(breakdown_prob,repair_prob,bufferTable[j-1],bufferTable[j],"Machine"+str(j+1)))
    system = System(numberMachine, machineTable, bufferTable)
    print("------Choosing simulation type------")
    print("--Click A: Automatic simulation")
    print("--Click B: 1-step simulation")
    choice = input("Choose simulation type : ")
    if (choice == "A"):
        timeUnit = input("Enter the time slot : ")
    


if __name__ == "__main__":
    main()
