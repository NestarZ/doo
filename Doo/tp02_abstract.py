#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel.corsini@u-bordeaux.fr>"

"""
On definit la classe de reference pour les algos du type minmax
CE CODE NE DOIT PAS ETRE MODIFIE
"""

from abstract import Game, Player

BIGVALUE = 1e10

class Base(object):
    def __init__(self,unJeu):
        """ constructeur ne pas modifier, ni surcharger """
        self.__game = None
        self.__player = None
        self.__checkType(unJeu)

    @property
    def moi(self): return self.__player

    @property
    def jeu(self): return self.__game

    def __getattr__(self,attr):
        """ si on ne connait pas l'attribut on demande a self.jeu """
        return getattr(self.__game,attr)

    def __checkType(self,unJeu):
        """
        verifie que l'on dispose de tous les outils
        methode privee
        """
        if isinstance(unJeu,Game): self.__game = unJeu
        else: # ne derive pas de la classe game
            _lattr = ['listeCoups', 'joue', 'adversaire', 'configuration',
                      'finPartie', 'evaluation']
            for attr in _lattr:
                try:
                    assert(hasattr(unJeu,attr))
                except:
                    raise Exception("%s unknown" % attr)
            self.__game = unJeu

    def minmax(self,joueur,profondeur,code=0, evaluation=None):
        """ effectue le calcul minmax
        en fonction de code:
            - 0 : _minmax methode recursive # Obligatoire
            - 1 : _minmax_iter methode iterative
            - 2 : _negamax methode recursive # Obligatoire
            - 3 : _negamax_iter methode iterative
            - 4 : _alphabeta methode recursive # Obligatoire
            - 5 : _alphabeta_negamax méthode récursive basée sur negamax

        """
        self.__player = joueur
        if code > 5 or code <= 0 : # si on est hors de l'intervalle
            return self._minmax(joueur, profondeur, evaluation)
        if code == 1 :
            return self._minmax_iter(joueur,profondeur, evaluation)
        if code == 2 :
            return self._negamax(joueur,profondeur, evaluation)
        if code == 3 :
            return self._negamax_iter(joueur,profondeur, evaluation)
        if code == 4 :
            return self._alphabeta(joueur,-BIGVALUE,BIGVALUE,profondeur, evaluation)
        if code == 5 :
            return self._alphabeta_negamax(joueur,-BIGVALUE,
                                           BIGVALUE,profondeur, evaluation)

    def _minmax(self,*args,**kwargs):
        """
        cette methode est recursive
        renvoie le meilleur coup et son estimation
        """
        return None,0

    def _minmax_iter(self,*args,**kwargs):
        """
        methode iterative effectuant le calcul du minmax
        renvoie le meilleur coup et son estimation
        """
        return None, 0

    def _negamax(self,*args,**kwargs):
        """
        calcul du negamax de maniere recursive
        renvoie le meilleur coup et son estimation
        """
        return None, 0

    def _negamax_iter(self,*args,**kwargs):
        """
        calcul du negamax de maniere iterative
        renvoie le meilleur coup et son estimation
        """
        return None, 0

    def _alphabeta(self,*args,**kwargs):
        """
        calcul alphabeta de maniere recursive
        renvoie le meilleur coup et son estimation
        """
        return None,0

    def _alphabeta_negamax(self,*args,**kwargs):
        """
        calcul recursif de alphabeta en utilisant la convention negamax
        renvoie le meilleur coup et son estimation
        """
        return None,0
    
    def positionGagnante(self,joueur):
        """
           Une position est gagnante s'il existe un coup tel
           que la nouvelle position soit perdante pour l'adversaire

           renvoie le coup à jouer, True si la position est gagnante
           renvoie None, diagnostic en cas de finPartie
           par défaut:
           renvoie None, False si la position n'est pas gagnante
        """

        if self.finPartie(joueur): return None,self.gagnant(joueur)
        return None, False # partie à développer

    def positionPerdante(self,joueur):
        """
           Une position est perdante, si toute position pour
           l'adversaire sera une position gagnante

           renvoie diagnostic (booléen)
           par défaut:
           renvoie False
        """
        
        if self.finPartie(joueur): return self.perdant( joueur )
        return False # partie à développer
        

class IAPlayer(Player):
    """ constructeur
    lvl la profondeur de l'arbre >= 1
    code le type d'implementation de minmax
    0 : recursif
    1 : iteratif
    2 : negamax recursif
    3 : negamax iteratif
    4 : alphabeta approche minmax, récursif
    5 : alphabeta approche negamax, récursif
    """
    def __init__(self,lvl,code=0, evaluation=None):
        self.nom = "zeOrdinator"
        self.__niveau = 1 # initialisation de la profondeur de calcul
        self.__code = 0 # initialisation du type d'algo de parcours
        self.niveau = lvl
        self.code = code
        self.evaluation = evaluation
        print(evaluation)

    @property
    def niveau(self): return self.__niveau
    @niveau.setter
    def niveau(self,val):
        """ choisit la profondeur max d'exploration """
        try:
            assert(isinstance(val,int))
            self.__niveau = max(1,val)
        except:
            print( val,"ignoree")

    @property
    def code(self): return self.__code
    @code.setter
    def code(self,val):
        """
           choisit le type de parcours 0 à 5
           0 minmax ... 5 alphabeta_negamax cf tp02_base
        """
        try:
            assert(val in range(6))
            self.__code = val
        except:
            print( val,"ignoree")
    
