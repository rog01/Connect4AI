# Plateau
import numpy as np
import pygame
import sys
import os
import time

import random
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

from collections import deque

#import unittest

sys.path.append("./classes")
#sys.path.insert(0,"./classes") ####### A TESTER
#sys.path.append("classes") ####### A TESTER
from plateau import *
from joueur import *
from entsort import *

from DQN import *

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

def joue(joueur, jeu, es, model= None):
    if joueur.get_type()== "HUMAIN":
        colonne= es.entre_cp(jeu.ColonneDispo(),  message= f"{joueur.nom} 1, colonne ?: ")
        #time.sleep(0.5)
    elif joueur.get_type()== "BOT":
        colonne= joueur.bot_joue(jeu.ColonneDispo())

    elif joueur.get_type()== "JEDI":
        colonne= joueur.jedi_joue(jeu.ColonneDispo(), jeu.get_board(), jeu, model= model)

    matrice, fin_de_jeu, recompense= jeu.place_jeton(colonne,joueur.get_couleur())
    es.aff_matrice(jeu.get_board())


    return matrice, fin_de_jeu, recompense, colonne

# Construction d'un tableau:
jeu= Plateau(largeur= 7, hauteur= 6, a_la_suite= 4)
jeu.init_board()


# Choix des joueurs
joueur1= Alea(couleur= 1)
#model= load_model("./modeles/model-conv10.h5")
#joueur2= Jedi(model, couleur= -1)
joueur2= Alea(couleur= -1)

# Choix des entrées / sorties
es= Console()
#es= py_game()

if es.get_type_entsort()== "pygame": # IMPOSER UN PLATEAU 7x6
    pass

# DQN
dqn_agent= DQN(jeu.get_board())
#print("shape du board:",jeu.get_board().shape)

entrainement= 0
if entrainement: # Mode apprentissage
    cpt_partie_nulle= 0    
    for game in range(entrainement):
        #es= console()

        cur_state = jeu.init_board()
        while True:
            
            
            if joueur1.get_type()== "JEDI":
                new_state, terminal, reward, action = joue(joueur1, jeu, es, model) #(1, game.player1)
            else:
                new_state, terminal, reward, action = joue(joueur1, jeu, es) #(1, game.player1)
            
            action= action-1 # Passage coordonnée compatible coord matrice


            print(f"debut agent: game= {game}")
            dqn_agent.remember(cur_state, action, reward, new_state, terminal)
            print(f"Fin remember, debut replay")
            dqn_agent.replay()       # internally iterates default (prediction) model
            print(f"Fin replay, debut target_train")
            dqn_agent.target_train() # iterates target model
            cur_state= new_state
            print("Fin agent")

            if terminal:
                joueur1.recompense(reward)  ##### UTILE ????? car géré par dqn_agent
                joueur2.recompense(-reward)  ##### UTILE ????? car géré par dqn_agent
                break

            if jeu.plein():
                cpt_partie_nulle+= 1
                break ## Affichage d'un message sur le plateau de jeu

            # Joueur 2 joue
            
            if joueur2.get_type()== "JEDI":
                new_state, terminal, reward, action = joue(joueur2, jeu, es, model) #(1, game.player1)
            else:
                new_state, terminal, reward, action = joue(joueur2, jeu, es) #(1, game.player1)
            action= action-1 # Passage coordonnée compatible coord matrice

            dqn_agent.remember(cur_state, action, reward, new_state, terminal)
            dqn_agent.replay()       # internally iterates default (prediction) model
            dqn_agent.target_train() # iterates target model
            cur_state= new_state
            
            if terminal:  
                joueur1.recompense(-reward)  ##### UTILE ????? car géré par dqn_agent
                joueur2.recompense(reward)  ##### UTILE ????? car géré par dqn_agent
                break

            if jeu.plein():
                cpt_partie_nulle+= 1
                break ## Affichage d'un message sur le plateau de jeu

            # train the player
    print(f"Sauvegarde de l'agent. Nombre de partie nulle: {cpt_partie_nulle}")
    dqn_agent.save_model(f"model-conv{entrainement}.h5")


else: # Mode sans DQN
    es.aff_matrice(jeu.get_board())
    while True:
        # Joueur 1 joue
        matrice, fin_de_jeu, recompense, _= joue(joueur1, jeu, es)

        if fin_de_jeu:
            joueur1.recompense(recompense)
            joueur2.recompense(-recompense)
            break

        if jeu.plein(): break ## Affichage d'un message sur le plateau de jeu

        # Joueur 2 joue
        if joueur2.get_type()== "JEDI":
            matrice, fin_de_jeu, recompense, _ = joue(joueur2, jeu, es, model= model) #(1, game.player1)
        else:
            matrice, fin_de_jeu, recompense, _ = joue(joueur2, jeu, es) #(1, game.player1)



        if fin_de_jeu:
            joueur1.recompense(-recompense)
            joueur2.recompense(recompense)
            break

        if jeu.plein(): break ## Affichage d'un message sur le plateau de jeu


print(f"Récompence joueur 1: {joueur1.get_recompense()}")
print(f"Récompence joueur 2: {joueur2.get_recompense()}")

es.aff_matrice(jeu.get_board())

input(f"Fin de partie: entrez pour quitter !")
