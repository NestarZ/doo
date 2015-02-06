import unittest

from tp01 import Doo
from tp01 import J_ATT, J_DEF, BLANCS, NOIRS, ROI, VIDE



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
