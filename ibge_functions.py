#pip install ibge-parser

import string
import ibgeparser
import pandas as pd
from pandas import DataFrame
import numpy as np

# import da classe principal
from ibgeparser.microdados import Microdados
# import dos enums para facilitar as buscas
from ibgeparser.enums import Anos, Estados, Modalidades

#https://colab.research.google.com/drive/1Cv0fw4YmLETOy-HEqRLJvyt9HEo90gkH?authuser=1#scrollTo=hzJqOaQJOruE
def function_obterdados_especificacao_coluna(ano_ac, estados_ac, modalidades_ac):
    # instanciando a classe
    ibgeparser = Microdados()
    # obter dados
    ibgeparser.obter_dados_ibge(ano_ac, estados_ac, modalidades_ac)
    ibgeparser.obter_especificacao_coluna('palavra-chave', modalidades_ac)
    return

def Filtrar_Dados_Censo(path,name):

    file = path + name
    X = pd.read_csv(file,usecols=["V6036", "V6400", "V6352", "V6354", "V6356", "V6461",  "V6471", "V6462", "V6472","V6511","V6514","V0601","V0656"],sep=",")    
    dict = {
            "V6036":"Idade_em_Anos",
            "V6400":"Nível_instrução",
            "V6352":"Curso_Superior_Graduação_Código",
            "V6354":"Curso_Mestrado_Código",
            "V6356":"Curso_Doutorado_Código",
            "V6461":"Ocupação_Código",
            "V6471":"Atividade_Código",
            "V6462":"CBO-Domiciliar",
            "V6472":"CNAE-Domiciliar",
            "V6511":"Valor_rend_bruto_M",
            "V6514":"Qtdade_Salario",
            "V0601":"gênero",
            "V0656":"rendimento_aposentadoria_pensao"
            }
    X.rename(columns=dict,inplace=True)
        
    name_path = name.split(".csv")
    name_path = '/home/essantos/Downloads/ibge-2010/processados/' + name_path[0] + "_Fase1.csv"
    X.to_csv(name_path) 
    return X

def Limpeza_Arquivo_Censo_Graduados_NaoGraduados_1_2(path,name):

    file = path + name
    X = pd.read_csv(file, sep=",")  
    X = X.drop(columns=['Unnamed: 0'])
    
    print("Linhas faltantes:==============================")
    print(X.isnull().sum())

    #removendo quem não tem ocupação
    X = X.dropna(subset=['Ocupação_Código'])
    
    #removendo pessoas com ocupações mal-definidas
    X.drop(X[(X['Ocupação_Código'] <1)].index, inplace=True)
    

    print("Listando os NANs que ainda restam:==============================")
    print(X.isnull().sum())

    #print("Tratando Valores Faltantes - Substituindo todos os nulos(NAN) por zero")
    X.fillna(0, inplace = True)

    #Removendo CBO-Domiciliar
    X = X.drop(columns=['CBO-Domiciliar'])
    
    # removendo que tem graduação, mas o curso superior é igual  a Zero
    X.drop(X[(X['Nível_instrução'] ==4) & (X['Curso_Superior_Graduação_Código'] ==0)].index, inplace=True) ## alterado 23/09/2023 #=============================
   

    name_path = name.split(".csv")
    name_path = '/home/essantos/Downloads/ibge-2010/processados/' + name_path[0] + "_Fase2.csv"
    X.to_csv(name_path) 
    return    