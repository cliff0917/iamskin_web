
import yaml
import json
import pickle
import os
import pprint
import shutil

def loadYaml(path='environment.yaml'):

    with open(path) as paper:
        
        content = yaml.load(paper, yaml.loader.SafeLoader)
        pass

    return(content)

def loadJson(path):

    with open(path) as paper:
        
        content = json.loads(paper)
        pass

    return(content)

def loadPickle(path):

    with open(path, 'rb') as paper:

        content = pickle.load(paper)
        pass

    return(content)

def savePickle(content, path):

    if(not os.path.exists(path)): os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as paper:

        output = pickle.dump(content, paper)
        pass

    return(output)

def writeText(content, path):

    text = pprint.pformat(content)
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    with open(path, 'w') as paper: _ = paper.write(text) 
    return

def copyFolder(source, destination):

    exist = os.path.exists(destination)
    if(exist): shutil.rmtree(destination)
    shutil.copytree(source, destination)
    return

def saveYaml(content, path):

    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    with open(path, 'w') as paper: _ = yaml.dump(content, paper, default_flow_style=None)
    return

