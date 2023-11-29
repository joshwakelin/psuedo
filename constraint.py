import json

from manager import grab

def sort(promptData):

  ## profile amount manual overwrite 
  if promptData[2] == -1:
    promptData[2] = 0 
    
  return {
    'ageMinimum': promptData[0],
    'ageMaximum': promptData[1],
    'profiles': promptData[2] + 1,
    'country': promptData[3],
    'gender': promptData[4]
    
  }
  


def checkInput(input, succMsg, errMsg, validAnswers, isDigit, rangeAbove):
  
    if isDigit and not input.isnumeric():
        if input.lower() == "none":
            print(succMsg)
            return -1
        else:
            print(errMsg)
            return False
    else:
        if input.lower() == "none":
          print(succMsg)
          return -1
          
        if validAnswers and input.lower() in validAnswers:
            print(succMsg)
            return input
        elif validAnswers:
            print(errMsg)
            return False

    if rangeAbove != -1:
        if rangeAbove.isnumeric():
            if int(input) <= int(rangeAbove):
                print(succMsg)
                return int(input)
            else:
                print(errMsg)
                return False
        else:
            checkIndex = int(rangeAbove.split("]")[0].split("[")[1])
            print(checkIndex)
            if answers[checkIndex] >= int(input):
                print(errMsg)
                return False
            else:
                print(succMsg)
                return int(input)
    else:
        print(succMsg)
        return int(input)


questions = [
    "Would you like to use constraints?", 
    "Please select a minimum age you'd like to generate. Your answer must be an integer. Type 'none' if you do not want to use any.", 
    "Please select a maximum age you'd like to generate. Your answer must be an integer. Type 'none' if you do not want to use any.", 
    "How many extra profiles on top of the first profile would you like to generate? You can generate a maximum of 9 more. Type 'none' if you do not want to generate any additional profiles.", 
    "Please enter the country you'd like these profiles to be generated from. Type 'none' if you do not want to generate any profiles from a specific country.",
  "Please enter the gender for the profile. If you do not have a preferred gender to generate, type 'none'. "
]

answers = []

parameters = {
    1: ["\n Response Recorded! \n", "\n You did not enter an integer. Please retry. \n", [], True, -1], 
    2: ["\n Response Recorded! \n", "\n You did not enter an integer, or your minimum age is higher than your maximum age. Please retry. \n", [], True, "[0]"],
    3: ["\n Response Recorded! \n", "\n You did not enter an integer, or you entered a number higher than 9. Please retry. \n", [], True, "9"],
    4: ["\n Response Recorded! \n", "\n You did not enter a valid country name, please retry. \n", grab("countries.json", None), False, -1],
  5: ["\n Response Recorded! \n", "\n You did not enter a recognized gender name. Please retry. \n", ["male", "female", "non binary", "m", "f", "nb"], False, -1]
}

def prompt():
    answers.clear()
    print("retry")
    for index, question in enumerate(questions):
        inputResponse = input(question + "\n").lower()
        if index == 0:   
            if inputResponse in ["yes", "y"]:
                print("\n You have chosen to use constraints for this generation.\n")
            elif inputResponse in ["no", "n"]:
                print(" \n No constraints have been selected for this generation.\n")
                return {
                'ageMinimum': -1,
                'ageMaximum': -1,
                'profiles': 1,
                'country': -1,
                'gender': -1

              }
            else:
                print("\n The input you entered was invalid. Please retry.\n")
                prompt()
                break
        else:
            parameterTable = parameters[index]
            res = checkInput(inputResponse, parameterTable[0], parameterTable[1], parameterTable[2], parameterTable[3], parameterTable[4])
            if not res: 
                
                prompt()
                break
            else:
                answers.append(res)


            


    return sort(answers)
