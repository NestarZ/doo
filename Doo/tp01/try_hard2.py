import itertools
import tp01b

from tp01a import Doo
from tp01a import J_ATT, J_DEF, BLANCS, NOIRS, ROI, VIDE
                
def final_configurations():
    confs_win = {J_ATT: [], J_DEF: []}
    confs_lose = {J_ATT: [], J_DEF: []}

    doo = Doo()
    j_trait = doo.trait
    
    done = []
    to_check = list(futur_confs())
    
    print(len(to_check))
    while to_check:
        conf = to_check.pop()
        if conf not in done:
            _tr = 10 if conf[1] == J_DEF else 11
            doo.configuration = conf[0], _tr
            win = doo.gagnant(doo.trait)
            lose = doo.perdant(doo.trait)
            if win:
                print(Doo.format(conf))
                confs_win[j_trait].append(conf)
            elif lose:
                confs_lose[j_trait].append(conf)
            else:
                to_check2 = futur_confs(doo)
                for e in to_check2:
                    if e not in done:
                        to_check.append(e)
            done.append(conf)
    print(len(done))
    
    print('nb win noir', len(confs_win[J_ATT]))
    print('nb win blanc', len(confs_win[J_DEF]))
    print('nb lose noir', len(confs_lose[J_ATT]))
    print('nb lose blanc', len(confs_lose[J_DEF]))

def futur_confs(doo=None):
    if doo != None:
        for coup in doo.listeCoups(doo.trait):
            conf = doo.joue(doo.trait, coup)
            yield conf[0], doo.trait
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
                    yield temp, J_ATT
                    yield temp, J_DEF
                    
final_configurations()
