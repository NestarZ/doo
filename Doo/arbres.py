#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel.corsini@u-bordeaux.fr>"

from tp02_abstract import Base, IAPlayer
# Remplacer XXXX par le nom du fichier correspondant au tp01b
from XXXX import VIDE, BLANCS, NOIRS, ROI, J_DEF, J_ATT

import copy

class Parcours(Base):
    """ constructeur """
    def __init__(self,unJeu):
        super(Parcours,self).__init__(unJeu)


    def _minmax(self,joueur,profondeur):
        """ minmax recursif doit renvoyer un coup,une evaluation
        self.moi permet de connaitre le joueur de reference
        si self.moi == joueur : on est sur niveau MAX
        sinon on est sur un niveau MIN

        self.jeu.configuration
        self.joue( ... )
        self.listeCoups( ... )
        self.finPartie( .... )
        self.adversaire( ... )

        sont disponibles
        """

        # On sauvegarde l'etat dans lequel on entre
        _etat_entrant = copy.deepcopy(self.jeu.configuration)

        if self.finPartie(joueur) or profondeur == 0 :
            if self.moi == joueur :
                return None,self.evaluation(joueur)
            else: # c'est pas mon point de vue
                return None,- self.evaluation(joueur)

        elif joueur == self.moi :
            print('MAX')
            # faire le traitement
        else:
            print("MIN")
            # faire le traitement

        # avant de sortir on restaure le bon etat
        self.jeu.configuration = _etat_entrant
        # renvoie le coup et son évaluation
        return None,0

    def _negamax(self,jtrait,profondeur):
        """
        version recursive du negamax :

        self.jeu.configuration
        self.joue( ... )
        self.listeCoups( ... )
        self.finPartie( .... )
        self.adversaire( ... )

        sont disponibles
        """
        raise NotImplementedError("_negamax: AFAIRE")


    def _alphabeta(self,jtrait,alpha,beta,profondeur):
        """
        self.jeu.configuration la configuration de jeu a analyser
        jtrait le joueur ayant le trait pour cet etat
        alpha le maximum des minima
        beta le minimum des maxima
        profondeur la profondeur a laquelle se trouve etat dans l'arbre

        self.moi permet de connaitre le joueur de reference
        if self.moi == jtrait : niveau MAX
        else: niveau MIN
        """
        raise NotImplementedError("_alphabeta: AFAIRE")
    
    def positionGagnante(self,jtrait):
        """
           à développer
        """
        raise NotImplementedError("positionGagnante: coup U { None } x Bool")

    def positionPerdante(self,jtrait):
        """
           à développer
        """
        raise NotImplementedError("positionPerdante: Bool")



class IA(IAPlayer):
    """ seule choixCoup est à modifier """
    def __init__(self,lvl,code=0,name=None):
        super(IA,self).__init__(lvl,code)
        if name is not None: self.nom = name

    def choixCoup(self,unJeu,joueur):
        """
            methode permettant de choisir le cp à jouer
            utilise la classe Parcours
            appelle minmax avec les bons paramètres
            renvoie le coup calculé
        """
        raise NotImplementedError("choixCoup: AFAIRE")
    
if __name__ == "__main__" :

    _lattr = ['_minmax','_minmax_iter',
              '_negamax', '_negamax_iter',
              '_alphabeta', '_alphabeta_negamax' ]
    for attr in _lattr :
        if hasattr(Parcours,attr):
            _msg = "existe"
        else:
            _msg = "n'existe pas"

        print( attr,_msg )
