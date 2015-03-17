#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel.corsini@u-bordeaux.fr>"

from tp02_abstract import Base, IAPlayer, BIGVALUE
# Remplacer XXXX par le nom du fichier correspondant au tp01b
from tp01a import VIDE, BLANCS, NOIRS, ROI, J_DEF, J_ATT
from tp01a import Doo
import copy

i = 0

class Parcours(Base):
    """ constructeur """
    def __init__(self,unJeu):
        super(Parcours,self).__init__(unJeu)

    def _minmax(self,joueur,profondeur, evaluation):
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
                return None, evaluation(self.jeu, joueur)
            else: # c'est pas mon point de vue
                return None, -evaluation(self.jeu, joueur)

        elif self.moi == joueur :
            f = max
            rep = -BIGVALUE
        else:
            f = min
            rep = BIGVALUE

        bestcoup = None
        for conf, coup in futur_confs(self.jeu):
            self.jeu.configuration = conf
            nrep = f(rep, self._minmax(self.adversaire(joueur), profondeur-1, evaluation)[1])
            self.jeu.configuration = _etat_entrant
            if nrep != rep:
                rep = nrep
                bestcoup = coup

        # avant de sortir on restaure le bon etat
        self.jeu.configuration = _etat_entrant
        # renvoie le coup et son évaluation
        return bestcoup,rep

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
        # On sauvegarde l'etat dans lequel on entre
        _etat_entrant = copy.deepcopy(self.jeu.configuration)
        
        if self.finPartie(jtrait) or profondeur == 0 :
            return None,jtrait*self.evaluation(jtrait)

        rep = 0
        for conf, coup in futur_confs(self.jeu):
            self.jeu.configuration = conf
            rep = -max(-rep, -self._negamax(-jtrait, profondeur-1)[1])
            self.jeu.configuration = _etat_entrant
        return coup, rep
    
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
        _etat_entrant = self.jeu.configuration
        for conf, coup in futur_confs(self.jeu):
            self.jeu.configuration = standardconf(conf)
            position_perdante_adv = self.jeu.perdant(jtrait)
            if position_perdante_adv:
                self.jeu.configuration = _etat_entrant
                return coup, True
        self.jeu.configuration = _etat_entrant
        return None, False

    def positionPerdante(self,jtrait):
        """
           à développer
        """
        _etat_entrant = self.jeu.configuration
        for conf, coup in futur_confs(self.jeu):
            self.jeu.configuration = standardconf(conf)
            position_gagnante_adv = self.jeu.gagnant(jtrait)
            if not position_gagnante_adv:
                self.jeu.configuration = _etat_entrant
                return False
        self.jeu.configuration = _etat_entrant
        return True


class IA(IAPlayer):
    """ seule choixCoup est à modifier """
    def __init__(self,lvl,code=0, evaluation=None, name=None):
        super(IA,self).__init__(lvl,code, evaluation)
        if name is not None: self.nom = name

    def choixCoup(self,unJeu,joueur):
        """
            methode permettant de choisir le cp à jouer
            utilise la classe Parcours
            appelle minmax avec les bons paramètres
            renvoie le coup calculé
        """
        par = Parcours(unJeu)
        bestcoup, eval = par.minmax(joueur, self.niveau, self.code, self.evaluation)
        return bestcoup

def futur_confs(doo):
    """
    Génerateur des nouvelles configurations possibles
    """
    for coup in doo.listeCoups(doo.trait):
        conf = doo.joue(doo.trait, coup)
        yield (conf[0], conf[1]), coup

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
