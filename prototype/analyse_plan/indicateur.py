import planning_donnees as planning


#Je m'interesse uniquement au creneau nuit mais possible d'etendre aux autres creneaux si plus de temps
#indicateur à 3 si ecart depasse 120% du seuil
def indicateurCreneaux(plan):
    resu = []
    for c in range(3):
        nb = 0
        for s in plan.semaines:
            for j in s:
                if 0 in j[c]:
                    nb += 1
        min = nb
        max = nb
        agent_max = 0
        agent_min = 0
        for a in range(1,plan.nbAgents):
            nb = 0
            for s in plan.semaines:
                for j in s:
                    if a in j[c]:
                        nb += 1
            if nb/plan.proratas[a] < min/plan.proratas[agent_min]:
                min = nb
                agent_min = a
            if nb/plan.proratas[a] > max/plan.proratas[agent_max]:
                max = nb
                agent_max = a
        ecart = max/plan.proratas[agent_max] - min/plan.proratas[agent_min]
        if ecart < plan.seuilEquiteCreneaux:
            indicateur = 1
        elif ecart < plan.seuilEquiteCreneaux*1.2:
            indicateur = 2
        else:
            indicateur = 3
        resu.append((indicateur, agent_max))
    return resu

def indicateurJca(plan):
    c = 3
    nb = 0
    for s in plan.semaines:
        for j in s:
            if 0 in j[c]:
                nb += 1
    min = nb
    max = nb
    agent_max = 0
    agent_min = 0
    for a in range(1, plan.nbAgents):
        nb = 0
        for s in plan.semaines:
            for j in s:
                if a in j[c]:
                    nb += 1
        if nb/plan.proratas[a] < min/plan.proratas[agent_min]:
            min = nb
            agent_min = a
        if nb/plan.proratas[a] > max/plan.proratas[agent_max]:
            max = nb
            agent_max = a
    ecart = max/plan.proratas[agent_max] - min/plan.proratas[agent_min]
    print(ecart)
    if ecart < plan.seuilEquiteCreneaux:
        indicateur = 1
    elif ecart < plan.seuilEquiteCreneaux*1.5:
        indicateur = 2
    else:
        indicateur = 3
    return (indicateur, agent_max)


if __name__ == "__main__":
    #test
    besoinsJcaS1 = [0, 0, 1, 0, 0, 0, 0]
    besoinsS1 = [[1,0,1], [0,2,0], [0,0,0], [1,1,1], [0,0,0], [1,1,1], [1,1,1]]
    plan = [[[1],[],[0],[]], [[],[0,1],[],[]], [[],[],[],[1]], [[0],[0],[1],[]], [[],[],[],[]], [[0],[0],[0],[1]], [[0],[0],[0],[1]]]
    plan1 = planning.Planning(2, [besoinsS1], [besoinsJcaS1], [plan], [1,1], 2, 2)
    print(indicateurCreneaux(plan1))
    print()
    print(indicateurJca(plan1))


