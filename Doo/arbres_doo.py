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
from tp01a import Doo

def main(force=3,code=0):
    """
    par defaut : une partie 
    minmax recursif (code 0) niveau 3 (force 3)
    contre First
    """
    jA = IA(force,code, Doo.evaluation)
    jB = IA(force, code, Doo.evaluation) # joueur par défaut
    #B = Human('B')
    print(jA,"force %d" % jA.niveau)
    score, tour, hist = manche(jA,jB)
    replay(hist)
    

if __name__ == "__main__" :
    # force: la profondeur, code: l'algorithme
    main(force=4,code=0)
