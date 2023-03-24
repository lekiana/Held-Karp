import configparser
import numpy as np


def read_config(config_name, section_name):
    config = configparser.ConfigParser()
    config.read(config_name)
    output = list()
    section = config[section_name]
    for key, value in section.items():
        output.append(value)
    return output


def read_data(file_name):
    data = open(file_name)
    size = int(data.readline())
    connections = np.ndarray(shape=(size, size), dtype=int)
    for y in range(size):
        line = data.readline()
        x = 0
        distance = ""

        for i in range(len(line)):
            if i == 0 and line[i] == " ":
                continue

            if line[i] != " ":
                distance += line[i]
                if i == len(line) - 1:
                    connections[y][x] = distance
            else:
                if line[i - 1] != " ":
                    connections[y][x] = distance
                    x += 1
                    distance = ""
    return size, connections
