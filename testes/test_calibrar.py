"""Testes das partes puras da calibração e da formatação das tabelas."""

import unittest

from medicoes.calibrar import inicio_das_vitorias_finais, ultimo_antes_da_derrota
from medicoes.tabelas import numero, tabela


class TestDecisoes(unittest.TestCase):
    def test_ultimo_antes_da_derrota(self):
        self.assertEqual(ultimo_antes_da_derrota([(1, True), (2, True), (3, False), (4, True)]), 2)

    def test_ultimo_antes_da_derrota_sem_derrota(self):
        self.assertEqual(ultimo_antes_da_derrota([(1, True), (2, True)]), 2)

    def test_ultimo_antes_da_derrota_perdendo_de_cara(self):
        self.assertIsNone(ultimo_antes_da_derrota([(1, False), (2, True)]))

    def test_inicio_das_vitorias_finais(self):
        resultados = [(16, False), (32, True), (64, False), (128, True), (256, True)]
        self.assertEqual(inicio_das_vitorias_finais(resultados), 128)

    def test_inicio_das_vitorias_finais_perdendo_no_fim(self):
        self.assertIsNone(inicio_das_vitorias_finais([(16, True), (32, False)]))

    def test_inicio_das_vitorias_finais_sempre_vencendo(self):
        self.assertEqual(inicio_das_vitorias_finais([(16, True), (32, True)]), 16)


class TestTabelas(unittest.TestCase):
    def test_numero_usa_virgula(self):
        self.assertEqual(numero(2.5), "2,50")
        self.assertEqual(numero(1234.56, 1), "1234,6")

    def test_tabela_markdown(self):
        self.assertEqual(
            tabela(["a", "b"], [[1, "x"], [2, "y"]]),
            "| a | b |\n|---|---|\n| 1 | x |\n| 2 | y |",
        )


if __name__ == "__main__":
    unittest.main()
