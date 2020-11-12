from indicateurs_de_performance import *
from SharedFunctions import *
from Buffer import *
from System import System
from Machine import Machine

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
    historicSimulations = []
    while(1):
        
        print("************************************")
        print("------Choosing simulation type------")
        print("--Click A: Automatic simulation")
        print("--Click B: 1-step simulation")
        print("--Click Q: Exit")
        choice = input("Pick your choice : ").upper()
        if (choice == "Q"):
            graph_proba_distrib_LT_plusieurs_simulations(historicSimulations)
            #graph_work_in_progress_plusieurs_simulations(historicSimulations)
            #graph_blocking_probability_plusieurs_simulations(historicSimulations)
            break
        else:
            if (choice == "A"):
                timeUnit = int(input("Enter the time slot : "))
                occurenceSimulation = int(input("Automation occurences : "))
                occurence = 0
                while (occurence < occurenceSimulation):
                    print("Simulation: ")
                    print("T = 0")
                    print(generateStringState(system))
                    resetTables(system)
                    instantT = 0
                    while(instantT < timeUnit):
                        copyOutputValue = OUTPUT_CNT_BUF.getCurrent()
                        copyInputValue = abs(INPUT_CNT_BUF.getCurrent())
                        print("T = " + str(instantT+1))
                        simulatingAStep(system)
                        print(generateStringState(system)) 
                        differenceOutput = OUTPUT_CNT_BUF.getCurrent() - copyOutputValue
                        differenceInput = abs(INPUT_CNT_BUF.getCurrent()) - copyInputValue
                        summarizedState = generateSummarizedState(system,differenceOutput,differenceInput)
                        summarizedStateCopy = summarizedState[:]
                        system.getHistoricState().append(summarizedStateCopy)
                        instantT +=1
                    occurence += 1
                    historicStateCopy = system.getHistoricState()[:]
                    historicSimulations.append(historicStateCopy)
            elif(choice == 'B'):
                instantT = 0
                while(True):
                    print("T = " + str(instantT))
                    print(generateStringState(system))
                    print("Click S : Skip the one-step Simulation: ")
                    print("Click C : Go to" + str(instantT+1) + " time in the one-step Simulation: ")
                    print("Click any other input : Stop the simulation")
                    choiceManual = input("Make your choice: ").upper()
                    if (choiceManual == "C"):
                        simulatingAStep(system)
                        instantT +=1
                    elif(choiceManual == "S"):
                        print("Choose the final time to stop the simulation ")
                        finalTime = int(input("Enter the final time"))
                        while(instantT < finalTime):
                            instantT += 1
                            print("T = " + str(instantT))
                            print(generateStringState(system))
                            simulatingAStep(system)
                        break
                    else:
                        break

                        

if __name__ == "__main__":
    main()
