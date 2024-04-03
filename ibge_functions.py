pip install ibge-parser

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
    for i in range(len(estados_ac)):
        ibgeparser.obter_dados_ibge(ano_ac, estados_ac[i], modalidades_ac)
        ibgeparser.obter_especificacao_coluna('palavra-chave', modalidades_ac)
    return

def Filtrar_Dados_Censo(name):

    for i in range(len(name)):
        X = pd.read_csv(name[i],usecols=["V6036", "V6400", "V6352", "V6354", "V6356", "V6461",  "V6471", "V6462", "V6472","V6511","V6514","V0601","V0656"],sep=",")    
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
        path = '/ibge-2010/processados/'
        name_path = name_path[0] + path + "_clean_QtdadeSal_Graduados_NaoGraduados.csv"
        X.to_csv(name_path)

    return X