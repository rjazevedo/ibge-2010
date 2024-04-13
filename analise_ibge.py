
#pip install ibge-parser
#pip install ibge-parser

# inclua todos os demais imports aqui
import argparse
import sys
import os
import numpy as np
import ibgeparser
import pandas as pd
from pandas import DataFrame
import numpy as np
import glob
from functools import reduce
#import da classe principal
from ibgeparser.microdados import Microdados
#import dos enums para facilitar as buscas
from ibgeparser.enums import Anos, Estados, Modalidades
#import original.ibge_functions
import ibge_functions_full
import ibge_variable_full
import ibge_functions_preprocessing_full

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
   ibge_functions_full.ibge_download() 
   pass    

# Fase 1: Filtrar somente os dados relevantes. Aqui significa que 
# você precisa filtrar todos os dados que possam ser utilizados no futuro.
#if fase >= 1:
if fase == 1:
   ibge_functions_full.ibge_filter()
   pass

# Fase 2: Limpeza dos dados. Agora começa a processar algo mais complexo desde que seja definitivo
# Pré-Processamento
#if fase >= 2:
if fase == 2:
   
   ibge_functions_full.ibge_Graduados_NaoGraduados()

   ibge_functions_full.ibge_Pivot_Feminino()

   ibge_functions_full.ibge_Pivot_Masculino()

   ibge_functions_full.ibge_Pivot_Geral()        

   ibge_functions_full.ibge_PivotTableFinal()

   ibge_functions_full.ibge_Graduados()
 
   ibge_functions_full.ibge_JuntarCSVs()      
pass      

     


# Fase 10: Essa é a primeira fase que você faz no dia a dia. Aqui você começa a fazer a análise dos dados
# Fase 10: Análise Descritiva ... ...
#if fase >= 10:
if fase == 10:
    pass

# Fase 11: Análise Exploratória ...
if fase == 20:
    pass

# Fase 12: Resultados da Análise ...
if fase == 30: 
    pass

# Fase 99: Aqui você pode explorar coisas novas que não afetam os dados anteriores.
#if fase >= 99:
#if fase == 99:
#    pass
