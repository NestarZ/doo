from arbres import Parcours, create_id
from tp01a import *

import itertools
import sys
import json


def generate_combination(nb_noirs, nb_blancs, dont_spawn_on_doo=True):
    available = set(range(12))
    if dont_spawn_on_doo:
        available.remove(4)
    for black_pos in itertools.combinations(available, nb_noirs):
        board = [VIDE for i in range(12)]
        for pos in black_pos:
            board[pos] = NOIRS
        available_for_white = available - set(black_pos)
        for white_pos in itertools.combinations(available_for_white, nb_blancs):
            curboard = board[:]
            for pos in white_pos:
                curboard[pos] = BLANCS
            yield curboard


def create_id(conf, jtrait):
    if isinstance(conf[0], int):
        return ((conf[1] % 2) * 2 - 1) * conf[0]
    dico_pions = {VIDE: 1, ROI: 100, NOIRS: 10000, BLANCS: 1000000}
    identifiant = 0
    for i, case in enumerate(conf[0]):
        identifiant ^= dico_pions[case] * (i+1)
    if jtrait == J_DEF:
        identifiant = -identifiant
    return identifiant

if __name__ == "__main__":
    doo = Doo()
    par = Parcours(doo)

    pos_too_deep = []
    for nb_noirs in range(1, 5):
        for nb_blancs in range(1, 8):
            for comb in generate_combination(nb_noirs, nb_blancs):
                try:
                    doo.configuration = comb, 11
                    par.positionGagnante(J_ATT)
                    par.positionPerdante(J_ATT)
                except RuntimeError:
                    print('Wow so deep, much computation', file=sys.stderr)
                    pos_too_deep.append((comb, 11))

    with open('all_pos_win_black.json') as f:
        json.dump(par.dico_win, f)
    with open('all_pos_lose_black.json') as f:
        json.dump(par.dico_lose, f)

    doo = Doo()
    par = Parcours(doo)

    pos_too_deep = []
    for nb_noirs in range(1, 5):
        for nb_blancs in range(1, 8):
            for comb in generate_combination(nb_noirs, nb_blancs):
                try:
                    doo.configuration = comb, 10
                    par.positionGagnante(J_DEF)
                    par.positionPerdante(J_DEF)
                except RuntimeError:
                    print('Wow so deep, much computation', file=sys.stderr)
                    pos_too_deep.append((comb, 11))
    with open('all_pos_win_white.json') as f:
        json.dump(par.dico_win, f)
    with open('all_pos_lose_white.json') as f:
        json.dump(par.dico_lose, f)
