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

    def get2d(self, t1D):
        _t2D = [[t1D[k] for k in range(i,i+3)] for i in range(0,len(t1D),3)]
        return _t2D

    def get1d(self, t2D):
        _t1D = [x[i] for i in range(3) for x in t2D]
        return _t1D
        
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
        return self.perdant(joueur)

    def listeCoups(self,joueur):
        """ renvoie la liste des coups autorises pour le joueur """
        _t1D, _tr = self.configuration
        _t2D = self.get2d(_t1D)
        
        if joueur == J_ATT:
            _mangeable = (BLANCS,)
            _control = (NOIRS,ROI)
            _trait = _tr%2 != 0
        else:
            _control = (BLANCS,)
            _mangeable = (NOIRS,ROI)
            _trait = _tr%2 == 0
            
        if _trait and _tr<8:
            r1 = lambda i: not i == 4 and (not i in (1,3,5) or _tr > 1) #notB2 and (not(A2,B1,C2) or tour>1)
            _pose = [(type,i) for i,x in enumerate(_t1D) if x in (VIDE,) and r1(i) for type in _control]
            return tuple(_pose)
        elif _trait:
            _hr = [(i,i+1) for i,x in enumerate(_t1D) if x in _control and (i+1)%3 != 0 and _t1D[i+1] in (VIDE,)]
            _hl = [(i,i-1) for i,x in enumerate(_t1D) if x in _control and i%3 != 0 and _t1D[i-1] in (VIDE,)]
            _vu = [(i,i+3) for i,x in enumerate(_t1D) if x in _control and 0<i+3<len(_t1D) and _t1D[i+3] in (VIDE,)]
            _vd = [(i,i-3) for i,x in enumerate(_t1D) if x in _control and 0<i-3<len(_t1D) and _t1D[i-3] in (VIDE,)]
            _prise = [self.__prise_recursive(i, i, [], (_t1D, _tr)) for i,x in enumerate(_t1D) if x in _mangeable]
            _unpack_prise = [x[i] for x in _prise if x for i in range(len(x))]
            if joueur == J_ATT:
                _dur = [(i,i+1) for i,x in enumerate(_t1D) if x in _control and (i+1)%3 != 0 and _t1D[i+1] in (VIDE,)]
                _dul = [(i,i-1) for i,x in enumerate(_t1D) if x in _control and i%3 != 0 and _t1D[i-1] in (VIDE,)]
                _ddl = [(i,i+3) for i,x in enumerate(_t1D) if x in _control and 0<i+3<len(_t1D) and _t1D[i+3] in (VIDE,)]
                _ddr = [(i,i-3) for i,x in enumerate(_t1D) if x in _control and 0<i-3<len(_t1D) and _t1D[i-3] in (VIDE,)]                
            return tuple(_hr+_hl+_vu+_vd+_unpack_prise)
        return tuple()

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

d = Doo()
print(d)
print(d.listeCoups(J_ATT))
print(d.listeCoups(J_DEF))
