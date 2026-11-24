from abc import ABC, abstractmethod
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


"""
Classe abstrata define principais padrões de requisitos para aposentadoria.
Contrato flexível usando o modelo Segurado, mas classe pai adianta principais padrões.
"""


class Aposentadoria(ABC):  # Classe não instanciada.
    # Padrões de contagem que se repetem em vários tipos de aposentadoria.
    min_tempo_contribuicao = 25
    min_servico_publico = 15
    min_cargo = 5
    percentual_de_contrib: float | None = 1.0

    def __init__(self, segurado: Segurado):
        self.segurado = segurado

    @classmethod
    @abstractmethod
    def checar_tipo(cls, segurado: Segurado) -> bool:
        pass

    # Coeficiente redutor aplicado somente no caso de Aposentadoria Compulsória (< 20 anos).
    # Cálculo geral: (60% + 2% por ano que passar de 20 anos) x (média de 100% das contribuições desde 1994)


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
            segurado.idade >= idade_minima
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

class IncapacidadePermanente(Aposentadoria):
    @classmethod
    def checar_tipo(cls, segurado: Segurado) -> bool:
        return segurado.incapacidade_permanente

class AcidentedeTrabalho(IncapacidadePermanente):
    percentual_de_contrib = 0.8  # Herda calcular_proventos() e já retorna (0.8, 1.0)!
    @classmethod
    def checar_tipo(cls, segurado: Segurado) -> bool:
        return segurado.incapacidade_permanente and segurado.acidente_de_trabalho

class RegraDeTransicao_2003(Aposentadoria):
    data_limite_ingresso = date(2019, 12, 31)

class RegraDeTransicao_2003_A(RegraDeTransicao_2003):
    min_servico_publico = 20
    
    @classmethod
    def checar_tipo(cls, segurado: Segurado) -> bool:
        if segurado.data_ingresso_servico_publico is None:
            return False

        if segurado.sexo == 'F':
            idade_minima = 55
            min_tempo_contribuicao = 30
            tempo_min_magisterio = 25
        else:
            idade_minima = 60
            min_tempo_contribuicao = 35
            tempo_min_magisterio = 30          
        
        if segurado.tempo_magisterio >= tempo_min_magisterio:
            idade_minima -= 5
            min_tempo_contribuicao -= 5

        return (
            segurado.data_ingresso_servico_publico <= cls.data_limite_ingresso
            and segurado.idade >= idade_minima
            and segurado.tempo_contribuicao >= min_tempo_contribuicao
            and segurado.tempo_servico_publico >= cls.min_servico_publico
            and segurado.tempo_cargo >= cls.min_cargo
        )

class RegraDeTransicao_2003_B(RegraDeTransicao_2003): #Regra de Transição sem Idade Mínima
    min_servico_publico = 25
    min_tempo_carreira = 15

    @classmethod
    def checar_tipo(cls, segurado: Segurado) -> bool:
        if segurado.data_ingresso_servico_publico is None:
            return False
            
        if segurado.sexo == 'F':
            idade_minima = 55
            min_tempo_contribuicao = 30
        else:
            idade_minima = 60
            min_tempo_contribuicao = 35
            
        anos_excedentes = max(0, segurado.tempo_contribuicao - min_tempo_contribuicao)
        idade_minima -= anos_excedentes
        
        return (
            segurado.data_ingresso_servico_publico <= cls.data_limite_ingresso
            and segurado.idade >= idade_minima
            and segurado.tempo_contribuicao >= min_tempo_contribuicao
            and segurado.tempo_carreira >= cls.min_tempo_carreira
            and segurado.tempo_servico_publico >= cls.min_servico_publico
            and segurado.tempo_cargo >= cls.min_cargo
        )

class RegraDeTransicao_2019(Aposentadoria):
    data_limite_ingresso = date(2019, 11, 13)
    min_servico_publico = 20

    @classmethod
    def checar_tipo(cls, segurado: Segurado) -> bool:
        if segurado.data_ingresso_servico_publico is None:
            return False
            
        if segurado.sexo == 'F':
            idade_minima = 55
            min_tempo_contribuicao = 30
            tempo_min_magisterio = 25
        else:
            idade_minima = 60
            min_tempo_contribuicao = 35
            tempo_min_magisterio = 30

        if segurado.tempo_magisterio >= tempo_min_magisterio:
            idade_minima -= 5
            min_tempo_contribuicao -= 5

        return (
            segurado.data_ingresso_servico_publico <= cls.data_limite_ingresso
            and segurado.idade >= idade_minima
            and segurado.tempo_contribuicao >= min_tempo_contribuicao
            and segurado.tempo_servico_publico >= cls.min_servico_publico
            and segurado.tempo_cargo >= cls.min_cargo
        )

class Especial_2019(RegraDeTransicao_2019):
    min_tempo_carreira = 15

    @classmethod
    def checar_tipo(cls, segurado: Segurado) -> bool:
        if segurado.data_ingresso_servico_publico is None:
            return False
            
        pontuacao = segurado.idade + segurado.tempo_contribuicao

        return (
            segurado.data_ingresso_servico_publico <= cls.data_limite_ingresso
            and segurado.tempo_servico_publico >= cls.min_servico_publico
            and segurado.tempo_cargo >= cls.min_cargo
            and segurado.tempo_carreira >= cls.min_tempo_carreira
            and segurado.exposicao >= 25
            and pontuacao >= 85
        )





