
#pip install ibge-parser

# inclua todos os demais imports aqui
import argparse
import sys
import os
import numpy as np
import ibgeparser
import pandas as pd
from pandas import DataFrame
import glob
from functools import reduce
#import da classe principal
from ibgeparser.microdados import Microdados
#import dos enums para facilitar as buscas
from ibgeparser.enums import Anos, Estados, Modalidades
#import original.ibge_functions
import ibge_functions
import ibge_variable
import ibge_functions_preprocessing
import logging

# Esse arquivo não pode conter código que não seja chamada de funções e verificação de parâmetros
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fase', type=int, help='Indica a fase do fluxo para começar a execução')
args = parser.parse_args()

# Setup do pacote logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if args.fase is None:
     fase = 10
else:
     fase = args.fase

# Fase 0: Download dos dados do IBGE da web
#if fase >= 0:
if fase == 0:
    # for p in ["microdados-ibge/original", "microdados-ibge/processados", "microdados-ibge/graficos"]:
    #   if not os.path.exists(p):
    #       os.makedirs(p)
    for p in ["microdados-ibge/original", "processados", "graficos"]:
      if not os.path.exists(p):
          os.makedirs(p)

    ibge_functions.ibge_download() 

# Fase 1: Filtrar somente os dados relevantes. Aqui significa que 
# você precisa filtrar todos os dados que possam ser utilizados no futuro.
#if fase >= 1:
if fase == 1:
    ibge_functions.ibge_filter()

# Fase 2: Limpeza dos dados. Agora começa a processar algo mais complexo desde que seja definitivo
# Pré-Processamento
#if fase >= 2:
if fase == 2:

    ibge_functions.ibge_Graduados_NaoGraduados()

    ibge_functions.ibge_Pivot_Feminino()

    ibge_functions.ibge_Pivot_Masculino()

    ibge_functions.ibge_Pivot_Geral()          

    ibge_functions.ibge_PivotTableFinal()

    ibge_functions.ibge_Graduados()

    ibge_functions.ibge_JuntarCSVs()        
    
# Fase 10: Essa é a primeira fase que você faz no dia a dia. Aqui você começa a fazer a análise dos dados
# Fase 10: Análise Descritiva ... ...
#if fase >= 10:
if fase == 10:
    ibge_functions.ibge_cursos_profissoes() #https://colab.research.google.com/drive/1_Nx4oOzrgCQvSolh9XG-UgWTQ508Md1M?authuser=1#scrollTo=o9GsbqjctkkL
   
    # ibge_functions.ibge_relacionamentos_cursos_profissoes()

    # ibge_functions.ibge_corte_CBO()

    ibge_functions.ibge_idas_voltas_cursos_profissoes()

    ibge_functions.ibge_trabalho_recenseados()
    pass
    

# Fase 20: Análise Exploratória ...
if fase == 20:
     
    ibge_functions.Profissoes_Cursos()
     
    pass

# Fase 30: Resultados da Análise ...
if fase == 30: 
    ibge_functions.Filtro_Masculino_Feminino() 
    ibge_functions.Ida_Volta_Masculino_Feminino()
    ibge_functions.Tabela_Ida_Volta_Masculino_Feminino()  
    ibge_functions.Profissoes_Cursos_Masculino_Feminino()   
    pass

if fase == 31:
    #QP1
    pass 
if fase == 32:
    #QP2
    pass 
if fase == 33:   
    #  #QP3
    #  ibge_functions.Genero_Profissoes_Masc_Fem()
    #  ibge_functions.Genero_Profissoes_Masc_Fem_Grupos()
    #  ibge_functions.Genero_Profissoes_Desequilibradas()
    #  ibge_functions.Genero_Profissoes_Equilibradas()
    pass
if fase == 34:
    #  #QP4
    #  ibge_functions.Idade_Profissoes_Cursos()
    #  ibge_functions.Idade_Profissoes_Cursos_Grupos()
    #  ibge_functions.Idade_Profissoes_Cursos_Aposentados()
    #  ibge_functions.Idade_Profissoes_Cursos_Administrativos()
    #  ibge_functions.Idade_Profissoes_Cursos_Administrativos_Fem()
    #  ibge_functions.Idade_Profissoes_Cursos_Administrativos_Masc()
    pass

if fase == 35:     
    #  #QP5
    #  ibge_functions.Salario_Grupos()
    #  ibge_functions.Salario_Idade_Grupos()
    #  ibge_functions.Salario_Genero_Grupos()
    #  ibge_functions.Salario_MaxMinMed_Grupos()
    #  ibge_functions.Salario_CBO_Idade_TresProf()
    #  ibge_functions.Salario_Profissoes_Genero()
    #  ibge_functions.Salario_Median_TresProf()
    #  ibge_functions.Salario_Plato_TresProf()
    #  ibge_functions.Salario_Analise_Porcent_IdaVolta()
    pass

# Fase 99: Aqui você pode explorar coisas novas que não afetam os dados anteriores.
#if fase >= 99:
#if fase == 99:
#     pass
