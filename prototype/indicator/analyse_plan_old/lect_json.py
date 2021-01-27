import json
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import planning_donnees as pld
import contraintes as ct

@dataclass_json
@dataclass
class Journee:
    besoin_matin: int
    besoin_soir: int
    besoin_nuit: int
    besoin_sve: int
    nb_jca: int
    matin: list
    soir: list
    nuit: list
    sve: list
    jca: list

def lecture(path_planjs, path_agentjs):
    with open(path_agentjs, 'r') as jsfile:
        liste_des_agents = json.load(jsfile)
    with open(path_planjs, 'r') as jsfile:
        dictjours = json.load(jsfile)

    besoins = []
    besoinsJca = []
    plan = []
    for _ in range(len(dictjours)//7):
        besoins.append([])
        besoinsJca.append([])
        plan.append([])

    for d in range(len(dictjours)):
        besoins[d//7].append([])
        besoinsJca[d//7].append([])
        plan[d//7].append([])


    for j,data in enumerate(dictjours):
        besoins[j//7][j%7] = [data['besoin_matin'], data['besoin_soir'], data['besoin_nuit']]
        besoinsJca[j//7][j%7] = data['nb_jca']
        if j%7 == 4:
            besoins[j//7][j%7][1] += data['besoin_sve']

    prorata = []
    nb_agents = len(liste_des_agents)
    for agent in liste_des_agents:
        prorata.append(agent['pourcentage']/100)

    for d in range(len(dictjours)):
        j = d%7
        w = d//7
        m = []
        s = []
        n = []
        jca = []
        _ = [m.append(a['numero']) if a['matin'][d] else None  for a in liste_des_agents]
        _ = [s.append(a['numero']) if a['soir'][d] or a['sve'][d] else None  for a in liste_des_agents]
        _ = [n.append(a['numero']) if a['nuit'][d] else None  for a in liste_des_agents]
        _ = [jca.append(a['numero']) if a['jca'][d] else None  for a in liste_des_agents]
        plan[w][j] = [m,s,n,jca]

    return (nb_agents, besoins, besoinsJca, plan, prorata)







# print(nb_agents)
# print(liste_des_agents)
# with open('planning.json', 'w') as jsfile:
#     lsjours =[]
#     for j in planning:
#         lsjours.append(j.to_dict())
#     json.dump(lsjours, jsfile)
# with open('agents.json', 'w') as jsfile:
#     json.dump(liste_des_agents, jsfile)
# 
if __name__ == "__main__":
    chemin_plan = "../converter/Importer/planning.json"
    chemin_agents = "../converter/Importer/agents.json"
    planok = pld.Planning(*lecture(chemin_plan, chemin_agents))
    print(lecture(chemin_plan, chemin_agents)[1])
    print(ct.besoinsOK(planok))




