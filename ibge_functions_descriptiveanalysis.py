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

# https://colab.research.google.com/drive/1VVTquZ7fw01kCo7Tzd7YOxP5PwF-o6Vh?authuser=1#scrollTo=Ws0X7KPad6JS
# #Achar CBOs por Curso
# def CBOs_Curso(csv_estado,csv_CBO,curso_num,titulo10,titulo3):
#     #Leitura de Arquivos CSVs ...
#     X = pd.read_csv(csv_estado)
#     CBO = pd.read_csv(csv_CBO, dtype ='str')
#     #CURSOS = pd.read_csv(csv_CURSOS, dtype ='str')
#     # drop the 'Unnamed:0' column
#     CBO = CBO.drop(columns=['Unnamed: 0'])
#     #CURSOS = CURSOS.drop(columns=['Unnamed: 0'])

#     #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
#     X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']]
#     X_CURSO_CBO.shape

#     #...
#     #CBOs por curso
#     #Indice ===========================================================================================================
#     #print (X_CURSO_CBO.index[X_CURSO_CBO['Curso_Superior_Graduação_Código'] == 380].tolist())
#     dir = X_CURSO_CBO.index[X_CURSO_CBO['Curso_Superior_Graduação_Código'] == curso_num].tolist()
#     #dir
#     # ...
#     Curso_dir = []
#     Cbo_dir = []
#     for i in range(len(dir)):
#         #print(direito[i])
#         curso = X_CURSO_CBO._get_value(dir[i],'Curso_Superior_Graduação_Código')
#         cbo = X_CURSO_CBO._get_value(dir[i],'Ocupação_Código')
#         #print("Curso:",curso,"CBO:",str(int(cbo)))
#         Curso_dir.append(curso)
#         Cbo_dir.append(cbo)
#         #...
#     resultados_dir=[]
#     for i in range(len(Curso_dir)):
#       tupla=(Curso_dir[i],Cbo_dir[i])
#       resultados_dir.append(tupla)
#     #...
#     Curso_Cbo_dir = pd.DataFrame(resultados_dir)
#     #Curso_Cbo_dir.shape
#     #...
#     #Curso_Cbo_dir.columns
#     dict = {0:"Curso",
#     1:"Cbo",
#     }
#     Curso_Cbo_dir.rename(columns=dict,inplace=True)
#     #type(Curso_Cbo_dir)
#     #CBOs Unicos ============================================================
#     Curso_Cbo_dir_unique = np.unique(Curso_Cbo_dir.Cbo)
#     #Curso_Cbo_dir_unique
#     #len(Curso_Cbo_dir_unique)
#     #Plot====================================================================
#     Cbo_Unique = Curso_Cbo_dir['Cbo'].astype(int).tolist()
#     Cbo_Unique = np.unique(Cbo_Unique)
#     Cbo_Unique
#     #...
#     Curso_Cbo_dir['Cbo'].value_counts().sort_index()
#     #Curso_Cbo_dir['Cbo'].value_counts().sort_index().tolist()
#     #...
#     from numpy.ma.core import sort
#     A = Curso_Cbo_dir['Cbo'].value_counts().sort_index()
#     #...
#     #Curso_Cbo_dir.loc[1:3, ['Cbo']]
#     A = pd.DataFrame(A)
#     #print(A.shape)
#     #A
#     A_cbo = A.sort_values("Cbo",ascending=False)
#     A_cbo_10 = A_cbo.head(10)
#     #passando o CBO para string, para poder plotar o nome
#     #str(int(A_cbo_10.index[0]))
#     #...
#     #Coletando o nome do CBOs ...
#     NomeCbo = []
#     for i in range(len(A_cbo_10)):
#         cbo=str(int(A_cbo_10.index[i]))
#         for indexx, row in CBO.iterrows():
#             if (row['Cod_CBO'] == cbo):
#                 NomeCbo.append(row['Nome_CBO'])
#                 #print(row['Cod_CBO'],":",row['Nome_CBO'])
#     #import pandas as pd
#     #list_name = ['item_1', 'item_2', 'item_3', ...]
#     NomeCbo = pd.DataFrame(NomeCbo, columns=['Nome_CBO'])
#     #print(NomeCbo.shape)
#     #print(NomeCbo.columns)
#     #NomeCbo.Nome_CBO[0]
#     #...
#     A_cbo_10["Nome"] = 1
#     #...
#     import warnings
#     for i in range(len(A_cbo_10)):
#         A_cbo_10['Nome'][i] = NomeCbo.Nome_CBO[i]
#     #A_cbo_10
#     A_cbo_10.reset_index(inplace=True)
#     A_cbo_10 = A_cbo_10.rename(columns = {'index':'Cod_CBO'})
#     #A_cbo_10
#     #...
#     A_cbo_10['Cod_CBO'] = A_cbo_10['Cod_CBO'].astype("float").astype('str')
#     A_cbo_10['CBO_Nome'] = A_cbo_10['Cod_CBO'].str.cat(A_cbo_10['Nome'], sep =" ")
#     #print(A_cbo_10)
#     #
#     tresprimeiros = []
#     for i in range(3):
#         tresprimeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
#     #...
#     #Deletar coluna
#     del A_cbo_10["Cod_CBO"]
#     del A_cbo_10["Nome"]
#     #A_cbo_10
#     #...
#     tresnomes = []
#     for i in range(3):
#         tresnomes.append(A_cbo_10.CBO_Nome[i])
#     #...
#     A_cbo_10 = A_cbo_10.set_index('CBO_Nome')
#     #...
#     #Plotando ...
#     #A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
#     A_cbo_10_sort = A_cbo_10.sort_values("Cbo",ascending=True)
#     #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
#     A_cbo_10_sort.plot(kind='barh',title=titulo10)
#     plt.xlabel("")
#     plt.show()
#     #...
#     #A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
#     A_cbo_10_sort = A_cbo_10.iloc[0:3].sort_values("Cbo",ascending=True)
#     #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
#     A_cbo_10_sort.plot(kind='barh',title=titulo3)
#     plt.xlabel("")
#     plt.show()

#     return tresprimeiros,tresnomes
#     #return A_cbo_10.iloc[0:3].sort_values("Cbo",ascending=False)

# # https://colab.research.google.com/drive/1eeYR718YV5StogTdcb31mXXObz-_Wq4g?authuser=1#scrollTo=mNjedfIcbM2m
# #Achar CBOs por Curso
# def CBOs_Curso_v4(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3):
#     #Leitura de Arquivos CSVs ...
#     X = pd.read_csv(csv_estado)
#     CBO = pd.read_csv(csv_CBO, dtype ='str')
#     # CURSOS = pd.read_csv(csv_CURSOS, dtype ='str') ... 23/04/2024
#     # drop the 'Unnamed:0' column
#     CBO = CBO.drop(columns=['Unnamed: 0'])
#     # CURSOS = CURSOS.drop(columns=['Unnamed: 0']) ... 23/04/2024
#     # Acrescentando essa linha em 06/09/23 ===========================================================================
#     #Profissionais das ciências e das artes
#     #CBO = CBO.iloc[47:173]
#     #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
#     X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']]
#     # Fazer uma validação ...
#     #print(X_CURSO_CBO.shape)
#     #print(X_CURSO_CBO.head())
#     #print(X_CURSO_CBO.dtypes)
#     #print(type(X_CURSO_CBO['Ocupação_Código']))
#     #X_CURSO_CBO["Ocupação_Código"]= X_CURSO_CBO["Ocupação_Código"].astype(str)
#     #X_CURSO_CBO['Ocupação_Código'] = X_CURSO_CBO['Ocupação_Código'].astype(str)
#     #X_CURSO_CBO["Ocupação_Código"] = X_CURSO_CBO["Ocupação_Código"].apply(lambda x: str(x))
#     for i in range(len(X_CURSO_CBO)):
#         X_CURSO_CBO.Ocupação_Código[i] = str(X_CURSO_CBO.Ocupação_Código[i])
#     #X_CURSO_CBO = X_CURSO_CBO[X_CURSO_CBO['Ocupação_Código'][0]=='2' or X_CURSO_CBO['Ocupação_Código'][0]=='1']
#     # ...
#     Curso_Superior_Graduação_Código = []
#     Ocupação_Código = []
#     for i in range(len(X_CURSO_CBO)):
#         if (X_CURSO_CBO.Ocupação_Código[i][0] == '2') or (X_CURSO_CBO.Ocupação_Código[i][0] == '1'):
#             Curso_Superior_Graduação_Código.append(X_CURSO_CBO.Curso_Superior_Graduação_Código[i])
#             Ocupação_Código.append(X_CURSO_CBO.Ocupação_Código[i])
#     # ...
#     X_CURSO_CBO_Filter=[]
#     for i in range(len(Curso_Superior_Graduação_Código)):
#       tupla=(Curso_Superior_Graduação_Código[i],Ocupação_Código[i])
#       X_CURSO_CBO_Filter.append(tupla)
#     # ...
#     X_CURSO_CBO = pd.DataFrame(X_CURSO_CBO_Filter)
#     # ...
#      # ...
#     dict = {0:"Curso_Superior_Graduação_Código",
#     1:"Ocupação_Código",
#     }
#     X_CURSO_CBO.rename(columns=dict,inplace=True)
#     #print(X_CURSO_CBO.shape)
#     #print(X_CURSO_CBO.columns)
#     #sys.exit() #======================================================================================================
#     #...
#     #CBOs por curso
#     #Indice ===========================================================================================================
#     #print (X_CURSO_CBO.index[X_CURSO_CBO['Curso_Superior_Graduação_Código'] == 380].tolist())
#     dir = X_CURSO_CBO.index[X_CURSO_CBO['Curso_Superior_Graduação_Código'] == curso_num].tolist()
#     #sys.exit() #=======================================================================================================
#     #dir
#     # ...
#     Curso_dir = []
#     Cbo_dir = []
#     for i in range(len(dir)):
#         #print(direito[i])
#         curso = X_CURSO_CBO._get_value(dir[i],'Curso_Superior_Graduação_Código')
#         cbo = X_CURSO_CBO._get_value(dir[i],'Ocupação_Código')
#         #print("Curso:",curso,"CBO:",str(int(cbo)))
#         Curso_dir.append(curso)
#         Cbo_dir.append(cbo)
#         #...
#     resultados_dir=[]
#     for i in range(len(Curso_dir)):
#       tupla=(Curso_dir[i],Cbo_dir[i])
#       resultados_dir.append(tupla)
#     #...
#     Curso_Cbo_dir = pd.DataFrame(resultados_dir)
#     #Curso_Cbo_dir.shape
#     #...
#     #Curso_Cbo_dir.columns
#     dict = {0:"Curso",
#     1:"Cbo",
#     }
#     Curso_Cbo_dir.rename(columns=dict,inplace=True)
#     #sys.exit() #===============================================================================================
#     #CBOs Unicos ============================================================
#     Curso_Cbo_dir_unique = np.unique(Curso_Cbo_dir.Cbo)
#     #Curso_Cbo_dir_unique
#     #len(Curso_Cbo_dir_unique)
#     #sys.exit() #===============================================================================================
#     #Plot====================================================================
#     #Cbo_Unique = Curso_Cbo_dir['Cbo'].astype(int).tolist() # comentado em 07/09/2023
#     #Cbo_Unique = np.unique(Cbo_Unique)                     # comentado em 07/09/2023
#     #Cbo_Unique                                             # comentado em 07/09/2023
#     #...
#     Curso_Cbo_dir['Cbo'].value_counts().sort_index()
#     #Curso_Cbo_dir['Cbo'].value_counts().sort_index().tolist()
#     #...
#     from numpy.ma.core import sort
#     A = Curso_Cbo_dir['Cbo'].value_counts().sort_index()
#     #...
#     #Curso_Cbo_dir.loc[1:3, ['Cbo']]
#     A = pd.DataFrame(A)
#     #print(A.shape)
#     #A
#     A_cbo = A.sort_values("Cbo",ascending=False)
#     #A_cbo_10 = A_cbo.head(10)
#     A_cbo_10 = A_cbo.head(10) #Alterado em 06/09/23
#     #print(A_cbo_10) # Coloquei essa linha em 06/09/2023 para plotar o erro ...
#     #sys.exit() #===============================================================================================
#     #passando o CBO para string, para poder plotar o nome
#     #str(int(A_cbo_10.index[0]))
#     #...
#     #Coletando o nome do CBOs ...
#     NomeCbo = []
#     for i in range(len(A_cbo_10)):
#         cbo=str(int(float(str(A_cbo_10.index[i])))) #Comentei pra ver se corrige o erro
#         for indexx, row in CBO.iterrows():
#             #print(row['Cod_CBO'], cbo)
#             if (row['Cod_CBO'] == cbo):
#                 #print(row['Cod_CBO'],A_cbo_10.index[i])
#                 NomeCbo.append(row['Nome_CBO'])
#                 #print(row['Cod_CBO'],":",row['Nome_CBO'])
#     #import pandas as pd
#     #list_name = ['item_1', 'item_2', 'item_3', ...]
#     NomeCbo = pd.DataFrame(NomeCbo, columns=['Nome_CBO'])
#     #print(NomeCbo.shape)
#     #print(NomeCbo.columns)
#     #NomeCbo.Nome_CBO[0]
#     #print("")
#     #print(NomeCbo)
#     #sys.exit() #===============================================================================================
#     #...
#     A_cbo_10["Nome"] = 1
#     #...
#     #import warnings
#     for i in range(len(A_cbo_10)):
#         A_cbo_10['Nome'][i] = NomeCbo.Nome_CBO[i]
#     #A_cbo_10
#     A_cbo_10.reset_index(inplace=True)
#     A_cbo_10 = A_cbo_10.rename(columns = {'index':'Cod_CBO'})
#     #print(A_cbo_10)
#     #sys.exit() #===============================================================================================
#     #A_cbo_10
#     #...
#     A_cbo_10['Cod_CBO'] = A_cbo_10['Cod_CBO'].astype("float").astype('str')
#     A_cbo_10['CBO_Nome'] = A_cbo_10['Cod_CBO'].str.cat(A_cbo_10['Nome'], sep =" ")
#     #print(A_cbo_10)
#     #sys.exit() #===============================================================================================
#     #
#     #tresprimeiros = []
#     #for i in range(3):
#     #    tresprimeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
#     tresprimeiros = [] # Alterado em 06/09/2023
#     if (len(A_cbo_10)<3):
#         for i in range(len(A_cbo_10)):
#             tresprimeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
#     else:
#         for i in range(3):
#             tresprimeiros.append(int(float(A_cbo_10.Cod_CBO[i])))

#     #...
#     #Deletar coluna
#     del A_cbo_10["Cod_CBO"]
#     del A_cbo_10["Nome"]
#     #A_cbo_10
#     #...
#     #tresnomes = []
#     #for i in range(3):
#     #    tresnomes.append(A_cbo_10.CBO_Nome[i])
#     tresnomes = [] # Alterado em 06/09/2023
#     if (len(A_cbo_10)<3):
#         for i in range(len(A_cbo_10)):
#             tresnomes.append(A_cbo_10.CBO_Nome[i])
#     else:
#         for i in range(3):
#             tresnomes.append(A_cbo_10.CBO_Nome[i])
#     #...
#     A_cbo_10 = A_cbo_10.set_index('CBO_Nome')
#     #...
#     #Plotando ... Alterado em 06/09/23 ... tirei o plot dos dez maiores #07/09/2023 voltei o plot dos dez maiores ...
#     #A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
#     A_cbo_10_sort = A_cbo_10.sort_values("Cbo",ascending=True)
#     #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
#     A_cbo_10_sort.plot(kind='barh',title=titulo10)
#     plt.xlabel("")
#     plt.show()
#     #...
#     #A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
#     A_cbo_10_sort = A_cbo_10.iloc[0:3].sort_values("Cbo",ascending=True)
#     #A_cbo_10_sort = A_cbo_10.iloc[0:len(A_cbo_10)].sort_values("Cbo",ascending=True) #Alterado para 06/09/2023
#     #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
#     A_cbo_10_sort.plot(kind='barh',title=titulo3)
#     plt.xlabel("")
#     plt.show()

#     return tresprimeiros,tresnomes,curso_num,curso_nome
#     #return A_cbo_10.iloc[0:3].sort_values("Cbo",ascending=False)
#     #return

#import warnings
#import matplotlib.pyplot as plt
#import pandas as pd
# matplotlib inline
from matplotlib.pyplot import *
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
#Achar CBOs por Curso
def CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,porcent_param,save_results_to):
    #Leitura de Arquivos CSVs ...
    X = pd.read_csv(csv_estado)
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    # CURSOS = pd.read_csv(csv_CURSOS, dtype ='str') # 23/04/2024
    # drop the 'Unnamed:0' column
    CBO = CBO.drop(columns=['Unnamed: 0'])
    #  CURSOS = CURSOS.drop(columns=['Unnamed: 0']) # 23/04/2024
    # Acrescentando essa linha em 06/09/23 ===========================================================================
    #Profissionais das ciências e das artes
    #CBO = CBO.iloc[47:173]
    #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
    X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']]
    # Fazer uma validação ...
    #print(X_CURSO_CBO.shape)
    #print(X_CURSO_CBO.head())
    #print(X_CURSO_CBO.dtypes)
    #print(type(X_CURSO_CBO['Ocupação_Código']))
    #X_CURSO_CBO["Ocupação_Código"]= X_CURSO_CBO["Ocupação_Código"].astype(str)
    #X_CURSO_CBO['Ocupação_Código'] = X_CURSO_CBO['Ocupação_Código'].astype(str)
    #X_CURSO_CBO["Ocupação_Código"] = X_CURSO_CBO["Ocupação_Código"].apply(lambda x: str(x))
    for i in range(len(X_CURSO_CBO)):
        X_CURSO_CBO.Ocupação_Código[i] = str(X_CURSO_CBO.Ocupação_Código[i])
    #X_CURSO_CBO = X_CURSO_CBO[X_CURSO_CBO['Ocupação_Código'][0]=='2' or X_CURSO_CBO['Ocupação_Código'][0]=='1']
    # ...
    Curso_Superior_Graduação_Código = []
    Ocupação_Código = []
    for i in range(len(X_CURSO_CBO)):
        if (X_CURSO_CBO.Ocupação_Código[i][0] == '2') or (X_CURSO_CBO.Ocupação_Código[i][0] == '1'):
            Curso_Superior_Graduação_Código.append(X_CURSO_CBO.Curso_Superior_Graduação_Código[i])
            Ocupação_Código.append(X_CURSO_CBO.Ocupação_Código[i])
    # ...
    X_CURSO_CBO_Filter=[]
    for i in range(len(Curso_Superior_Graduação_Código)):
      tupla=(Curso_Superior_Graduação_Código[i],Ocupação_Código[i])
      X_CURSO_CBO_Filter.append(tupla)
    # ...
    X_CURSO_CBO = pd.DataFrame(X_CURSO_CBO_Filter)
    # ...
    # ...
    dict = {0:"Curso_Superior_Graduação_Código",
    1:"Ocupação_Código",
    }
    X_CURSO_CBO.rename(columns=dict,inplace=True)
    #print(X_CURSO_CBO.shape)
    #print(X_CURSO_CBO.columns)
    #sys.exit() #======================================================================================================
    #...
    #CBOs por curso
    #Indice ===========================================================================================================
    #print (X_CURSO_CBO.index[X_CURSO_CBO['Curso_Superior_Graduação_Código'] == 380].tolist())
    dir = X_CURSO_CBO.index[X_CURSO_CBO['Curso_Superior_Graduação_Código'] == curso_num].tolist()
    #sys.exit() #=======================================================================================================
    #dir
    # ...
    Curso_dir = []
    Cbo_dir = []
    for i in range(len(dir)):
        #print(direito[i])
        curso = X_CURSO_CBO._get_value(dir[i],'Curso_Superior_Graduação_Código')
        cbo = X_CURSO_CBO._get_value(dir[i],'Ocupação_Código')
        #print("Curso:",curso,"CBO:",str(int(cbo)))
        Curso_dir.append(curso)
        Cbo_dir.append(cbo)
        #...
    resultados_dir=[]
    for i in range(len(Curso_dir)):
      tupla=(Curso_dir[i],Cbo_dir[i])
      resultados_dir.append(tupla)
    #...
    Curso_Cbo_dir = pd.DataFrame(resultados_dir)
    #Curso_Cbo_dir.shape
    #...
    #Curso_Cbo_dir.columns
    dict = {0:"Curso",
    1:"Cbo",
    }
    Curso_Cbo_dir.rename(columns=dict,inplace=True)
    #sys.exit() #===============================================================================================
    #CBOs Unicos ============================================================
    Curso_Cbo_dir_unique = np.unique(Curso_Cbo_dir.Cbo)
    #Curso_Cbo_dir_unique
    #len(Curso_Cbo_dir_unique)
    #sys.exit() #===============================================================================================
    #Plot====================================================================
    #Cbo_Unique = Curso_Cbo_dir['Cbo'].astype(int).tolist() # comentado em 07/09/2023
    #Cbo_Unique = np.unique(Cbo_Unique)                     # comentado em 07/09/2023
    #Cbo_Unique                                             # comentado em 07/09/2023
    #...
    Curso_Cbo_dir['Cbo'].value_counts().sort_index()
    #Curso_Cbo_dir['Cbo'].value_counts().sort_index().tolist()
    #...
    from numpy.ma.core import sort
    A = Curso_Cbo_dir['Cbo'].value_counts().sort_index()
    #...
    #Curso_Cbo_dir.loc[1:3, ['Cbo']]
    A = pd.DataFrame(A)
    #print(A.shape)
    #A
    A_cbo = A.sort_values("Cbo",ascending=False)
    Total = A_cbo["Cbo"].sum() #==========================================================================================================
    #====================================================================================================================================
    #porcento = Total*0.1
    porcento = Total*porcent_param
    porcento_10 = round(porcento/Total * 100, 2)
    #print('Total: ',Total)
    #print('porcento: ', porcento)
    #print('porcento_10: ', porcento_10)
    #sys.exit() #===============================================================================================
    # ...
    Porcentagem = []
    for i in range(len(A_cbo)):
        #Porcentagem = (A_Curso['Curso_Repet']/Total)*100
        #Porcentagem = (A_Curso['Curso_Repet']/Total)
         Porcentagem = round(A_cbo['Cbo']/Total * 100, 2)
    A_cbo['Porcentagem'] = Porcentagem

    #####=================================================essa parte precisa de alteração =======================================================================================
    #####=================================================essa parte precisa de alteração =======================================================================================
    #####=================================================essa parte precisa de alteração =======================================================================================
    #A_cbo_10 = A_cbo.head(10)
    #A_cbo_10 = A_cbo.head(3) #Alterado em 06/09/23 ... #Alterado em 17/09/2023   =========================
    #print(A_cbo.index)
    #print(type(A_cbo.index))
    #sys.exit() #===============================================================================================
    qtdade = 0
    for i in range(len(A_cbo)):
        #print(A_cbo.Porcentagem[i])
        if (A_cbo.Porcentagem[i]>= porcento_10):
            qtdade = qtdade+1
    #print(qtdade)
    A_cbo_10 = A_cbo.head(qtdade) #Alterado 29/09/2023   =========================
    #========================================================================================================================
    #========================================================================================================================
    # Validação =============================================================================================================
    if(len(A_cbo_10>=1)):
        #sys.exit() #===============================================================================================
        #===================================================================================================== Altera aqui. Ao invés de pegar os três, pega os que são maior que 10%
        #print(A_cbo_10) # Coloquei essa linha em 06/09/2023 para plotar o erro ...
        #sys.exit() #===============================================================================================
        #passando o CBO para string, para poder plotar o nome
        #str(int(A_cbo_10.index[0]))
        #...
        #Coletando o nome do CBOs ...
        NomeCbo = []
        for i in range(len(A_cbo_10)):
            cbo=str(int(float(str(A_cbo_10.index[i])))) #Comentei pra ver se corrige o erro
            for indexx, row in CBO.iterrows():
                #print(row['Cod_CBO'], cbo)
                if (row['Cod_CBO'] == cbo):
                    #print(row['Cod_CBO'],A_cbo_10.index[i])
                    NomeCbo.append(row['Nome_CBO'])
                    #print(row['Cod_CBO'],":",row['Nome_CBO'])
        #import pandas as pd
        #list_name = ['item_1', 'item_2', 'item_3', ...]
        NomeCbo = pd.DataFrame(NomeCbo, columns=['Nome_CBO'])
        #print(NomeCbo.shape)
        #print(NomeCbo.columns)
        #NomeCbo.Nome_CBO[0]
        #print("")
        #print(NomeCbo)
        #sys.exit() #===============================================================================================
        #...
        A_cbo_10["Nome"] = 1
        #...
        #import warnings
        for i in range(len(A_cbo_10)):
            A_cbo_10['Nome'][i] = NomeCbo.Nome_CBO[i]
        #A_cbo_10
        A_cbo_10.reset_index(inplace=True)
        A_cbo_10 = A_cbo_10.rename(columns = {'index':'Cod_CBO'})
        #print(A_cbo_10)
        #sys.exit() #===============================================================================================
        #A_cbo_10
        #...
        A_cbo_10['Cod_CBO'] = A_cbo_10['Cod_CBO'].astype("float").astype('str')
        A_cbo_10['CBO_Nome'] = A_cbo_10['Cod_CBO'].str.cat(A_cbo_10['Nome'], sep =" ")
        #print(A_cbo_10)
        #print("")
        #sys.exit() #===============================================================================================
        #
        #tresprimeiros = []
        #for i in range(3):
        #    tresprimeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
        # ...
        #tresprimeiros = [] # Alterado em 06/09/2023
        #if (len(A_cbo_10)<3):
        #    for i in range(len(A_cbo_10)):
        #        tresprimeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
        #else:
        #    for i in range(3):
        #        tresprimeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
        primeiros = [] # Alterado em 29/09/2023
        if (len(A_cbo_10)<1):
            #for i in range(len(A_cbo_10)):
            #    tresprimeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
            print("Não existe CBOs para este curso")
            sys.exit() #===============================================================================================
        else:
            for i in range(len(A_cbo_10)):
                primeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
        #...
        #Deletar coluna
        del A_cbo_10["Cod_CBO"]
        del A_cbo_10["Nome"]
        #A_cbo_10
        #...
        #tresnomes = []
        #for i in range(3):
        #    tresnomes.append(A_cbo_10.CBO_Nome[i])
        # ...
        #tresnomes = [] # Alterado em 06/09/2023
        #if (len(A_cbo_10)<3):
        #    for i in range(len(A_cbo_10)):
        #        tresnomes.append(A_cbo_10.CBO_Nome[i])
        #else:
        #    for i in range(3):
        #        tresnomes.append(A_cbo_10.CBO_Nome[i])
        nomes = [] # Alterado em 26/09/2023
        if (len(A_cbo_10)<1):
            #for i in range(len(A_cbo_10)):
            #    nomes.append(A_cbo_10.CBO_Nome[i])
            print("Não existe CBOs para este curso")
            sys.exit() #===============================================================================================
        else:
            for i in range(len(A_cbo_10)):
                nomes.append(A_cbo_10.CBO_Nome[i])
        porcentagens = []
        if (len(A_cbo_10)<1):
            #for i in range(len(A_cbo_10)):
            #    nomes.append(A_cbo_10.CBO_Nome[i])
            print("Não existe CBOs para este curso")
            sys.exit() #===============================================================================================
        else:
            for i in range(len(A_cbo_10)):
                porcentagens.append(A_cbo_10.Porcentagem[i])
        #####================================================= ate aqui =======================================================================================
        #####================================================= ate aqui =======================================================================================
        #####================================================= ate aqui  =======================================================================================
        #...
        #A_cbo_10 = A_cbo_10.set_index('CBO_Nome')
        #print(A_cbo_10)
        #sys.exit() #===============================================================================================
        #...
        x='CBO_Nome'
        #y='Curso_Repet'
        y='Porcentagem'
        #Plotando ... Alterado em 06/09/23 ... tirei o plot dos dez maiores #07/09/2023 voltei o plot dos dez maiores ...
        #A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
        #####A_cbo_10_sort = A_cbo_10.sort_values("Cbo",ascending=True)##################################################################
        #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
        #####A_cbo_10_sort.plot(kind='barh',title=titulo10)           ##################################################################
        #####plt.xlabel("")                                           ##################################################################
        #####plt.show()                                               ##################################################################
        #...
        #A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
        #A_cbo_10_sort = A_cbo_10.iloc[0:3].sort_values("Cbo",ascending=True)
        A_cbo_10_sort = A_cbo_10.iloc[0:3].sort_values("Porcentagem",ascending=True)
        #A_cbo_10_sort = A_cbo_10.iloc[0:len(A_cbo_10)].sort_values("Cbo",ascending=True) #Alterado para 06/09/2023
        #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
        plt.rcParams["figure.figsize"] = (18, 8)
        plt.rcParams["figure.autolayout"] = True
        #A_cbo_10_sort.plot(kind='barh',title=titulo3)
        #ax = A_cbo_10_sort.plot(kind='barh',title=titulo3)
        ax = A_cbo_10_sort.plot(x,y,kind='barh',title=titulo3,legend=False)
        #ax = A_Curso_11_sort.plot(x,y,kind='barh',title=tituloalterado,color=colors,legend=False)
        ax.bar_label(ax.containers[0])
        plt.xlabel("Porcentagem")
        #plt.show()
        string = str(curso_num) + " - " + curso_nome + ".pdf"
        #plt.savefig(string)
        #save_results_to = '/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/Experimentos_25_09_a_02_09/7Porcento-Todos-IdaVolta/CBOs_Cursos_Ida/'
        plt.savefig(save_results_to + string)
        plt.show()
        #ida = 'Ida'
    else:
         print("Não existe CBOs para este curso")
         #sys.exit() #===============================================================================================
    return primeiros,nomes,porcentagens,curso_num,curso_nome
    #return primeiros,nomes,porcentagens,curso_num,curso_nome,ida
    #return tresprimeiros,tresnomes,curso_num,curso_nome
    #return A_cbo_10.iloc[0:3].sort_values("Cbo",ascending=False)
    #return

#Cursos por CBO
#def Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo10,titulo3):#===comentando essa parte do grafico dos 10 maiores cursos
def Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo3):
    #Leitura de Arquivos CSVs ...
    X = pd.read_csv(csv_estado)
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    CURSOS = pd.read_csv(csv_CURSOS, dtype ='str')
    # drop the 'Unnamed:0' column
    CBO = CBO.drop(columns=['Unnamed: 0'])
    CURSOS = CURSOS.drop(columns=['Unnamed: 0'])

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
    #...
    #Curso_Cbo_dir.loc[1:3, ['Cbo']]
    A_dir_curso_cbos_sort = pd.DataFrame(A_dir_curso_cbos)
    #print(A_dir_curso_cbos_sort.shape)
    #A_dir_curso_cbos_sort
    #...
    A_Curso = A_dir_curso_cbos_sort.sort_values("Curso_Repet",ascending=False)
    #...
    A_Curso_11 = A_Curso.head(11)
    #A_Curso_11
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
    #A_Curso_11
    #...
    tresprimeiros = []
    for i in range(3):
        tresprimeiros.append(int(float(A_Curso_11.Curso[i])))
    #...
    #Deletar coluna
    del A_Curso_11["Curso"]
    del A_Curso_11["Nome"]
    #A_Curso_11
    A_Curso_11 = A_Curso_11.set_index('Curso_Nome')
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
    A_Curso_11_sort = A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=True)
    #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
    #A_Curso_11_sort.plot(kind='barh',title="CBO 2611: Advogados e Juristas -  Os 3 maiores Cursos")
    A_Curso_11_sort.plot(kind='barh',title=titulo3)
    plt.xlabel("")
    plt.show()
    #return A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=False)
    return tresprimeiros

#Função para plotar os três primeiros cursos dos três primeiros CBOs ...
def Plot_Cursos_CBOs(csv_estado,csv_CBO,csv_CURSOS,primeirosCursos,primeirosCbos):
    for i in range (len(primeirosCbos)):
          titulo3= primeirosCursos[i] + " -  Os 3 maiores Cursos"
          tresprimeirosCursos=Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3)
    return



def relacionamentos_fortes_naofortes_cursos_profissoes():
    
    path = ibge_variable.paths(11)
    name = ibge_variable.names(7)
    csv_estado = os.path.join(path[0],name[0])
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)
    csv_CBO = os.path.join(path1[0],name1[1])
    csv_CURSOS = os.path.join(path1[0],name1[2])

    curso_num=481.0
    curso_nome="Ciência da Computação"
    titulo10="Curso 481: Ciência da Computação -  Os 10 maiores"
    titulo3="Curso 481: Ciência da Computação -  Os 3 maiores"
    
    # primeirosCbos,primeirosCursos=CBOs_Curso(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3)
    # primeirosCbos,primeirosCursos=CBOs_Curso_v4(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3)
    # primeirosCbos,primeirosCursos=CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3)
    save_results_to = 'microdados-ibge/original/'
    primeirosCbos,primeirosCbos_Nome,Porcentagens,CURSO_NUM,CURSO_NOME=CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0.1,save_results_to)


    # print(primeirosCursos)
    # print("")
    # print(primeirosCbos)

    # print(primeirosCbos)
    # print(primeirosCursos)
    # Plot_Cursos_CBOs(csv_estado,csv_CBO,csv_CURSOS,primeirosCursos,primeirosCbos)
    return
