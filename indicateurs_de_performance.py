import matplotlib.pyplot as plt
import numpy as np


# Tableaux test

T1 = [[True,1,3,False,0,4,True,4,4,False,0,1],[False,1,3,True,1,4,True,4,4,True,0,1],[False,0,3,True,1,4,True,3,4,False,1,0]]

T2 = [[True,1,3,False,0,4,True,4,4,False,4,5,True,4,5,False,2,6,False,0,1],

    [True,2,3,True,1,4,True,4,4,False,3,5,True,4,5,False,2,6,False,0,1],
    
    [True,1,3,False,0,4,True,4,4,False,2,5,True,4,5,False,2,6,False,0,1],
    
    [True,1,3,False,0,4,True,3,4,False,1,5,True,4,5,False,2,6,False,1,1],
    
    [True,1,3,False,0,4,True,4,4,False,0,5,True,4,5,False,2,6,False,0,0],
    
    [True,1,3,False,0,4,True,4,4,True,1,5,True,4,5,False,2,6,False,1,0]]



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
        LT.append(T_sortie[k]-T_entree[k])
    
    S = 0
    for t in LT:
        if t == temps_attendu:
            S+=1
            
    Proba_temps_attendu = S/len(LT)  #Nombre de pieces fabriquées avec le temps_attendu diviser par nombre total de pieces sorties
    return Proba_temps_attendu
    
def graph_proba_distrib_LT(TableauSimulation):
    Delais = []
    Probas = []
    Tmax = len(TableauSimulation)
    
    for t in range(Tmax):
        Delais.append(t)
        Probas.append(proba_distrib_LT(TableauSimulation,t))
    plt.plot(Delais,Probas)
    plt.show()
    
def graph_proba_distrib_LT_plusieurs_simulations(ListeTableauSimulation):
    Delais = []
    Probas = []
    N = len(ListeTableauSimulation)
    Tmax = len(ListeTableauSimulation[0])
    
    for t in range(Tmax):
        Delais.append(t)
        
        Liste_Probas_a_t = []
        for k in range(N):
            Liste_Probas_a_t.append(proba_distrib_LT(ListeTableauSimulation[k],t))
        Probas.append(np.mean(Liste_Probas_a_t))
    plt.plot(Delais,Probas)
    plt.xlabel("unité de temps")
    plt.ylabel("Probabilité du lead time")
    plt.show()

    
# WORK IN PROGRESS
    
    
def work_in_progress(TableauSimulation, t):
    
    S = 0
    nb_bi = int(len(TableauSimulation[0])/3 - 1)
    for k in range(nb_bi):  
        S += TableauSimulation[t][3*k+1]  # On ne regarde que l'étape t pour compter les biens pas encore fini
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
    plt.show()
    
def graph_work_in_progress_plusieurs_simulations(ListeTableauSimulation, taille_max):
    L = [] * taille_max
    N = len(ListeTableauSimulation)
    Tmax = len(ListeTableauSimulation[0])

    for k in range(N):
        i = ListeTableauSimulation[k][2]
        wip = work_in_progress(ListeTableauSimulation[k],Tmax-1) 
        L[i].append(wip)
    
    Tailles_buffer = [ k for k in range(taille_max)]
    WIP = [ np.mean(L[k]) for k in range(taille_max)]
 
    plt.plot(Tailles_buffer,WIP)
    plt.xlabel("Taille du buffer")
    plt.ylabel("nombre de pièces en cours de traitement")
    plt.show()
    
def troughput(TableauSimulation):
    S = 0
    Tmax = len(TableauSimulation)
    
    for t in range(Tmax):
        S += TableauSimulation[t][-2]
    return S

def graph_throughput_plusieurs_simulations(ListeTableauSimulation, taille_max):
    L = [] * taille_max
    N = len(ListeTableauSimulation)
    Tmax = len(ListeTableauSimulation[0])

    for k in range(N):
        i = ListeTableauSimulation[k][2]
        troughput = troughput(ListeTableauSimulation[k]) 
        L[i].append(wip)
    
    Tailles_buffer = [ k for k in range(taille_max)]
    tp = [ np.mean(L[k]) for k in range(taille_max)]
 
    plt.plot(Tailles_buffer,tp)
    plt.xlabel("Taille du buffer")
    plt.ylabel("Nombre de pièces terminées")
    plt.show()

    
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
    plt.plot(Buffer,Proba_full)
    plt.xlabel("numero du buffer")
    plt.ylabel("Proba d'être ")
    plt.show()
    
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
    plt.plot(Buffer,Proba_full)
    plt.show()
 
     
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
            if TableauSimulation[tau][-1] == 1:                 # Si une piece sort
                nb_exit+=1
        t+=1
        
    return nb_exit / t             # Car t est aussi le nombre de fenetre qu'on a considéré
    
def total_production_rate_plusieurs_simulations(ListeTableauSimulation, window_lenght):
    Moyennes = []
    N = len(ListeTableauSimulation)
    
    for k in range(N):
        Moyennes.append(total_production_rate(ListeTableauSimulation[k], window_lenght))
    return np.mean(Moyennes)
    
# def graph_total_production_rate(ListeTableauSimulation, window_lenght):
#     Tailles_bufffer = []
#     Prod_rate =[]
#     N = len(ListeTableauSimulation)
#     Tmax = len(ListeTableauSimulation[0])
# 
#     for k in range(N):
#         Tailles_buffer.append(k+1)
#         
#         
#         troughput = troughput(ListeTableauSimulation[k]) 
#         L[i].append(wip)
#     
#     Tailles_buffer = [ k for k in range(taille_max)]
#     tp = [ np.mean(L[k]) for k in range(taille_max)]
#  
#     plt.plot(Tailles_buffer,tp)
#     plt.xlabel("Taille du buffer")
#     plt.ylabel("Nombre de pièces terminées")
#     plt.show()



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
                lt= T_sortie[k] - T_entree[k]
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
