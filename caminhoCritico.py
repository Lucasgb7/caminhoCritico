from Graphs import Graphs


# https://escritoriodeprojetos.com.br/metodo-do-caminho-critico


def forward_pass(task):
    for fw in task:  # atividade de ida
        if '-1' in task[fw]['dependencies']:  # verifica se e a primeira atividade (vertice)
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


def backward_pass(task, keys_reverse):
    for bw in keys_reverse:
        if (keys_reverse.index(bw) == 0):  # verifica se e a ultima atividade
            task[bw]['LF'] = task[bw]['EF']
            task[bw]['LS'] = task[bw]['ES']

        for dependency in task[bw]['dependencies']:  # passa por todos as atividades dependentes
            if (dependency != '-1'):  # verifica se nao e a ultima dependencia
                if (task[dependency]['LF'] == 0):  # verifica se a dependencia ja foi analizada
                    # print('ID dependency: '+str(task[dependency]['id']) + ' bw: '+str(task[bw]['id']))
                    task[dependency]['LF'] = int(task[bw]['LS']) - 1
                    task[dependency]['LS'] = int(task[dependency]['LF']) - int(
                        task[dependency]['duration']) + 1
                    task[dependency]['float'] = int(task[dependency]['LF']) - int(
                        task[dependency]['EF'])
                    # print('IF1 dip LS: '+str(task[dependency]['LS']) +' dip LF: '+str(task[dependency]['LF']) + ' bw: '+str(task[bw]['id'])+' bw ES '+ str(task[bw]['ES']))
                if (int(task[dependency]['LF']) > int(
                        task[bw]['LS'])):  # insere o menor valor do LF para atividade dependente
                    task[dependency]['LF'] = int(task[bw]['LS']) - 1
                    task[dependency]['LS'] = int(task[dependency]['LF']) - int(
                        task[dependency]['duration']) + 1
                    task[dependency]['float'] = int(task[dependency]['LF']) - int(
                        task[dependency]['EF'])
                    # print('IF2 dip LS: '+str(task[dependencies]['LS']) +' dip LF: '+str(task[dependencies]['LF']) + ' bw: '+str(task[bw]['id']))


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

    forward_pass(task)  # faz o caminho de ida

    keys = list()
    for e in task.keys():  # lista das chaves das atividades
        keys.append(e)

    keys_reverse = list()
    while len(keys) > 0:  # lista das chaves ao contrario para caminho de volta
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
    for t in task:
        if (task[t]['float'] == 0):  # folga = 0 faz parte do caminho critico
            task[t]['isCritical'] = True
        print(str(task[t]['id']) + ', ' + str(task[t]['name']) + ', ' + str(task[t]['duration']) + ', ' + str(
            task[t]['ES']) + ', ' + str(task[t]['EF']) + ', ' + str(task[t]['LS']) + ', ' + str(
            task[t]['LF']) + ', ' + str(task[t]['float']) + ', ' + str(task[t]['isCritical']))
