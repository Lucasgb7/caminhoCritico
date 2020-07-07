from Vertice import Vertice

class Grafo:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0
        self.tempoCritico = 0

    def addVertice(self, key, duracao):
        self.numVertices = self.numVertices + 1
        verticeAtual = Vertice(key, duracao)
        self.vertList[key] = verticeAtual
        return verticeAtual

    def getVertice(self, n):
        if n in self:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addAresta(self, v1, v2, duracao=1):
        if v1 not in self.vertList:
            self.addVertice(v1, duracao)
        if v2 not in self.vertList:
            self.addVertice(v2, duracao)
        self.vertList[v1].addAmigo(self.vertList[v2])

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())