import itertools
import copy
import readData
import xlsxwriter as excel_writer
from time import perf_counter


previous = list()


def held_karp(vertices, size, connections, i, prev_cost):  # cost = list() - list of tuples <set, dictionary>
    if i == size:
        cost = list()
        com = set()
        for j in range(size):
            com.add(j)
        v = 0
        di = dict()
        di_p = dict()
        for j in range(len(prev_cost)):  # look for the predecessor of the start vertex
            min_weight = 1000000
            for key in prev_cost[j][1]:  # look for the end vertex for which the path value is the smallest
                weight = prev_cost[j][1][key] + connections[int(key)][v]
                if weight < min_weight:
                    min_weight = weight
                    di_p[str(v)] = int(key)
            di[str(v)] = min_weight
        cost.append((com, di))
        previous.append((com, di_p))

        # trace back
        opt = list()
        p = previous[len(previous)-1][1][str(0)]  # look for the predecessor 0 -> p
        opt.append(p)  # vertex before 0
        n = previous[len(previous)-2][1][str(p)]  # look for the predecessor p
        opt.append(n)  # n - vertex for which we are looking for a predecessor
        prev_com = previous[len(previous)-2][0]
        prev_com.remove(p)

        for i in range(size-3):
            for prev in previous:  # we are looking for the combination of the predecessor
                if prev[0] == prev_com:  # from the combination of the antecedent
                    prev_com.remove(n)
                    n = prev[1].get(str(n))
                    opt.append(n)
                    break
        opt.append(0)
        opt.reverse()
        c = cost[0][1]["0"]
        return c, opt
    else:
        combinations = list(itertools.combinations(vertices, i))
        cost = list()
        for com in combinations:
            di = dict()
            di_p = dict()
            for v in com:
                com = set(com)
                prev_com = copy.copy(com)
                prev_com.remove(v)
                for j in range(len(prev_cost)):  # look for the previous combination
                    if prev_cost[j][0] == prev_com:
                        min_weight = 1000000
                        for key in prev_cost[j][1]:  # look for the end vertex for which the path value is the smallest
                            weight = prev_cost[j][1][key] + connections[int(key)][v]
                            if weight < min_weight:
                                min_weight = weight
                                di_p[str(v)] = int(key)
                        di[str(v)] = min_weight
            cost.append((com, di))
            previous.append((com, di_p))
    i += 1
    return held_karp(vertices, size, connections, i, cost)


def main():

    # READ CONFIGURATION FILE #
    data_files = readData.read_config('config.ini', 'FILE')
    it_read = readData.read_config('config.ini', 'ITERATOR')
    iterators = [int(x) for x in it_read]
    opt_read = readData.read_config('config.ini', 'OPTIMAL_VALUE')
    optimal_values = [int(x) for x in opt_read]
    optimal_paths = readData.read_config('config.ini', 'OPTIMAL_PATH')
    output_files = readData.read_config('config.ini', 'OUTPUT')

    # CREATING OUTPUT FILE(S) #
    workbooks = list()
    for file in output_files:
        workbooks.append(excel_writer.Workbook(file))
    wb = workbooks[0]

    # HELD-KARP #
    idx = 0
    for file in data_files:
        it = iterators[idx]  # number of iterations
        opt = optimal_values[idx]  # optimal path value
        path = optimal_paths[idx]  # optimal path

        worksheet = wb.add_worksheet(file)  # write to the output file
        worksheet.write(0, 0, 'Instance name')
        worksheet.write(1, 0, file)
        worksheet.write(0, 2, 'Number of iterations')
        worksheet.write(1, 2, it)
        worksheet.write(0, 4, 'Optimal value')
        worksheet.write(1, 4, opt)
        worksheet.write(0, 6, 'Optimal path')
        worksheet.write(1, 6, path)
        worksheet.write(3, 0, 'Execution time [s]:')

        ret = readData.read_data(file)  # read the data from the file
        size = ret[0]  # instance size
        connections = ret[1]  # connection matrix
        cities = list()  # create instance elements list

        for j in range(1, size):  # node list
            cities.append(j)

        start_vertex = 0
        base_case = list()
        for k in range(1, size):  # initial case, (0 - start node)
            vertex = set()
            vertex.add(k)
            weight = dict()
            weight[str(k)] = connections[start_vertex][k]
            base_case.append((vertex, weight))

        for i in range(it):
            start = perf_counter()  # start timing
            ret = held_karp(cities, size, connections, 2, base_case)  # Held-Karp execution
            end = perf_counter()  # end timing
            elapsed = end - start
            min_dist = ret[0]
            min_path = ret[1]
            worksheet.write(i + 4, 0, elapsed)  # entry of the algorithm execution time into the output file

        print('Instance name: ' + file)
        print('Iteration nr:' + str(it))
        print('Optimal value: ' + str(min_dist))
        print('Optimal path: ' + str(min_path) + '\n')

        idx += 1
    wb.close()


if __name__ == '__main__':
    main()
