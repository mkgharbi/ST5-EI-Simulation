from PerformanceIndicator import *
from SharedFunctions import *
from Buffer import *
from System import System
from Machine import Machine

NUMBERMACHINE = 2 
#EXPERIMENT 1A
PROBABILITYEXPERIMENT1ABREAKDOWN = 0.01
PROBABILITYEXPERIMENT1AREPAIR = 0.1
BUFFERSIZEEXPERIMENT1A = 25
TIMESLOTEXPERIMENT1 = 30
# EXPERIMENT 1B
PROBABILITYEXPERIMENT1AM1BREAKDOWN = 0.02
PROBABILITYEXPERIMENT1AM2BREAKDOWN = 0.01
PROBABILITYEXPERIMENT1AM1REPAIR = 0.05
PROBABILITYEXPERIMENT1AM2REPAIR = 0.1
#EXPERIMENT 2 
MAXBUFFERSIZE = 50
MINBUFFERSIZE = 5
PROBABILITYEXPERIMENT1AM1BREAKDOWN = 0.01
PROBABILITYEXPERIMENT1AM2BREAKDOWN = 0.02
PROBABILITYEXPERIMENT1AM1REPAIR = 0.05
PROBABILITYEXPERIMENT1AM1REPAIR = 0.2
LEADTIMETHRESHOLDN = 40


def generateSystemExperiment1B():
    bufferTable = [Buffer(Buffer.Type.MIDDLE,BUFFERSIZEEXPERIMENT1A,"Buffer1")]
    machineTable = [
        Machine(PROBABILITYEXPERIMENT1AM1BREAKDOWN,PROBABILITYEXPERIMENT1AM1REPAIR,INPUT_CNT_BUF,bufferTable[0],"M1"),
        Machine(PROBABILITYEXPERIMENT1AM2BREAKDOWN,PROBABILITYEXPERIMENT1AM2REPAIR,bufferTable[0],OUTPUT_CNT_BUF,"M2"),
    ]
    return System(2,machineTable,bufferTable)

def generateSystemExperiment1A():
    bufferTable = [Buffer(Buffer.Type.MIDDLE,BUFFERSIZEEXPERIMENT1A,"Buffer1")]
    machineTable = [
        Machine(PROBABILITYEXPERIMENT1ABREAKDOWN,PROBABILITYEXPERIMENT1AREPAIR,INPUT_CNT_BUF,bufferTable[0],"M1"),
        Machine(PROBABILITYEXPERIMENT1ABREAKDOWN,PROBABILITYEXPERIMENT1AREPAIR,OUTPUT_CNT_BUF,OUTPUT_CNT_BUF,"M2"),
    ]
    return System(2,machineTable,bufferTable)

    
def main():
    print("------Experiments------")    
    while(1):
        print("************************************")
        print("------ Choosing Experiement ------")
        while(True):
            print("-- Click A: 1a Experiment")
            print("-- Click B: 1b Experiment")
            print("-- Click C: 2a Experiment")
            print("-- Click D: 2b Experiment")
            print("-- Click E: 3 Experiment")
            print("-- Any other input : Exit")
            choice = input("Pick your choice : ").upper()
            if (choice == "A"): # Experiment 1a
                systemExperiment1A = generateSystemExperiment1A()
            elif (choice == "B"):  # Experiment 1b
                systemExperiment1B = generateSystemExperiment1B()
            elif (choice == "C"):  # Experiment 2a
                break
            elif (choice == "D"):  # Experiment 2b
                break
            elif (choice == "E"):  # Experiment 3
                break
            else:
                break
                        

if __name__ == "__main__":
    main()
