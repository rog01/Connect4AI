import numpy as np

class Test:
        
    __board= np.array([
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0], 
        [0,1,-1,0,0,1,-1], 
        [0,1,1,-1,0,-1,1], 
        [0,1,-1,-1,1,1,-1], 
        [1,1,-1,-1,1,-1,1]
        ])
    lig= 2
    col= 1
    fenetre= [1,1,1,1]
    __A_LA_SUITE= 4

    def _verif_colonne(self):
        self.init_test_colonne()
        # On extrait la colonne
        lig2= self.lig+self.__A_LA_SUITE
        if lig2 > self.__board.shape[0]: lig2= self.__board.shape[0]
        colonne = self.__board[self.lig:lig2,self.col]
        if len(colonne) >= self.__A_LA_SUITE: # On ne teste la colonne que si elle comporte au moins "__A_LA_SUITE" éléments
            #print(f"colonne: {colonne}\nfenetre: {fenetre}")
            assert (colonne== self.fenetre).all() == True
        else:
            assert False

#Test.init_test_colonne()