import matplotlib.pyplot as plt
import numpy as np


# Tableaux test

T1 = [[True,1,3,False,0,4,True,4,4,False,0,1],
        [False,1,3,True,1,4,True,4,4,True,0,1],
        [False,0,3,True,1,4,True,3,4,False,1,0]]

T2 = [[True,1,3,False,0,4,True,4,4,False,4,5,True,4,5,False,2,6,False,0,1],
      [True,2,3,True,1,4,True,4,4,False,3,5,True,4,5,False,2,6,False,0,1],    
      [True,1,3,False,0,4,True,4,4,False,2,5,True,4,5,False,2,6,False,0,1],    
      [True,1,3,False,0,4,True,3,4,False,1,5,True,4,5,False,2,6,False,1,1],    
      [True,1,3,False,0,4,True,4,4,False,0,5,True,4,5,False,2,6,False,0,0],    
      [True,1,3,False,0,4,True,4,4,True,1,5,True,4,5,False,2,6,False,1,0]]

T3 = [[True,1,3,False,0,4,True,4,4,False,4,5,True,4,5,False,2,6,False,0,1],
      [True,2,3,True,1,4,True,4,4,False,3,5,True,4,5,False,2,6,False,0,1],    
      [True,1,3,False,0,4,True,4,4,False,2,5,True,4,5,False,2,6,False,0,1],    
      [True,1,3,False,0,4,True,3,4,False,1,5,True,4,5,False,2,6,False,1,1],    
      [True,1,3,False,0,4,True,4,4,False,0,5,True,4,5,False,2,6,False,0,0],    
      [True,1,3,False,0,4,True,4,4,True,3,5,True,4,5,False,6,6,False,1,0]]


# PROBA DISTRIB


def proba_distrib_LT(TableauSimulation, temps_attendu):
    T_entree = []
    T_sortie = []
    T = len(TableauSimulation)
    
    for t in range(T):
        if TableauSimulation[t][-1] == 1:      # Si une piece rentre
            T_entree.append(t)
        if TableauSimulation[t][-2] == 1:      # Si une piece sort
            T_sortie.append(t)
            
    LT = []
    for k in range(len(T_sortie)):
        LT.append(T_sortie[k]-T_entree[k]+1)
    
    if LT ==[]:
        return "pas de pieces qui sortent, on ne peut pas définir une moyenne"
    S = 0
    for t in LT:
        if t == temps_attendu:
            S+=1
            
    Proba_temps_attendu = S/len(LT)  
    return Proba_temps_attendu
    
def graph_proba_distrib_LT(TableauSimulation):
    Delais = []
    Probas = []
    Tmax = len(TableauSimulation)
    
    for t in range(Tmax):
        Delais.append(t+1)
        Probas.append(proba_distrib_LT(TableauSimulation,t+1))
    plt.plot(Delais,Probas)
    plt.xlabel("Temps nécéssaire à la fabrication d'une pièce")
    plt.ylabel("Probabilité")
    plt.show()
    
def graph_proba_distrib_LT_plusieurs_simulations(ListeTableauSimulation):
    Delais = []
    Probas = []
    N = len(ListeTableauSimulation)
    Tmax = len(ListeTableauSimulation[0])
    
    for t in range(Tmax):
        Delais.append(t+1)
        
        Liste_Probas_a_t = []
        for k in range(N):
            Liste_Probas_a_t.append(proba_distrib_LT(ListeTableauSimulation[k],t+1))
        Probas.append(np.mean(Liste_Probas_a_t))
    plt.plot(Delais,Probas)
    plt.xlabel("Temps nécéssaire à la fabrication d'une pièce")
    plt.ylabel("Probabilité")
    plt.show()

def graph_LT_p1_p2_r1_r2(ListeTableauSimulation, proba_controlee):
    N = len(ListeTableauSimulation)
    T = len(ListeTableauSimulation[0])
    LT = []
    Probas = [k/100 for k in range(1,101)]
    
    for k in range(N):
        Delais_ponderes = []
        for t in range(T):
            Delais_ponderes.append(t*proba_distrib_LT(ListeTableauSimulation[k],t))
        LT.append(sum(Delais_ponderes))
    plt.plot(Probas, LT, label = "Temps moyen en fonction de" + proba_controlee )
    plt.xlabel("Temps nécéssaire à la fabrication d'une pièce")
    plt.legend()
    
    
# WORK IN PROGRESS
    
    
def work_in_progress(TableauSimulation,t):
    S = 0
    nb_bi = int(len(TableauSimulation[0])/3 - 1)
    for k in range(nb_bi):  
        S += TableauSimulation[t][3*k+1]  
    return S
    
def graph_work_in_progress(TableauSimulation): 
    Temps = []
    Nb_piece_in_process = []
    Tmax = len(TableauSimulation)
    
    for t in range(Tmax):
        Temps.append(t)
        Nb_piece_in_process.append(work_in_progress(TableauSimulation,t))
    plt.plot(Temps,Nb_piece_in_process)
    plt.xlabel("unité de temps")
    plt.ylabel("nombre de pièces en cours de traitement")
    
def graph_work_in_progress_plusieurs_simulations(ListeTableauSimulation, nb_simulation):
    N = len(ListeTableauSimulation)
    Tmax = len(ListeTableauSimulation[0])
    WIP = []
    wip = []
    Tailles_buffer = []
    
    for k in range(N):
        wip.append(work_in_progress(ListeTableauSimulation[k],Tmax-1))
        if k % nb_simulation == nb_simulation-1:
            Tailles_buffer.append((k+1)/nb_simulation)
            WIP.append(np.mean(wip))
            wip = []
    
    plt.plot(Tailles_buffer, WIP, label = "Nombre de pièces en cours de traitement")
    plt.xlabel("Taille du buffer")
    plt.legend()
    
def graph_WIP_p1_p2_r1_r2(ListeTableauSimulation, nb_simulation, parametre_controle ):
    N = len(ListeTableauSimulation)
    Tmax = len(ListeTableauSimulation[0])
    WIP = []
    wip = []
    Proba = []
    
    for k in range(N):
        wip.append(work_in_progress(ListeTableauSimulation[k],Tmax-1))
        if k % nb_simulation == nb_simulation-1:
            Proba.append(0.01*(k+1)/nb_simulation)
            WIP.append(np.mean(wip))
            wip = []
    
    plt.plot(Proba, WIP, label="WIP en fonction de " + parametre_controle)
    plt.ylabel("WIP")
    plt.legend()
    
    
#  THROUGHPUT


def throughput(TableauSimulation):
    S = 0
    Tmax = len(TableauSimulation)
    
    for t in range(Tmax):
        S += TableauSimulation[t][-2]
    return S

def graph_throughput_plusieurs_simulations(ListeTableauSimulation, nb_simulation):
    Tailles_buffer = []
    N = len(ListeTableauSimulation)
    Tmax = len(ListeTableauSimulation[0])
    Thoughputs = []
    thoughputs = []

    for k in range(N):
        thoughputs.append(throughput(ListeTableauSimulation[k]))
        if k % nb_simulation == nb_simulation-1:
            Tailles_buffer.append((k+1)/nb_simulation)
            Thoughputs.append(np.mean(thoughputs))
            thoughputs = []
    
    plt.plot(Tailles_buffer, Thoughputs, label = "nombre de pièces terminées")
    plt.xlabel("Taille du buffer")
    plt.legend()
    

# BLOCKING PROBABILITY


def blocking_probability(TableauSimulation,i):
    S_full = 0
    S = 0
    Tmax = len(TableauSimulation)
    for t in range(Tmax):
        if TableauSimulation[t][3*i+1] == TableauSimulation[t][3*i+2]:
            S_full += 1
        S += 1
    return S_full/S
    
def graph_blocking_probability(TableauSimulation): 
    Buffer = []
    nb_buffer = int(len(TableauSimulation[0])/3 - 1)
    Proba_full = []    
    
    for i in range(nb_buffer):
        Buffer.append(i)
        Proba_full.append(blocking_probability(TableauSimulation,i))
    plt.plot(Buffer, Proba_full, label = "proba d'être bloqué")
    plt.xlabel("numero du buffer")
    plt.legend()
    
def graph_blocking_probability_plusieurs_simulations(ListeTableauSimulation):
    Buffer = []
    nb_buffer = int(len(ListeTableauSimulation[0][0])/3 - 1)
    Proba_full = []  
    N = len(ListeTableauSimulation)
    
    for i in range(nb_buffer):
        Buffer.append(i)
        
        Liste_Probas_buffer_i = []
        for k in range(N):
            Liste_Probas_buffer_i.append(blocking_probability(ListeTableauSimulation[k],i))
        Proba_full.append(np.mean(Liste_Probas_buffer_i))
    plt.plot(Buffer, Proba_full, label = "Probabilité d'avoir un buffer bloqué")
    plt.xlabel("numéro du buffer")
    plt.legend()
 
     
# STRAVATION PROBABILITY


def stravation_probability(TableauSimulation,i):
    S = 0
    S_empty = 0
    T = len(TableauSimulation)
    
    for t in range(T):
        if TableauSimulation[t][3*i+1] == 0:
            S_empty += 1
        S += 1
    return S_empty/S
    
def graph_stravation_probability(TableauSimulation): 
    Buffer = []
    nb_buffer = int(len(TableauSimulation[0])/3 - 1)
    Proba_empty = []    
    
    for i in range(nb_buffer):
        Buffer.append(i)
        Proba_empty.append(stravation_probability(TableauSimulation,i))
    plt.plot(Buffer,Proba_empty)
    plt.show()
    
def graph_stravation_probability_plusieurs_simulations(ListeTableauSimulation):
    Buffer = []
    nb_buffer = int(len(ListeTableauSimulation[0][0])/3 - 1)
    Proba_empty = []  
    N = len(ListeTableauSimulation)
    
    for i in range(nb_buffer):
        Buffer.append(i)
        
        Liste_Probas_buffer_i = []
        for k in range(N):
            Liste_Probas_buffer_i.append(stravation_probability(ListeTableauSimulation[k],i))
        Proba_empty.append(np.mean(Liste_Probas_buffer_i))
    plt.plot(Buffer,Proba_empty)
    plt.show()
    

# TOTAL PRODUCTION RATE
    
    
def total_production_rate(TableauSimulation, window_lenght):
    T = len(TableauSimulation)
    wl = window_lenght
    nb_exit = 0

    t = 0
    while t <= T - wl:
        for tau in range(t,t+wl):
            nb_exit +=  TableauSimulation[tau][-2]                # nb de pièces sorties
        t+=1
    return nb_exit / t             # Car t est aussi le nombre de fenetre qu'on a considéré
    
def total_production_rate_plusieurs_simulations(ListeTableauSimulation, window_lenght):
    Moyennes = []
    N = len(ListeTableauSimulation)
    
    for k in range(N):
        Moyennes.append(total_production_rate(ListeTableauSimulation[k], window_lenght))
    return np.mean(Moyennes)
    
def graph_total_production_rate(ListeTableauSimulation, wl):
    N = len(ListeTableauSimulation)
    Tailles_buffer = []
    Prod_rate =[]
    prod_rate = []

    for k in range(N):
        prod_rate.append(effective_production_rate(ListeTableauSimulation[k],wl))
        if k % nb_simul == nb_simul-1:
            Tailles_buffer.append((k+1)/nb_simul)
            Prod_rate.append(np.mean(prod_rate))
            prod_rate = []
        
    plt.plot(Tailles_buffer, Prod_rate, label = "Taux de production total pour une fenêtre de taille"+ str(wl))
    plt.xlabel("Taille du buffer")
    plt.legend()


# EFFECTIVE PRODUCTION RATE



def effective_production_rate(TableauSimulation, window_lenght):
    T_entree = []
    T_sortie = []
    T = len(TableauSimulation)
    
    for t in range(T):
        if TableauSimulation[t][-1] == 1:    # Si une piece rentre
            T_entree.append(t)
        if TableauSimulation[t][-2] == 1:    # Si une piece sort
            T_sortie.append(t)

    wl = window_lenght
    nb_exit = 0
    
    t = 0
    while t <= T - wl :
        for tau in range(t,t+wl):
            if tau in T_sortie :
                k = T_sortie.index(tau) 
                lt = T_sortie[k] - T_entree[k] + 1
                if lt <= wl:
                    nb_exit +=1
        t+=1
        
    return nb_exit / t
    
def effective_production_rate_plusieurs_simulations(ListeTableauSimulation, window_lenght):
    Moyennes = []
    N = len(ListeTableauSimulation)
    
    for k in range(N):
        Moyennes.append(effective_production_rate(ListeTableauSimulation[k], window_lenght))
    return np.means(Moyennes)
    
def graph_effective_production_rate(ListeTableauSimulation, wl, nb_simul):
    N = len(ListeTableauSimulation)
    Tailles_buffer = []
    eeff = []
    EEFF =[]

    for k in range(N):
        eeff.append(effective_production_rate(ListeTableauSimulation[k],wl))
        if k % nb_simul == nb_simul-1:
            Tailles_buffer.append((k+1)/nb_simul)
            EEFF.append(np.mean(eeff))
            eeff = []
        
    plt.plot(Tailles_buffer, EEFF, label = "Taux effectif de production pour une fenêtre de taille"+ str(wl))
    plt.xlabel("Taille du buffer")
    plt.legend()

def graph_effective_production_rate_r1(ListeTableauSimulation, wl, buf_size, nb_simul):
    N = len(ListeTableauSimulation)
    eeff = []
    Eeff = []
    Probas = []
    
    for k in range(N):
        eeff.append(effective_production_rate(ListeTableauSimulation[k], wl))
        if k % nb_simul == nb_simul-1:
            Probas.append(0.01*(k+1)/nb_simul)
            Eeff.append(np.mean(eeff))
            eeff = []
    
    plt.plot(Probas, Eeff, label = "B = " + str(buf_size))
    plt.xlabel("r1")
    plt.ylabel("Effective production rate")
    plt.legend()

    
    
    
    
