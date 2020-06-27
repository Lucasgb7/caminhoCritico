import numpy as np
from Graphs import Graphs
# https://escritoriodeprojetos.com.br/metodo-do-caminho-critico


def forward_pass(task):
    for fw in task: # atividade de ida
        if '-1' in task[fw]['dependencies']:    # verifica se e a primeira atividade (vertice)
            task[fw]['ES'] = 1
            task[fw]['EF'] = task[fw]['duration']
        else:
            for k in task.keys():
                for dependency in task[k]['dependencies']:  # passa por todas as dependencias de uma atividade
                    if dependency != '-1' and len(task[k]['dependencies']) == 1:
                        task[k]['ES'] = int(task[dependency]['EF']) + 1
                        task[k]['EF'] = int(task[k]['ES']) + int(task[k]['duration']) - 1
                    elif dependency != '-1':
                        if int(task[dependency]['EF']) > int(task[k]['ES']):
                            task[k]['ES'] = int(task[dependency]['EF']) + 1
                            task[k]['EF'] = int(task[k]['ES']) + int(task[k]['duration']) - 1


def backward_pass(task):
    for taskBW in bList:
        if (bList.index(taskBW) == 0):  # check if it's the last task (so no more task)
            tasks[taskBW]['LF'] = tasks[taskBW]['EF']
            tasks[taskBW]['LS'] = tasks[taskBW]['ES']

        for dipendenza in tasks[taskBW]['dependencies']:  # slides all the dependency in a single task
            if (dipendenza != '-1'):  # check if it's NOT the last task
                if (tasks['task' + dipendenza]['LF'] == 0):  # check if the the dependency is already analyzed
                    # print('ID dipendenza: '+str(tasks['task'+dipendenza]['id']) + ' taskBW: '+str(tasks[taskBW]['id']))
                    tasks['task' + dipendenza]['LF'] = int(tasks[taskBW]['LS']) - 1
                    tasks['task' + dipendenza]['LS'] = int(tasks['task' + dipendenza]['LF']) - int(
                        tasks['task' + dipendenza]['duration']) + 1
                    tasks['task' + dipendenza]['float'] = int(tasks['task' + dipendenza]['LF']) - int(
                        tasks['task' + dipendenza]['EF'])
                    # print('IF1 dip LS: '+str(tasks['task'+dipendenza]['LS']) +' dip LF: '+str(tasks['task'+dipendenza]['LF']) + ' taskBW: '+str(tasks[taskBW]['id'])+' taskBW ES '+ str(tasks[taskBW]['ES']))
                if (int(tasks['task' + dipendenza]['LF']) > int(
                        tasks[taskBW]['LS'])):  # put the minimun value of LF for the dependencies of a task
                    tasks['task' + dipendenza]['LF'] = int(tasks[taskBW]['LS']) - 1
                    tasks['task' + dipendenza]['LS'] = int(tasks['task' + dipendenza]['LF']) - int(
                        tasks['task' + dipendenza]['duration']) + 1
                    tasks['task' + dipendenza]['float'] = int(tasks['task' + dipendenza]['LF']) - int(
                        tasks['task' + dipendenza]['EF'])
                    # print('IF2 dip LS: '+str(tasks['task'+dipendenza]['LS']) +' dip LF: '+str(tasks['task'+dipendenza]['LF']) + ' taskBW: '+str(tasks[taskBW]['id']))

if __name__ == '__main__':
    # Tabela de atividades
    # activity = ['A', 'B', 'C', 'D', 'E', 'F']    # atividades
    # duration = [10, 4, 7, 5, 5, 2]               # duracao de cada atividade
    # previous = ['', 'A', 'A', 'C', 'B,D', 'C']  # precedente das atividades
    activity = ['0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', '1']  # atividades
    duration = [0, 6, 2, 3, 10, 3, 2, 4, 5, 8, 6, 4, 2]  # duracao de cada atividade
    previous = ['', '0', '0', '0', 'A', 'A', 'B', 'C', 'E', 'F,G', 'G', 'I', 'J',
                'D,H,K,L']  # precedente das atividades
    table_length = len(activity)

    task = dict()
    for i in range(table_length):
        task[i] = dict()
        task[i]['id'] = activity[i]
        task[i]['duration'] = duration[i]
        if len(previous[i]) > 1:  # mais de uma dependencia
            aux = previous[i].split(',')
            for d in aux:
                task[i]['dependencies'] = d
        else:
            task[i]['dependencies'] = previous[i]
        task[i]['ES'] = 0
        task[i]['EF'] = 0
        task[i]['LS'] = 0
        task[i]['LF'] = 0
        task[i]['ES'] = 0
        task[i]['float'] = 0
        task[i]['critical'] = False

    forward_pass(task)
    edges = []
    for i in range(table_length):  # Em cada atividade
        if len(previous[i]) < 1:
            root = activity[i]  # vertice inicial
            task['id'] = root
            edges.append([root, root])  # caso nao tenha antecessor e o proprio vertice inicial
        elif len(previous[i]) > 1:
            aux = previous[i].split(',')
            for j in aux:
                edges.append([j, activity[i]])  # Caso tenha mais de um antecessor, adiciona cada um
        else:
            edges.append([previous[i], activity[i]])  # Adiciona o antecessor

    print("Arestas: ", edges)  # add edges
    graph = Graphs(edges, True)  # insere as arestas, e determina como 'direcionado'
    visited = []
    dfs(graph, root, visited)
    print("DFS: ", visited)
    visited = []
    bfs(graph, root, visited)
    print("BFS: ", visited)
