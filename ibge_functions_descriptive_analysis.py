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
import matplotlib.pyplot as plt
import warnings
import sys
import ibge_functions
import logging
import sklearn
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

def ibge_cnae(path,name,i):
    #...
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
    file = os.path.join(path,name)
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
    file = os.path.join(path,name)
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

def ibge_cursos_filter(path,name):   
    #...
    file = os.path.join(path,name)
    cursos = pd.read_csv(file, dtype ='str')
    CURSO = []
    NOME  = []
    for i in range(len(cursos)):
        # print(len(cursos.Cod_Curso[i]),cursos.Cod_Curso[i])
        if len(cursos.Cod_Curso[i]) >=3:
           CURSO.append(cursos.Cod_Curso[i])
           NOME.append(cursos.Nome_Curso[i])
           # print(len(cursos.Cod_Curso[i]),cursos.Cod_Curso[i])
              
    Cursos_Censo=[]
    for i in range(len(CURSO)):
        tupla=(CURSO[i],NOME[i])
        Cursos_Censo.append(tupla)
    #...
    CursosCenso = pd.DataFrame(Cursos_Censo)
    # print(CursosCenso.columns)
    # Curso_Cbo_dir_curso_cbos.shape
    nomes = {0:"curso_num",
             1:"curso_nome",
            }
    CursosCenso.rename(columns=nomes,inplace=True)
    # print(CursosCenso.columns)
    # print(CursosCenso.shape)
    # exit(0)
    CursosCenso = CursosCenso.sort_values(by=['curso_num'])       
    CursosCenso.to_csv(path + 'Curso_Censo.csv')       
    return CursosCenso
    # return 

def ibge_qtdadeCursos(path,name): 
    file = path + name
    CURSOS = pd.read_csv(file, dtype ='str')
           
    CURSOS = CURSOS.drop(columns=['Unnamed: 0'])

    CURSO = []
    for l in range(len(CURSOS)):
        if len(CURSOS.Cod_Curso[l]) >=5:
           CURSO.append(CURSOS.Cod_Curso[l])
        #    print(CURSOS.Cod_Curso[l])
    return len(CURSO)

def ibge_qtdadeProfissoes(path,name): 
    file = path + name
    CBOS = pd.read_csv(file, dtype ='str')
           
    CBOS = CBOS.drop(columns=['Unnamed: 0'])
    #print(CBOS.columns)
    CBO = []
    for l in range(len(CBOS)):
        if len((CBOS.Cod_CBO[l])) >=4:
          # 0000 - OCUPAÇÕES MALDEFINIDAS  ...  # Nome_CBO
          if (CBOS.Cod_CBO[l]) != '0000':
             # print(CBOS.Cod_CBO[l])
             CBO.append(CBOS.Cod_CBO[l])          
    return len(CBO)
    # return 

#def ibge_qtdadeCursos_recenseados(path,name,i,path1,name1): 
def ibge_qtdadeCursos_recenseados(path1,name1): 
 
    # file = os.path.join(path,name)
    # CURSOS = pd.read_csv(file, dtype ='str')
    file1 = os.path.join(path1 + name1)
    Brasil = pd.read_csv(file1)
    
    # CURSOS = CURSOS.drop(columns=['Unnamed: 0'])
    # print(len(CURSOS.Cod_Curso))

    Cursos_Censo = Brasil.Curso_Superior_Graduação_Código

    Cursos_Censo_unique = Cursos_Censo.unique()
    # print(len(Cursos_Censo_unique))

    # Não remover esse comentário ...
    # Essa validação não é necessária para os cursos do Censo, pois o recenseados já tem os mesmos cursos do censo
    # Essa validação só é necessária para validação de cursos como da Unicamp, mec e etc ... 
    # CURSO_NUM  = []
    # CURSO_NOME = []
    # for l in range(len(Cursos_Censo_unique)):
    #     #if(l==1):
    #     #   break
    #     for i, j in CURSOS.iterrows():
    #         #print(CURSOS.Cod_Curso[i])
    #         if(CURSOS.Cod_Curso[i]== str(Cursos_Censo_unique[l])):
    #             #print(Cursos_Censo_unique[l])
    #             #print('CURSOS.Cod_Curso[i]: ', CURSOS.Cod_Curso[i] + " - CURSOS.Nome_Curso[i]: ", CURSOS.Nome_Curso[i])
    #             CURSO_NUM.append(CURSOS.Cod_Curso[i])
    #             CURSO_NOME.append(CURSOS.Nome_Curso[i])

    # Cursos_Censo=[]
    # for i in range(len(CURSO_NUM)):
    #     tupla=(CURSO_NUM[i],CURSO_NOME[i])
    #     Cursos_Censo.append(tupla)
    # #...
    # CursosCenso = pd.DataFrame(Cursos_Censo)
    # #Curso_Cbo_dir_curso_cbos.shape
    # nomes = {0:"curso_num",
    #          1:"curso_nome",
    #         }
    # CursosCenso.rename(columns=nomes,inplace=True)
    # CursosCenso = CursosCenso.sort_values(by=['curso_num'])

    # index_names = CursosCenso[ CursosCenso['curso_nome'] == 'NÃO SABE E SUPERIOR NÃO ESPECIFICADO' ].index
    # CursosCenso.drop(index_names, inplace = True)
    # print(CursosCenso)
        
    # return len(CursosCenso)
    return len(Cursos_Censo_unique)

def ibge_qtdadeProfissoes_recenseados(path1,name1): 
    # file = os.path.join(path,name)
    # CURSOS = pd.read_csv(file, dtype ='str')
    file1 = os.path.join(path1 + name1)
    Brasil = pd.read_csv(file1)
    
    # CURSOS = CURSOS.drop(columns=['Unnamed: 0'])
    # print(len(CURSOS.Cod_Curso))

    Profissoes_Censo = Brasil.Ocupação_Código
    # print( Brasil.columns)
    Profissoes_Censo_unique = Profissoes_Censo.unique()
    #print(len(Profissoes_Censo_unique))
    return len(Profissoes_Censo_unique)


def ibge_qtdadeCursos_recenseados_feminino(path1,name1): 
     
    # file = os.path.join(path,name)
    # CURSOS = pd.read_csv(file, dtype ='str')
    file1 = os.path.join(path1 + name1)
    Brasil = pd.read_csv(file1)
    # print(Brasil.shape)
    
    # CURSOS = CURSOS.drop(columns=['Unnamed: 0'])
    # print(len(CURSOS.Cod_Curso))

    # removendo pessoas do sexo masculino ...
    # X.drop(X[(X['gênero'] ==1)].index, inplace=True)
    filtro  = Brasil['gênero'] == 2
    Brasil_copia = Brasil[filtro]
    # print(Brasil_copia.shape)
    
    Cursos_Censo = Brasil_copia.Curso_Superior_Graduação_Código

    Cursos_Censo_unique = Cursos_Censo.unique()
    # print(len(Cursos_Censo_unique))

    return len(Cursos_Censo_unique)
    
    

def ibge_qtdadeCursos_recenseados_masculino(path1,name1): 
           
    # file = os.path.join(path,name)
    # CURSOS = pd.read_csv(file, dtype ='str')
    file1 = os.path.join(path1 + name1)
    Brasil = pd.read_csv(file1)
    # print(Brasil.shape)
    
    # CURSOS = CURSOS.drop(columns=['Unnamed: 0'])
    # print(len(CURSOS.Cod_Curso))

    # removendo pessoas do sexo feminino ...
    # X.drop(X[(X['gênero'] ==1)].index, inplace=True)
    filtro  = Brasil['gênero'] == 1
    Brasil_copia = Brasil[filtro]
    # print(Brasil_copia.shape)
    
    Cursos_Censo = Brasil_copia.Curso_Superior_Graduação_Código

    Cursos_Censo_unique = Cursos_Censo.unique()
    # print(len(Cursos_Censo_unique))

    return len(Cursos_Censo_unique)

def ibge_qtdadeProfissoes_recenseados_feminino(path1,name1): 
    # file = os.path.join(path,name)
    # CURSOS = pd.read_csv(file, dtype ='str')
    file1 = os.path.join(path1 + name1)
    Brasil = pd.read_csv(file1)
    
    # CURSOS = CURSOS.drop(columns=['Unnamed: 0'])
    # print(len(CURSOS.Cod_Curso))
    
    filtro  = Brasil['gênero'] == 2
    Brasil_copia = Brasil[filtro]

    Profissoes_Censo = Brasil_copia.Ocupação_Código
    # print( Brasil.columns)
    Profissoes_Censo_unique = Profissoes_Censo.unique()
    #print(len(Profissoes_Censo_unique))
    return len(Profissoes_Censo_unique)

def ibge_qtdadeProfissoes_recenseados_masculino(path1,name1): 
    # file = os.path.join(path,name)
    # CURSOS = pd.read_csv(file, dtype ='str')
    file1 = os.path.join(path1 + name1)
    Brasil = pd.read_csv(file1)
    
    # CURSOS = CURSOS.drop(columns=['Unnamed: 0'])
    # print(len(CURSOS.Cod_Curso))
    
    filtro  = Brasil['gênero'] == 1
    Brasil_copia = Brasil[filtro]
    
    Profissoes_Censo = Brasil_copia.Ocupação_Código
    # print( Brasil.columns)
    Profissoes_Censo_unique = Profissoes_Censo.unique()
    #print(len(Profissoes_Censo_unique))
    return len(Profissoes_Censo_unique)

def CBOs_Curso(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,save_results_to):
    # Abrir csv do Brasil inteiro
    brasil = pd.read_csv(csv_estado)
    # Abrir CSV do CBO
    CBO = pd.read_csv(csv_CBO)
    # Abrir CSV de Cursos
    # cursos = pd.read_csv(csv_CURSOS)

    # # Identificar todos os CBOs únicos da tabela brasil utilizando a coluna ocupacao_codigo
    # CBO_unicos = brasil['Ocupação_Código'].unique()
    # # Imprima a quantidade de CBO únicos
    # print(len(CBO_unicos))

    # # Identificar todos os cursos únicos da tabela brasil utilizando a coluna Curso_Superior_Graduação_Código
    # cursos_unicos = brasil['Curso_Superior_Graduação_Código'].unique()
    # # Imprima a quantidade de cursos únicos
    # print(len(cursos_unicos))

    # # Monte um dataframe que indique a quantidade de cada CBO por curso que temos na tabela brasil
    # # Vamos fazer isso utilizando a função crosstab do pandas
    # crosstab_curso = pd.crosstab(index=brasil['Curso_Superior_Graduação_Código'], columns=brasil['Ocupação_Código'])
    # # Imprima o crosstab
    # print(crosstab_curso)

    # # Faça a mesma coisa da ordem inversa, montando um dataframe que indique a quantidade de cada curso por CBO
    # crosstab_cbo = pd.crosstab(index=brasil['Ocupação_Código'], columns=brasil['Curso_Superior_Graduação_Código'])
    # # Imprima o crosstab
    # print(crosstab_cbo)

    # A partir do arquivo brasil, criar um novo dataframe somente com cursos e cbos para facilitar 
    X_CURSO_CBO = brasil[['Curso_Superior_Graduação_Código','Ocupação_Código']]
    # print(X_CURSO_CBO)

    # Transforma  X_CURSO_CBO.Ocupação_Código de Float para String 
    # A partir do arquivo brasil, criar um novo dataframe somente com cursos e cbos para facilitar 
    Curso_Superior_Graduação_Código = []
    Ocupação_Código = []
    Ocupação_Código_temp = []    
    for i in range(len(X_CURSO_CBO)):        
        Ocupação_Código_temp.append(str(int(X_CURSO_CBO.Ocupação_Código[i])))   
    # print(len(Ocupação_Código_temp))
    for i in range(len(X_CURSO_CBO)):         
        if (Ocupação_Código_temp[i][0] == '2') or (Ocupação_Código_temp[i][0] == '1'):
            Curso_Superior_Graduação_Código.append(X_CURSO_CBO.Curso_Superior_Graduação_Código[i])
            Ocupação_Código.append(X_CURSO_CBO.Ocupação_Código[i])
    # print(len(Ocupação_Código))     
    # Transforma a lista de CBOs da familia 1 e 2 para Dataframe
    X_CURSO_CBO_Filter=[]
    for i in range(len(Curso_Superior_Graduação_Código)):
        tupla=(Curso_Superior_Graduação_Código[i],Ocupação_Código[i])
        X_CURSO_CBO_Filter.append(tupla)     
    X_CURSO_CBO = pd.DataFrame(X_CURSO_CBO_Filter)
    dict = {0:"Curso_Superior_Graduação_Código", 1:"Ocupação_Código"}
    X_CURSO_CBO.rename(columns=dict,inplace=True)
    # print(len(X_CURSO_CBO))
    #CBOs por curso
    dir = X_CURSO_CBO.index[X_CURSO_CBO['Curso_Superior_Graduação_Código'] == curso_num].tolist()
    Curso_dir = []
    Cbo_dir = []
    # print(dir)
    for i in range(len(dir)):
        curso = X_CURSO_CBO._get_value(dir[i],'Curso_Superior_Graduação_Código')
        cbo = X_CURSO_CBO._get_value(dir[i],'Ocupação_Código')
        Curso_dir.append(curso)
        Cbo_dir.append(cbo)
    resultados_dir=[]
    for i in range(len(Curso_dir)):
        tupla=(Curso_dir[i],Cbo_dir[i])
        resultados_dir.append(tupla)
    Curso_Cbo_dir = pd.DataFrame(resultados_dir)
    # print(resultados_dir)
    dict = {0:"Curso",1:"Cbo"}
    Curso_Cbo_dir.rename(columns=dict,inplace=True)
    # print(Curso_Cbo_dir.columns)

    #CBOs Unicos 
    Curso_Cbo_dir_unique = np.unique(Curso_Cbo_dir.Cbo)
    Curso_Cbo_dir['Cbo'].value_counts().sort_index()
    from numpy.ma.core import sort
    A = Curso_Cbo_dir['Cbo'].value_counts().sort_index()
    A = pd.DataFrame(A)
    A_cbo = A.sort_values("Cbo",ascending=False)
    A_cbo_10 = A_cbo.head(10) #Alterado em 06/09/23
    # print(len(A_cbo_10))

	#Coletando o nome do CBOs ...
    NomeCbo = []
    for i in range(len(A_cbo_10)):
        #print(type(str(int(A_cbo_10['Cbo'].iloc[i]))))
        #print(A_cbo_10['Cbo'].iloc[i])
        cbo = str(int(float(A_cbo_10.index[i])))
        #print(type(cbo))
        #print(cbo)
        for i in range(len(CBO)):
            # print(type(CBO['Cod_CBO'].iloc[i]))
            if (str(int(CBO['Cod_CBO'].iloc[i])) == cbo):
                NomeCbo.append(CBO['Nome_CBO'].iloc[i])      
    NomeCbo = pd.DataFrame(NomeCbo, columns=['Nome_CBO'])
    # print(len(NomeCbo))

    #Adicionar a coluna Nome no dataframe A_cbo_10
    A_cbo_10.insert(loc=1, column='Nome', value=[1,1,1,1,1,1,1,1,1,1])
    for i in range(len(A_cbo_10)):
        A_cbo_10['Nome'].iloc[i]= NomeCbo['Nome_CBO'].iloc[i]
    A_cbo_10.reset_index(inplace=True)
    A_cbo_10 = A_cbo_10.rename(columns = {'index':'Cod_CBO'})    
    A_cbo_10['Cod_CBO'] = A_cbo_10['Cod_CBO'].astype("float").astype('str')
    A_cbo_10['CBO_Nome'] = A_cbo_10['Cod_CBO'].str.cat(A_cbo_10['Nome'], sep =" ")
    # print(A_cbo_10)
    #print('')

    # tresprimeiros Cbos
    tresprimeiros = [] 
    if (len(A_cbo_10)<3):
        for i in range(len(A_cbo_10)):
            # print(str(int(float(A_cbo_10['Cod_CBO'][i]))))
            tresprimeiros.append(str(int(float(A_cbo_10['Cod_CBO'].iloc[i]))))
    else:
        for l in range(3):
            tresprimeiros.append(str(int(float(A_cbo_10['Cod_CBO'].iloc[l]))))
    del A_cbo_10["Cod_CBO"]
    del A_cbo_10["Nome"]
    # print(tresprimeiros)

    #  Nomes dos três primeiros cbos
    tresnomes = []
    if (len(A_cbo_10)<3):
        for i in range(len(A_cbo_10)):
            tresnomes.append(A_cbo_10.CBO_Nome[i])
    else:
        for i in range(3):
            tresnomes.append(A_cbo_10.CBO_Nome[i])

    A_cbo_10 = A_cbo_10.set_index('CBO_Nome')
    #Plotando ... 
    A_cbo_10_sort = A_cbo_10.sort_values("Cbo",ascending=True)
    plt.rcParams["figure.figsize"] = (18, 8)
    plt.rcParams["figure.autolayout"] = True
    A_cbo_10_sort.plot(kind='barh',title=titulo10)
    plt.xlabel("")
    string ="_" + str(curso_num) + " - " + curso_nome + "_10.pdf"
    plt.savefig(save_results_to + string)
    # plt.show()
    #...
    A_cbo_10_sort = A_cbo_10.iloc[0:3].sort_values("Cbo",ascending=True)
    plt.rcParams["figure.figsize"] = (18, 8)
    plt.rcParams["figure.autolayout"] = True
    A_cbo_10_sort.plot(kind='barh',title=titulo3)
    plt.xlabel("")
    string = "_" + str(curso_num) + " - " + curso_nome + "_3.pdf"
    plt.savefig(save_results_to + string)
    # plt.show()
    return tresprimeiros,tresnomes,curso_num,curso_nome

#Função para achar a quantidade de Não-Graduados na Pivot Table --- 27/04/2024
def NaoGraduados_PivotTable(primeirosCbos,csv_PivotTableFinal):
    PivotTableFinal = pd.read_csv(csv_PivotTableFinal)
    # print(PivotTableFinal)
    NaoGraduados = []
    for i in range(len(primeirosCbos)):
        # print( type(int(str(primeirosCbos[0]))))
        Valor1 = PivotTableFinal.loc[PivotTableFinal.Ocupação_Código==int(str(primeirosCbos[i])), '1.0'].values[0]
        Valor2 = PivotTableFinal.loc[PivotTableFinal.Ocupação_Código==int(str(primeirosCbos[i])), '2.0'].values[0]
        Valor3 = PivotTableFinal.loc[PivotTableFinal.Ocupação_Código==int(str(primeirosCbos[i])), '3.0'].values[0]
        Valor5 = PivotTableFinal.loc[PivotTableFinal.Ocupação_Código==int(str(primeirosCbos[i])), '5.0'].values[0]
        ValorFinal= Valor1 + Valor2 + Valor3 + Valor5
        NaoGraduados.append(ValorFinal)
    return NaoGraduados

# Função para achar a quantidade de Não-Graduados na Pivot Table --- 28/04/2024
def NaoGraduados_PivotTable_2(primeirosCbos,csv_PivotTableFinal):
    PivotTableFinal = pd.read_csv(csv_PivotTableFinal)
    # print(PivotTableFinal)
    NaoGraduados = []
    Graduados_Nao = []
    Graduados = []
    for i in range(len(primeirosCbos)):
        # print( type(primeirosCbos[i]))
        # print('primeirosCbos',primeirosCbos)
        # exit(0)
        # Valor1 = PivotTableFinal.loc[PivotTableFinal.Ocupação_Código==int(str(primeirosCbos[i])), '1.0'].values[0]  
        Valor1 = PivotTableFinal.loc[PivotTableFinal['CBO-Domiciliar']==int(str(primeirosCbos[i])), '1.0'].values[0]   
        # print('Valor1:',Valor1)  
        # exit(0)       
        # Valor2 = PivotTableFinal.loc[PivotTableFinal.Ocupação_Código==int(str(primeirosCbos[i])), '2.0'].values[0]
        Valor2 = PivotTableFinal.loc[PivotTableFinal['CBO-Domiciliar']==int(str(primeirosCbos[i])), '2.0'].values[0]
        # Valor3 = PivotTableFinal.loc[PivotTableFinal.Ocupação_Código==int(str(primeirosCbos[i])), '3.0'].values[0]
        Valor3 = PivotTableFinal.loc[PivotTableFinal['CBO-Domiciliar']==int(str(primeirosCbos[i])), '3.0'].values[0]
        # Valor5 = PivotTableFinal.loc[PivotTableFinal.Ocupação_Código==int(str(primeirosCbos[i])), '5.0'].values[0]
        Valor5 = PivotTableFinal.loc[PivotTableFinal['CBO-Domiciliar']==int(str(primeirosCbos[i])), '5.0'].values[0]
        ValorFinal= Valor1 + Valor2 + Valor3 + Valor5
        # Valor4 = PivotTableFinal.loc[PivotTableFinal.Ocupação_Código==int(str(primeirosCbos[i])), '4.0'].values[0]
        Valor4 = PivotTableFinal.loc[PivotTableFinal['CBO-Domiciliar']==int(str(primeirosCbos[i])), '4.0'].values[0]
        ValorTotal= Valor1 + Valor2 + Valor3 + Valor4 + Valor5
        NaoGraduados.append(ValorFinal)
        Graduados_Nao.append(ValorTotal)
        Graduados.append(Valor4)
    return primeirosCbos,NaoGraduados,Graduados_Nao,Graduados


#Cursos por CBO --- 27/04/2024
def Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo3,NaoGraduados_qtdade,curso_num,curso_nome,primeirosCbos_Nome,i):
    numero = i
    #Leitura de Arquivos CSVs ...
    X = pd.read_csv(csv_estado)
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    CURSOS = pd.read_csv(csv_CURSOS, dtype ='str')
    # drop the 'Unnamed:0' column
    CBO = CBO.drop(columns=['Unnamed: 0'])
    CURSOS = CURSOS.drop(columns=['Unnamed: 0'])
    #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
    X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']]
    # print(X_CURSO_CBO.shape)
    # print(X_CURSO_CBO)

    #Cursos por CBO
    #Indice =================================================================================================
    X_CURSO_CBO['Ocupação_Código'] = X_CURSO_CBO['Ocupação_Código'].astype(int)
    dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['Ocupação_Código'] == int(str(cbo_num))].tolist()
    # print(dir_curso_cbos)
    # ...
    Curso_dir_curso_cbos = []
    Cbo_dir_curso_cbos = []
    for i in range(len(dir_curso_cbos)):
        #print(direito[i])
        curso = X_CURSO_CBO._get_value(dir_curso_cbos[i],'Curso_Superior_Graduação_Código')
        cbo = X_CURSO_CBO._get_value(dir_curso_cbos[i],'Ocupação_Código')
        #print("Curso:",curso,"CBO:",str(int(cbo)))
        Curso_dir_curso_cbos.append(curso)
        Cbo_dir_curso_cbos.append(cbo)
    #..
    resultados_dir_curso_cbos=[]
    for i in range(len(Curso_dir_curso_cbos)):
      tupla=(Curso_dir_curso_cbos[i],Cbo_dir_curso_cbos[i])
      resultados_dir_curso_cbos.append(tupla)
    #...
    Curso_Cbo_dir_curso_cbos = pd.DataFrame(resultados_dir_curso_cbos)
    #Curso_Cbo_dir_curso_cbos.shape
    dict = {0:"Curso_Repet",
        1:"Cbo_Repet",
        }
    Curso_Cbo_dir_curso_cbos.rename(columns=dict,inplace=True)
    # print(Curso_Cbo_dir_curso_cbos)
    #Cursos Únicos por CBO ====================================================================================
    Curso_Cbo_dir_curso_cbos_unique = np.unique(Curso_Cbo_dir_curso_cbos.Curso_Repet)
    #Plot======================================================================================================
    Curso_Unique = Curso_Cbo_dir_curso_cbos['Curso_Repet'].astype(int).tolist()
    #...
    Curso_Cbo_dir_curso_cbos['Curso_Repet'].value_counts().sort_index()
    #...
    from numpy.ma.core import sort
    A_dir_curso_cbos = Curso_Cbo_dir_curso_cbos['Curso_Repet'].value_counts().sort_index()
    #...
    #Curso_Cbo_dir.loc[1:3, ['Cbo']]
    A_dir_curso_cbos_sort = pd.DataFrame(A_dir_curso_cbos)
    #...
    A_Curso = A_dir_curso_cbos_sort.sort_values("Curso_Repet",ascending=False)
    #...
    A_Curso_11 = A_Curso.head(10)
    # print(A_Curso_11)
    #Coletando o nome dos Cursos ...
    NomeCurso = []
    for i in range(len(A_Curso_11)):
        curso=str(float(A_Curso_11.index[i]))
        for indexx, row in CURSOS.iterrows():
            if (row['Cod_Curso'] == curso):
            #if(row['Cod_Curso'] == A_Curso_10.index[i]):
                NomeCurso.append(row['Nome_Curso'])
                #print(row['Cod_Curso'],":",row['Nome_Curso'])
    #...
    NomeCurso = pd.DataFrame(NomeCurso, columns=['Nome_Curso'])
    # ...
    # A_Curso_11["Nome"] = 1
    A_Curso_11.insert(loc=1, column='Nome', value=[1,1,1,1,1,1,1,1,1,1])
    import warnings
    for i in range(len(A_Curso_11)):
        # A_Curso_11['Nome'][i] = NomeCurso.Nome_Curso[i]
        A_Curso_11['Nome'].iloc[i]= NomeCurso['Nome_Curso'].iloc[i]
    # print(A_Curso_11)   
    #...
    A_Curso_11.reset_index(inplace=True)
    A_Curso_11 = A_Curso_11.rename(columns = {'index':'Curso'})
    #A_Curso_11
    A_Curso_11['Curso'] = A_Curso_11['Curso'].astype("float").astype('str')
    A_Curso_11['Curso_Nome'] = A_Curso_11['Curso'].str.cat(A_Curso_11['Nome'], sep =" ")

    A_Curso_11['Curso'].iloc[3]= 0
    A_Curso_11['Curso_Repet'].iloc[3]= NaoGraduados_qtdade
    A_Curso_11['Nome'].iloc[3]= "Não-Graduados"
    A_Curso_11['Curso_Nome'].iloc[3]= "Não-Graduados"
    tresprimeiros = []
    if (len(A_Curso_11)<3):
        for i in range(len(A_Curso_11)):
            tresprimeiros.append(int(float(A_Curso_11.Curso[i])))
    else:
        #for i in range(3):
        for i in range(4): #Alterado em 09/09/2023 para pegar o 4º Elemento
            tresprimeiros.append(int(float(A_Curso_11.Curso[i])))
    A_Curso_11_sort = A_Curso_11.iloc[0:4].sort_values("Curso_Repet",ascending=True) #Alterado em 09/09/2023 para pegar os 4 primeiros
    index =  A_Curso_11_sort.index
    for i in range(len(index)):
        if ((i==0)and(A_Curso_11_sort['Curso'].iloc[i]==0)):
            colors = ['green', 'blue', 'blue','blue'] #4ª posição
            break
        if ((i==1)and(A_Curso_11_sort['Curso'].iloc[i]==0)):
            colors = ['blue', 'green', 'blue','blue'] #3ª posição
            break
        if ((i==2)and(A_Curso_11_sort['Curso'].iloc[i]==0)):
            colors = ['blue', 'blue', 'green','blue'] #2ª posição
            break
        if ((i==3)and(A_Curso_11_sort['Curso'].iloc[i]==0)):
            colors = ['blue', 'blue', 'blue','green'] #1ª posição
            break
    tituloalterado = titulo3 + " : " + "Cbo fraco"
    tituloalterado = titulo3 + " : " + "Weak Cbo"
    curso_num = str(float(curso_num))
    intensidade = 'Fraco'
    for i in range(len(index)):
        if ((i==3)and(A_Curso_11_sort['Curso'].iloc[i]==str(curso_num))): #curso_num
            tituloalterado = titulo3 + " : " + "Cbo forte"
            tituloalterado = titulo3 + " : " + "Strong Cbo"
            intensidade ='Forte'
            break
    x='Curso_Nome'
    y='Curso_Repet'
    A_Curso_11_sort.plot(x,y,kind='barh',title=tituloalterado,color=colors,legend=False)
    string = "_" + str(curso_num) + " - " + curso_nome + " : " + primeirosCbos_Nome[numero] +".pdf"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string)
    # plt.show()
    return curso_nome,primeirosCbos_Nome,intensidade
#Função para plotar os três primeiros cursos dos três primeiros CBOs ... # 27/04/2024
def Plot_Cursos_CBOs_11(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos_Nome,primeirosCbos,NaoGraduados,curso_num,curso_nome):
    Intensidade = []
    for i in range (len(primeirosCbos)):
          titulo3=primeirosCbos_Nome[i]
          Curso,tresprimeirosCursos,intensidade=Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],curso_num,curso_nome,primeirosCbos_Nome,i)
          Intensidade.append(intensidade)          
    return Curso,tresprimeirosCursos,Intensidade    



# Cursos por CBO 28/04/2024
# Achar CBOs por Curso
def CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,porcent_param,save_results_to):
    X = pd.read_csv(csv_estado)
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    # CBO = CBO.drop(columns=['Unnamed: 0']) #comentado  em 12/08/2025 ... troca de arquivo de CBOs
   
    #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
    # X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']]
    X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','CBO-Domiciliar']] #mudado  em 12/08/2025 ... troca de arquivo de CBOs
    
    
    # Transforma  X_CURSO_CBO.Ocupação_Código de Float para String 
    # A partir do arquivo brasil, criar um novo dataframe somente com cursos e cbos para facilitar 
    Curso_Superior_Graduação_Código = []
    Ocupação_Código = []
    Ocupação_Código_temp = []    
    for i in range(len(X_CURSO_CBO)):        
        # Ocupação_Código_temp.append(str(int(X_CURSO_CBO.Ocupação_Código[i]))) 
        Ocupação_Código_temp.append(str(int(X_CURSO_CBO['CBO-Domiciliar'][i])))  
    for i in range(len(X_CURSO_CBO)):         
        if (Ocupação_Código_temp[i][0] == '2') or (Ocupação_Código_temp[i][0] == '1'):
            Curso_Superior_Graduação_Código.append(X_CURSO_CBO.Curso_Superior_Graduação_Código[i])
            # Ocupação_Código.append(X_CURSO_CBO.Ocupação_Código[i])
            Ocupação_Código.append(X_CURSO_CBO['CBO-Domiciliar'][i])
    # ...
    X_CURSO_CBO_Filter=[]
    for i in range(len(Curso_Superior_Graduação_Código)):
      tupla=(Curso_Superior_Graduação_Código[i],Ocupação_Código[i])
      X_CURSO_CBO_Filter.append(tupla)
    X_CURSO_CBO = pd.DataFrame(X_CURSO_CBO_Filter)
    dict = {0:"Curso_Superior_Graduação_Código",
    #1:"Ocupação_Código",
    1:"CBO-Domiciliar",
    }
    X_CURSO_CBO.rename(columns=dict,inplace=True)
    # print(X_CURSO_CBO)
    #...
    #CBOs por curso
    #Indice ===========================================================================================================
    # dir = X_CURSO_CBO.index[X_CURSO_CBO['Curso_Superior_Graduação_Código'] == curso_num].tolist()
    dir = X_CURSO_CBO.index[X_CURSO_CBO['Curso_Superior_Graduação_Código'] == curso_num].tolist()
    # print("curso_num",type(curso_num))
    # print("len(dir)",len(dir))
    if(len(dir)>=1):
        Curso_dir = []
        Cbo_dir = []
        for i in range(len(dir)):
            curso = X_CURSO_CBO._get_value(dir[i],'Curso_Superior_Graduação_Código')
            # cbo = X_CURSO_CBO._get_value(dir[i],'Ocupação_Código')
            cbo = X_CURSO_CBO._get_value(dir[i],'CBO-Domiciliar') #comentado  em 12/08/2025 ... troca de arquivo de CBOs
            Curso_dir.append(curso)
            Cbo_dir.append(cbo)
        # print("Curso_dir",Curso_dir)  
        # print("Cbo_dir",Cbo_dir)
        resultados_dir=[]
        for i in range(len(Curso_dir)):
            tupla=(Curso_dir[i],Cbo_dir[i])
            resultados_dir.append(tupla)
        Curso_Cbo_dir = pd.DataFrame(resultados_dir)
        # print("Curso_Cbo_dir[0]", Curso_Cbo_dir[0])
        dict = {0:"Curso", 1:"Cbo",}
        Curso_Cbo_dir.rename(columns=dict,inplace=True)
        # print("Curso_Cbo_dir",Curso_Cbo_dir)
        #CBOs Unicos ============================================================
        Curso_Cbo_dir_unique = np.unique(Curso_Cbo_dir.Cbo)
        A = Curso_Cbo_dir['Cbo'].value_counts().sort_index()
        A = pd.DataFrame(A)
        A_cbo = A.sort_values("Cbo",ascending=False)
        Total = A_cbo["Cbo"].sum() #==========================================================================================================
        #====================================================================================================================================
        porcento = Total*porcent_param
        # print("porcento", porcento)
        # exit(0)
        porcento_10 = round(porcento/Total * 100, 2)
        # print(porcento_10)
        # exit(0)

        # if (porcent_param == 1):
        #     porcento = Total
        #     # print("porcento",porcento) #30/07/2025
        #     porcento_10 = round(porcento/Total, 2)
        #     # print("porcento_10",porcento_10) #30/07/2025
        #     # exit(0) #30/07/2025
        # else:
        #     porcento = Total*porcent_param
        #     # print("porcento",porcento) #30/07/2025
        #     porcento_10 = round(porcento/Total * 100, 2)
        #     # print("porcento_10",porcento_10) #30/07/2025
        #     # exit(0) #30/07/2025
        ## ...
        Porcentagem = []
        Porcentagem = round(A_cbo['Cbo']/Total * 100, 2)
        # Adicionar a coluna Nome no dataframe A_cbo_10
        A_cbo['Porcentagem'] = Porcentagem
        # print(A_cbo)
        qtdade = 0
        for i in A_cbo.index:
            if (A_cbo.Porcentagem[i]>= porcento_10):
                qtdade = qtdade+1
        A_cbo_10 = A_cbo.iloc[:qtdade].copy()  # Ensure a copy of the top 'qtdade' rows for further modifications
        print("A_cbo_10 ...")
        print(A_cbo_10) #30/07/2025
        # exit(0) #30/07/2025
        if(len(A_cbo_10>=1)):
        # # Validação para testar se existem cbos para deteminado curso
        # if(len(A_cbo_10>=1)):
            #Coletando o nome do CBOs ...
            # CBO_Inexistente = []
            NomeCbo = []
            # for i in range(len(A_cbo_10)):
            #     cbo = str(int(float(A_cbo_10.index[i])))
            #     for i in range(len(CBO)):
            #         if (str(int(CBO['Cod_CBO'].iloc[i])) == cbo):
            #             NomeCbo.append(CBO['Nome_CBO'].iloc[i])    
            #         #else:   
            #             #CBO_Inexistente.append(cbo)   #encontrando CBOs que não existem no arquivo de CBOs ... 16/08/2025
            #             #print("CBO_Inexistente", CBO_Inexistente) #16/08/2025
            #         #     # sys.exit() #===============================================================================================
            #         #     primeiros=0
            #         #     nomes=0
            #         #     porcentagens=0
            #         #     return primeiros,nomes,porcentagens,curso_num,curso_nome  

            # Para encontrar todos os CBOs que estão em A_cbo_10 e também em CBO['Cod_CBO'], você pode usar o método isin do pandas:
            cbo_indices = [str(int(float(idx))) for idx in A_cbo_10.index]
            # Filtra o DataFrame CBO para manter apenas os CBOs presentes em cbo_indices
            CBO_filtrado = CBO[CBO['Cod_CBO'].astype(str).isin(cbo_indices)]
            NomeCbo = CBO_filtrado['Nome_CBO'].tolist()

            # Para guardar os CBOs que estão em A_cbo_10 e não estão em CBO['Cod_CBO']:
            cbo_nao_encontrados = [cbo for cbo in cbo_indices if cbo not in set(CBO['Cod_CBO'].astype(str))]
            # Agora cbo_nao_encontrados contém os códigos que não existem em CBO['Cod_CBO']

            NomeCbo = pd.DataFrame(NomeCbo, columns=['Nome_CBO'])
            # CBO_Inexistente = list(set(CBO_Inexistente))
            # print("CBO_Inexistente=======================================", CBO_Inexistente) #16/08/2025
            print("cbo_nao_encontrados",cbo_nao_encontrados) #18/08/2025
            #...
            # A_cbo_10["Nome"] = 1
            #...
            #import warnings
            #A_cbo_10['Nome'] = NomeCbo['Nome_CBO'].values
            A_cbo_10 = A_cbo_10.iloc[:len(NomeCbo)] # 12/08/2025 ajuste por causa da mudança de arquivo de CBOs
            A_cbo_10['Nome'] = NomeCbo['Nome_CBO'].values
            #A_cbo_10
            A_cbo_10.reset_index(inplace=True)
            A_cbo_10 = A_cbo_10.rename(columns = {'index':'Cod_CBO'})
            print("len(A_cbo_10)",len(A_cbo_10))
            #A_cbo_10
            #...
            if (len(A_cbo_10)>=1): #if (len(A_cbo_10)>1): 16/08/2025
                A_cbo_10['Cod_CBO'] = A_cbo_10['Cod_CBO'].astype("float").astype('str')
                A_cbo_10['CBO_Nome'] = A_cbo_10['Cod_CBO'].str.cat(A_cbo_10['Nome'], sep =" ")
                print("A_cbo_10...")
                print(A_cbo_10) #16/08/2025
                # exit(0) #30/07/2025
                # tresprimeiros Cbos
                primeiros = [] # Alterado em 29/09/2023
                if (len(A_cbo_10)<1):
                    print("Não existe CBOs para este curso...")
                    # sys.exit() #===============================================================================================
                else:
                    for i in range(len(A_cbo_10)):
                        primeiros.append(str(int(float(A_cbo_10['Cod_CBO'].iloc[i]))))
                        # primeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
                #...
                #Deletar coluna
                del A_cbo_10["Cod_CBO"]
                del A_cbo_10["Nome"]
                # A_cbo_10

                #  Nomes dos três primeiros cbos
                nomes = [] # Alterado em 26/09/2023
                if (len(A_cbo_10)<1):
                    print("Não existe CBOs para este curso ...")
                    # sys.exit() #===============================================================================================
                else:
                    for i in range(len(A_cbo_10)):
                        nomes.append(A_cbo_10.CBO_Nome[i])
                porcentagens = []
                if (len(A_cbo_10)<1):
                    print("Não existe CBOs para este curso...")
                    # sys.exit() #===============================================================================================
                else:
                    for i in range(len(A_cbo_10)):
                        porcentagens.append(A_cbo_10.Porcentagem[i])
                #...
                x='CBO_Nome'
                y='Porcentagem'
                # x='CBO_Name'
                # y='Percentage'
                #Plotando ... Alterado em 06/09/23 ... tirei o plot dos dez maiores #07/09/2023 voltei o plot dos dez maiores ...
                A_cbo_10_sort = A_cbo_10.iloc[0:3].sort_values("Porcentagem",ascending=True)
                print("A_cbo_10_sort...") #14/08/2025
                print(A_cbo_10_sort) #14/08/2025
                # exit(0) #14/08/2025
                plt.rcParams["figure.figsize"] = (18, 8)
                plt.rcParams["figure.autolayout"] = True
                ax = A_cbo_10_sort.plot(x,y,kind='barh',title=titulo3,legend=False)
                ax.bar_label(ax.containers[0])
                # plt.xlabel("Porcentagem")
                plt.xlabel("Percentage")
                plt.ylabel("CBO_Name")
                # string = str(curso_num) + " - " + curso_nome + "_" + str(porcent_param) +".pdf"
                string = str(curso_num) + " - " + curso_nome + "_" + str(porcent_param) +".png"
                plt.savefig(save_results_to + string)
                # plt.show()
            else:
                print("Não existem CBOs para este curso :::")
                # sys.exit() #===============================================================================================
                primeiros=0
                nomes=0
                porcentagens=0
                return primeiros,nomes,porcentagens,curso_num,curso_nome    
        else:
            print("As porcentagens dos CBOs são menores que o parâmetro de porcentagem")
            #  sys.exit() #===============================================================================================
            primeiros=0
            nomes=0
            porcentagens=0
            return primeiros,nomes,porcentagens,curso_num,curso_nome                
    else:
         print("Não existe CBOs para este curso")
         #  sys.exit() #===============================================================================================
         primeiros=0
         nomes=0
         porcentagens=0
         return primeiros,nomes,porcentagens,curso_num,curso_nome
    # print(primeiros,nomes,porcentagens,curso_num,curso_nome)
    # exit(0) #30/07/2025
    return primeiros,nomes,porcentagens,curso_num,curso_nome




def Cursos_CBO_14_10(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo3,NaoGraduados_qtdade,curso_num,curso_nome,primeirosCbos_Nome,i,porcent_param):
    numero = i
    #Leitura de Arquivos CSVs ...
    X = pd.read_csv(csv_estado)
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    CURSOS = pd.read_csv(csv_CURSOS, dtype ='str')
    # drop the 'Unnamed:0' column
    # CBO = CBO.drop(columns=['Unnamed: 0']) #comentado  em 12/08/2025 ... troca de arquivo de CBOs
    CURSOS = CURSOS.drop(columns=['Unnamed: 0']) 
  
    #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
    # Filter only the relevant columns for courses and occupations
    # X_CURSO_CBO = X.loc[:, ['Curso_Superior_Graduação_Código', 'Ocupação_Código']]
    X_CURSO_CBO = X.loc[:, ['Curso_Superior_Graduação_Código', 'CBO-Domiciliar']]
    X_CURSO_CBO.shape

    #Cursos por CBO
    #Indice =================================================================================================
    # X_CURSO_CBO['Ocupação_Código'] = X_CURSO_CBO['Ocupação_Código'].astype(int)  #comentado  em 12/08/2025 ... troca de arquivo de CBOs
    # dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['Ocupação_Código'] == int(str(cbo_num))].tolist() #comentado  em 12/08/2025 ... troca de arquivo de CBOs
    X_CURSO_CBO['CBO-Domiciliar'] = X_CURSO_CBO['CBO-Domiciliar'].astype(int)
    dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['CBO-Domiciliar'] == int(str(cbo_num))].tolist()
    # ...
    Curso_dir_curso_cbos = []
    Cbo_dir_curso_cbos = []
    for i in range(len(dir_curso_cbos)):
        #print(direito[i])
        curso = X_CURSO_CBO._get_value(dir_curso_cbos[i],'Curso_Superior_Graduação_Código')
        # cbo = X_CURSO_CBO._get_value(dir_curso_cbos[i],'Ocupação_Código') #comentado  em 12/08/2025 ... troca de arquivo de CBOs
        cbo = X_CURSO_CBO._get_value(dir_curso_cbos[i],'CBO-Domiciliar') 
        #print("Curso:",curso,"CBO:",str(int(cbo)))
        Curso_dir_curso_cbos.append(curso)
        Cbo_dir_curso_cbos.append(cbo)
    #..
    resultados_dir_curso_cbos=[]
    for i in range(len(Curso_dir_curso_cbos)):
      tupla=(Curso_dir_curso_cbos[i],Cbo_dir_curso_cbos[i])
      resultados_dir_curso_cbos.append(tupla)
    #...
    Curso_Cbo_dir_curso_cbos = pd.DataFrame(resultados_dir_curso_cbos)
    #Curso_Cbo_dir_curso_cbos.shape
    dict = {0:"Curso_Repet",
        1:"Cbo_Repet",
        }
    Curso_Cbo_dir_curso_cbos.rename(columns=dict,inplace=True)
    # print(Curso_Cbo_dir_curso_cbos)
    #Cursos Únicos por CBO ====================================================================================
    Curso_Cbo_dir_curso_cbos_unique = np.unique(Curso_Cbo_dir_curso_cbos.Curso_Repet)
    Curso_Unique = Curso_Cbo_dir_curso_cbos['Curso_Repet'].astype(int).tolist()
    #...
    Curso_Cbo_dir_curso_cbos['Curso_Repet'].value_counts().sort_index()
    #...
    from numpy.ma.core import sort
    A_dir_curso_cbos = Curso_Cbo_dir_curso_cbos['Curso_Repet'].value_counts().sort_index()
    #...
    A_dir_curso_cbos_sort = pd.DataFrame(A_dir_curso_cbos)
    #...
    A_Curso = A_dir_curso_cbos_sort.sort_values("Curso_Repet",ascending=False)
    # print("A_Curso",A_Curso) #30/07/2025
    Total = A_Curso['Curso_Repet'].sum()
    # print("Total",Total) #30/07/2025
    # if (porcent_param == 1):
    #     porcento = Total
    #     # print("porcento",porcento) #30/07/2025
    #     porcento_10 = round(porcento/Total, 2)
    #     # print("porcento_10",porcento_10) #30/07/2025
    #     # exit(0) #30/07/2025
    # else:
    porcento = Total*porcent_param
    # print("porcento",porcento) #30/07/2025
    porcento_10 = round(porcento/Total * 100, 2)
    # print("porcento_10",porcento_10) #30/07/2025
    # exit(0) #30/07/2025
    Porcentagem = []
    for i in range(len(A_Curso)):
        Porcentagem = round(A_Curso['Curso_Repet']/Total * 100, 2)
    A_Curso['Porcentagem'] = Porcentagem
    #...
    qtdade = 0
    A_Curso.index = A_Curso.index.astype(str)
    for i in range(len(A_Curso)):
        if (A_Curso.Porcentagem[i]>= porcento_10):
            qtdade = qtdade+1
    # print("A_Curso",A_Curso) #30/07/2025
    # print("qtdade",qtdade) #30/07/2025
    # exit(0) #30/07/2025 # Teste para saber se existem cursos para determinado CBO

    A_Curso_11 = A_Curso.iloc[:qtdade].copy()  # Garante uma cópia das 'qtdade' primeiras linhas para modificações posteriores
    # print("A_Curso_11",A_Curso_11) #30/07/2025
    # exit(0) #30/07/2025 # Teste para saber se existem cursos para determinado CBO
    if(len(A_Curso_11)>=1):
      #...
      #Coletando o nome dos Cursos ...
      NomeCurso = []
      for i in range(len(A_Curso_11)):
          curso=str(int(A_Curso_11.index[i]))
          # print("curso",curso)
          for indexx, row in CURSOS.iterrows():
              if (row['Cod_Curso'] == curso):
              #if(row['Cod_Curso'] == A_Curso_10.index[i]):
                  NomeCurso.append(row['Nome_Curso'])
                  #print(row['Cod_Curso'],":",row['Nome_Curso'])
      #...
      NomeCurso = pd.DataFrame(NomeCurso, columns=['Nome_Curso'])
      #...
      import warnings
      # print(A_Curso_11)
      # print("")
      # print(NomeCurso)
      # exit(0)
    #   print("A_Curso_11",A_Curso_11) #30/07/2025
    #   print("NomeCurso",NomeCurso) #30/07/2025
    #   exit(0) #30/07/2025
    #   A_Curso_11['Nome'] = NomeCurso['Nome_Curso'].values
      A_Curso_11['Nome'] = NomeCurso['Nome_Curso'].values[:len(A_Curso_11)] #Essa linha foi adaptada para permitir rodar o codigo com porcentagem 100%
        #...
      A_Curso_11.reset_index(inplace=True)
      A_Curso_11 = A_Curso_11.rename(columns = {'index':'Curso'})
      A_Curso_11['Curso'] = A_Curso_11['Curso'].astype("float").astype('str')
      A_Curso_11['Curso_Nome'] = A_Curso_11['Curso'].str.cat(A_Curso_11['Nome'], sep =" ")
      
      primeiros = []
      if (len(A_Curso_11)<1):
          print("Não existem cursos para este CBO..")
        #   exit(0)
      else:
          for i in range(len(A_Curso_11)): #Alterado em 09/09/2023 para pegar o 4º Elemento
              primeiros.append(int(float(A_Curso_11.Curso[i])))
      A_Curso_11_sort = A_Curso_11.iloc[0:qtdade].sort_values("Porcentagem",ascending=True)  #26/09
      index =  A_Curso_11_sort.index
      colors = []
      for i in range(len(index)):
          colors.append('black')
            
      # tituloalterado = titulo3 + " : " + "Cbo fraco"
      tituloalterado = titulo3 + " : " + "Weak CBO"    
      curso_num = str(float(curso_num))
      
      intensidade = 'Fraco'     
      for i in range(len(index)):
          if ((A_Curso_11_sort.index[i]==0)and(A_Curso_11_sort['Curso'].iloc[i]==str(curso_num))): #curso_num
              # tituloalterado = titulo3 + " : " + "Cbo forte"
              tituloalterado = titulo3 + " : " + "Strong Cbo"
              intensidade ='Forte'
              break
      cursos = [] # Alterado em 26/09/2023
      if (len(A_Curso_11)<1):
         print("Não existe CBOs para este curso..")
        #  sys.exit() #===============================================================================================
      else:
          for i in range(len(A_Curso_11)):
              cursos.append(A_Curso_11.Curso[i])
      nomes = [] # Alterado em 26/09/2023
      if (len(A_Curso_11)<1):
          print("Não existe CBOs para este curso..")
        #   sys.exit() #===============================================================================================
      else:
          for i in range(len(A_Curso_11)):
              nomes.append(A_Curso_11.Nome[i])
      porcentagens = []
      if (len(A_Curso_11)<1):
          print("Não existe CBOs para este curso..")
        #   sys.exit() #===============================================================================================
      else:
          for i in range(len(A_Curso_11)):
              porcentagens.append(A_Curso_11.Porcentagem[i])
      x='Curso_Nome'
      y='Porcentagem'
      plt.rcParams["figure.figsize"] = (18, 8)
      plt.rcParams["figure.autolayout"] = True
      ax = A_Curso_11_sort.plot(x,y,kind='barh',title=tituloalterado,color=colors,legend=False)
      ax.bar_label(ax.containers[0])
      # plt.xlabel("Porcentagem")
      plt.xlabel("Percentage")
      plt.ylabel("CBO_Name")
      # string = str(curso_num) + " - " + curso_nome + " : " + primeirosCbos_Nome[numero] + "_" + str(porcent_param) +".pdf"
      string = str(curso_num) + " - " + curso_nome + " : " + primeirosCbos_Nome[numero] + "_" + str(porcent_param) +".png"
      save_results_to =  'graficos/'   
      plt.savefig(save_results_to + string)
      volta = 'Volta'
    else:
       print("Não existe cursos para esse CBO..")
       # exit(0)
       intensidade = "0"
       string = ""
       cursos = "0"
       nomes = "0"
       porcentagens = "0"
    # print(cbo_num,curso_nome,primeirosCbos_Nome,intensidade,plt,string,cursos,nomes,porcentagens)   
    # exit()
    return cbo_num,curso_nome,primeirosCbos_Nome,intensidade,plt,string,cursos,nomes,porcentagens
  

def Cursos_CBO_13_10(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo3,NaoGraduados_qtdade,Graduados_Nao_Total,curso_num,curso_nome,primeirosCbos_Nome,i,porcent_param,save_results_to):
    numero = i
    #Leitura de Arquivos CSVs ...
    X = pd.read_csv(csv_estado)
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    CURSOS = pd.read_csv(csv_CURSOS, dtype ='str')
    # drop the 'Unnamed:0' column
    # CBO = CBO.drop(columns=['Unnamed: 0'])  #comentado  em 12/08/2025 ... troca de arquivo de CBOs
    CURSOS = CURSOS.drop(columns=['Unnamed: 0'])
    
    #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
    # X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']] #comentado  em 12/08/2025 ... troca de arquivo de CBOs
    X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','CBO-Domiciliar']]

    X_CURSO_CBO.shape

    #Cursos por CBO
    #Indice =================================================================================================
    # X_CURSO_CBO['Ocupação_Código'] = X_CURSO_CBO['Ocupação_Código'].astype(int)  #comentado  em 12/08/2025 ... troca de arquivo de CBOs
    # dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['Ocupação_Código'] == int(str(cbo_num))].tolist()  #comentado  em 12/08/2025 ... troca de arquivo de CBOs
    X_CURSO_CBO['CBO-Domiciliar'] = X_CURSO_CBO['CBO-Domiciliar'].astype(int) 
    dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['CBO-Domiciliar'] == int(str(cbo_num))].tolist()  
    # dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['Ocupação_Código'] == cbo_num].tolist()
    # ...
    Curso_dir_curso_cbos = []
    Cbo_dir_curso_cbos = []
    for i in range(len(dir_curso_cbos)):
        #print(direito[i])
        curso = X_CURSO_CBO._get_value(dir_curso_cbos[i],'Curso_Superior_Graduação_Código')
        # cbo = X_CURSO_CBO._get_value(dir_curso_cbos[i],'Ocupação_Código') #comentado  em 12/08/2025 ... troca de arquivo de CBOs
        cbo = X_CURSO_CBO._get_value(dir_curso_cbos[i],'CBO-Domiciliar') 
        #print("Curso:",curso,"CBO:",str(int(cbo)))
        Curso_dir_curso_cbos.append(curso)
        Cbo_dir_curso_cbos.append(cbo)
    #..
    resultados_dir_curso_cbos=[]
    for i in range(len(Curso_dir_curso_cbos)):
      tupla=(Curso_dir_curso_cbos[i],Cbo_dir_curso_cbos[i])
      resultados_dir_curso_cbos.append(tupla)
    #...
    Curso_Cbo_dir_curso_cbos = pd.DataFrame(resultados_dir_curso_cbos)
    #Curso_Cbo_dir_curso_cbos.shape
    dict = {0:"Curso_Repet",1:"Cbo_Repet",}
    Curso_Cbo_dir_curso_cbos.rename(columns=dict,inplace=True)
    #Cursos Únicos por CBO ====================================================================================
    Curso_Cbo_dir_curso_cbos_unique = np.unique(Curso_Cbo_dir_curso_cbos.Curso_Repet)
    Curso_Unique = Curso_Cbo_dir_curso_cbos['Curso_Repet'].astype(int).tolist()
    #...
    Curso_Cbo_dir_curso_cbos['Curso_Repet'].value_counts().sort_index()
    #...
    from numpy.ma.core import sort
    A_dir_curso_cbos = Curso_Cbo_dir_curso_cbos['Curso_Repet'].value_counts().sort_index()
    A_dir_curso_cbos_sort = pd.DataFrame(A_dir_curso_cbos)
    #...
    A_Curso = A_dir_curso_cbos_sort.sort_values("Curso_Repet",ascending=False)
    Total = A_Curso['Curso_Repet'].sum()
    porcento = Total*porcent_param
    porcento_10 = round(porcento/Total * 100, 2)
    Porcentagem = []
    for i in range(len(A_Curso)):
        Porcentagem = round(A_Curso['Curso_Repet']/Total * 100, 2)
    A_Curso['Porcentagem'] = Porcentagem
    qtdade = 0
    A_Curso.index = A_Curso.index.astype(str)
    for i in range(len(A_Curso)):
        if (A_Curso.Porcentagem[i]>= porcento_10):
            qtdade = qtdade+1
    A_Curso_11 = A_Curso.head(qtdade) #Alterado 29/09/2023   =========================
    # print("A_Curso_11================================================================")
    # print(A_Curso_11)


    if(len(A_Curso_11)>=1):
        NomeCurso = []
        for i in range(len(A_Curso_11)):
            curso=str(int(A_Curso_11.index[i]))
            for indexx, row in CURSOS.iterrows():
                if (row['Cod_Curso'] == curso):
                #if(row['Cod_Curso'] == A_Curso_10.index[i]):
                    NomeCurso.append(row['Nome_Curso'])
                    #print(row['Cod_Curso'],":",row['Nome_Curso'])
        # print("NomeCurso ================================================================")
        # print(NomeCurso)            
        #...
        #import pandas as pd
        #list_name = ['item_1', 'item_2', 'item_3', ...]
        NomeCurso = pd.DataFrame(NomeCurso, columns=['Nome_Curso'])
        # ...
        A_Curso_11["Nome"] = 1
        import warnings
        for i in range(len(A_Curso_11)):
            # A_Curso_11['Nome'][i] = NomeCurso.Nome_Curso[i]
            A_Curso_11['Nome'].iloc[i]= NomeCurso['Nome_Curso'].iloc[i]
            
        #...
        A_Curso_11.reset_index(inplace=True)
        A_Curso_11 = A_Curso_11.rename(columns = {'index':'Curso'})
        #A_Curso_11
        A_Curso_11['Curso'] = A_Curso_11['Curso'].astype("float").astype('str')
        #type(A_Curso_11.Curso )
        A_Curso_11['Curso_Nome'] = A_Curso_11['Curso'].str.cat(A_Curso_11['Nome'], sep =" ")
        # print("A_Curso_11 ================================================================")
        # print(A_Curso_11)  

        qtdadenv=qtdade
        
        A_Curso_11.loc[qtdade] = [0,0,0,0,0]
        
        A_Curso_11['Curso'].iloc[qtdade]= 0
        A_Curso_11['Curso_Repet'].iloc[qtdade]= NaoGraduados_qtdade
        A_Curso_11['Nome'].iloc[qtdade]= "Não-Graduados"
        A_Curso_11['Curso_Nome'].iloc[qtdade]= "Não-Graduados"
        
        A_Curso_11['Porcentagem'].iloc[qtdade]= round(NaoGraduados_qtdade/Graduados_Nao_Total * 100, 2) #26/09
        # print("A_Curso_11 ================================================================")
        # print(A_Curso_11)  

        primeiros = []
        if (len(A_Curso_11)<1):
            print("Não existem cursos para este CBO")
        else:
            for i in range(len(A_Curso_11)): #Alterado em 09/09/2023 para pegar o 4º Elemento
                primeiros.append(int(float(A_Curso_11.Curso[i])))
        # print("primeiros ================================================================")
        # print(primeiros)        
        #...
        
        A_Curso_11_sort = A_Curso_11.iloc[0:qtdadenv+1].sort_values("Porcentagem",ascending=True)  #26/09
        
        index =  A_Curso_11_sort.index
        # print("index")
        # print(len(index))

        colors = []
        for i in range(len(index)):
            if (A_Curso_11_sort['Curso'].iloc[i]==0):
                colors.append('red')
            else:
                colors.append('black')
        # print("colors ================================================================")
        # print(colors)

        #tituloalterado = titulo3 + " : " + "Cbo fraco"
        tituloalterado = titulo3 + " : " + "Weak Cbo"
        curso_num = str(float(curso_num))
        
        intensidade = 'Fraco'
        for i in range(len(index)):
            # print("index =================================================================",index)
            if ((A_Curso_11_sort.index[i]==0)and(A_Curso_11_sort['Curso'].iloc[i]==str(curso_num))): #curso_num
                #colors = ['blue', 'blue', 'blue','green'] #1ª posição
                #tituloalterado = titulo3 + " : " + "Cbo forte"
                tituloalterado = titulo3 + " : " + "Strong Cbo"
                intensidade ='Forte'
                # break

            cursos = [] # Alterado em 26/09/2023
            if (len(A_Curso_11)<1):
              #for i in range(len(A_cbo_10)):
              #    nomes.append(A_cbo_10.CBO_Nome[i])
              print("Não existe CBOs para este curso")
            #   sys.exit() #===============================================================================================
            else:
                for i in range(len(A_Curso_11)):
                    cursos.append(A_Curso_11.Curso[i])
            # print("cursos ================================================================")
            # print(cursos)      

            nomes = [] # Alterado em 26/09/2023
            if (len(A_Curso_11)<1):
                #for i in range(len(A_cbo_10)):
                #    nomes.append(A_cbo_10.CBO_Nome[i])
                print("Não existe CBOs para este curso")
                # sys.exit() #===============================================================================================
            else:
                for i in range(len(A_Curso_11)):
                    nomes.append(A_Curso_11.Nome[i])
            # print("nomes ================================================================")
            # print(nomes)

            porcentagens = []
            if (len(A_Curso_11)<1):
                #for i in range(len(A_cbo_10)):
                #    nomes.append(A_cbo_10.CBO_Nome[i])
                print("Não existe CBOs para este curso")
                # sys.exit() #===============================================================================================
            else:
                for i in range(len(A_Curso_11)):
                    porcentagens.append(A_Curso_11.Porcentagem[i])
            # print("porcentagens ================================================================")
            # print(porcentagens)     
       

        x='Curso_Nome'
        y='Porcentagem'
        
        ax = A_Curso_11_sort.plot(x,y,kind='barh',title=tituloalterado,color=colors,legend=False)

        ax.bar_label(ax.containers[0])
        # plt.xlabel("Porcentagem")
        plt.xlabel("Percentage")
        plt.ylabel("CBO_Name")
        
        # string = str(curso_num) + " - " + curso_nome + " : " + primeirosCbos_Nome[numero] + "_" + str(porcent_param) +".pdf"
        string = str(curso_num) + " - " + curso_nome + " : " + primeirosCbos_Nome[numero] + "_" + str(porcent_param) +".png"
        save_results_to = 'graficos/'  
        plt.savefig(save_results_to + string)        
    else:
       print("Não existe cursos para esse CBO")
       cursos=0
       nomes=0
       porcentagens=0
       return cbo_num,curso_nome,primeirosCbos_Nome,intensidade,plt,string, cursos, nomes, 
    return cbo_num,curso_nome,primeirosCbos_Nome,intensidade,plt,string, cursos, nomes, porcentagens

# https://colab.research.google.com/drive/1UCEDMTAdZqIRaNGpXHN66pqq_IwHyAe7?authuser=1#scrollTo=vC50rzZCwdHj
def relacionamentos_fortes_naofortes_cursos_profissoes_plot1(path,name,path1,name1):
    csv_estado = os.path.join(path[0],name[0]) # arquivo do censo do Brasil inteiro (somente graduados)
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)
    csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
    csv_CURSOS = os.path.join(path1[0],name1[2]) # Tabela de Cursos
    path2 = ibge_variable.paths(8)
    name2 = ibge_variable.names(8)         
    csv_PivotTableFinal =  os.path.join(path2[0],name2[0]) #Pivo Table Final

    CursosCenso = ibge_cursos_filter(path1[0],name1[2])
    # print(CursosCenso.head(50))
    # 33 ... direito // 43 ... computação
    curso_num  = float(CursosCenso.curso_num.iloc[74])
    curso_nome = CursosCenso.curso_nome.iloc[74]
    titulo10 =  "Curso:  " +  str(curso_num) + ": " + curso_nome + " - Os 10 maiores"
    titulo3  =  "Curso:  " +  str(curso_num) + ": " + curso_nome + " - Os 3 maiores"
    save_results_to = 'graficos/'  

    # 27/04/2024 ==================================================================
    # CBOs por Curso ...
    # Plota os 10 maiores CBOs Curso
    # Plota os 3 maiores CBOs por curso
    # Validação para chamar somente os CBOs da Familia 1 e 2
    # Retorna os três primeiros CBOs, os três primeiros CBOs acompanhado dos respectivos nomes, o numero do Curso, e o nome do Curso 
    primeirosCbos,primeirosCbos_Nome,CURSO_NUM,CURSO_NOME=CBOs_Curso(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,save_results_to)
    # Cursos por CBO ...
    NaoGraduados = NaoGraduados_PivotTable(primeirosCbos, csv_PivotTableFinal)
    # Acha CBOs por Curso ...
    # Define forte ou Fraco via Código
    # Plota Não-Graduados em Cor Diferente - Verde (3 primeiros cursos plotando Não-Graduados)
    Curso,PrimeirosCbos_Nome,intensidade = Plot_Cursos_CBOs_11(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos_Nome,primeirosCbos,NaoGraduados,curso_num,curso_nome)
       
    
# https://colab.research.google.com/drive/1UCEDMTAdZqIRaNGpXHN66pqq_IwHyAe7?authuser=1#scrollTo=vC50rzZCwdHj
def relacionamentos_fortes_naofortes_cursos_profissoes_plot2(path,name,path1,name1):
    csv_estado = os.path.join(path[0],name[0]) # arquivo do censo do Brasil inteiro (somente graduados)
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)
    csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
    csv_CURSOS = os.path.join(path1[0],name1[2]) # Tabela de Cursos
    path2 = ibge_variable.paths(8)
    name2 = ibge_variable.names(8)         
    csv_PivotTableFinal =  os.path.join(path2[0],name2[0]) #Pivo Table Final

    CursosCenso = ibge_cursos_filter(path1[0],name1[2])
    curso_num  = float(CursosCenso.curso_num.iloc[43])
    curso_nome = CursosCenso.curso_nome.iloc[43]
    titulo10 =  "Course:  " +  str(curso_num) + ": " + curso_nome + " - Os 10 maiores"
    # titulo3  =  "Curso:  " +  str(curso_num) + ": " + curso_nome + " - Os 3 maiores"
    titulo3  =  "Course:  " +  str(curso_num) + ": " + curso_nome 

    save_results_to = 'graficos/'  

           
    # 28/04/2024 ==================================================================   
    # Plota os 3 maiores CBOs por curso
    # Validação para chamar somente os CBOs da Familia 1 e 2
    # Retorna os três primeiros CBOs, os três primeiros CBOs acompanhado dos respectivos nomes, o numero do Curso, e o nome do Curso
    # save_results_to
    primeirosCbos,primeirosCbos_Nome,Porcentagens,CURSO_NUM,CURSO_NOME=CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0.07,save_results_to)
    # CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0.1,save_results_to)
    # NaoGraduados_PivotTable_2(primeirosCbos, csv_PivotTableFinal)
    primeirosCbos,NaoGraduados,Graduados_Nao,Graduados = NaoGraduados_PivotTable_2(primeirosCbos, csv_PivotTableFinal)
    #=====================================================Plotando os cursos de determinado cbo, sem função e salvando os plots ...
    Intensidade = []
    Porcentagens_vol = []
    CBO_vol = []
    Cursos_vol = []
    Nomes_vol  = []
    for i in range (len(primeirosCbos)):
        titulo3=primeirosCbos_Nome[i]
        if(int(float(primeirosCbos[i]))>=2000):
            # Acha CBOs por Curso
            # Define forte ou Fraco via Código
            # Plota Não-Graduados em Cor Diferente - Verde
            # save_results_to
            CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_14_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.07)
            Intensidade.append(intensidade)
            Porcentagens_vol.append(porcentagens_vol)
            CBO_vol.append(CBO)
            Cursos_vol.append(cursos_vol)
            Nomes_vol.append(nomes_vol)
        else:
            # Acha CBOs por Curso
            # Define forte ou Fraco via Código
            # Plota Não-Graduados em Cor Diferente - Verde
            # save_results_to
            CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_13_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],Graduados_Nao[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.07,save_results_to)
            Intensidade.append(intensidade)
            Porcentagens_vol.append(porcentagens_vol)
            CBO_vol.append(CBO)
            Cursos_vol.append(cursos_vol)
            Nomes_vol.append(nomes_vol)    
# https://colab.research.google.com/drive/1UCEDMTAdZqIRaNGpXHN66pqq_IwHyAe7?authuser=1#scrollTo=vC50rzZCwdHj
def relacionamentos_fortes_naofortes_cursos_profissoes_plot10(path,name,path1,name1):
    csv_estado = os.path.join(path[0],name[0]) # arquivo do censo do Brasil inteiro (somente graduados)
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)
    csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
    csv_CURSOS = os.path.join(path1[0],name1[2]) # Tabela de Cursos
    path2 = ibge_variable.paths(8)
    name2 = ibge_variable.names(8)         
    csv_PivotTableFinal =  os.path.join(path2[0],name2[0]) #Pivo Table Final

    CursosCenso = ibge_cursos_filter(path1[0],name1[2])
    # 
    curso_num  = float(CursosCenso.curso_num.iloc[43]) # Ciência da Computação
    # 
    curso_nome = CursosCenso.curso_nome.iloc[43]
    # curso_num  = float(CursosCenso.curso_num.iloc[19]) #Psicologia
    # curso_nome = CursosCenso.curso_nome.iloc[19]
    # curso_num  = float(CursosCenso.curso_num.iloc[68]) #Odontologia
    # curso_nome = CursosCenso.curso_nome.iloc[68]
    # curso_num  = float(CursosCenso.curso_num.iloc[2])  #FORMAÇÃO DE PROFESSORES DE EDUCAÇÃO INFANTIL
    # curso_nome = CursosCenso.curso_nome.iloc[2]
    curso_num  = float(CursosCenso.curso_num.iloc[70]) # 
    curso_nome = CursosCenso.curso_nome.iloc[70]

    titulo10 =  "Curso:  " +  str(curso_num) + ": " + curso_nome + " - Os 10 maiores"
    # titulo3  =  "Curso:  " +  str(curso_num) + ": " + curso_nome + " - Os 3 maiores"
    titulo3  =  "Course:  " +  str(curso_num) + ": " + curso_nome    
    save_results_to = 'graficos/'  

           
    # 28/04/2024 ==================================================================   
    # Plota os 3 maiores CBOs por curso
    # Validação para chamar somente os CBOs da Familia 1 e 2
    # Retorna os três primeiros CBOs, os três primeiros CBOs acompanhado dos respectivos nomes, o numero do Curso, e o nome do Curso
    # save_results_to
    primeirosCbos,primeirosCbos_Nome,Porcentagens,CURSO_NUM,CURSO_NOME=CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0.07,save_results_to)
    # CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0.1,save_results_to)
    # NaoGraduados_PivotTable_2(primeirosCbos, csv_PivotTableFinal)
    primeirosCbos,NaoGraduados,Graduados_Nao,Graduados = NaoGraduados_PivotTable_2(primeirosCbos, csv_PivotTableFinal)
    #=====================================================Plotando os cursos de determinado cbo, sem função e salvando os plots ...
    Intensidade = []
    Porcentagens_vol = []
    CBO_vol = []
    Cursos_vol = []
    Nomes_vol  = []
    for i in range (len(primeirosCbos)):
        titulo3=primeirosCbos_Nome[i]
        if(int(float(primeirosCbos[i]))>=2000):
            # Acha CBOs por Curso
            # Define forte ou Fraco via Código
            # Plota Não-Graduados em Cor Diferente - Verde
            # save_results_to
            CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_14_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.07)
            Intensidade.append(intensidade)
            Porcentagens_vol.append(porcentagens_vol)
            CBO_vol.append(CBO)
            Cursos_vol.append(cursos_vol)
            Nomes_vol.append(nomes_vol)
        else:
            # Acha CBOs por Curso
            # Define forte ou Fraco via Código
            # Plota Não-Graduados em Cor Diferente - Verde
            # save_results_to
            CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_13_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],Graduados_Nao[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.07,save_results_to)
            Intensidade.append(intensidade)
            Porcentagens_vol.append(porcentagens_vol)
            CBO_vol.append(CBO)
            Cursos_vol.append(cursos_vol)
            Nomes_vol.append(nomes_vol)   

def AcharFortes_Fracos(Curso,PrimeirosCbos_Nome,intensidade):
    nomes_Fortes=[]
    nomes_Fracos=[]
    cbos_Fortes=[]
    cbos_Fracos=[]
    for i in range(len(PrimeirosCbos_Nome)):
        if (intensidade[i] == 'Forte'):
            tupla=(PrimeirosCbos_Nome[i])
            nomes_Fortes.append(tupla)
            cbos_Fortes.append(intensidade[i])
        if (intensidade[i] == 'Fraco'):
            tupla_fraca =(PrimeirosCbos_Nome[i])
            nomes_Fracos.append(tupla_fraca)
            cbos_Fracos.append(intensidade[i])
    return nomes_Fortes,cbos_Fortes,nomes_Fracos,cbos_Fracos   

def tabela(i,j,nomes_Fortes,cbos_Fortes,nomes_Fracos,cbos_Fracos,Tabela_Certa):
    if (len(cbos_Fortes)>=1):
        if (cbos_Fortes[i] == 'Forte'):
            Tabela_Certa.Forte1.loc[j] = nomes_Fortes[i]
        if (len(cbos_Fortes)>1):
            if (cbos_Fortes[i+1] == 'Forte'):
                Tabela_Certa.Forte2.loc[j] = nomes_Fortes[i+1]
            if (len(cbos_Fortes)>2):
                if (cbos_Fortes[i+2] == 'Forte'):
                    Tabela_Certa.Forte3.loc[j] = nomes_Fortes[i+2]

    #i= 0 #Fracos ...
    if (len(cbos_Fracos)>=1):
        if (cbos_Fracos[i] == 'Fraco'):
            Tabela_Certa.Fraco1.loc[j] = nomes_Fracos[i]
        if (len(cbos_Fracos)>1):
            if (cbos_Fracos[i+1] == 'Fraco'):
                Tabela_Certa.Fraco2.loc[j] = nomes_Fracos[i+1]
            if (len(cbos_Fracos)>2):
                if (cbos_Fracos[i+2] == 'Fraco'):
                    Tabela_Certa.Fraco3.loc[j] = nomes_Fracos[i+2]
    # print("")
    # Tabela_Certa

    left_aligned_df = Tabela_Certa.style.set_properties(**{'text-align': 'center'})
    left_aligned_df = left_aligned_df.set_table_styles([dict(selector = 'th', props=[('text-align', 'left')])])

    left_aligned_df
    return left_aligned_df


def Tabela_Censo_CbosFortes_Fracos_Familia1_Familia2(path,name,path1,name1):
    logging.info(" Gerando a tabela de onde trabalham as pessoas recenseadas")   
    csv_estado = os.path.join(path[0],name[0]) # arquivo do censo do Brasil inteiro (somente graduados)
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)
    csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
    csv_CURSOS = os.path.join(path1[0],name1[2]) # Tabela de Cursos
    path2 = ibge_variable.paths(8)
    name2 = ibge_variable.names(8)         
    csv_PivotTableFinal =  os.path.join(path2[0],name2[0]) #Pivo Table Final

    CursosCenso = ibge_cursos_filter(path1[0],name1[2])
    # print(len(CursosCenso))
    curso_num  = float(CursosCenso.curso_num.iloc[43])
    curso_nome = CursosCenso.curso_nome.iloc[43]
    titulo10 =  "Curso:  " +  str(curso_num) + ": " + curso_nome + " - Os 10 maiores"
    titulo3  =  "Curso:  " +  str(curso_num) + ": " + curso_nome + " - Os 3 maiores"
    save_results_to = 'graficos/'  

    for j in range(0,88):
        curso_num= float(CursosCenso.curso_num.iloc[j])
        curso_nome= CursosCenso.curso_nome.iloc[j]
        titulo10= "Curso " +  CursosCenso.curso_num.iloc[j] + ": " + CursosCenso.curso_nome.iloc[j] + " - 10% "
        titulo3=  "Curso " +  CursosCenso.curso_num.iloc[j] + ": " + CursosCenso.curso_nome.iloc[j] + " - 10%"
        print("curso_num:", curso_num, "curso_nome:",curso_nome)
        print(j)
        print("")
        #======================================================Plotando os cbos de determinado curso, usando função ...
        primeirosCbos,primeirosCbos_Nome,Porcentagens,CURSO_NUM,CURSO_NOME=CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0.1,save_results_to)
        if (primeirosCbos!=0)&(primeirosCbos!=0)&(Porcentagens!=0):
            #======================================================Achando a quantidade de Não-Graduados na PivotTable
            primeirosCbos,NaoGraduados,Graduados_Nao,Graduados = NaoGraduados_PivotTable_2(primeirosCbos, csv_PivotTableFinal)
            #=====================================================Plotando os cursos de determinado cbo, sem função e salvando os plots ...
            Intensidade = []
            Porcentagens_vol = []
            CBO_vol = []
            Cursos_vol = []
            Nomes_vol  = []
            for i in range (len(primeirosCbos)):
                titulo3=primeirosCbos_Nome[i]
                if(int(float(primeirosCbos[i]))>=2000):
                    CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_14_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.1)
                    Intensidade.append(intensidade)
                    Porcentagens_vol.append(porcentagens_vol)
                    CBO_vol.append(CBO)
                    Cursos_vol.append(cursos_vol)
                    Nomes_vol.append(nomes_vol)
                else:
                    CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_13_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],Graduados_Nao[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.1,save_results_to)
                    Intensidade.append(intensidade)
                    Porcentagens_vol.append(porcentagens_vol)
                    CBO_vol.append(CBO)
                    Cursos_vol.append(cursos_vol)
                    Nomes_vol.append(nomes_vol)                


            #==================================================================Colocando Ida e Volta no mesmo grafico
            # ...
            if(j==0): #Se for imprimindo desde o inicio
                data = pd.DataFrame()
                Tabela_Certa = pd.DataFrame(data, columns=['Curso','Forte1','Forte2','Forte3','Fraco1','Fraco2','Fraco3'])
                
            PrimeirosCbos_Nome = tresprimeirosCursos
            nomes_Fortes,cbos_Fortes,nomes_Fracos,cbos_Fracos = AcharFortes_Fracos(Curso,PrimeirosCbos_Nome,Intensidade)
            i=0
            Tabela_Certa.loc[j] = [curso_nome, '-','-', '-','-', '-','-']
            Tabela =  tabela(i,j,nomes_Fortes,cbos_Fortes,nomes_Fracos,cbos_Fracos,Tabela_Certa)
            # display(Tabela)
    Tabela.to_excel(save_results_to + 'OndeTrabalhamAsPessoasDeCadaCursoDoCenso.xlsx')
    return 
           
#Função para achar os pontos da Ida
def Ida(primeirosCbos,CURSO_NUM,Porcentagens,comeco,x_,y_,z_,v_):
    if (comeco ==1):
        x = []
        y = []
        z = []
        v = []
        #print(x,y,z)
        #sys.exit()
        for i in range(len(primeirosCbos)):
              x.append(primeirosCbos[i])
              y.append(CURSO_NUM)
              z.append(Porcentagens[i])
              v.append(0)
    else:
         x = x_
         y = y_
         z = z_
         v = v_
         for i in range(len(primeirosCbos)):
              x.append(primeirosCbos[i])
              y.append(CURSO_NUM)
              z.append(Porcentagens[i])
              v.append(0)
    return x,y,z,v

#Função para achar os pontos da volta
def Volta(cursos_vol,CBO,porcentagens_vol, comeco,x_,y_,z_,v_):
    if (comeco ==1):
        x = []
        y = []
        z = []
        v = []
        for i in range(len(cursos_vol)):
            x.append(CBO)
            y.append(cursos_vol[i])
            z.append(0)
            v.append(porcentagens_vol[i])
    else:
         x = x_
         y = y_
         z = z_
         v = v_
         for i in range(len(cursos_vol)):
              x.append(CBO)
              y.append(cursos_vol[i])
              z.append(0)
              v.append(porcentagens_vol[i])

    return x,y,z,v

# Função para passar os pontos para o dataframe
def x_y_z_v_df(x,y,z,v):
    result=[]
    for i in range(len(x)):
      tupla=(x[i],y[i],z[i],v[i])
      result.append(tupla)
    #...
    df = pd.DataFrame(result)
    #Curso_Cbo_dir_curso_cbos.shape
    dicion = {0:"CB",
        1:"CR",
        2:"Ida",
        3:"Volta",
        }
    df.rename(columns=dicion,inplace=True)
    return df

def Jun_Ida_Volta(X_,Y_,Z_,V_,CBO_VOL,CURSO_NUM):
    for i in range(len(V_)):
        #print("")
        #print('i', i)
        j=i+1
        #print("j:",j)
        if (X_[i]==CBO_VOL) and (Y_[i] == CURSO_NUM) and (V_[i]==0):
            #print(X_[i],Y_[i],Z_[i],V_[i])
            CB = CBO_VOL
            CR = CURSO_NUM
            for j in range(j, len(V_)):
                  if (X_[j]== CB) and (float(Y_[j]) == CR) and (int(Z_[j])==0):
                        #print(X_[j],Y_[j],Z_[j],V_[j])
                        #print('V[i] = V[j]',V_[i],V_[j])
                        #print('Z[j] = Z[i]',Z_[j],Z_[i])
                        V_[i] = V_[j]
                        Z_[j] = Z_[i]
                        #return
                        break
    return

def Ida_Volta(path,name,path1,name1):

    logging.info(" Gerando as idas e voltas")   
    csv_estado = os.path.join(path[0],name[0]) # arquivo do censo do Brasil inteiro (somente graduados)
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)
    csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
    csv_CURSOS = os.path.join(path1[0],name1[2]) # Tabela de Cursos
    path2 = ibge_variable.paths(8)
    name2 = ibge_variable.names(8)         
    csv_PivotTableFinal =  os.path.join(path2[0],name2[0]) #Pivo Table Final

    CursosCenso = ibge_cursos_filter(path1[0],name1[2])
    # print(len(CursosCenso))
    # exit(0)
    # curso_num  = float(CursosCenso.curso_num.iloc[88])
    # curso_nome = CursosCenso.curso_nome.iloc[88]
    # titulo10 =  "Curso:  " +  str(curso_num) + ": " + curso_nome + " - Os 10 maiores"
    # titulo3  =  "Curso:  " +  str(curso_num) + ": " + curso_nome + " - Os 3 maiores"
    # print(curso_num)
    # print(curso_nome)
    # print(titulo10)
    # print(titulo3)
    # Inserir comando para criar a pasta ida
    save_results_to = 'graficos/'  
    # N = 1 # Variável para controlar se existe cursos ou não
    # Testar curso 79,80,85...
    for f in range(0,60):
    #   if (f==83):
    #     f=f+1 # Pular o curso 83, que não tem CBOs. curso_num: 852.0 curso_nome: AMBIENTES NATURAIS E VIDA SELVAGEM
    #   if (f==88):
    #     f=f+1 # Pular o curso 88. curso_num: 863.0 curso_nome: SETOR MILITAR E DE DEFESA
    #   else:    
        curso_num= float(CursosCenso.curso_num.iloc[f])
        curso_nome= CursosCenso.curso_nome.iloc[f]
        titulo10= "Course " +  CursosCenso.curso_num.iloc[f] + ": " + CursosCenso.curso_nome.iloc[f] + " - 10% "
        titulo3=  "Course " +  CursosCenso.curso_num.iloc[f] + ": " + CursosCenso.curso_nome.iloc[f] + " - 10%"
        print("=================================================================================================")
        print("curso_num:", curso_num, "curso_nome:",curso_nome)
        print(f)
        
        #======================================================Plotando os cbos de determinado curso, usando função ...
        #10%
        primeirosCbos,primeirosCbos_Nome,Porcentagens,CURSO_NUM,CURSO_NOME=CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0.1,save_results_to)
        # 100%
        # primeirosCbos,primeirosCbos_Nome,Porcentagens,CURSO_NUM,CURSO_NOME=CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0,save_results_to)

        if (primeirosCbos!=0)&(primeirosCbos!=0)&(Porcentagens!=0):
            #======================================================Achando a quantidade de Não-Graduados na PivotTable
            primeirosCbos,NaoGraduados,Graduados_Nao,Graduados = NaoGraduados_PivotTable_2(primeirosCbos, csv_PivotTableFinal)
            #=====================================================Plotando os cursos de determinado cbo, sem função e salvando os plots ...
            Intensidade = []
            Porcentagens_vol = []
            CBO_vol = []
            Cursos_vol = []
            Nomes_vol  = []
            # print("primeirosCbos:", primeirosCbos)
            # exit(0)
            for i in range (len(primeirosCbos)):
                titulo3=primeirosCbos_Nome[i]
                if(int(float(primeirosCbos[i]))>=2000):
                    #10%
                    CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_14_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.1)
                    #100%
                    # CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_14_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],curso_num,curso_nome,primeirosCbos_Nome,i,0)
                    if (cursos_vol!=0)&(nomes_vol!=0)&(porcentagens_vol!=0):
                      Intensidade.append(intensidade)
                      # print(intensidade)
                      Porcentagens_vol.append(porcentagens_vol)
                      CBO_vol.append(CBO)
                      Cursos_vol.append(cursos_vol)
                      Nomes_vol.append(nomes_vol)
                    else:
                        print("Não existe cursos para esse CBO")   
                        # N = 0
                else:
                    # print(primeirosCbos[i])
                    #10%
                    CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_13_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],Graduados_Nao[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.1,save_results_to)
                    #100%
                    # CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_13_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],Graduados_Nao[i],curso_num,curso_nome,primeirosCbos_Nome,i,0,save_results_to)
                    if (cursos_vol!=0)&(nomes_vol!=0)&(porcentagens_vol!=0):
                        Intensidade.append(intensidade)
                        Porcentagens_vol.append(porcentagens_vol)
                        CBO_vol.append(CBO)
                        Cursos_vol.append(cursos_vol)
                        Nomes_vol.append(nomes_vol)
                    else:
                        print("Não existe cursos para esse CBO")  
                        # N = 0

            # ======================================================Plotando os cbos de determinado curso, usando função ...
            # if N == "0":
            #     print("Não existem cursos para esse CBO")
            # else:
            #     # ==================================================================Colocando Ida e Volta no mesmo grafico
            if(f==0):
            #if(f==88):
                # Se for a primeira execução, tem que criar as listas ... e o paramentro da ida é 1
                #Recuperando as idas e voltas ...
                x_ = []
                y_ = []
                z_ = []
                v_ = []
                X_,Y_,Z_,V_= Ida(primeirosCbos,CURSO_NUM,Porcentagens,1,x_,y_,z_,v_)
                x_= X_
                y_= Y_
                z_= Z_
                v_= V_
                for i in range(len(primeirosCbos)):
                    X_,Y_,Z_,V_= Volta(Cursos_vol[i],primeirosCbos[i],Porcentagens_vol[i], 0,x_,y_,z_,v_)

                x_= X_
                y_= Y_
                z_= Z_
                v_= V_
                #df1 = x_y_z_v_df(X_,Y_,Z_,V_)
                #print(df1)
                #Juntando as idas e voltas ...
                for l in range(len(CBO_vol)):
                    Jun_Ida_Volta(X_,Y_,Z_,V_, CBO_vol[l],CURSO_NUM)
                #atribuição
                x_= X_
                y_= Y_
                z_= Z_
                v_= V_
            else:
                #Recuperando as idas e voltas ...
                X_,Y_,Z_,V_= Ida(primeirosCbos,CURSO_NUM,Porcentagens,0,x_,y_,z_,v_)
                x_= X_
                y_= Y_
                z_= Z_
                v_= V_
                for i in range(len(primeirosCbos)):
                    X_,Y_,Z_,V_= Volta(Cursos_vol[i],primeirosCbos[i],Porcentagens_vol[i], 0,x_,y_,z_,v_)

                x_= X_
                y_= Y_
                z_= Z_
                v_= V_
                #df1 = x_y_z_v_df(X_,Y_,Z_,V_)
                #print(df1)
                #Juntando as idas e voltas ...
                for l in range(len(CBO_vol)):
                    Jun_Ida_Volta(X_,Y_,Z_,V_, CBO_vol[l],CURSO_NUM)
                #atribuição
                x_= X_
                y_= Y_
                z_= Z_
                v_= V_

    df = x_y_z_v_df(x_,y_,z_,v_)  
    #10%  
    df.to_csv(save_results_to + '10Porcent_DF.csv')
    #100%
    # df.to_csv(save_results_to + '100Porcent_DF.csv')
    return           

def Tabela_Ida_Volta(path2,name2):
    # df =  os.path.join(path2[0],name2[1])
    df ='graficos/10Porcent_DF.csv' 
    # df ='graficos/100Porcent_DF.csv' 
    df1 = pd.read_csv(df)    
    save_results_to = 'graficos/'  


    # Remover_Voltas_semIdas_e_Idas_semVoltas
    # tive que passar tudo pra float porque tem valores menores do que 0 ...
    for i in range(len(df1)):
        if (df1['Ida'][i].astype('float')==0.00) & (df1['Volta'][i].astype('float')!=0.00):
            df1 = df1.drop(i)
        else:
            if (df1['Ida'][i].astype('float')!=0.00) & (df1['Volta'][i].astype('float')==0.00):
                df1 = df1.drop(i)
            else:
                if (df1['Ida'][i].astype('float')==0.00) & (df1['Volta'][i].astype('float')==0.00):
                    df1 = df1.drop(i)
    # Remover_Duplicados
    df1 = df1.drop_duplicates(subset=['Ida','Volta'])
    # Reset_Indice
    df1 = df1.reset_index(drop=True)
    # Salvar_Tabela
    # # 10%
    df1.to_csv(save_results_to + '10Porcent_DF_Limpo.csv')
    df1.to_excel(save_results_to + '10Porcent_DF_Limpo.xlsx')
    # # 100%
    # df1.to_csv(save_results_to + '100Porcent_DF_Limpo.csv')
    # df1.to_excel(save_results_to + '100Porcent_DF_Limpo.xlsx')
    return



