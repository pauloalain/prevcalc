from dataclasses import dataclass, field
from datetime import date
from typing import Any

@dataclass
class Segurado:
    # --- Dados Base (já tipados) ---
    sexo: str
    idade: int = 0
    tempo_contribuicao: int = 0
    tempo_servico_publico: int = 0
    tempo_cargo: int = 0
    data_ingresso_servico_publico: date | None = None  # Novo campo!

    # --- Dados Específicos ---
    tempo_carreira: int = 0
    tempo_magisterio: int = 0
    exposicao: int = 0
    deficiencia: bool = False
    grau_deficiencia: str = ''
    incapacidade_permanente: bool = False
    acidente_de_trabalho: bool = False

    # --- Extras ---
    dados_extras: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        # Apenas regras de domínio (não conversão de formatos externos)
        if self.sexo not in ('M', 'F'):
            raise ValueError("Sexo deve ser 'M' ou 'F'.")

        if self.data_ingresso_servico_publico and self.data_ingresso_servico_publico > date.today():
            raise ValueError("Data de ingresso não pode ser no futuro.")

        campos_numericos = (
            self.idade,
            self.tempo_contribuicao,
            self.tempo_servico_publico,
            self.tempo_cargo,
            self.tempo_carreira,
            self.tempo_magisterio,
            self.exposicao,
        )
        if any(valor < 0 for valor in campos_numericos):
            raise ValueError("Tempos e idade não podem ser negativos.")

    class ResultadoCalculo(NamedTuple):
        percentual_media: float | None
        coeficiente_proporcao: float

