#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel.corsini@u-bordeaux.fr>"

"""
Petit programme pour regarder le fonctionnement de arbres
sur le jeu de Doo
"""

# changer XXXX par le nom du fichier correspondant à tp01b
from tp01b import manche, replay, Human
from arbres import Parcours, IA
from tp01a import *
from all_pos_win_lose import create_id
import json
import itertools
import pprint



def play_manche(eval1, eval2, force=3,code=0):
    """
    par defaut : une partie
    minmax recursif (code 0) niveau 3 (force 3)
    contre First
    """
    jA = IA(force,code, eval1)
    jB = IA(force, code, eval2) # joueur par défaut
    #jA = Human()
    try:
        print(jA,"force %d code %d" % (jA.niveau, jA.code))
    except:
        pass
    score, tour, hist = manche(jA,jB)
    # replay(hist)
    return score, hist


def main():
    evaluations = [evaluation5, evaluation4]
    score_att = {evaluation: 0 for evaluation in evaluations}
    score_def = {evaluation: 0 for evaluation in evaluations}
    # replay(play_manche(evaluation1, evaluation2)[1])
    # return;
    for eval1, eval2 in itertools.permutations(evaluations, 2):  # génère toutes les combinaisons d'évaluations, sans self vs self
        score = play_manche(eval1, eval2, force=3, code=0)[0]
        if score > 0:
            score_att[eval1] += score
        else:
            score_def[eval2] += 1
    print('défense: ')
    pprint.pprint(score_def)
    print('attaque: ')
    pprint.pprint(score_att)

def dummy(self, joueur):
    if self.perdant(joueur): return -100
    if self.gagnant(joueur): return 100
    return 0


def evaluation1(self, joueur, memory):
    """
    evalue numeriquement la situation dans lequel se trouve le joueur
    """
    if self.perdant(joueur): return -100
    if self.gagnant(joueur): return 100
    if self.pose:
        score = 0
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                score -= self._distance_from_doo(i)
        return score
    else:
        nb_blancs = self.board.count(BLANCS)
        nb_noirs = 0
        smallest_distance = 3
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                nb_noirs += 1
                smallest_distance = min(smallest_distance, self._distance_from_doo(i))
        return - (smallest_distance)**2 - 3*nb_blancs

def evaluation2(self, joueur, memoire):
    """
    evalue numeriquement la situation dans lequel se trouve le joueur
    """
    if self.perdant(joueur): return -100
    if self.gagnant(joueur): return 100
    if self.pose:
        score = 0
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                score -= self._distance_from_doo(i)
        return score
    else:
        nb_blancs = self.board.count(BLANCS)
        nb_noirs = 0
        smallest_distance = 3
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                nb_noirs += 1
                smallest_distance = min(smallest_distance, self._distance_from_doo(i))
        return - (smallest_distance)**2 - nb_blancs - abs(nb_noirs - 1)

def evaluation3(self, joueur, memoire):
    """
    evalue numeriquement la situation dans lequel se trouve le joueur
    """
    if self.perdant(joueur): return -100
    if self.gagnant(joueur): return 100
    if self.pose:
        score = 0
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                score -= self._distance_from_doo(i)
        return score
    else:
        nb_blancs = self.board.count(BLANCS)
        nb_noirs = 0
        smallest_distance = 3
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                nb_noirs += 1
                smallest_distance = min(smallest_distance, self._distance_from_doo(i))
        return -3**abs(nb_blancs -1) + nb_noirs

def evaluation4(self, joueur, memory):
    board = self.configuration[0]
    pose = self.configuration[1] < 8
    id_ = create_id(self.configuration, joueur)
    if self.perdant(joueur): return -100
    if self.gagnant(joueur): return 100
    if pose:
        score = 0
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                score -= self._distance_from_doo(i)
        return score
    else:
        if id_ in memory[:-1]: # on regarde tout les configurations sauf celle sur laquelle on travaille
            return -100
        nb_blancs = board.count(BLANCS)
        nb_noirs = 0
        smallest_distance = 3
        for i, pion in enumerate(board):
            if pion == NOIRS or pion == ROI:
                nb_noirs += 1
                smallest_distance = min(smallest_distance, self._distance_from_doo(i))
        return - (smallest_distance) - abs(nb_blancs -1)**2 - 3*int(board[4] == BLANCS) - abs(nb_noirs - 1)

def evaluation5(self, joueur, memory):
    global pos_win
    board = self.configuration[0]
    id_ = create_id(self.configuration, joueur)
    pose = self.configuration[1] < 8
    if self.perdant(joueur): return -100
    if self.gagnant(joueur): return 100
    if pose:
        score = 0
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                score -= self._distance_from_doo(i)
        return score
    else:
        if id_ in memory[:-1]:
            return -100
        nb_blancs = board.count(BLANCS)
        nb_noirs = 0
        smallest_distance = 3
        for i, pion in enumerate(board):
            if pion == NOIRS or pion == ROI:
                nb_noirs += 1
                smallest_distance = min(smallest_distance, self._distance_from_doo(i))
        if nb_blancs < 3 and nb_noirs < 3:
            if id_ in pos_win:
                print("ok")
                return 100 - 3*(nb_blancs + nb_noirs)**2
        if (board[4] == BLANCS):
            return - (smallest_distance) - 3*int(board[4] == BLANCS) - nb_blancs
        return - (smallest_distance) - abs(nb_noirs - 1)


if __name__ == "__main__" :
    # force: la profondeur, code: l'algorithme
    with open('pos_win.txt', 'r') as f:
        pos_win = set(json.load(f))
    main()
