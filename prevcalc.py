# Classe abstrata Aposentadoria 
from abc import ABC, abstractmethod
"""
#Classe abstrata define principais padrões de requisitos para aposentadoria e **kwargs permite outros parâmetros para classes filhas. Contrato flexível, mas classe pai adianta principais padrões.

Criei uma forma que fosse genérica para múltiplos usos, extrair dados de uma planilha, banco de dados, formulário, chatbot.
"""
#TODO Construir método abstrato de cálculo.
class Aposentadoria(ABC):   #Classe não instanciada.
# Padrões de contagem que se repetem em vários tipos de aposentadoria.
    min_tempo_contribuicao = 25
    min_servico_publico = 15
    min_cargo = 5
#Parâmetros principais para avaliação e cálculo de aposentadoria. Vão ser mais importantes quando for feito o Método de cálculo.
    def __init__(self, **kwargs):
        self.sexo = kwargs.get('sexo', '').upper()
        self.idade = int(kwargs.get('idade', 0))
        self.tempo_contribuicao = int(kwargs.get('tempo_contribuicao', 0))
        self.tempo_servico_publico = int(kwargs.get('tempo_servico_publico', 0))
        self.tempo_cargo = int(kwargs.get('tempo_cargo', 0))
        self.dados_extras = kwargs

    #Encapsulamento 
    @property
    def sexo(self):
        return self._sexo

    @sexo.setter
    def sexo(self, valor):
        valor = str(valor).strip().upper()
        if valor not in('M', 'F'):
            raise ValueError("Sexo deve ser M ou F.")
        self._sexo = valor

    @property
    def idade(self):
        return self._idade

    @idade.setter
    def idade(self, valor):
        valor = int(valor)
        if valor < 0:
            raise ValueError("Idade não pode ser negativa.")
        self._idade = valor

    @property
    def tempo_contribuicao(self)
        return self._tempo_contribuicao

    @tempo_contribuicao.setter
    def tempo_contribuicao(self, valor):
        valor = int(valor)
        if valor < 0:
            raise ValueError("Tempo de contribuição não pode ser negativo.")
        self._tempo_contribuicao = valor

    @property
    def tempo_servico_publico(self):
        return self._tempo_servico_publico

    @tempo_servico_publico.setter
    def tempo_servico_publico(self, valor):
        valor = int(valor)
        if valor < 0:
            raise ValueError("Tempo de serviço público não pode ser negativo.")
        self._tempo_servico_publico = valor

    @property
    def tempo_cargo(self):
        return self._tempo_cargo

    @tempo_cargo.setter
    def tempo_cargo(self, valor):
        valor = int(valor)
        if valor < 0:
            raise ValueError("Tempo no cargo não pode ser negativo.")
        self._tempo_cargo = valor


        
# Class method e abstract method para atribuição de classes aos objetos de acordo com os requisitos.
    @classmethod
    @abstractmethod
    def checar_tipo(cls, **kwargs):
        pass
    
    @classmethod
    def coeficiente_redutor(cls, **kwargs):
        return 1
# Coeficiente redutor aplicado somente no caso de Aposentadoria Compulsória, com contribuição menor que 20 anos. Definida na classe Compulsoria(Aposentadoria)
    @classmethod
    def calcular_proventos(cls, **kwargs):
        tempo_contribuicao = int(kwargs.get('tempo_contribuicao', 0))
        basecalculo = 0.60
        anos_excedentes = max(0, tempo_contribuicao - 20)
        bonus = anos_excedentes * 0.02
        coeficiente = (basecalculo + bonus)*cls.coeficiente_redutor(**kwargs)
        return coeficiente
"""
#Calculo geral baseado na lei: (60% + 02% por ano que passar de 20 anos) x (100% da média das contribuições desde 1994)

"""
"""
    # Aposentadoria Voluntária - Padrão típico de aposentadoria baseado em Idade, Tempo de contribuição, tempo de serviço público e tempo no cargo.
"""
class Voluntaria(Aposentadoria):
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        
    @classmethod
    
    def checar_tipo(cls,**kwargs):
        sexo = kwargs.get('sexo', '').upper()
        idade = int(kwargs.get('idade', 0))
        tempo_contribuicao = int(kwargs.get('tempo_contribuicao', 0))
        tempo_servico_publico = int(kwargs.get('tempo_servico_publico', 0))
        tempo_cargo = int(kwargs.get('tempo_cargo', 0))
        tempo_magisterio = int(kwargs.get('tempo_magisterio', 0)) #Requisito extra, modificador de Idade mínima. 
        
        idade_minima = 65
        if sexo.upper() == 'F':
            idade_minima = 60
        elif sexo.upper() != 'M':
            return False
        
        if tempo_magisterio >= 25: #Redução de 5 anos de idade mínima caso cumpra o tempo de contribuição em magistério.
            idade_minima -= 5
        
        return (idade >= idade_minima and 
                tempo_contribuicao >= cls.min_tempo_contribuicao and 
                tempo_servico_publico >= cls.min_servico_publico and 
                tempo_cargo >= cls.min_cargo)
        

    
class Especial(Aposentadoria):
        def __init__(self,  **kwargs):
            super().__init__(**kwargs)
            
        @classmethod      
        
        def checar_tipo(cls,**kwargs):
            especial = kwargs.get('especial', '').upper()
            sexo = kwargs.get('sexo', '').upper()
            idade = int(kwargs.get('idade', 0))
            tempo_contribuicao = int(kwargs.get('tempo_contribuicao', 0))
            tempo_servico_publico = int(kwargs.get('tempo_servico_publico', 0))
            tempo_cargo = int(kwargs.get('tempo_cargo', 0))
            tempo_exposicao = int(kwargs.get('exposicao', 0))
            
            idade_minima = 60
            if sexo.upper() == 'F':
                idade_minima = 57
            elif sexo.upper() != 'M':
                return False
            return (especial == 'S' and idade >= idade_minima and 
                    tempo_contribuicao >= cls.min_tempo_contribuicao and 
                    tempo_servico_publico >= cls.min_servico_publico and 
                    tempo_cargo >= cls.min_cargo and
                    tempo_exposicao >= 25)
        
class Deficiencia(Aposentadoria):
        def __init__(self, modificador=None, **kwargs):
            sexo = kwargs.get('sexo', '').upper()
            self.modificador = modificador or self.__class__.modificador_tempo(sexo)
            super().__init__(**kwargs)
            
        @classmethod
        
        def modificador_tempo(cls, sexo):
            return -10

        @classmethod      
        
        def checar_tipo(cls,**kwargs):
            deficiencia = kwargs.get('deficiencia', '').upper()
            sexo = kwargs.get('sexo', '').upper()
            idade = int(kwargs.get('idade', 0))
            tempo_contribuicao = int(kwargs.get('tempo_contribuicao', 0))
            tempo_servico_publico = int(kwargs.get('tempo_servico_publico', 0))
            tempo_cargo = int(kwargs.get('tempo_cargo', 0))
            grau_deficiencia_raw = kwargs.get('grau_deficiencia', '')
            grau_informado = str(grau_deficiencia_raw or "").strip().upper()
            
            if grau_informado in ("0", "NONE"):
                grau_informado = ""
                
            graudaclasse = cls.__name__.replace('Deficiencia', '').upper()
            
            if graudaclasse == "":
                valida_grau = True
                idade_minima = 60 if sexo == 'M' else 55
            else:
                valida_grau = (grau_informado == graudaclasse)
                idade_minima = 0
                
            if sexo not in ['M', 'F']:
                return False
                        
            return (deficiencia == 'S' and valida_grau and idade >= idade_minima and 
                    tempo_contribuicao >= (cls.min_tempo_contribuicao + cls.modificador_tempo(sexo)) and 
                    tempo_servico_publico >= cls.min_servico_publico and 
                    tempo_cargo >= cls.min_cargo)
            
class DeficienciaGrave(Deficiencia):
    @classmethod
    def modificador_tempo(cls, sexo):
        return -5 if sexo == 'F' else 0

class DeficienciaModerada(Deficiencia):
    @classmethod
    def modificador_tempo(cls, sexo):
        return -1 if sexo == 'F' else 4

class DeficienciaLeve(Deficiencia):
    @classmethod
    def modificador_tempo(cls, sexo ):
        return 3 if sexo == 'F' else 8
    
class Compulsoria(Aposentadoria):
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)    
        
    @classmethod
    def checar_tipo(cls, **kwargs):
        idade = int(kwargs.get('idade', 0))
        return idade >= 75
    
    @classmethod
    def coeficiente_redutor(cls,**kwargs):
        tempo_contribuicao = int(kwargs.get('tempo_contribuicao', 0))
        if tempo_contribuicao < 20:
            return max(1, tempo_contribuicao/20)
        return 1
    
class IncapacidadePermanente(Aposentadoria):
    @classmethod
    def checar_tipo(cls, **kwargs):
        incapacidade_permanente = kwargs.get('incapacidade_permanente', '').upper()
        return incapacidade_permanente == 'S'
    
    @classmethod
    def calcular_proventos(cls, **kwargs):
        return 1
    
class AcidentedeTrabalho(IncapacidadePermanente):
    def checar_tipo(cls, **kwargs):
        incapacidade_permanente = kwargs.get('incapacidade_permanente', '').upper()
        acidente_de_trabalho = kwargs.get('acidente_de_trabalho', '').upper()
        return incapacidade_permanente == 'S' and acidente_de_trabalho == 'S'
    
    @classmethod
    def calcular_proventos(cls, **kwargs):
        return 0.8
        
    
    
    
    
