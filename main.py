from constraint import prompt
from manager import grab

from datetime import timedelta
from datetime import datetime

import random
from random import randrange

import requests 
import json




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
                          
  print(fixCountryName(country))
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
    

    print("\n \n ====== PROFILE #" + str(i+1) + " ====== \n \n ")
    print("Name: " + fullName['firstName'] + " " + fullName['lastName'])
    print("Age: " + str(age))
    print("Birthdate: " + birthdate)
    print("Gender: " + str(fullName['gender']))
    print("Country: " + locationBlob['country'])
    print("City: " + locationBlob['city'])
    print("Google Maps Link: " + f'https://www.google.com/maps/place/{coords[0]}+{coords[1]}')
    
    print("\n \n  ====== END OF PROFILE #" + str(i+1) + " ====== \n \n ")

main()
