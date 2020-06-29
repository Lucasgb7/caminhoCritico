from Graphs import Graphs
# https://escritoriodeprojetos.com.br/metodo-do-caminho-critico


def forward_pass(task):
    for fw in task: # atividade de ida
        if '-1' in task[fw]['dependencies']:    # verifica se e a primeira atividade (vertice)
            task[fw]['ES'] = 1
            task[fw]['EF'] = task[fw]['duration']
        else:
            for k in task.keys():***
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
        if (keys_reverse.index(bw) == 0):   # verifica se e a ultima atividade
            tasks[bw]['LF'] = tasks[bw]['EF']
            tasks[bw]['LS'] = tasks[bw]['ES']

        for dependency in tasks[bw]['dependencies']:  # slides all the dependency in a single task
            if (dependency != '-1'):  # check if it's NOT the last task
                if (tasks[dependency]['LF'] == 0):  # check if the the dependency is already analyzed
                    # print('ID dependency: '+str(tasks['task'+dependency]['id']) + ' bw: '+str(tasks[bw]['id']))
                    tasks[dependency]['LF'] = int(tasks[bw]['LS']) - 1
                    tasks[dependency]['LS'] = int(tasks[dependency]['LF']) - int(
                        tasks[dependency]['duration']) + 1
                    tasks[dependency]['float'] = int(tasks[dependency]['LF']) - int(
                        tasks[dependency]['EF'])
                    # print('IF1 dip LS: '+str(tasks['task'+dependency]['LS']) +' dip LF: '+str(tasks['task'+dependency]['LF']) + ' bw: '+str(tasks[bw]['id'])+' bw ES '+ str(tasks[bw]['ES']))
                if (int(tasks[dependency]['LF']) > int(
                        tasks[bw]['LS'])):  # put the minimun value of LF for the dependencies of a task
                    tasks[dependency]['LF'] = int(tasks[bw]['LS']) - 1
                    tasks[dependency]['LS'] = int(tasks[dependency]['LF']) - int(
                        tasks[dependency]['duration']) + 1
                    tasks[dependency]['float'] = int(tasks[dependency]['LF']) - int(
                        tasks[dependency]['EF'])
                    # print('IF2 dip LS: '+str(tasks['task'+dipendenza]['LS']) +' dip LF: '+str(tasks['task'+dipendenza]['LF']) + ' bw: '+str(tasks[bw]['id']))

if __name__ == '__main__':
    # Tabela de  atividades
    # activity = ['A', 'B', 'C', 'D', 'E', 'F']    # atividades
    # duration = [10, 4, 7, 5, 5, 2]               # duracao de cada atividade
    # previous = ['', 'A', 'A', 'C', 'B,D', 'C']  # precedente das atividades
    activity = ['0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', '1']  # atividades
    duration = [0, 6, 2, 3, 10, 3, 2, 4, 5, 8, 6, 4, 2, 0]  # duracao de cada atividade
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

    forward_pass(task) # faz o caminho de ida

    keys = list()
    for e in task.keys(): # lista das chaves das atividades
        keys.append(e)

    keys_reverse = list()
    while len(keys) > 0:    # lista das chaves ao contrario para caminho de volta
        keys_reverse.append(keys.pop())
    
    backward_pass(task, keys_reverse)

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

    print('task id, task name, duration, ES, EF, LS, LF, float, isCritical')
    for task in tasks:
        if(tasks[task]['float'] == 0): # folga = 0 faz parte do caminho critico
            tasks[task]['isCritical'] = True
        print(str(tasks[task]['id']) +', '+str(tasks[task]['name']) +', '+str(tasks[task]['duration']) +', '+str(tasks[task]['ES']) +', '+str(tasks[task]['EF']) +', '+str(tasks[task]['LS']) +', '+str(tasks[task]['LF']) +', '+str(tasks[task]['float']) +', '+str(tasks[task]['isCritical']))
