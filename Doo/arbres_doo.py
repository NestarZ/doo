#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel.corsini@u-bordeaux.fr>"

"""
Petit programme pour regarder le fonctionnement de arbres
sur le jeu de Doo
"""

# changer XXXX par le nom du fichier correspondant à tp01b
from tp01b import manche, replay, Human
from arbres import Parcours, IA
from tp01a import *

def main(force=3,code=0):
    """
    par defaut : une partie 
    minmax recursif (code 0) niveau 3 (force 3)
    contre First
    """
    jA = IA(force,code, evaluation)
    jB = IA(force, code, evaluation2) # joueur par défaut
    #B = Human('B')
    print(jA,"force %d" % jA.niveau)
    score, tour, hist = manche(jA,jB)
    # replay(hist)
    print(hist)



def evaluation(self, joueur):
        """
        evalue numeriquement la situation dans lequel se trouve le joueur
        """
        if self.perdant(joueur): return -100
        if self.gagnant(joueur): return 100
        if self.pose:
            score = 0
            for i, pion in enumerate(self.board):
                if pion == NOIRS or pion == ROI:
                    score -= self._distance_from_doo(i)
            return score
        else:
            nb_blancs = self.board.count(BLANCS)
            nb_noirs = 0
            smallest_distance = float("inf")
            for i, pion in enumerate(self.board):
                if pion == NOIRS or pion == ROI:
                    nb_noirs += 1
                    smallest_distance = min(smallest_distance, self._distance_from_doo(i))
            return - (smallest_distance)**2 - nb_blancs

def evaluation2(self, joueur):
        """
        evalue numeriquement la situation dans lequel se trouve le joueur
        """
        if self.perdant(joueur): return -100
        if self.gagnant(joueur): return 100
        if self.pose:
            score = 0
            for i, pion in enumerate(self.board):
                if pion == NOIRS or pion == ROI:
                    score -= self._distance_from_doo(i)
            return score
        else:
            nb_blancs = self.board.count(BLANCS)
            nb_noirs = 0
            smallest_distance = float("inf")
            for i, pion in enumerate(self.board):
                if pion == NOIRS or pion == ROI:
                    nb_noirs += 1
                    smallest_distance = min(smallest_distance, self._distance_from_doo(i))
            return - (smallest_distance)**2 - nb_blancs - abs(nb_noirs - 1)
    

if __name__ == "__main__" :
    # force: la profondeur, code: l'algorithme
    main(force=4,code=0)

