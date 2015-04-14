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


class Human(Player):
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
            print(game)
            pose = game.configuration[1] < 8
            if pose and joueur == J_ATT:
                coup = self._ask_pose_att()
            elif pose and joueur == J_DEF:
                coup = self._ask_pose_def()
            else:
                coup = self._ask_coup()
                if coup not in lcoups and coup != None: # Si deplacement, alors pas en list
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
            print(dest_l)
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
    jtrait = J_ATT
    hist = []
    while not doo.finPartie(jtrait) and not cycling(hist):
        if jtrait == J_ATT:
            coup = funA(doo, jtrait)
        else:
            coup = funB(doo, jtrait)
        hist.append(coup)
        doo.hist = hist[:]
        conf = doo.joue(jtrait, coup)
        doo.configuration = conf
        jtrait = doo.adversaire(jtrait)
    if doo.gagnant(J_ATT):
        points = 1
        if doo.configuration[0][4] == ROI:
            points += 1
        if doo.configuration[0].count(BLANCS) == 1:
            points += 1
    else:
        points = 0
    if cycling(hist):
        print("cycling !")
        replay(hist)
        print(hist)
    #print(doo)
    return points, doo.configuration[1], hist

def is_prise(coup):
    """Détermine si le coup est une prise"""
    return isinstance(coup[1], list)

def cycling(hist):
    """
    Vérifie qu'il n'y a pas de cycle dans l'historique
    """
    if len(hist) < 3:
        return False
    couple = (hist[-1], hist[-2])
    if any(is_prise(coup) for coup in couple):
            return False

    for i in reversed(range(len(hist) - 2)):
        if is_prise(hist[i - 1]):
            return False
        if (hist[i], hist[i - 1]) == couple:
            return True
    return False

def partie(j1, j2, min_manche=1):
    """
    Affiche le nom du gagnant, son score et le nombre de manches effectuées
    Renvoie un dictionnaire dont les index sont les numéros de manche,
    les valeurs étant la liste des coups au cours de chaque manche.
    """
    # print("Début d'une partie !")
    def creation_joueur(n):
        x = None
        types = {'1':Human, '2':Random, '3':First}
        while x not in types.keys():
            x = input("J{} - Choisir un joueur : "
                      "1:Human, 2:Random, 3:First\n>".format(n))
        return types[x](input('Entrez un nom:\n>'))
    jatt = j1 if j1 else Random() # creation_joueur(1)
    jdef = j2 if j2 else Random()  # creation_joueur(2)
    points, log, m = {jatt:0, jdef:0}, {jatt:[], jdef:[]}, 1
    while not (points[jdef] >= 5 and m%2==0) or points[jatt]==points[jdef]:
        p, foo, log[m] = manche(jatt, jdef)
        points[jatt] += p
        jatt, jdef = jdef, jatt
        m += 1
    gagnant = max(points, key=points.get)
    # print('Winner: {} ({} points)'.format(gagnant.name, points[gagnant]))
    # print('Manches: {}'.format(m))
    # print("Fin de la partie !")
    return tuple(points.values()), log

def replay(hist):
    role = {J_ATT:"J_ATT", J_DEF:"J_DEF"}
    doo = Doo()
    jtrait = J_ATT
    lstr, spl = '', '{}: {} {}\n'
    lstr += ">>> Phase 1 - Pose\n"
    print(hist)
    for c in hist:
        if doo.configuration[1] == 8:
            lstr += ">>> Phase 2 - Duel\n"
            spl = '{}: {} -> {}\n'
        conf = doo.joue(jtrait, c)
        lstr += str(doo) + '\n\n'
        doo.configuration = conf
        if isinstance(c[0], str):
            lstr += spl.format(role[jtrait],
                               c[0],ordi2humain(c[1]))
        elif isinstance(c[1], list):
            cc1 = [ordi2humain(_) for _ in c[1]]
            lstr += spl.format(role[jtrait],
                               ordi2humain(c[0]), ' -> '.join(cc1))
        else:
            lstr += spl.format(role[jtrait], ordi2humain(c[0]),
                               ordi2humain(c[1]))
        jtrait = doo.adversaire(jtrait)
    is_end = doo.finPartie(jtrait)
    lstr += "Fin de manche : {}".format(is_end)
    print(lstr)
    return is_end

if __name__ == "__main__":
    doo = Doo()  # Remplacer Doo par le nom de la classe de votre jeu
    a = Random()
    b = First()
    c = Human()
    if False:  # NEVER
        print(a.name, "en attaque", a(doo, J_ATT))
        print(a.name, "en defense", a(doo, J_DEF))
        print('='*10)
        print(b.name, "en attaque", b(doo, J_ATT))
        print(b.name, "en defense", b(doo, J_DEF))
        print('='*10)
        print(c.name, "en attaque", c(doo, J_ATT))
        print(c.name, "en defense", c(doo, J_DEF))
    foo, histp = partie(None, None)
    replay(histp[1])
