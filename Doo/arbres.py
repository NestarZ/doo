#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel.corsini@u-bordeaux.fr>"

from tp02_abstract import Base, IAPlayer, BIGVALUE
# Remplacer XXXX par le nom du fichier correspondant au tp01b
from tp01a import VIDE, BLANCS, NOIRS, ROI, J_DEF, J_ATT
from tp01a import Doo
import copy

INDECIS = 0
POS_WIN = 1
POS_LOSE = 2
POS_OSEF = 3

i = 0

class Parcours(Base):
    """ constructeur """
    def __init__(self,unJeu):
        super(Parcours,self).__init__(unJeu)
        self.dico_try_hard = {}

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
        if not evaluation:
            evaluation = self.jeu.evaluation.__func__
        _etat_entrant = copy.deepcopy(self.jeu.configuration)
        if self.finPartie(joueur) or profondeur == 0 :
            if self.moi == joueur:
                return None, evaluation(self.jeu, self.moi)
            else:
                return None, -evaluation(self.jeu, self.moi)

        bestcoup = None

        if self.moi == joueur :
            rep = -BIGVALUE
            for conf, coup in futur_confs(self.jeu):
                self.jeu.configuration = conf
                nrep = max(rep, self._minmax(self.adversaire(joueur), profondeur-1, evaluation)[1])
                self.jeu.configuration = _etat_entrant
                if nrep > rep:
                    rep = nrep
                    bestcoup = coup
        else:
            rep = +BIGVALUE
            for conf, coup in futur_confs(self.jeu):
                self.jeu.configuration = conf
                nrep = min(rep, self._minmax(self.adversaire(joueur), profondeur-1, evaluation)[1])
                self.jeu.configuration = _etat_entrant
                if nrep < rep:
                    rep = nrep
                    bestcoup = coup

        # avant de sortir on restaure le bon etat
        self.jeu.configuration = _etat_entrant
        # renvoie le coup et son évaluation
        return bestcoup,rep

    def _negamax(self,jtrait,profondeur, evaluation=None):
        """
        version recursive du negamax :

        self.jeu.configuration
        self.joue( ... )
        self.listeCoups( ... )
        self.finPartie( .... )
        self.adversaire( ... )

        sont disponibles
        """
        if not evaluation:
            evaluation = Doo.evaluation
        # On sauvegarde l'etat dans lequel on entre
        _etat_entrant = copy.deepcopy(self.jeu.configuration)
        
        if self.finPartie(jtrait) or profondeur == 0 :
            if jtrait == J_ATT:
                signe = 1
            else:
                signe = -1
            return None, signe*evaluation(self.jeu, jtrait)

        rep = -BIGVALUE
        for conf, coup in futur_confs(self.jeu):
            self.jeu.configuration = conf
            rep = max(rep, -self._negamax(self.adversaire(jtrait), profondeur-1)[1])
            self.jeu.configuration = _etat_entrant
        return coup, rep
    
    def _alphabeta(self,jtrait,alpha,beta,profondeur, evaluation=None):
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
        if not evaluation:
            evaluation = Doo.evaluation
        _etat_entrant = copy.deepcopy(self.jeu.configuration)

        if profondeur == 0 or self.finPartie(jtrait):
            if jtrait == J_ATT:
                signe = 1
            else:
                signe = -1
            return None, signe*evaluation(self.jeu, jtrait)

        best = -BIGVALUE
        for conf, coup in futur_confs(self.jeu):
            self.jeu.configuration = conf
            rep = max(best, -self._alphabeta(self.adversaire(jtrait), -beta, -alpha, profondeur - 1, evaluation)[1]) 
            self.jeu.configuration = _etat_entrant
            if alpha >= beta:
                break
        return coup, best

    def positionGagnante(self,jtrait):
        """
           à développer
        """
        identifiant = self.create_id(self.jeu.configuration, jtrait)
        if identifiant in self.dico_try_hard:
            if self.dico_try_hard[identifiant][0] == INDECIS:
                return None, True  # Opération identité du all de positionPerdante --> On ignore le cas
            return (self.dico_try_hard[identifiant][0] == POS_WIN, self.dico_try_hard[identifiant][1])

        self.dico_try_hard[identifiant] = (INDECIS, None)
        if self.finPartie(jtrait):
            self.dico_try_hard[identifiant] = (POS_WIN, None) if self.jeu.gagnant(jtrait) else (POS_LOSE, None)
            return None, self.jeu.gagnant(jtrait)

        _etat_entrant = self.jeu.configuration
        for conf, coup in futur_confs(self.jeu):
            self.jeu.configuration = conf
            position_perdante_adv = self.positionPerdante(self.adversaire(jtrait))
            if position_perdante_adv:
                self.jeu.configuration = _etat_entrant
                self.dico_try_hard[identifiant] = (POS_WIN, coup)
                return coup, True
            self.jeu.configuration = _etat_entrant
        self.dico_try_hard[identifiant] = (POS_OSEF, None)
        return None, False

    def positionPerdante(self,jtrait):
        """
           à développer
        """
        identifiant = self.create_id(self.jeu.configuration, jtrait)
        if identifiant in self.dico_try_hard:
            if self.dico_try_hard[identifiant][0] == INDECIS:
                return False  # Opération identité du any de positionGagnante --> On ignore le cas
            return self.dico_try_hard[identifiant][0] == POS_LOSE

        if self.finPartie(jtrait):
            self.dico_try_hard[identifiant] = (POS_LOSE, None) if self.jeu.perdant(jtrait) else (POS_WIN, None)
            return self.jeu.perdant(jtrait)
        _etat_entrant = self.jeu.configuration
        for conf, coup in futur_confs(self.jeu):
            self.jeu.configuration = conf
            position_gagnante_adv = self.positionGagnante(self.adversaire(jtrait))[1]
            if not position_gagnante_adv:
                self.jeu.configuration = _etat_entrant
                self.dico_try_hard[identifiant] = (POS_OSEF, None)
                return False
            self.jeu.configuration = _etat_entrant

        self.dico_try_hard[identifiant] = (POS_LOSE, None)
        return True

    def create_id(self, conf, jtrait):
        dico_pions = {VIDE: 13, ROI: 17, NOIRS: 19, BLANCS: 23}
        identifiant = 0
        for i, case in enumerate(conf[0]):
            identifiant ^= dico_pions[case] * (i+1)
        if jtrait == J_ATT:
            identifiant ^= 898  # max id = 276 pour les cases
        return identifiant

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
    trait = J_ATT if doo.configuration[1]%2 == 1 else J_DEF
    for coup in doo.listeCoups(trait):
        conf = doo.joue(trait, coup)
        yield (conf[0], conf[1]), coup

if __name__ == "__main__" :

    doo = Doo()
    doo.configuration = [BLANCS, NOIRS, VIDE,
                         NOIRS, VIDE, BLANCS,
                         VIDE, BLANCS, VIDE,
                         NOIRS, BLANCS, VIDE], 11
    par = Parcours(doo)
    print(par.positionGagnante(J_ATT))
    doo.configuration = doo.configuration[0], 10
    print(par.positionPerdante(J_DEF))


    _lattr = ['_minmax','_minmax_iter',
              '_negamax', '_negamax_iter',
              '_alphabeta', '_alphabeta_negamax' ]
    for attr in _lattr :
        if hasattr(Parcours,attr):
            _msg = "existe"
        else:
            _msg = "n'existe pas"

        print( attr,_msg )
