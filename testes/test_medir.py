"""Testes do cálculo das razões usado na medição final."""

import math
import unittest

from medicoes.medir import media_geometrica, razoes


class TestRazoes(unittest.TestCase):
    def test_razao_para_o_mais_rapido_do_cenario(self):
        medianas = {
            "c1": {"a": 2.0, "b": 1.0},
            "c2": {"a": 3.0, "b": 6.0},
        }
        self.assertEqual(razoes(medianas), {"a": {"c1": 2.0, "c2": 1.0},
                                            "b": {"c1": 1.0, "c2": 2.0}})

    def test_recusou_vira_infinito(self):
        medianas = {"c1": {"a": 1.0, "b": None}}
        self.assertEqual(razoes(medianas)["b"]["c1"], math.inf)

    def test_media_geometrica(self):
        self.assertAlmostEqual(media_geometrica([1.0, 4.0]), 2.0)
        self.assertEqual(media_geometrica([1.0, math.inf]), math.inf)


if __name__ == "__main__":
    unittest.main()
