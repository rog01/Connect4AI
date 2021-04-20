import sys
#sys.path.append("..")
sys.path.append("../classes")

import entsort
import abc
from abc import ABC, abstractmethod
import pygame


class TestEntSort(ABC):
    __TYPE_ENTSORT= 0
    
    #@abstractmethod
    def test_entre_cp(self):
        pass

    def test_sortie(self):
        pass

    def test_aff_matrice(self):
        pass

    def test_get_type_entsort(self):
        pass

class TestConsole(TestEntSort):
    __TYPE_ENTSORT= "console"


    def test_entre_cp(self, colonne_disponible = [0, 1, 2, 3, 4, 5, 6] , message=""):
        while True:
            #cp= input(message)
            cp = 1
            try:
                cp= int(cp)
                if cp in colonne_disponible:
                    break
                else:
                    print(f"la colonne {cp} n'est pas disponible! Colonne disponible: {colonne_disponible}!")

            except :
                print(f"{cp} doit être un entier inclu dans {colonne_disponible}!")

        assert cp == 1
                   

    
    def test_sortie(message):
        print(message)

    def test_aff_matrice(matrice):
        print(matrice)

    def test_get_type_entsort(self):
        assert self.__TYPE_ENTSORT == self.__TYPE_ENTSORT