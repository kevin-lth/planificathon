class Planning():
    def __init__(self, nbAgents, besoins, besoinsJca, semaines, proratas, seuilEquiteCreneaux = 4, seuilEquiteJca = 4):
        self.nbAgents = nbAgents
        self.besoins = besoins
        self.besoinsJca = besoinsJca
        self.semaines = semaines
        self.nombreSemaines = len(semaines)
        self.nombreCreneaux = len(semaines[0][0])
        self.proratas = proratas
        self.seuilEquiteCreneaux = seuilEquiteCreneaux
        self.seuilEquiteJca = seuilEquiteJca
    
    def getBesoins():
        return self.besoins

    def getBesoinsJca():
        return self.besoinsJca
    
    def agentTravailATelleDate(self, agent, semaine, jour):
        for c in self.semaines[semaine][jour]:
            if agent in c:
                return True
        return False


    def heuresTravaillees(self, semaine, agent):
        resu = 0
        for j in self.semaines[semaine]:
            for c in j:
                if agent in c:
                    resu += 1
        return resu*8
    

    
