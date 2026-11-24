from models import ResultadoCalculo, Segurado
from regras import (
    AcidentedeTrabalho,
    Aposentadoria,
    Compulsoria,
    IncapacidadePermanente,
    RegraDeTransicao_2003,
    RegraDeTransicao_2019,
)


class CalculadoraProventos:
    @staticmethod
    def calcular(segurado: Segurado, regra: type[Aposentadoria]) -> ResultadoCalculo:
        # 1. Regras de Transição de 2003 (e suas filhas A e B): Integralidade e Paridade
        if issubclass(regra, RegraDeTransicao_2003):
            return ResultadoCalculo(percentual_media=None, coeficiente=1.0)

        # 2. Regras de Transição de 2019 (e Especial_2019): Média de 80% com 100%
        if issubclass(regra, RegraDeTransicao_2019):
            return ResultadoCalculo(percentual_media=0.8, coeficiente=1.0)

        # 3. Acidente de Trabalho (testar antes de IncapacidadePermanente pois é filha dela!)
        if issubclass(regra, AcidentedeTrabalho):
            return ResultadoCalculo(percentual_media=0.8, coeficiente=1.0)

        # 4. Incapacidade Permanente comum
        if issubclass(regra, IncapacidadePermanente):
            return ResultadoCalculo(percentual_media=1.0, coeficiente=1.0)

        # 5. Regra Geral (Voluntaria, Especial, Deficiencia, Compulsoria)
        base_calculo = 0.60
        anos_excedentes = max(0, segurado.tempo_contribuicao - 20)
        coeficiente = base_calculo + (anos_excedentes * 0.02)

        if issubclass(regra, Compulsoria) and segurado.tempo_contribuicao < 20:
            coeficiente *= (segurado.tempo_contribuicao / 20)

        return ResultadoCalculo(percentual_media=1.0, coeficiente=round(coeficiente, 4))
