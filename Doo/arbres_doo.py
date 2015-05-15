#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel.corsini@u-bordeaux.fr>"

"""
Petit programme pour regarder le fonctionnement de arbres
sur le jeu de Doo
"""

from tp01b import manche, Human
from arbres import IA
from tp01a import *
from evaluations import dummy, evaluation1, evaluation2, evaluation3, evaluation4, evaluation5, evaluation6

import itertools
import pprint
import time


def play_manche(eval1, eval2, force=3, code=0):
    """
    Fait jouer une manche entre deux IA avec la force `force` et l'algorithme associé à `code`.
    """
    jA = IA(force, code, eval1)
    jB = IA(force, code, eval2)
    #jA = Human()
    try:
        print(jA.nom, "force %d code %d with %s" % (jA.niveau, jA.code, jA.evaluation.__name__))
    except:
        pass
    try:
        print(jB.nom, "force %d code %d with %s" % (jB.niveau, jB.code, jB.evaluation.__name__))
    except:
        pass
    score, tour, hist = manche(jA, jB)
    return score, hist


def main():
    """
    organise un tounoi entre toutes les IA dans la liste `evaluations`.
    """
    start = time.time()
    evaluations = [evaluation5, evaluation6, evaluation4, evaluation3, evaluation2, evaluation1,
                   dummy]
    score_att = {evaluation: 0 for evaluation in evaluations}
    score_def = {evaluation: 0 for evaluation in evaluations}
    # fait s'affronter toutes les évalutations, sans self vs self
    for eval1, eval2 in itertools.permutations(evaluations, 2):
        score = play_manche(eval1, eval2, force=3, code=0)[0]
        if score > 0:
            score_att[eval1] += score
        else:
            score_def[eval2] += 1
    print('défense: ')
    pprint.pprint(score_def)
    print('attaque: ')
    pprint.pprint(score_att)
    print(time.time() - start)


if __name__ == "__main__":
    # force: la profondeur, code: l'algorithme
    main()
