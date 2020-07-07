import networkx as nx
import matplotlib.pyplot as plt
from Grafos import Grafo


# Funcao para fazer o caminho de ida da busca
def caminhoIda(grafo, vertice, tempo):
    if tempo >= vertice.getEs():  # verifica se ja foi percorrido
        vertice.setEs(tempo)  # atribui ao ES do vertice
        tempoAtual = tempo + vertice.getDuracao()  # faz a soma do tempo atual + a duracao
        vertice.setEf(tempoAtual)  # atribui ao EF do vertice
        if vertice.getEf() > grafo.tempoCritico:  # caso seja o maior tempo encontrado
            grafo.tempoCritico = vertice.getEf()  # vertice e o caminho critico
    for amigo in vertice.getConexoes():  # vai passando entre cada um dos vertices conectados
        caminhoIda(grafo, amigo, tempoAtual)


# Funcao para fazer o caminho de volta da busca
def caminhoVolta(vertice, tempo):
    tempoAtual = vertice.getLs()
    if tempo <= vertice.getLf() or vertice.getLf() == -1:  # se já foi percorrido ou se é o ultimo
        vertice.setLf(tempo)
        tempoAtual = tempo - vertice.getDuracao()  # calculo da duracao
        vertice.setLs(tempoAtual)
    for amigo in vertice.getPredecessores():
        caminhoVolta(amigo, tempoAtual)  # repete para o proximo vertice


# Funcao que calculo a folga de todos os vertices para identificar o caminho critico
def calculaFolga(grafo):
    for i in range(grafo.numVertices):
        grafo.getVertice(i).changeFolga()


# Vertices iniciais e finais para auxilio da busca
def verticesAuxiliares(grafo, vertice_final):
    for i in range(grafo.numVertices - 1):
        if not grafo.getVertice(i).getConexoes():
            grafo.addAresta(i, vertice_final)


if __name__ == '__main__':
    g = Grafo()
    g.addVertice(0, 0)  # adiciona o vertice inicial (aux)
    ultimoVertice = 0  # adiciona o vertice final  (aux)
    input_file = open("task2.txt", "r")
    for line in input_file.readlines():
        x = line.split(';')  # separando cada elemento
        g.addVertice(int(x[0]), int(x[1]))
        ultimoVertice = int(x[0])
        y = x[2].split(',')
        if y[0] == '\n':
            y = '0'
        else:
            y[-1] = y[-1].replace('\n', '')
        for i in y:
            g.addAresta(int(i), int(x[0]))

    g.addVertice(ultimoVertice + 1, 0)  # adicionando o ultimo vertice depois do(s) ultimo(s)
    verticesAuxiliares(g, ultimoVertice + 1)

    # ================================ REALIZACAO DO ALGORTIMO =============================
    caminhoIda(g, g.getVertice(0), 0)
    caminhoVolta(g.getVertice(ultimoVertice + 1), g.tempoCritico)
    calculaFolga(g)

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
