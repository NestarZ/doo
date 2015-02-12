#!/usr/bin/python3
# -*- coding: utf-8 -*-

#======== VARIABLES A INITIALISER EN FONCTION DE VOTRE CODE ========#
J_ATT = -1 # le code désignant le joueur ayant les noirs
J_DEF = 1 # le code désignant le joueur ayant les blancs
BLANCS = "B" # le code désignant un pion blanc
NOIRS = "N" # le code désignant un pion noir
ROI = "R" # le code désignant le Roi
VIDE = None # le code désignant une case vide
#===================================================================#

#================== importation ====================================#
# ICI VOUS METTEZ LES IMPORTATIONS DES MODULES/METHODES NECESSAIRES #
# exple: from abstract import ... cf allumettes.py                  #
#-------------------------------------------------------------------#
from abstract import Game, Player
#================ Debut de votre code ==============================#

DOO = 4

class Doo(Game):

    def __init__(self):
        self.configuration = [VIDE if not case == 7 else BLANCS for case in range(12)], 1

    def format(self, configuration):
        _tab, _tr = configuration
        _str = "c'est au tour de {} ({})".format("J_ATT" if _tr%2 else "J_DEF", _tr)
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
        return self.__etat

    @configuration.setter
    def configuration(self, newcfg):
        assert isinstance(newcfg,(list,tuple))
        assert len(newcfg) == 2
        assert isinstance(newcfg[0],list)
        assert isinstance(newcfg[1],int)
        self.__etat = newcfg

    @classmethod
    def regles(cls):
        """ affiche les regles du jeux """
        _msg = """
        Regles du Doo (A remplir)
        """
        return _msg

    def adversaire(self,joueur):
        """ renvoie l'autre joueur """
        return -joueur

    def gagnant(self,joueur):
        """ renvoie True si l'etat est une victoire pour le joueur """
        board, tour = self.configuration
        j_def_trait = tour % 2 == 0
        nb_pions = board.count(ROI) + board.count(NOIRS)
        if tour < 8:
            return False
        if joueur == J_ATT:
            return board[DOO] in (NOIRS, ROI) and nb_pions == 1
        else:
            if j_def_trait:
                joueur_qui_a_le_trait = J_DEF
            else:
                joueur_qui_a_le_trait = J_ATT
            return not self._listeCoupsosef(joueur_qui_a_le_trait) and not self.gagnant(J_ATT) or nb_pions == 0

    def perdant(self,joueur):
        """ renvoie True si l'etat est une defaite pour le joueur """
        return self.gagnant(self.adversaire(joueur))

    def finPartie(self,joueur):
        """ renvoie True si la partie est terminee """
        return self.gagnant(joueur) or self.gagnant(self.adversaire(joueur))

    def listeCoups(self,joueur):
        """ renvoie la liste des coups autorises pour le joueur """
        _board, _tr = self.configuration

        if joueur == J_ATT:
            _trait = _tr % 2 != 0
        else:
            _trait = _tr % 2 == 0
            
        if not _trait:
            return []
        
        if self.gagnant(J_ATT):
            return []
        elif self.finPartie(J_DEF):
            return []

        return self._listeCoupsosef(joueur)


    def _listeCoupsosef(self, joueur):
        possibles_dir = {J_ATT : ['u', 'd', 'r', 'l', 'ur', 'ul', 'dl', 'dr'],
                         J_DEF : ['u', 'd', 'r', 'l']}
        _board, _tr = self.configuration
        best_chain = 0  # Plus grand nombre de pions mangeable en un coup

        if joueur == J_ATT:
            _mangeable = (BLANCS,)
            _control = (NOIRS,ROI)
        else:
            _control = (BLANCS,)
            _mangeable = (NOIRS,ROI)

        if  _tr<8:  # Si on est en phase de pose
            r1 = lambda i: not i == 4 and (not i in (1,3,5) or _tr > 1)  # not B2 and (not(A2,B1,C2) or tour>1)
            if ROI in _board and ROI in _control:
                _control = (NOIRS, )
            if joueur == J_ATT:
                _pose = [(type_,i) for i,x in enumerate(_board) if x == VIDE and r1(i) for type_ in _control]
            else:
                _pose = [(i, j) for i in range(12) for j in range(i+1, 12) if r1(i) and r1(j) and _board[i] == VIDE and _board[j] == VIDE]
            return _pose
        else:
            pions = [i for i, pion in enumerate(_board) if pion in _control]
            liste_coup = []
            for pion in pions:
                if best_chain == 0:  # S'il n'y a rien à prendre (ou joueur en attaque)
                    for dest in possibles_dir[joueur]:
                        try:
                            current = self.cell(pion, dest)
                        except ValueError:
                            pass
                        else:
                            if _board[current] == VIDE:
                                liste_coup.append((pion, current))
                liste_prises = self.prise(pion, _mangeable, possibles_dir[J_DEF], joueur == J_DEF)
                if liste_prises:
                        chain = len(liste_prises[0][1])
                else:
                    chain = 0
                if joueur == J_ATT:
                    liste_coup.extend(liste_prises)
                elif liste_prises:  # Si le joueur est en défense et il peut prendre
                    if chain > best_chain:
                        liste_coup = liste_prises
                        best_chain = chain
                    elif chain == best_chain:
                        liste_coup.extend(liste_prises)
            return liste_coup

    def prise(self, pion, mangeable, dirs, biggest, already_eaten=None, path=None):
        """
        Donne la liste des prises possibles en partant de `pion` et en pouvant manger les `mangeable`
        Si `biggest` vaut True, alors la liste des prises est récursive et retourne les plus longues
        chaînes possibles.
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
                    if biggest:
                        if prises and len(cur_path) > len(prises[0][1]):
                            prises = [(pion, cur_path)]
                        elif not prises or len(cur_path) == len(prises[0][1]):
                            prises.append((pion, cur_path))
                        new_prises = self.prise(pion, mangeable, dirs, biggest, already_eaten + [other], cur_path)
                        if new_prises and len(new_prises[0][1]) > len(prises[0][1]):
                            prises = new_prises
                        elif new_prises and len(new_prises[0][1]) == len(prises[0][1]):
                            prises += new_prises
                    else:
                        prises.append((pion, cur_path))
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
    
    def joue(self,joueur,coup):
        """
        renvoie une nouvelle configuration
        apres que le joueur a effectue son coup
        """
        _t, _tr = self.configuration
        _temp_t, _temp_tr = _t[:], _tr + 1
        if coup in self.listeCoups(joueur):
            if isinstance(coup[0], str):
                _temp_t[coup[1]] = coup[0]
            elif isinstance(coup[1], int) and _tr < 8:
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
            return _temp_t, _temp_tr
        
    def evaluation(self,joueur):
        """
        evalue numeriquement la situation dans lequel se trouve le joueur
        """
        if self.perdant(joueur): return -10
        if self.gagnant(joueur): return 10
        return 0

class PlayerDoo(Player):
    pass
