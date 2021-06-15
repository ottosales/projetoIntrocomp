# JSON reading, asset loading, etc

import json

def loadJSON(path):
    f = open(path)
    data = json.load(f)
    f.close()
    return data

def printData(data):
    print(data)

def loadTxt(path):
    data = []
    with open(path) as openfileobject:
        for line in openfileobject:
            data.append(line.rstrip('\n'))
    openfileobject.close()
    return data