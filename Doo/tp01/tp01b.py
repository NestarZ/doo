#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ================== importation ====================================#
# ICI VOUS METTEZ LES IMPORTATIONS DES MODULES/METHODES NECESSAIRES #
# exple: from abstract import ... cf allumettes.py                  #
# -------------------------------------------------------------------#

# Remplacez XXX par le nom de votre fichier de la première partie du TP01
from tp01a import Doo, J_ATT, J_DEF, ROI, BLANCS
from abstract import Player
import random
# ================ Debut de votre code ==============================#


def humain2ordi(position):
    """
    position est une chaine de 2 caracteres
        - le premier est un nombre entre 1 et 4
        - le second une lettre dans ABC
        renvoie le numéro de la position (entre 0 et 11)

        pos = humain2ordi( ordi2humain( pos ) )
    """
    if not (isinstance(position, str) and len(position) == 2) \
            and not (position[0] in "1234" and position[1].upper() in "ABC"):
        raise ValueError
    lig = int(position[0])-1  # compte à partir de 0
    col = position[1].upper()  # passage en majuscule
    return lig * 3 + "ABC".index(col)


def ordi2humain(position):
    """ position est un entier entre 0 et 11
        renvoie une chaine de 2 caracteres, le premier
        est un entier entre 1 et 4, le second une lettre dans ABC

        pos = ordi2humain( humain2ordi( pos ) )
    """
    assert(position in range(12))

    i, j = 1 + (position - (position % 3)) // 3, position % 3
    return "%d%s" % (i, "ABC"[j])


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
        valid = False
        lcoups = game.listeCoups(joueur)
        if not lcoups:
            return None
        while not valid:
            pose = game.configuration[1] < 8
            if pose and joueur == J_ATT:
                coup = self._ask_pose_att()
            elif pose and joueur == J_DEF:
                coup = self._ask_pose_def()
            else:
                coup = self._ask_coup()
                if coup not in lcoups:  # Si deplacement, alors pas en list
                    coup = (coup[0], coup[1][0])
            valid = coup in lcoups
        return coup

    def _ask_pose_att(self):
        print('Vous êtes en attaque, veuillez entrer le type de pion (R, N) que'
              ' vous souhaitez poser ainsi que sa coordonnée.')
        print('Exemple:')
        print('exemple> R 3A')
        print('Pose un roi à la ligne 3 colonne A.')
        try:
            type_, coord_human = input('>>> ').split(None, 1)
            coord_ordi = humain2ordi(coord_human)
        except ValueError:
            print('Entrée invalide, veuillez recommencer')
            return None
        else:
            return type_, coord_ordi

    def _ask_pose_def(self):
        print('Vous êtes en défense, veuillez entrer les coordonnées des deux'
              ' pions que vous souhaitez poser.')
        print('Exemple:')
        print('exemple> 2A 4A')
        print('Pose un pion à la ligne 2 colonne A et un autre à la ligne 4'
              ' colonne A.')
        try:
            c1_h, c2_h = input('>>> ').split(None, 1)
            c1 = humain2ordi(c1_h)
            c2 = humain2ordi(c2_h)
        except ValueError:
            print('Entrée invalide, veuillez recommencer')
            return None
        else:
            if c1 > c2:
                c1, c2 = c2, c1
            return c1, c2

    def _ask_coup(self):
        print('Veuillez entrer le coup que vous souhaitez jouer.')
        print('Par exemple si vous souhaitez utiliser votre pion en 3C pour'
              ' manger un pion en 2C (et donc atterir en 1C')
        print('exemple> 3C 1C')
        print('Pour chainer vos coups:')
        print('exemple> 3C 1C 1A 3A')
        try:
            start_h, dest_h = input('>>> ').split(None, 1)
            dest_l = dest_h.split()
            start = humain2ordi(start_h)
            dest = [humain2ordi(c) for c in dest_l]
        except ValueError:
            print('Entrée invalide, veuillez recommencer')
            return None
        else:
            return start, dest


def manche(funA=None, funB=None):
    if funA is None:
        funA = First()
    if funB is None:
        funB = First()
    doo = Doo()
    print(doo)
    jtrait = J_ATT
    hist = []
    while not doo.finPartie(jtrait) and not cycling(hist):
        if jtrait == J_ATT:
            coup = funA(doo, jtrait)
        else:
            coup = funB(doo, jtrait)
        hist.append(coup)
        conf = doo.joue(jtrait, coup)
        doo.configuration = conf
        print(doo)
        jtrait = doo.adversaire(jtrait)
    if doo.gagnant(J_ATT):
        points = 1
        if doo.configuration[0][4] == ROI:
            points += 1
        if doo.configuration[0].count(BLANCS) == 1:
            points += 1
    else:
        points = 0
    return points, doo.configuration[1], hist


def cycling(hist):
    """
    Vérifie qu'il n'y a pas de cycle dans l'historique
    """
    if len(hist) < 3:
        return False
    couple = (hist[-1], hist[-2])
    for coup in couple:  # Si l'un des dernier coup est une prise, osef du cycle
        if isinstance(coup[1], list):  # Si c'est une prise
            return False

    i = len(hist) - 2
    run = True
    while run:
        if (hist[i], hist[i - 1]) == couple:
            return True
        i -= 1
        if i < 9 or isinstance(hist[i - 1][1], list):  # si c'est un prise
            run = False
    return False

if __name__ == "__main__":
    doo = Doo()  # Remplacer Doo par le nom de la classe de votre jeu
    a = Random()
    b = First()
    c = Humain()
    if False:  # NEVER
        print(a.name, "en attaque", a(doo, J_ATT))
        print(a.name, "en defense", a(doo, J_DEF))
        print('='*10)
        print(b.name, "en attaque", b(doo, J_ATT))
        print(b.name, "en defense", b(doo, J_DEF))
        print('='*10)
        print(c.name, "en attaque", c(doo, J_ATT))
        print(c.name, "en defense", c(doo, J_DEF))
    print(manche(Random(), Random()))
