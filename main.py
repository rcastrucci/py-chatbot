from html import entities
import random
import json
import os.path

intentsFile = "intents.json"
entitiesFile = "entities.json"


def isJsonFile(filename):
    with open(filename, "r") as file:
        try:
            json.load(file)
            return True
        except ValueError:
            return False

 
def checkFiles(listOfFiles):
    for file in listOfFiles:
        if os.path.exists(file):
            if isJsonFile(file):
                continue
            else:
                print("Resource files are not in json format ({})".format(file))
                return False
        else:
            print("Resource file not found ({})".format(file))
            return False
    return True


def openJson(filename):
    with open(filename) as file:
        return json.load(file)


def loadIntents(filename):
    listOfIntents = []
    for intents in openJson(filename)['intents']:
        listOfIntents.append(intents['tag'])
    return listOfIntents


def loadEntities(filename):
    listOfEntities = []
    for entities in openJson(filename)['entities']:
        for ent in entities:
            listOfEntities.append(ent)
    return listOfEntities


if checkFiles([intentsFile, entitiesFile]):
    print(loadIntents(intentsFile))
    print(loadEntities(entitiesFile))