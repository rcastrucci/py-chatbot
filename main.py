import json
import os.path


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


def loadIntents(INTENTS):
    listOfIntents = []
    for intents in INTENTS:
        listOfIntents.append(intents['tag'])
    return listOfIntents


def loadEntities(ENTITIES):
    listOfEntities = []
    for entities in ENTITIES:
        for ent in entities:
            listOfEntities.append(ent)
    return listOfEntities


def loadEntitiesValues(ENTITIES):
    listOfEntitiesValues = []
    for i in range(len(ENTITIES)):
        for entity in ENTITIES[i]:
            for value in ENTITIES[i][entity]:
                listOfEntitiesValues.append((entity, value['value']))
    return listOfEntitiesValues


def loadEntitiesSynonymous(ENTITIES):
    listOfEntitiesSynonymous = []
    for i in range(len(ENTITIES)):
        for entity in ENTITIES[i]:
            for value in ENTITIES[i][entity]:
                for synonymous in value['synonymous']:
                    listOfEntitiesSynonymous.append((value['value'], synonymous))
    return listOfEntitiesSynonymous


def search(arg, tuplesList):
    for i in range(len(tuplesList)):
        if arg.lower() in tuplesList[i][1].lower():
            return tuplesList[i]
    return False


intentsFile = "intents.json"
entitiesFile = "entities.json"

if checkFiles([intentsFile, entitiesFile]):
    INTENTS = openJson(intentsFile)['intents']
    ENTITIES = openJson(entitiesFile)['entities']
    intentsList = loadIntents(INTENTS)
    entitiesList = loadEntities(ENTITIES)
    entitiesValues = loadEntitiesValues(ENTITIES)
    entitiesSynonymous = loadEntitiesSynonymous(ENTITIES)

    def predict(word):
        hardValue = search(word, entitiesValues)
        synonymousValue = search(word, entitiesSynonymous)
        if hardValue:
            return hardValue
        else:
            if synonymousValue:
                return search(synonymousValue[0], entitiesValues)
            else:
                return False

    while True:
        inp = input("You: ")
        if inp == "quit":
            break
        else:                
            answer = predict(inp)
            if answer:
                print(answer)
            else:
                print("Not found")