#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel.corsini@u-bordeaux.fr>"

"""
Petit programme pour regarder le fonctionnement de arbres
sur le jeu des allumettes
"""

from allumettes import partie,Player,humain
from arbres import Parcours

class ia(Player):
    """ constructeur
    lvl la profondeur de l'arbre >= 1
    code le type d'implementation de minmax
    0 : recursif
    1 : iteratif
    2 : negamax recursif
    3 : negamax iteratif
    4 : alphabeta approche minmax, récursif
    5 : alphabeta approche negamax, récursif
    """
    def __init__(self,lvl,code=0, nom="zeOrdinato"):
        self.nom = nom
        self.__niveau = 1 # initialisation de la profondeur de calcul
        self.__code = 0 # initialisation du type d'algo de parcours
        self.niveau = lvl
        self.code = code

    @property
    def niveau(self): return self.__niveau
    @niveau.setter
    def niveau(self,val):
        """ choisit la profondeur max d'exploration """
        try:
            assert(isinstance(val,int))
            self.__niveau = max(1,val)
        except:
            print( val,"ignoree")

    @property
    def code(self): return self.__code
    @code.setter
    def code(self,val):
        """
           choisit le type de parcours 0 à 5
           0 minmax ... 5 alphabeta_negamax cf tp02_base
        """
        try:
            assert(val in range(6))
            self.__code = val
        except:
            print( val,"ignoree")

    def choixCoup(self,unJeu,joueur):
        """ envoie un coup calcule par minmax a la profondeur niveau """
        x = Parcours(unJeu) # prépare l'arbre de calcul
        # minmax renvoie le coup et son evaluation
        coup,valeur = x.minmax(joueur,self.niveau,self.code)
        print("je choisis",coup,"valeur",valeur)
        return coup # renvoie l'info attendue, le coup à jouer

def main(force=3,code=0):
    """
    par defaut : une partie humain contre
    minmax recursif (code 0) niveau 3 (force 3)
    """
    jA = humain("Roger")
    jB = ia(force,code, "Albert")
    print(jB,"force %d" % jB.niveau)
    print( partie(jA,jB) )

if __name__ == "__main__" :
    main(3, 4)
