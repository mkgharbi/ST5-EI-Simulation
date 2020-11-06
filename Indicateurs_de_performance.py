import random as rd    # seulement pour tester les programmes 
p_entree = 0.9         # seulement pour tester les programmes 
p_sortie = 0.5         # seulement pour tester les programmes



def proba_distrib_LT(TableauMi, TableauBi, temps_attendu):
    T_entree = []
    T_sortie = []
    T = len(TableauMi)
    
    for t in range(T):
        if rd.random() < p_entree:    # Si une piece rentre, condition à modifier
            T_entree.append(t)
        if rd.random() < p_sortie:    # Si une piece sort, condition à modifier
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
    
    
    
def work_in_progress(TableauBi, t):
    
    S = 0
    for bi in TableauBi[t]:  # On ne regarde que l'étape t pour compter les biens pas encore fini
        S+=bi
        
    return S
    
    

#def blocking_probability        
#depend trop de comment seront codés les résultats de simulation pour etre implémenter maintenant



def stravation_probability(TableauBi):
    S = 0
    S_empty = 0
    
    for bi in TableauBi:
        if bi==0:
            S_empty+=1
        S+=1
        
    return S_empty/S
    
    
    
def total_production_rate(TableauMi, TableauBi, window_lenght):
    T = len(TableauMi)
    wl = window_lenght
    nb_exit = 0
    
    t = 0
    while t < T - wl:
        for tau in range(t,t+wl):
            if True:               # Si une piece sort, condition à changer
                nb_exit+=1
        t+=1
        
    return nb_exit / t             # Car t est aussi le nombre de fenetre qu'on a considéré
    
    

def effective_production_rate(TableauMi, TableauBi, window_lenght):
    T_entree = []
    T_sortie = []
    T = len(TableauMi)
    
    for t in range(T):
        if rd.random() < p_entree:    # Si une piece rentre, condition à modifier
            T_entree.append(t)
        if rd.random() < p_sortie:    # Si une piece sort, condition à modifier
            T_sortie.append(t)

    wl = window_lenght
    nb_exit = 0
    
    t = 0
    while t < T - wl :
        for tau in range(t,t+window_lenght):
            if t in T_sortie :
                k = T_sortie.index(t) 
                lt= T_sortie[k] - T_entree[k]
                if lt < wl:
                    nb_exit +=1
        t+=1
        
    return nb_exit / t
    