from models import ResultadoCalculo, Segurado
from regras import (
    AcidentedeTrabalho,
    Aposentadoria,
    Compulsoria,
    Deficiencia,
    Especial,
    Especial_2019,
    IncapacidadePermanente,
    Regra2003_A,
    Regra2003_B,
    RegraDeTransicao_2003,
    RegraDeTransicao_2019,
    Voluntaria,
)


class CalculadoraProventos:
    @staticmethod
    def _calcular_regra_geral(segurado: Segurado) -> float:
        """Fórmula padrão da EC 103/2019: 60% + 2% por ano acima de 20 anos."""
        base_calculo = 0.60
        anos_excedentes = max(0, segurado.tempo_contribuicao - 20)
        return base_calculo + (anos_excedentes * 0.02)

    @classmethod
    def calcular(cls, segurado: Segurado, regra: type[Aposentadoria]) -> ResultadoCalculo:
        # --- Regras de Transição 2003 ---
        if regra in (RegraDeTransicao_2003, Regra2003_A, Regra2003_B):
            return ResultadoCalculo(percentual_media=None, coeficiente=1.0)

        # --- Regras de Transição 2019 ---
        if regra in (RegraDeTransicao_2019, Especial_2019):
            return ResultadoCalculo(percentual_media=0.8, coeficiente=1.0)

        # --- Incapacidade e Acidente ---
        if regra is AcidentedeTrabalho:
            return ResultadoCalculo(percentual_media=0.8, coeficiente=1.0)

        if regra is IncapacidadePermanente:
            return ResultadoCalculo(percentual_media=1.0, coeficiente=1.0)

        # --- Regras que usam a Fórmula Padrão (Explícitas) ---
        if regra is Voluntaria:
            coeficiente = cls._calcular_regra_geral(segurado)
            return ResultadoCalculo(percentual_media=1.0, coeficiente=round(coeficiente, 4))

        if regra is Especial:
            coeficiente = cls._calcular_regra_geral(segurado)
            return ResultadoCalculo(percentual_media=1.0, coeficiente=round(coeficiente, 4))

        if regra is Deficiencia:
            coeficiente = cls._calcular_regra_geral(segurado)
            return ResultadoCalculo(percentual_media=1.0, coeficiente=round(coeficiente, 4))

        if regra is Compulsoria:
            coeficiente = cls._calcular_regra_geral(segurado)
            if segurado.tempo_contribuicao < 20:
                coeficiente *= (segurado.tempo_contribuicao / 20)
            return ResultadoCalculo(percentual_media=1.0, coeficiente=round(coeficiente, 4))

        raise ValueError(f"Regra não mapeada na calculadora: {regra.__name__}")
