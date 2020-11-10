import matplotlib.pyplot as plt
import numpy as np

# Tableau test

T1 = [["UP",1,3,"DOWN",0,4,"Up",4,4,"DOWN",0,1],["DOWN",1,3,"UP",1,4,"UP",4,4,"UP",0,1],["DOWN",0,3,"UP",1,4,"UP",3,4,"DOWN",1,0]]

T2 = [["UP",1,3,"DOWN",0,4,"UP",4,4,"DOWN","UP",4,5,"DOWN",2,6,"DOWN",0,1],

    ["UP",2,3,"UP",1,4,"UP",4,4,"DOWN",3,5,"UP",4,5,"DOWN",2,6,"DOWN",0,1],
    
    ["UP",1,3,"DOWN",0,4,"UP",4,4,"DOWN",2,5,"UP",4,5,"DOWN",2,6,"DOWN",0,1],
    
    ["UP",1,3,"DOWN",0,4,"UP",4,4,"DOWN",1,5,"UP",4,5,"DOWN",2,6,"DOWN",1,1],
    
    ["UP",1,3,"DOWN",0,4,"UP",4,4,"DOWN",0,5,"UP",4,5,"DOWN",2,6,"DOWN",0,0],
    
    ["UP",1,3,"DOWN",0,4,"Up",4,4,"UP",1,5,"UP",4,5,"DOWN",2,6,"DOWN",1,0]]

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
        Probas.append(np.mean(Liste_Probas_a_t)
    plt.plot(Delais,Probas)
    plt.show()
    

    
# WORK IN PROGRESS
    
def work_in_progress(TableauSimulation, t):
    
    S = 0
    nb_bi = int(len(TableauSimulation[0])/3 - 1)
    for k in range(nb_bi):  # On ne regarde que l'étape t pour compter les biens pas encore fini
        S+=TableauSimulation[t][3*k+1]
        
    return S
    
#  def graph_work_in_progress_  je la fais incessemment sous peu

#def blocking_probability        
#depend trop de comment seront codés les résultats de simulation pour etre implémenter maintenant



def stravation_probability(TableauSimulation):
    S = 0
    S_empty = 0
    T = len(TableauSimulation)
    nb_bi = int(len(TableauSimulation[0])/3 - 1)
    
    for t in range(T):
        for k in range(nb_bi):
            if TableauSimulation[t][3*k+1] == 0:
                S_empty += 1
            S += 1
    return S_empty/S
    
    
    
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
    