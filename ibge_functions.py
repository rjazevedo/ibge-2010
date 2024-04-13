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
import ibge_variable_full
import ibge_functions_preprocessing_full


def ibge_download():
    # Leia os dados do IBGE
    ano_ac = Anos.DEZ
    modalidades_ac = [Modalidades.PESSOAS]
    estados = ibge_variable_full.estados()

    for i in range(len(estados)):
        estados_ac = estados[i]
        #original.ibge_functions.function_obterdados_especificacao_coluna(ano_ac, estados_ac, modalidades_ac)
        ibge_functions_preprocessing_full.function_obterdados_especificacao_coluna(ano_ac, estados_ac, modalidades_ac)
    return

def ibge_filter():
    path  = ibge_variable_full.paths(1,1)
    names = ibge_variable_full.names(1,1)        
    for j in range(len(names)):          
        ibge_functions_preprocessing_full.Filtrar_Dados_Censo(path[0],names[j],0)           
    return

def ibge_Graduados_NaoGraduados():
    path  = ibge_variable_full.paths(2,2)
    names = ibge_variable_full.names(2,1)
    for j in range(len(names)):      
        ibge_functions_preprocessing_full.Limpeza_Arquivo_Censo_Graduados_NaoGraduados_1_2(path[0],names[j],0)
    return

def ibge_Pivot_Feminino():
    gender = "F"
    path = ibge_variable_full.paths(2,3)
    names = ibge_variable_full.names(2,2)
    for i in range(len(names)):
        ibge_functions_preprocessing_full.Pivot_Table_Censo(path[0],names[i],gender,i)
    return

def ibge_Pivot_Masculino():
    gender = "M"
    path = ibge_variable_full.paths(2,3)
    names = ibge_variable_full.names(2,2)
    for i in range(len(names)):
        ibge_functions_preprocessing_full.Pivot_Table_Censo(path[0],names[i],gender,i)
    return

def ibge_Pivot_Geral():
    gender = "G"
    path = ibge_variable_full.paths(2,3)
    names = ibge_variable_full.names(2,2)
    for i in range(len(names)):
        ibge_functions_preprocessing_full.Pivot_Table_Censo(path[0],names[i],gender,i)
    return

def ibge_PivotTableFinal():
    pivotfinal = []
    estado = ['Brasil']
    gender = [1,2,3]
    path = ibge_variable_full.paths(2,7)
    name = ibge_variable_full.names(2,3)
    for i in range(len(gender)):
        for x in range(len(name[i])):
            pivotfinal.append(ibge_functions_preprocessing_full.SomaPivotTable(path[i],name[i][x],i))
        ibge_functions_preprocessing_full.Reduzir(pivotfinal,estado[0],gender[i])   
    return

def ibge_Graduados():
     path = ibge_variable_full.paths(2,3)
     names = ibge_variable_full.names(2,2)
     for i in range(len(names)):
     #for state_name in names:
         ibge_functions_preprocessing_full.Limpeza_Arquivo_Censo_Graduados_2(path[0],names[i],0)   
     return

def ibge_JuntarCSVs():
     opcao = ['Graduados', 'Não-Graduados']
     path = ibge_variable_full.paths(2,10)
     dir = os.getcwd()
     for i in range(len(opcao)):   
         ibge_functions_preprocessing_full.JuntarCSVs(path[i],opcao[i],dir)  
     return
