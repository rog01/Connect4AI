# Plateau
#from  import Alea
import numpy as np
import pygame
import sys
import os


import argparse

sys.path.append("./classes")
#sys.path.insert(0,"./classes") ####### A TESTER
#sys.path.append("classes") ####### A TESTER
from plateau import *
from joueur import *
from entsort import *
from game import *
from DQN import *

# Ligne de commande, utilisation de argparse
parser = argparse.ArgumentParser(description='Power 4 !')
parser = argparse.ArgumentParser()
parser.version = '1.0'
parser.add_argument('--play1','-p1', action='store', help='--play1 "Humain" or "CodeR4" or "CodeR43" or "Jedi" or nothing (=Humain)')
parser.add_argument('--play2','-p2', action='store', help='--play2 "Humain" or "CodeR4" or "CodeR43" or "Jedi" or nothing (=Humain)')

parser.add_argument('--inout','-io', action='store', help='--inout "console" or "pygame" or "tkinter" or nothing (=console)')

parser.add_argument('--board','-b', action='store', type= int, help='--board integer integer integer', nargs= 3)

parser.add_argument('--training_mode','-trm', action='store', type= int, help='--training_mode integer')
parser.add_argument('--tournement_mode','-tm', action='store', type= int,  help='--tournement_mode integer')

parser.add_argument('--modelplay1','-mp1', action='store', help='--modelplay1 path/file.h5')
parser.add_argument('--modelplay2','-mp2', action='store', help='--modelplay2 path/file.h5')

"""
python connect4.py --help
python connect4.py --mode hxh  # pour humain contre humain
python connect4.py --mode hxr  # pour humain contre robot (humain commencent)
python connect4.py --mode rxh  # pour humain contre robot (robot commence)
python connect4.py --mode rxr  # pour robot contre robot
"""
# parser.add_argument('-c', action='store_true')
# parser.add_argument('-e', action='append')
# parser.add_argument('-f', action='append_const', const=42)
# parser.add_argument('-g', action='count')
# parser.add_argument('-j', action='version')

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


if __name__ == "__main__":

    arguments = parser.parse_args()
    #print("arguement",arguments) 
    #    

 
    if arguments.play1 not in ["Humain","CodeR4","CodeR43","Jedi","Alea"]:
         arguments.play1= "Humain"
    if arguments.play2 not in ["Humain","CodeR4","CodeR43","Jedi","Alea"]:
         arguments.play2= "Humain"

    if arguments.inout not in ["console","pygame","tkinter"]:
        arguments.inout= "console"

    if arguments.board== None: arguments.board= (6,7,4) ##########################################

    if arguments.training_mode== None: arguments.training_mode= 0
    if arguments.tournement_mode== None: arguments.tournement_mode= 1

    game= Game(play1=  arguments.play1, play2= arguments.play2, inout= arguments.inout, board= (6,7,4),\
                training_mode= arguments.training_mode, tournement_mode= arguments.tournement_mode, \
                modelplay1= arguments.modelplay1, modelplay2= arguments.modelplay2)

    # game= Game(play1= "Alea", play2= "Jedi", inout= "console", board= (6,7,4), training_mode= 0, tournement_mode= 20, \
    #     modelplay1= "", modelplay2="./model42-24-7 50-CODER43 vs CODER43 17 20.h5")

    if game.training_mode(): game.apprentissage()
    if game.tournement_mode(): game.tournoi()
