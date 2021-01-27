from openpyxl import load_workbook
from openpyxl.utils.cell import range_boundaries
import json
from dataclasses import dataclass
from dataclasses_json import dataclass_json

def xlsx_to_dict(filename, sheetname):

    wk = load_workbook(filename=filename, data_only=True)

    sheet  = wk[sheetname]

    row_count = sheet.max_row
    column_count = sheet.max_column

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

    liste_des_agents = []
    nb_agents = 0
    agent_row_start = None
    for i in range(1, row_count):
        if sheet.cell(row=i, column=1).value:
            if isinstance(sheet.cell(row=i, column=1).value, int):
                if not agent_row_start:
                    agent_row_start = i
                nb_agents += 1
                liste_des_agents.append(dict({'numero': nb_agents, 'pourcentage':sheet.cell(row=i,column=2).value}))

    for r in range(agent_row_start, agent_row_start+nb_agents):
        matin = [1 if (sheet.cell(column=c, row=r).value == 'M') else 0 for c in range(4, column_count)]
        soir = [1 if (sheet.cell(column=c, row=r).value == 'S') else 0 for c in range(4, column_count)]
        nuit = [1 if (sheet.cell(column=c, row=r).value == 'N') else 0 for c in range(4, column_count)]
        sve = [1 if (sheet.cell(column=c, row=r).value == 'Sve') else 0 for c in range(4, column_count)]
        jca = [1 if (sheet.cell(column=c, row=r).value == 'Jca') else 0 for c in range(4, column_count)]
        i = r - agent_row_start
        liste_des_agents[i]['matin'] = matin
        liste_des_agents[i]['soir'] = soir
        liste_des_agents[i]['nuit'] = nuit
        liste_des_agents[i]['sve'] = sve
        liste_des_agents[i]['jca'] = jca

    besoins_matin = [sheet.cell(column=c, row=nb_agents+agent_row_start).value for c in range(4, column_count)]
    besoins_soir = [sheet.cell(column=c, row=nb_agents+agent_row_start+1).value for c in range(4, column_count)]
    besoins_nuit = [sheet.cell(column=c, row=nb_agents+agent_row_start+2).value for c in range(4, column_count)]
    besoins_sve = [sheet.cell(column=c, row=nb_agents+agent_row_start+3).value for c in range(4, column_count)]
    nb_jca = [sheet.cell(column=c, row=nb_agents+agent_row_start+4).value for c in range(4, column_count)]
    for k in range(len(nb_jca)):
        if nb_jca[k] is None:
            nb_jca[k] = 0
    planning = []
    for d in range(column_count - 4):
        bm = besoins_matin[d]
        bs = besoins_soir[d]
        bn = besoins_nuit[d]
        bv = besoins_sve[d]
        nj = nb_jca[d]
        matin_ass = []
        soir_ass = []
        nuit_ass = []
        sve_ass = []
        jca_ass = []
        for a in liste_des_agents:
            if a['matin'][d]:
                matin_ass.append(a['numero'])
            if a['soir'][d]:
                soir_ass.append(a['numero'])
            if a['nuit'][d]:
                nuit_ass.append(a['numero'])
            if a['sve'][d]:
                sve_ass.append(a['numero'])
            if a['jca'][d]:
                jca_ass.append(a['numero'])
        jour = Journee(bm,bs,bn,bv,nj,matin_ass,soir_ass,nuit_ass,sve_ass,jca_ass)
        planning.append(jour)

    lsjours =[]
    for j in planning:
        lsjours.append(j.to_dict())
    return { "planning": lsjours, "agents": liste_des_agents }
