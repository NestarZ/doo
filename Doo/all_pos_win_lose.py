from tp01b import manche, replay, Human
from arbres import Parcours, IA
from tp01a import *

import itertools

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
        return ((conf[1]%2)*2-1) * conf[0]
    dico_pions = {VIDE: 1, ROI: 100, NOIRS: 10000, BLANCS: 1000000}
    identifiant = 0
    for i, case in enumerate(conf[0]):
        identifiant ^= dico_pions[case] * (i+1)
    if jtrait == J_ATT:
        identifiant ^= 898  # max id = 276 pour les cases
    return identifiant

if __name__ == "__main__":
	doo = Doo()
	par = Parcours(doo)


	pos_win_black = []
	for nb_noirs in range(1, 3):
		for nb_blancs in range(1, 3):
			for comb in generate_combination(nb_noirs, nb_blancs):
			    doo.configuration = comb, 11
			    if (par.positionGagnante(J_ATT)[1]):
			        pos_win_black.append(create_id(doo.configuration, J_ATT))

	print(sorted(pos_win_black))
