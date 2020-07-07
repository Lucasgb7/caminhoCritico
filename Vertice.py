class Vertice:
    def __init__(self, key, duracao):
        self.id = key
        self.sucessor = {}  # sucessores
        self.predecessor = {}  # predecessores
        self.duracao = duracao  # duracao no node
        self.es = 0  # tempo inicial mais cedo
        self.ef = 0  # tempo final mais cedo
        self.ls = -1  # tempo inicial mais tarde
        self.lf = -1  # tempo final mais tarde
        self.folga = 0  # folga

    def addAmigo(sel, amigo):
        sel.sucessor[amigo] = 1
        amigo.predecessor[sel] = 1

    def setDuracao(self, duracao):
        self.duracao = duracao

    def setEs(self, es):
        self.es = es

    def setEf(self, ef):
        self.ef = ef

    def setLs(self, ls):
        self.ls = ls

    def setLf(self, lf):
        self.lf = lf

    def changeFolga(self):
        self.folga = self.lf - self.ef

    def getConexoes(self):
        return self.sucessor.keys()

    def getPredecessores(self):
        return self.predecessor.keys()

    def getId(self):
        return self.id

    def getDuracao(self):
        return self.duracao

    def getEs(self):
        return self.es

    def getEf(self):
        return self.ef

    def getLs(self):
        return self.ls

    def getLf(self):
        return self.lf

    def getFolga(self):
        return self.folga