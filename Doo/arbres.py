#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel.corsini@u-bordeaux.fr>"

from tp02_abstract import Base, IAPlayer, BIGVALUE
# Remplacer XXXX par le nom du fichier correspondant au tp01b
from tp01a import VIDE, BLANCS, NOIRS, ROI, J_DEF, J_ATT
from tp01a import Doo
from allumettes import allumettes
import copy

INDECIS = object()


class Parcours(Base):
    """ constructeur """
    def __init__(self,unJeu):
        super(Parcours,self).__init__(unJeu)
        self.dico_win = {}
        self.dico_lose = {}

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
        if 'hist' in dir(self.jeu):
            _etat_entrant_hist = self.jeu.hist[:]
        if self.finPartie(joueur) or profondeur == 0 :
            if self.moi == joueur:
                return None, evaluation(self.jeu, joueur)
            else:
                return None, -evaluation(self.jeu, joueur)

        bestcoup = None

        if self.moi == joueur :
            rep = -BIGVALUE
            for conf, coup in futur_confs(self.jeu):
                self.jeu.configuration = conf
                nrep = max(rep, self._minmax(self.adversaire(joueur), profondeur-1, evaluation)[1])
                self.jeu.configuration = copy.deepcopy(_etat_entrant)
                if 'hist' in dir(self.jeu):
                    _etat_entrant_hist = self.jeu.hist[:]
                if nrep > rep:
                    rep = nrep
                    bestcoup = coup
        else:
            rep = +BIGVALUE
            for conf, coup in futur_confs(self.jeu):
                self.jeu.configuration = conf
                if 'hist' in dir(self.jeu):
                    self.jeu.hist.append(coup)
                nrep = min(rep, self._minmax(self.adversaire(joueur), profondeur-1, evaluation)[1])
                self.jeu.configuration = copy.deepcopy(_etat_entrant)
                if 'hist' in dir(self.jeu):
                    self.jeu.hist = copy.deepcopy(_etat_entrant_hist)
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
            evaluation = self.jeu.evaluation.__func__
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

    def _alphabeta2(self,jtrait,alpha,beta,profondeur, evaluation=None):
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
            evaluation = self.jeu.evaluation.__func__
        _etat_entrant = copy.deepcopy(self.jeu.configuration)

        if profondeur == 0 or self.finPartie(jtrait):
            if jtrait == self.moi:
                return None, evaluation(self.jeu, jtrait)
            else:
                return None, evaluation(self.jeu, self.adversaire(jtrait))

        if jtrait == self.moi:
            rep = -BIGVALUE
            for conf, coup in futur_confs(self.jeu):
                self.jeu.configuration = conf
                rep = max(rep, self._alphabeta(self.adversaire(jtrait), alpha, beta, profondeur - 1, evaluation)[1])
                alpha = max(alpha, rep)
                self.jeu.configuration = _etat_entrant
                if alpha >= beta:
                    return coup, rep
                print(coup, rep, "jr:{}, profondeur:{}".format(jtrait, profondeur))
        else:
            rep = BIGVALUE
            for conf, coup in futur_confs(self.jeu):
                self.jeu.configuration = conf
                rep = min(rep, self._alphabeta(self.adversaire(jtrait), alpha, beta, profondeur - 1, evaluation)[1])
                beta = min(beta, rep)
                self.jeu.configuration = _etat_entrant
                if alpha >= beta:
                    return coup, rep
                print(coup, rep, "jr:{}, profondeur:{}".format(jtrait, profondeur))
        return coup, rep

    def _alphabeta(self,jtrait,alpha,beta,profondeur, evaluation=None): #Need to be changed _negamax style
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
        _etat_entrant = copy.deepcopy(self.jeu.configuration)
        print(profondeur)
        if self.finPartie(jtrait) or profondeur == 0 :
            if self.moi == jtrait:
                return None, self.evaluation(jtrait)
            else:
                return None, self.evaluation(self.adversaire(jtrait))

        else:

            if self.moi == jtrait:
                rep = -BIGVALUE
                for fils in self.listeCoups(jtrait):
                    self.jeu.configuration = copy.deepcopy(_etat_entrant)
                    self.jeu.configuration = self.joue(jtrait, fils)

                    if rep > alpha :
                        print("CUT")
                        return fils, rep
                    petit_fils, rep_temp = self._alphabeta(self.adversaire(jtrait), alpha, beta, profondeur-1)

                    if rep_temp > rep:
                        rep = rep_temp
                        best = fils
                        alpha = rep_temp
                    print(best, rep, "jr:{}, profondeur:{}".format(jtrait, profondeur))

            else:
                rep = BIGVALUE
                for fils in self.listeCoups(jtrait):
                    self.jeu.configuration = copy.deepcopy(_etat_entrant)
                    self.jeu.configuration = self.joue(jtrait, fils)

                    if rep < beta :
                        print("CUT")
                        return fils, rep

                    petit_fils, rep_temp = self._alphabeta(self.adversaire(jtrait), alpha, beta, profondeur-1)


                    if rep_temp < rep:
                        rep = rep_temp
                        best = fils
                        beta = rep_temp
                    print(best, rep, "jr:{}, profondeur:{}".format(jtrait, profondeur))

        self.jeu.configuration = copy.deepcopy(_etat_entrant)
        return best,rep

    def positionGagnante(self,jtrait):
        """
           à développer
        """
        identifiant = self.create_id(self.jeu.configuration, jtrait)
        if identifiant in self.dico_win:
            if self.dico_win[identifiant][0] == INDECIS:
                return None, True  # Opération identité du all de positionPerdante --> On ignore le cas
            return (self.dico_win[identifiant][1], self.dico_win[identifiant][0])

        self.dico_win[identifiant] = (INDECIS, None)
        if self.finPartie(jtrait):
            self.dico_win[identifiant] = (self.jeu.gagnant(jtrait), None)
            return None, self.jeu.gagnant(jtrait)

        _etat_entrant = self.jeu.configuration
        for conf, coup in futur_confs(self.jeu):
            self.jeu.configuration = conf
            position_perdante_adv = self.positionPerdante(self.adversaire(jtrait))
            if position_perdante_adv:
                self.jeu.configuration = _etat_entrant
                self.dico_win[identifiant] = (True, coup)
                return coup, True
            self.jeu.configuration = _etat_entrant
        self.dico_win[identifiant] = (False, None)
        return None, False

    def positionPerdante(self,jtrait):
        """
           à développer
        """
        identifiant = self.create_id(self.jeu.configuration, jtrait)
        if identifiant in self.dico_lose:
            if self.dico_lose[identifiant][0] == INDECIS:
                return False  # Opération identité du any de positionGagnante --> On ignore le cas
            return self.dico_lose[identifiant][0]

        if self.finPartie(jtrait):
            self.dico_lose[identifiant] = (self.jeu.perdant(jtrait), None)
            return self.jeu.perdant(jtrait)
        _etat_entrant = self.jeu.configuration
        for conf, coup in futur_confs(self.jeu):
            self.jeu.configuration = conf
            position_gagnante_adv = self.positionGagnante(self.adversaire(jtrait))[1]
            if not position_gagnante_adv:
                self.jeu.configuration = _etat_entrant
                self.dico_lose[identifiant] = (False, None)
                return False
            self.jeu.configuration = _etat_entrant

        self.dico_lose[identifiant] = (True, None)
        return True

    def create_id(self, conf, jtrait):
        if isinstance(conf[0], int):
            return ((conf[1]%2)*2-1) * conf[0]
        dico_pions = {VIDE: 1, ROI: 100, NOIRS: 10000, BLANCS: 1000000}
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
    # doo = Doo()
    # doo.configuration = [VIDE, NOIRS, VIDE,
    #                      BLANCS, BLANCS, VIDE,
    #                      NOIRS, VIDE, BLANCS,
    #                      VIDE, VIDE, VIDE], 11
    # par = Parcours(doo)
    # print('pos gagnant J_ATT')
    # print(par.positionGagnante(J_ATT))
    # doo.configuration = doo.configuration[0], 10
    # print('pos lose J_DEF')
    # print(par.positionPerdante(J_DEF))
    # print('pos win J_DEF')
    # print(par.positionGagnante(J_DEF))

    al = allumettes(700)
    par = Parcours(al)
    print("pos gagnant 0")
    print(par.positionGagnante(0))

    _lattr = ['_minmax','_minmax_iter',
              '_negamax', '_negamax_iter',
              '_alphabeta', '_alphabeta_negamax' ]
    for attr in _lattr :
        if hasattr(Parcours,attr):
            _msg = "existe"
        else:
            _msg = "n'existe pas"

        print( attr,_msg )
