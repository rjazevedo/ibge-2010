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
import logging


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
    X = pd.read_csv(file, usecols=["V6036", "V6400", "V6352", "V6354", "V6356", "V6461",  "V6471", "V6462", "V6472","V6511","V6514","V0601","V0656","V0648"], sep=",")    
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
            "V0656":"rendimento_aposentadoria_pensao",
            "V0648":"Categoria_Emprego"

            }
    X.rename(columns=dict,inplace=True)
        
    name_path = name.split(".csv")
    path_proc = ibge_variable.paths(2)
    name_path = os.path.join(path_proc[i], name_path[0]+"_Fase1.csv")
    X.to_csv(name_path) 
    return X

def Limpeza_Arquivo_Censo_Graduados_NaoGraduados_1_2(path,name,i): 

    file = os.path.join(path,name)
    print(file)
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
    # X = X.drop(columns=['CBO-Domiciliar'])
    # 02/08/2025 Porque remover CBO-Domicilar ?
    
    # removendo que tem graduação, mas o curso superior é igual a Zero
    X.drop(X[(X['Nível_instrução'] ==4) & (X['Curso_Superior_Graduação_Código'] ==0)].index, inplace=True) ## alterado 23/09/2023 #=============================
    # removendo que tem graduação, mas o CBO-Domiciliar é igual a Zero
    X.drop(X[(X['Nível_instrução'] ==4) & (X['CBO-Domiciliar'] ==0)].index, inplace=True) ## alterado 08/08/2023 #=============================

    # Alteração 12/5/2025
    #removendo pessoas sem remuneração
    X.drop(X[(X['Categoria_Emprego'] ==7)].index, inplace=True) ## alterado 12/05/2025 #=============================
    X.drop(X[(X['Categoria_Emprego'] ==0)].index, inplace=True) ## alterado 12/05/2025 #=============================


    name_path = name.split("_Fase1.csv")
    path_proc =  ibge_variable.paths(3)

    # Modifica cada coluna para tipo inteiro 19/04/2024 Werneck 
    for c in X.columns:
        X[c] = X[c].astype(int)
  
    # Crie o diretório de destino se ele não existir
    if not os.path.exists(path_proc[0]):
        os.makedirs(path_proc[0])

    name_path = os.path.join(path_proc[i], name_path[0]+"_Todos.csv")
    X.to_csv(name_path) 
    return

def Limpeza_Arquivo_Censo_Graduados_2(path,name,i):     

    file = os.path.join(path,name)
    print(file)
    X = pd.read_csv(file, sep=",")  
    X = X.drop(columns=['Unnamed: 0'])
 
    # Deixando somente os graduados ...
    X.drop(X[(X['Curso_Superior_Graduação_Código'] ==0)].index, inplace=True) #Essa condição, deixa o dataset somente com as pessoas graduadas ...
    # Deixando somente os graduados que exercem função de graduados
    # X.drop(X[(X['CBO-Domiciliar']>3000)].index, inplace=True) #Essa condição, deixa o dataset somente com as pessoas graduadas que exercem função de graduados ...

    name_path = name.split("_Todos.csv")
    path_proc =  ibge_variable.paths(9)

    # Crie o diretório de destino se ele não existir
    if not os.path.exists(path_proc[i]):
        os.makedirs(path_proc[i])

    name_path = os.path.join(path_proc[i], name_path[0] + "_Graduados.csv")
    X.to_csv(name_path) 
    return

#https://colab.research.google.com/drive/16TrgyaIq6T0fbGKl9gOWBXxbAIUfJtCD?authuser=1#scrollTo=qXidkc7VxkIT
#https://colab.research.google.com/drive/1byICdSAZxE2L8mS5NYpVjMcxKSqvlPUo?authuser=1#scrollTo=SQYQRsulgWpt
def Pivot_Table_Censo(path,name,gender,i):
    #...
    if gender == "M":
        
        file = os.path.join(path,name)      
        # X= pd.read_csv(file,usecols=["Nível_instrução", "Ocupação_Código", "gênero"], sep=",")  	
        X= pd.read_csv(file,usecols=["Nível_instrução", "CBO-Domiciliar", "gênero"], sep=",") #12/08/2025 	

        #removendo pessoas do sexo feminino ...
        X.drop(X[(X['gênero'] ==2)].index, inplace=True)
        
        X_1 = Pivot_Table(X)

        name_path = name.split("_Todos.csv")
        pathh = ibge_variable.paths(5)

        # Crie o diretório de destino se ele não existir
        if not os.path.exists(pathh[0]):
            os.makedirs(pathh[0])

        name_path = os.path.join(pathh[0],  name_path[0] + "_PivotTabletMasculina.csv")
        X_1.to_csv(name_path)
    else:
        if gender == "F":
           
            file = os.path.join(path,name)
            # X= pd.read_csv(file,usecols=["Nível_instrução", "Ocupação_Código", "gênero"], sep=",")  	
            X= pd.read_csv(file,usecols=["Nível_instrução", "CBO-Domiciliar", "gênero"], sep=",") #12/08/2025 	

            #removendo pessoas do sexo masculino ...
            X.drop(X[(X['gênero'] ==1)].index, inplace=True)

            X_1 = Pivot_Table(X)

            name_path = name.split("_Todos.csv")
            pathh = ibge_variable.paths(4)

            # Crie o diretório de destino se ele não existir
            if not os.path.exists(pathh[0]):
                os.makedirs(pathh[0])

            name_path = os.path.join(pathh[0], name_path[0] +  "_PivotTabletFeminina.csv")
            X_1.to_csv(name_path)
        else:
            file = os.path.join(path,name)
            # print(file)
            # exit(0)
            # X= pd.read_csv(file,usecols=["Nível_instrução", "Ocupação_Código", "gênero"], sep=",")  	
            X= pd.read_csv(file,usecols=["Nível_instrução", "CBO-Domiciliar", "gênero"], sep=",") #12/08/2025 	

            X_1 = Pivot_Table(X)

            name_path = name.split("_Todos.csv")
            pathh = ibge_variable.paths(6)

            # Crie o diretório de destino se ele não existir
            if not os.path.exists(pathh[0]):
                os.makedirs(pathh[0])

            name_path =  os.path.join(pathh[0],name_path[0] + "_PivotTablet.csv")
            X_1.to_csv(name_path)
    return X_1

def Pivot_Table(X):
    
    # X[["Nível_instrução", "Ocupação_Código"]]
    X[["Nível_instrução", "CBO-Domiciliar"]] #12/08/2025


    #Remover todas as linhas que tem CBO = Nan ---------------------------------------------------------------------------------------------------------------------------------
    # X = X.dropna(subset=['Ocupação_Código'])    
    X = X.dropna(subset=['CBO-Domiciliar']) #12/08/2025
    

    #Gerando a Pivot table
    X['Ensino Superior']=1
    # X_Pivot= pd.pivot_table(X, values=['Ensino Superior'], index=['Ocupação_Código'],columns=['Nível_instrução'],aggfunc='count',fill_value=0) 
    X_Pivot= pd.pivot_table(X, values=['Ensino Superior'], index=['CBO-Domiciliar'],columns=['Nível_instrução'],aggfunc='count',fill_value=0) #12/08/2025

    return X_Pivot

def df2pivot(df):
    from copy import deepcopy
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
    pathh =  ibge_variable.paths(8)

    # Crie o diretório de destino se ele não existir
    if not os.path.exists(pathh[0]):
        os.makedirs(pathh[0])

    if gender ==1:
       name_path = str(pathh[0]) + estado + '_PivotFinalMasculina.csv'
       pivotfinal.to_csv(name_path)    
    else:
         if gender ==2:
            name_path = str(pathh[0]) + estado + '_PivotFinalFeminina.csv'
            pivotfinal.to_csv(name_path)   
         else:
              if gender ==3:
                 name_path = str(pathh[0]) + estado + '_PivotFinal.csv'
                 pivotfinal.to_csv(name_path)          
    return

# # def SomaPivotTable(path,name,i):
# def SomaPivotTable(pivot):
#     # #...
#     # file = path + name
#     # pivot = pd.read_csv(file)  
#     pivot = df2pivot(pivot) 
#     return pivot


def SomaPivotTable(path,name,i):
    ##...
    file = path + name
    pivot = pd.read_csv(file)  
    pivot = df2pivot(pivot) 
    return pivot

# def Soma_PivotTableFinal():
#      return
# def filtrar_por_genero(path):
def filtrar_por_genero():
    # Ler o arquivo Brasil_Graduados.csv
    # file_path = os.path.join(path, "Brasil_Graduados.csv")
    file_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv"
    df = pd.read_csv(file_path)

    # Filtrar por gênero feminino
    df_fem = df[df['gênero'] == 2] 

    # Filtrar por gênero masculino
    df_masc = df[df['gênero'] == 1]

    # Salvar os arquivos filtrados
    pathh = ibge_variable.paths(11)
    # name_path_fem = os.path.join(pathh[0], "Brasil_Graduados_Fem.csv")
    # name_path_masc = os.path.join(pathh[0], "Brasil_Graduados_Masc.csv")
    name_path_fem = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_Fem.csv"
    name_path_masc = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_Masc.csv"
    df_fem.to_csv(name_path_fem, index=False, encoding='utf-8-sig')
    df_masc.to_csv(name_path_masc, index=False, encoding='utf-8-sig')
    return

#def JuntarCSVs(path,opcao,dir):
def JuntarCSVs(path,opcao):
    # TODO: remover o parâmetro dir
    
    all_filenames = [i for i in glob.glob(os.path.join(path,'*.csv'))]

    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    pathh = ibge_variable.paths(11)

    # Crie o diretório de destino se ele não existir
    if not os.path.exists(pathh[0]):
        os.makedirs(pathh[0])
    if not os.path.exists(pathh[1]):
        os.makedirs(pathh[1])

    if opcao == "Graduados": 
        logging.info("Gerando Arquivo Final de Graduados")  
        name_path = os.path.join(pathh[0], "Brasil_Graduados.csv")
        # criar função para gerar o arquivo final de graduados fem e masc
        # filtrar_por_genero(pathh[0])  
        # print("name_path:", name_path)          
    elif opcao == "Não-Graduados":
        logging.info("Gerando Arquivo Final de Não-Graduados") 
        name_path = os.path.join(pathh[1], "Brasil_Não-Graduados.csv")
    else:
        logging.error("Opção inválida")

    combined_csv.to_csv(name_path, index=False, encoding='utf-8-sig')   
    return 

# def ibge_trocar_CBO_Domiciliar_por_CBO():
#     # # Ler o arquivo Brasil_Graduados.csv         --------------------------------------
#     # file_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv"
#     # df = pd.read_csv(file_path)

#     # file_path1 = "/documentacao/CBO_CSV.csv"
#     # df = pd.read_csv(file_path1)

#     # Carregar o arquivo Brasil_Graduados.csv
#     file_path_graduados = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv"
#     df_graduados = pd.read_csv(file_path_graduados)
#     # print(df_graduados)
#     # exit(0)

#     # Carregar o arquivo CBO_CSV.csv
#     file_path_cbo = "documentacao/CBO_CSV.csv"
#     # df_cbo = pd.read_csv(file_path_cbo)
#     df_cbo = pd.read_csv(file_path_cbo, dtype=str)

#     # Obter o conjunto de códigos válidos de CBO
#     set_cbo = set(df_cbo['Cod_CBO'].astype(int))

#     # Encontrar os valores de CBO-Domiciliar que não estão em Cod_CBO
#     nao_encontrados = df_graduados[~df_graduados['CBO-Domiciliar'].astype(int).isin(set_cbo)]['CBO-Domiciliar'].unique()

#     print("Valores de CBO-Domiciliar que não estão em Cod_CBO:")
#     print(sorted(nao_encontrados))
#     print(len(nao_encontrados))
    
#     print("")
#     # Ler o arquivo CBO_CSV_TabelaAuxiliar.csv
#     file_path_aux = "documentacao/CBO_CSV_TabelaAuxiliar.csv"
#     df_aux = pd.read_csv(file_path_aux)

#     # Garantir que Cod_Dom é inteiro para comparação correta
#     cod_dom_set = set(df_aux['Cod_Dom'].astype(int))

#     # Encontrar valores de nao_encontrados que NÃO estão em Cod_Dom
#     nao_encontrados_na_aux = [v for v in nao_encontrados if int(v) not in cod_dom_set]

#     print("Valores de CBO-Domiciliar que não estão em Cod_CBO nem em Cod_Dom da tabela auxiliar:")
#     print(sorted(nao_encontrados_na_aux))
#     print(len(nao_encontrados_na_aux))

#     # ============================================================================================
#     # Substituir valores de CBO-Domiciliar usando a tabela auxiliar
#     # Crie um dicionário de mapeamento Cod_Dom -> Cod_CBO
#     aux_map = dict(zip(df_aux['Cod_Dom'].astype(int), df_aux['Cod_CBO'].astype(int)))

#     # Substituir apenas os valores em nao_encontrados que estão em Cod_Dom
#     df_graduados['CBO-Domiciliar'] = df_graduados['CBO-Domiciliar'].apply(
#         lambda x: aux_map[int(x)] if int(x) in aux_map else x
#     )
#     # Salvar o DataFrame atualizado em um novo arquivo
#     save_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO.csv"
#     df_graduados.to_csv(save_path, index=False)
#     # print(df_graduados)
#     # exit(0)

#     return

def ibge_trocar_CBO_Domiciliar_por_CBO():
    # # Ler o arquivo Brasil_Graduados.csv         --------------------------------------
    # file_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv"
    # df = pd.read_csv(file_path)

    # file_path1 = "/documentacao/CBO_CSV.csv"
    # df = pd.read_csv(file_path1)

    # Carregar o arquivo Brasil_Graduados.csv
    file_path_graduados = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv"
    df_graduados = pd.read_csv(file_path_graduados)
    

    # Carregar o arquivo CBO_CSV.csv
    file_path_cbo = "documentacao/CBO_CSV.csv"
    # df_cbo = pd.read_csv(file_path_cbo)
    df_cbo = pd.read_csv(file_path_cbo, dtype=str)
    # print(df_cbo)
    # exit(0)

    # Obter o conjunto de códigos válidos de CBO como string, preservando zeros à esquerda
    set_cbo = set(df_cbo['Cod_CBO'].astype(str))

    # Encontrar os valores de CBO-Domiciliar que não estão em Cod_CBO, também como string
    nao_encontrados = df_graduados[~df_graduados['CBO-Domiciliar'].astype(str).isin(set_cbo)]['CBO-Domiciliar'].astype(str).unique()

    print("Valores de CBO-Domiciliar que não estão em Cod_CBO:")
    print(sorted(nao_encontrados))
    print(len(nao_encontrados))
    
    print("")
    # Ler o arquivo CBO_CSV_TabelaAuxiliar.csv
    file_path_aux = "documentacao/CBO_CSV_TabelaAuxiliar.csv"
    # df_aux = pd.read_csv(file_path_aux)
    df_aux = pd.read_csv(file_path_aux, dtype=str)
    # print(df_aux)
    # exit(0)

    # Garantir que Cod_Dom é string para comparação correta (preservando zeros à esquerda)
    cod_dom_set = set(df_aux['Cod_Dom'].astype(str))

    # Encontrar valores de nao_encontrados que NÃO estão em Cod_Dom (como string)
    nao_encontrados_na_aux = [v for v in nao_encontrados if str(v) not in cod_dom_set]

    print("Valores de CBO-Domiciliar que não estão em Cod_CBO nem em Cod_Dom da tabela auxiliar:")
    print(sorted(nao_encontrados_na_aux))
    print(len(nao_encontrados_na_aux))
    # exit(0)
    # ============================================================================================
    # Substituir valores de CBO-Domiciliar usando a tabela auxiliar
    # Crie um dicionário de mapeamento Cod_Dom -> Cod_CBO (como string para preservar zeros à esquerda)
    aux_map = dict(zip(df_aux['Cod_Dom'].astype(str), df_aux['Cod_CBO'].astype(str)))

    # Substituir apenas os valores em nao_encontrados que estão em Cod_Dom, mantendo como string
    df_graduados['CBO-Domiciliar'] = df_graduados['CBO-Domiciliar'].astype(str).apply(
        lambda x: aux_map[x] if x in aux_map else x
    )
    # Salvar o DataFrame atualizado em um novo arquivo
    save_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO.csv"
    # Garanta que CBO-Domiciliar seja salva como texto para preservar zeros à esquerda
    df_graduados.to_csv(save_path, index=False, encoding='utf-8-sig', quoting=1)
    # print(df_graduados)
    # exit(0)

    return

# def ibge_trocar_CBO_Domiciliar_por_CBO_PivotTable():
#     # # Ler o arquivo Brasil_Graduados.csv         --------------------------------------
#     # file_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv"
#     # df = pd.read_csv(file_path)

#     # file_path1 = "/documentacao/CBO_CSV.csv"
#     # df = pd.read_csv(file_path1)

#     # Carregar o arquivo Brasil_Graduados.csv
#     # file_path_graduados = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv"
#     file_path_Brasil_PivotFinalFeminina = "processados/CSVs_PivotTableFinal/Brasil_PivotFinalFeminina.csv"
#     file_path_Brasil_PivotFinalMasculina = "processados/CSVs_PivotTableFinal/Brasil_PivotFinalMasculina.csv"
#     file_path_Brasil_PivotFinal = "processados/CSVs_PivotTableFinal/Brasil_PivotFinal.csv"
#     # df_graduados = pd.read_csv(file_path_graduados)
#     df_Brasil_PivotFinalFeminina = pd.read_csv(file_path_Brasil_PivotFinalFeminina)
#     df_Brasil_PivotFinalMasculina = pd.read_csv(file_path_Brasil_PivotFinalMasculina)
#     df_Brasil_PivotFinal = pd.read_csv(file_path_Brasil_PivotFinal)

#     # Carregar o arquivo CBO_CSV.csv
#     file_path_cbo = "documentacao/CBO_CSV.csv"
#     df_cbo = pd.read_csv(file_path_cbo)

#     # Obter o conjunto de códigos válidos de CBO
#     set_cbo = set(df_cbo['Cod_CBO'].astype(int))

#     # Encontrar os valores de CBO-Domiciliar que não estão em Cod_CBO
#     # nao_encontrados = df_graduados[~df_graduados['CBO-Domiciliar'].astype(int).isindf_Brasil_PivotFinalFeminina(set_cbo)]['CBO-Domiciliar'].unique()
#     nao_encontrados_Brasil_PivotFinal = df_Brasil_PivotFinal[~df_Brasil_PivotFinal['CBO-Domiciliar'].astype(int).isin(set_cbo)]['CBO-Domiciliar'].unique()
#     nao_encontrados_Brasil_PivotFinalMasculina = df_Brasil_PivotFinalMasculina[~df_Brasil_PivotFinalMasculina['CBO-Domiciliar'].astype(int).isin(set_cbo)]['CBO-Domiciliar'].unique()
#     nao_encontrados_Brasil_PivotFinalFeminina = df_Brasil_PivotFinalFeminina[~df_Brasil_PivotFinalFeminina['CBO-Domiciliar'].astype(int).isin(set_cbo)]['CBO-Domiciliar'].unique()

#     print("Valores de CBO-Domiciliar que não estão em Cod_CBO:")
#     # print(sorted(nao_encontrados))
#     # print(len(nao_encontrados))
#     print(sorted(nao_encontrados_Brasil_PivotFinal))
#     print(len(nao_encontrados_Brasil_PivotFinal))
#     print(sorted(nao_encontrados_Brasil_PivotFinalMasculina))
#     print(len(nao_encontrados_Brasil_PivotFinalMasculina))
#     print(sorted(nao_encontrados_Brasil_PivotFinalFeminina))
#     print(len(nao_encontrados_Brasil_PivotFinalFeminina))
    
#     print("")
#     # Ler o arquivo CBO_CSV_TabelaAuxiliar.csv
#     file_path_aux = "documentacao/CBO_CSV_TabelaAuxiliar.csv"
#     df_aux = pd.read_csv(file_path_aux)

#     # Garantir que Cod_Dom é inteiro para comparação correta
#     cod_dom_set = set(df_aux['Cod_Dom'].astype(int))

#     # Encontrar valores de nao_encontrados que NÃO estão em Cod_Dom
#     # nao_encontrados_na_aux = [v for v in nao_encontrados if int(v) not in cod_dom_set]
#     nao_encontrados_na_aux_Brasil_PivotFinal = [v for v in nao_encontrados_Brasil_PivotFinal if int(v) not in cod_dom_set]
#     nao_encontrados_na_aux_Brasil_PivotFinalMasculina = [v for v in nao_encontrados_Brasil_PivotFinal if int(v) not in cod_dom_set]
#     nao_encontrados_na_aux_Brasil_PivotFinalFeminina = [v for v in nao_encontrados_Brasil_PivotFinalFeminina if int(v) not in cod_dom_set]



#     print("Valores de CBO-Domiciliar que não estão em Cod_CBO nem em Cod_Dom da tabela auxiliar:")
#     # print(sorted(nao_encontrados_na_aux))
#     # print(len(nao_encontrados_na_aux))
#     print(sorted(nao_encontrados_na_aux_Brasil_PivotFinal))
#     print(len(nao_encontrados_na_aux_Brasil_PivotFinal))
#     print(sorted(nao_encontrados_na_aux_Brasil_PivotFinalMasculina))
#     print(len(nao_encontrados_na_aux_Brasil_PivotFinalMasculina))
#     print(sorted(nao_encontrados_na_aux_Brasil_PivotFinalFeminina))
#     print(len(nao_encontrados_na_aux_Brasil_PivotFinalFeminina))

#     # ============================================================================================
#     # Substituir valores de CBO-Domiciliar usando a tabela auxiliar
#     # Crie um dicionário de mapeamento Cod_Dom -> Cod_CBO
#     aux_map = dict(zip(df_aux['Cod_Dom'].astype(int), df_aux['Cod_CBO'].astype(int)))

#     # Substituir apenas os valores em nao_encontrados que estão em Cod_Dom
#     # df_graduados['CBO-Domiciliar'] = df_graduados['CBO-Domiciliar'].apply(
#     #     lambda x: aux_map[int(x)] if int(x) in aux_map else x
#     # )
#     df_Brasil_PivotFinal['CBO-Domiciliar'] = df_Brasil_PivotFinal['CBO-Domiciliar'].apply(
#         lambda x: aux_map[int(x)] if int(x) in aux_map else x
#     )
#     df_Brasil_PivotFinalMasculina['CBO-Domiciliar'] = df_Brasil_PivotFinalMasculina['CBO-Domiciliar'].apply(
#         lambda x: aux_map[int(x)] if int(x) in aux_map else x
#     )
#     df_Brasil_PivotFinalFeminina['CBO-Domiciliar'] = df_Brasil_PivotFinalFeminina['CBO-Domiciliar'].apply(
#         lambda x: aux_map[int(x)] if int(x) in aux_map else x
#     )
#     # Salvar o DataFrame atualizado em um novo arquivo
#     # save_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO.csv"
#     # df_graduados.to_csv(save_path, index=False)
#     save_path_Brasil_PivotFinal_CBO = "processados/CSVs_PivotTableFinal/Brasil_PivotFinal_CBO.csv"
#     save_path_Brasil_PivotFinalMasculina_CBO = "processados/CSVs_PivotTableFinal/Brasil_PivotFinalMasculina_CBO.csv"
#     save_path_Brasil_PivotFinalFeminina_CBO = "processados/CSVs_PivotTableFinal/Brasil_PivotFinalFeminina_CBO.csv"
#     df_Brasil_PivotFinal.to_csv(save_path_Brasil_PivotFinal_CBO, index=False)
#     df_Brasil_PivotFinalMasculina.to_csv(save_path_Brasil_PivotFinalMasculina_CBO, index=False)
#     df_Brasil_PivotFinalFeminina.to_csv(save_path_Brasil_PivotFinalFeminina_CBO, index=False)

#     return

def ibge_trocar_CBO_Domiciliar_por_CBO_PivotTable():
    # # Ler o arquivo Brasil_Graduados.csv         --------------------------------------
    # file_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv"
    # df = pd.read_csv(file_path)

    # file_path1 = "/documentacao/CBO_CSV.csv"
    # df = pd.read_csv(file_path1)

    # Carregar o arquivo Brasil_Graduados.csv
    # file_path_graduados = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv"
    file_path_Brasil_PivotFinalFeminina = "processados/CSVs_PivotTableFinal/Brasil_PivotFinalFeminina.csv"
    file_path_Brasil_PivotFinalMasculina = "processados/CSVs_PivotTableFinal/Brasil_PivotFinalMasculina.csv"
    file_path_Brasil_PivotFinal = "processados/CSVs_PivotTableFinal/Brasil_PivotFinal.csv"
    # df_graduados = pd.read_csv(file_path_graduados)
    df_Brasil_PivotFinalFeminina = pd.read_csv(file_path_Brasil_PivotFinalFeminina)
    df_Brasil_PivotFinalMasculina = pd.read_csv(file_path_Brasil_PivotFinalMasculina)
    df_Brasil_PivotFinal = pd.read_csv(file_path_Brasil_PivotFinal)

    # Carregar o arquivo CBO_CSV.csv
    file_path_cbo = "documentacao/CBO_CSV.csv"
    df_cbo = pd.read_csv(file_path_cbo, dtype=str)
    # print(df_cbo)
    # exit(0)

    # Obter o conjunto de códigos válidos de CBO como string (preservando zeros à esquerda)
    set_cbo = set(df_cbo['Cod_CBO'].astype(str))

    # Encontrar os valores de CBO-Domiciliar que não estão em Cod_CBO, também como string
    nao_encontrados_Brasil_PivotFinal = df_Brasil_PivotFinal[~df_Brasil_PivotFinal['CBO-Domiciliar'].astype(str).isin(set_cbo)]['CBO-Domiciliar'].astype(str).unique()
    nao_encontrados_Brasil_PivotFinalMasculina = df_Brasil_PivotFinalMasculina[~df_Brasil_PivotFinalMasculina['CBO-Domiciliar'].astype(str).isin(set_cbo)]['CBO-Domiciliar'].astype(str).unique()
    nao_encontrados_Brasil_PivotFinalFeminina = df_Brasil_PivotFinalFeminina[~df_Brasil_PivotFinalFeminina['CBO-Domiciliar'].astype(str).isin(set_cbo)]['CBO-Domiciliar'].astype(str).unique()

    print("Valores de CBO-Domiciliar que não estão em Cod_CBO:")
    # print(sorted(nao_encontrados))
    # print(len(nao_encontrados))
    print(sorted(nao_encontrados_Brasil_PivotFinal))
    print(len(nao_encontrados_Brasil_PivotFinal))
    print(sorted(nao_encontrados_Brasil_PivotFinalMasculina))
    print(len(nao_encontrados_Brasil_PivotFinalMasculina))
    print(sorted(nao_encontrados_Brasil_PivotFinalFeminina))
    print(len(nao_encontrados_Brasil_PivotFinalFeminina))
    
    print("")
    # Ler o arquivo CBO_CSV_TabelaAuxiliar.csv
    file_path_aux = "documentacao/CBO_CSV_TabelaAuxiliar.csv"
    df_aux = pd.read_csv(file_path_aux, dtype=str)
    # print(df_aux)
    # exit(0)

    # Garantir que Cod_Dom é string para comparação correta (preservando zeros à esquerda)
    cod_dom_set = set(df_aux['Cod_Dom'].astype(str))

    # Encontrar valores de nao_encontrados que NÃO estão em Cod_Dom (como string)
    nao_encontrados_na_aux_Brasil_PivotFinal = [v for v in nao_encontrados_Brasil_PivotFinal if str(v) not in cod_dom_set]
    nao_encontrados_na_aux_Brasil_PivotFinalMasculina = [v for v in nao_encontrados_Brasil_PivotFinalMasculina if str(v) not in cod_dom_set]
    nao_encontrados_na_aux_Brasil_PivotFinalFeminina = [v for v in nao_encontrados_Brasil_PivotFinalFeminina if str(v) not in cod_dom_set]


    print("Valores de CBO-Domiciliar que não estão em Cod_CBO nem em Cod_Dom da tabela auxiliar:")
    # print(sorted(nao_encontrados_na_aux))
    # print(len(nao_encontrados_na_aux))
    print(sorted(nao_encontrados_na_aux_Brasil_PivotFinal))
    print(len(nao_encontrados_na_aux_Brasil_PivotFinal))
    print(sorted(nao_encontrados_na_aux_Brasil_PivotFinalMasculina))
    print(len(nao_encontrados_na_aux_Brasil_PivotFinalMasculina))
    print(sorted(nao_encontrados_na_aux_Brasil_PivotFinalFeminina))
    print(len(nao_encontrados_na_aux_Brasil_PivotFinalFeminina))

    # ============================================================================================
    # Substituir valores de CBO-Domiciliar usando a tabela auxiliar
    # Crie um dicionário de mapeamento Cod_Dom -> Cod_CBO (como string para preservar zeros à esquerda)
    aux_map = dict(zip(df_aux['Cod_Dom'].astype(str), df_aux['Cod_CBO'].astype(str)))

    # Substituir apenas os valores em nao_encontrados que estão em Cod_Dom, mantendo como string
    df_Brasil_PivotFinal['CBO-Domiciliar'] = df_Brasil_PivotFinal['CBO-Domiciliar'].astype(str).apply(
        lambda x: aux_map[x] if x in aux_map else x
    )
    df_Brasil_PivotFinalMasculina['CBO-Domiciliar'] = df_Brasil_PivotFinalMasculina['CBO-Domiciliar'].astype(str).apply(
        lambda x: aux_map[x] if x in aux_map else x
    )
    df_Brasil_PivotFinalFeminina['CBO-Domiciliar'] = df_Brasil_PivotFinalFeminina['CBO-Domiciliar'].astype(str).apply(
        lambda x: aux_map[x] if x in aux_map else x
    )
    # Salvar os DataFrames atualizados em novos arquivos, garantindo que CBO-Domiciliar seja salva como texto
    save_path_Brasil_PivotFinal_CBO = "processados/CSVs_PivotTableFinal/Brasil_PivotFinal_CBO.csv"
    save_path_Brasil_PivotFinalMasculina_CBO = "processados/CSVs_PivotTableFinal/Brasil_PivotFinalMasculina_CBO.csv"
    save_path_Brasil_PivotFinalFeminina_CBO = "processados/CSVs_PivotTableFinal/Brasil_PivotFinalFeminina_CBO.csv"
    df_Brasil_PivotFinal.to_csv(save_path_Brasil_PivotFinal_CBO, index=False, encoding='utf-8-sig', quoting=1)
    df_Brasil_PivotFinalMasculina.to_csv(save_path_Brasil_PivotFinalMasculina_CBO, index=False, encoding='utf-8-sig', quoting=1)
    df_Brasil_PivotFinalFeminina.to_csv(save_path_Brasil_PivotFinalFeminina_CBO, index=False, encoding='utf-8-sig', quoting=1)

    return

def diminuirCurso():
    # # Ler o arquivo Brasil_Graduados.csv         --------------------------------------
    # # file_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv"
    # file_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO.csv"
    # df = pd.read_csv(file_path)

    # # Reduzir um dígito da coluna Curso_Superior_Graduação_Código se tiver 3 dígitos
    # df['Curso_Superior_Graduação_Código'] = df['Curso_Superior_Graduação_Código'].apply(
    #     lambda x: int(str(x)[:-1]) if len(str(x)) == 3 else int(str(x))
    # )

    # # Salvar em novo arquivo
    # # save_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO4_Curso2.csv"
    # save_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO_CBO4_Curso2.csv"
    # df.to_csv(save_path, index=False)

    # # Ler o arquivo Brasil_Graduados_DiminuidoCBO2.csv ------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # # file_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_DiminuidoCBO2.csv"
    # file_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO_DiminuidoCBO2.csv"

    # df = pd.read_csv(file_path)

    # # Reduzir um dígito da coluna Curso_Superior_Graduação_Código se tiver 3 dígitos
    # df['Curso_Superior_Graduação_Código'] = df['Curso_Superior_Graduação_Código'].apply(
    #     lambda x: int(str(x)[:-1]) if len(str(x)) == 3 else int(str(x))
    # )

    # # Salvar em novo arquivo
    # # save_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_DiminuidoCBO2_Curso2.csv"
    # save_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO_DiminuidoCBO2_Curso2.csv"
    # df.to_csv(save_path, index=False)
    # file_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_DiminuidoCBO3.csv"
    file_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO_DiminuidoCBO2.csv"
    df = pd.read_csv(file_path, dtype={'CBO-Domiciliar': str})

    # Imprimir registros onde CBO-Domiciliar tem zeros à esquerda
    # print(df[df['CBO-Domiciliar'].str.startswith('0')])
    # print("-----------------------------------")
    # Reduzir um dígito da coluna Curso_Superior_Graduação_Código se tiver 3 dígitos
    df['Curso_Superior_Graduação_Código'] = df['Curso_Superior_Graduação_Código'].apply(
        lambda x: int(str(x)[:-1]) if len(str(x)) == 3 else int(str(x))
    )

    # Salvar em novo arquivo, mantendo zeros à esquerda na coluna CBO-Domiciliar
    save_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO_DiminuidoCBO2_Curso2.csv"
    # Imprimir registros onde CBO-Domiciliar tem zeros à esquerda
    # print(df[df['CBO-Domiciliar'].str.startswith('0')])
    # df.to_csv(save_path, index=False, encoding='utf-8-sig', quoting=1)

    # Ler o arquivo Brasil_Graduados_DiminuidoCBO3.csv---------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # file_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_DiminuidoCBO3.csv"
    file_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO_DiminuidoCBO3.csv"
    df = pd.read_csv(file_path, dtype={'CBO-Domiciliar': str})

    # Imprimir registros onde CBO-Domiciliar tem zeros à esquerda
    # print(df[df['CBO-Domiciliar'].str.startswith('0')])
    # print("-----------------------------------")
    # Reduzir um dígito da coluna Curso_Superior_Graduação_Código se tiver 3 dígitos
    df['Curso_Superior_Graduação_Código'] = df['Curso_Superior_Graduação_Código'].apply(
        lambda x: int(str(x)[:-1]) if len(str(x)) == 3 else int(str(x))
    )

    # Salvar em novo arquivo, mantendo zeros à esquerda na coluna CBO-Domiciliar
    save_path = "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO_DiminuidoCBO3_Curso2.csv"
    # Imprimir registros onde CBO-Domiciliar tem zeros à esquerda
    # print(df[df['CBO-Domiciliar'].str.startswith('0')])
    # df.to_csv(save_path, index=False, encoding='utf-8-sig', quoting=1)
    return

# def ibge_diminuirCBOs(opcao):
#     if opcao ==2:
#        # Process the first file
#        # file_path_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv'
#        file_path_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO.csv'

#        df_graduados = pd.read_csv(file_path_graduados)
#        # Subtract one digit from the specified columns
#        # df_graduados['Curso_Superior_Graduação_Código'] = df_graduados['Curso_Superior_Graduação_Código'].astype(str).str[:-1].astype(int)
#        # df_graduados['CBO-Domiciliar'] = df_graduados['CBO-Domiciliar'].astype(str).str[:-2].astype(int)
#        df_graduados['CBO-Domiciliar'] = df_graduados['CBO-Domiciliar'].apply(
#         lambda x: int(str(x)[:-2]) if len(str(x)) == 4 else (
#             int(str(x)[:-1]) if len(str(x)) == 3 else int(str(x))
#         )
#        )
#        # Save the transformed DataFrame to a new file
#        # save_results_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_DiminuidoCBO2.csv'
#        save_results_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO_DiminuidoCBO2.csv'
#        df_graduados.to_csv(save_results_graduados, index=False)

#        # Process the second file
#        # file_path_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal.csv'
#        file_path_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_CBO.csv'
#        df_pivot = pd.read_csv(file_path_pivot)
#        # Subtract one digit from the Ocupação_Código column
#        # df_pivot['CBO-Domiciliar'] = df_pivot['CBO-Domiciliar'].astype(str).str[:-2].astype(int)
#        df_pivot['CBO-Domiciliar'] = df_pivot['CBO-Domiciliar'].apply(
#         lambda x: int(str(x)[:-2]) if len(str(x)) == 4 else (
#             int(str(x)[:-1]) if len(str(x)) == 3 else int(str(x))
#         )
#        )
#        # Save the transformed DataFrame to a new file
#        # save_results_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_DiminuidaCBO2.csv'
#        save_results_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_CBO_DiminuidaCBO2.csv'
#        df_pivot.to_csv(save_results_pivot, index=False) # opcao=2

#     elif opcao ==3:
#        # Process the first file
#        # file_path_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv'
#        file_path_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO.csv'
#        df_graduados = pd.read_csv(file_path_graduados)
#        # Subtract one digit from the specified columns
#        # df_graduados['Curso_Superior_Graduação_Código'] = df_graduados['Curso_Superior_Graduação_Código'].astype(str).str[:-1].astype(int)
#        # df_graduados['CBO-Domiciliar'] = df_graduados['CBO-Domiciliar'].astype(str).str[:-2].astype(int)
#        df_graduados['CBO-Domiciliar'] = df_graduados['CBO-Domiciliar'].apply(
#         lambda x: int(str(x)[:-1]) if len(str(x)) == 4 else int(str(x))
#         )
#        # Save the transformed DataFrame to a new file
#        # save_results_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_DiminuidoCBO3.csv'
#        save_results_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO_DiminuidoCBO3.csv'
#        df_graduados.to_csv(save_results_graduados, index=False)

#        # Process the second file
#     #    file_path_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal.csv'      
#        file_path_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_CBO.csv'

#        df_pivot = pd.read_csv(file_path_pivot)
#        # Subtract one digit from the Ocupação_Código column
#        # df_pivot['CBO-Domiciliar'] = df_pivot['CBO-Domiciliar'].astype(str).str[:-2].astype(int)
#        df_pivot['CBO-Domiciliar'] = df_pivot['CBO-Domiciliar'].apply(
#         lambda x: int(str(x)[:-1]) if len(str(x)) == 4 else int(str(x))
#        )
#        # Save the transformed DataFrame to a new file
#        # save_results_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_DiminuidaCBO3.csv'
#        save_results_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_CBO_DiminuidaCBO3.csv'
#        df_pivot.to_csv(save_results_pivot, index=False)
#     return

def ibge_diminuirCBOs(opcao):
    if opcao ==2:
       # Process the first file
       # file_path_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv'
       file_path_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO.csv'
       # df_graduados = pd.read_csv(file_path_graduados)
       df_graduados = pd.read_csv(file_path_graduados, dtype=str)


    #    # Subtract one digit from the specified columns
    #    # df_graduados['Curso_Superior_Graduação_Código'] = df_graduados['Curso_Superior_Graduação_Código'].astype(str).str[:-1].astype(int)
    #    # df_graduados['CBO-Domiciliar'] = df_graduados['CBO-Domiciliar'].astype(str).str[:-2].astype(int)
    #    df_graduados['CBO-Domiciliar'] = df_graduados['CBO-Domiciliar'].apply(
    #     lambda x: int(str(x)[:-2]) if len(str(x)) == 4 else (
    #         int(str(x)[:-1]) if len(str(x)) == 3 else int(str(x))
    #     )
    #    )
    #    # Save the transformed DataFrame to a new file
    #    # save_results_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_DiminuidoCBO2.csv'
    #    save_results_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO_DiminuidoCBO2.csv'
    #    df_graduados.to_csv(save_results_graduados, index=False)
        
       # Subtrair dígitos da coluna CBO-Domiciliar baseada em string (preservando zeros à esquerda)
       df_graduados['CBO-Domiciliar'] = df_graduados['CBO-Domiciliar'].apply(
       lambda x: x[:-2] if len(x) == 4 else (x[:-1] if len(x) == 3 else x)
       )
       # Salvar o DataFrame transformado em um novo arquivo
       save_results_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO_DiminuidoCBO2.csv'
       # Imprimir os primeiros registros mostrando os zeros à esquerda
       # print(df_graduados.head().to_string(index=False))
       df_graduados.to_csv(save_results_graduados,  index=False, encoding='utf-8-sig', quoting=1)



    #    # Process the second file
    #    # file_path_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal.csv'
    #    file_path_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_CBO.csv'
    #    df_pivot = pd.read_csv(file_path_pivot)
    #    # Subtract one digit from the Ocupação_Código column
    #    # df_pivot['CBO-Domiciliar'] = df_pivot['CBO-Domiciliar'].astype(str).str[:-2].astype(int)
    #    df_pivot['CBO-Domiciliar'] = df_pivot['CBO-Domiciliar'].apply(
    #     lambda x: int(str(x)[:-2]) if len(str(x)) == 4 else (
    #         int(str(x)[:-1]) if len(str(x)) == 3 else int(str(x))
    #     )
    #    )
    #    # Save the transformed DataFrame to a new file
    #    # save_results_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_DiminuidaCBO2.csv'
    #    save_results_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_CBO_DiminuidaCBO2.csv'
    #    df_pivot.to_csv(save_results_pivot, index=False) 

       # Process the second file
       # file_path_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal.csv'
       file_path_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_CBO.csv'
       df_pivot = pd.read_csv(file_path_pivot, dtype=str)
       # Subtrair dígitos da coluna CBO-Domiciliar baseada em string (preservando zeros à esquerda)
       df_pivot['CBO-Domiciliar'] = df_pivot['CBO-Domiciliar'].apply(
        lambda x: x[:-2] if len(x) == 4 else (x[:-1] if len(x) == 3 else x)
        )
       # Salvar o DataFrame transformado em um novo arquivo
       save_results_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_CBO_DiminuidaCBO2.csv'
       # print(df_pivot.head().to_string(index=False))
       df_pivot.to_csv(save_results_pivot,  index=False, encoding='utf-8-sig', quoting=1)

    elif opcao ==3:
       # Process the first file
       # file_path_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv'
       file_path_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO.csv'
    #    df_graduados = pd.read_csv(file_path_graduados)
       df_graduados = pd.read_csv(file_path_graduados, dtype=str)

    #    # Subtract one digit from the specified columns
    #    # df_graduados['Curso_Superior_Graduação_Código'] = df_graduados['Curso_Superior_Graduação_Código'].astype(str).str[:-1].astype(int)
    #    # df_graduados['CBO-Domiciliar'] = df_graduados['CBO-Domiciliar'].astype(str).str[:-2].astype(int)
    #    df_graduados['CBO-Domiciliar'] = df_graduados['CBO-Domiciliar'].apply(
    #     lambda x: int(str(x)[:-1]) if len(str(x)) == 4 else int(str(x))
    #     )
    #    # Save the transformed DataFrame to a new file
    #    # save_results_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_DiminuidoCBO3.csv'
    #    save_results_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO_DiminuidoCBO3.csv'
    #    df_graduados.to_csv(save_results_graduados, index=False)

       # Subtrair um dígito da coluna CBO-Domiciliar baseada em string (preservando zeros à esquerda)
       df_graduados['CBO-Domiciliar'] = df_graduados['CBO-Domiciliar'].apply(
       lambda x: x[:-1] if len(x) == 4 else x
       )
       # Salvar o DataFrame transformado em um novo arquivo
       save_results_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO_DiminuidoCBO3.csv'
       df_graduados.to_csv(save_results_graduados, index=False, encoding='utf-8-sig', quoting=1)

       # Process the second file
       # file_path_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal.csv'      
       file_path_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_CBO.csv'
    #    df_pivot = pd.read_csv(file_path_pivot)
       df_pivot = pd.read_csv(file_path_pivot, dtype=str)

    #    # Subtract one digit from the Ocupação_Código column
    #    # df_pivot['CBO-Domiciliar'] = df_pivot['CBO-Domiciliar'].astype(str).str[:-2].astype(int)
    #    df_pivot['CBO-Domiciliar'] = df_pivot['CBO-Domiciliar'].apply(
    #     lambda x: int(str(x)[:-1]) if len(str(x)) == 4 else int(str(x))
    #    )
    #    # Save the transformed DataFrame to a new file
    #    # save_results_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_DiminuidaCBO3.csv'
    #    save_results_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_CBO_DiminuidaCBO3.csv'
    #    df_pivot.to_csv(save_results_pivot, index=False)
       df_pivot = pd.read_csv(file_path_pivot, dtype=str)
       # Subtrair um dígito da coluna CBO-Domiciliar baseada em string (preservando zeros à esquerda)
       df_pivot['CBO-Domiciliar'] = df_pivot['CBO-Domiciliar'].apply(
        lambda x: x[:-1] if len(x) == 4 else x
        )
       # Salvar o DataFrame transformado em um novo arquivo
       save_results_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_CBO_DiminuidaCBO3.csv'
       df_pivot.to_csv(save_results_pivot, index=False, encoding='utf-8-sig', quoting=1)
    return
