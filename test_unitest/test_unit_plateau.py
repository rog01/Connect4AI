import unittest
import numpy as np
import pygame
import abc
from abc import ABC, abstractmethod
import pygame
import sys
import unittest
from pygame.locals import *
import os
import numpy as np

if os.environ.get('DISPLAY','') == '':
    #rint('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')



class test(unittest.TestCase):

    def test__verif_colonne(self, lig = 2, col = 4, fenetre = [-1,-1,-1,-1]):
        __A_LA_SUITE= len(fenetre)
        
        __board = np.array([
        [0,0,0,0,0,0,0,0], 
        [0,0,0,0,0,0,0,1], 
        [0,0,0,0,-1,0,-1,1],
        [0,0,0,0,-1,1,1,-1],
        [0,0,0,0,-1,-1,1,1],
        [0,0,0,0,-1,-1,1,1]])
        lig2= lig+__A_LA_SUITE
        if lig2 > __board.shape[0]: lig2= __board.shape[0]
        colonne = __board[lig:lig2,col]
        if len(colonne) >= __A_LA_SUITE: 
            assert True 
        else:
            assert False





    def test__verif_ligne(self, lig = 5, col = 3, fenetre = [1,1,1,1]):
        __A_LA_SUITE= len(fenetre)    
            
        __board = np.array([
        [0,0,0,0,0,0,0,0], 
        [0,0,0,0,0,0,0,1], 
        [0,0,0,0,0,0,-1,1],
        [0,0,0,0,-1,1,1,-1],
        [0,0,0,0,-1,-1,1,1],
        [1,1,1,1,-1,1,1,1]])
       
        c1= col - __A_LA_SUITE + 1
        if c1 < 0: c1= 0
        c2= col + __A_LA_SUITE
        if c2> __board.shape[1]: c2= __board.shape[1]
    
        colonne = __board[lig,c1:c2]
        conv= np.convolve(colonne, fenetre)
        
        if __A_LA_SUITE in conv:
            assert True
        else:
            assert False






    def test__verif_diag(self,lig =2, col = 6, fenetre=[-1,-1,-1,-1]):
        __A_LA_SUITE= len(fenetre)   
              
        __board = np.array([
        [0, 0,0,0,0,0, 0, 0], 
        [0, 0,0,0,0, 0, 0,1], 
        [0,0,0,0,0, 0, -1,1],
        [0,0,0,0,-1,-1,1,-1],
        [0,0,0,0,-1,-1, 1,1],
        [1,1,1,-1,-1, 1, 1,1]])
        
        pad_board= np.pad(__board, (__A_LA_SUITE - 1, __A_LA_SUITE - 1),constant_values= (0, 0))

        board_augmente= pad_board[lig : lig + 2 * __A_LA_SUITE - 1, col : col + 2 * __A_LA_SUITE - 1]
        diag1= np.diag(board_augmente)

        conv= np.convolve(diag1, fenetre)
       
        if __A_LA_SUITE in conv:
            assert True

        board_augmente= board_augmente.T[::-1] 
        diag2= np.diag(board_augmente)
        conv= np.convolve(diag2, fenetre)
        
        if __A_LA_SUITE in conv:
            assert True
        else:
            assert False




if __name__ == '__main__':
    unittest.main()   
   
