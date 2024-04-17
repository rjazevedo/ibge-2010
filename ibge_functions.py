#pip install ibge-parser

import string
import ibgeparser
import pandas as pd
from pandas import DataFrame
import numpy as np
import os
import glob
from functools import reduce
from os import chmod
from copy import deepcopy
import subprocess
import glob
# import da classe principal
from ibgeparser.microdados import Microdados
# import dos enums para facilitar as buscas
from ibgeparser.enums import Anos, Estados, Modalidades
import ibge_variable
import ibge_functions_preprocessing
import ibge_functions_descriptiveanalysis
import ibge_functions_results
import logging

# Fase 0: Download dos dados do IBGE da web
def ibge_download():
    # Leia os dados do IBGE
    logging.info("Fazendo download dos dados do IBGE")    
    ano_ac = Anos.DEZ
    modalidades_ac = [Modalidades.PESSOAS]
    estados = ibge_variable.estados()


# Fase 1: Filtrar somente os dados relevantes. Aqui significa que 
# você precisa filtrar todos os dados que possam ser utilizados no futuro.
    for i in range(len(estados)):
        estados_ac = estados[i]
        #original.ibge_functions.function_obterdados_especificacao_coluna(ano_ac, estados_ac, modalidades_ac)
        ibge_functions_preprocessing.function_obterdados_especificacao_coluna(ano_ac, estados_ac, modalidades_ac)
    return

def ibge_filter():
    path  = ibge_variable.paths(1,1)
    names = ibge_variable.names(1,1)        
    for j in range(len(names)):          
        ibge_functions_preprocessing.Filtrar_Dados_Censo(path[0],names[j],0)           
    return

def ibge_Graduados_NaoGraduados():
    path  = ibge_variable.paths(2,2)
    names = ibge_variable.names(2,1)
    for j in range(len(names)):      
        ibge_functions_preprocessing.Limpeza_Arquivo_Censo_Graduados_NaoGraduados_1_2(path[0],names[j],0)
    return

def ibge_Pivot_Feminino():
    gender = "F"
    path = ibge_variable.paths(2,3)
    names = ibge_variable.names(2,2)
    for i in range(len(names)):
        ibge_functions_preprocessing.Pivot_Table_Censo(path[0],names[i],gender,i)
    return

def ibge_Pivot_Masculino():
    gender = "M"
    path = ibge_variable.paths(2,3)
    names = ibge_variable.names(2,2)
    for i in range(len(names)):
        ibge_functions_preprocessing.Pivot_Table_Censo(path[0],names[i],gender,i)
    return

def ibge_Pivot_Geral():
    gender = "G"
    path = ibge_variable.paths(2,3)
    names = ibge_variable.names(2,2)
    for i in range(len(names)):
        ibge_functions_preprocessing.Pivot_Table_Censo(path[0],names[i],gender,i)
    return

def ibge_PivotTableFinal():
    pivotfinal = []
    estado = ['Brasil']
    gender = [1,2,3]
    path = ibge_variable.paths(2,7)
    name = ibge_variable.names(2,3)
    for i in range(len(gender)):
        for x in range(len(name[i])):
            pivotfinal.append(ibge_functions_preprocessing.SomaPivotTable(path[i],name[i][x],i))
        ibge_functions_preprocessing.Reduzir(pivotfinal,estado[0],gender[i])   
    return

def ibge_Graduados():
     path = ibge_variable.paths(2,3)
     names = ibge_variable.names(2,2)
     for i in range(len(names)):
     #for state_name in names:
         ibge_functions_preprocessing.Limpeza_Arquivo_Censo_Graduados_2(path[0],names[i],0)   
     return

def ibge_JuntarCSVs():
     opcao = ['Graduados', 'Não-Graduados']
     path = ibge_variable.paths(2,10)
     dir = os.getcwd()
     for i in range(len(opcao)):   
         ibge_functions_preprocessing.JuntarCSVs(path[i],opcao[i],dir)  
     return


## Fase 10: Essa é a primeira fase que você faz no dia a dia. Aqui você começa a fazer a análise dos dados
# Fase 10: Análise Descritiva ... ...
def ibge_cursos_profissoes():
    
    #Cursos e Profissões do Censo ...
    path = ibge_variable.paths(3,1)
    name = ibge_variable.names(3,1)
    ibge_functions_descriptiveanalysis.ibge_cnae(path[0],name[0],0)

    path = ibge_variable.paths(3,1)
    name = ibge_variable.names(3,1)
    ibge_functions_descriptiveanalysis.ibge_cbo(path[0],name[1],0)

    path = ibge_variable.paths(3,1)
    name = ibge_variable.names(3,1)
    ibge_functions_descriptiveanalysis.ibge_cursos(path[0],name[2],0)

    path = ibge_variable.paths(3,1)
    name = ibge_variable.names(3,2)
    path1 = ibge_variable.paths(3,2)
    name1 = ibge_variable.names(3,3)
    ibge_functions_descriptiveanalysis.ibge_qtdadeCursos(path[0],name[2],0,path1[0],name1[0])

    '''
    ibge_functions_descriptiveanalysis.ibge_qtdadeProfissoes()

    #Cursos e Profissões das pessoas recenseadas ...
    ibge_functions_descriptiveanalysis.ibge_qtdadeCursos_recenseados()
    ibge_functions_descriptiveanalysis.ibge_qtdadeProfissoes_recenseados()

    #Cursos e Profissões associadas ao Gênero Feminino
    ibge_functions_descriptiveanalysis.ibge_qtdadeCursos_recenseados_feminino()
    ibge_functions_descriptiveanalysis.ibge_qtdadeProfissoes_recenseados_feminino()

    #Cursos e Profissões associadas ao Gênero Masculino
    ibge_functions_descriptiveanalysis.ibge_qtdadeCursos_recenseados_masculino()
    ibge_functions_descriptiveanalysis.ibge_qtdadeProfissoes_recenseados_masculino()
    '''
    return

'''
def ibge_relacionamentos_cursos_profissoes():
    return

def ibge_corte_CBO():
    return

def ibge_idas_voltas_cursos_profissoes():
    return

def ibge_trabalho_recenseados():
    return
'''


# Fase 20: Análise Exploratória ...
'''
def Profissoes_Cursos():
    return
'''


# Fase 30: Resultados da Análise ...    
'''
def Genero_Profissoes_Masc_Fem_Grupos():
    ibge_functions_results.Genero_Profissoes_Masc_Fem_Grupo1()
    ibge_functions_results.Genero_Profissoes_Masc_Fem_Grupo2()
    ibge_functions_results.Genero_Profissoes_Masc_Fem_Grupo3()
    return

def Genero_Profissoes_Desequilibradas():
    ibge_functions_results.Genero_Profissoes_Desequilibradas_Deslocamentos()
    ibge_functions_results.Genero_Profissoes_Desequilibradas_Mudanca_Voronoi()
    return

def Genero_Profissoes_Equilibradas():
    ibge_functions_results.Genero_Profissoes_Equilibradas_tabela()
    ibge_functions_results.Genero_Profissoes_Equilibradas_Tab_Sel()
    ibge_functions_results.Genero_Profissoes_Equilibradas_Graf_Sel()
    ibge_functions_results.Genero_Profissoes_Equilibradas_Gen_Idade_Fem()
    ibge_functions_results.Genero_Profissoes_Equilibradas_Gen_Idade_Masc()
    return
'''    
   