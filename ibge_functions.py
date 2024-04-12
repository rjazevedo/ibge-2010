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


def ibge_download():
    # Leia os dados do IBGE
    ano_ac = Anos.DEZ
    modalidades_ac = [Modalidades.PESSOAS]
    estados = ibge_variable.estados()

    for i in range(len(estados)):
        estados_ac = estados[i]
        #original.ibge_functions.function_obterdados_especificacao_coluna(ano_ac, estados_ac, modalidades_ac)
        ibge_functions_preprocessing.function_obterdados_especificacao_coluna(ano_ac, estados_ac, modalidades_ac)
    return

def ibge_filter():
    path  = ibge_variable.paths(1,1)
    names = ibge_variable.names(1,1)
    for i in range(len(names)):
       namess = len(names[i])
       for j in range(namess):
           name = str(names[i][j])
           ibge_functions_preprocessing.Filtrar_Dados_Censo(path[i],name,i)           
    return

def ibge_Graduados_NaoGraduados():
    path  = ibge_variable.paths(2,2)
    names = ibge_variable.names(2,1)
    for i in range(len(names)):
        namess = len(names[i])
        for j in range(namess):
            name = str(names[i][j])
            ibge_functions_preprocessing.Limpeza_Arquivo_Censo_Graduados_NaoGraduados_1_2(path[i],name,i)    
    return

def ibge_Pivot_Feminino():
    gender = "F"
    path = ibge_variable.paths(2,3)
    names = ibge_variable.names(2,2)
    for i in range(len(names)):
        namess = len(names[i])
        for j in range(namess):
            name = str(names[i][j])
            ibge_functions_preprocessing.Pivot_Table_Censo(path[i],name,gender,i)      
    return

def ibge_Pivot_Masculino():
    gender = "M"
    path = ibge_variable.paths(2,3)
    names = ibge_variable.names(2,2)
    for i in range(len(names)):
        namess = len(names[i])
        for j in range(namess):
            name = str(names[i][j])
            ibge_functions_preprocessing.Pivot_Table_Censo(path[i],name,gender,i)
            #print(path[i],name,gender,i)
    return

def ibge_Pivot_Geral():
    gender = "G"
    path = ibge_variable.paths(2,3)
    names = ibge_variable.names(2,2)
    for i in range(len(names)):
        namess = len(names[i])
        for j in range(namess):
            name = str(names[i][j])
            ibge_functions_preprocessing.Pivot_Table_Censo(path[i],name,gender,i)
           
    return

def ibge_PivotTableFinal():
    pivotfinal = []
    estado = ['Sul','Centro_Oeste','Norte','Nordeste','Sudeste']
    gender = [1,2,3]
    linha = 0
    path = ibge_variable.paths(2,7)
    name = ibge_variable.names(2,3)
    for x in range(len(estado)):
         for i in range(len(path[x])):            
             coluna = 0
             for j in range(len(name[i])):                
                 pivotfinal.append(ibge_functions_preprocessing.SomaPivotTable(str(path[x][i]),str(name[linha][coluna]),i))
                 coluna = coluna + 1
             ibge_functions_preprocessing.Reduzir(pivotfinal,estado[x],gender[i])                  
             linha = linha +1    
    return

def ibge_PivotTableFinalB():
    pivotfinal = []
    estado = ['Brasil']
    gender = [1,2,3]
    path = ibge_variable.paths(2,12)
    name = ibge_variable.names(2,4)
    for x in range(len(gender)):
         for i in range(5):            
             file = str(path[x])+ str(name[x][i])
             X = pd.read_csv(file, sep=",")  
             pivotfinal.append(X)
         ibge_functions_preprocessing.Reduzir(pivotfinal,estado[0],gender[x])                  
    return

def ibge_Graduados():
     path = ibge_variable.paths(2,3)
     names = ibge_variable.names(2,2)
     for i in range(len(names)):
         namess = len(names[i])
         for j in range(namess):
             name = str(names[i][j])
             ibge_functions_preprocessing.Limpeza_Arquivo_Censo_Graduados_2(path[i],name,i)    
   
     return

def ibge_JuntarCSVs():
     estados = ['Sul', 'Centro_Oeste','Norte','Nordeste','Sudeste','Brasil']   
     opcao = ['Graduados', 'Não-Graduados']
     path = ibge_variable.paths(2,10)
     coluna = 0
     dir = os.getcwd()
     for i in range(len(opcao)):   
        print("...")
        for j in range(len(estados)):    
             ibge_functions_preprocessing.JuntarCSVs(path[j][coluna],estados[j],opcao[i],dir)    
             #print(path[j][coluna],estados[j],opcao[i],dir)          
        coluna = coluna + 1    
     return
