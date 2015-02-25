from tp01a import Doo
from tp01a import J_ATT, J_DEF, BLANCS, NOIRS, VIDE


def standardconf(customconf):
    """
    Retourne une configuration standardisé (tablier, tour) avec tour > 8
    à partir d'une configuration customisé (tablier, trait)
    """
    return customconf[0], 10 if customconf[1] == J_DEF else 11


def exist_position_adv_perdante(to_check):
    """
    On dit qu'une position est gagnante pour un joueur si il existe un coup tel
    que la nouvelle configuration est une position perdante pour l'adversaire
    """
    temp_doo = Doo()
    for new_conf in to_check:
        temp_doo.configuration = standardconf(new_conf)
        position_perdante_adv = temp_doo.perdant(temp_doo.trait)
        if position_perdante_adv:
            return True
    return False


def all_position_adv_gagnante(to_check):
    """
    Une position est perdante pour un joueur, si quelque soit son coup
    la nouvelle configuration est une position gagnante pour l'adversaire
    """
    temp_doo = Doo()
    for new_conf in to_check:
        temp_doo.configuration = standardconf(new_conf)
        position_gagnante_adv = temp_doo.gagnant(temp_doo.trait)
        if not position_gagnante_adv:
            return False
    return True


def final_configurations():
    """
    Retourne les configurations gagnantes/perdantes pour chaque camp
    """

    confs_win = {J_ATT: [], J_DEF: []}
    confs_lose = {J_ATT: [], J_DEF: []}

    doo = Doo()

    done = []
    to_check = list(futur_confs())

    while to_check:
        conf = to_check.pop()
        if conf not in done:
            doo.configuration = standardconf(conf)
            if not doo.finPartie(conf[1]):  # Si la game gen n'est pas gagnante
                to_check2 = list(futur_confs(doo))
                win = exist_position_adv_perdante(to_check2)
                lose = all_position_adv_gagnante(to_check2)
                if win:
                    confs_win[doo.trait].append(conf)
                elif lose:
                    confs_lose[doo.trait].append(conf)
                else:
                    for e in to_check2:
                        if e not in done:
                            to_check.append(e)
            done.append(conf)

    print('nb win noir', len(confs_win[J_ATT]))
    print('nb win blanc', len(confs_win[J_DEF]))
    print('nb lose noir', len(confs_lose[J_ATT]))
    print('nb lose blanc', len(confs_lose[J_DEF]))


def futur_confs(doo=None):
    """
    Génerateur des nouvelles configurations possibles
    """
    if doo is not None:
        for coup in doo.listeCoups(doo.trait):
            conf = doo.joue(doo.trait, coup)
            yield conf[0], doo.adversaire(doo.trait)
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
                    if temp.count(BLANCS) == 0:
                        print(temp)
                    yield temp, J_ATT
                    yield temp, J_DEF


if __name__ == '__main__':
    final_configurations()
