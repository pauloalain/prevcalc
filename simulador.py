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
# Class method e abstract method para atribuição de classes aos objetos de acordo com os requisitos.
    @classmethod
    @abstractmethod
    def checar_tipo(cls, **kwargs):
        pass
    
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
    
def simulador_aposentadoria():
    print("=== Simulador de Aposentadoria ===")
    
    # Coleta de dados básicos
    dados = {
        'sexo': input("Sexo (M/F): ").strip().upper(),
        'idade': int(input("Idade: ") or 0),
        'tempo_contribuicao': int(input("Tempo de Contribuição (anos): ") or 0),
        'tempo_servico_publico': int(input("Tempo de Serviço Público (anos): ") or 0),
        'tempo_cargo': int(input("Tempo no Cargo Atual (anos): ") or 0),
    }

    # Pergunta sobre condições específicas
    print("\n--- Condições Especiais ---")
    dados['deficiencia'] = input("Possui deficiência? (S/N): ").strip().upper()
    if dados['deficiencia'] == 'S':
        dados['grau_deficiencia'] = input("Grau (GRAVE, MODERADA, LEVE ou deixe em branco para Idade): ").strip().upper()
    
    dados['especial'] = input("Trabalha sob exposição a agentes nocivos? (S/N): ").strip().upper()
    if dados['especial'] == 'S':
        dados['exposicao'] = int(input("Tempo de exposição (anos): ") or 0)
        
    dados['tempo_magisterio'] = int(input("Tempo em Magistério (se não houver, digite 0): ") or 0)

    # Lista de classes para testar
    classes_para_testar = [
        ("Voluntária Comum", Voluntaria),
        ("Especial (Agentes Nocivos)", Especial),
        ("PCD Grave", DeficienciaGrave),
        ("PCD Moderada", DeficienciaModerada),
        ("PCD Leve", DeficienciaLeve),
        ("PCD por Idade", Deficiencia)
    ]

    print("\n=== Resultado da Análise ===")
    concedida = False
    
    for nome, classe in classes_para_testar:
        if classe.checar_tipo(**dados):
            # Instancia para mostrar os detalhes
            obj = classe(**dados)
            mod_texto = f" (Modificador de tempo: {obj.modificador})" if hasattr(obj, 'modificador') else ""
            
            print(f"[✅] Aposentadoria {nome} CONCEDIDA!{mod_texto}")
            concedida = True
    
    if not concedida:
        print("[❌] Infelizmente você ainda não cumpre os requisitos para nenhum dos tipos testados.")

# Executa o simulador
if __name__ == "__main__":
    simulador_aposentadoria()


    