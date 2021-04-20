
import numpy as np
import pygame

class Plateau:
    # Attribut de classe: private
    __compteur_plateau= 0
    __LARGEUR= 7
    __HAUTEUR= 6
    __A_LA_SUITE= 4
    
    __MINIMUM_LARGEUR= __A_LA_SUITE
    __MINIMUM_HAUTEUR= __A_LA_SUITE
    
    # JOUEUR OU PLATEAU VISU?
    _ROUGE= 2
    _NOIR= 1
    _VIDE= 0

    __board=[] # Anciennement mat
    __MAT_ID=[]
    __MAT_COL=[]
    
    __CONTINUE= 1
    __STOP= 0
    __RECOMPENSE= 0

    
    
    def __init__(self, largeur= __LARGEUR, hauteur= __HAUTEUR, a_la_suite= __A_LA_SUITE ):
        #print(largeur, hauteur, a_la_suite)
        if largeur < Plateau.__MINIMUM_LARGEUR or hauteur < Plateau.__MINIMUM_HAUTEUR or a_la_suite < 3 or \
            a_la_suite >  min(largeur, hauteur):
            msg= f"La dimension minimum de la matrice doit être de {Plateau.__MINIMUM_LARGEUR} x {Plateau.__MINIMUM_HAUTEUR}.\n"+\
                   f"D'autre par le nombre d'alignement (ici {a_la_suite}) doit être supérieur à 3 et inférieur à {min(largeur, hauteur)}"
            raise ValueError(msg)
        self.__compteur_plateau+= 1
        self.__LARGEUR= largeur
        self.__HAUTEUR= hauteur
        self.__board= np.zeros((hauteur,largeur), dtype= int)
        self.__MAT_ID= np.eye(a_la_suite,dtype= int)
        self.__MAT_COL_1= np.ones((a_la_suite,1), dtype= int)
        
    def affiche_param(self):
        print(f"Compteur: {self.__compteur_plateau}")
        print(f"Largeur: {self.__LARGEUR}")
        print(f"Hauteur: {self.__HAUTEUR}")
        print(f"Puissance: {self.__A_LA_SUITE}")
        print(f"État du plateau:\n{self.__board}")
        print(f"\nMatrice ID:\n{self.__MAT_ID}")
        print(f"\nMatrice Col_1:\n{self.__MAT_COL_1}")
        
        
    def plein(self):
        m= 1
        for i in range(self.__LARGEUR):
            m*= self.__board[0][i]
            if m== 0: return False
        return True
    
    def ColonneDispo(self):
        cd=[]
        for i in range(self.__LARGEUR):
            if self.__board[0][i]== 0: cd.append(i+1)
        return cd
    
    def place_jeton(self, col, couleur):
        fenetre= np.array(self.__A_LA_SUITE * [couleur])
        recompense= 0
        fin_de_jeu= 0
        
        # On place le jeton
        col= col- 1 # On joue à partir de la colonne 1 qui correspond à la colonne 0 du __board
        colonne= self.__board[:,col].reshape(self.__board.shape[0]) # on récupère la colonne 'col' de la matrice board
        #print("Place jeton avant np.where: colonne: ",colonne)
        a= np.where(colonne== 0) # Liste des élément à 0
        #print("Place jeton aprés np.where: a: ",a)
        if len(a[0]) == 0:
            print("\nERREUR dans place_jeton longeur matrice a nulle !!!! \n")
        lig= a[0].max() # On prend l'élément le plus profond
        self.__board[lig,col]= couleur # On place le jeton au dessus de la pile à la 1ère case "vide"
        
        # On vérifie la colonne
        gagne= self.__verif_colonne(lig, col, fenetre)
        if gagne== False: # Pas de gagnant sur la colonne, on vérifie la ligne
            gagne= self.__verif_ligne(lig, col, fenetre)
            if gagne== False: # Pas de gagnant sur la ligne, on teste les diagonales
                gagne= self.__verif_diag(lig, col, fenetre)

        if gagne:
            recompense= 1
            fin_de_jeu= 1

        
        return self.__board, fin_de_jeu, recompense
    
    def __verif_colonne(self, lig, col, fenetre):
        # On extrait la colonne
        lig2= lig+self.__A_LA_SUITE
        if lig2 > self.__board.shape[0]: lig2= self.__board.shape[0]
        colonne = self.__board[lig:lig2,col]
        if len(colonne) >= self.__A_LA_SUITE: # On ne teste la colonne que si elle comporte au moins "__A_LA_SUITE" éléments
            #print(f"colonne: {colonne}\nfenetre: {fenetre}")
            return (colonne== fenetre).all()
        return False

    def __verif_ligne(self, lig, col, fenetre):
        # On extrait la colonne
        c1= col - self.__A_LA_SUITE + 1
        if c1 < 0: c1= 0 # évite d'avoir un indice de colonne négatifs
        c2= col + self.__A_LA_SUITE
        if c2> self.__board.shape[1]: c2= self.__board.shape[1] # évite de déborder: L'indice max est la largeur du board
 
        colonne = self.__board[lig,c1:c2] # Rappel: pour la notation c1:c2 le 1er indice (c1) est inclu, le 2ème (c2) est exclu.
        conv= np.convolve(colonne, fenetre)
        # print(f"Conv: {conv}")
        if self.__A_LA_SUITE in conv:
            return True
        return False

    def __verif_diag(self,lig, col, fenetre):
        pad_board= np.pad(self.__board, (self.__A_LA_SUITE - 1, self.__A_LA_SUITE - 1),constant_values= (0, 0))

        # lig et col dans le nouveau référentiel de pad board sont décalé de "A_LA_SUITE"
        board_augmente= pad_board[lig : lig + 2 * self.__A_LA_SUITE - 1, col : col + 2 * self.__A_LA_SUITE - 1]
        diag1= np.diag(board_augmente)

        conv= np.convolve(diag1, fenetre)
        # print(f"Conv: {conv}")
        if self.__A_LA_SUITE in conv:
            return True

        board_augmente= board_augmente.T[::-1] # On récupère la diagonale opposée
        diag2= np.diag(board_augmente)
        conv= np.convolve(diag2, fenetre)
        #print(f"diag1: {diag1}\ndiag2: {diag2}")
        #print(f"Conv: {conv}")
        if self.__A_LA_SUITE in conv:
            return True

        return False



    def init_board(self):
        self.__board[:,:]= 0
        return self.__board

    """
    def matrice_cellule_dispo(self, mat):
        mat0= np.zeros((self.__HAUTEUR, self.__LARGEUR))
        col_dispo= self.ColonneDispo()
        print(f"col_dispo: {col_dispo} shape de mat0: {mat0.shape}")
        for el in col_dispo:
            print(f"el: {el}")
            a= np.where(mat[:,el-1]== 0) # Liste des élément à 0
            print(f"a: {a}")
            lig= a[0].max() # On prend l'élément le plus profond
            print(f"lig: {lig}")
            mat0[lig,el-1]= 1

        return mat0
    """

    def get_board(self):
        #board= np.copy(self.__board) 
        return np.copy(self.__board)
    
    def get_A_LA_SUITE(self):
        return self.__A_LA_SUITE
    
