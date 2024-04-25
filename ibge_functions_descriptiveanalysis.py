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

# def CBOs_Curso_v4(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3):
#     return


def relacionamentos_fortes_naofortes_cursos_profissoes():
    path = ibge_variable.paths(11)
    name = ibge_variable.names(7)
    csv_estado = os.path.join(path[0],name[0]) # arquivo do censo do Brasil inteiro (somente graduados)
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)
    csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
    csv_CURSOS = os.path.join(path1[0],name1[2]) # Tabela de Cursos

    # Passar o indice do curso ao invés de fazer manualmente ...
    curso_num=481.0
    curso_nome="Ciência da Computação"
    titulo10="Curso 481: Ciência da Computação -  Os 10 maiores"
    titulo3="Curso 481: Ciência da Computação -  Os 3 maiores"
    save_results_to = 'graficos/'

     
    # Abrir csv do Brasil inteiro
    brasil = pd.read_csv(csv_estado)
    # Abrir CSV do CBO
    CBO = pd.read_csv(csv_CBO)
    # Abrir CSV de Cursos
    cursos = pd.read_csv(csv_CURSOS)

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
    dict = {0:"Curso",1:"Cbo"}
    Curso_Cbo_dir.rename(columns=dict,inplace=True)
    # print(len(Curso_Cbo_dir))

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
        # A_cbo_10['Nome'][i] = NomeCbo.Nome_CBO[i]
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
    
    return
