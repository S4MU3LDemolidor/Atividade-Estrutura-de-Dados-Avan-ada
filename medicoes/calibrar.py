"""Calibração dos limiares usados pelo escolhedor.

Faz varreduras para encontrar os pontos de virada entre os métodos (por exemplo,
até que tamanho a inserção ganha da híbrida), grava tudo em
resultados/calibracao.md e imprime os limiares sugeridos.

Uso: python3 -m medicoes.calibrar [--repeticoes 5] [--semente 2026]
"""

import argparse
import datetime
import operator
import random
import sys
from functools import partial
from itertools import islice
from pathlib import Path

from medicoes import cenarios
from medicoes.tabelas import numero, tabela
from medicoes.tempo import cronometrar_intercalado, descrever_maquina
from ordenacao.base import base
from ordenacao.contagem import contagem
from ordenacao.escolhedor import perfil
from ordenacao.hibrida import hibrida
from ordenacao.insercao import insercao
from ordenacao.intercalacao import intercalacao
from ordenacao.rapida import rapida

SAIDA = Path(__file__).resolve().parent.parent / "resultados" / "calibracao.md"

N = 10_000
CORTES = [1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64]
TAMANHOS_MINUSCULOS = [2, 3, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64]
LISTAS_POR_LOTE = 1000
FRACOES_LOCAIS = [0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
TROCAS_LONGE = [1, 2, 3, 5, 8, 10, 13, 16, 20, 30, 50, 100]
RAZOES_FAIXA = [0.01, 0.1, 0.5, 1, 2, 4, 8, 16, 32, 64, 128]
PASSADAS = range(1, 13)
TAMANHOS_BASE = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]
ELEMENTOS_POR_LOTE_BASE = 16384


# ---------------------------------------------------------------------------
# Regras para tirar um limiar de uma varredura

def ultimo_antes_da_derrota(resultados: list[tuple]) -> object | None:
    """Percorre (valor, venceu) em ordem e devolve o último valor antes da
    primeira derrota. None se perde logo no primeiro."""
    ultimo = None
    for valor, venceu in resultados:
        if not venceu:
            break
        ultimo = valor
    return ultimo


def inicio_das_vitorias_finais(resultados: list[tuple]) -> object | None:
    """Menor valor a partir do qual só há vitórias até o fim da varredura.
    None se perde no último."""
    inicio = None
    for valor, venceu in reversed(resultados):
        if not venceu:
            break
        inicio = valor
    return inicio


# ---------------------------------------------------------------------------
# Experimentos

class Calibracao:
    def __init__(self, repeticoes: int, semente: int):
        self.repeticoes = repeticoes
        self.semente = semente
        self.secoes: list[str] = []
        self.limiares: dict[str, object] = {}

    def menores(self, funcoes: dict, entrada, em_lote: bool = False) -> dict[str, float]:
        """Menor tempo (s) de cada função, com as repetições intercaladas."""
        tempos = cronometrar_intercalado(funcoes, entrada, self.repeticoes, em_lote=em_lote)
        return {nome: min(lista) for nome, lista in tempos.items()}

    def secao(self, titulo: str, texto: str, cabecalho: list, linhas: list, conclusao: str):
        self.secoes.append(f"## {titulo}\n\n{texto}\n\n{tabela(cabecalho, linhas)}\n\n{conclusao}\n")
        print(f"  {titulo}: {conclusao}", file=sys.stderr)

    def medir_corte(self):
        v = cenarios.aleatorio_chaves_grandes(N, self.semente)
        tempos = self.menores({c: partial(hibrida, corte=c) for c in CORTES}, v)
        melhor = min(tempos, key=tempos.get)
        self.limiares["CORTE"] = melhor
        self.hibrida = partial(hibrida, corte=melhor)
        self.secao(
            "CORTE da híbrida",
            f"Híbrida numa lista aleatória de {N} chaves grandes, variando o tamanho "
            "a partir do qual a sublista vai para a inserção.",
            ["corte", "tempo (ms)"],
            [[c, numero(t * 1e3)] for c, t in tempos.items()],
            f"Mais rápido: **CORTE = {melhor}**. Os experimentos seguintes usam esse corte.",
        )

    def medir_minuscula(self):
        concorrentes = {"insercao": insercao, "intercalacao": intercalacao,
                        "rapida": rapida, "hibrida": self.hibrida, "base": base}
        linhas, resultados = [], []
        for n in TAMANHOS_MINUSCULOS:
            lote = cenarios.lote_minusculas(LISTAS_POR_LOTE, n, self.semente + n)
            tempos = self.menores(concorrentes, lote, em_lote=True)
            vencedor = min(tempos, key=tempos.get)
            resultados.append((n, vencedor == "insercao"))
            linhas.append([n] + [numero(tempos[nome] * 1e6) for nome in concorrentes] + [vencedor])
        n_minuscula = ultimo_antes_da_derrota(resultados) or 1
        self.limiares["N_MINUSCULA"] = n_minuscula
        self.secao(
            "N_MINUSCULA",
            f"Lotes de {LISTAS_POR_LOTE} listas aleatórias com valores em "
            f"[0, {cenarios.CHAVE_MINUSCULA}). Tempo médio por lista, em microssegundos. "
            f"A contagem fica de fora: ela alocaria {cenarios.CHAVE_MINUSCULA} contadores "
            "para ordenar poucos elementos.",
            ["n"] + list(concorrentes) + ["vencedor"],
            linhas,
            f"A inserção vence todos até **N_MINUSCULA = {n_minuscula}**.",
        )

    def _outros(self):
        return {"intercalacao": intercalacao, "rapida": rapida,
                "hibrida": self.hibrida, "base": base}

    def _insercao_contra_outros(self, v):
        tempos = self.menores({"insercao": insercao, **self._outros()}, v)
        t_insercao = tempos.pop("insercao")
        melhor = min(tempos, key=tempos.get)
        return t_insercao, melhor, tempos[melhor]

    def medir_descidas(self):
        linhas, resultados = [], []
        for fracao in FRACOES_LOCAIS:
            v = cenarios.quase_ordenado(N, self.semente, fracao=fracao)
            p = perfil(v)
            t_ins, melhor, t_melhor = self._insercao_contra_outros(v)
            venceu = t_ins <= t_melhor
            resultados.append((p.descidas / N, venceu))
            linhas.append([numero(fracao * 100, 1) + "%", numero(p.descidas / N, 4),
                           numero(p.quedas / (p.maximo - p.minimo), 2),
                           numero(t_ins * 1e3), f"{melhor} {numero(t_melhor * 1e3)}",
                           "sim" if venceu else "não"])
        maior = ultimo_antes_da_derrota(resultados) or 0.0
        fracao_descidas = round(maior / 2, 3)
        self.limiares["FRACAO_DESCIDAS"] = fracao_descidas
        self.secao(
            "FRACAO_DESCIDAS (desordem local)",
            f"Listas quase ordenadas de {N} chaves grandes, com uma fração crescente "
            "de trocas entre vizinhos (até 10 posições). Tempos em ms.",
            ["trocas", "descidas/n", "quedas/amplitude", "inserção", "melhor outro", "inserção vence?"],
            linhas,
            f"Maior descidas/n com vitória da inserção: {numero(maior, 4)}. "
            f"Com margem de 2x: **FRACAO_DESCIDAS = {fracao_descidas}**.",
        )

    def medir_quedas(self):
        linhas, resultados = [], []
        ordenada = sorted(cenarios.aleatorio_chaves_grandes(N, self.semente))
        for trocas in TROCAS_LONGE:
            gerador = random.Random(self.semente + trocas)
            v = list(ordenada)
            for _ in range(trocas):
                i, j = gerador.randrange(N), gerador.randrange(N)
                v[i], v[j] = v[j], v[i]
            p = perfil(v)
            razao = p.quedas / (p.maximo - p.minimo)
            t_ins, melhor, t_melhor = self._insercao_contra_outros(v)
            venceu = t_ins <= t_melhor
            resultados.append((razao, venceu))
            linhas.append([trocas, numero(p.descidas / N, 4), numero(razao, 2),
                           numero(t_ins * 1e3), f"{melhor} {numero(t_melhor * 1e3)}",
                           "sim" if venceu else "não"])
        maior = ultimo_antes_da_derrota(resultados) or 0.0
        fator_quedas = round(maior / 2, 2)
        self.limiares["FATOR_QUEDAS"] = fator_quedas
        self.secao(
            "FATOR_QUEDAS (desordem longe)",
            f"Lista ordenada de {N} chaves grandes com trocas entre posições sorteadas. "
            "As descidas continuam poucas, mas cada troca obriga a inserção a "
            "atravessar muitas posições. Tempos em ms.",
            ["trocas", "descidas/n", "quedas/amplitude", "inserção", "melhor outro", "inserção vence?"],
            linhas,
            f"Maior quedas/amplitude com vitória da inserção: {numero(maior, 2)}. "
            f"Com margem de 2x: **FATOR_QUEDAS = {fator_quedas}**.",
        )

    def medir_contagem(self):
        linhas, resultados = [], []
        for razao in RAZOES_FAIXA:
            faixa = max(2, int(razao * N))
            gerador = random.Random(self.semente)
            v = [gerador.randrange(faixa) for _ in range(N)]
            minimo, maximo = min(v), max(v)
            tempos = self.menores({"contagem": partial(contagem, minimo=minimo, maximo=maximo),
                                   "base": partial(base, minimo=minimo, maximo=maximo),
                                   "hibrida": self.hibrida}, v)
            t_cont, t_base, t_hib = tempos["contagem"], tempos["base"], tempos["hibrida"]
            venceu = t_cont <= min(t_base, t_hib)
            resultados.append((razao, venceu))
            linhas.append([numero(razao, 2), faixa, numero(t_cont * 1e3),
                           numero(t_base * 1e3), numero(t_hib * 1e3), "sim" if venceu else "não"])
        fator = ultimo_antes_da_derrota(resultados) or 0
        self.limiares["FATOR_CONTAGEM"] = fator
        self.secao(
            "FATOR_CONTAGEM",
            f"Listas aleatórias de {N} valores numa faixa k = razão × n, com mínimo e "
            "máximo repassados (como o ordenar faz). Tempos em ms.",
            ["razão k/n", "k", "contagem", "base", "híbrida", "contagem vence?"],
            linhas,
            f"A contagem vence até **FATOR_CONTAGEM = {fator}**. Sem margem: errar "
            "aqui custa um fator constante, não O(n²).",
        )

    def medir_base(self):
        def com_faixa(metodo):
            return lambda t: metodo(t[0], t[1], t[2])

        rodar_base = com_faixa(base)
        rodar_hibrida = lambda t: self.hibrida(t[0])
        tabela_n_min, linhas = {}, []
        for p in PASSADAS:
            faixa = 256**p
            resultados, celulas = [], []
            for n in TAMANHOS_BASE:
                gerador = random.Random(self.semente * 1000 + p * 100 + n)
                lote = []
                for _ in range(max(1, ELEMENTOS_POR_LOTE_BASE // n)):
                    v = [gerador.randrange(faixa) for _ in range(n)]
                    lote.append((v, min(v), max(v)))
                tempos = self.menores({"base": rodar_base, "hibrida": rodar_hibrida}, lote, em_lote=True)
                razao = tempos["base"] / tempos["hibrida"]
                resultados.append((n, razao < 1))
                celulas.append(numero(razao))
            n_min = inicio_das_vitorias_finais(resultados)
            if n_min is not None:
                tabela_n_min[p] = n_min
            linhas.append([p] + celulas + [n_min if n_min is not None else "nunca"])
        self.limiares["N_MIN_BASE"] = tabela_n_min
        self.secao(
            "N_MIN_BASE",
            "Razão tempo(base) / tempo(híbrida) para chaves com p bytes (valores em "
            "[0, 256^p)) e tamanhos n. Abaixo de 1, a base vence. Cada célula mede um "
            f"lote de cerca de {ELEMENTOS_POR_LOTE_BASE} elementos.",
            ["passadas"] + [f"n={n}" for n in TAMANHOS_BASE] + ["base vence a partir de"],
            linhas,
            f"**N_MIN_BASE = {tabela_n_min}**",
        )

    def medir_passada(self):
        def nativas(v):
            return min(v), max(v), sum(map(operator.gt, v, islice(v, 1, None)))

        linhas, comparacoes = [], []
        for nome, v in [("aleatória", cenarios.aleatorio_chaves_grandes(N, self.semente)),
                        ("quase ordenada", cenarios.quase_ordenado(N, self.semente))]:
            tempos = self.menores({"perfil": perfil, "nativas": nativas}, v)
            t_perfil, t_nativas = tempos["perfil"], tempos["nativas"]
            razao = t_perfil / t_nativas
            linhas.append([nome, numero(t_perfil * 1e3, 3), numero(t_nativas * 1e3, 3), numero(razao)])
            comparacoes.append(f"na lista {nome}, a passada única custa {numero(razao)}x o tempo das nativas")
        self.secao(
            "Custo de olhar a lista",
            f"`perfil(v)` (uma passada em Python: mínimo, máximo, descidas e quedas) contra "
            f"três passadas com funções nativas em C (`min`, `max` e descidas com `map`, "
            f"sem as quedas), em listas de {N}. Tempos em ms.",
            ["lista", "perfil (1 passada)", "nativas (3 passadas)", "perfil / nativas"],
            linhas,
            "Resultado: " + "; ".join(comparacoes) + ". Na aleatória, metade dos elementos é "
            "descida e soma uma queda, por isso a passada única fica mais cara.",
        )

    def relatorio(self) -> str:
        limiares = "\n".join(f"{nome} = {valor!r}" for nome, valor in self.limiares.items())
        cabecalho = (
            "# Calibração dos limiares\n\n"
            f"Gerado por `python3 -m medicoes.calibrar` em {datetime.date.today():%d/%m/%Y}.\n\n"
            f"- Máquina: {descrever_maquina()}\n"
            f"- {self.repeticoes} repetições intercaladas entre os concorrentes de cada ponto; vale o menor tempo\n"
            f"- Semente: {self.semente}\n\n"
            "## Limiares sugeridos\n\n"
            f"```python\n{limiares}\n```\n"
        )
        return cabecalho + "\n" + "\n".join(self.secoes)


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Calibra os limiares do escolhedor.")
    parser.add_argument("--repeticoes", type=int, default=5)
    parser.add_argument("--semente", type=int, default=2026)
    args = parser.parse_args(argv)

    random.seed(args.semente)
    calibracao = Calibracao(args.repeticoes, args.semente)
    print("Calibrando (cerca de 1 minuto)...", file=sys.stderr)
    for experimento in (calibracao.medir_corte, calibracao.medir_minuscula, calibracao.medir_descidas,
                        calibracao.medir_quedas, calibracao.medir_contagem, calibracao.medir_base,
                        calibracao.medir_passada):
        experimento()

    SAIDA.parent.mkdir(exist_ok=True)
    SAIDA.write_text(calibracao.relatorio(), encoding="utf-8")
    print(f"\nResultados em {SAIDA}\n\nLimiares sugeridos:", file=sys.stderr)
    for nome, valor in calibracao.limiares.items():
        print(f"{nome} = {valor!r}")


if __name__ == "__main__":
    main()
