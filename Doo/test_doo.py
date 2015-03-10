import unittest

from tp01a import Doo
from tp01a import J_ATT, J_DEF, BLANCS, NOIRS, ROI, VIDE



class TestDoo(unittest.TestCase):

    def test_listecoup(self):
        doo = Doo()
        board = [VIDE, VIDE, VIDE,
                 VIDE, VIDE, VIDE,
                 VIDE, BLANCS, VIDE,
                 VIDE, VIDE, VIDE]

        t = 10
        doo.configuration = board, t
        print(doo.listeCoups(J_DEF))

        board = [VIDE, VIDE, VIDE,
                 VIDE, NOIRS, VIDE,
                 VIDE, BLANCS, VIDE,
                 VIDE, VIDE, VIDE]
        t = 10
        doo.configuration = board, t
        print(doo.listeCoups(J_DEF))

        board = [ VIDE, NOIRS, VIDE,
                 NOIRS, BLANCS, ROI,
                 BLANCS, NOIRS, VIDE,
                 VIDE, VIDE, VIDE ]
        t = 10
        doo.configuration = board, t
        print(doo.listeCoups(J_DEF))

        board = [ VIDE, NOIRS, VIDE,
                 NOIRS, BLANCS, ROI,
                 BLANCS, NOIRS, BLANCS,
                 VIDE, VIDE, VIDE ]
        t = 10
        doo.configuration = board, t
        print(doo.listeCoups(J_DEF))

        board = [ VIDE, VIDE, VIDE,
                 VIDE, NOIRS, ROI,
                 BLANCS, BLANCS, BLANCS,
                 VIDE, VIDE, VIDE ]
        t = 10
        doo.configuration = board, t
        print(doo.listeCoups(J_DEF))

        board = [ NOIRS, VIDE, VIDE,
                 VIDE, BLANCS, VIDE,
                 VIDE, VIDE, VIDE,
                 VIDE, VIDE, VIDE ]
        t = 13
        doo.configuration = board, t
        print(doo.listeCoups(J_ATT))

        board = [ BLANCS, BLANCS, BLANCS,
                 NOIRS, VIDE, BLANCS,
                 BLANCS, BLANCS, NOIRS,
                 BLANCS, NOIRS, ROI ]
        t = 13
        doo.configuration = board, t
        print(doo.listeCoups(J_ATT))
