#!/usr/bin/python3
# -*- coding: utf-8 -*-

#================== importation ====================================#
# ICI VOUS METTEZ LES IMPORTATIONS DES MODULES/METHODES NECESSAIRES #
# exple: from abstract import ... cf allumettes.py                  #
#-------------------------------------------------------------------#

# Remplacez XXX par le nom de votre fichier de la première partie du TP01
from tp01a import *
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


class First(Player):
    def __init__(self, nickname="MazelDOOf"):
        self.name = nickname

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        assert isinstance(value, str), 'Must be string'
        self.__name = value

    def choixCoup(self, game, joueur):
        assert isinstance(game, Doo), "Must be Doo"
        assert joueur in (J_ATT, J_DEF), "Must be a player"
        lcoups = game.listeCoups(joueur)
        return None if not lcoups else lcoups[0]

class Random(Player):
    def __init__(self, nickname="McDOO-Random"):
        self.name = nickname

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        assert isinstance(value, str), 'Must be string'
        self.__name = value

    def choixCoup(self, game, joueur):
        assert isinstance(game, Doo), "Must be Doo"
        assert joueur in (J_ATT, J_DEF), "Must be a player"
        lcoups = game.listeCoups(joueur)
        return None if not lcoups else random.choice(lcoups)

class Humain(Player):
    def __init__(self, nickname="MamaDOO-Human"):
        self.name = nickname

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        assert isinstance(value, str), 'Must be string'
        self.__name = value

    def choixCoup(self, game, joueur):
        assert isinstance(game, Doo), "Must be Doo"
        assert joueur in (J_ATT, J_DEF), "Must be a player"
        lcoups = game.listeCoups(joueur)
        return None if not lcoups else input("Entrez un coup respectant la syntaxe.\n>>> ")

if __name__ == "__main__":
    doo = Doo() # Remplacer Doo par le nom de la classe de votre jeu
    a = Random()
    b = First()
    c = Humain()
    print(a.name,"en attaque",a(doo,J_ATT))
    print(a.name,"en defense",a(doo,J_DEF))
    print('='*10)
    print(b.name,"en attaque",b(doo,J_ATT))
    print(b.name,"en defense",b(doo,J_DEF))
    print('='*10)
    print(c.name,"en attaque",c(doo,J_ATT))
    print(c.name,"en defense",c(doo,J_DEF))
