#!/usr/bin/python3
# -*- coding: utf-8 -*-

#======== VARIABLES A INITIALISER EN FONCTION DE VOTRE CODE ========#
J_ATT = -1  # le code désignant le joueur ayant les noirs
J_DEF = 1  # le code désignant le joueur ayant les blancs
BLANCS = "B"  # le code désignant un pion blanc
NOIRS = "N"  # le code désignant un pion noir
ROI = "R"  # le code désignant le Roi
VIDE = None  # le code désignant une case vide
#===================================================================#

#================== importation ====================================#
# ICI VOUS METTEZ LES IMPORTATIONS DES MODULES/METHODES NECESSAIRES #
# exple: from abstract import ... cf allumettes.py                  #
#-------------------------------------------------------------------#
from abstract import Game
#================ Debut de votre code ==============================#

DOO = 4  # L'identitifiant de la case qui représente le Doo.


class Doo(Game):

    def __init__(self):
        self.configuration = [VIDE if not case == 7 else BLANCS for case in range(12)], 1
        self.hist = []

    @property
    def trait(self):
        if self.configuration[1] % 2 == 1:
            return J_ATT
        else:
            return J_DEF

    @property
    def pose(self):
        return self.tour < 8

    @classmethod
    def format(cls, configuration):
        _tab, _tr = configuration
        _str = "c'est au tour de {} ({})".format("J_ATT" if _tr % 2 else "J_DEF", _tr)
        _border = '{}*{}*'.format('\n', '-'*(len(_tab)//3+1))
        for i, case in enumerate(_tab):
            _str += _border + '\n|' if i % 3 == 0 else ''
            _str += '{}|'.format(case if case else ' ')
        return _str + _border

    def __str__(self):
        return self.format(self.configuration)

    @property
    def configuration(self):
        """
        renvoie la configuration courante du jeu
        """
        return self.board, self.tour

    @configuration.setter
    def configuration(self, newcfg):
        assert isinstance(newcfg, (list, tuple))
        assert len(newcfg) == 2
        assert isinstance(newcfg[0], list)
        assert isinstance(newcfg[1], int)
        self.board, self.tour = newcfg

    @classmethod
    def regles(cls):
        """ affiche les regles du jeux """
        _msg = """
        Regles du Doo (A remplir)
        """
        return _msg

    def adversaire(self, joueur):
        """ renvoie l'autre joueur """
        return -joueur

    def gagnant(self, joueur):
        """ renvoie True si l'etat est une victoire pour le joueur """
        nb_pions_noirs = self.board.count(ROI) + self.board.count(NOIRS)
        if self.pose:
            return False
        if joueur == J_ATT:
            return self.board[DOO] in (NOIRS, ROI) and nb_pions_noirs == 1
        else:
            return self.finPartie(joueur) and not self.gagnant(J_ATT)

    def perdant(self, joueur):
        """ renvoie True si l'etat est une defaite pour le joueur """
        return self.gagnant(self.adversaire(joueur))

    def finPartie(self, joueur):
        """ renvoie True si la partie est terminee """
        nb_pions_noirs = self.board.count(ROI) + self.board.count(NOIRS)
        nb_pions_blancs = self.board.count(BLANCS)
        return not self.pose and (not self._listeCoupsosef(self.trait)
                                  or self.gagnant(J_ATT)
                                  or nb_pions_noirs == 0
                                  or nb_pions_blancs == 0)

    def listeCoups(self, joueur):
        """ renvoie la liste des coups autorises pour le joueur """

        if self.trait != joueur:
            return []

        if self.gagnant(J_ATT):
            return []
        elif self.finPartie(J_DEF):
            return []

        return self._listeCoupsosef(joueur)

    def _listeCoupsosef(self, joueur):
        possibles_dir = {J_ATT: ['u', 'd', 'r', 'l', 'ur', 'ul', 'dl', 'dr'],
                         J_DEF: ['u', 'd', 'r', 'l']}
        best_chain = 0  # Plus grand nombre de pions mangeable en un coup

        if joueur == J_ATT:
            _mangeable = (BLANCS,)
            _control = (NOIRS, ROI)
        else:
            _control = (BLANCS,)
            _mangeable = (NOIRS, ROI)

        if self.pose:
            r1 = lambda i: not i == 4 and (not i in (1, 3, 5) or self.tour > 1)
            if ROI in self.board and ROI in _control:
                _control = (NOIRS, )
            elif not ROI in self.board and self.board.count(NOIRS) == 3:
                _control = (ROI, )
            if joueur == J_ATT:
                _pose = [(type_, i) for i, x in enumerate(self.board)
                         if x == VIDE and r1(i) for type_ in _control]
            else:
                _pose = [(i, j) for i in range(12) for j in range(i+1, 12)
                         if r1(i) and r1(j) and self.board[i] == VIDE and self.board[j] == VIDE]
            return _pose
        else:
            pions = [i for i, pion in enumerate(self.board) if pion in _control]
            liste_coup = []
            for pion in pions:
                if best_chain == 0:  # S'il n'y a rien à prendre (ou joueur en attaque)
                    for dest in possibles_dir[joueur]:
                        try:
                            current = self.cell(pion, dest)
                        except ValueError:
                            pass
                        else:
                            if self.board[current] == VIDE:
                                liste_coup.append((pion, current))
                liste_prises = self.prise(pion, _mangeable, possibles_dir[J_DEF], joueur == J_DEF)
                if joueur == J_ATT:
                    liste_coup.extend(liste_prises)
                elif liste_prises:  # Si le joueur est en défense et il peut prendre
                    if liste_prises:
                        chain = max(len(liste_prises[i][1]) for i in range(len(liste_prises)))
                    else:
                        chain = 0
                    if chain > best_chain:
                        liste_coup = [prise for prise in liste_prises if len(prise[1]) == chain]
                        best_chain = chain
                    elif chain == best_chain:
                        liste_coup.extend(liste_prises)
            return liste_coup

    def prise(self, pion, mangeable, dirs, biggest, already_eaten=None, path=None):
        """
        Donne la liste des prises possibles en partant de `pion` et en pouvant manger les
        `mangeable`. Si `biggest` vaut True, alors la liste des prises est récursive et
        retourne toutes les chaînes possibles.
        """
        board = self.configuration[0]
        prises = []
        if not path:
            path = []
        if not already_eaten:
            already_eaten = []
        for dest in dirs:
            if path:
                start = path[-1]
            else:
                start = pion
            try:
                other = self.cell(start, dest)
                end = self.cell(start, dest*2)
            except ValueError:
                pass
            else:
                if board[other] in mangeable and board[end] == VIDE and other not in already_eaten:
                    cur_path = path + [end]
                    prises.append((pion, cur_path))
                    if biggest:
                        prises += self.prise(pion, mangeable, dirs, biggest,
                                             already_eaten + [other], cur_path)
        return prises

    def cell(self, pos, direction):
        """
        Donne la case dans la direction demandée si possible, sinon retourne une ValueError

        exemple :
        cell(4, 'u') -> 1
        cell(10, 'd') -> ValueError
        cell(3, 'ur') -> 1
        cell(3, 'ul') -> ValueError
        """
        for char in direction:
            if char == 'u':
                if pos >= 3:
                    pos -= 3
                else:
                    raise ValueError
            if char == 'd':
                if pos <= 8:
                    pos += 3
                else:
                    raise ValueError
            if char == 'l':
                if pos % 3 != 0:
                    pos -= 1
                else:
                    raise ValueError
            if char == 'r':
                if pos % 3 != 2:
                    pos += 1
                else:
                    raise ValueError
        return pos

    def joue(self, joueur, coup):
        """
        renvoie une nouvelle configuration
        apres que le joueur a effectue son coup
        """
        _t, _tr = self.configuration
        _temp_t, _temp_tr = _t[:], _tr + 1
        if coup in self.listeCoups(joueur):
            if isinstance(coup[0], str):
                _temp_t[coup[1]] = coup[0]
            elif isinstance(coup[1], int) and self.pose:
                _temp_t[coup[0]] = BLANCS
                _temp_t[coup[1]] = BLANCS
            elif isinstance(coup[1], int):
                _temp_t[coup[0]] = VIDE
                _temp_t[coup[1]] = _t[coup[0]]
            elif isinstance(coup[1], list):
                depart, end = coup
                for i in range(len(end)):
                    distance = end[i] - depart
                    _temp_t[depart+distance] = _temp_t[depart]
                    _temp_t[depart] = VIDE
                    _temp_t[depart+(distance//2)] = VIDE
                    depart = end[i]
        else:
            raise ValueError
        return _temp_t, _temp_tr

    def evaluation(self, joueur):
        """
        evalue numeriquement la situation dans lequel se trouve le joueur
        """
        if self.perdant(joueur):
            return -100
        if self.gagnant(joueur):
            return 100
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

    def _distance_from_doo(self, i):
        """
        Retourne la distance de entre le case `i` et le Doo, quand on peut se déplacer dans
        les 8 directions possibles.
        +---+---+---+
        | 1 | 1 | 1 |
        +---+---+---+
        | 1 | 0 | 1 |
        +---+---+---+
        | 1 | 1 | 1 |
        +---+---+---+
        | 2 | 2 | 2 |
        +---+---+---+
        """
        if i == DOO:
            return 0
        if i <= 8:
            return 1
        else:
            return 2
