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


def loadIntentsPatterns(INTENTS):
    listOfIntentsPatterns = []
    for intents in INTENTS:
        for patterns in intents['patterns']:
            listOfIntentsPatterns.append((intents['tag'], patterns))
    return listOfIntentsPatterns


def loadIntentsResponses(INTENTS):
    listOfIntentsResponses = []
    for intents in INTENTS:
        for responses in intents['responses']:
            listOfIntentsResponses.append((intents['tag'], responses))
    return listOfIntentsResponses


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
    ''' INTENTS '''
    INTENTS = openJson(intentsFile)['intents']
    intentsList = loadIntents(INTENTS)
    intentsPatterns = loadIntentsPatterns(INTENTS)
    intentsResponses = loadIntentsResponses(INTENTS)
    ''' ENTITIES '''
    ENTITIES = openJson(entitiesFile)['entities']
    entitiesList = loadEntities(ENTITIES)
    entitiesValues = loadEntitiesValues(ENTITIES)
    entitiesSynonymous = loadEntitiesSynonymous(ENTITIES)
    

    class predict:
        def intent(word):
            hardValue = search(word, intentsPatterns)
            if hardValue:
                return hardValue
            else:
                return False

        def entity(word):
            hardValue = search(word, entitiesValues)
            synonymousValue = search(word, entitiesSynonymous)
            if hardValue:
                return hardValue
            else:
                if synonymousValue:
                    return search(synonymousValue[0], entitiesValues)
                else:
                    return False

    class chat:
        def read(query):
            queryEntity = predict.entity(query)
            queryIntent = predict.intent(query)
            if queryEntity or queryIntent:
                print(queryIntent, queryEntity)
            else:
                print("Not found")

    print("Welcome to our chatbot! Type 'quit' to leave the chat")
    while True:
        query = input("You: ")
        if query == "quit":
            break
        else:
            chat.read(query)