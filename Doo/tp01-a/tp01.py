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
import time
#================ Debut de votre code ==============================#

class Doo(Game):

    def __init__(self):
        self.configuration = [VIDE if not case == 7 else BLANCS for case in range(12)], 1

    def format(self, configuration):
        _tab, _tr = configuration
        _str = "c'est le tour {}".format(_tr)
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
        return self.perdant(self.adversaire(joueur))

    def perdant(self,joueur):
        """ renvoie True si l'etat est une defaite pour le joueur """
        return (self.configuration[0] == 0)

    def finPartie(self,joueur):
        """ renvoie True si la partie est terminee """
        return self.perdant(joueur) or self.perdant(self.adversaire(joueur))

    def listeCoups(self,joueur):
        """ renvoie la liste des coups autorises pour le joueur """
        possibles_dir = {J_ATT : ['u', 'd', 'r', 'l', 'ur', 'ul', 'dl', 'dr'],
                         J_DEF : ['u', 'd', 'r', 'l']}
        _board, _tr = self.configuration
        best_chain = 0  # Plus grand nombre de pions mangeable en un coup

        if joueur == J_ATT:
            _mangeable = (BLANCS,)
            _control = (NOIRS,ROI)
            _trait = _tr%2 != 0
        else:
            _control = (BLANCS,)
            _mangeable = (NOIRS,ROI)
            _trait = _tr%2 == 0

        if not _trait:
            return tuple()

        if  _tr<8:  # Si on est en phase de pose
            r1 = lambda i: not i == 4 and (not i in (1,3,5) or _tr > 1)  # not B2 and (not(A2,B1,C2) or tour>1)
            if ROI in _board and ROI in _control:
                _control = (NOIRS, )
            if joueur == J_ATT:
                _pose = [(type_,i) for i,x in enumerate(_board) if x == VIDE and r1(i) for type_ in _control]
            else:
                _pose = [(i, j) for i in range(12) for j in range(i+1, 12) if r1(i) and r1(j) and i == VIDE and j == VIDE]
            print(_pose)
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
                liste_prises = self.prise(pion, _mangeable, possibles_dir[joueur], joueur == J_DEF)
                if liste_prises:
                    try:
                        chain = len(liste_prises[0][1])
                    except TypeError:  # Si ce n'est que l'indice de la case d'arrivée et pas un chemin
                        chain = 1
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
                            prises = [cur_path]
                        elif not prises or len(cur_path) == len(prises[0][1]):
                            prises.append((pion, cur_path))
                        new_prises = self.prise(pion, mangeable, dirs, biggest, already_eaten + [other], cur_path)
                        if new_prises and len(new_prises[0][1]) > len(prises[0][1]):
                            prises = new_prises
                    else:
                        prises.append((pion, cur_path))
        final = []
        for prise in prises:
            if len(prise[1]) == 1:
                final.append((prise[0], prise[1][0]))
            else:
                final.append(prise)
        return final


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


    def __prise_recursive(self, start, temp_pos, l, temp_cfg):
        _t, _tr = temp_cfg
        _c = [2] if len(_t)>temp_pos+2 and _t[temp_pos+1] and not _t[temp_pos+2] and (temp_pos+2)%3!=0 and (temp_pos+1)%3!=0 else []
        _c += [-2] if temp_pos-2>=0 and _t[temp_pos-1] and not _t[temp_pos-2] and temp_pos%3!=0 and (temp_pos-1)%3!=0 else []
        _c += [+6] if len(_t)>temp_pos+6 and _t[temp_pos+3] and not _t[temp_pos+6] else []
        _c += [-6] if temp_pos-6>=0 and _t[temp_pos-3] and not _t[temp_pos-6] else []
        if _c:
            _all = []
            for c in _c:
                _temp_t = _t[:]
                _temp_t[temp_pos] = VIDE
                _temp_t[temp_pos+(c//2)] = VIDE
                _temp_t[temp_pos+c] = _t[temp_pos]
                for a in self.__prise_recursive(start, temp_pos+c, l+[temp_pos+c], (_temp_t, _tr)):
                    _all.append(a) #récupere tous les différentes prises possibles
            return _all
        elif l:
            return [(start, l)]

    def joue(self,joueur,coup):
        """
        renvoie une nouvelle configuration
        apres que le joueur a effectue son coup
        """
        _oldA,_oldT = self.configuration
        return _oldA - coup, _oldT+1

    def evaluation(self,joueur):
        """
        evalue numeriquement la situation dans lequel se trouve le joueur
        """
        if self.perdant(joueur): return -10
        if self.gagnant(joueur): return 10
        return 0

class PlayerDoo(Player):
    pass
