from arbres import Parcours, create_id
from tp01a import *

import itertools
import sys
import json
import multiprocessing


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


def compute(joueur, type_):
    doo = Doo()
    par = Parcours(doo)
    pos_too_deep = []
    for nb_noirs in range(1, 5):
        for nb_blancs in range(1, 9):
            for comb in generate_combination(nb_noirs, nb_blancs, False):
                try:
                    if joueur == J_ATT:
                        doo.configuration = comb, 11
                    else:
                        doo.configuration = comb, 10
                    if type_ == "win":
                        par.positionGagnante(joueur)
                    else:
                        par.positionPerdante(joueur)
                except RuntimeError:
                    print('Wow so deep, much computation', file=sys.stderr)
                    pos_too_deep.append((comb, 11))

    if joueur == J_ATT:
        joueur_str = "black"
    else:
        joueur_str = "white"
    with open('all_pos_' + type_ + '_' + joueur_str + '.json', 'w') as f:
        if type_ == "win":
            pos_win = [key for key, item in par.dico_win[joueur].items() if item[0] is True]
            json.dump(list(sorted(pos_win)), f, indent=4)
        else:
            pos_lose = [key for key, item in par.dico_lose[joueur].items() if item[0] is True]
            json.dump(list(sorted(pos_lose)), f, indent=4)


if __name__ == "__main__":
    to_do = []
    for joueur in [J_ATT, J_DEF]:
        for type_ in ['win', 'lose']:
            to_do.append((joueur, type_))
    with multiprocessing.Pool(3) as p:
        p.starmap(compute, to_do, 1)
    try:
        import winsound
        winsound.MessageBeep()
    except:
        pass
    #print(len(list(generate_combination(1, 1))))
