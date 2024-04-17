#pip install ibge-parser

import string
import ibgeparser
from pandas import *
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

def ibge_cnae(path,name,i):
    
    file = path + name
    CNAE_CSV = pd.DataFrame(pd.read_excel(file))

    dict = {"CLASSIFICAÇÃO NACIONAL DE ATIVIDADES ECONÔMICAS DOMICILIAR 2.0 - CNAE-DOMICILIAR 2.0": "CNAE_GrandeArea","Unnamed: 1":"CNAE_Area", "Unnamed: 2":"CNAE_Cod", "Unnamed: 3":"CNAE_Desc", }
    CNAE_CSV.rename(columns=dict,inplace=True)

    #### Substituindo todos os nulos(NAN) por vazio
    CNAE_CSV.fillna('', inplace = True)
    
    CNAE_CSV.to_csv(path + 'CNAE_CSV.csv')
    return CNAE_CSV

def ibge_cbo(path,name,i):   
    #...
    file = path + name
    CBO_CSV = pd.DataFrame(pd.read_excel(file))
  
    dict = {"CLASSIFICAÇÃO DE OCUPAÇÕES PARA PESQUISAS DOMICILIARES  - COD": "Cod_CBO","Unnamed: 1":"Nome_CBO", }
    CBO_CSV.rename(columns=dict,inplace=True)

    #limpando dados nulos das colunas
    CBO_CSV = CBO_CSV.dropna(subset=["Cod_CBO"])

    # drop the 'CBO-Domiciliar' column
    CBO_CSV = CBO_CSV.drop(columns=['Unnamed: 2'])

    # Removendo a primeira linha ...
    CBO_CSV = CBO_CSV.drop(CBO_CSV.iloc[0:1].index)
     
    CBO_CSV['Cod_CBO'] = CBO_CSV['Cod_CBO'].astype('str')
    CBO_CSV.to_csv(path +'CBO_CSV.csv')
    return CBO_CSV


def ibge_cursos(path,name,i):   
    #...
    file = path + name
    Curso_CSV = pd.DataFrame(pd.read_excel(file))
    
    dict = {"Áreas gerais, específicas e detalhadas de formação dos cursos de nível superior": "Cod_Curso", "Unnamed: 1":"Nome_Curso",}
    Curso_CSV.rename(columns=dict,inplace=True)

    ##limpando dados nulos das colunas
    Curso_CSV = Curso_CSV.dropna(subset=["Cod_Curso"])

    ## drop the 'CBO-Domiciliar' column
    Curso_CSV = Curso_CSV.drop(columns=['Unnamed: 2'])

    Curso_CSV['Cod_Curso'] = Curso_CSV['Cod_Curso'].astype('str')
    Curso_CSV.to_csv(path + 'Curso_CSV.csv')
    return Curso_CSV

def ibge_qtdadeCursos(path,name,i,path1,name1): 

    file = path + name
    CURSOS = pd.read_csv(file, dtype ='str')
    file1 = path1 + name1
    Brasil = pd.read_csv(file1)

    CURSOS = CURSOS.drop(columns=['Unnamed: 0'])

    Cursos_Censo = Brasil.Curso_Superior_Graduação_Código

    Cursos_Censo_unique = Cursos_Censo.unique()
   
    CURSO_NUM  = []
    CURSO_NOME = []
    for l in range(len(Cursos_Censo_unique)):
        #if(l==1):
        #   break
        for i, j in CURSOS.iterrows():
            #print(CURSOS.Cod_Curso[i])
            if(CURSOS.Cod_Curso[i]== str(Cursos_Censo_unique[l])):
                #print(Cursos_Censo_unique[l])
                #print('CURSOS.Cod_Curso[i]: ', CURSOS.Cod_Curso[i] + " - CURSOS.Nome_Curso[i]: ", CURSOS.Nome_Curso[i])
                CURSO_NUM.append(CURSOS.Cod_Curso[i])
                CURSO_NOME.append(CURSOS.Nome_Curso[i])

    Cursos_Censo=[]
    for i in range(len(CURSO_NUM)):
        tupla=(CURSO_NUM[i],CURSO_NOME[i])
        Cursos_Censo.append(tupla)
    #...
    CursosCenso = pd.DataFrame(Cursos_Censo)
    #Curso_Cbo_dir_curso_cbos.shape
    nomes = {0:"curso_num",
             1:"curso_nome",
            }
    CursosCenso.rename(columns=nomes,inplace=True)
    CursosCenso = CursosCenso.sort_values(by=['curso_num'])

    index_names = CursosCenso[ CursosCenso['curso_nome'] == 'NÃO SABE E SUPERIOR NÃO ESPECIFICADO' ].index
    CursosCenso.drop(index_names, inplace = True)
    #print(len(CursosCenso))
    return len(CursosCenso)
'''
def ibge_qtdadeCursos_graduados(path,name,i,path1,name1): 
    return
def ibge_qtdadeCursos_recenseados(path,name,i,path1,name1): 
    return
def ibge_qtdadeCursos_recenseados_feminino(path,name,i,path1,name1): 
    return
def ibge_qtdadeCursos_recenseados_masculino(path,name,i,path1,name1): 
    return

def ibge_qtdadeProfissoes():
    return
def ibge_qtdadeProfissoes_recenseados():
    return
def ibge_qtdadeProfissoes_recenseados_feminino():
    return
def ibge_qtdadeProfissoes_recenseados_masculino():
    return

'''
