import json

dependants = ["countries.json", "names.json"]

loadedJson = {}


def get():
   for fileName in dependants:
     with open("data/" + fileName) as dependancyJson:
       loadedJson[fileName] = json.load(dependancyJson)
  
def grab(fileName, subSection):
  if loadedJson[fileName]:
    if subSection:
      if loadedJson[fileName][subSection]:
        return loadedJson[fileName][subSection]
      else:
       return -1
    else:
      return loadedJson[fileName]
  else:
    return -1


get()

    
