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



def Cursos_CBO_13_10_1(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo3,NaoGraduados_qtdade,Graduados_Nao_Total,curso_num,curso_nome,primeirosCbos_Nome,i,porcent_param,save_results_to):
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
    X_CURSO_CBO.shape

    #Cursos por CBO
    #Indice =================================================================================================
    X_CURSO_CBO['Ocupação_Código'] = X_CURSO_CBO['Ocupação_Código'].astype(int)
    dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['Ocupação_Código'] == int(str(cbo_num))].tolist()
    # dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['Ocupação_Código'] == cbo_num].tolist()
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
            # curso=str(float(A_Curso_11.index[i]))
            curso= A_Curso_11.index[i]
            for indexx, row in CURSOS.iterrows():               
                if (row['curso_num'] == curso): #if(row['Cod_Curso'] == A_Curso_10.index[i]): 10/05/2025
                    NomeCurso.append(row['curso_num']) #NomeCurso.append(row['Nome_Curso'])
                    # print(row['Cod_Curso'],":",row['Nome_Curso'])
                    # print(row['curso_num'], curso)
        # print("NomeCurso ================================================================")
        # print(NomeCurso)            
        #...
        #import pandas as pd
        #list_name = ['item_1', 'item_2', 'item_3', ...]
        NomeCurso = pd.DataFrame(NomeCurso, columns=['Nome_Curso'])
        print(NomeCurso)
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
            print("index =================================================================",index)
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


# Cursos por CBO 28/04/2024
# Achar CBOs por Curso
def CBOs_Curso_v6_1(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,porcent_param,save_results_to):
    X = pd.read_csv(csv_estado)
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    CBO = CBO.drop(columns=['Unnamed: 0'])
   
    #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
    X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']]
    
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
            cbo = X_CURSO_CBO._get_value(dir[i],'Ocupação_Código')
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
        porcento_10 = round(porcento/Total * 100, 2)
        # print(porcento_10)
        ...
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
        # print("A_cbo_10",A_cbo_10)
        if(len(A_cbo_10>=1)):
        # # Validação para testar se existem cbos para deteminado curso
        # if(len(A_cbo_10>=1)):
            #Coletando o nome do CBOs ...
            NomeCbo = []
            for i in range(len(A_cbo_10)):
                cbo = str(int(float(A_cbo_10.index[i])))
                for i in range(len(CBO)):
                    if (str(int(CBO['Cod_CBO'].iloc[i])) == cbo):
                        NomeCbo.append(CBO['Nome_CBO'].iloc[i])      
            NomeCbo = pd.DataFrame(NomeCbo, columns=['Nome_CBO'])
            #...
            # A_cbo_10["Nome"] = 1
            #...
            #import warnings
            if len(NomeCbo['Nome_CBO'].values) == len(A_cbo_10):
                A_cbo_10['Nome'] = NomeCbo['Nome_CBO'].values          
                # A_cbo_10['Nome'] = NomeCbo['Nome_CBO'].values
                #A_cbo_10
                A_cbo_10.reset_index(inplace=True)
                A_cbo_10 = A_cbo_10.rename(columns = {'index':'Cod_CBO'})
                # print(A_cbo_10)
                #A_cbo_10
                #...
                A_cbo_10['Cod_CBO'] = A_cbo_10['Cod_CBO'].astype("float").astype('str')
                A_cbo_10['CBO_Nome'] = A_cbo_10['Cod_CBO'].str.cat(A_cbo_10['Nome'], sep =" ")
                #print(A_cbo_10)

                # tresprimeiros Cbos
                primeiros = [] # Alterado em 29/09/2023
                if (len(A_cbo_10)<1):
                    print("Não existe CBOs para este curso")
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
                    print("Não existe CBOs para este curso")
                    # sys.exit() #===============================================================================================
                else:
                    for i in range(len(A_cbo_10)):
                        nomes.append(A_cbo_10.CBO_Nome[i])
                porcentagens = []
                if (len(A_cbo_10)<1):
                    print("Não existe CBOs para este curso")
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
                print("Erro: Comprimento dos valores não corresponde ao comprimento do índice.")
                print(f"Comprimento de NomeCbo['Nome_CBO']: {len(NomeCbo['Nome_CBO'].values)}")
                print(f"Comprimento de A_cbo_10: {len(A_cbo_10)}")
                # Ajuste aqui conforme necessário, por exemplo, truncar ou preencher os valores
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
    
    return primeiros,nomes,porcentagens,curso_num,curso_nome