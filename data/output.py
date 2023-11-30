from colorama import init as colorama_init
from colorama import Fore
from colorama import Style



colorings = {
  'yellow': Fore.YELLOW,
  'green': Fore.GREEN,
  'red': Fore.RED,
  'blue': Fore.BLUE
  
}

def tag(tag):
  print("tag placeholder")


def display(text, color):
  return f"{colorings[color]}{text}{Style.RESET_ALL}"

def skittle(array):
  skittleString = f""
  
  for i in array:
    skittleString = skittleString + colorings[i[1]] + i[0] + Style.RESET_ALL + " "

  return skittleString

def init():
  colorama_init()

init()
