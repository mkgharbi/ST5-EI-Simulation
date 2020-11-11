from Machine import Machine
from PerformanceIndicator import *
from SharedFunctions import *
from System import System
from Buffer import *
MAXSIMULATIONBUFFERINCREMENTED = 50


def creationSystemCommonBuffer(numberMachine, machineTable, bufferTable):
    for i in range(numberMachine-1) :
        bufferTable.append(Buffer(Buffer.Type.MIDDLE,1,'Buffer'+str(i+1)))
    for j in range(numberMachine):
        breakdown_prob = probabilityBreakdownInput(j)
        repair_prob = probabilityRepairInput(j)
        if (j == 0):
            machineTable.append(Machine(breakdown_prob,repair_prob,INPUT_CNT_BUF,bufferTable[j],"Machine1"))
        elif (j == numberMachine-1):
            machineTable.append(Machine(breakdown_prob,repair_prob,bufferTable[j-1],OUTPUT_CNT_BUF,"Machine"+str(j+1)))
        else:
            machineTable.append(Machine(breakdown_prob,repair_prob,bufferTable[j-1],bufferTable[j],"Machine"+str(j+1)))
    return System(numberMachine, machineTable, bufferTable)
    
def incrementBufferSize(system):
    for bufferElement in system.getBuffers():
        bufferElement.incrementCapacity()

def main():
    print("------Simulation------")
    print("---Creating the System")
    numberMachine = int(input("Enter the number of machines: "))
    machineTable = []
    bufferTable = []
    while(True):
        print("---Choose type of calculation")
        print("--Click A: Increment buffer size by one unit")
        print("--Click B: Choose which probability to variate")
        print("--Click Q: Exit")
        choice = input("Make your choice: ").upper()
        if (choice == "A"):
            historicSimulations = []
            system = creationSystemCommonBuffer(numberMachine, machineTable, bufferTable)
            timeSlot = int(input("Enter time slot of the simulation: "))
            simulationCounter = 1
            while(simulationCounter <= MAXSIMULATIONBUFFERINCREMENTED):
                system.setCommonCapacity(simulationCounter)
                print("Simulation: ")
                print("T = 0")
                print(generateStringState(system))
                for buf in system.getBuffers():
                    buf.reset()
                for machine in system.getMachines():
                    machine.reset()
                system.resetHistoric()
                instantT = 0
                while(instantT < timeSlot):
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
                    summarizedStateCopy = summarizedState[:]
                    system.getHistoricState().append(summarizedStateCopy)
                    instantT +=1
                    historicStateCopy = system.getHistoricState()[:]
                    historicSimulations.append(historicStateCopy)
                simulationCounter +=1
        elif(choice == "B"):
            print("TODO")
            
        elif(choice == "Q"):
            break


if __name__ == "__main__":
    main()
