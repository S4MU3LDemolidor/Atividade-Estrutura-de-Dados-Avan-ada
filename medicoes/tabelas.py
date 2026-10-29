"""Formatação dos resultados em Markdown."""


def numero(x: float, casas: int = 2) -> str:
    """Número com vírgula decimal, como se escreve em português."""
    return f"{x:.{casas}f}".replace(".", ",")


def tabela(cabecalho: list, linhas: list[list]) -> str:
    """Tabela Markdown a partir do cabeçalho e das linhas."""
    partes = ["| " + " | ".join(str(c) for c in cabecalho) + " |",
              "|" + "---|" * len(cabecalho)]
    partes += ["| " + " | ".join(str(c) for c in linha) + " |" for linha in linhas]
    return "\n".join(partes)
