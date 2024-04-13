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


#https://colab.research.google.com/drive/1Cv0fw4YmLETOy-HEqRLJvyt9HEo90gkH?authuser=1#scrollTo=hzJqOaQJOruE
def function_obterdados_especificacao_coluna(ano_ac, estados_ac, modalidades_ac):
    # instanciando a classe
    ibgeparser = Microdados()
    # obter dados
    ibgeparser.obter_dados_ibge(ano_ac, estados_ac, modalidades_ac)
    ibgeparser.obter_especificacao_coluna('palavra-chave', modalidades_ac)
    return

def Filtrar_Dados_Censo(path,name,i):

    file = path + name
    X = pd.read_csv(file,usecols=["V6036", "V6400", "V6352", "V6354", "V6356", "V6461",  "V6471", "V6462", "V6472","V6511","V6514","V0601","V0656"],sep=",")    
    dict = {
            "V6036":"Idade_em_Anos",
            "V6400":"Nível_instrução",
            "V6352":"Curso_Superior_Graduação_Código",
            "V6354":"Curso_Mestrado_Código",
            "V6356":"Curso_Doutorado_Código",
            "V6461":"Ocupação_Código",
            "V6471":"Atividade_Código",
            "V6462":"CBO-Domiciliar",
            "V6472":"CNAE-Domiciliar",
            "V6511":"Valor_rend_bruto_M",
            "V6514":"Qtdade_Salario",
            "V0601":"gênero",
            "V0656":"rendimento_aposentadoria_pensao"
            }
    X.rename(columns=dict,inplace=True)
        
    name_path = name.split(".csv")
    path_proc = ibge_variable_full.paths(1,2)
    name_path = path_proc[i] + name_path[0] + "_Fase1.csv"
    X.to_csv(name_path) 
    return X

def Limpeza_Arquivo_Censo_Graduados_NaoGraduados_1_2(path,name,i):

    file = path + name
    #print(file)
    X = pd.read_csv(file, sep=",")  
    X = X.drop(columns=['Unnamed: 0'])
    
   
    #removendo quem não tem ocupação
    X = X.dropna(subset=['Ocupação_Código'])
    
    #removendo pessoas com ocupações mal-definidas
    X.drop(X[(X['Ocupação_Código'] <1)].index, inplace=True)
    

    #print("Listando os NANs que ainda restam:==============================")
    #print(X.isnull().sum())

    #print("Tratando Valores Faltantes - Substituindo todos os nulos(NAN) por zero")
    X.fillna(0, inplace = True)

    #Removendo CBO-Domiciliar
    X = X.drop(columns=['CBO-Domiciliar'])
    
    # removendo que tem graduação, mas o curso superior é igual  a Zero
    X.drop(X[(X['Nível_instrução'] ==4) & (X['Curso_Superior_Graduação_Código'] ==0)].index, inplace=True) ## alterado 23/09/2023 #=============================
   

    name_path = name.split(".csv")
    path_proc =  ibge_variable_full.paths(2,3)
    name_path = path_proc[i] + name_path[0] + "_Graduados_NaoGraduados.csv"
    X.to_csv(name_path) 
    return   

#https://colab.research.google.com/drive/16TrgyaIq6T0fbGKl9gOWBXxbAIUfJtCD?authuser=1#scrollTo=qXidkc7VxkIT
#https://colab.research.google.com/drive/1byICdSAZxE2L8mS5NYpVjMcxKSqvlPUo?authuser=1#scrollTo=SQYQRsulgWpt
def Pivot_Table_Censo(path,name,gender,i):
    #...
    if gender == "M":
        
        file = path + name
        X= pd.read_csv(file,usecols=["Nível_instrução", "Ocupação_Código", "gênero"], sep=",")  	

        #removendo pessoas do sexo feminino ...
        X.drop(X[(X['gênero'] ==2)].index, inplace=True)
        
        X_1 = Pivot_Table(X)

        name_path = name.split(".csv")
        pathh = ibge_variable_full.paths(2,5)
        name_path = pathh[0] +  name_path[0] + "_PivotTabletMasculina.csv"
        X_1.to_csv(name_path)
    else:
        if gender == "F":
           
           file = path + name
           X= pd.read_csv(file,usecols=["Nível_instrução", "Ocupação_Código", "gênero"], sep=",")  	

           #removendo pessoas do sexo masculino ...
           X.drop(X[(X['gênero'] ==1)].index, inplace=True)

           X_1 = Pivot_Table(X)

           name_path = name.split(".csv")
           pathh = ibge_variable_full.paths(2,4)
           name_path = pathh[0] + name_path[0] +  "_PivotTabletFeminina.csv"
           X_1.to_csv(name_path)
        else:
             file = path + name
             X= pd.read_csv(file,usecols=["Nível_instrução", "Ocupação_Código", "gênero"], sep=",")  	

             X_1 = Pivot_Table(X)

             name_path = name.split(".csv")
             pathh = ibge_variable_full.paths(2,6)
             name_path =  pathh[0] + name_path[0] + "_PivotTablet.csv"
             X_1.to_csv(name_path)
    return 

def Pivot_Table(X):
    
    X[["Nível_instrução", "Ocupação_Código"]]

    #Remover todas as linhas que tem CBO = Nan ---------------------------------------------------------------------------------------------------------------------------------
    X = X.dropna(subset=['Ocupação_Código'])        

    #Gerando a Pivot table
    X['Ensino Superior']=1
    X_Pivot= pd.pivot_table(X, values=['Ensino Superior'], index=['Ocupação_Código'],columns=['Nível_instrução'],aggfunc='count',fill_value=0) 
    return X_Pivot

def Limpeza_Arquivo_Censo_Graduados_2(path,name,i):     

    file = path + name
    X = pd.read_csv(file, sep=",")  
    X = X.drop(columns=['Unnamed: 0'])
 
    # Deixando somente os graduados ...
    X.drop(X[(X['Curso_Superior_Graduação_Código'] ==0)].index, inplace=True) #Essa condição, deixa o dataset somente com as pessoas graduadas ...
    
    name_path = name.split(".csv")
    path_proc =  ibge_variable_full.paths(2,9)
    name_path = path_proc[i] + name_path[0] + "_QtdadeSal_SoGraduados.csv"
    X.to_csv(name_path) 
    return

def df2pivot(df):
    #from copy import deepcopy
    pivot = deepcopy(df)
    inst = list(pivot.iloc[0])
    cod = list(pivot.iloc[1])[0]
    pivot.columns = [cod] + inst[1:]
    pivot = pivot.iloc[2:]
    pivot.set_index(cod, inplace=True)
    return pivot

def Reduzir(pivot_final,estado,gender):
    #...
    #pivotfinal = reduce(lambda a, b: a.add(b, fill_value=0), [pivot_final[0], pivot_final[1]])
    pivotfinal = reduce(lambda a, b: a.add(b, fill_value=0), pivot_final)
   
    if gender ==1:
       pathh =  ibge_variable_full.paths(2,8)
       name_path = str(pathh[0]) + estado + '_PivotFinalMasculina.csv'
       pivotfinal.to_csv(name_path)    
    else:
         if gender ==2:
            pathh =  ibge_variable_full.paths(2,8)
            name_path = str(pathh[0]) + estado + '_PivotFinalFeminina.csv'
            pivotfinal.to_csv(name_path)   
         else:
              if gender ==3:
                 pathh =  ibge_variable_full.paths(2,8)
                 name_path = str(pathh[0]) + estado + '_PivotFinal.csv'
                 pivotfinal.to_csv(name_path)          
    return

def SomaPivotTable(path,name,i):
    #...
    file = path + name
    pivot = pd.read_csv(file)  
    pivot = df2pivot(pivot) 
    return pivot

#def Soma_PivotTableFinal():
##    #...
#    return
#
def JuntarCSVs(path,opcao,dir):
    
    file = (dir+path)
    os.chdir(file)
    
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    if opcao == "Graduados":           
       name = "Brasil"
       name_path = name.split(".csv")
       pathh = ibge_variable_full.paths(2,11)
       name_path = dir + pathh[0] + name_path[0] + "_Graduados.csv"
       combined_csv.to_csv(name_path, index=False, encoding='utf-8-sig')    
    if opcao == "Não-Graduados":
       name = "Brasil"
       name_path = name.split(".csv")
       pathh = ibge_variable_full.paths(2,11)
       name_path = dir + str(pathh[1])+ name_path[0] + "_Não-Graduados.csv"
       combined_csv.to_csv(name_path, index=False, encoding='utf-8-sig')   
    return 


