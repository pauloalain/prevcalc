from models import Segurado
import regras  # Garante que todas as classes do módulo sejam carregadas na memória
from regras import Aposentadoria


class MotorEnquadramento:
    @staticmethod
    def _listar_todas_regras(classe_base: type = Aposentadoria) -> list[type[Aposentadoria]]:
        """Busca recursivamente todas as subclasses (filhas, netas, etc.) de Aposentadoria."""
        todas = []
        for subclasse in classe_base.__subclasses__():
            todas.append(subclasse)
            todas.extend(MotorEnquadramento._listar_todas_regras(subclasse))
        return todas

    @classmethod
    def enquadrar(cls, segurado: Segurado) -> list[type[Aposentadoria]]:
        """Recebe o Segurado normalizado, testa todas as regras e retorna apenas as classes elegíveis."""
        elegiveis: list[type[Aposentadoria]] = []

        for regra in cls._listar_todas_regras():
            try:
                if regra.elegivel(segurado):
                    elegiveis.append(regra)
            except Exception:
                # Se faltar algum dado (None) ou ocorrer erro na avaliação desta regra,
                # o motor não para e continua testando todas as outras regras normalmente.
                continue

        return elegiveis
