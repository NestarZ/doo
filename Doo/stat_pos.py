"""
Fichier pour calculer des informations sur la pose, comme le pourcentage de poses qui mène à
une victoire des noirs (défaite des blancs)
"""

from tp01a import NOIRS, BLANCS, VIDE, Doo, J_DEF
import json
from arbres import create_id

import itertools


def generate_combination(nb_noirs, nb_blancs, dont_spawn_on_doo=True, premier_blanc_sous_doo=False):
    """
    Génère l'ensemble des combinaisons possibles d'un jeu de Doo avec `nb_nois` noirs et
    `nb_blancs` blancs.
    Si dont_spawn_on_doo est False, alors la case du Doo peut être occupée à la génération.
    """
    available = set(range(12))
    if dont_spawn_on_doo:
        available.remove(4)
    if premier_blanc_sous_doo:
        available.remove(7)
        nb_blancs -= 1

    for black_pos in itertools.combinations(available, nb_noirs):
        board = [VIDE for i in range(12)]
        if premier_blanc_sous_doo:
            board[7] = BLANCS
        for pos in black_pos:
            board[pos] = NOIRS
        available_for_white = available - set(black_pos)
        for white_pos in itertools.combinations(available_for_white, nb_blancs):
            curboard = board[:]
            for pos in white_pos:
                curboard[pos] = BLANCS
            yield curboard


with open('all_pos_win_black.json', 'r') as f:
    pos_win_black = set(json.load(f))
with open('all_pos_win_white.json', 'r') as f:
    pos_win_white = set(json.load(f))
with open('all_pos_lose_black.json', 'r') as f:
    pos_lose_black = set(json.load(f))
with open('all_pos_lose_white.json', 'r') as f:
    pos_lose_white = set(json.load(f))

nb_lose = 0
nb_win = 0
for comb in generate_combination(4, 7, True, True):
    doo = Doo()
    doo.configuration = comb, 8
    id_ = create_id(doo.configuration, J_DEF)

    if id_ in pos_lose_white:
        nb_lose += 1
    elif id_ in pos_win_white:
        nb_win += 1
    else:
        print('weird')
print('nb_lose', nb_lose)
print('nb_win', nb_win)
print('le blanc perd dans {:.2%}'.format(nb_lose / (nb_lose + nb_win)))
