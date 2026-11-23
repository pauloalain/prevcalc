from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Segurado:
    # --- Dados Base (já tipados) ---
    sexo: str
    idade: int = 0
    tempo_contribuicao: int = 0
    tempo_servico_publico: int = 0
    tempo_cargo: int = 0

    # --- Dados Específicos ---
    tempo_magisterio: int = 0
    especial: bool = False
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

        campos_numericos = (
            self.idade,
            self.tempo_contribuicao,
            self.tempo_servico_publico,
            self.tempo_cargo,
            self.tempo_magisterio,
            self.exposicao,
        )
        if any(valor < 0 for valor in campos_numericos):
            raise ValueError("Tempos e idade não podem ser negativos.")


"""
Classe abstrata define principais padrões de requisitos para aposentadoria.
Contrato flexível usando o modelo Segurado, mas classe pai adianta principais padrões.
"""


class Aposentadoria(ABC):  # Classe não instanciada.
    # Padrões de contagem que se repetem em vários tipos de aposentadoria.
    min_tempo_contribuicao = 25
    min_servico_publico = 15
    min_cargo = 5

    def __init__(self, segurado: Segurado):
        self.segurado = segurado

    @classmethod
    @abstractmethod
    def checar_tipo(cls, segurado: Segurado) -> bool:
        pass

    @classmethod
    def coeficiente_redutor(cls, segurado: Segurado) -> float:
        return 1.0

    # Coeficiente redutor aplicado somente no caso de Aposentadoria Compulsória (< 20 anos).
    # Cálculo geral: (60% + 2% por ano que passar de 20 anos) x (100% da média das contribuições desde 1994)
    @classmethod
    def calcular_proventos(cls, segurado: Segurado) -> float:
        base_calculo = 0.60
        anos_excedentes = max(0, segurado.tempo_contribuicao - 20)
        bonus = anos_excedentes * 0.02
        coeficiente = (base_calculo + bonus) * cls.coeficiente_redutor(segurado)
        return coeficiente


class Voluntaria(Aposentadoria):
    """
    Aposentadoria Voluntária - Padrão típico de aposentadoria baseado em Idade,
    Tempo de contribuição, tempo de serviço público e tempo no cargo.
    """
    @classmethod
    def checar_tipo(cls, segurado: Segurado) -> bool:
        idade_minima = 60 if segurado.sexo == 'F' else 65

        # Redução de 5 anos de idade mínima caso cumpra o tempo de contribuição em magistério.
        if segurado.tempo_magisterio >= 25:
            idade_minima -= 5

        return (
            segurado.idade >= idade_minima
            and segurado.tempo_contribuicao >= cls.min_tempo_contribuicao
            and segurado.tempo_servico_publico >= cls.min_servico_publico
            and segurado.tempo_cargo >= cls.min_cargo
        )


class Especial(Aposentadoria):
    @classmethod
    def checar_tipo(cls, segurado: Segurado) -> bool:
        idade_minima = 57 if segurado.sexo == 'F' else 60

        return (
            segurado.especial
            and segurado.idade >= idade_minima
            and segurado.tempo_contribuicao >= cls.min_tempo_contribuicao
            and segurado.tempo_servico_publico >= cls.min_servico_publico
            and segurado.tempo_cargo >= cls.min_cargo
            and segurado.exposicao >= 25
        )


class Deficiencia(Aposentadoria):
    def __init__(self, segurado: Segurado, modificador: int | None = None):
        super().__init__(segurado)
        self.modificador = (
            modificador
            if modificador is not None
            else self.__class__.modificador_tempo(segurado.sexo)
        )

    @classmethod
    def modificador_tempo(cls, sexo: str) -> int:
        return -10

    @classmethod
    def checar_tipo(cls, segurado: Segurado) -> bool:
        grau_da_classe = cls.__name__.replace('Deficiencia', '').upper()

        if grau_da_classe == '':
            valida_grau = True
            idade_minima = 55 if segurado.sexo == 'F' else 60
        else:
            valida_grau = (segurado.grau_deficiencia == grau_da_classe)
            idade_minima = 0

        tempo_minimo_necessario = cls.min_tempo_contribuicao + cls.modificador_tempo(segurado.sexo)

        return (
            segurado.deficiencia
            and valida_grau
            and segurado.idade >= idade_minima
            and segurado.tempo_contribuicao >= tempo_minimo_necessario
            and segurado.tempo_servico_publico >= cls.min_servico_publico
            and segurado.tempo_cargo >= cls.min_cargo
        )


class DeficienciaGrave(Deficiencia):
    @classmethod
    def modificador_tempo(cls, sexo: str) -> int:
        return -5 if sexo == 'F' else 0


class DeficienciaModerada(Deficiencia):
    @classmethod
    def modificador_tempo(cls, sexo: str) -> int:
        return -1 if sexo == 'F' else 4


class DeficienciaLeve(Deficiencia):
    @classmethod
    def modificador_tempo(cls, sexo: str) -> int:
        return 3 if sexo == 'F' else 8


class Compulsoria(Aposentadoria):
    @classmethod
    def checar_tipo(cls, segurado: Segurado) -> bool:
        return segurado.idade >= 75

    @classmethod
    def coeficiente_redutor(cls, segurado: Segurado) -> float:
        if segurado.tempo_contribuicao < 20:
            return segurado.tempo_contribuicao / 20
        return 1.0


class IncapacidadePermanente(Aposentadoria):
    @classmethod
    def checar_tipo(cls, segurado: Segurado) -> bool:
        return segurado.incapacidade_permanente

    @classmethod
    def calcular_proventos(cls, segurado: Segurado) -> float:
        return 1.0


class AcidentedeTrabalho(IncapacidadePermanente):
    @classmethod
    def checar_tipo(cls, segurado: Segurado) -> bool:
        return segurado.incapacidade_permanente and segurado.acidente_de_trabalho

    @classmethod
    def calcular_proventos(cls, segurado: Segurado) -> float:
        return 0.8
