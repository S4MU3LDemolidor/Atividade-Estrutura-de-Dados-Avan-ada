"""Medição final: os quatro cenários contra os seis métodos e o ordenar.

Grava os tempos brutos em resultados/medicoes.csv e as tabelas em
resultados/tabela.md.

Uso: python3 -m medicoes.medir [--n 10000] [--repeticoes 5] [--semente 2026]
"""

import argparse
import csv
import datetime
import math
import random
import sys
from dataclasses import dataclass, field
from functools import partial
from pathlib import Path

from medicoes import cenarios
from medicoes.tabelas import numero, tabela
from medicoes.tempo import cronometrar_intercalado, descrever_maquina
from ordenacao.base import base
from ordenacao.contagem import FaixaGrandeDemais, contagem
from ordenacao.escolhedor import METODOS, escolher, ordenar

RESULTADOS = Path(__file__).resolve().parent.parent / "resultados"
TAMANHO_MINUSCULA = 8
LISTAS_MINUSCULAS = 1000

CONCORRENTES = {**METODOS, "ordenar": ordenar}
FIXOS = list(METODOS)


@dataclass
class Cenario:
    nome: str
    descricao: str
    entrada: list        # a lista, ou o lote de listas quando em_lote
    em_lote: bool = False
    extras: dict = field(default_factory=dict)   # medições a mais, além dos concorrentes

    @property
    def unidade(self) -> str:
        return "µs por lista" if self.em_lote else "ms"

    @property
    def escala(self) -> float:
        return 1e6 if self.em_lote else 1e3

    @property
    def exemplo(self) -> list:
        return self.entrada[0] if self.em_lote else self.entrada


def com_faixa_repassada(metodo, v: list[int]):
    return partial(metodo, minimo=min(v), maximo=max(v))


def montar_cenarios(n: int, semente: int) -> tuple[list[Cenario], Cenario]:
    aleatorio = cenarios.aleatorio_chaves_grandes(n, semente)
    faixa = cenarios.faixa_estreita(n, semente)
    principais = [
        Cenario("Aleatório, chaves grandes",
                f"{n} valores em [0, 10^12)", aleatorio,
                extras={"base (mínimo e máximo repassados)": com_faixa_repassada(base, aleatorio)}),
        Cenario("Faixa estreita",
                f"{n} valores em [0, {cenarios.FAIXA_ESTREITA})", faixa,
                extras={"contagem (mínimo e máximo repassados)": com_faixa_repassada(contagem, faixa)}),
        Cenario("Quase ordenado",
                f"{n} chaves grandes ordenadas com 1% de trocas entre vizinhos (até 10 posições)",
                cenarios.quase_ordenado(n, semente)),
        Cenario("Lista minúscula",
                f"{LISTAS_MINUSCULAS} listas de {TAMANHO_MINUSCULA} valores em [0, {cenarios.CHAVE_MINUSCULA})",
                cenarios.lote_minusculas(LISTAS_MINUSCULAS, TAMANHO_MINUSCULA, semente),
                em_lote=True),
    ]
    extra = Cenario("Metades trocadas",
                    f"{n} chaves grandes ordenadas com a segunda metade movida para a frente",
                    cenarios.metades_trocadas(n, semente))
    return principais, extra


# ---------------------------------------------------------------------------
# Cálculos sobre os tempos

def razoes(tempos: dict[str, dict[str, float | None]]) -> dict[str, dict[str, float]]:
    """Para cada método e cenário, tempo / menor tempo do cenário.

    `tempos[cenario][metodo]` é None quando o método recusou a lista; isso vira
    razão infinita.
    """
    resultado: dict[str, dict[str, float]] = {}
    for cenario, por_metodo in tempos.items():
        menor = min(t for t in por_metodo.values() if t is not None)
        for metodo, t in por_metodo.items():
            resultado.setdefault(metodo, {})[cenario] = math.inf if t is None else t / menor
    return resultado


def media_geometrica(valores: list[float]) -> float:
    if any(math.isinf(v) for v in valores):
        return math.inf
    return math.exp(sum(math.log(v) for v in valores) / len(valores))


def texto_razao(r: float) -> str:
    return "∞" if math.isinf(r) else numero(r)


# ---------------------------------------------------------------------------
# Medição

class Medicao:
    def __init__(self, n: int, repeticoes: int, semente: int):
        self.n = n
        self.repeticoes = repeticoes
        self.semente = semente
        self.brutos: list[list] = []   # linhas do CSV
        self.avisos: list[str] = []

    def medir_cenario(self, cenario: Cenario, funcoes: dict) -> dict[str, float | None]:
        """Mede as funções no cenário, guarda os tempos brutos e devolve o menor
        tempo de cada uma (None se recusou)."""
        print(f"  {cenario.nome}...", file=sys.stderr)
        tempos = cronometrar_intercalado(funcoes, cenario.entrada, self.repeticoes,
                                         em_lote=cenario.em_lote, recusas=(FaixaGrandeDemais,))
        menores = {}
        for rotulo, lista in tempos.items():
            if lista is None:
                self.brutos.append([cenario.nome, rotulo, "", "", "recusou: faixa grande demais"])
                menores[rotulo] = None
            else:
                self.brutos += [[cenario.nome, rotulo, i, f"{t:.9f}", ""] for i, t in enumerate(lista, 1)]
                menores[rotulo] = min(lista)
        return menores

    def celula(self, cenario: Cenario, t: float | None, negrito: bool = False) -> str:
        if t is None:
            return "recusou"
        texto = numero(t * cenario.escala)
        return f"**{texto}**" if negrito else texto

    def executar(self) -> str:
        random.seed(self.semente)
        principais, extra = montar_cenarios(self.n, self.semente)
        medidos = {c.nome: self.medir_cenario(c, {**CONCORRENTES, "escolher": escolher, **c.extras})
                   for c in principais}
        tempos = {nome: {m: medidos[nome][m] for m in CONCORRENTES} for nome in medidos}
        secoes = [self.secao_tempos(principais, tempos),
                  self.secao_razoes(principais, tempos),
                  self.secao_custo_escolher(principais, medidos),
                  self.secao_reaproveitar(principais, medidos),
                  self.secao_erro(extra)]
        return self.cabecalho() + self.secao_avisos() + "\n".join(secoes)

    def cabecalho(self) -> str:
        return (
            "# Medições\n\n"
            f"Gerado por `python3 -m medicoes.medir` em {datetime.date.today():%d/%m/%Y}.\n\n"
            f"- Máquina: {descrever_maquina()}\n"
            f"- n = {self.n}, semente {self.semente}\n"
            f"- {self.repeticoes} repetições intercaladas entre os concorrentes; vale o menor tempo\n"
            "- Tempos brutos em `resultados/medicoes.csv`\n\n"
        )

    def secao_avisos(self) -> str:
        if not self.avisos:
            return ""
        return "> **Atenção:** " + " ".join(self.avisos) + "\n\n"

    def secao_tempos(self, principais, tempos) -> str:
        linhas = []
        for c in principais:
            fixos = {m: tempos[c.nome][m] for m in FIXOS}
            vencedor = min((m for m in FIXOS if fixos[m] is not None), key=fixos.get)
            linhas.append(
                [f"{c.nome} ({c.unidade})"]
                + [self.celula(c, fixos[m], negrito=(m == vencedor)) for m in FIXOS]
                + [self.celula(c, tempos[c.nome]["ordenar"]), vencedor, escolher(c.exemplo).metodo]
            )
        descricoes = "\n".join(f"- **{c.nome}**: {c.descricao}" for c in principais)
        return (
            "## Tempos\n\n"
            f"{descricoes}\n\n"
            f"{tabela(['cenário'] + FIXOS + ['ordenar', 'vencedor fixo', 'ordenar escolheu'], linhas)}\n\n"
            "Em negrito, o método fixo mais rápido do cenário. \"recusou\": a contagem "
            "lançou `FaixaGrandeDemais` antes de alocar os contadores.\n"
        )

    def secao_razoes(self, principais, tempos) -> str:
        r = razoes(tempos)
        nomes = [c.nome for c in principais]
        piores = {m: max(r[m].values()) for m in CONCORRENTES}
        linhas = [[m] + [texto_razao(r[m][c]) for c in nomes]
                  + [texto_razao(piores[m]), texto_razao(media_geometrica(list(r[m].values())))]
                  for m in CONCORRENTES]
        melhor_fixo = min(FIXOS, key=piores.get)
        ganhou = piores["ordenar"] < piores[melhor_fixo]
        conclusao = (
            f"Pior razão do `ordenar`: **{texto_razao(piores['ordenar'])}**. "
            f"Melhor método fixo por esse critério: **{melhor_fixo}**, com pior razão "
            f"**{texto_razao(piores[melhor_fixo])}**. "
            + ("O `ordenar` ganha de qualquer escolha fixa."
               if ganhou else "O `ordenar` NÃO ganhou de todas as escolhas fixas.")
        )
        return (
            "## Razão para o mais rápido de cada cenário\n\n"
            "Tempo de cada concorrente dividido pelo menor tempo do cenário (1,00 = o "
            "mais rápido). A pior razão mostra quanto se perde, no pior cenário, por "
            "ficar preso àquela escolha.\n\n"
            f"{tabela(['método'] + nomes + ['pior razão', 'média geométrica'], linhas)}\n\n"
            f"{conclusao}\n"
        )

    def secao_custo_escolher(self, principais, medidos) -> str:
        linhas = []
        for c in principais:
            t = medidos[c.nome]
            escolha = escolher(c.exemplo).metodo
            melhor_fixo = min(t[m] for m in FIXOS if t[m] is not None)
            if t["escolher"] > t["ordenar"]:
                self.avisos.append(
                    f"em \"{c.nome}\" o escolher sozinho saiu mais lento que o ordenar, "
                    "que o inclui; houve interferência na medição. Rode de novo."
                )
            linhas.append([c.nome, escolha, self.celula(c, t["escolher"]), self.celula(c, t[escolha]),
                           self.celula(c, t["ordenar"]),
                           numero(100 * t["escolher"] / t["ordenar"], 1) + "%",
                           numero(t["ordenar"] / melhor_fixo)])
        return (
            "## Custo do escolher\n\n"
            "Tempo do `escolher` sozinho comparado com o `ordenar` inteiro (que inclui o "
            "`escolher`). A última coluna compara o `ordenar` com o melhor método fixo do "
            "cenário.\n\n"
            + tabela(["cenário", "escolha", "escolher", "método escolhido sozinho", "ordenar",
                      "escolher / ordenar", "ordenar / melhor fixo"], linhas)
            + "\n\nUnidades como na primeira tabela (ms; µs por lista na minúscula).\n"
        )

    def secao_reaproveitar(self, principais, medidos) -> str:
        linhas = []
        for c in principais:
            for rotulo, t_repassado in medidos[c.nome].items():
                if "repassados" not in rotulo:
                    continue
                metodo = rotulo.split()[0]
                t_calculando = medidos[c.nome][metodo]
                linhas.append([c.nome, metodo, numero(t_calculando * 1e3, 3),
                               numero(t_repassado * 1e3, 3),
                               numero((t_calculando - t_repassado) * 1e3, 3),
                               numero(medidos[c.nome]["escolher"] * 1e3, 3)])
        return (
            "## Reaproveitar mínimo e máximo\n\n"
            "O `escolher` já calcula mínimo e máximo; o `ordenar` repassa os dois para a "
            "contagem e a base, que assim não percorrem a lista de novo. Tempos em ms.\n\n"
            + tabela(["cenário", "método", "calculando", "repassados", "economia",
                      "custo do escolher"], linhas)
            + "\n"
        )

    def secao_erro(self, extra: Cenario) -> str:
        tempos = self.medir_cenario(extra, CONCORRENTES)
        escolha = escolher(extra.entrada).metodo
        validos = {m: t for m, t in tempos.items() if t is not None and m in FIXOS}
        melhor = min(validos, key=validos.get)
        linhas = [[m, self.celula(extra, t, negrito=(m == melhor))] for m, t in tempos.items()]
        return (
            "## Cenário em que o escolher erra\n\n"
            f"**{extra.nome}**: {extra.descricao}. O `escolher` escolheu "
            f"**{escolha}**; o melhor método fixo foi **{melhor}**.\n\n"
            + tabela(["método", "tempo (ms)"], linhas)
            + f"\n\nO `ordenar` levou {numero(tempos['ordenar'] / validos[melhor], 1)}x o "
            "tempo do melhor método.\n"
        )

    def gravar_csv(self, caminho: Path) -> None:
        with caminho.open("w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["cenario", "metodo", "repeticao", "segundos", "observacao"])
            escritor.writerows(self.brutos)


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Mede os métodos e o ordenar nos cenários.")
    parser.add_argument("--n", type=int, default=10_000)
    parser.add_argument("--repeticoes", type=int, default=5)
    parser.add_argument("--semente", type=int, default=2026)
    args = parser.parse_args(argv)

    medicao = Medicao(args.n, args.repeticoes, args.semente)
    print("Medindo (cerca de 15 segundos com os valores padrão)...", file=sys.stderr)
    relatorio = medicao.executar()

    RESULTADOS.mkdir(exist_ok=True)
    (RESULTADOS / "tabela.md").write_text(relatorio, encoding="utf-8")
    medicao.gravar_csv(RESULTADOS / "medicoes.csv")
    for aviso in medicao.avisos:
        print(f"ATENÇÃO: {aviso}", file=sys.stderr)
    print(relatorio)


if __name__ == "__main__":
    main()
