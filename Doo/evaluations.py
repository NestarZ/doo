import random
from tp01a import ROI, BLANCS, NOIRS, VIDE, J_ATT, J_DEF
from tp01b import cycling
from arbres import create_id
import json


def dummy(self, joueur):
    if self.perdant(joueur):
        return -100
    if self.gagnant(joueur):
        return 100
    if cycling(self.hist):  # On punit fortement le cycling pour les deux joueurs
            if joueur == J_ATT:
                return -10000
            else:
                return 10000
    return 0


def evaluation1(self, joueur):
    """
    evalue numeriquement la situation dans lequel se trouve le joueur
    """
    if self.perdant(joueur): return -10000
    if self.gagnant(joueur): return 10000
    if self.pose:
        score = 0
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                score -= self._distance_from_doo(i)
                if i % 2 == 1 and (pion == NOIRS or pion == ROI):
                    score += 2
        return score
    else:
        if cycling(self.hist):
            if joueur == J_ATT:
                return -10000
            else:
                return 10000
        nb_blancs = self.board.count(BLANCS)
        nb_noirs = 0
        smallest_distance = 3
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                nb_noirs += 1
                smallest_distance = min(smallest_distance, self._distance_from_doo(i))
        return - (smallest_distance)**2 - 3*nb_blancs


def evaluation2(self, joueur):
    """
    evalue numeriquement la situation dans lequel se trouve le joueur
    """
    if self.perdant(joueur): return -100
    if self.gagnant(joueur): return 100
    if self.pose:
        score = 0
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                for d in 'rudl':
                    try:
                        score += int(self.cell(i, d) == BLANCS) * 2
                    except ValueError:
                        pass
        return score
    else:
        if cycling(self.hist):
            if joueur == J_ATT:
                return -10000
            else:
                return 10000
        nb_blancs = self.board.count(BLANCS)
        nb_noirs = 0
        smallest_distance = 3
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                nb_noirs += 1
                smallest_distance = min(smallest_distance, self._distance_from_doo(i))
        return - (smallest_distance)**2 - nb_blancs - abs(nb_noirs - 1)


def evaluation3(self, joueur):
    """
    evalue numeriquement la situation dans lequel se trouve le joueur
    """
    if self.perdant(joueur): return -10000
    if self.gagnant(joueur): return 10000
    if self.pose:
        score = 0
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                score -= self._distance_from_doo(i)
                for d in 'rudl':
                        try:
                            score += int(self.cell(i, d) == NOIRS) * 2
                        except ValueError:
                            pass
        return score
    else:
        if cycling(self.hist):
            if joueur == J_ATT:
                return -10000
            else:
                return 10000
        nb_blancs = self.board.count(BLANCS)
        nb_noirs = 0
        smallest_distance = 3
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                nb_noirs += 1
                smallest_distance = min(smallest_distance, self._distance_from_doo(i))
        return -3 ** abs(nb_blancs - 1) + nb_noirs


def evaluation4(self, joueur):
    board = self.configuration[0]
    pose = self.configuration[1] < 8
    if self.perdant(joueur): return -10000
    if self.gagnant(joueur): return 10000
    if pose:
        score = 0
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                for d in 'rudl':
                        try:
                            score -= int(self.cell(i, d) == NOIRS)
                        except ValueError:
                            pass
            score -= self._distance_from_doo(i)
            if pion == ROI:
                score -= self._distance_from_doo(i)
        return score
        #return random.randint(0,100)
    else:
        if cycling(self.hist):
            if joueur == J_ATT:
                return -10000
            else:
                return 10000
        nb_blancs = board.count(BLANCS)
        nb_noirs = 0
        smallest_distance = 3
        for i, pion in enumerate(board):
            if pion == NOIRS or pion == ROI:
                nb_noirs += 1
                smallest_distance = min(smallest_distance, self._distance_from_doo(i))
        return (- (smallest_distance) - abs(nb_blancs - 1) ** 2 - 3 * int(board[4] == BLANCS)
                - abs(nb_noirs - 1))


def evaluation5(self, joueur):
    global pos_win
    board = self.configuration[0]
    pose = self.configuration[1] < 8
    if self.perdant(joueur): return -10000-self.configuration[1]
    if self.gagnant(joueur): return 10000-self.configuration[1]
    if pose:
        score = 0
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                score -= self._distance_from_doo(i)
        return score
        #return random.randint(0, 100)
    else:
        if cycling(self.hist):
            if joueur == J_ATT:
                return -10000
            else:
                return 10000
        nb_blancs = board.count(BLANCS)
        nb_noirs = 0
        smallest_distance = 3
        for i, pion in enumerate(board):
            if pion == NOIRS or pion == ROI:
                nb_noirs += 1
                smallest_distance = min(smallest_distance, self._distance_from_doo(i))
        if (board[4] == BLANCS):
            return - (smallest_distance) - 4*int(board[4] == BLANCS) - nb_blancs
        return - (smallest_distance) - nb_blancs*3


def evaluation6(self, joueur):
    global pos_win_white, pos_lose_black, pos_lose_white, pos_win_black
    board = self.configuration[0]
    idboard = [pion if pion != ROI else NOIRS for pion in board]
    trait = J_ATT if self.configuration[1] % 2 == 1 else J_DEF
    id_ = create_id((idboard, self.configuration[1]), trait)
    pose = self.configuration[1] < 8

    if self.perdant(joueur):
        return -1000+self.configuration[1]
    if self.gagnant(joueur):
        return 1000-self.configuration[1]

    if pose:
        score = 0
        for i, pion in enumerate(self.board):
            if pion == NOIRS or pion == ROI:
                score -= self._distance_from_doo(i)
                for l in "rudl":
                    try:
                        score += int(self.doo.cell(i, l) == BLANCS or self.doo.cell(i, l) == VIDE) * 2
                    except:
                        pass
        return score
        #return random.randint(0, 100)
    else:
        if cycling(self.hist):
            if joueur == J_ATT:
                return -10000
            else:
                return 10000
        nb_blancs = board.count(BLANCS)
        nb_noirs = 0
        smallest_distance = 3
        for i, pion in enumerate(board):
            if pion == NOIRS or pion == ROI:
                nb_noirs += 1
                smallest_distance = min(smallest_distance, self._distance_from_doo(i))

        if id_ in pos_win_black or id_ in pos_lose_white:
            return 1000 - self.configuration[1] - 4*(nb_blancs + nb_noirs)
        elif id_ in pos_win_white or id_ in pos_lose_black:
            return -1000 + self.configuration[1] + 4*(nb_blancs + nb_noirs)
        if (board[4] == BLANCS):
            return - (smallest_distance) - 2*int(board[4] == BLANCS) - nb_blancs
        return - 5*nb_blancs - smallest_distance


def evaluation6_random(self, joueur):
    global pos_win_white, pos_lose_black, pos_lose_white, pos_win_black
    board = self.configuration[0]
    idboard = [pion if pion != ROI else NOIRS for pion in board]
    trait = J_ATT if self.configuration[1] % 2 == 1 else J_DEF
    id_ = create_id((idboard, self.configuration[1]), trait)
    pose = self.configuration[1] < 8

    if self.perdant(joueur):
        return -1000+self.configuration[1]
    if self.gagnant(joueur):
        return 1000-self.configuration[1]

    if pose:
        return random.randint(0, 100)
    else:
        if cycling(self.hist):
            if joueur == J_ATT:
                return -10000
            else:
                return 10000
        nb_blancs = board.count(BLANCS)
        nb_noirs = 0
        smallest_distance = 3
        for i, pion in enumerate(board):
            if pion == NOIRS or pion == ROI:
                nb_noirs += 1
                smallest_distance = min(smallest_distance, self._distance_from_doo(i))

        if id_ in pos_win_black or id_ in pos_lose_white:
            return 1000 - self.configuration[1] - 4*(nb_blancs + nb_noirs)
        elif id_ in pos_win_white or id_ in pos_lose_black:
            return -1000 + self.configuration[1] + 4*(nb_blancs + nb_noirs)
        if (board[4] == BLANCS):
            return - (smallest_distance) - 2*int(board[4] == BLANCS) - nb_blancs
        return - 5*nb_blancs - smallest_distance

with open('all_pos_win_black.json', 'r') as f:
    pos_win_black = set(json.load(f))
with open('all_pos_win_white.json', 'r') as f:
    pos_win_white = set(json.load(f))
with open('all_pos_lose_black.json', 'r') as f:
    pos_lose_black = set(json.load(f))
with open('all_pos_lose_white.json', 'r') as f:
    pos_lose_white = set(json.load(f))
