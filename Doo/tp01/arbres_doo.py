#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel.corsini@u-bordeaux.fr>"

"""
Petit programme pour regarder le fonctionnement de arbres
sur le jeu de Doo
"""

# changer XXXX par le nom du fichier correspondant à tp01b
from XXXX import manche, Human
from arbres import Parcours, IA

def main(force=3,code=0):
    """
    par defaut : une partie 
    minmax recursif (code 0) niveau 3 (force 3)
    contre First
    """
    jA = IA(force,code)
    jB = None # joueur par défaut
    #jB = Human('B')
    print(jA,"force %d" % jA.niveau)
    print( manche(jA,jB) )

if __name__ == "__main__" :
    # force: la profondeur, code: l'algorithme
    main(force=0,code=0)

