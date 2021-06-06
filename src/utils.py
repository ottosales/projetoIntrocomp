# JSON reading, asset loading, etc

import json

def loadJSON(path):
    f = open(path)
    data = json.load(f)
    f.close()
    return data

def printData(data):
    print(data)