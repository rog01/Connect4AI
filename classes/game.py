import sys
import numpy as np
import time

from keras.models import load_model

sys.path.append("./classes")

from joueur import *
from plateau import *
from DQN import *
from entsort import *


class Game():

    def __init__(self, play1= "Humain", play2= "Humain", inout= "Console", board= (6,7,4), training_mode= 0, tournement_mode= 1, \
                 modelplay1= None, modelplay2= None):
        self.__joueur1= self.__initjoueur(type_joueur= play1, couleur= 1, modelplay= modelplay1)
        self.__joueur2= self.__initjoueur(type_joueur= play2, couleur= -1, modelplay= modelplay2)
        self.__jeu= Plateau(hauteur= board[0], largeur= board[1], a_la_suite= board[2])
        self.__es= self.__inites(type_es= inout)
        self.__training_mode= training_mode
        self.__tournement_mode= tournement_mode
        self.__model1= modelplay1
        self.__model2= modelplay2

    def training_mode(self):
        return self.__training_mode

    def tournement_mode(self):
        return self.__tournement_mode


    def __initjoueur(self, type_joueur= "", couleur= 0, modelplay= None):
        if type_joueur== "Humain":
            joueur= Humain(couleur)
            return joueur

        if type_joueur== "Alea":
            joueur= Alea(couleur)
            return joueur

        if type_joueur== "CodeR4":
            joueur= CodeR(couleur,niveau= 4)
            return joueur

        if type_joueur== "CodeR43":
            #print("Init CodeR43")
            joueur= CodeR(couleur, niveau= 43)
            return joueur

        if type_joueur== "Jedi":
            print(f"Jedi : couleur : {couleur} matrice h5 : \n{modelplay}")
            model1= load_model(modelplay)
            
            joueur= Jedi(model= model1, couleur= couleur)

            return joueur

    def __inites(self, type_es= ""):
        #print(f"\ninites: type {type}\n")
        if type_es== "console":
            print("\nConsole\n")
            es= Console()
            return es

        elif type_es== "pygame":
            # IMPOSER UN PLATEAU 6x7
            self.__jeu= Plateau(hauteur= 6, largeur= 7, a_la_suite= 4)
            es= PyGame()
            return es

    def __joue(self, joueur, jeu, es, model= None):
        #print(f"dans joue: {joueur.get_couleur()} - {joueur.get_type()} - {es.get_type_entsort()}")
        if joueur.get_type()== "HUMAIN":
            colonne= es.entre_cp(jeu.ColonneDispo(),  message= f"{joueur.nom()} 1, colonne ?: ")
            #time.sleep(0.5)
        elif joueur.get_type()== "BOT":
            colonne= joueur.bot_joue(jeu.ColonneDispo())

        elif joueur.get_type()== "JEDI":
            print(f"Méthode __joue model= {model}")
            colonne= joueur.jedi_joue(jeu.ColonneDispo(), jeu.get_board(), jeu, model= joueur.get_model())

        elif joueur.get_type()== "CODER":
            colonne= joueur.attaque_defense(jeu.ColonneDispo(), jeu.get_board(), jeu.get_A_LA_SUITE())

        matrice, fin_de_jeu, recompense= jeu.place_jeton(colonne,joueur.get_couleur())
        es.aff_matrice(jeu.get_board())


        return matrice, fin_de_jeu, recompense, colonne

    def apprentissage(self): # Mode apprentissage
        cpt_partie_nulle= 0  
        j1= 0
        j2= 0
        # DQN
        dqn_agent= DQN(self.__jeu.get_board())
        #print("shape du board:",jeu.get_board().shape)
    
        for game in range(self.__training_mode):
            #es= console()

            cur_state = self.__jeu.init_board()
            while True: 

                if self.__joueur1.get_type()== "JEDI":
                    new_state, terminal, reward, action = self.__joue(self.__joueur1, self.__jeu, self.__es, model= self.__joueur1.get_model()) #(1, game.player1)
                else:
                    print("jeu !")
                    new_state, terminal, reward, action = self.__joue(self.__joueur1, self.__jeu, self.__es) #(1, game.player1)
                    print("fin de jeu")

                action= action-1 # Passage coordonnée compatible coord matrice


                print(f"debut agent: game= {game}")
                dqn_agent.remember(cur_state, action, reward, new_state, terminal)
                print(f"Fin remember, debut replay")
                dqn_agent.replay()       # internally iterates default (prediction) model
                print(f"Fin replay, debut target_train")
                dqn_agent.target_train() # iterates target model
                cur_state= new_state
                print("Fin agent joueur1")

                if terminal:
                    self.__joueur1.recompense(reward)  ##### UTILE ????? car géré par dqn_agent
                    j1+=1
                    self.__joueur2.recompense(-reward)  ##### UTILE ????? car géré par dqn_agent
                    break

                print("Joueur 1 jeu plein ?")
                if self.__jeu.plein():
                    cpt_partie_nulle+= 1
                    break ## Affichage d'un message sur le plateau de jeu

            # Joueur 2 joue
                if self.__joueur2.get_type()== "JEDI":
                    new_state, terminal, reward, action = self.__joue(self.__joueur2, self.__jeu, self.__es, model= self.__joueur2.get_model()) #(1, game.player1)
                else:
                    new_state, terminal, reward, action = self.__joue(self.__joueur2, self.__jeu, self.__es) #(1, game.player1)
                action= action-1 # Passage coordonnée compatible coord matrice

                dqn_agent.remember(cur_state, action, reward, new_state, terminal)
                dqn_agent.replay()       # internally iterates default (prediction) model
                dqn_agent.target_train() # iterates target model
                cur_state= new_state
                
                if terminal:  
                    j2+= 1
                    self.__joueur1.recompense(-reward)  ##### UTILE ????? car géré par dqn_agent
                    self.__joueur2.recompense(reward)  ##### UTILE ????? car géré par dqn_agent
                    break

                print("Joueur 2 jeu plein ?")
                if self.__jeu.plein():
                    cpt_partie_nulle+= 1
                    break ## Affichage d'un message sur le plateau de jeu
                print("Joueur 2. Fin jeu plein ?")

                # train the player
        print(f"Sauvegarde de l'agent. Nombre de partie nulle: {cpt_partie_nulle}")
        dqn_agent.save_model(f"model-20-100-100-1 {self.__training_mode}-{self.__joueur1.get_type()}43 "+\
            f"vs {self.__joueur2.get_type()}43 {j1} {j2} {cpt_partie_nulle}.h5")
        



    def tournoi(self):
        cpt_partie_nulle= 0  
        j1= 0
        j2= 0

        print(f"methode tournoi, tournement= {type(int(self.__tournement_mode))}")
 
        for game in range(self.__tournement_mode):

            matrice = self.__jeu.init_board()

            self.__es.aff_matrice(self.__jeu.get_board())
            while True:
                # Joueur 1 joue
                if self.__joueur1.get_type()== "JEDI":
                    matrice, fin_de_jeu, recompense, _= self.__joue(self.__joueur1, self.__jeu, self.__es, model= self.__joueur1.get_model()) #(1, game.player1)
                else:
                    matrice, fin_de_jeu, recompense, _= self.__joue(self.__joueur1, self.__jeu, self.__es) #(1, game.player1)

                if fin_de_jeu:
                    self.__joueur1.recompense(recompense)
                    self.__joueur2.recompense(-recompense)
                    j1+=1
                    break

                if self.__jeu.plein():
                    print(f"Jeu plein joueur {self.__joueur1} vient de jouer")
                    cpt_partie_nulle+= 1
                    break ## Affichage d'un message sur le plateau de jeu: A FAIRE

                # Joueur 2 joue
                if self.__joueur2.get_type()== "JEDI":
                    matrice, fin_de_jeu, recompense, _= self.__joue(self.__joueur2, self.__jeu, self.__es, model= self.__joueur2.get_model()) #(1, game.player1)
                else:
                    matrice, fin_de_jeu, recompense, _= self.__joue(self.__joueur2, self.__jeu, self.__es) #(1, game.player1)

                if fin_de_jeu:
                    self.__joueur1.recompense(-recompense)
                    self.__joueur2.recompense(recompense)
                    j2+= 1
                    break

                if self.__jeu.plein():
                    print(f"Jeu plein joueur {self.__joueur2} vient de jouer")
                    cpt_partie_nulle+= 1
                    break ## Affichage d'un message sur le plateau de jeu


            print(f"Récompence joueur 1: {self.__joueur1.get_recompense()}. Nb victoire: {j1}")
            print(f"Récompence joueur 2: {self.__joueur2.get_recompense()}. Nb victoire: {j2}")
            print(f"Nombre de parties nulle: {cpt_partie_nulle}")
            
            time.sleep(1) # 1seconde entre partie du tournoi pour lecture des infos

            self.__es.aff_matrice(self.__jeu.get_board())

        input(f"Fin de tournoi: entrez pour quitter !")
