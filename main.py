import math
from prettytable import PrettyTable

maxsize = float('inf')


def getFile():
    text = []
    with open("data.txt", "r") as file:
        lines = file.readlines()
        for i in lines:
            text.append(i.replace('\n', ''))
    for i in range(len(text)):
        text[i] = text[i].split(" ")
    return text


def copyToFinal(curr_path):
    final_path[:numberOfNodes + 1] = curr_path[:]
    final_path[numberOfNodes] = curr_path[0]


def firstMin(adj, i):
    min = maxsize
    for k in range(numberOfNodes):
        if adj[i][k] < min and i != k:
            min = adj[i][k]

    return min


def secondMin(adj, i):
    first, second = maxsize, maxsize
    for j in range(numberOfNodes):
        if i == j:
            continue
        if adj[i][j] <= first:
            second = first
            first = adj[i][j]
        elif (adj[i][j] <= second and
              adj[i][j] != first):
            second = adj[i][j]

    return second


def TSPRec(adj, curr_bound, curr_weight, level, curr_path, visited):
    global final_res

    if level == numberOfNodes:
        if adj[curr_path[level - 1]][curr_path[0]] != 0:
            curr_res = curr_weight + adj[curr_path[level - 1]][curr_path[0]]
            if curr_res < final_res:
                copyToFinal(curr_path)
                final_res = curr_res
        return

    for i in range(numberOfNodes):
        if adj[curr_path[level - 1]][i] != 0 and visited[i] == False:
            temp = curr_bound
            curr_weight += adj[curr_path[level - 1]][i]

            if level == 1:
                curr_bound -= ((firstMin(adj, curr_path[level - 1]) + firstMin(adj, i)) / 2)
            else:
                curr_bound -= ((secondMin(adj, curr_path[level - 1]) + firstMin(adj, i)) / 2)

            if curr_bound + curr_weight < final_res:
                curr_path[level] = i
                visited[i] = True

                TSPRec(adj, curr_bound, curr_weight, level + 1, curr_path, visited)

            curr_weight -= adj[curr_path[level - 1]][i]
            curr_bound = temp

            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True


def TSP(adj, N):
    curr_bound = 0
    curr_path = [-1] * (N + 1)
    visited = [False] * N

    for i in range(N):
        curr_bound += (firstMin(adj, i) + secondMin(adj, i))

    curr_bound = math.ceil(curr_bound / 2)

    visited[0] = True
    curr_path[0] = 0

    TSPRec(adj, curr_bound, 0, 1, curr_path, visited)


if __name__ == '__main__':
    array = getFile()
    array = [[int(j) if '.' not in j else float(j) for j in i] for i in array]
    numberOfNodes = int(array[0][0])
    matrix = array[1:]

    table = PrettyTable([chr(i) for i in range(65, 65 + numberOfNodes)])
    for i in matrix:
        table.add_row(i)
    print(table)

    final_path = [None] * (numberOfNodes + 1)
    visited = [False] * numberOfNodes
    final_res = maxsize

    TSP(matrix, numberOfNodes)

    for i in range(numberOfNodes + 1):
        final_path[i] += 1
    print("Min cost:", final_res)
    print('Path:', ' -> '.join(map(str, final_path)))
    print('Path:', ' -> '.join(map(lambda i: chr(64 + i), final_path)))
