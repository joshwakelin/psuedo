
from constraint import prompt
from manager import grab
from output import display, tag, skittle

from datetime import timedelta, datetime
## from datetime import datetime

import random
from random import randrange

import requests 
import json


def luhn():
  randomDigits = [random.randint(0, 9) for _ in range(16 - 1)]
  total = sum(randomDigits[::-2] + [sum(divmod(d * 2, 10)) for d in randomDigits[-2::-2]])
  checkDigit = (10 - (total % 10)) % 10
  randomDigits.append(checkDigit)
  luhnNumber = ''.join(map(str, randomDigits))

  return luhnNumber

def generateBirthday(age):
  currentYear = datetime.today().strftime('%Y')
  currentMonth, currentDay, time = datetime.today().strftime('%m'), datetime.today().strftime('%d'), datetime.today().strftime('%I:%M %p')
  birthYear = int(currentYear) - age

  start = datetime.strptime(f'1/1/{birthYear}', '%m/%d/%Y')
  end = datetime.strptime(f"{currentMonth}/{currentDay}/{birthYear}", '%m/%d/%Y')

  delta = end - start
  intDelta = (delta.days * 24 * 60 * 60)
  randomSecond = randrange(intDelta)
  birthdayTime = start + timedelta(seconds=randomSecond)
  return birthdayTime.strftime('%m/%d/%Y')

def fixCountryName(rawCountry):
  country = list(rawCountry)
  newName = ""
  

  for i in range(len(country)):
    if country[i] == " ":
      country[i + 1] = country[i + 1].upper()
    if i == 0:
      country[i] = country[i].upper()
    newName = newName + country[i]
  return newName


def generateAge(min, max):
 tempTable = [min, max]
 if -1 in tempTable:
   if min == -1 and max == -1:
    return random.randint(1, 100)
   elif min == -1:
     return random.randint(1, max)
   else:
      return random.randint(min, 100)
 else: 
   return random.randint(min, max)


def getName(gender):
  firstName = ""
  lastName = ""
  if gender == -1:
    gender = random.choice(["male", "female"])

  names = grab('names.json', gender)
  firstName = random.choice(names)
  lastName = random.choice(grab('names.json', 'last'))

  return {
    'firstName': firstName,
    'lastName': lastName,
    'gender': gender
  }


def generateLocation(country):
  if country == -1:
   country = random.choice(grab('countries.json', None))
                    
  try: 
      res = requests.get(f'https://temo-s0r.replit.app/v1/countries/random',  params = {'country': fixCountryName(country)})
      
      if res.status_code != 200:
       raise Exception("Cannot resolve.")
      else:
       return {
          'success': True,
          'country': fixCountryName(country),
          'region:': res.json()['region'],
          'city': res.json()['city'],
          'coords': [ res.json()['lat'], res.json()['long'] ] 
       }

      
    
       
  except Exception as e:
    return {
      'success': False,
      'error': 0,
      'message': e,
    }





def main():
  constraintAnswers = prompt()
  for i in range(constraintAnswers["profiles"] or 1):
    age = generateAge(constraintAnswers["ageMinimum"], constraintAnswers["ageMaximum"])
    birthdate = generateBirthday(age)
    fullName = getName(constraintAnswers["gender"])
    locationBlob = generateLocation(constraintAnswers["country"])
    coords = locationBlob['coords']

    print(skittle([
      ["[SUCCESSFULLY GENERATED]", "green"], ["Generation " + str(i+1) + "/" + str(constraintAnswers["profiles"]), "blue"] 
    ]))

    print(display("Name: ", "yellow") + fullName['firstName'] + ' ' + fullName['lastName'] ) 
    print(display("Age: ", "yellow") + str(age))
    print(display("Date of Birth: ", "yellow") + birthdate)
    print(display("Country: ", "yellow") + locationBlob['country'])
    print(display("City: ", "yellow") + locationBlob['city'])
    print(display("Google Maps Link: ", "yellow") + f"https://www.google.com/maps/place/{coords[0]},{coords[1]}")
    print(display("Luhn Number: ", "yellow") + luhn())
    print("\n")
    ##www.google.com/maps/place/43.1879889,-79.8105746
    

    
  
main()
