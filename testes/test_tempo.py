"""Testes da cronometragem usada nas medições."""

import gc
import unittest

from medicoes.tempo import cronometrar, cronometrar_intercalado, cronometrar_lote


class TestCronometrar(unittest.TestCase):
    def test_chama_a_funcao_uma_vez_por_repeticao(self):
        chamadas = []
        tempos = cronometrar(chamadas.append, "entrada", 4)
        self.assertEqual(chamadas, ["entrada"] * 4)
        self.assertEqual(len(tempos), 4)
        self.assertTrue(all(t >= 0 for t in tempos))

    def test_lote_chama_para_cada_lista_e_divide_pelo_tamanho(self):
        chamadas = []
        lote = [[1], [2], [3]]
        tempos = cronometrar_lote(chamadas.append, lote, 2)
        self.assertEqual(chamadas, lote * 2)
        self.assertEqual(len(tempos), 2)
        self.assertTrue(all(t >= 0 for t in tempos))

    def test_religa_o_coletor_mesmo_com_erro(self):
        self.assertTrue(gc.isenabled())

        def falha(_):
            raise RuntimeError("falhou")

        with self.assertRaises(RuntimeError):
            cronometrar(falha, None, 1)
        self.assertTrue(gc.isenabled())


class TestIntercalado(unittest.TestCase):
    def test_gira_a_ordem_a_cada_rodada(self):
        ordem = []
        funcoes = {nome: (lambda _, nome=nome: ordem.append(nome)) for nome in "abc"}
        tempos = cronometrar_intercalado(funcoes, None, 3)
        self.assertEqual("".join(ordem), "abc" "bca" "cab")
        self.assertTrue(all(len(t) == 3 for t in tempos.values()))

    def test_recusa_vira_none_e_nao_e_chamada_de_novo(self):
        chamadas = []

        def recusa(_):
            chamadas.append(1)
            raise ValueError("faixa grande")

        tempos = cronometrar_intercalado({"ok": len, "recusa": recusa}, [1], 3,
                                         recusas=(ValueError,))
        self.assertIsNone(tempos["recusa"])
        self.assertEqual(len(chamadas), 1)
        self.assertEqual(len(tempos["ok"]), 3)

    def test_outros_erros_nao_sao_engolidos(self):
        def quebra(_):
            raise KeyError("bug")

        with self.assertRaises(KeyError):
            cronometrar_intercalado({"x": quebra}, None, 1, recusas=(ValueError,))

    def test_em_lote_chama_para_cada_lista(self):
        chamadas = []
        cronometrar_intercalado({"a": chamadas.append}, [[1], [2]], 2, em_lote=True)
        self.assertEqual(chamadas, [[1], [2], [1], [2]])


if __name__ == "__main__":
    unittest.main()
