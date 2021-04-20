import abc
from abc import ABC, abstractmethod
import pygame


class EntSort(ABC):
    __TYPE_ENTSORT= 0
    
    @abstractmethod
    def entre_cp(self, message):
        pass

    def sortie(self,message):
        pass

    def aff_matrice(self,matrice):
        pass

    def get_type_entsort(self):
        pass

class Console(EntSort):
    __TYPE_ENTSORT= "console"


    def entre_cp(self, colonne_disponible, message=""):
        #print(f"entre_cp: colonne_disponible: {colonne_disponible:} message: {message}")
        while True:
            cp= input(message)
            try:
                cp= int(cp)
                if cp in colonne_disponible:
                    break
                else:
                    print(f"la colonne {cp} n'est pas disponible! Colonne disponible: {colonne_disponible}!")

            except :
                print(f"{cp} doit être un entier inclu dans {colonne_disponible}!")

        return cp          

    
    def sortie(self,message):
        print(message)

    def aff_matrice(self,matrice):
        print(matrice)

    def get_type_entsort(self):
        return self.__TYPE_ENTSORT
        
class PyGame(EntSort):
    __TYPE_ENTSORT= "pygame"
    
    def __init__(self):
        #init  pygame.init ()
        self.image = pygame.image.load ("./pygame/Grille.png")
        size = self.image.get_size ()
        self.screen = pygame.display.set_mode(size)
        self.screen.blit (self.image, (0,0))
        pygame.display.flip ()

        self.pionjaune = pygame.image.load("./pygame/PionJaune.png")
        self.pionrouge = pygame.image.load("./pygame/PionRouge.png")

    def entre_cp(self, colonne_disponible, message=""):
        #print(f"entre_cp: colonne_disponible: {colonne_disponible:} message: {message}")
        if message== "joueur1":
            bandeau= pygame.image.load("./pygame/joueur1joue.png")
            self.screen.blit(bandeau, (0,0))
            # AFFICHER LE BANDEAU
        while True:
            row= 0
            for event in pygame.event.get():                
                if event.type == pygame.MOUSEBUTTONUP: 
                    # En fonction de la position du clic, on joue une certaine colonne
                    if event.pos[0]<96 : row = 1
                    if event.pos[0]>100 and event.pos[0]<192 : row = 2
                    if event.pos[0]>196 and event.pos[0]<288 : row = 3
                    if event.pos[0]>292 and event.pos[0]<384 : row = 4
                    if event.pos[0]>388 and event.pos[0]<480 : row = 5
                    if event.pos[0]>484 and event.pos[0]<576 : row = 6
                    if event.pos[0]>580 and event.pos[0]<672 : row = 7
                        
                if event.type == pygame.QUIT:
                    sys.exit(0)
                        
            if row in colonne_disponible:
                break
                
        #print(f"row: {row}. Colonne disponnible: {colonne_disponible}")
        return row

    
    def aff_matrice(self,matrice):
        print(f"aff_matrice():\n{matrice}")
        nb_ligne= matrice.shape[0]
        nb_colonne= matrice.shape[1]
        # Affichage
        self.screen.fill((0,0,0))
        self.screen.blit(self.image,(0,0))
        
        for i in range(nb_ligne):
            for j in range(nb_colonne):
                if matrice[i,j]== 1:    #### VOIR AVEC CLASSE JOUEUR
                    #print('i,j',i,j)
                    self.screen.blit(self.pionrouge,(16+97*j,16+97*i)) #### ATTENTION AVEC TAILLE MATRICE VOIR SI GRILLE POSSIBLE
                    pygame.display.flip()
                if matrice[i,j]== -1:
                    #print('i,j',i,j)
                    self.screen.blit(self.pionjaune,(16+97*j,16+97*i))
                    pygame.display.flip()
        
        pygame.display.flip()
        
        
        
    def get_type_entsort(self):
        return self.__TYPE_ENTSORT
        


