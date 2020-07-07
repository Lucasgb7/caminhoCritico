import networkx as nx
import matplotlib.pyplot as plt
from Grafos import Grafo


def caminhoIda(grafo, vertice, tempo):
    if tempo >= vertice.getEs():
        vertice.setEs(tempo)
        tempoAtual = tempo + vertice.getDuracao()
        vertice.setEf(tempoAtual)
        if vertice.getEf() > grafo.tempoCritico:
            grafo.tempoCritico = vertice.getEf()
    for amigo in vertice.getConexoes():
        caminhoIda(grafo, amigo, tempoAtual)


def caminhoVolta(vertice, tempo):
    tempoAtual = vertice.getLs()
    if tempo <= vertice.getLf() or vertice.getLf() == -1:
        vertice.setLf(tempo)
        tempoAtual = tempo - vertice.getDuracao()
        vertice.setLs(tempoAtual)
    for amigo in vertice.getPredecessores():
        caminhoVolta(amigo, tempoAtual)


def calculaFolga(grafo):
    for i in range(grafo.numVertices):
        grafo.getVertice(i).changeFolga()


def verticesAuxiliares(grafo, vertice_final):
    for i in range(grafo.numVertices - 1):
        if not grafo.getVertice(i).getConexoes():
            grafo.addAresta(i, vertice_final)


# NOJO
if __name__ == '__main__':
    g = Grafo()
    g.addVertice(0, 0)  # inicio
    ultimoVertice = 0
    input_file = open("task2.txt", "r")
    for line in input_file.readlines():
        x = line.split(';')
        g.addVertice(int(x[0]), int(x[1]))
        ultimoVertice = int(x[0])
        y = x[2].split(',')
        if y[0] == '\n':
            y = '0'
        else:
            y[-1] = y[-1].replace('\n', '')
        for i in y:
            g.addAresta(int(i), int(x[0]))

    g.addVertice(ultimoVertice + 1, 0)  # fim
    verticesAuxiliares(g, ultimoVertice + 1)
    # for i in range(g.numVertices):
    #    print(g.getVertice(i))
    caminhoIda(g, g.getVertice(0), 0)
    caminhoVolta(g.getVertice(ultimoVertice + 1), g.tempoCritico)
    calculaFolga(g)

    # for i in range(1, g.numVertices - 1):
    #    print(str(i) + ": " + str(g.getVertice(i).getEs()) + "-" + str(g.getVertice(i).getEf()) + " / " + str(g.getVertice(i).getLs()) + "-" + str(g.getVertice(i).getLf()) + " / " + str(g.getVertice(i).getGap()))

    # ================================ VIADAGEM PRA PRINTAR =============================
    G = nx.DiGraph()

    for i in range(g.numVertices):
        if i == 0:
            string = "Início"
        elif i == ultimoVertice + 1:
            string = "Fim"
        else:
            string = str(g.getVertice(i).getId()) + "\n" + str(g.getVertice(i).getEs()) + "-" + str(
                g.getVertice(i).getEf()) + "\n" + str(g.getVertice(i).getLs()) + "-" + str(
                g.getVertice(i).getLf()) + "\n" + str(g.getVertice(i).getFolga())
        G.add_node(string)

    for i in range(g.numVertices):
        for j in g.getVertice(i).getConexoes():
            if i == 0:
                stringI = "Início"
            else:
                stringI = str(g.getVertice(i).getId()) + "\n" + str(g.getVertice(i).getEs()) + "-" + str(
                    g.getVertice(i).getEf()) + "\n" + str(g.getVertice(i).getLs()) + "-" + str(
                    g.getVertice(i).getLf()) + "\n" + str(g.getVertice(i).getFolga())
            if j.getId() == ultimoVertice + 1:
                stringJ = "Fim"
            else:
                stringJ = str(j.getId()) + "\n" + str(j.getEs()) + "-" + str(j.getEf()) + "\n" + str(
                    j.getLs()) + "-" + str(j.getLf()) + "\n" + str(j.getFolga())
            G.add_edge(stringI, stringJ)

    color_map = []
    for i in range(g.numVertices):
        if i == 0 or i == ultimoVertice + 1:
            color_map.append('green')
        elif g.getVertice(i).getFolga() == 0:
            color_map.append('red')
        else:
            color_map.append('blue')

    # nx.draw_circular(G, arrows=True, with_labels=True, node_size=2600, node_color=color_map, font_size=10)
    pos = nx.spring_layout(G)
    plt.figure(3, figsize=(10, 10))
    nx.draw(G, pos, arrows=True, with_labels=True, node_size=3500, node_color=color_map, font_size=12)
    plt.show()
