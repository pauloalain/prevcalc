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
        self.tempo_cargo = int(kwargs.get('tempo_cargo', 0))
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
        redutor_especifico = 0
        def __init__(self,  **kwargs):
            super().__init__(**kwargs)
            
        @classmethod      
        
        def checar_tipo(cls,**kwargs):
            deficiencia = kwargs.get('deficiencia', '').upper()
            sexo = kwargs.get('sexo', '').upper()
            idade = int(kwargs.get('idade', 0))
            tempo_contribuicao = int(kwargs.get('tempo_contribuicao', 0))
            tempo_servico_publico = int(kwargs.get('tempo_servico_publico', 0))
            tempo_cargo = int(kwargs.get('tempo_cargo', 0))

# TODO: CRIAR A VARIÁVEL DEFICIENCIA, FAZER AS SUBCLASSES
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
                    tempo_contribuicao >= cls.min_tempo_contribuicao - 10 and 
                    tempo_servico_publico >= cls.min_servico_publico and 
                    tempo_cargo >= cls.min_cargo)
            
class DeficienciaGrave(Deficiencia):
        @classmethod      

        def checar_tipo(cls,**kwargs):
            deficiencia = kwargs.get('deficiencia', '').upper()
            sexo = kwargs.get('sexo', '').upper()
            tempo_contribuicao = int(kwargs.get('tempo_contribuicao', 0))
            tempo_servico_publico = int(kwargs.get('tempo_servico_publico', 0))
            tempo_cargo = int(kwargs.get('tempo_cargo', 0))
            
            redutor = 5 if sexo =='F' else 0
             
            return deficiencia == S and tempo_contribuicao >= cls.min_tempo_contribuicao - redutor and tempo_servico_publico >= cls.min_servico_publico and tempo_cargo >= cls.min_cargo
    

class DeficienciaModerada(Deficiencia):
    pass

class DeficienciaLeve(Deficiencia):
    pass