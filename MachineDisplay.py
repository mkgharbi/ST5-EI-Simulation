from tkinter import *
from functools import partial
from Machine import *
from PerformanceIndicator import *
from Buffer import *
from System import *
def main_window():

    machines=[]
    buffers=[]
    def add_buffer():
        popup = Tk()
        
        
        name=StringVar(popup)
        capacity=StringVar(popup)

        Label(popup,text="Nom du buffer").grid(row=0)
        Label(popup,text="Capacité du buffer").grid(row=1)
        Entry(popup,textvariable=name).grid(row=0,column=1)
        Entry(popup,textvariable=capacity).grid(row=1,column=1)
        

        def destroy():
            """Validation des entrées"""
            if(len(machines)==0):
                popup.destroy()
                add_machine()
            else: 
                if((len(capacity.get())>0 and  len(name.get())>0)and (float(capacity.get()).is_integer())):
                    
                    buffers.append((name.get(),int(capacity.get())))
                    popup.destroy()
                    add_machine()
                else:
                    invalid_entry_warning()
            

        Grid.rowconfigure(popup,2,weight=1)
        Button(popup,text="Ajouter le buffer",command=destroy).grid(row=2)   
            
            
        popup.wm_title("Ajout d'un buffer")
        if(len(machines)==0):
            destroy()
        else : 
            popup.mainloop()
        
        
    def add_machine():
        popup = Tk()

        name = StringVar(popup)
        breakdown_prob = StringVar(popup)
        repair_prob = StringVar(popup)
        
        Label(popup,text="Nom de la machine").grid(row=0)
        Label(popup,text="Probabilité de se casser").grid(row=1)
        Label(popup,text="Probabilité de se réparer").grid(row=2)

        Entry(popup,textvariable=name).grid(row=0,column=1)
        Entry(popup,textvariable=breakdown_prob).grid(row=1,column=1)
        Entry(popup,textvariable=repair_prob).grid(row=2,column=1)

        def destroy():
            """Validation des entrées"""
            if((len(breakdown_prob.get())>0 and len(repair_prob.get())>0 and len(name.get())>0)and (float(breakdown_prob.get())<=1 and float(breakdown_prob.get())>=0) and (float(repair_prob.get())<=1 and float(repair_prob.get())>=0)):
                machines.append((name.get(),float(breakdown_prob.get()),float(repair_prob.get())))
                popup.destroy()
                display_machine()
                    
            else:
                invalid_entry_warning()
            

        Grid.rowconfigure(popup,3,weight=1)
        Button(popup,text="Ajouter la machine",command=destroy).grid(row=3)   
            
            
        popup.wm_title("Ajout d'une machinne")
        popup.mainloop()

    def invalid_entry_warning():
        def destroy():
            popup.destroy()
        popup=Tk()
        Label(popup,text="Veuillez rentrer des valeurs valides").grid(row=0)
        Button(popup,text="Confirmer",command=destroy).grid(row=1)
    def select_time_unit():
        popup = Tk()
        time_unit=StringVar(popup)

        Label(popup,text="Nombre d'unités de temps pour la simulation").grid(row=0)
        Entry(popup,textvariable=time_unit).grid(row=0,column=1)
        

        def destroy():
            """Validation des entrées"""
            if((len(time_unit.get())>0 and (float(time_unit.get()).is_integer()))):
                popup.destroy()
                launch_simulation(root_window,machines,buffers,time_unit.get())
            else:
                invalid_entry_warning()
            

        Grid.rowconfigure(popup,2,weight=1)
        Button(popup,text="Lancer la simulation",command=destroy).grid(row=2)   
            
            
        popup.wm_title("Lancer la simulation")
        popup.mainloop()
        

    """Définie la fenêtre de saisie des données utilisateurs"""
    root_window = Tk()
    root_window.configure(background = "white")
    root_window.title("Système de production")    
    root_window.resizable(0,0)
    root_window.geometry('400x400')

    def format_machine_display(machine):
        return machine[0]+" : p="+str(machine[1])+", r="+str(machine[2])

    def format_buffer_display(buffer):
        return buffer[0]+" : capacité="+str(buffer[1])
    machine_frame=Frame(root_window)
    machine_frame.configure(background="white")
    machine_frame.grid(row=0,column=0)
    button_frame=Frame(root_window)
    button_frame.configure(background = "white")
    Grid.columnconfigure(root_window,0,weight=1)
    button_frame.grid(row=1,column=0)
    Grid.rowconfigure(button_frame,0,weight=1)
    Grid.columnconfigure(button_frame,0,weight=1)

    def display_machine():
        if(len(machines)>0):
            Label(machine_frame,bg="white",fg="red",text=format_machine_display(machines[0])).grid(row=0)
        if(len(machines)>1):
            create_system_button = Button(button_frame,text="Lancer la simulation",bg="black",fg="snow",command=select_time_unit)
            create_system_button.textcolor="snow"
            create_system_button.grid(row=0,column=1)
            
            for i in range(len(buffers)):
                Label(machine_frame,bg="white",fg="green",text=format_buffer_display(buffers[i])).grid(row=2*i+1)
                Label(machine_frame,bg="white",fg="red",text=format_machine_display(machines[i+1])).grid(row=2*(i+1))

    
    add_machine_button = Button(button_frame,text="Ajouter une machine", bg = "black", fg = "snow",command=add_buffer)
    add_machine_button.textcolor = "snow"
    add_machine_button.grid(row=0,column=0)


    root_window.mainloop()

def launch_simulation(root_window,machines,buffers,time_unit):
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
    bufferTable,machineTable = [],[]
    for buffer in buffers:
        bufferTable.append(Buffer(Buffer.Type.MIDDLE,buffer[1],buffer[0]))
    machineTable.append(Machine(machines[0][1],machines[0][2],INPUT_CNT_BUF,bufferTable[0],machines[0][0]))
    for i in range(1,len(machines)-1):
        machine = machines[i]
        
        machineTable.append(Machine(machine[1],machine[2],bufferTable[i-1],bufferTable[i],machine[0]))
        
    machineTable.append(Machine(machines[-1][1],machines[-1][2],bufferTable[-1],OUTPUT_CNT_BUF,machines[-1][0]))
    
    system = System(len(machineTable), machineTable, bufferTable)
    instantT = 0
    stateStrings=[]
    
    while(instantT <= int(time_unit)):
        copyOutputValue = OUTPUT_CNT_BUF.getCurrent()
        copyInputValue = abs(INPUT_CNT_BUF.getCurrent())
        for machine in system.getMachines():
            machine.phase_1_rand()
        for machine in system.getMachines():
            machine.phase_2()
        
        differenceOutput = OUTPUT_CNT_BUF.getCurrent() - copyOutputValue
        differenceInput = abs(INPUT_CNT_BUF.getCurrent()) - copyInputValue
        summarizedState = generateSummarizedState(system,differenceOutput,differenceInput)
        summarizedStateCopy = summarizedState[:] 
        system.getHistoricState().append(summarizedStateCopy)
        stateStrings.append(generateStringState(system))
        instantT +=1
    
    def get_historic_states(number_of_simulations):
        historicSimulations = []
        occurence = 0
        while (occurence < int(number_of_simulations)):
            for buf in system.getBuffers():
                buf.reset()
            for machine in system.getMachines():
                machine.reset()
            OUTPUT_CNT_BUF.reset()
            INPUT_CNT_BUF.reset()
            system.resetHistoric()
            instantT = 0
            while(instantT < int(time_unit)):
                copyOutputValue = OUTPUT_CNT_BUF.getCurrent()
                copyInputValue = abs(INPUT_CNT_BUF.getCurrent())
                for machine in system.getMachines():
                    machine.phase_1_rand()
                for machine in system.getMachines():
                    machine.phase_2()  
                differenceOutput = OUTPUT_CNT_BUF.getCurrent() - copyOutputValue
                differenceInput = abs(INPUT_CNT_BUF.getCurrent()) - copyInputValue
                
                summarizedState = generateSummarizedState(system,differenceOutput,differenceInput)
                summarizedStateCopy = summarizedState[:]
                system.getHistoricState().append(summarizedStateCopy)
                instantT +=1
            occurence += 1
            historicStateCopy = system.getHistoricState()[:]
            historicSimulations.append(historicStateCopy)
            
        return historicSimulations
    
    def display_lead_time_distribution():
        popup = Tk()
        number_of_simulations=StringVar(popup)

        Label(popup,text="Nombre de simulations à effectuer : ").grid(row=0)
        Entry(popup,textvariable=number_of_simulations).grid(row=0,column=1)
        

        def destroy():
            graph_proba_distrib_LT_plusieurs_simulations(get_historic_states(number_of_simulations.get()))
            popup.destroy()

        Grid.rowconfigure(popup,2,weight=1)
        Button(popup,text="Lancer les simulations",command=destroy).grid(row=2)   
        popup.wm_title("Calculer le lead time distribution")
        popup.mainloop()
    def display_total_production_rate():
        pass
    def display_effective_production_rate():
        popup = Tk()
        number_of_simulations=StringVar(popup)
        window_lenght=StringVar(popup)

        Label(popup,text="Nombre de simulations à effectuer : ").grid(row=0)
        Entry(popup,textvariable=number_of_simulations).grid(row=0,column=1)
        Label(popup,text="Taille de la fenêtre : ").grid(row=1)
        Entry(popup,textvariable=window_lenght).grid(row=1,column=1)
        

        def destroy():
            Prod_rate = effective_production_rate_plusieurs_simulations(get_historic_states(number_of_simulations.get()),int(window_lenght.get()))
            Tailles_buffer = [i+1 for i in range(time_unit)]
            plt.plot(Tailles_buffer, Prod_rate, label = "Taux effectif de production pour une fenêtre de taille"+ str(window_lenght.get()))
            plt.xlabel("Taille du buffer")
            plt.legend()
            popup.destroy()

        Grid.rowconfigure(popup,2,weight=1)
        Button(popup,text="Lancer les simulations",command=destroy).grid(row=2)   
        popup.wm_title("Calculer l'effective production rate")
        popup.mainloop()
        
    def display_blocking_probability():
        popup = Tk()
        number_of_simulations=StringVar(popup)

        Label(popup,text="Nombre de simulations à effectuer : ").grid(row=0)
        Entry(popup,textvariable=number_of_simulations).grid(row=0,column=1)
        

        def destroy():
            graph_blocking_probability_plusieurs_simulations(get_historic_states(number_of_simulations.get()))
            plt.show()
            popup.destroy()

        Grid.rowconfigure(popup,2,weight=1)
        Button(popup,text="Lancer les simulations",command=destroy).grid(row=2)   
        popup.wm_title("Calculer la blocking probability")
        popup.mainloop()
    def get_historic_states_buffer(number_of_simulations):
        WIP = []
        
        for buffer_size in range(1,51):
            localBufferTable=[Buffer(Buffer.Type.MIDDLE,buffer_size,"Test Buffer")]
            machines = system.getMachines()
            localMachineTable =[]
            localMachineTable.append(Machine(machines[0].up_to_down,machines[0].down_to_up,INPUT_CNT_BUF,localBufferTable[0],"Machine 1"))
        
            localMachineTable.append(Machine(machines[0].up_to_down,machines[0].down_to_up,localBufferTable[0],OUTPUT_CNT_BUF,"Machine 2"))
        
    
            localSystem = System(2, localMachineTable, localBufferTable)
            occurence = 0
            fixed_buffer_size_wip=[]    
            while (occurence < int(number_of_simulations)):
                for buf in localSystem.getBuffers():
                    buf.reset()
                for machine in localSystem.getMachines():
                    machine.reset()
                OUTPUT_CNT_BUF.reset()
                INPUT_CNT_BUF.reset()
                localSystem.resetHistoric()
                instantT = 0
                fixed_buffer_size_state=[]
                while(instantT < int(time_unit)):
                    copyOutputValue = OUTPUT_CNT_BUF.getCurrent()
                    copyInputValue = abs(INPUT_CNT_BUF.getCurrent())
                    for machine in localSystem.getMachines():
                        machine.phase_1_rand()
                    for machine in localSystem.getMachines():
                        machine.phase_2()  
                    differenceOutput = OUTPUT_CNT_BUF.getCurrent() - copyOutputValue
                    differenceInput = abs(INPUT_CNT_BUF.getCurrent()) - copyInputValue
                    
                    summarizedState = generateSummarizedState(localSystem,differenceOutput,differenceInput)
                    summarizedStateCopy = summarizedState[:]
                    fixed_buffer_size_state.append(summarizedStateCopy)
                    localSystem.getHistoricState().append(summarizedStateCopy)
                    instantT +=1
                fixed_buffer_size_wip.append(work_in_progress(fixed_buffer_size_state,int(time_unit)-1))
                occurence += 1
                historicStateCopy = localSystem.getHistoricState()[:]
                
            WIP.append(np.mean(fixed_buffer_size_wip))
        return WIP
    def display_work_in_progress():
        popup = Tk()
        number_of_simulations=StringVar(popup)

        Label(popup,text="Nombre de simulations à effectuer : ").grid(row=0)
        Entry(popup,textvariable=number_of_simulations).grid(row=0,column=1)
        

        def destroy():
            Tailles_buffer = [i+1 for i in range(1,51)]
            WIP = (get_historic_states_buffer(number_of_simulations.get()))
            plt.plot(Tailles_buffer, WIP, label = "Nombre de pièces en cours de traitement")
            plt.xlabel("Taille du buffer")
            plt.legend()
            plt.show()
            popup.destroy()

        Grid.rowconfigure(popup,2,weight=1)
        Button(popup,text="Lancer les simulations",command=destroy).grid(row=2)   
        popup.wm_title("Calculer le work in progress pour des capacités de buffer de 1 à 50")
        popup.mainloop()

    simulation_window = Toplevel(root_window)
    simulation_window.configure(background = "white")
    simulation_window.resizable(0,0)
    simulation_window.title("Simulation")
    

    indicators_frame = Frame(simulation_window,bg="snow") 
    indicators_frame.grid(row=0,column=0)

    Button(indicators_frame,text="Lead time distribution",bg="black",fg="snow",command=display_lead_time_distribution).grid(row=0,column=0)
    #Button(indicators_frame,bg="black",fg="snow",text="Total production rate",command=display_total_production_rate).grid(row=0,column=1)
    #Button(indicators_frame,bg="black",fg="snow",text="Effective production rate",command=display_effective_production_rate).grid(row=0,column=2)
    #Button(indicators_frame,bg="black",fg="snow",text="Blocking probability",command=display_blocking_probability).grid(row=0,column=3)
    Button(indicators_frame,bg="black",fg="snow",text="Work in progress",command=display_work_in_progress).grid(row=0,column=1)

    simulation_frame = Frame(simulation_window,bg="white")
    simulation_frame.grid(row=1,column=0)
    Grid.columnconfigure(simulation_frame,0,weight=1)
    Grid.rowconfigure(simulation_frame,0,weight=1)
    simulation_steps_frame = Frame(simulation_frame,bg="black",width="300")
    
    for i in range(len(stateStrings)):
        step_label = Label(simulation_steps_frame,text="Etape "+str(i),fg="white",bg="black")
        step_label.bind("<Button-1>",lambda e,index=i:display_details(index))
        step_label.grid(row=i)
    simulation_steps_frame.grid(row=0,column=0,sticky="w")
    simulation_details_frame = Frame(simulation_frame,width="600",bg="white")
    simulation_details_frame.grid(row=0,column=1)
    for i in range(len(stateStrings)):
        Label(simulation_details_frame,text=stateStrings[i],bg="white").grid(row=i)
    def display_details(index):
        for child in simulation_details_frame.winfo_children():
            child.destroy()
        Label(simulation_details_frame,text="Etape " + str(index),bg="white").grid(row=0)
        Label(simulation_details_frame,text=stateStrings[index],bg="white").grid(row=1)
        Label(simulation_details_frame,bg="white",text="Work in progress : "+str(work_in_progress(system.getHistoricState(),index))).grid(row=2)
        Label(simulation_details_frame,bg="white",text="Througput : "+str(throughput(system.getHistoricState()[:index]))).grid(row=3)
        
    
     
    
if __name__ == '__main__':
    main_window()