from . import planning_donnees as planning

#Contrainte de couverture des besoins de l'hopital, revoie si l'alerte est trigger et l'ensembles des (semaine, jour, creneau) qui trigger l'alerte
def besoinsOK(plan):
    resu = []
    for s in range(plan.nombreSemaines):
        for j in range(7):
            for c in range(plan.nombreCreneaux-1):
                if len(plan.semaines[s][j][c]) != plan.besoins[s][j][c]:
                    resu.append((s,j,c))
    return len(resu) != 0, resu

#Contrainte de couverture des besoins en Jca de l'hopital , revoie si l'alerte est trigger et l'ensembles des (semaine, jour) qui trigger l'alerte
def besoinsJcaOK(plan):
    resu = []
    for s in range(plan.nombreSemaines):
        for j in range(7):
            jca = plan.nombreCreneaux-1
            if len(plan.semaines[s][j][jca]) != plan.besoinsJca[s][j]:
                resu.append((s,j))
    return len(resu) != 0, resu

#Contrainte d'encadrement de durée de travail par semaine, revoie si l'alerte est trigger et l'ensembles des (agent, semaine) qui trigger l'alerte
def encadrementDureeTravail(plan):
    resu = []
    for a in range(plan.nbAgents):
        for s in range(plan.nombreSemaines):
            h = plan.heuresTravaillees(s,a)
            if h < 35*plan.proratas[a] - 8 or h > 35*plan.proratas[a] + 8:
                resu.append((a,s))
    return len(resu) != 0, resu

#Contrainte de repos journalière, revoie si l'alerte est trigger et l'ensembles des (agent, semaine, jour) qui trigger l'alerte
def reposJournalier(plan):
    resu = []
    for a in range(plan.nbAgents):
        for s in range(plan.nombreSemaines):
            for j in range(7):
                nb = 0
                for c in range(plan.nombreCreneaux):
                    if a in plan.semaines[s][j][c]:
                        nb+= 1
                if nb > 1:
                    resu.append((a,s,j))
    return len(resu) != 0, resu

#Contrainte pas de travail un jour seul, au moins 2 jours consecutifs, revoie si l'alerte est trigger et l'ensembles des (agent, semaine, jour) qui trigger l'alerte
def jourIsole(plan):
    resu = []
    for a in range(plan.nbAgents):
        for s in range(plan.nombreSemaines):
            for j in range(7):
                bool = False
                if plan.agentTravailATelleDate(a, s, j):
                    bool = True
                    if j < 6:
                        if plan.agentTravailATelleDate(a, s, j+1):
                            bool = False
                    if bool and j == 6:
                        if s < plan.nombreSemaines-1:
                            if plan.agentTravailATelleDate(a,s+1,0):
                                bool = False
                    if bool and j > 0:
                        if plan.agentTravailATelleDate(a,s,j-1):
                            bool = False
                    if bool and j == 0:
                        if s > 0:
                            if agentTravailATelleDate(a,s-1,6):
                                bool = False
                if bool:
                    resu.append((a,s,j))
    return len(resu) != 0, resu



if __name__ == "__main__":
    #test1
    besoinsJcaS1 = [0, 0, 1, 0, 0, 0, 0]
    besoinsS1 = [[1,0,1], [0,2,0], [0,0,0], [1,1,1], [0,0,0], [0,0,0], [0,0,0]]
    planS1Y = [[[1],[],[0],[]], [[],[0,1],[],[]], [[],[],[],[1]], [[0],[0],[1],[]], [[],[],[],[]], [[],[],[],[]], [[],[],[],[]]]
    planS1NBes = [[[1],[],[],[]], [[],[0,1],[],[]], [[],[],[],[1]], [[0],[0],[1],[]], [[],[],[],[]], [[],[],[],[]], [[],[],[],[]]]
    planS1NJca = [[[1],[],[0],[]], [[],[0,1],[],[]], [[],[],[],[]], [[0],[0],[1],[]], [[],[],[],[]], [[],[],[],[]], [[],[],[],[]]]
    planOK = planning.Planning(2, [besoinsS1], [besoinsJcaS1], [planS1Y], [1,1])
    planNBes = planning.Planning(2, [besoinsS1], [besoinsJcaS1], [planS1NBes], [1,1])
    planNJca = planning.Planning(2, [besoinsS1], [besoinsJcaS1], [planS1NJca], [1,1])
    print(besoinsOK(planOK))
    print(besoinsOK(planNBes))
    print()
    print(besoinsJcaOK(planOK))
    print(besoinsJcaOK(planNJca))
    print()

    planNE = planning.Planning(2, [besoinsS1], [besoinsJcaS1], [planS1Y], [1,3])
    print(encadrementDureeTravail(planOK))
    print(encadrementDureeTravail(planNE))
    print()

    print(reposJournalier(planOK))
    print()

    print(planOK.agentTravailATelleDate(0,0,4))
    print(planOK.agentTravailATelleDate(0,0,5))
    print(jourIsole(planOK))
    print()
    
# agents, semaine, jour, creneau sont des int
# indicateurs gravité croissante de 1 à 3
# {"alertes" : 
#   {"besoin incomplets" : [boolean, array[semaine, jour, creneau]],
#    "besoin jca incomplets" : [boolean , array[semaine, jour]],
#    "duree de travail hebdomadaire invalide" : [boolean, array[agent, semaine, jour]],
#    "repos journalier insuffisant" : [boolean, array[agent, semaine, jour]],
#    "repos bihebdo insuffisant" : [boolean, array[agent, semaine1, semaine2]],
#    "jour isolé" : [boolean, array[semaine, jour]],
#    "plus de 5 jours consécutifs travailles" : [boolean, array[agent, semaine]]
#   },
#  "indicateurs" : 
#    {"équité creneaux penibles" : [123, agent qui a le plus de creneaux penibles],
#     "équité jca" : [123, agent qui a le plus de creneaux penibles]
#    }
# }
