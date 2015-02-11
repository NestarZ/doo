#!/usr/bin/python3
# -*- coding: utf-8 -*-

#================== importation ====================================#
# ICI VOUS METTEZ LES IMPORTATIONS DES MODULES/METHODES NECESSAIRES #
# exple: from abstract import ... cf allumettes.py                  #
#-------------------------------------------------------------------#

# Remplacez XXX par le nom de votre fichier de la première partie du TP01
from XXX import *
from abstract import Player, manche, partie
import random
#================ Debut de votre code ==============================#

def humain2ordi(position):
    """ position est une chaine de 2 caracteres
        - le premier est un nombre entre 1 et 4
        - le second une lettre dans ABC
        renvoie le numéro de la position (entre 0 et 11)

        pos = humain2ordi( ordi2humain( pos ) )
    """
    assert(isinstance(position,str) and len(position) == 2)
    assert(position[0] in "1234" and position[1].upper() in "ABC")
           
    lig = int(position[0])-1 # compte à partir de 0
    col = position[1].upper() # passage en majuscule
    return lig*3+"ABC".index(col)

def ordi2humain(position):
    """ position est un entier entre 0 et 11
        renvoie une chaine de 2 caracteres, le premier
        est un entier entre 1 et 4, le second une lettre dans ABC

        pos = ordi2humain( humain2ordi( pos ) )
    """
    assert( position in range(12) )
    
    i,j = 1+(position-(position%3))//3,position%3
    return "%d%s" % (i,"ABC"[j])


