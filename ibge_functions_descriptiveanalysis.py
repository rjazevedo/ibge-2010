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
        # print(len(cursos.Cod_Curso[i]))
        if len(cursos.Cod_Curso[i]) >=5:
           CURSO.append(cursos.Cod_Curso[i])
           NOME.append(cursos.Nome_Curso[i])
           #print(cursos.Cod_Curso[i])     
              
    Cursos_Censo=[]
    for i in range(len(CURSO)):
        tupla=(CURSO[i],NOME[i])
        Cursos_Censo.append(tupla)
    #...
    CursosCenso = pd.DataFrame(Cursos_Censo)
    #Curso_Cbo_dir_curso_cbos.shape
    nomes = {0:"curso_num",
             1:"curso_nome",
            }
    CursosCenso.rename(columns=nomes,inplace=True)
    CursosCenso = CursosCenso.sort_values(by=['curso_num'])       
    CursosCenso.to_csv(path + 'Curso_Censo.csv')       
    return CursosCenso

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
    string = str(curso_num) + " - " + curso_nome + "_10.pdf"
    plt.savefig(save_results_to + string)
    # plt.show()
    #...
    A_cbo_10_sort = A_cbo_10.iloc[0:3].sort_values("Cbo",ascending=True)
    plt.rcParams["figure.figsize"] = (18, 8)
    plt.rcParams["figure.autolayout"] = True
    A_cbo_10_sort.plot(kind='barh',title=titulo3)
    plt.xlabel("")
    string = str(curso_num) + " - " + curso_nome + "_3.pdf"
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

#Cursos por CBO --- 27/04/2024
def Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo3,NaoGraduados_qtdade,curso_num,curso_nome,primeirosCbos_Nome):
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
    curso_num = str(float(curso_num))
    intensidade = 'Fraco'
    for i in range(len(index)):
        if ((i==3)and(A_Curso_11_sort['Curso'].iloc[i]==str(curso_num))): #curso_num
            tituloalterado = titulo3 + " : " + "Cbo forte"
            intensidade ='Forte'
            break
    x='Curso_Nome'
    y='Curso_Repet'
    A_Curso_11_sort.plot(x,y,kind='barh',title=tituloalterado,color=colors,legend=False)
    plt.show()
    return curso_nome,primeirosCbos_Nome,intensidade
#Função para plotar os três primeiros cursos dos três primeiros CBOs ... # 27/04/2024
def Plot_Cursos_CBOs_11(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos_Nome,primeirosCbos,NaoGraduados,curso_num,curso_nome):
    Intensidade = []
    for i in range (len(primeirosCbos)):
          titulo3=primeirosCbos_Nome[i]
          Curso,tresprimeirosCursos,intensidade=Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],curso_num,curso_nome,primeirosCbos_Nome)
          Intensidade.append(intensidade)          
    return Curso,tresprimeirosCursos,Intensidade    



# Cursos por CBO 28/04/2024
# Achar CBOs por Curso
def CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,porcent_param,save_results_to):
    X = pd.read_csv(csv_estado)
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    CBO = CBO.drop(columns=['Unnamed: 0'])
   
    #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
    X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']]
    # for i in range(len(X_CURSO_CBO)):
    #     X_CURSO_CBO.Ocupação_Código[i] = str(X_CURSO_CBO.Ocupação_Código[i])
    # # ...
    # Curso_Superior_Graduação_Código = []
    # Ocupação_Código = []
    # for i in range(len(X_CURSO_CBO)):
    #     if (X_CURSO_CBO.Ocupação_Código[i][0] == '2') or (X_CURSO_CBO.Ocupação_Código[i][0] == '1'):
    #         Curso_Superior_Graduação_Código.append(X_CURSO_CBO.Curso_Superior_Graduação_Código[i])
    #         Ocupação_Código.append(X_CURSO_CBO.Ocupação_Código[i])

    # Transforma  X_CURSO_CBO.Ocupação_Código de Float para String 
    # A partir do arquivo brasil, criar um novo dataframe somente com cursos e cbos para facilitar 
    Curso_Superior_Graduação_Código = []
    Ocupação_Código = []
    Ocupação_Código_temp = []    
    for i in range(len(X_CURSO_CBO)):        
        Ocupação_Código_temp.append(str(int(X_CURSO_CBO.Ocupação_Código[i])))   
    for i in range(len(X_CURSO_CBO)):         
        if (Ocupação_Código_temp[i][0] == '2') or (Ocupação_Código_temp[i][0] == '1'):
            Curso_Superior_Graduação_Código.append(X_CURSO_CBO.Curso_Superior_Graduação_Código[i])
            Ocupação_Código.append(X_CURSO_CBO.Ocupação_Código[i])
    # ...
    X_CURSO_CBO_Filter=[]
    for i in range(len(Curso_Superior_Graduação_Código)):
      tupla=(Curso_Superior_Graduação_Código[i],Ocupação_Código[i])
      X_CURSO_CBO_Filter.append(tupla)
    X_CURSO_CBO = pd.DataFrame(X_CURSO_CBO_Filter)
    dict = {0:"Curso_Superior_Graduação_Código",
    1:"Ocupação_Código",
    }
    X_CURSO_CBO.rename(columns=dict,inplace=True)
    #...
    #CBOs por curso
    #Indice ===========================================================================================================
    dir = X_CURSO_CBO.index[X_CURSO_CBO['Curso_Superior_Graduação_Código'] == curso_num].tolist()
    Curso_dir = []
    Cbo_dir = []
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
    dict = {0:"Curso", 1:"Cbo",}
    Curso_Cbo_dir.rename(columns=dict,inplace=True)
    #CBOs Unicos ============================================================
    Curso_Cbo_dir_unique = np.unique(Curso_Cbo_dir.Cbo)
    # print(Curso_Cbo_dir_unique)
    # Curso_Cbo_dir['Cbo'].value_counts().sort_index()
    # from numpy.ma.core import sort
    A = Curso_Cbo_dir['Cbo'].value_counts().sort_index()
    A = pd.DataFrame(A)
    A_cbo = A.sort_values("Cbo",ascending=False)
    Total = A_cbo["Cbo"].sum() #==========================================================================================================
    #====================================================================================================================================
    porcento = Total*porcent_param
    porcento_10 = round(porcento/Total * 100, 2)
    # print(porcento_10)
    ...
    Porcentagem = []
    Porcentagem = round(A_cbo['Cbo']/Total * 100, 2)
    # Adicionar a coluna Nome no dataframe A_cbo_10
    A_cbo['Porcentagem'] = Porcentagem
    qtdade = 0
    for i in A_cbo.index:
        if (A_cbo.Porcentagem[i]>= porcento_10):
            qtdade = qtdade+1
    A_cbo_10 = A_cbo.head(qtdade) #Alterado 29/09/2023   =========================
    print(A_cbo_10)
    # #========================================================================================================================
    #========================================================================================================================
    # Validação =============================================================================================================
    if(len(A_cbo_10>=1)):
        #Coletando o nome do CBOs ...
        NomeCbo = []
        for i in range(len(A_cbo_10)):
            cbo = str(int(float(A_cbo_10.index[i])))
            for i in range(len(CBO)):
                if (str(int(CBO['Cod_CBO'].iloc[i])) == cbo):
                    NomeCbo.append(CBO['Nome_CBO'].iloc[i])      
        NomeCbo = pd.DataFrame(NomeCbo, columns=['Nome_CBO'])
        #...
        A_cbo_10["Nome"] = 1
        #...
        #import warnings
        for i in range(len(A_cbo_10)):
            A_cbo_10['Nome'].iloc[i]= NomeCbo['Nome_CBO'].iloc[i]
        #A_cbo_10
        A_cbo_10.reset_index(inplace=True)
        A_cbo_10 = A_cbo_10.rename(columns = {'index':'Cod_CBO'})
        print(A_cbo_10)
    #     #sys.exit() #===============================================================================================
    #     #A_cbo_10
    #     #...
    #     A_cbo_10['Cod_CBO'] = A_cbo_10['Cod_CBO'].astype("float").astype('str')
    #     A_cbo_10['CBO_Nome'] = A_cbo_10['Cod_CBO'].str.cat(A_cbo_10['Nome'], sep =" ")
    #     #print(A_cbo_10)
    #     #print("")
    #     #sys.exit() #===============================================================================================
    #     #
    #     #tresprimeiros = []
    #     #for i in range(3):
    #     #    tresprimeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
    #     # ...
    #     #tresprimeiros = [] # Alterado em 06/09/2023
    #     #if (len(A_cbo_10)<3):
    #     #    for i in range(len(A_cbo_10)):
    #     #        tresprimeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
    #     #else:
    #     #    for i in range(3):
    #     #        tresprimeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
    #     primeiros = [] # Alterado em 29/09/2023
    #     if (len(A_cbo_10)<1):
    #         #for i in range(len(A_cbo_10)):
    #         #    tresprimeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
    #         print("Não existe CBOs para este curso")
    #         sys.exit() #===============================================================================================
    #     else:
    #         for i in range(len(A_cbo_10)):
    #             primeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
    #     #...
    #     #Deletar coluna
    #     del A_cbo_10["Cod_CBO"]
    #     del A_cbo_10["Nome"]
    #     #A_cbo_10
    #     #...
    #     #tresnomes = []
    #     #for i in range(3):
    #     #    tresnomes.append(A_cbo_10.CBO_Nome[i])
    #     # ...
    #     #tresnomes = [] # Alterado em 06/09/2023
    #     #if (len(A_cbo_10)<3):
    #     #    for i in range(len(A_cbo_10)):
    #     #        tresnomes.append(A_cbo_10.CBO_Nome[i])
    #     #else:
    #     #    for i in range(3):
    #     #        tresnomes.append(A_cbo_10.CBO_Nome[i])
    #     nomes = [] # Alterado em 26/09/2023
    #     if (len(A_cbo_10)<1):
    #         #for i in range(len(A_cbo_10)):
    #         #    nomes.append(A_cbo_10.CBO_Nome[i])
    #         print("Não existe CBOs para este curso")
    #         sys.exit() #===============================================================================================
    #     else:
    #         for i in range(len(A_cbo_10)):
    #             nomes.append(A_cbo_10.CBO_Nome[i])
    #     porcentagens = []
    #     if (len(A_cbo_10)<1):
    #         #for i in range(len(A_cbo_10)):
    #         #    nomes.append(A_cbo_10.CBO_Nome[i])
    #         print("Não existe CBOs para este curso")
    #         sys.exit() #===============================================================================================
    #     else:
    #         for i in range(len(A_cbo_10)):
    #             porcentagens.append(A_cbo_10.Porcentagem[i])
    #     #####================================================= ate aqui =======================================================================================
    #     #####================================================= ate aqui =======================================================================================
    #     #####================================================= ate aqui  =======================================================================================
    #     #...
    #     #A_cbo_10 = A_cbo_10.set_index('CBO_Nome')
    #     #print(A_cbo_10)
    #     #sys.exit() #===============================================================================================
    #     #...
    #     x='CBO_Nome'
    #     #y='Curso_Repet'
    #     y='Porcentagem'
    #     #Plotando ... Alterado em 06/09/23 ... tirei o plot dos dez maiores #07/09/2023 voltei o plot dos dez maiores ...
    #     #A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
    #     #####A_cbo_10_sort = A_cbo_10.sort_values("Cbo",ascending=True)##################################################################
    #     #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
    #     #####A_cbo_10_sort.plot(kind='barh',title=titulo10)           ##################################################################
    #     #####plt.xlabel("")                                           ##################################################################
    #     #####plt.show()                                               ##################################################################
    #     #...
    #     #A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
    #     #A_cbo_10_sort = A_cbo_10.iloc[0:3].sort_values("Cbo",ascending=True)
    #     A_cbo_10_sort = A_cbo_10.iloc[0:3].sort_values("Porcentagem",ascending=True)
    #     #A_cbo_10_sort = A_cbo_10.iloc[0:len(A_cbo_10)].sort_values("Cbo",ascending=True) #Alterado para 06/09/2023
    #     #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
    #     plt.rcParams["figure.figsize"] = (18, 8)
    #     plt.rcParams["figure.autolayout"] = True
    #     #A_cbo_10_sort.plot(kind='barh',title=titulo3)
    #     #ax = A_cbo_10_sort.plot(kind='barh',title=titulo3)
    #     ax = A_cbo_10_sort.plot(x,y,kind='barh',title=titulo3,legend=False)
    #     #ax = A_Curso_11_sort.plot(x,y,kind='barh',title=tituloalterado,color=colors,legend=False)
    #     ax.bar_label(ax.containers[0])
    #     plt.xlabel("Porcentagem")
    #     #plt.show()
    #     string = str(curso_num) + " - " + curso_nome + ".pdf"
    #     #plt.savefig(string)
    #     #save_results_to = '/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/Experimentos_25_09_a_02_09/7Porcento-Todos-IdaVolta/CBOs_Cursos_Ida/'
    #     plt.savefig(save_results_to + string)
    #     plt.show()
    #     #ida = 'Ida'
    # else:
    #      print("Não existe CBOs para este curso")
    #      #sys.exit() #===============================================================================================
    # return primeiros,nomes,porcentagens,curso_num,curso_nome
    # #return primeiros,nomes,porcentagens,curso_num,curso_nome,ida
    # #return tresprimeiros,tresnomes,curso_num,curso_nome
    # #return A_cbo_10.iloc[0:3].sort_values("Cbo",ascending=False)
    return

# Função para achar a quantidade de Não-Graduados na Pivot Table --- 28/04/2024
def NaoGraduados_PivotTable(primeirosCbos,csv_PivotTableFinal):
    PivotTableFinal = pd.read_csv(csv_PivotTableFinal)
    NaoGraduados = []
    Graduados_Nao = []
    Graduados = []
    for i in range(len(primeirosCbos)):
        Valor1 = PivotTableFinal.loc[PivotTableFinal.Ocupação_Código==primeirosCbos[i], '1.0'].values[0]
        Valor2 = PivotTableFinal.loc[PivotTableFinal.Ocupação_Código==primeirosCbos[i], '2.0'].values[0]
        Valor3 = PivotTableFinal.loc[PivotTableFinal.Ocupação_Código==primeirosCbos[i], '3.0'].values[0]
        Valor5 = PivotTableFinal.loc[PivotTableFinal.Ocupação_Código==primeirosCbos[i], '5.0'].values[0]
        ValorFinal= Valor1 + Valor2 + Valor3 + Valor5
        Valor4 = PivotTableFinal.loc[PivotTableFinal.Ocupação_Código==primeirosCbos[i], '4.0'].values[0]
        ValorTotal= Valor1 + Valor2 + Valor3 + Valor4 + Valor5
        NaoGraduados.append(ValorFinal)
        Graduados_Nao.append(ValorTotal)
        Graduados.append(Valor4)
    return primeirosCbos,NaoGraduados,Graduados_Nao,Graduados


# def Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo10,titulo3):#===comentando essa parte do grafico dos 10 maiores cursos
def Cursos_CBO_14_10(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo3,NaoGraduados_qtdade,curso_num,curso_nome,primeirosCbos_Nome,i,porcent_param):
    numero = i
    #Leitura de Arquivos CSVs ...
    X = pd.read_csv(csv_estado)
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    CURSOS = pd.read_csv(csv_CURSOS, dtype ='str')
    # drop the 'Unnamed:0' column
    CBO = CBO.drop(columns=['Unnamed: 0'])
    CURSOS = CURSOS.drop(columns=['Unnamed: 0'])
    # Acrescentando essa linha em 06/09/23 ===========================================================================
    #Profissionais das ciências e das artes
    #CBO = CBO.iloc[47:173]

    #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
    X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']]
    X_CURSO_CBO.shape

    #Cursos por CBO
    #Indice =================================================================================================
    dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['Ocupação_Código'] == cbo_num].tolist()
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
    #Cursos Únicos por CBO ====================================================================================
    Curso_Cbo_dir_curso_cbos_unique = np.unique(Curso_Cbo_dir_curso_cbos.Curso_Repet)
    #Curso_Cbo_dir_curso_cbos_unique
    #len(Curso_Cbo_dir_curso_cbos_unique)
    #Plot======================================================================================================
    Curso_Unique = Curso_Cbo_dir_curso_cbos['Curso_Repet'].astype(int).tolist()
    #Curso_Unique = np.unique(Curso_Unique)
    #Curso_Unique
    #...
    Curso_Cbo_dir_curso_cbos['Curso_Repet'].value_counts().sort_index()
    #Curso_Cbo_dir['Cbo'].value_counts().sort_index().tolist()
    #Curso_Cbo_dir_curso_cbos.sort_values("Curso",ascending=True)
    #...
    from numpy.ma.core import sort
    A_dir_curso_cbos = Curso_Cbo_dir_curso_cbos['Curso_Repet'].value_counts().sort_index()
    #print(A_dir_curso_cbos)
    #sys.exit() #=======================================================================================================
    #...
    #Curso_Cbo_dir.loc[1:3, ['Cbo']]
    A_dir_curso_cbos_sort = pd.DataFrame(A_dir_curso_cbos)
    #print(A_dir_curso_cbos_sort)
    #sys.exit() #=======================================================================================================
    #print(A_dir_curso_cbos_sort.shape)
    #A_dir_curso_cbos_sort
    #...
    A_Curso = A_dir_curso_cbos_sort.sort_values("Curso_Repet",ascending=False)
    #print(A_Curso)
    ##print(type(A_Curso))
    Total = A_Curso['Curso_Repet'].sum()
    #porcento = Total*0.1
    porcento = Total*porcent_param
    porcento_10 = round(porcento/Total * 100, 2)
    #print("")
    #print(Total)
    #print(porcento)
    #print(porcento_10)
    #sys.exit() #=======================================================================================================
    Porcentagem = []
    for i in range(len(A_Curso)):
        #Porcentagem = (A_Curso['Curso_Repet']/Total)*100
        #Porcentagem = (A_Curso['Curso_Repet']/Total)
        Porcentagem = round(A_Curso['Curso_Repet']/Total * 100, 2)
    A_Curso['Porcentagem'] = Porcentagem
    #print(A_Curso['Curso_Repet'].sum())
    #print(Porcentagem)
    #print(A_Curso)
    #sys.exit() #=======================================================================================================
    #...
    qtdade = 0
    #print(A_Curso.index)
    #print(type(A_Curso.index))
    A_Curso.index = A_Curso.index.astype(str)
    #print(type(A_Curso.index))
    #sys.exit() #===============================================================
    for i in range(len(A_Curso)):
    #print(A_Curso.Porcentagem[i])
        if (A_Curso.Porcentagem[i]>= porcento_10):
            qtdade = qtdade+1
    A_Curso_11 = A_Curso.head(qtdade)
    if(len(A_Curso_11)>=1):
      #A_Curso_11 = A_Curso.head(10)
      #print(A_Curso_11) # Apagando daqui pra baixo, da pra ver o erro ...================================================================================
      #sys.exit() #===============================================================
      #...
      #passando o CBO para string, para poder plotar o nome
      #str(int(A_Curso_11.index[0]))
      #...
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
      #import pandas as pd
      #list_name = ['item_1', 'item_2', 'item_3', ...]
      NomeCurso = pd.DataFrame(NomeCurso, columns=['Nome_Curso'])
      #print(NomeCurso.shape)
      #print(NomeCurso.columns)
      #NomeCurso
      # ...
      #NomeCurso=NomeCurso.drop(3)
      #print(type(CURSOS.Cod_Curso[0]))
      #print(type(A_Curso_11.index[0]))
      # ...
      A_Curso_11["Nome"] = 1
      import warnings
      for i in range(len(A_Curso_11)):
          A_Curso_11['Nome'][i] = NomeCurso.Nome_Curso[i]
          #if (i>=3):
          #    A_Curso_11['Nome'][i] = NomeCurso.Nome_Curso[i+1]
          #else:
          #    A_Curso_11['Nome'][i] = NomeCurso.Nome_Curso[i]
      #A_Curso_11
      #A_Curso_11.columns
      #...
      A_Curso_11.reset_index(inplace=True)
      A_Curso_11 = A_Curso_11.rename(columns = {'index':'Curso'})
      #A_Curso_11
      A_Curso_11['Curso'] = A_Curso_11['Curso'].astype("float").astype('str')
      #type(A_Curso_11.Curso )
      A_Curso_11['Curso_Nome'] = A_Curso_11['Curso'].str.cat(A_Curso_11['Nome'], sep =" ")
      #A_Curso_11['Curso'].iloc[3]= 0 # Linhas 112 a 115 comentadas para não pegar os não graduados
      #A_Curso_11['Curso_Repet'].iloc[3]= NaoGraduados_qtdade
      #A_Curso_11['Nome'].iloc[3]= "Não-Graduados"
      #A_Curso_11['Curso_Nome'].iloc[3]= "Não-Graduados"
      #print( A_Curso_11.iloc[0:5])
      #sys.exit() #=======================================================================================================
      #...
      #tresprimeiros = []
      #if (len(A_Curso_11)<3):
      #    for i in range(len(A_Curso_11)):
      #        tresprimeiros.append(int(float(A_Curso_11.Curso[i])))
      #else:
      #    #for i in range(3):
      #    #for i in range(4): #Alterado em 09/09/2023 para pegar o 4º Elemento
      #    for i in range(3): #Alterado em 20/09/2023 para não pegar os não-graduados
      #        tresprimeiros.append(int(float(A_Curso_11.Curso[i])))
      primeiros = []
      if (len(A_Curso_11)<1):
          print("Não existem cursos para este CBO")
      else:
          for i in range(len(A_Curso_11)): #Alterado em 09/09/2023 para pegar o 4º Elemento
              primeiros.append(int(float(A_Curso_11.Curso[i])))
      #sys.exit() #=======================================================================================================
      #...
      #Comentei em 09/09/2023 ============================================================================================
      #Deletar coluna
      #del A_Curso_11["Curso"]
      #del A_Curso_11["Nome"]
      #print("")
      #print(A_Curso_11)
      #A_Curso_11 = A_Curso_11.set_index('Curso_Nome')
      #A_Curso_11
      ## ...  Plotando o gráfico ... comentando essa parte do grafico dos 10 maiores cursos ======================================================
      ##A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
      #A_Curso_11_sort = A_Curso_11.sort_values("Curso_Repet",ascending=True)
      ##A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
      #A_Curso_11_sort.plot(kind='barh',title=titulo10)
      #plt.xlabel("")
      #plt.show()
      #...
      #A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
      #print("")
      #print(A_Curso_11)
      #sys.exit() #=======================================================================================================
      #Comentei em 09/09/2023 ============================================================================================
    # if (len(A_Curso_11)<3):
    #    A_Curso_11_sort = A_Curso_11.iloc[0:len(A_Curso_11)].sort_values("Curso_Repet",ascending=True)
    #    #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
    #    #A_Curso_11_sort.plot(kind='barh',title="CBO 2611: Advogados e Juristas -  Os 3 maiores Cursos")
    #    A_Curso_11_sort.plot(x="Curso_Nome", y="Curso_Repet",kind='barh',title=titulo3,color=colors)
    #    plt.xlabel("")
    #    plt.show()
    # else:
    #     A_Curso_11_sort = A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=True)
    #     #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
    #     #A_Curso_11_sort.plot(kind='barh',title="CBO 2611: Advogados e Juristas -  Os 3 maiores Cursos")
    #     colors = ['red', 'green', 'blue']
    #     #A_Curso_11_sort.plot(kind='barh',title=titulo3,color=colors)
    #     #A_Curso_11_sort.plot(x=A_Curso_11['Curso_Nome'], y=A_Curso_11['Curso_Repet'],kind='barh',title=titulo3,color=colors)
    #     A_Curso_11_sort.plot(y=A_Curso_11['Curso_Repet'],kind='barh',title=titulo3,color=colors)
    #     plt.xlabel("")
    #    plt.show()
    #     #return A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=False)
    #     #return A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=False)
      #Daqui em diante alterado 09/09/2023 =================================================================================
      #A_Curso_11_sort = A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=True)
      #A_Curso_11_sort = A_Curso_11.iloc[0:4].sort_values("Curso_Repet",ascending=True) #Alterado em 09/09/2023 para pegar os 4 primeiros
      A_Curso_11_sort = A_Curso_11.iloc[0:qtdade].sort_values("Porcentagem",ascending=True)  #26/09
      #print(A_Curso_11_sort)
      #sys.exit() # ===========================================================================================================
      #A_Curso_11_sort_df = pd.DataFrame(A_Curso_11_sort)
      #print("===================================")
      #print(A_Curso_11_sort)
      ###print("======================")
      ##print(A_Curso_11_sort_df)
      #print("===================================")
      #print("===================================")
      ##index = A_Curso_11_sort_df.index
      index =  A_Curso_11_sort.index
      #print("index",index)
      #print("===================================")
      #print("===================================")
      #print("")
      #print(A_Curso_11_sort_df.columns)
      #for i in index:
      #tituloalterado = titulo3 + "Cbo forte ou fraco?"
      #print("curso_num", curso_num)
      #print("tituloalterado", tituloalterado)
      #for i in range(len(index)): # linhas 191 ... 203 comentadas para não plotar não graduados
      #    if ((i==0)and(A_Curso_11_sort['Curso'].iloc[i]==0)):
      #        colors = ['green', 'blue', 'blue','blue'] #4ª posição
      #        break
      #    if ((i==1)and(A_Curso_11_sort['Curso'].iloc[i]==0)):
      #        colors = ['blue', 'green', 'blue','blue'] #3ª posição
      #        break
      #    if ((i==2)and(A_Curso_11_sort['Curso'].iloc[i]==0)):
      #        colors = ['blue', 'blue', 'green','blue'] #2ª posição
      #        break
      #    if ((i==3)and(A_Curso_11_sort['Curso'].iloc[i]==0)):
      #        colors = ['blue', 'blue', 'blue','green'] #1ª posição
      #        break
      #colors = ['black', 'blue', 'blue']
      colors = []
      for i in range(len(index)):
          colors.append('black')
            #if (A_Curso_11_sort['Curso'].iloc[i]==0):
            #    colors.append('red')
            #else:
            #    colors.append('black')
          #print("i",i)
          #print("index[i]",index[i])
          #print('A_Curso_11_sort.iloc[i]', A_Curso_11_sort['Curso'].iloc[i])
          #print('A_Curso_11_sort.iloc[index[i]]', A_Curso_11_sort['Curso'].iloc[index[i]])
          #print("===================================")
      tituloalterado = titulo3 + " : " + "Cbo fraco"
      curso_num = str(float(curso_num))
      #print(curso_num)
      #print(A_Curso_11_sort['Curso'].iloc[i])
      #sys.exit() #==========================================================================
      intensidade = 'Fraco'
      #print(len(index))
      #print("")
      #print(A_Curso_11_sort)
      #print(A_Curso_11_sort.index[2])
      #sys.exit() #==========================================================================
      for i in range(len(index)):
          #print("===================================")
          #print("i",i)
          #print('A_Curso_11_sort.iloc[i]', A_Curso_11_sort['Curso'].iloc[i])
          #print(type( A_Curso_11_sort['Curso'].iloc[i]))
          #if ((i==3)and(A_Curso_11_sort['Curso'].iloc[i]=='380.0')): #curso_num
          #if ((i==3)and(A_Curso_11_sort['Curso'].iloc[i]==str(curso_num))): #curso_num
          #if ((i==0)and(A_Curso_11_sort['Curso'].iloc[i]==str(curso_num))): #curso_num # alterei dia 05/10 porque tava dando erro
          if ((A_Curso_11_sort.index[i]==0)and(A_Curso_11_sort['Curso'].iloc[i]==str(curso_num))): #curso_num
              #print(curso_num)
              #print(A_Curso_11_sort['Curso'].iloc[i])
              #colors = ['blue', 'blue', 'blue','green'] #1ª posição
              tituloalterado = titulo3 + " : " + "Cbo forte"
              intensidade ='Forte'
              break
      cursos = [] # Alterado em 26/09/2023
      if (len(A_Curso_11)<1):
        #for i in range(len(A_cbo_10)):
        #    nomes.append(A_cbo_10.CBO_Nome[i])
        print("Não existe CBOs para este curso")
        sys.exit() #===============================================================================================
      else:
          for i in range(len(A_Curso_11)):
              cursos.append(A_Curso_11.Curso[i])
      nomes = [] # Alterado em 26/09/2023
      if (len(A_Curso_11)<1):
          #for i in range(len(A_cbo_10)):
          #    nomes.append(A_cbo_10.CBO_Nome[i])
          print("Não existe CBOs para este curso")
          sys.exit() #===============================================================================================
      else:
          for i in range(len(A_Curso_11)):
              nomes.append(A_Curso_11.Nome[i])
      porcentagens = []
      if (len(A_Curso_11)<1):
          #for i in range(len(A_cbo_10)):
          #    nomes.append(A_cbo_10.CBO_Nome[i])
          print("Não existe CBOs para este curso")
          sys.exit() #===============================================================================================
      else:
          for i in range(len(A_Curso_11)):
              porcentagens.append(A_Curso_11.Porcentagem[i])
      #for i in range(len(A_Curso_11_sort)):
      #    if (A_Curso_11_sort['Nome'][i]== 'Não-Graduados'):
      #        print("i:", i)
      #        print("")
      #        print(A_Curso_11_sort['Nome'][i])
      #print(A_Curso_11_sort['Nome']== 'Não-Graduados')
      #sys.exit() #=======================================================================================================
      #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
      #A_Curso_11_sort.plot(kind='barh',title="CBO 2611: Advogados e Juristas -  Os 3 maiores Cursos")
      #colors = ['blue', 'blue', 'blue','red'] #1ª posição
      #colors = ['blue', 'blue', 'red','blue'] #2ª posição
      #A_Curso_11_sort.plot(kind='barh',title=titulo3,color=colors)
      #A_Curso_11_sort.plot(x=A_Curso_11['Curso_Nome'], y=A_Curso_11['Curso_Repet'],kind='barh',title=titulo3,color=colors)
      x='Curso_Nome'
      #y='Curso_Repet'
      y='Porcentagem'
      #print(x)
      #print("")
      #print(y)
      #("")
      #sys.exit() #=======================================================================================================
      #A_Curso_11_sort.plot(x,y,kind='barh',title=tituloalterado,color=colors,legend=False)
      plt.rcParams["figure.figsize"] = (18, 8)
      plt.rcParams["figure.autolayout"] = True
      ax = A_Curso_11_sort.plot(x,y,kind='barh',title=tituloalterado,color=colors,legend=False)
      #plot= A_Curso_11_sort.plot(x,y,kind='barh',title=tituloalterado,color=colors,legend=False)
      ax.bar_label(ax.containers[0])
      plt.xlabel("Porcentagem")
      string = str(curso_num) + " - " + curso_nome + " : " + primeirosCbos_Nome[numero] +".pdf"
      #plt.savefig(string)
      save_results_to = '/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/Experimentos_25_09_a_02_09/7Porcento-Todos-IdaVolta/CURSOS_Cbos_Volta/'
      plt.savefig(save_results_to + string)
      #plt.show()
      #fig = plot.get_figure()
      #fig.savefig("output.png")
      #sys.exit() #=======================================================================================================
      #return A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=False)
      #return A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=False)
      volta = 'Volta'
    else:
       print("Não existe cursos para esse CBO")
    return cbo_num,curso_nome,primeirosCbos_Nome,intensidade,plt,string,cursos,nomes,porcentagens
    #return
    #plot = dtf.plot()
    #fig = plot.get_figure()
    #fig.savefig("output.png")     

def Cursos_CBO_13_10(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo3,NaoGraduados_qtdade,Graduados_Nao_Total,curso_num,curso_nome,primeirosCbos_Nome,i,porcent_param,save_results_to):
    numero = i
    #Leitura de Arquivos CSVs ...
    X = pd.read_csv(csv_estado)
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    CURSOS = pd.read_csv(csv_CURSOS, dtype ='str')
    # drop the 'Unnamed:0' column
    CBO = CBO.drop(columns=['Unnamed: 0'])
    CURSOS = CURSOS.drop(columns=['Unnamed: 0'])
    # Acrescentando essa linha em 06/09/23 ===========================================================================
    #Profissionais das ciências e das artes
    #CBO = CBO.iloc[47:173]

    #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
    X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']]
    X_CURSO_CBO.shape

    #Cursos por CBO
    #Indice =================================================================================================
    dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['Ocupação_Código'] == cbo_num].tolist()
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
    #Cursos Únicos por CBO ====================================================================================
    Curso_Cbo_dir_curso_cbos_unique = np.unique(Curso_Cbo_dir_curso_cbos.Curso_Repet)
    #Curso_Cbo_dir_curso_cbos_unique
    #len(Curso_Cbo_dir_curso_cbos_unique)
    #Plot======================================================================================================
    Curso_Unique = Curso_Cbo_dir_curso_cbos['Curso_Repet'].astype(int).tolist()
    #Curso_Unique = np.unique(Curso_Unique)
    #Curso_Unique
    #...
    Curso_Cbo_dir_curso_cbos['Curso_Repet'].value_counts().sort_index()
    #Curso_Cbo_dir['Cbo'].value_counts().sort_index().tolist()
    #Curso_Cbo_dir_curso_cbos.sort_values("Curso",ascending=True)
    #...
    from numpy.ma.core import sort
    A_dir_curso_cbos = Curso_Cbo_dir_curso_cbos['Curso_Repet'].value_counts().sort_index()
    #print(A_dir_curso_cbos)
    #sys.exit() #=======================================================================================================
    #...
    #Curso_Cbo_dir.loc[1:3, ['Cbo']]
    A_dir_curso_cbos_sort = pd.DataFrame(A_dir_curso_cbos)
    #print(A_dir_curso_cbos_sort)
    #sys.exit() #=======================================================================================================
    #print(A_dir_curso_cbos_sort.shape)
    #A_dir_curso_cbos_sort
    #...
    A_Curso = A_dir_curso_cbos_sort.sort_values("Curso_Repet",ascending=False)
    #print(A_Curso)
    #sys.exit() #=======================================================================================================
    ##print(type(A_Curso))
    Total = A_Curso['Curso_Repet'].sum()
    #porcento = Total*0.1
    porcento = Total*porcent_param
    porcento_10 = round(porcento/Total * 100, 2)
    #print("")
    #print(Total)
    #print(porcento)
    #print(porcento_10)
    #sys.exit() #=======================================================================================================
    Porcentagem = []
    for i in range(len(A_Curso)):
        #Porcentagem = (A_Curso['Curso_Repet']/Total)*100
        #Porcentagem = (A_Curso['Curso_Repet']/Total)
         Porcentagem = round(A_Curso['Curso_Repet']/Total * 100, 2)
    A_Curso['Porcentagem'] = Porcentagem
    #print(A_Curso['Curso_Repet'].sum())
    #print(Porcentagem)
    #print(A_Curso)
    #sys.exit() #=======================================================================================================
    #...
    #####=================================================essa parte precisa de alteração =======================================================================================
    #####=================================================essa parte precisa de alteração =======================================================================================
    #####=================================================essa parte precisa de alteração =======================================================================================
    qtdade = 0
    #print(A_Curso.index)
    #print(type(A_Curso.index))
    A_Curso.index = A_Curso.index.astype(str)
    #print(type(A_Curso.index))
    #print("")
    #print(A_Curso.Curso_Repet[1])
    #sys.exit() #=======================================================================================================
    for i in range(len(A_Curso)):
        #print(A_Curso.Porcentagem[i])
        if (A_Curso.Porcentagem[i]>= porcento_10):
            qtdade = qtdade+1
    #print(qtdade)
    #sys.exit() #=======================================================================================================
    A_Curso_11 = A_Curso.head(qtdade) #Alterado 29/09/2023   =========================
    #indice=len(A_Curso_11)
    #print('indice', indice)
    #sys.exit() #=======================================================================================================
    #print(type(A_Curso_11.index))
    #sys.exit() #=======================================================================================================
    #print('A_Curso_11.index[i]',A_Curso_11.index[0])
    #sys.exit() #=======================================================================================================

    if(len(A_Curso_11)>=1):
        #print("if...")
        #A_Curso_11 = A_Curso.head(10)
        #print(A_Curso_11) # Apagando daqui pra baixo, da pra ver o erro ...================================================================================
        #...
        #passando o CBO para string, para poder plotar o nome
        #str(int(A_Curso_11.index[0]))
        #...
        #Coletando o nome dos Cursos ...
        #A_Curso.index = A_Curso.index.astype(str)
        #print("str(float(A_Curso_11.index[i]",str(float(A_Curso_11.index[0])))
        #print('A_Curso_11.index[i]',A_Curso_11.index[0])
        #sys.exit() #=======================================================================================================
        NomeCurso = []
        for i in range(len(A_Curso_11)):
            curso=str(float(A_Curso_11.index[i]))
            #print(curso)
            for indexx, row in CURSOS.iterrows():
                if (row['Cod_Curso'] == curso):
                #if(row['Cod_Curso'] == A_Curso_10.index[i]):
                    NomeCurso.append(row['Nome_Curso'])
                    #print(row['Cod_Curso'],":",row['Nome_Curso'])
        #...
        #import pandas as pd
        #list_name = ['item_1', 'item_2', 'item_3', ...]
        NomeCurso = pd.DataFrame(NomeCurso, columns=['Nome_Curso'])
        #print(NomeCurso.shape)
        #print(NomeCurso.columns)
        #print(NomeCurso)
        #sys.exit() #=======================================================================================================
        # ...
        #NomeCurso=NomeCurso.drop(3)
        #print(type(CURSOS.Cod_Curso[0]))
        #print(type(A_Curso_11.index[0]))
        # ...
        A_Curso_11["Nome"] = 1
        import warnings
        for i in range(len(A_Curso_11)):
            A_Curso_11['Nome'][i] = NomeCurso.Nome_Curso[i]
            #if (i>=3):
            #    A_Curso_11['Nome'][i] = NomeCurso.Nome_Curso[i+1]
            #else:
            #    A_Curso_11['Nome'][i] = NomeCurso.Nome_Curso[i]
        #A_Curso_11
        #A_Curso_11.columns
        #...
        A_Curso_11.reset_index(inplace=True)
        A_Curso_11 = A_Curso_11.rename(columns = {'index':'Curso'})
        #A_Curso_11
        A_Curso_11['Curso'] = A_Curso_11['Curso'].astype("float").astype('str')
        #type(A_Curso_11.Curso )
        A_Curso_11['Curso_Nome'] = A_Curso_11['Curso'].str.cat(A_Curso_11['Nome'], sep =" ")

        #indice=len(A_Curso_11)
        #print(indice)
        #sys.exit() #=======================================================================================================

        #A_Curso_11['Curso'].iloc[3]= 0
        #A_Curso_11['Curso_Repet'].iloc[3]= NaoGraduados_qtdade
        #A_Curso_11['Nome'].iloc[3]= "Não-Graduados"
        #A_Curso_11['Curso_Nome'].iloc[3]= "Não-Graduados"
        qtdadenv=qtdade
        #print(qtdadenv)
        #print("")
        #sys.exit() #=======================================================================================================
        #print(A_Curso_11['Curso'].iloc[qtdade-1])
        #sys.exit() #=======================================================================================================
        A_Curso_11.loc[qtdade] = [0,0,0,0,0]
        #print(A_Curso_11)
        #sys.exit() #=======================================================================================================
        #print(A_Curso_11)
        A_Curso_11['Curso'].iloc[qtdade]= 0
        A_Curso_11['Curso_Repet'].iloc[qtdade]= NaoGraduados_qtdade
        A_Curso_11['Nome'].iloc[qtdade]= "Não-Graduados"
        A_Curso_11['Curso_Nome'].iloc[qtdade]= "Não-Graduados"
        #print(NaoGraduados_qtdade)
        #print(Graduados_Nao_Total)
        #sys.exit() #=======================================================================================================
        #A_Curso_11['Porcentagem'].iloc[3]= round(NaoGraduados_qtdade/Graduados_Nao_Total * 100, 2) #26/09
        A_Curso_11['Porcentagem'].iloc[qtdade]= round(NaoGraduados_qtdade/Graduados_Nao_Total * 100, 2) #26/09
        #print(A_Curso_11)
        #sys.exit() #=======================================================================================================
        #print( A_Curso_11.iloc[0:5])
        #print( A_Curso_11)
        #...
        #tresprimeiros = []
        #if (len(A_Curso_11)<3):
        #    for i in range(len(A_Curso_11)):
        #        tresprimeiros.append(int(float(A_Curso_11.Curso[i])))
        #else:
        #    #for i in range(3):
        #    for i in range(4): #Alterado em 09/09/2023 para pegar o 4º Elemento
        #        tresprimeiros.append(int(float(A_Curso_11.Curso[i])))
        primeiros = []
        if (len(A_Curso_11)<1):
            print("Não existem cursos para este CBO")
        else:
            for i in range(len(A_Curso_11)): #Alterado em 09/09/2023 para pegar o 4º Elemento
                primeiros.append(int(float(A_Curso_11.Curso[i])))
        #sys.exit() #=======================================================================================================
        #...
        #Comentei em 09/09/2023 ============================================================================================
        #Deletar coluna
        #del A_Curso_11["Curso"]
        #del A_Curso_11["Nome"]
        #print("")
        #print(A_Curso_11)
        #A_Curso_11 = A_Curso_11.set_index('Curso_Nome')
        #A_Curso_11
        ## ...  Plotando o gráfico ... comentando essa parte do grafico dos 10 maiores cursos ======================================================
        ##A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
        #A_Curso_11_sort = A_Curso_11.sort_values("Curso_Repet",ascending=True)
        ##A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
        #A_Curso_11_sort.plot(kind='barh',title=titulo10)
        #plt.xlabel("")
        #plt.show()
        #...
        #A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
        #print("")
        #print(A_Curso_11)
        #sys.exit() #=======================================================================================================
        #Comentei em 09/09/2023 ============================================================================================
      # if (len(A_Curso_11)<3):
      #    A_Curso_11_sort = A_Curso_11.iloc[0:len(A_Curso_11)].sort_values("Curso_Repet",ascending=True)
      #    #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
      #    #A_Curso_11_sort.plot(kind='barh',title="CBO 2611: Advogados e Juristas -  Os 3 maiores Cursos")
      #    A_Curso_11_sort.plot(x="Curso_Nome", y="Curso_Repet",kind='barh',title=titulo3,color=colors)
      #    plt.xlabel("")
      #    plt.show()
      # else:
      #     A_Curso_11_sort = A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=True)
      #     #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
      #     #A_Curso_11_sort.plot(kind='barh',title="CBO 2611: Advogados e Juristas -  Os 3 maiores Cursos")
      #     colors = ['red', 'green', 'blue']
      #     #A_Curso_11_sort.plot(kind='barh',title=titulo3,color=colors)
      #     #A_Curso_11_sort.plot(x=A_Curso_11['Curso_Nome'], y=A_Curso_11['Curso_Repet'],kind='barh',title=titulo3,color=colors)
      #     A_Curso_11_sort.plot(y=A_Curso_11['Curso_Repet'],kind='barh',title=titulo3,color=colors)
      #     plt.xlabel("")
      #    plt.show()
      #     #return A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=False)
      #     #return A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=False)
        #Daqui em diante alterado 09/09/2023 =================================================================================
        #A_Curso_11_sort = A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=True)
        #A_Curso_11_sort = A_Curso_11.iloc[0:4].sort_values("Curso_Repet",ascending=True) #Alterado em 09/09/2023 para pegar os 4 primeiros
        #A_Curso_11_sort = A_Curso_11.iloc[0:4].sort_values("Porcentagem",ascending=True)  #26/09
        A_Curso_11_sort = A_Curso_11.iloc[0:qtdadenv+1].sort_values("Porcentagem",ascending=True)  #26/09
        #print('A_Curso_11.iloc[0:qtdadenv+1]',A_Curso_11.iloc[0:qtdadenv+1])
        #sys.exit() #=======================================================================================================
        #A_Curso_11_sort_df = pd.DataFrame(A_Curso_11_sort)
        #print("===================================")
        #print(A_Curso_11_sort)
        ###print("======================")
        ##print(A_Curso_11_sort_df)
        #print("===================================")
        #print("===================================")
        ##index = A_Curso_11_sort_df.index
        index =  A_Curso_11_sort.index
        #print("index",index)
        #sys.exit() #=======================================================================================================
        #print("===================================")
        #print("===================================")
        #print("")
        #print(A_Curso_11_sort_df.columns)
        #for i in index:
        #tituloalterado = titulo3 + "Cbo forte ou fraco?"
        #print("curso_num", curso_num)
        #print("tituloalterado", tituloalterado)
        #for i in range(len(index)):
        #    if ((i==0)and(A_Curso_11_sort['Curso'].iloc[i]==0)):
        #        colors = ['green', 'blue', 'blue','blue'] #4ª posição
        #        break
        #    if ((i==1)and(A_Curso_11_sort['Curso'].iloc[i]==0)):
        #        colors = ['blue', 'green', 'blue','blue'] #3ª posição
        #        break
        #    if ((i==2)and(A_Curso_11_sort['Curso'].iloc[i]==0)):
        #        colors = ['blue', 'blue', 'green','blue'] #2ª posição
        #        break
        #    if ((i==3)and(A_Curso_11_sort['Curso'].iloc[i]==0)):
        #        colors = ['blue', 'blue', 'blue','green'] #1ª posição
        #        break
            #print("i",i)
            #print("index[i]",index[i])
            #print('A_Curso_11_sort.iloc[i]', A_Curso_11_sort['Curso'].iloc[i])
            #print('A_Curso_11_sort.iloc[index[i]]', A_Curso_11_sort['Curso'].iloc[index[i]])
            #print("===================================")
        colors = []
        for i in range(len(index)):
            if (A_Curso_11_sort['Curso'].iloc[i]==0):
                colors.append('red')
            else:
                colors.append('black')

        tituloalterado = titulo3 + " : " + "Cbo fraco"
        curso_num = str(float(curso_num))
        #print(curso_num)
        #print(type(curso_num))
        #sys.exit()
        intensidade = 'Fraco'
        #print(index)
        #sys.exit() #==========================================================================
        for i in range(len(index)):
            #print("===================================")
            #print("i",i)
            #print('A_Curso_11_sort.iloc[i]', A_Curso_11_sort['Curso'].iloc[i])
            #print(type( A_Curso_11_sort['Curso'].iloc[i]))
            #if ((i==3)and(A_Curso_11_sort['Curso'].iloc[i]=='380.0')): #curso_num
           # if ((i==3)and(A_Curso_11_sort['Curso'].iloc[i]==str(curso_num))): #curso_num
            #if ((i==0)and(A_Curso_11_sort['Curso'].iloc[i]==str(curso_num))): #curso_num #alterei dia 05/10 porque tava dando erro
            if ((A_Curso_11_sort.index[i]==0)and(A_Curso_11_sort['Curso'].iloc[i]==str(curso_num))): #curso_num
                #colors = ['blue', 'blue', 'blue','green'] #1ª posição
                tituloalterado = titulo3 + " : " + "Cbo forte"
                intensidade ='Forte'
                break

            cursos = [] # Alterado em 26/09/2023
            if (len(A_Curso_11)<1):
              #for i in range(len(A_cbo_10)):
              #    nomes.append(A_cbo_10.CBO_Nome[i])
              print("Não existe CBOs para este curso")
              sys.exit() #===============================================================================================
            else:
                for i in range(len(A_Curso_11)):
                    cursos.append(A_Curso_11.Curso[i])
            nomes = [] # Alterado em 26/09/2023
            if (len(A_Curso_11)<1):
                #for i in range(len(A_cbo_10)):
                #    nomes.append(A_cbo_10.CBO_Nome[i])
                print("Não existe CBOs para este curso")
                sys.exit() #===============================================================================================
            else:
                for i in range(len(A_Curso_11)):
                    nomes.append(A_Curso_11.Nome[i])

            porcentagens = []
            if (len(A_Curso_11)<1):
                #for i in range(len(A_cbo_10)):
                #    nomes.append(A_cbo_10.CBO_Nome[i])
                print("Não existe CBOs para este curso")
                sys.exit() #===============================================================================================
            else:
                for i in range(len(A_Curso_11)):
                    porcentagens.append(A_Curso_11.Porcentagem[i])

        #for i in range(len(A_Curso_11_sort)):
        #    if (A_Curso_11_sort['Nome'][i]== 'Não-Graduados'):
        #        print("i:", i)
        #        print("")
        #        print(A_Curso_11_sort['Nome'][i])
        #print(A_Curso_11_sort['Nome']== 'Não-Graduados')
        #sys.exit() #=======================================================================================================
        #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
        #A_Curso_11_sort.plot(kind='barh',title="CBO 2611: Advogados e Juristas -  Os 3 maiores Cursos")
        #colors = ['blue', 'blue', 'blue','red'] #1ª posição
        #colors = ['blue', 'blue', 'red','blue'] #2ª posição
        #A_Curso_11_sort.plot(kind='barh',title=titulo3,color=colors)
        #A_Curso_11_sort.plot(x=A_Curso_11['Curso_Nome'], y=A_Curso_11['Curso_Repet'],kind='barh',title=titulo3,color=colors)
        #####================================================= ate aqui =======================================================================================
        #####================================================= ate aqui =======================================================================================
        #####================================================= ate aqui  =======================================================================================
        x='Curso_Nome'
        #y='Curso_Repet'
        y='Porcentagem'
        #print(x)
        #print("")
        #print(y)
        #("")
        #sys.exit() #=======================================================================================================
        #A_Curso_11_sort.plot(x,y,kind='barh',title=tituloalterado,color=colors,legend=False)
        #plt.rcParams["figure.figsize"] = (18, 8)
        #plt.rcParams["figure.autolayout"] = True
        ax = A_Curso_11_sort.plot(x,y,kind='barh',title=tituloalterado,color=colors,legend=False)
        #plot = A_Curso_11_sort.plot(x,y,kind='barh',title=tituloalterado,color=colors,legend=False)
        ax.bar_label(ax.containers[0])
        plt.xlabel("Porcentagem")
        #print(primeirosCbos_Nome[numero])
        #sys.exit() #=======================================================================================================
        string = str(curso_num) + " - " + curso_nome + " : " + primeirosCbos_Nome[numero] +".pdf"
        #plt.savefig(string)
        #save_results_to = '/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/Experimentos_25_09_a_02_09/7Porcento-Todos-IdaVolta/CURSOS_Cbos_Volta/'
        plt.savefig(save_results_to + string)
        #volta = 'Volta'
        #plt.show()
        #fig = plot.get_figure()
        #fig.savefig("output.png")
        #sys.exit() #=======================================================================================================
        #return A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=False)
        #return A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=False)
        #return cbo_num,curso_nome,primeirosCbos_Nome,intensidade, ax,plt,string
    else:
       print("Não existe cursos para esse CBO")
    return cbo_num,curso_nome,primeirosCbos_Nome,intensidade,plt,string, cursos, nomes, porcentagens
    #return cbo_num,curso_nome,primeirosCbos_Nome,intensidade,plt,string, cursos, nomes, porcentagens, volta
    #return
    #plot = dtf.plot()
    #fig = plot.get_figure()
    #fig.savefig("output.png")

def relacionamentos_fortes_naofortes_cursos_profissoes(path,name,path1,name1):
    csv_estado = os.path.join(path[0],name[0]) # arquivo do censo do Brasil inteiro (somente graduados)
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)
    csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
    csv_CURSOS = os.path.join(path1[0],name1[2]) # Tabela de Cursos
    path2 = ibge_variable.paths(8)
    name2 = ibge_variable.names(8)         
    csv_PivotTableFinal =  os.path.join(path2[0],name2[0]) #Pivo Table Final

    CursosCenso = ibge_cursos_filter(path1[0],name1[2])
    curso_num  = float(CursosCenso.curso_num.iloc[1])
    curso_nome = CursosCenso.curso_nome.iloc[1]
    titulo10 =  "Curso:  " +  str(curso_num) + ": " + curso_nome + " - Os 10 maiores"
    titulo3  =  "Curso:  " +  str(curso_num) + ": " + curso_nome + " - Os 3 maiores"
    save_results_to = 'graficos/'  

    # # 27/04/2024 ==================================================================
    # CBOs por Curso ...
    # # Plota os 10 maiores CBOs Curso
    # # Plota os 3 maiores CBOs por curso
    # # Validação para chamar somente os CBOs da Familia 1 e 2
    # # Retorna os três primeiros CBOs, os três primeiros CBOs acompanhado dos respectivos nomes, o numero do Curso, e o nome do Curso 
    # primeirosCbos,primeirosCbos_Nome,CURSO_NUM,CURSO_NOME=CBOs_Curso(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,save_results_to)
    # Cursos por CBO ...
    # NaoGraduados = NaoGraduados_PivotTable(primeirosCbos, csv_PivotTableFinal)
    # # Acha CBOs por Curso ...
    # # Define forte ou Fraco via Código
    # # Plota Não-Graduados em Cor Diferente - Verde (3 primeiros cursos plotando Não-Graduados)
    # Curso,PrimeirosCbos_Nome,intensidade = Plot_Cursos_CBOs_11(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos_Nome,primeirosCbos,NaoGraduados,curso_num,curso_nome)
        
    # 28/04/2024 ==================================================================   
    # Plota os 3 maiores CBOs por curso
    # Validação para chamar somente os CBOs da Familia 1 e 2
    # Retorna os três primeiros CBOs, os três primeiros CBOs acompanhado dos respectivos nomes, o numero do Curso, e o nome do Curso
    # save_results_to
    # primeirosCbos,primeirosCbos_Nome,Porcentagens,CURSO_NUM,CURSO_NOME=CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0.1,save_results_to)
    CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0.1,save_results_to)
    # primeirosCbos,NaoGraduados,Graduados_Nao,Graduados = NaoGraduados_PivotTable(primeirosCbos, csv_PivotTableFinal)
    # #=====================================================Plotando os cursos de determinado cbo, sem função e salvando os plots ...
    # Intensidade = []
    # Porcentagens_vol = []
    # CBO_vol = []
    # Cursos_vol = []
    # Nomes_vol  = []
    # for i in range (len(primeirosCbos)):
    #     titulo3=primeirosCbos_Nome[i]
    #     if(int(float(primeirosCbos[i]))>=2000):
    #         # Acha CBOs por Curso
    #         # Define forte ou Fraco via Código
    #         # Plota Não-Graduados em Cor Diferente - Verde
    #         # save_results_to
    #         CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_14_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.1)
    #         Intensidade.append(intensidade)
    #         Porcentagens_vol.append(porcentagens_vol)
    #         CBO_vol.append(CBO)
    #         Cursos_vol.append(cursos_vol)
    #         Nomes_vol.append(nomes_vol)
    #     else:
    #         # Acha CBOs por Curso
    #         # Define forte ou Fraco via Código
    #         # Plota Não-Graduados em Cor Diferente - Verde
    #         # save_results_to
    #         CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_13_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],Graduados_Nao[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.1)
    #         Intensidade.append(intensidade)
    #         Porcentagens_vol.append(porcentagens_vol)
    #         CBO_vol.append(CBO)
    #         Cursos_vol.append(cursos_vol)
    #         Nomes_vol.append(nomes_vol)
            