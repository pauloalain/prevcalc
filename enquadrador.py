from models import Segurado
import regras  # Carrega todas as regras na memória
from regras import Aposentadoria


class MotorEnquadramento:
    @staticmethod
    def _listar_todas_regras(classe_base: type = Aposentadoria) -> list[type[Aposentadoria]]:
        """Busca recursivamente todas as subclasses concretas de Aposentadoria."""
        todas = []
        for subclasse in classe_base.__subclasses__():
            # Se __abstractmethods__ estiver vazio, a classe já implementou checar_tipo
            if not subclasse.__abstractmethods__:
                todas.append(subclasse)
            todas.extend(MotorEnquadramento._listar_todas_regras(subclasse))
        return todas

    @classmethod
    def enquadrar(cls, segurado: Segurado) -> list[type[Aposentadoria]]:
        """Testa todas as regras concretas usando checar_tipo e retorna as elegíveis."""
        elegiveis: list[type[Aposentadoria]] = []

        for regra in cls._listar_todas_regras():
            try:
                if regra.checar_tipo(segurado):
                    elegiveis.append(regra)
            except Exception:
                continue

        return elegiveis
