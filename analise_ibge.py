
#pip install ibge-parser
#pip install ibge-parser



# inclua todos os demais imports aqui
import argparse
import sys
import os
import pandas as pd 
import numpy as np

import ibgeparser
import pandas as pd
from pandas import DataFrame
import numpy as np

# import da classe principal
from ibgeparser.microdados import Microdados
# import dos enums para facilitar as buscas
from ibgeparser.enums import Anos, Estados, Modalidades

import original.ibge_functions

# Esse arquivo não pode conter código que não seja chamada de funções e verificação de parâmetros

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fase', type=int, help='Indica a fase do fluxo para começar a execução')
args = parser.parse_args()

if args.fase is None:
    fase = 10
else:
    fase = args.fase

# Fase 0: Download dos dados do IBGE da web
#if fase >= 0:
if fase == 0:
    
    # Leia os dados do IBGE
    ano_ac = Anos.DEZ
    modalidades_ac = [Modalidades.PESSOAS]
    estados = [Estados.ACRE], [Estados.AMAPA], [Estados.AMAZONAS]
    #estados_ac = [Estados.ACRE], [Estados.AMAPA], [Estados.AMAZONAS], [Estados.PARA],[Estados.RONDONIA], [Estados.RORAIMA],  [Estados.TOCANTINS], [Estados.ALAGOAS], [Estados.BAHIA], [Estados.CEARA],  [Estados.MARANHAO], [Estados.PARAIBA], [Estados.PERNAMBUCO], [Estados.RIO_GRANDE_DO_NORTE], [Estados.SERGIPE], [Estados.ESPIRITO_SANTO], [Estados.MINAS_GERAIS], [Estados.RIO_DE_JANEIRO], [Estados.SAO_PAULO_SP1], [Estados.SAO_PAULO_SP2_RM],  [Estados.PARANA], [Estados.RIO_GRANDE_DO_SUL], [Estados.SANTA_CATARINA], [Estados.DISTRITO_FEDERAL], [Estados.GOIAS], [Estados.MATO_GROSSO], [Estados.MATO_GROSSO_DO_SUL]
    
    for i in range(len(estados)):
        estados_ac = estados[i]
        original.ibge_functions.function_obterdados_especificacao_coluna(ano_ac, estados_ac, modalidades_ac)


# Fase 1: Filtrar somente os dados relevantes. Aqui significa que 
# você precisa filtrar todos os dados que possam ser utilizados no futuro.
#if fase >= 1:
if fase >= 1:
    path = '/home/essantos/Downloads/ibge-2010/original/'
    #name = ['Amostra_Pessoas_41_PR.csv','Amostra_Pessoas_42_SC.csv','Amostra_Pessoas_43_RS.csv',
    #'Amostra_Pessoas_32_ES.csv','Amostra_Pessoas_33_RJ.csv','Amostra_Pessoas_35_RMSP_SP2_RM.csv','Amostra_Pessoas_35_outras_SP1.csv', 'Amostra_Pessoas_31_MG.csv',    
    #'Amostra_Pessoas_50_MS.csv',  'Amostra_Pessoas_51_MT.csv',  'Amostra_Pessoas_52_GO.csv', 'Amostra_Pessoas_53_DF.csv', 
    #'Amostra_Pessoas_11_RO.csv', 'Amostra_Pessoas_12_AC.csv', 'Amostra_Pessoas_13_AM.csv', 'Amostra_Pessoas_14_RR.csv','Amostra_Pessoas_15_PA.csv','Amostra_Pessoas_16_AP.csv','Amostra_Pessoas_17_TO.csv',    
    #'Amostra_Pessoas_29_BA.csv','Amostra_Pessoas_21_MA.csv',  'Amostra_Pessoas_23_CE.csv',  'Amostra_Pessoas_24_RN.csv','Amostra_Pessoas_25_PB.csv',  'Amostra_Pessoas_26_PE.csv', 'Amostra_Pessoas_27_AL.csv',  'Amostra_Pessoas_28_SE.csv']
    names = 'Amostra_Pessoas_12_AC.csv', 'Amostra_Pessoas_16_AP.csv', 'Amostra_Pessoas_13_AM.csv'
    for i in range(len(names)):
       name = names[i]
       original.ibge_functions.Filtrar_Dados_Censo(path,str(name))
    pass

# Fase 2: Limpeza dos dados. Agora começa a processar algo mais complexo desde que seja definitivo
if fase >= 2:
   pass

# Fase 10: Essa é a primeira fase que você faz no dia a dia. Aqui você começa a fazer a análise dos dados
if fase >= 10:
    pass



# Fase 99: Aqui você pode explorar coisas novas que não afetam os dados anteriores.
