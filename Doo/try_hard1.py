import itertools
import tp01b

from tp01a import Doo
from tp01a import J_ATT, J_DEF, BLANCS, NOIRS, ROI, VIDE


def lol():
    confs_win = {J_ATT: [], J_DEF: []}
    confs_lose = {J_ATT: [], J_DEF: []}

    a_traiter = [doo for doo in futur_confs()]
    traite = []
    i = 0
    while a_traiter:
        if i % 100 == 0:
            print('a traiter:', len(a_traiter))
            print('traité:', len(traite))
            i = 0
        i += 1
        doo = Doo()
        conf = a_traiter.pop()
        doo.configuration = conf
        if (conf[0], doo.trait) not in traite:
            lose = True
            for futur in futur_confs(doo):
                doo_t = Doo()
                doo_t.configuration = futur
                if not doo_t.gagnant(doo.trait):
                    lose = False
                    break
            if lose:
                confs_lose[doo.trait].append((conf[0], doo.trait))
                conf_sym = sym(conf[0])
                if conf_sym != conf[0]:
                    confs_lose[doo.trait].append((conf_sym, doo.trait))

            win = False

            for futur in futur_confs(doo):
                doo_t = Doo()
                doo_t.configuration = futur
                if doo_t.perdant(doo_t.trait):
                    win = True
                    break
            if win:
                confs_win[doo.trait].append((conf[0], doo.trait))
                conf_sym = sym(conf[0])
                if conf_sym != conf[0]:
                    confs_win[doo.trait].append((conf_sym, doo.trait))

            if not win and not lose:
                for futur in futur_confs(doo):
                    a_traiter.append(futur)
            traite.append((conf[0], doo.trait))
            conf_sym = sym(conf[0])
            if conf_sym != conf[0]:
                    traite.append((conf_sym, doo.trait))

    print('nb win noir', len(confs_win[J_ATT]))
    print('nb win blanc', len(confs_win[J_DEF]))
    print('nb lose noir', len(confs_lose[J_ATT]))
    print('nb lose blanc', len(confs_lose[J_DEF]))

    for conf in confs_lose[J_DEF]:
        doo = Doo()
        doo.configuration = conf
        print(doo)

def sym(board):
    retour = board[:]
    for i in range(4):
        retour[i*3], retour[i*3+2] = retour[i*3+2], retour[i*3]
    return retour


def futur_confs(doo=None):
    if doo != None:
        for coup in doo.listeCoups(doo.trait):
            conf = doo.joue(doo.trait, coup)
            yield conf
    else:
        doo = Doo()
        board = [VIDE, VIDE, VIDE,
                 VIDE, VIDE, VIDE,
                 VIDE, VIDE, VIDE,
                 VIDE, VIDE, VIDE]
        for x in range(12):
            for y in range(12):
                if x != y:
                    temp = board[:]
                    temp[x] = NOIRS
                    temp[y] = BLANCS
                    yield temp, 8
                    yield temp, 9
lol()