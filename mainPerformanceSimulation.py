from Machine import Machine
from SharedFunctions import *
from System import System
from Buffer import *
from indicateurs_de_performance import *
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

def incrementMachineProbability(system,indexInMachineTable ,variableChoice, probabilityValue):
    if (variableChoice % 2 == 1):
        system.getMachines()[indexInMachineTable].setBreakdownProbability(probabilityValue)   
    else:
        system.getMachines()[indexInMachineTable].setRepairProbability(probabilityValue)

def generateVariableOptions(machineNumber):
    possibleOptions = machineNumber*2
    machineIndex = 1
    for i in range(1,possibleOptions+1):
        if (i % 2 == 1):
            print("Click " + str(i) + " : Variate only the breakdown probability of the machine " + str(machineIndex))
        else :
            print("Click " + str(i) + " : Variate only the repair probability of the machine " + str(machineIndex))
            machineIndex += 1 

def ChoosingPrabilities(indexInMachineTable, choiceVariable, numberMachine, machineTable, bufferTable):
    for j in range(numberMachine):
        breakdown_prob = 0
        repair_prob = 0
        if (j == indexInMachineTable):
            if (choiceVariable % 2 == 1):
                breakdown_prob = 0.02
                repair_prob = probabilityRepairInput(j)
            else:
                repair_prob = 0.02
                breakdown_prob = probabilityBreakdownInput(j)
        else: 
            breakdown_prob = probabilityBreakdownInput(j)
            repair_prob = probabilityRepairInput(j)
        if (j == 0):
            machineTable.append(Machine(breakdown_prob,repair_prob,INPUT_CNT_BUF,bufferTable[j],"Machine1"))
        elif (j == numberMachine-1):
            machineTable.append(Machine(breakdown_prob,repair_prob,bufferTable[j-1],OUTPUT_CNT_BUF,"Machine"+str(j+1)))
        else:  
            machineTable.append(Machine(breakdown_prob,repair_prob,bufferTable[j-1],bufferTable[j],"Machine"+str(j+1))) 
    return machineTable

def main():
    print("------Simulation------")
    print("---Creating the System")
    numberMachine = int(input("Enter the number of machines: "))
    machineTable = []
    bufferTable = []
    historicSimulations = []
    while(True):
        print("---Choose type of calculation")
        print("--Click A: Increment buffer size by one unit")
        print("--Click B: Choose which probability to variate")
        print("--Click Q: Exit")
        choice = input("Make your choice: ").upper()
        if (choice == "A"):
            bufferTable.clear()
            machineTable.clear()
            historicSimulations.clear()
            system = creationSystemCommonBuffer(numberMachine, machineTable, bufferTable)
            timeSlot = int(input("Enter time slot of the simulation: "))
            simulationCounter = 1
            while(simulationCounter <= MAXSIMULATIONBUFFERINCREMENTED):
                system.setCommonCapacity(simulationCounter)
                simulation = 0
                while(simulation < 1000):
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
                        for machine in system.getMachines():
                            machine.phase_1_rand()
                        for machine in system.getMachines():
                            machine.phase_2()
                        print("T = " + str(instantT+1))
                        print(generateStringState(system))
                        differenceOutput = OUTPUT_CNT_BUF.getCurrent() - copyOutputValue
                        differenceInput = abs(INPUT_CNT_BUF.getCurrent()) - copyInputValue
                        summarizedState = generateSummarizedState(system,differenceOutput,differenceInput)
                        summarizedStateCopy = summarizedState[:]
                        system.getHistoricState().append(summarizedStateCopy)
                        instantT +=1
                    historicStateCopy = system.getHistoricState()[:]
                    historicSimulations.append(historicStateCopy)
                    simulation += 1
                simulationCounter +=1
        elif(choice == "B"):
            bufferTable.clear()
            machineTable.clear()
            historicSimulations = []
            for i in range(numberMachine-1) :
                sizei = bufferInput(i)
                bufferTable.append(Buffer(Buffer.Type.MIDDLE,sizei,'Buffer'+str(i+1)))
            print("Choose which variable to change")
            generateVariableOptions(numberMachine)
            while(True):
                choiceVariable = int(input("Choose which variable: "))
                if choiceVariable in range(1, numberMachine*2 + 1):
                    indexMachine = choiceVariable
                    if (choiceVariable % 2 == 1): # Breakdown proba
                        indexMachine = choiceVariable + 1
                    indexInMachineTable = int(indexMachine / 2) - 1
                    print(indexInMachineTable)
                    machineTable = ChoosingPrabilities(indexInMachineTable,choiceVariable,numberMachine,machineTable,bufferTable)
                    system = System(numberMachine,machineTable,bufferTable)
                    timeSlot = int(input("Enter time slot of the simulation: "))
                    probabilityValue = 0.01
                    while(probabilityValue <= 0.4):
                        print("----------")
                        print("Simulation: " + str(probabilityValue))
                        incrementMachineProbability(system,indexInMachineTable ,choiceVariable, probabilityValue)
                        nbSimulation = 0
                        while(nbSimulation < 1000):
                            for buf in system.getBuffers():
                                buf.reset()
                            for machine in system.getMachines():
                                machine.reset()
                            system.resetHistoric()
                            instantT = 0
                            print("T = 0")
                            print(generateStringState(system))
                            while(instantT < timeSlot):
                                copyOutputValue = OUTPUT_CNT_BUF.getCurrent()
                                copyInputValue = abs(INPUT_CNT_BUF.getCurrent())
                                simulatingAStep(system)
                                print("T = " + str(instantT+1))
                                print(generateStringState(system))
                                differenceOutput = OUTPUT_CNT_BUF.getCurrent() - copyOutputValue
                                differenceInput = abs(INPUT_CNT_BUF.getCurrent()) - copyInputValue
                                summarizedState = generateSummarizedState(system,differenceOutput,differenceInput)
                                summarizedStateCopy = summarizedState[:]
                                system.getHistoricState().append(summarizedStateCopy)
                                instantT +=1
                            historicStateCopy = system.getHistoricState()[:]
                            historicSimulations.append(historicStateCopy)
                            nbSimulation += 1
                        probabilityValue += 0.01
                    graph_effective_production_rate_r1(historicSimulations,30, sizei, 1000)
                    break
                else:
                    print("Choose a number from those proposed ")
        elif(choice == "Q"):
            print(len(historicSimulations))
            #print(historicSimulations)
            # Done: graph_work_in_progress_plusieurs_simulations(historicSimulations, 1000)
            # Done: graph_throughput_plusieurs_simulations(historicSimulations,1000)
            # done: graph_WIP_p1_p2_r1_r2(historicSimulations,1000,"r2")
            # 2a : graph_total_production_rate(historicSimulations, 40, 1000)
            plt.show()
            break

if __name__ == "__main__":
    main()
