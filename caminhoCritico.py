from Graphs import Graphs
from collections import defaultdict


# https://escritoriodeprojetos.com.br/metodo-do-caminho-critico


def forward_pass(task):
    for fw in task:  # atividade de ida
        if '-1' in task[fw]['dependencies']:  # verifica se e a primeira atividade (vertice)
            task[fw]['ES'] = 1  # early start
            task[fw]['EF'] = task[fw]['duration']   # early finish
        else:  # nao e a primeira atividade
            for k in task.keys():
                for dependency in task[k]['dependencies']:  # passa por todas as dependencias de uma atividade
                    if dependency != '-1' and len(task[k]['dependencies']) == 1:
                        task[k]['ES'] = int(task[dependency]['EF']) + 1
                        task[k]['EF'] = int(task[k]['ES']) + int(task[k]['duration']) - 1
                    elif dependency != '-1':
                        if int(task[dependency]['EF']) > int(task[k]['ES']):
                            task[k]['ES'] = int(task[dependency]['EF']) + 1
                            task[k]['EF'] = int(task[k]['ES']) + int(task[k]['duration']) - 1


def backward_pass(task, keys_reverse):
    for bw in keys_reverse:
        if keys_reverse.index(bw) == 0:  # verifica se e a ultima atividade
            task[bw]['LF'] = task[bw]['EF']
            task[bw]['LS'] = task[bw]['ES']

        for dependency in task[bw]['dependencies']:  # passa por todos as atividades dependentes
            if dependency != '-1':  # verifica se nao e a ultima dependencia
                if task[dependency]['LF'] == 0:  # verifica se a dependencia ja foi analizada
                    print('ID_Depedencia: '+str(task[dependency]['id']) + ' bw: '+str(task[bw]['id']))
                    task[dependency]['LF'] = int(task[bw]['LS']) - 1
                    task[dependency]['LS'] = int(task[dependency]['LF']) - int(task[dependency]['duration']) + 1
                    task[dependency]['float'] = int(task[dependency]['LF']) - int(task[dependency]['EF'])
                    print('IF1 dip LS: '+str(task[dependency]['LS']) +' dip LF: '+str(task[dependency]['LF']) + ' bw: '+str(task[bw]['id'])+' bw ES '+ str(task[bw]['ES']))
                if int(task[dependency]['LF']) > int(task[bw]['LS']):  # insere o menor valor do LF para atividade dependente
                    task[dependency]['LF'] = int(task[bw]['LS']) - 1
                    task[dependency]['LS'] = int(task[dependency]['LF']) - int(task[dependency]['duration']) + 1
                    task[dependency]['float'] = int(task[dependency]['LF']) - int(task[dependency]['EF'])
                    print('IF2 dip LS: '+str(task[dependency]['LS']) +' dip LF: '+str(task[dependency]['LF']) + ' bw: '+str(task[bw]['id']))


if __name__ == '__main__':
    ### Tabela de  atividades
    # activity = ['A', 'B', 'C', 'D', 'E', 'F']    # atividades
    # duration = [10, 4, 7, 5, 5, 2]               # duracao de cada atividade
    # previous = ['', 'A', 'A', 'C', 'B,D', 'C']  # precedente das atividades

    # activity = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', '1']  # atividades
    # duration = [6, 2, 3, 10, 3, 2, 4, 5, 8, 6, 4, 2, 0]  # duracao de cada atividade
    # previous = ['', '', '', 'A', 'A', 'B', 'C', 'E', 'F,G', 'G', 'I', 'J', 'D,H,K,L']  # precedente das atividades

    # activity = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']  # atividades
    # duration = [12, 6, 12, 18, 2, 10, 8, 8, 6, 2, 8]  # duracao de cada atividade
    # previous = ['', 'A', 'A', 'A', 'B', 'C,D', 'D', 'E', 'F', 'G', 'H,I,J']

    line = list()   # cada linha do txt
    element = list()   # cada elemento do txt
    task = dict()
    file = open('task2.txt')

    for line in file:
        element = line.split(',')
        for i in range(len(element)):
            task[element[0]] = dict()
            task[element[0]]['id'] = element[0]
            task[element[0]]['name'] = element[1]
            task[element[0]]['duration'] = element[2]
            if element[3] != "\n":  # tem dependencia
                task[element[0]]['dependencies'] = element[3].strip().split(';')
            else:
                task[element[0]]['dependencies'] = ['-1']  # nao tem dependencia
            task[element[0]]['ES'] = 0
            task[element[0]]['EF'] = 0
            task[element[0]]['LS'] = 0
            task[element[0]]['LF'] = 0
            task[element[0]]['float'] = 0
            task[element[0]]['critical'] = False

    forward_pass(task)  # faz o caminho de ida

    keys = list()
    for e in task.keys():  # lista das chaves das atividades
        keys.append(e)

    keys_reverse = list()
    while len(keys) > 0:  # lista das chaves ao contrario para caminho de volta
        keys_reverse.append(keys.pop())

    backward_pass(task, keys_reverse)

    """""
    edges = []
    for i in range(table_length):  # Em cada atividade
        if len(previous[i]) < 1:
            root = activity[i]  # vertice inicial
            edges.append([root, root])  # caso nao tenha antecessor e o proprio vertice inicial
        elif len(previous[i]) > 1:
            aux = previous[i].split(',')
            for j in aux:
                edges.append([j, activity[i]])  # Caso tenha mais de um antecessor, adiciona cada um
        else:
            edges.append([previous[i], activity[i]])  # Adiciona o antecessor

    print("Arestas: ", edges)  # add edges
    """

    print('ID Atividade, Duracao, ES, EF, LS, LF, float, critical')
    for t in task:
        if task[t]['float'] == 0:  # folga = 0 faz parte do caminho critico
            task[t]['critical'] = True
        print(str(task[t]['id']) + ', ' + str(task[t]['name']) + ',' + str(task[t]['duration']) + ', ' + str(
            task[t]['ES']) + ', ' + str(task[t]['EF']) + ', ' + str(task[t]['LS']) + ', ' + str(
            task[t]['LF']) + ', ' + str(task[t]['float']) + ', ' + str(task[t]['critical']))
