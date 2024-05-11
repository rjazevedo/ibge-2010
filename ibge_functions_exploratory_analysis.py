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
import ibge_functions
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def Profissoes_Cursos(path1,name1,path2,name2): # https://colab.research.google.com/drive/1cTpvuIkd7FGZbzEkScU4xKGFb6sSbGog?authuser=1#scrollTo=MGx4AWThonQb

    # Leitura
    df =  os.path.join(path2[0],name2[2])
    X = pd.read_csv(df)    
    save_results_to = 'graficos/' 
    X = X.drop(columns=['Unnamed: 0'])
    X = X.drop(columns=['Unnamed: 0.1'])

    # Remoção de Features 
    X = X.drop(columns=['CB'])
    X = X.drop(columns=['CR'])

    CursosCenso = ibge_functions.ibge_cursos_filter(path1[0],name1[2])
    csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
    CBO = pd.read_csv(csv_CBO)


    # # Plotagem dos Dados Originais
    # # print(X.iloc[:,0])
    # plt.figure(figsize=(6, 4))
    # plt.title("10%  - Todos os Cursos - Clusterização ")
    # plt.xlabel('Ida')
    # plt.ylabel('Volta')
    # plt.ylim(0, 100) # definir limite do eixo
    # plt.xlim(0, 100) # definir limite do eixo
    # plt.grid()
    # plt.scatter(X.iloc[:,0],X.iloc[:,1],marker = '*')
    # # plt.show()
    # string = "10%  - Todos os Cursos - Dados Originais " +".pdf"
    # save_results_to = 'graficos/'  
    # plt.savefig(save_results_to + string)    

    # # The Elbow Method Graph
    # wcss=[]
    # for i in range(1,11):
    #     kmeans = KMeans(n_clusters=i, init ='k-means++', max_iter=300,  n_init=10,random_state=0 )
    #     kmeans.fit(X)
    #     wcss.append(kmeans.inertia_)
    # plt.plot(range(1,11),wcss,'bx-')
    # plt.title('The Elbow Method Graph')
    # plt.xlabel('Number of clusters')
    # plt.ylabel('WCSS')
    # # plt.show()
    # string1 = "10%  - The Elbow Method Graph " +".pdf"
    # save_results_to = 'graficos/'  
    # plt.savefig(save_results_to + string1)  

    # De acordo com o Metodo Elbow, determinar o numero de clusters
    kmeans = KMeans(n_clusters=3, init ='k-means++', max_iter=300, n_init=10,random_state=0 )
    y_kmeans = kmeans.fit_predict(X)
    # print(y_kmeans)
    # print(kmeans.labels_)

    #Clusterização
    plt.figure(figsize=(6, 4))
    plt.title("10%  - Todos os Cursos - Clusterização ")
    plt.xlabel('Cursos')
    plt.ylabel('Profissões')
    plt.ylim(0, 100) # definir limite do eixo
    plt.xlim(0, 100) # definir limite do eixo
    plt.grid()
    #6 Visualising the clusters
    plt.scatter(X.iloc[y_kmeans==0, 0], X.iloc[y_kmeans==0, 1], s=100, c='red', label ='Cluster 1', marker = '*')
    plt.scatter(X.iloc[y_kmeans==1, 0], X.iloc[y_kmeans==1, 1], s=100, c='blue', label ='Cluster 2', marker = '*')
    plt.scatter(X.iloc[y_kmeans==2, 0], X.iloc[y_kmeans==2, 1], s=100, c='green', label ='Cluster 3', marker = '*')
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='yellow', label = 'Centroids', marker = '*')
    plt.legend()
    # plt.show()
    string1 = "10%  - Todos os Cursos - Clusterização " +".pdf"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string1)  

    # # Centróides
    # kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1]
    # # cluster 1 : 27.00526316,21.78263158  ... Vermelho
    # # cluster 2 : 66.464375,  77.656875    ... Azul
    # # cluster 3:  25.76357143,62.88071429  ... Verde

    # # O que tem em cada cluster? ===================================================================================================================
    X['cluster'] = kmeans.labels_
    X = X.sort_values("cluster",ascending=True)
    # print(X)

    X_Original = pd.read_csv(df)
    X_Original = X_Original.drop(columns=['Unnamed: 0'])
    X_Original = X_Original.drop(columns=['Unnamed: 0.1'])
    # print(X_Original)

    # selecao_Kmeans3 = X_['cluster']==0
    selecao_Kmeans3 = X['cluster']==0
    X_0_Kmeans3 = X[selecao_Kmeans3]
    X_0_Kmeans3

    Kmeans3_CursoNum =[]
    Kmeans3_CboNum =[]
    for index, row in X_Original.iterrows():
        for indexx, roww in X_0_Kmeans3.iterrows():
            if (row['Ida']== roww['Ida']) and (row['Volta']==roww['Volta']):
                #CR_Cluster1Cursos_Kmeans3.append(row['CR'])
                Kmeans3_CursoNum.append(row['CR'])
                #Kmeans3_CursoNome.append(row['CR'])
                Kmeans3_CboNum.append(row['CB'])
                #Kmeans3_CboNome.append(row['CR'])#
    #print("len(Kmeans3_CursoNum):", len(Kmeans3_CursoNum))
    #print("len(Kmeans3_CboNum):", len(Kmeans3_CboNum))		 

    Kmeans3_CursoNome =[]
    for i in range (len(Kmeans3_CursoNum)):
        for index, row in CursosCenso.iterrows():
            if (str(Kmeans3_CursoNum[i]) == CursosCenso['curso_num'][index]):
                Kmeans3_CursoNome.append(CursosCenso['curso_nome'][index])
    #Kmeans3_CursoNome		

    Kmeans3_CboNome =[]
    for i in range (len(Kmeans3_CboNum)):
        for index, row in CBO.iterrows():
            if (int(Kmeans3_CboNum[i]) == CBO['Cod_CBO'][index]):
                Kmeans3_CboNome.append(CBO['Nome_CBO'][index])
    #Kmeans3_CboNome 
    
    Kmeans3_resultados_0=[]
    for i in range(len(Kmeans3_CursoNum)):
        tupla=(Kmeans3_CursoNum[i],Kmeans3_CursoNome[i],Kmeans3_CboNum[i],Kmeans3_CboNome[i])
        Kmeans3_resultados_0.append(tupla)
    #...
    kmeans3_0= pd.DataFrame(Kmeans3_resultados_0)
    #...
    dict = {0:"Curso",
            1:"Curso_Nome",
            2:"Cbo",
            3:"Cbo_Nome",
    }
    kmeans3_0.rename(columns=dict,inplace=True)
    # print(kmeans3_0)
    # print("")

    # selecao_Kmeans3 = X_['cluster']==1
    selecao_Kmeans3 = X['cluster']==1
    X_1_Kmeans3 = X[selecao_Kmeans3]

    Kmeans3_CursoNum =[]
    Kmeans3_CboNum =[]
    for index, row in X_Original.iterrows():
        for indexx, roww in X_1_Kmeans3.iterrows():
            if (row['Ida']== roww['Ida']) and (row['Volta']==roww['Volta']):
                #CR_Cluster1Cursos_Kmeans3.append(row['CR'])
                Kmeans3_CursoNum.append(row['CR'])
                #Kmeans3_CursoNome.append(row['CR'])
                Kmeans3_CboNum.append(row['CB'])
                #Kmeans3_CboNome.append(row['CR'])#
    # print("len(Kmeans3_CursoNum):", len(Kmeans3_CursoNum))
    # print("len(Kmeans3_CboNum):", len(Kmeans3_CboNum))    
    Kmeans3_CursoNome =[]

    for i in range (len(Kmeans3_CursoNum)):
        for index, row in CursosCenso.iterrows():
            if (str(Kmeans3_CursoNum[i]) == CursosCenso['curso_num'][index]):
                Kmeans3_CursoNome.append(CursosCenso['curso_nome'][index]) 
    # Kmeans3_CursoNome
    Kmeans3_CboNome =[]
    for i in range (len(Kmeans3_CboNum)):
        for index, row in CBO.iterrows():
            if (int(Kmeans3_CboNum[i]) == CBO['Cod_CBO'][index]):
                Kmeans3_CboNome.append(CBO['Nome_CBO'][index])   
    # Kmeans3_CboNome
    Kmeans3_resultados_1=[]
    for i in range(len(Kmeans3_CursoNum)):
        tupla=(Kmeans3_CursoNum[i],Kmeans3_CursoNome[i],Kmeans3_CboNum[i],Kmeans3_CboNome[i])
        Kmeans3_resultados_1.append(tupla)
    #...
    kmeans3_1= pd.DataFrame(Kmeans3_resultados_1)
    #...
    dict = {0:"Curso",
            1:"Curso_Nome",
            2:"Cbo",
            3:"Cbo_Nome",
    }
    kmeans3_1.rename(columns=dict,inplace=True) 
    # print(kmeans3_1)
    # print("")

    # selecao_Kmeans3 = X_['cluster']==2    
    selecao_Kmeans3 = X['cluster']==2
    X_2_Kmeans3 = X[selecao_Kmeans3]   
    # X_2_Kmeans3

    Kmeans3_CursoNum =[]
    Kmeans3_CboNum =[]
    for index, row in X_Original.iterrows():
        for indexx, roww in X_2_Kmeans3.iterrows():
            if (row['Ida']== roww['Ida']) and (row['Volta']==roww['Volta']):
                #CR_Cluster1Cursos_Kmeans3.append(row['CR'])
                Kmeans3_CursoNum.append(row['CR'])
                #Kmeans3_CursoNome.append(row['CR'])
                Kmeans3_CboNum.append(row['CB'])
                #Kmeans3_CboNome.append(row['CR'])#     
    # print("len(Kmeans3_CursoNum):", len(Kmeans3_CursoNum))
    # print("len(Kmeans3_CboNum):", len(Kmeans3_CboNum))
    
    Kmeans3_CursoNome =[]
    for i in range (len(Kmeans3_CursoNum)):
        for index, row in CursosCenso.iterrows():
            if (str(Kmeans3_CursoNum[i]) == CursosCenso['curso_num'][index]):
                Kmeans3_CursoNome.append(CursosCenso['curso_nome'][index])
    # Kmeans3_CursoNome
    
    Kmeans3_CboNome =[]
    for i in range (len(Kmeans3_CboNum)):
        for index, row in CBO.iterrows():
            if (int(Kmeans3_CboNum[i]) == CBO['Cod_CBO'][index]):
                Kmeans3_CboNome.append(CBO['Nome_CBO'][index])
    # Kmeans3_CboNome

    Kmeans3_resultados_2=[]
    for i in range(len(Kmeans3_CursoNum)):
        tupla=(Kmeans3_CursoNum[i],Kmeans3_CursoNome[i],Kmeans3_CboNum[i],Kmeans3_CboNome[i])
        Kmeans3_resultados_2.append(tupla)
    #...
    kmeans3_2= pd.DataFrame(Kmeans3_resultados_2)
    #...
    dict = {0:"Curso",
            1:"Curso_Nome",
            2:"Cbo",
            3:"Cbo_Nome",
    }
    kmeans3_2.rename(columns=dict,inplace=True) 
    # print(kmeans3_2)   

    # # O que tem em todos os  cluster? ===================================================================================================================
    Kmeans3_CursoNum =[]
    Kmeans3_CboNum =[]
    Kmeans3_CursosIda = []
    Kmeans3_CursosVolta = []
    Kmeans3_Cursoscluster = []

    for index, row in X_Original.iterrows():
        for indexx, roww in X.iterrows():
            if (row['Ida']== roww['Ida']) and (row['Volta']==roww['Volta']):
                Kmeans3_CursoNum.append(row['CR'])
                Kmeans3_CboNum.append(row['CB'])
                Kmeans3_CursosIda.append(row['Ida'])
                Kmeans3_CursosVolta.append(row['Volta'])
                Kmeans3_Cursoscluster.append(roww['cluster'])
                #Kmeans5_Cursoscluster.append(X_['cluster'][indexx])   
    # print("len(Kmeans3_CursoNum):", len(Kmeans3_CursoNum))
    # print("len(Kmeans3_CboNum):", len(Kmeans3_CboNum))
    # print("len(Kmeans3_CursosIda):", len(Kmeans3_CursosIda))
    # print("len(Kmeans3_CursosVolta):", len(Kmeans3_CursosVolta))
    # print("len(Kmeans3_Cursoscluster):", len(Kmeans3_Cursoscluster))     
    # Kmeans3_Cursoscluster
    Kmeans3_CursoNome =[]
    for i in range (len(Kmeans3_CursoNum)):
        for index, row in CursosCenso.iterrows():
            if (str(Kmeans3_CursoNum[i]) == CursosCenso['curso_num'][index]):
                Kmeans3_CursoNome.append(CursosCenso['curso_nome'][index])
    # Kmeans3_CursoNome  
    Kmeans3_CboNome =[]
    for i in range (len(Kmeans3_CboNum)):
        for index, row in CBO.iterrows():
            if (int(Kmeans3_CboNum[i]) == CBO['Cod_CBO'][index]):
                Kmeans3_CboNome.append(CBO['Nome_CBO'][index])                      
    # Kmeans3_CboNome
    Kmeans3_resultados_T=[]
    for i in range(len(Kmeans3_CursoNum)):
        tupla=(Kmeans3_CursosIda[i],Kmeans3_CursosVolta[i],Kmeans3_Cursoscluster[i], Kmeans3_CursoNum[i],Kmeans3_CursoNome[i],Kmeans3_CboNum[i],Kmeans3_CboNome[i])
        Kmeans3_resultados_T.append(tupla)
    #...
    Kmeans3_T= pd.DataFrame(Kmeans3_resultados_T)
    #...
    dict = {0:"Ida",
            1:"Volta",
            2:"Cluster",
            3:"Curso",
            4:"Curso_Nome",
            5:"Cbo",
            6:"Cbo_Nome"
    }
    Kmeans3_T.rename(columns=dict,inplace=True)       
    # Unique_Cursos = Kmeans3_T.Curso_Nome.unique()
    # len(Unique_Cursos)     
    # Unique_Cbo = Kmeans3_T.Cbo_Nome.unique()
    # len(Unique_Cbo)
    # Kmeans3_T
    Kmeans3_T.to_csv(save_results_to +'Kmeans3_T.csv')
    return