import json
import os

class FileHandler:


    def readJson(self, fileName, folderName):
        directory = os.getcwd() + folderName
        # print(directory)
        print(" |--> {}.json".format(fileName))
        jsonFile = open(os.path.join(directory, "{}.json".format(fileName)), "r").read()
        jsonData = json.loads(jsonFile)

        return jsonData


    def writeJson(self, fileName, folderName, data):
        directory = os.getcwd() + folderName
        with open(os.path.join(directory, "{}.json".format(fileName)), "w") as jsonFile:
            jsonFile.write(json.dumps(data))
        jsonFile.close()


    def readRouteFile(self, fileName):
        route = []
        routeFile = open("{}.txt".format(fileName), "r")
        for direction in routeFile:
            route.append(direction.split())
        routeFile.close()

        return route
