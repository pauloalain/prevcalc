# Classe abstrata Aposentadoria 
from abc import ABC, abstractmethod

#Classe abstrata define principais padrões de requisitos para aposentadoria e **kwargs permite outros parâmetros para classes filhas. Contrato flexível, mas classe pai adianta principais padrões.

class Aposentadoria(ABC):   
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
        self.tempo_cargo = int(kwargs.get('tempo_cargo'))
        self.dados_extras = kwargs

    @classmethod
    @abstractmethod
    def checar_tipo(cls, **kwargs):
        pass
    
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
        tempo_magisterio = int(kwargs.get('tempo_magisterio', 0))
        
        idade_minima = 65
        if sexo.upper() == 'F':
            idade_minima = 60
        elif sexo.upper() != 'M':
            return False
        
        if tempo_magisterio >= 25:
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
            return (idade >= idade_minima and 
                    tempo_contribuicao >= cls.min_tempo_contribuicao and 
                    tempo_servico_publico >= cls.min_servico_publico and 
                    tempo_cargo >= cls.min_cargo and
                    tempo_exposicao >= 25)
        
class Deficiencia(Aposentadoria):
        def __init__(self,  **kwargs):
            super().__init__(**kwargs)
            
        @classmethod      
        
        def checar_tipo(cls,**kwargs):
            sexo = kwargs.get('sexo', '').upper()
            idade = int(kwargs.get('idade', 0))
            tempo_contribuicao = int(kwargs.get('tempo_contribuicao', 0))
            tempo_servico_publico = int(kwargs.get('tempo_servico_publico', 0))
            tempo_cargo = int(kwargs.get('tempo_cargo', 0))

# TODO: CRIAR A VARIÁVEL DEFICIENCIA, FAZER AS SUBCLASSES


            grau_deficiencia = str(kwargs.get('grau_deficiencia', '').upper())
               
               
            idade_minima = 60
            if sexo == 'F':
                idade_minima = 55
            elif sexo != 'M':
                return False
            
            return (grau_deficiencia == cls.__name__.replace('Deficiencia', '').upper() and idade >= idade_minima and 
                    tempo_contribuicao >= cls.min_tempo_contribuicao - 10 and 
                    tempo_servico_publico >= cls.min_servico_publico and 
                    tempo_cargo >= cls.min_cargo)
            
class DeficienciaGrave(Deficiencia):
    raise NotImplementedError