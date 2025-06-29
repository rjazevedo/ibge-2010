#pip install ibge-parser

import logging
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
import ibge_functions_descriptive_analysis
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# def Profissoes_Cursos_1(path1,name1,path2,name2): # https://colab.research.google.com/drive/1cTpvuIkd7FGZbzEkScU4xKGFb6sSbGog?authuser=1#scrollTo=MGx4AWThonQb

#     # Leitura
#     df =  os.path.join(path2[0],name2[2])
#     X = pd.read_csv(df)    
#     save_results_to = 'graficos/' 
#     X = X.drop(columns=['Unnamed: 0'])
#     X = X.drop(columns=['Unnamed: 0.1'])

#     # Remoção de Features 
#     X = X.drop(columns=['CB'])
#     X = X.drop(columns=['CR'])

#     CursosCenso = ibge_functions_descriptive_analysis.ibge_cursos_filter(path1[0],name1[2])
#     csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
#     CBO = pd.read_csv(csv_CBO)


#     # # Plotagem dos Dados Originais
#     # # print(X.iloc[:,0])
#     # plt.figure(figsize=(6, 4))
#     # plt.title("10%  - Todos os Cursos - Clusterização ")
#     # plt.xlabel('Ida')
#     # plt.ylabel('Volta')
#     # plt.ylim(0, 100) # definir limite do eixo
#     # plt.xlim(0, 100) # definir limite do eixoA
#     # plt.grid()
#     # plt.scatter(X.iloc[:,0],X.iloc[:,1],marker = '*')
#     # # plt.show()
#     # string = "10%  - Todos os Cursos - Dados Originais " +".pdf"
#     # save_results_to = 'graficos/'  
#     # plt.savefig(save_results_to + string)    

#     # # The Elbow Method Graph
#     # wcss=[]
#     # for i in range(1,11):
#     #     kmeans = KMeans(n_clusters=i, init ='k-means++', max_iter=300,  n_init=10,random_state=0 )
#     #     kmeans.fit(X)
#     #     wcss.append(kmeans.inertia_)
#     # plt.plot(range(1,11),wcss,'bx-')
#     # plt.title('The Elbow Method Graph')
#     # plt.xlabel('Number of clusters')
#     # plt.ylabel('WCSS')
#     # # plt.show()
#     # string1 = "10%  - The Elbow Method Graph " +".pdf"
#     # save_results_to = 'graficos/'  
#     # plt.savefig(save_results_to + string1)  

#     # De acordo com o Metodo Elbow, determinar o numero de clusters
#     kmeans = KMeans(n_clusters=3, init ='k-means++', max_iter=300, n_init=10,random_state=0 )
#     y_kmeans = kmeans.fit_predict(X)
#     # print(y_kmeans)
#     # print(kmeans.labels_)

#     #Clusterização
#     #plt.figure(figsize=(6, 4))
#     #plt.title("10%  - Todos os Cursos - Clusterização ")
#     #plt.xlabel('Cursos')
#     #plt.ylabel('Profissões')
#     # plt.title("10% - All Courses - Clustering") # Diversos  ( Explicações e correções) e Estilo de texto 
#     plt.xlabel('Courses')
#     plt.ylabel('Professions')
#     plt.ylim(0, 100) # definir limite do eixo
#     plt.xlim(0, 100) # definir limite do eixo
#     plt.grid()
#     # Visualising the clusters
#     plt.scatter(X.iloc[y_kmeans==0, 0], X.iloc[y_kmeans==0, 1], s=100, c='red', label ='Cluster 0', marker = '*')

#     # Filtrar cursos específicos
#     cursos_especificos = [214, 342, 520, 721, 726]
#     for curso in cursos_especificos:
#         plt.scatter(X.iloc[y_kmeans==2, 0], X.iloc[y_kmeans==curso, 1], s=100, label=f'Cluster {curso}', marker='*')
#         plt.scatter(X.iloc[y_kmeans==1, 0], X.iloc[y_kmeans==1, 1], s=100, c='blue', label ='Cluster 1', marker = '*')
#         plt.scatter(X.iloc[y_kmeans==2, 0], X.iloc[y_kmeans==2, 1], s=100, c='green', label ='Cluster 2', marker = '*')
#     # plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='yellow', label = 'Centroids', marker = '*') # Diversos  ( Explicações e correções) e Estilo de texto 
#     plt.legend()
#     # plt.show()
#     # string1 = "10%  - Todos os Cursos - Clusterização " +".pdf"
#     # string1 = "10% - All Courses - Clustering" +".pdf"
#     string1 = "10% - All Courses - Clustering - 1" +".png"
#     save_results_to = 'graficos/'  
#     plt.savefig(save_results_to + string1)  

#     # # Centróides
#     # kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1]
#     # # cluster 1 : 27.00526316,21.78263158  ... Vermelho
#     # # cluster 2 : 66.464375,  77.656875    ... Azul
#     # # cluster 3:  25.76357143,62.88071429  ... Verde

#     # # O que tem em cada cluster? ===================================================================================================================
#     X['cluster'] = kmeans.labels_
#     X = X.sort_values("cluster",ascending=True)
#     # print(X)

#     X_Original = pd.read_csv(df)
#     X_Original = X_Original.drop(columns=['Unnamed: 0'])
#     X_Original = X_Original.drop(columns=['Unnamed: 0.1'])
#     # print(X_Original)

#     # selecao_Kmeans3 = X_['cluster']==0
#     selecao_Kmeans3 = X['cluster']==0
#     X_0_Kmeans3 = X[selecao_Kmeans3]
#     X_0_Kmeans3

#     Kmeans3_CursoNum =[]
#     Kmeans3_CboNum =[]
#     for index, row in X_Original.iterrows():
#         for indexx, roww in X_0_Kmeans3.iterrows():
#             if (row['Ida']== roww['Ida']) and (row['Volta']==roww['Volta']):
#                 #CR_Cluster1Cursos_Kmeans3.append(row['CR'])
#                 Kmeans3_CursoNum.append(row['CR'])
#                 #Kmeans3_CursoNome.append(row['CR'])
#                 Kmeans3_CboNum.append(row['CB'])
#                 #Kmeans3_CboNome.append(row['CR'])#
#     #print("len(Kmeans3_CursoNum):", len(Kmeans3_CursoNum))
#     #print("len(Kmeans3_CboNum):", len(Kmeans3_CboNum))		 

#     Kmeans3_CursoNome =[]
#     for i in range (len(Kmeans3_CursoNum)):
#         for index, row in CursosCenso.iterrows():
#             if (str(Kmeans3_CursoNum[i]) == CursosCenso['curso_num'][index]):
#                 Kmeans3_CursoNome.append(CursosCenso['curso_nome'][index])
#     #Kmeans3_CursoNome		

#     Kmeans3_CboNome =[]
#     for i in range (len(Kmeans3_CboNum)):
#         for index, row in CBO.iterrows():
#             if (int(Kmeans3_CboNum[i]) == CBO['Cod_CBO'][index]):
#                 Kmeans3_CboNome.append(CBO['Nome_CBO'][index])
#     #Kmeans3_CboNome 
    
#     Kmeans3_resultados_0=[]
#     for i in range(len(Kmeans3_CursoNum)):
#         tupla=(Kmeans3_CursoNum[i],Kmeans3_CursoNome[i],Kmeans3_CboNum[i],Kmeans3_CboNome[i])
#         Kmeans3_resultados_0.append(tupla)
#     #...
#     kmeans3_0= pd.DataFrame(Kmeans3_resultados_0)
#     #...
#     dict = {0:"Curso",
#             1:"Curso_Nome",
#             2:"Cbo",
#             3:"Cbo_Nome",
#     }
#     kmeans3_0.rename(columns=dict,inplace=True)
#     # print(kmeans3_0)
#     # print("")

#     # selecao_Kmeans3 = X_['cluster']==1
#     selecao_Kmeans3 = X['cluster']==1
#     X_1_Kmeans3 = X[selecao_Kmeans3]

#     Kmeans3_CursoNum =[]
#     Kmeans3_CboNum =[]
#     for index, row in X_Original.iterrows():
#         for indexx, roww in X_1_Kmeans3.iterrows():
#             if (row['Ida']== roww['Ida']) and (row['Volta']==roww['Volta']):
#                 #CR_Cluster1Cursos_Kmeans3.append(row['CR'])
#                 Kmeans3_CursoNum.append(row['CR'])
#                 #Kmeans3_CursoNome.append(row['CR'])
#                 Kmeans3_CboNum.append(row['CB'])
#                 #Kmeans3_CboNome.append(row['CR'])#
#     # print("len(Kmeans3_CursoNum):", len(Kmeans3_CursoNum))
#     # print("len(Kmeans3_CboNum):", len(Kmeans3_CboNum))    
#     Kmeans3_CursoNome =[]

#     for i in range (len(Kmeans3_CursoNum)):
#         for index, row in CursosCenso.iterrows():
#             if (str(Kmeans3_CursoNum[i]) == CursosCenso['curso_num'][index]):
#                 Kmeans3_CursoNome.append(CursosCenso['curso_nome'][index]) 
#     # Kmeans3_CursoNome
#     Kmeans3_CboNome =[]
#     for i in range (len(Kmeans3_CboNum)):
#         for index, row in CBO.iterrows():
#             if (int(Kmeans3_CboNum[i]) == CBO['Cod_CBO'][index]):
#                 Kmeans3_CboNome.append(CBO['Nome_CBO'][index])   
#     # Kmeans3_CboNome
#     Kmeans3_resultados_1=[]
#     for i in range(len(Kmeans3_CursoNum)):
#         tupla=(Kmeans3_CursoNum[i],Kmeans3_CursoNome[i],Kmeans3_CboNum[i],Kmeans3_CboNome[i])
#         Kmeans3_resultados_1.append(tupla)
#     #...
#     kmeans3_1= pd.DataFrame(Kmeans3_resultados_1)
#     #...
#     dict = {0:"Curso",
#             1:"Curso_Nome",
#             2:"Cbo",
#             3:"Cbo_Nome",
#     }
#     kmeans3_1.rename(columns=dict,inplace=True) 
#     # print(kmeans3_1)
#     # print("")

#     # selecao_Kmeans3 = X_['cluster']==2    
#     selecao_Kmeans3 = X['cluster']==2
#     X_2_Kmeans3 = X[selecao_Kmeans3]   
#     # X_2_Kmeans3

#     Kmeans3_CursoNum =[]
#     Kmeans3_CboNum =[]
#     for index, row in X_Original.iterrows():
#         for indexx, roww in X_2_Kmeans3.iterrows():
#             if (row['Ida']== roww['Ida']) and (row['Volta']==roww['Volta']):
#                 #CR_Cluster1Cursos_Kmeans3.append(row['CR'])
#                 Kmeans3_CursoNum.append(row['CR'])
#                 #Kmeans3_CursoNome.append(row['CR'])
#                 Kmeans3_CboNum.append(row['CB'])
#                 #Kmeans3_CboNome.append(row['CR'])#     
#     # print("len(Kmeans3_CursoNum):", len(Kmeans3_CursoNum))
#     # print("len(Kmeans3_CboNum):", len(Kmeans3_CboNum))
    
#     Kmeans3_CursoNome =[]
#     for i in range (len(Kmeans3_CursoNum)):
#         for index, row in CursosCenso.iterrows():
#             if (str(Kmeans3_CursoNum[i]) == CursosCenso['curso_num'][index]):
#                 Kmeans3_CursoNome.append(CursosCenso['curso_nome'][index])
#     # Kmeans3_CursoNome
    
#     Kmeans3_CboNome =[]
#     for i in range (len(Kmeans3_CboNum)):
#         for index, row in CBO.iterrows():
#             if (int(Kmeans3_CboNum[i]) == CBO['Cod_CBO'][index]):
#                 Kmeans3_CboNome.append(CBO['Nome_CBO'][index])
#     # Kmeans3_CboNome

#     Kmeans3_resultados_2=[]
#     for i in range(len(Kmeans3_CursoNum)):
#         tupla=(Kmeans3_CursoNum[i],Kmeans3_CursoNome[i],Kmeans3_CboNum[i],Kmeans3_CboNome[i])
#         Kmeans3_resultados_2.append(tupla)
#     #...
#     kmeans3_2= pd.DataFrame(Kmeans3_resultados_2)
#     #...
#     dict = {0:"Curso",
#             1:"Curso_Nome",
#             2:"Cbo",
#             3:"Cbo_Nome",
#     }
#     kmeans3_2.rename(columns=dict,inplace=True) 
#     # print(kmeans3_2)   

#     # # O que tem em todos os  cluster? ===================================================================================================================
#     Kmeans3_CursoNum =[]
#     Kmeans3_CboNum =[]
#     Kmeans3_CursosIda = []
#     Kmeans3_CursosVolta = []
#     Kmeans3_Cursoscluster = []

#     for index, row in X_Original.iterrows():
#         for indexx, roww in X.iterrows():
#             if (row['Ida']== roww['Ida']) and (row['Volta']==roww['Volta']):
#                 Kmeans3_CursoNum.append(row['CR'])
#                 Kmeans3_CboNum.append(row['CB'])
#                 Kmeans3_CursosIda.append(row['Ida'])
#                 Kmeans3_CursosVolta.append(row['Volta'])
#                 Kmeans3_Cursoscluster.append(roww['cluster'])
#                 #Kmeans5_Cursoscluster.append(X_['cluster'][indexx])   
#     # print("len(Kmeans3_CursoNum):", len(Kmeans3_CursoNum))
#     # print("len(Kmeans3_CboNum):", len(Kmeans3_CboNum))
#     # print("len(Kmeans3_CursosIda):", len(Kmeans3_CursosIda))
#     # print("len(Kmeans3_CursosVolta):", len(Kmeans3_CursosVolta))
#     # print("len(Kmeans3_Cursoscluster):", len(Kmeans3_Cursoscluster))     
#     # Kmeans3_Cursoscluster
#     Kmeans3_CursoNome =[]
#     for i in range (len(Kmeans3_CursoNum)):
#         for index, row in CursosCenso.iterrows():
#             if (str(Kmeans3_CursoNum[i]) == CursosCenso['curso_num'][index]):
#                 Kmeans3_CursoNome.append(CursosCenso['curso_nome'][index])
#     # Kmeans3_CursoNome  
#     Kmeans3_CboNome =[]
#     for i in range (len(Kmeans3_CboNum)):
#         for index, row in CBO.iterrows():
#             if (int(Kmeans3_CboNum[i]) == CBO['Cod_CBO'][index]):
#                 Kmeans3_CboNome.append(CBO['Nome_CBO'][index])                      
#     # Kmeans3_CboNome
#     Kmeans3_resultados_T=[]
#     for i in range(len(Kmeans3_CursoNum)):
#         tupla=(Kmeans3_CursosIda[i],Kmeans3_CursosVolta[i],Kmeans3_Cursoscluster[i], Kmeans3_CursoNum[i],Kmeans3_CursoNome[i],Kmeans3_CboNum[i],Kmeans3_CboNome[i])
#         Kmeans3_resultados_T.append(tupla)
#     #...
#     Kmeans3_T= pd.DataFrame(Kmeans3_resultados_T)
#     #...
#     dict = {0:"Ida",
#             1:"Volta",
#             2:"Cluster",
#             3:"Curso",
#             4:"Curso_Nome",
#             5:"Cbo",
#             6:"Cbo_Nome"
#     }
#     Kmeans3_T.rename(columns=dict,inplace=True)       
#     # Unique_Cursos = Kmeans3_T.Curso_Nome.unique()
#     # len(Unique_Cursos)     
#     # Unique_Cbo = Kmeans3_T.Cbo_Nome.unique()
#     # len(Unique_Cbo)
#     # Kmeans3_T
#     Kmeans3_T.to_csv(save_results_to +'Kmeans3_T.csv')
#     return

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

    CursosCenso = ibge_functions_descriptive_analysis.ibge_cursos_filter(path1[0],name1[2])
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
    #plt.figure(figsize=(6, 4))
    #plt.title("10%  - Todos os Cursos - Clusterização ")
    plt.xlabel('Cursos')
    plt.ylabel('Profissões')
    # plt.title("10% - All Courses - Clustering") # Diversos  ( Explicações e correções) e Estilo de texto 
    # plt.xlabel('Courses')
    # plt.ylabel('Professions')
    plt.ylim(0, 100) # definir limite do eixo
    plt.xlim(0, 100) # definir limite do eixo
    plt.grid()
    # Visualising the clusters
    plt.scatter(X.iloc[y_kmeans==0, 0], X.iloc[y_kmeans==0, 1], s=100, c='red', label ='Cluster 0', marker = '*')
    plt.scatter(X.iloc[y_kmeans==1, 0], X.iloc[y_kmeans==1, 1], s=100, c='blue', label ='Cluster 1', marker = '*')
    plt.scatter(X.iloc[y_kmeans==2, 0], X.iloc[y_kmeans==2, 1], s=100, c='green', label ='Cluster 2', marker = '*')
    # plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='yellow', label = 'Centroids', marker = '*') # Diversos  ( Explicações e correções) e Estilo de texto 
    plt.legend()
    # plt.show()
    # string1 = "10%  - Todos os Cursos - Clusterização " +".pdf"
    # string1 = "10% - All Courses - Clustering" +".pdf"
    string1 = "10% - All Courses - Clustering" +".png"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string1)  


    # # Centróides
    # kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1]
    # # cluster 1 : 27.00526316,21.78263158  ... Vermelho
    # # cluster 2 : 66.464375,  77.656875    ... Azul
    # # cluster 3:  25.76357143,62.88071429  ... Verde
          
    
   # Obtendo os centróides
    centroids = kmeans.cluster_centers_
    # Criando um DataFrame com os centróides
    df_centroids = pd.DataFrame(centroids, columns=['x', 'y'])
    # Salvando os centróides em um arquivo CSV
    df_centroids.to_csv(save_results_to + 'centroids.csv', index=False)

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





def Soma_PivotTable(path1,name1):
    ##### -------------------------------- Usar um arquivo de teste para empregabilidade
    # Carregar o arquivo CSV
    file_path = "graficos/Kmeans3_T.csv"  # Substitua pelo caminho do arquivo
    Kmeans3_T = pd.read_csv(file_path)
    save_results_to = 'graficos/' 
    
    #Kmeans3_T = Kmeans3_T.drop(columns=['Unnamed: 0'])

    Pivot = pd.read_csv("processados/CSVs_PivotTableFinal/Brasil_PivotFinal.csv", sep=",")
    # Pivot = Pivot.drop(columns=['Unnamed: 0'])
    
    # Somar as colunas 1, 2, 3, 4, 5 para cada ocupação
    Pivot['Soma'] = Pivot.iloc[:, 1:6].sum(axis=1)
    
    # Gerar um novo arquivo somente com as ocupações e a soma
    novo_arquivo = Pivot[['Ocupação_Código', 'Soma']]
    novo_arquivo.to_csv("processados/CSVs_PivotTableFinal/Soma_Ocupacao.csv", index=False)
    return    

# def Coluna_Empregabilidade(path2,name2):
#     ##### -------------------------------- Usar um arquivo de teste para empregabilidade
#     # Carregar o arquivo CSV
#     file_path = "graficos/Kmeans3_T.csv"  # Substitua pelo caminho do arquivo
#     Kmeans3_T = pd.read_csv(file_path)
#     save_results_to = 'graficos/' 
    
#     #Kmeans3_T = Kmeans3_T.drop(columns=['Unnamed: 0'])

#     Empregabilidade = pd.read_csv("processados/CSVs_PivotTableFinal/Soma_Ocupacao.csv", sep=",")
#     # Pivot = Pivot.drop(columns=['Unnamed: 0'])
    
#     # Juntar as colunas de Kmeans3_T e a coluna Soma de Empregabilidade
#     Kmeans3_T['Soma_Empregabilidade'] = Empregabilidade['Soma']
    
#     # Se Kmeans3_T .Curso == 520, então Empregabilidade['Soma']/500
#     Kmeans3_T.loc[Kmeans3_T['Curso'] == 214, 'Soma_Empregabilidade'] = Empregabilidade['Soma'] / 40
#     Kmeans3_T.loc[Kmeans3_T['Curso'] == 342, 'Soma_Empregabilidade'] = Empregabilidade['Soma'] / 40
#     Kmeans3_T.loc[Kmeans3_T['Curso'] == 520, 'Soma_Empregabilidade'] = Empregabilidade['Soma'] / 40
#     Kmeans3_T.loc[Kmeans3_T['Curso'] == 721, 'Soma_Empregabilidade'] = Empregabilidade['Soma'] / 40
#     Kmeans3_T.loc[Kmeans3_T['Curso'] == 726, 'Soma_Empregabilidade'] = Empregabilidade['Soma'] / 40
#     # Kmeans3_T.loc[Kmeans3_T['Soma_Empregabilidade'] > 4000, 'Soma_Empregabilidade'] = Empregabilidade['Soma'] / 30



def Coluna_Empregabilidade(path2,name2):
    ##### -------------------------------- Usar um arquivo de teste para empregabilidade
    # Carregar o arquivo CSV
    file_path = "graficos/Kmeans3_T.csv"  # Substitua pelo caminho do arquivo
    Kmeans3_T = pd.read_csv(file_path)
    save_results_to = 'graficos/' 
    
    #Kmeans3_T = Kmeans3_T.drop(columns=['Unnamed: 0'])

    Empregabilidade = pd.read_csv("processados/CSVs_PivotTableFinal/Soma_Ocupacao.csv", sep=",")
    # Pivot = Pivot.drop(columns=['Unnamed: 0'])
    
    # Juntar as colunas de Kmeans3_T e a coluna Soma de Empregabilidade
    Kmeans3_T['Soma_Empregabilidade'] = Empregabilidade['Soma']
    
    # Se Kmeans3_T .Curso == 520, então Empregabilidade['Soma']/500
    Kmeans3_T.loc[Kmeans3_T['Curso'] == 142, 'Soma_Empregabilidade'] = np.log(Empregabilidade['Soma'] + 1) * 10 # Multiplicando para ajustar a escala
    Kmeans3_T.loc[Kmeans3_T['Curso'] == 145, 'Soma_Empregabilidade'] = np.log(Empregabilidade['Soma'] + 1) * 10 # Multiplicando para ajustar a escala
    Kmeans3_T.loc[Kmeans3_T['Curso'] == 211, 'Soma_Empregabilidade'] = np.log(Empregabilidade['Soma'] + 1) * 10 # Multiplicando para ajustar a escala
    Kmeans3_T.loc[Kmeans3_T['Curso'] == 212, 'Soma_Empregabilidade'] = np.log(Empregabilidade['Soma'] + 1) * 10 # Multiplicando para ajustar a escala
    Kmeans3_T.loc[Kmeans3_T['Curso'] == 214, 'Soma_Empregabilidade'] = np.log(Empregabilidade['Soma'] + 1) * 10 # Multiplicando para ajustar a escala
    Kmeans3_T.loc[Kmeans3_T['Curso'] == 223, 'Soma_Empregabilidade'] = np.log(Empregabilidade['Soma'] + 1) * 10 # Multiplicando para ajustar a escala
    Kmeans3_T.loc[Kmeans3_T['Curso'] == 342, 'Soma_Empregabilidade'] = np.log(Empregabilidade['Soma'] + 1) * 10 # Multiplicando para ajustar a escala
    Kmeans3_T.loc[Kmeans3_T['Curso'] == 520, 'Soma_Empregabilidade'] = np.log(Empregabilidade['Soma'] + 1) * 10 # Multiplicando para ajustar a escala
    Kmeans3_T.loc[Kmeans3_T['Curso'] == 721, 'Soma_Empregabilidade'] = np.log(Empregabilidade['Soma'] + 1) * 10 # Multiplicando para ajustar a escala
    Kmeans3_T.loc[Kmeans3_T['Curso'] == 726, 'Soma_Empregabilidade'] = np.log(Empregabilidade['Soma'] + 1) * 10 # Multiplicando para ajustar a escala
    # Kmeans3_T.loc[Kmeans3_T['Soma_Empregabilidade'] > 4000, 'Soma_Empregabilidade'] = Empregabilidade['Soma'] / 30
   
    # Arredondar os valores da coluna 'Soma_Empregabilidade' para o inteiro mais próximo
    # Kmeans3_T['Soma_Empregabilidade'] = np.round(Kmeans3_T['Soma_Empregabilidade'])
    Kmeans3_T['Soma_Empregabilidade'] = Kmeans3_T['Soma_Empregabilidade'].astype(int)

    # Salvar o novo arquivo
    novo_arquivo = "graficos/Kmeans3_T_Empregabilidade_teste.csv"
    Kmeans3_T.to_csv(novo_arquivo, index=False)    
    return

def Empregabilidade(path1,name1,path2,name2):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    import pandas as pd
    import numpy as np
    from sklearn.cluster import KMeans

    ##### ---------------------------------- Gerar o arquivo de empregabilidade
    # # Carregar o arquivo CSV
    # file_path = "graficos/Kmeans3_T.csv"  # Substitua pelo caminho do arquivo
    # data = pd.read_csv(file_path)
    # save_results_to = 'graficos/' 
    
    # # Filtrar as linhas com CR: 214, 342, 520, 721, 726
    # cr_values = [214, 342, 520, 721, 726]
    # filtered_data = data[data['Curso'].isin(cr_values)]
       
    # # Salvar o novo arquivo
    # filtered_file_path = save_results_to + 'Kmeans3_T.csv_Empregabilidade.csv'
    # filtered_data.to_csv(filtered_file_path, index=False)
    
    ##### -------------------------------- Usar um arquivo de teste para empregabilidade
    # Carregar o arquivo CSV
    # file_path = "graficos/Kmeans3_T_Empregabilidade.csv"  # Substitua pelo caminho do arquivo
    file_path = "graficos/Kmeans3_T_Empregabilidade_teste.csv"  # Substitua pelo caminho do arquivo
    data = pd.read_csv(file_path)
    save_results_to = 'graficos/' 
    
    # Filtrar as linhas com CR: 214, 342, 520, 721, 726
    cr_values = [214, 342, 520, 721, 726]
    filtered_data = data[data['Curso'].isin(cr_values)]

    ##### -------------------------------- Gráfico separado por cursos 
    # Configurar o gráfico de dispersão usando as colunas 'Ida', 'Volta' e 'Cluster'
    plt.figure(figsize=(6, 4))    

    # # Lista de cores para os clusters
    cores_personalizadas = ['red', 'blue', 'brown', 'black', 'green']  # Adicione mais cores, se necessário

    # # Ordenar os clusters antes de criar o gráfico
    clusters_ordenados = sorted(filtered_data['Curso'].unique())


    # # Criar o scatter plot para os clusters com cores personalizadas
    for i, cluster in enumerate(clusters_ordenados):
          cluster_data = filtered_data[data['Curso'] == cluster]
          plt.scatter(
              cluster_data['Ida'], 
              cluster_data['Volta'], 
              label=f'Curso {int(cluster)}', 
              marker='.',  # Define o marcador como estrela
              color=cores_personalizadas[i % len(cores_personalizadas)],  # Escolhe a cor da lista
             #  s=100  # Define o tamanho dos marcadores
             #  s=cluster_data['Empregabilidade'] * 20,  # Define o tamanho dos pontos com base na empregabilidade (ajuste o fator de multiplicação conforme necessário)
              s=cluster_data['Soma_Empregabilidade'],  # Define o tamanho dos pontos com base na empregabilidade (ajuste o fator de multiplicação conforme necessário)

          )     

    # ##### -------------------------------- Gráfico separado por Clusters
    # # Configurar o gráfico de dispersão usando as colunas 'Ida', 'Volta' e 'Cluster'
    # plt.figure(figsize=(6, 4))    

    # # Lista de cores para os clusters
    # cores_personalizadas = ['red', 'blue', 'green', 'black', 'pink']  # Adicione mais cores, se necessário

    # # Ordenar os clusters antes de criar o gráfico
    # clusters_ordenados = sorted(filtered_data['Cluster'].unique())


    # # Criar o scatter plot para os clusters com cores personalizadas
    # for i, cluster in enumerate(clusters_ordenados):
    #      cluster_data = filtered_data[data['Cluster'] == cluster]
    #      plt.scatter(
    #          cluster_data['Ida'], 
    #          cluster_data['Volta'], 
    #          label=f'Cluster {int(cluster)}', 
    #          marker='.',  # Define o marcador como estrela
    #          color=cores_personalizadas[i % len(cores_personalizadas)],  # Escolhe a cor da lista
    #         #  s=100  # Define o tamanho dos marcadores
    #         s=cluster_data['Empregabilidade'] * 20,  # Define o tamanho dos pontos com base na empregabilidade (ajuste o fator de multiplicação conforme necessário)
    #      )   

    # Personalizar o gráfico
    # plt.figure(figsize=(100, 80))  # Aumentar o tamanho do gráfico
    plt.legend(title="Cursos", loc='lower right', prop={'size': 7})  # Reduzir o tamanho da legenda
    # plt.legend(markerscale=1)
    # plt.title('Empregabilidade ')
    plt.xlabel('Cursos')
    plt.ylabel('Profissões')
    plt.ylim(0, 100) # definir limite do eixo
    plt.xlim(0, 100) # definir limite do eixo
    # plt.legend(title="Cursos", loc='lower right')
    # plt.legend(title="Cursos", loc='lower right', prop={'size': 10})
    plt.grid()

    # Mostrar o gráfico
    # plt.show()
    # string1 = "Cursos e Profissões que mudam de Clusters" +".png"
    string1 = "Empregabilidade_Cursos_Profissões_mudam_Clusters" +".png"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string1)  
    return

def Empregabilidade_cursos_commaisprofissoes(path1,name1,path2,name2):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    import pandas as pd
    import numpy as np
    from sklearn.cluster import KMeans

    ##### ---------------------------------- Gerar o arquivo de empregabilidade
    # # Carregar o arquivo CSV
    # file_path = "graficos/Kmeans3_T.csv"  # Substitua pelo caminho do arquivo
    # data = pd.read_csv(file_path)
    # save_results_to = 'graficos/' 
    
    # # Filtrar as linhas com CR: 214, 342, 520, 721, 726
    # cr_values = [214, 342, 520, 721, 726]
    # filtered_data = data[data['Curso'].isin(cr_values)]
       
    # # Salvar o novo arquivo
    # filtered_file_path = save_results_to + 'Kmeans3_T.csv_Empregabilidade.csv'
    # filtered_data.to_csv(filtered_file_path, index=False)
    
    ##### -------------------------------- Usar um arquivo de teste para empregabilidade
    # Carregar o arquivo CSV
    # file_path = "graficos/Kmeans3_T_Empregabilidade.csv"  # Substitua pelo caminho do arquivo
    file_path = "graficos/Kmeans3_T_Empregabilidade_teste.csv"  # Substitua pelo caminho do arquivo
    data = pd.read_csv(file_path)
    save_results_to = 'graficos/' 
    
    # Filtrar as linhas com CR: 214, 342, 520, 721, 726
    # cr_values = [142, 145, 211, 212, 214, 223, 342, 520, 721, 726]
    cr_values = [142, 145, 211, 212, 223]
    filtered_data = data[data['Curso'].isin(cr_values)]

    ##### -------------------------------- Gráfico separado por cursos 
    # Configurar o gráfico de dispersão usando as colunas 'Ida', 'Volta' e 'Cluster'
    plt.figure(figsize=(6, 4))    

    # # Lista de cores para os clusters
    #cores_personalizadas = ['DarkViolet', 'DarkMagenta', 'DeepPink', 'Crimson',
    #                        'red', 'Yellow', 'blue', 'brown', 'black', 'green']  # Adicione mais cores, se necessário
    cores_personalizadas = ['red', 'blue', 'brown', 'black', 'green']  # Adicione mais cores, se necessário

    # # Ordenar os clusters antes de criar o gráfico
    clusters_ordenados = sorted(filtered_data['Curso'].unique())


    # # Criar o scatter plot para os clusters com cores personalizadas
    for i, cluster in enumerate(clusters_ordenados):
          cluster_data = filtered_data[data['Curso'] == cluster]
          plt.scatter(
              cluster_data['Ida'], 
              cluster_data['Volta'], 
              label=f'Curso {int(cluster)}', 
              marker='.',  # Define o marcador como estrela
              color=cores_personalizadas[i % len(cores_personalizadas)],  # Escolhe a cor da lista
             #  s=100  # Define o tamanho dos marcadores
             #  s=cluster_data['Empregabilidade'] * 20,  # Define o tamanho dos pontos com base na empregabilidade (ajuste o fator de multiplicação conforme necessário)
              s=cluster_data['Soma_Empregabilidade'],  # Define o tamanho dos pontos com base na empregabilidade (ajuste o fator de multiplicação conforme necessário)

          )     

    # ##### -------------------------------- Gráfico separado por Clusters
    # # Configurar o gráfico de dispersão usando as colunas 'Ida', 'Volta' e 'Cluster'
    # plt.figure(figsize=(6, 4))    

    # # Lista de cores para os clusters
    # cores_personalizadas = ['red', 'blue', 'green', 'black', 'pink']  # Adicione mais cores, se necessário

    # # Ordenar os clusters antes de criar o gráfico
    # clusters_ordenados = sorted(filtered_data['Cluster'].unique())


    # # Criar o scatter plot para os clusters com cores personalizadas
    # for i, cluster in enumerate(clusters_ordenados):
    #      cluster_data = filtered_data[data['Cluster'] == cluster]
    #      plt.scatter(
    #          cluster_data['Ida'], 
    #          cluster_data['Volta'], 
    #          label=f'Cluster {int(cluster)}', 
    #          marker='.',  # Define o marcador como estrela
    #          color=cores_personalizadas[i % len(cores_personalizadas)],  # Escolhe a cor da lista
    #         #  s=100  # Define o tamanho dos marcadores
    #         s=cluster_data['Empregabilidade'] * 20,  # Define o tamanho dos pontos com base na empregabilidade (ajuste o fator de multiplicação conforme necessário)
    #      )   

    # Personalizar o gráfico
    # plt.figure(figsize=(100, 80))  # Aumentar o tamanho do gráfico
    plt.legend(title="Cursos", loc='lower right', prop={'size': 7})  # Reduzir o tamanho da legenda
    # plt.legend(markerscale=1)
    # plt.title('Empregabilidade ')
    plt.xlabel('Cursos')
    plt.ylabel('Profissões')
    plt.ylim(0, 100) # definir limite do eixo
    plt.xlim(0, 100) # definir limite do eixo
    # plt.legend(title="Cursos", loc='lower right')
    # plt.legend(title="Cursos", loc='lower right', prop={'size': 10})
    plt.grid()

    # Mostrar o gráfico
    # plt.show()
    # string1 = "Cursos e Profissões que mudam de Clusters" +".png"
    # string1 = "Empregabilidade: cursos e profissões que tem profissionais atuando em mais de uma profissão" +".png"
    string1 = "Empregabilidade_cursos_profissões_profissionais_atuando_mais_profissão" +".png"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string1)  
    return

def median_salario(path1,name1,sx):
    # if sx == 'O':
    #     ##### -------------------------------- Usar um arquivo de teste para empregabilidade
    #     # Carregar o arquivo CSV
    #     file_path = "graficos/Kmeans3_T.csv"  # Substitua pelo caminho do arquivo
    #     Kmeans3_T = pd.read_csv(file_path)
    #     save_results_to = 'graficos/' 
        
    #     #Kmeans3_T = Kmeans3_T.drop(columns=['Unnamed: 0'])

    #     Final = pd.read_csv("processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv", sep=",")
    #     Final = Final.drop(columns=['Unnamed: 0'])
    #     #print(Final.head(3))
    #     # #Remove Zeros
    #     FinalSemZero = Final.loc[((Final['Valor_rend_bruto_M']!= 0))]
    #     FinalSemZero = Final.loc[((Final['Qtdade_Salario']> 0.0))]

    #     FinalSemZero = FinalSemZero.reset_index(drop=True)
    #     print(FinalSemZero.shape)
    #     # print(FinalSemZero.head(3))

    #     # # Filtra Zeros
    #     FinalZero = Final[(Final['Valor_rend_bruto_M'] == 0)]
    #     FinalZero.shape
    #     FinalZero = Final[(Final['Qtdade_Salario'] == 0)]
    #     # print(FinalZero.shape)

    #     # Adicionando os campos Min e Max
    #     resultados_T=[]
    #     minvalue =""
    #     maxvalue =""
    #     medianavalue = ""
    #     for i in range(len(Kmeans3_T['Curso'])):
    #         tupla=(Kmeans3_T['Ida'][i],Kmeans3_T['Volta'][i],Kmeans3_T['Cluster'][i], Kmeans3_T['Curso'][i],Kmeans3_T['Curso_Nome'][i],Kmeans3_T['Cbo'][i],Kmeans3_T['Cbo_Nome'][i],minvalue,maxvalue,medianavalue)
    #         resultados_T.append(tupla)
    #     #...
    #     Kmeans3_Sal= pd.DataFrame(resultados_T)
    #     #...
    #     dict = {
    #             0:"Ida",
    #             1:"Volta",
    #             2:"Cluster",
    #             3:"Curso",
    #             4:"Curso_Nome",
    #             5:"Cbo",
    #             6:"Cbo_Nome",
    #             7:"Max",
    #             8:"Min",
    #             9:"Median"
    #     }
    #     Kmeans3_Sal.rename(columns=dict,inplace=True)

    #     # print(len(Kmeans3_Sal))
    #     #================================================================================================================================================
        
    #     # Achando Max e Min 
    #     for j in range(len(Kmeans3_T)):
    #         gênero                                  = []
    #         Idade_em_Anos                           = []
    #         Nível_instrução                         = []
    #         Curso_Superior_Graduação_Código	        = []
    #         Curso_Mestrado_Código                   = []
    #         Curso_Doutorado_Código                  = []
    #         Ocupação_Código                         = []
    #         Atividade_Código                        = []
    #         Valor_rend_bruto_M                      = []
    #         Qtdade_Salario                          = []
    #         #CNAE_Domiciliar                        = []
    #         #Sal_Novo                               = []
    #         QtdadeTemp                              = []
    #         for i in range(len(FinalSemZero)):
    #             # print('str(FinalSemZero.Ocupação_Código[i]):', str(FinalSemZero.Ocupação_Código[i]))
    #             # print('str(Kmeans3_T.Cbo[j]):', str(int(Kmeans3_T.Cbo[j])))
    #             # print('str(FinalSemZero.Curso_Superior_Graduação_Código[i]):', str(FinalSemZero.Curso_Superior_Graduação_Código[i]))
    #             # print(' str(Kmeans3_T.Curso[j])', str(int(Kmeans3_T.Curso[j])))
    #             # print('----')
    #             # from time import sleep
    #             # sleep(1)
    #             if (str(FinalSemZero.Ocupação_Código[i])== str(int(Kmeans3_T.Cbo[j]))) & (str(FinalSemZero.Curso_Superior_Graduação_Código[i]) == str(int(Kmeans3_T.Curso[j]))):
    #                 gênero.append(FinalSemZero.gênero[i])
    #                 Idade_em_Anos.append(FinalSemZero.Idade_em_Anos[i])
    #                 Nível_instrução.append(FinalSemZero.Nível_instrução[i])
    #                 Curso_Superior_Graduação_Código.append(FinalSemZero.Curso_Superior_Graduação_Código[i])
    #                 Curso_Mestrado_Código. append(FinalSemZero.Curso_Mestrado_Código[i])
    #                 Curso_Doutorado_Código.append(FinalSemZero.Curso_Doutorado_Código[i])
    #                 Ocupação_Código.append(FinalSemZero.Ocupação_Código[i])
    #                 Atividade_Código.append(FinalSemZero.Atividade_Código[i])
    #                 Valor_rend_bruto_M.append(FinalSemZero.Valor_rend_bruto_M[i])
    #                 Qtdade_Salario.append(FinalSemZero.Qtdade_Salario[i]/100)
    #                 #QtdadeTemp = FinalSemZero.Qtdade_Salario[i]/100
    #                 #if(QtdadeTemp >=1):
    #                 #   Qtdade_Salario.append(QtdadeTemp)
    #                 #CNAE_Domiciliar.append(Final.CNAE-Domiciliar[i])
    #                 #Sal_Novo.append(FinalSemZero.Valor_rend_bruto_M[i]/FinalSemZero.Qtdade_Salario[i])
    #         #============================================================================================================================================================
    #         Final_Filter=[]
    #         for i in range(len(Curso_Superior_Graduação_Código)):
    #             #tupla=(gênero[i],Idade_em_Anos[i],Nível_instrução[i],Curso_Superior_Graduação_Código[i],Curso_Mestrado_Código[i],Curso_Doutorado_Código[i],Ocupação_Código[i],Atividade_Código[i],Valor_rend_bruto_M[i],Qtdade_Salario[i],CNAE_Domiciliar[i])
    #             #tupla=(gênero[i],Idade_em_Anos[i],Nível_instrução[i],Curso_Superior_Graduação_Código[i],Curso_Mestrado_Código[i],Curso_Doutorado_Código[i],Ocupação_Código[i],Atividade_Código[i],Valor_rend_bruto_M[i],Qtdade_Salario[i],Sal_Novo[i])
    #             tupla=(gênero[i],Idade_em_Anos[i],Nível_instrução[i],Curso_Superior_Graduação_Código[i],Curso_Mestrado_Código[i],Curso_Doutorado_Código[i],Ocupação_Código[i],Atividade_Código[i],Valor_rend_bruto_M[i],Qtdade_Salario[i])
    #             Final_Filter.append(tupla)
    #         #print(len(Final_Filter))      
    #         #===============================================================================================================================================
    #         Final2 = pd.DataFrame(Final_Filter)
    #         # Final2.shape
    #         # print(Final2)
    #         dict = {
    #         0:"gênero",
    #         1:"Idade_em_Anos",
    #         2:"Nível_instrução",
    #         3:"Curso_Superior_Graduação_Código",
    #         4:"Curso_Mestrado_Código",
    #         5:"Curso_Doutorado_Código",
    #         6:"Ocupação_Código",
    #         7:"Atividade_Código",
    #         8:"Valor_rend_bruto_M",
    #         9:"Qtdade_Salario"
    #         #10:"Sal_Novo"
    #         }
    #         Final2.rename(columns=dict,inplace=True)
    #         #===============================================================================================================================================
    #         # Final2.head(2)
    #         #===============================================================================================================================================
    #         for i in range(len(Kmeans3_Sal)):
    #             if (str(Kmeans3_Sal.Cbo[i])== str(Kmeans3_T.Cbo[j])) & (str(Kmeans3_Sal.Curso[i]) == str(Kmeans3_T.Curso[j])):
    #                 #Kmeans5_Sal.Max[i] = Final2['Valor_rend_bruto_M'].max()
    #                 #Kmeans5_Sal.Min[i] = Final2['Valor_rend_bruto_M'].min()
    #                 #Kmeans5_Sal.Max[i] = round(Final2['Sal_Novo'].max(),0)
    #                 #Kmeans5_Sal.Min[i] = round(Final2['Sal_Novo'].min(),0)
    #                 Kmeans3_Sal.Max[i] = round(Final2['Qtdade_Salario'].max())
    #                 Kmeans3_Sal.Min[i] = Final2['Qtdade_Salario'].min()
    #                 Kmeans3_Sal.Median[i] = Final2['Qtdade_Salario'].median()
    #                 break
        
    #     Kmeans3_Sal2 = Kmeans3_Sal.sort_values(["Cluster","Median"], ascending=[True, True])
    #     Kmeans3_Sal2.to_csv(save_results_to +'Kmeans3_T_Salarios_certo.csv')   
    #     print(Kmeans3_Sal2.head(3))   

    if sx == 'F':
        ##### -------------------------------- Usar um arquivo de teste para empregabilidade
        # Carregar o arquivo CSV
        file_path_Kmeans3_T = "graficos/Kmeans3_T.csv"  # Substitua pelo caminho do arquivo
        file_path = "graficos/Resultados_T_Fem_Masc_Kmeans3_Genero.csv"  # Substitua pelo caminho do arquivo
        
        Kmeans3_T_O = pd.read_csv(file_path_Kmeans3_T)
        Kmeans3_T = pd.read_csv(file_path)
        save_results_to = 'graficos/' 

        # Filtra Cbo e Curso Iguais       
        filtered_records = Kmeans3_T[
                (Kmeans3_T['Curso'].isin(Kmeans3_T_O['Curso'])) &
                (Kmeans3_T['Cbo'].isin(Kmeans3_T_O['Cbo'])) &
                (Kmeans3_T['Genero'].isin(['F', 'M', 'O']))
            ]
        filtered_records.to_csv(save_results_to + 'filtered_records.csv')     
        # Filtra somente os que tem Genero O, F e M 
        filtered_records_filtered = filtered_records.groupby(['Curso', 'Cbo']).filter(lambda x: set(x['Genero']) == {'O', 'F', 'M'})
        filtered_records_filtered.to_csv('graficos/filtered_records_filtered.csv', index=False)

        file_path = "graficos/filtered_records_filtered.csv"  # Substitua pelo caminho do arquivo
        Kmeans3_T = pd.read_csv(file_path)
        #Kmeans3_T = Kmeans3_T.drop(columns=['Unnamed: 0'])

        Final = pd.read_csv("processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_Fem.csv", sep=",")
        Final = Final.drop(columns=['Unnamed: 0'])
        #print(Final.head(3))
        # #Remove Zeros
        FinalSemZero = Final.loc[((Final['Valor_rend_bruto_M']!= 0))]
        FinalSemZero = Final.loc[((Final['Qtdade_Salario']> 0.0))]

        FinalSemZero = FinalSemZero.reset_index(drop=True)
        # print(FinalSemZero.shape)
        # print(FinalSemZero.head(3))

        # # Filtra Zeros
        FinalZero = Final[(Final['Valor_rend_bruto_M'] == 0)]
        # FinalZero.shape
        FinalZero = Final[(Final['Qtdade_Salario'] == 0)]
        # print(FinalZero.shape)

        # Adicionando os campos Min e Max
        resultados_T=[]
        minvalue =""
        maxvalue =""
        medianavalue = ""
        logging.info("Separando os Femininos ...") 
        for i in range(len(Kmeans3_T['Curso'])):
            if Kmeans3_T['Genero'][i] == "F":
               tupla=(Kmeans3_T['Ida'][i],Kmeans3_T['Volta'][i],Kmeans3_T['Cluster'][i], Kmeans3_T['Curso'][i],Kmeans3_T['Curso_Nome'][i],Kmeans3_T['Cbo'][i],Kmeans3_T['Cbo_Nome'][i],minvalue,maxvalue,medianavalue)
               resultados_T.append(tupla)
        #...
        Kmeans3_Sal= pd.DataFrame(resultados_T)
        #...
        dict = {
                0:"Ida",
                1:"Volta",
                2:"Cluster",
                3:"Curso",
                4:"Curso_Nome",
                5:"Cbo",
                6:"Cbo_Nome",
                7:"Max",
                8:"Min",
                9:"Median"
        }
        Kmeans3_Sal.rename(columns=dict,inplace=True)

        # print("len(Kmeans3_Sal)", len(Kmeans3_Sal))
        # # print("")
        # print(Kmeans3_Sal.head(10))
        #================================================================================================================================================
        
        # Achando Max e Min 
        logging.info("Achando Max e Min ...") 
        for j in range(len(Kmeans3_T)):
        # for j in range(3):
            gênero                                  = []
            Idade_em_Anos                           = []
            Nível_instrução                         = []
            Curso_Superior_Graduação_Código	        = []
            Curso_Mestrado_Código                   = []
            Curso_Doutorado_Código                  = []
            Ocupação_Código                         = []
            Atividade_Código                        = []
            Valor_rend_bruto_M                      = []
            Qtdade_Salario                          = []
            #CNAE_Domiciliar                        = []
            #Sal_Novo                               = []
            QtdadeTemp                              = []
            for i in range(len(FinalSemZero)):
            # for i in range(10):
                # print('str(FinalSemZero.Ocupação_Código[i]):', str(FinalSemZero.Ocupação_Código[i]))
                # print('str(Kmeans3_T.Cbo[j]):', str(int(Kmeans3_T.Cbo[j])))
                # print('str(FinalSemZero.Curso_Superior_Graduação_Código[i]):', str(FinalSemZero.Curso_Superior_Graduação_Código[i]))
                # print(' str(Kmeans3_T.Curso[j])', str(int(Kmeans3_T.Curso[j])))
                # print('----')
                # from time import sleep
                # sleep(1)
                if (str(FinalSemZero.Ocupação_Código[i])== str(int(Kmeans3_T.Cbo[j]))) & (str(FinalSemZero.Curso_Superior_Graduação_Código[i]) == str(int(Kmeans3_T.Curso[j]))):
                    gênero.append(FinalSemZero.gênero[i])
                    Idade_em_Anos.append(FinalSemZero.Idade_em_Anos[i])
                    Nível_instrução.append(FinalSemZero.Nível_instrução[i])
                    Curso_Superior_Graduação_Código.append(FinalSemZero.Curso_Superior_Graduação_Código[i])
                    Curso_Mestrado_Código. append(FinalSemZero.Curso_Mestrado_Código[i])
                    Curso_Doutorado_Código.append(FinalSemZero.Curso_Doutorado_Código[i])
                    Ocupação_Código.append(FinalSemZero.Ocupação_Código[i])
                    Atividade_Código.append(FinalSemZero.Atividade_Código[i])
                    Valor_rend_bruto_M.append(FinalSemZero.Valor_rend_bruto_M[i])
                    Qtdade_Salario.append(FinalSemZero.Qtdade_Salario[i]/100)
                    #QtdadeTemp = FinalSemZero.Qtdade_Salario[i]/100
                    #if(QtdadeTemp >=1):
                    #   Qtdade_Salario.append(QtdadeTemp)
                    #CNAE_Domiciliar.append(Final.CNAE-Domiciliar[i])
                    #Sal_Novo.append(FinalSemZero.Valor_rend_bruto_M[i]/FinalSemZero.Qtdade_Salario[i])
            #============================================================================================================================================================
            Final_Filter=[]
            for i in range(len(Curso_Superior_Graduação_Código)):
            # for i in range(10):
                #tupla=(gênero[i],Idade_em_Anos[i],Nível_instrução[i],Curso_Superior_Graduação_Código[i],Curso_Mestrado_Código[i],Curso_Doutorado_Código[i],Ocupação_Código[i],Atividade_Código[i],Valor_rend_bruto_M[i],Qtdade_Salario[i],CNAE_Domiciliar[i])
                #tupla=(gênero[i],Idade_em_Anos[i],Nível_instrução[i],Curso_Superior_Graduação_Código[i],Curso_Mestrado_Código[i],Curso_Doutorado_Código[i],Ocupação_Código[i],Atividade_Código[i],Valor_rend_bruto_M[i],Qtdade_Salario[i],Sal_Novo[i])
                tupla=(gênero[i],Idade_em_Anos[i],Nível_instrução[i],Curso_Superior_Graduação_Código[i],Curso_Mestrado_Código[i],Curso_Doutorado_Código[i],Ocupação_Código[i],Atividade_Código[i],Valor_rend_bruto_M[i],Qtdade_Salario[i])
                Final_Filter.append(tupla)
            # print("len(Final_Filter)",len(Final_Filter))   
            # print("")   
            #===============================================================================================================================================
            Final2 = pd.DataFrame(Final_Filter)
            # Final2.shape
            # print(Final2)
            dict = {
            0:"gênero",
            1:"Idade_em_Anos",
            2:"Nível_instrução",
            3:"Curso_Superior_Graduação_Código",
            4:"Curso_Mestrado_Código",
            5:"Curso_Doutorado_Código",
            6:"Ocupação_Código",
            7:"Atividade_Código",
            8:"Valor_rend_bruto_M",
            9:"Qtdade_Salario"
            #10:"Sal_Novo"
            }
            Final2.rename(columns=dict,inplace=True)
            #===============================================================================================================================================
            # print(Final2.head(50))
            # print("")
            #===============================================================================================================================================
            for i in range(len(Kmeans3_Sal)):
            # for i in range(10):
                if (str(Kmeans3_Sal.Cbo[i])== str(Kmeans3_T.Cbo[j])) & (str(Kmeans3_Sal.Curso[i]) == str(Kmeans3_T.Curso[j])):
                    #Kmeans5_Sal.Max[i] = Final2['Valor_rend_bruto_M'].max()
                    #Kmeans5_Sal.Min[i] = Final2['Valor_rend_bruto_M'].min()
                    #Kmeans5_Sal.Max[i] = round(Final2['Sal_Novo'].max(),0)
                    #Kmeans5_Sal.Min[i] = round(Final2['Sal_Novo'].min(),0)
                    Kmeans3_Sal.Max[i] = round(Final2['Qtdade_Salario'].max())
                    Kmeans3_Sal.Min[i] = Final2['Qtdade_Salario'].min()
                    Kmeans3_Sal.Median[i] = Final2['Qtdade_Salario'].median()
                    break
        
        Kmeans3_Sal2 = Kmeans3_Sal.sort_values(["Cluster","Median"], ascending=[True, True])
        Kmeans3_Sal2.to_csv(save_results_to +'Kmeans3_T_Salarios_certo_F.csv')   
        # print(Kmeans3_Sal2.head(3))    

    
    if sx == 'M':
        # ##### -------------------------------- Usar um arquivo de teste para empregabilidade
        # # Carregar o arquivo CSV
        # # file_path = "graficos/Kmeans3_T.csv"  # Substitua pelo caminho do arquivo
        # file_path = "graficos/Resultados_T_Fem_Masc_Kmeans3_Genero.csv"  # Substitua pelo caminho do arquivo   
        # Kmeans3_T = pd.read_csv(file_path)
        # save_results_to = 'graficos/' 
        
        # #Kmeans3_T = Kmeans3_T.drop(columns=['Unnamed: 0'])

        ##### -------------------------------- Usar um arquivo de teste para empregabilidade
        # Carregar o arquivo CSV
        file_path_Kmeans3_T = "graficos/Kmeans3_T.csv"  # Substitua pelo caminho do arquivo
        file_path = "graficos/Resultados_T_Fem_Masc_Kmeans3_Genero.csv"  # Substitua pelo caminho do arquivo
        
        Kmeans3_T_O = pd.read_csv(file_path_Kmeans3_T)
        Kmeans3_T = pd.read_csv(file_path)
        save_results_to = 'graficos/' 

        # Filtra Cbo e Curso Iguais       
        filtered_records = Kmeans3_T[
                (Kmeans3_T['Curso'].isin(Kmeans3_T_O['Curso'])) &
                (Kmeans3_T['Cbo'].isin(Kmeans3_T_O['Cbo'])) &
                (Kmeans3_T['Genero'].isin(['F', 'M', 'O']))
            ]
        filtered_records.to_csv(save_results_to + 'filtered_records.csv')     
        # Filtra somente os que tem Genero O, F e M 
        filtered_records_filtered = filtered_records.groupby(['Curso', 'Cbo']).filter(lambda x: set(x['Genero']) == {'O', 'F', 'M'})
        filtered_records_filtered.to_csv('graficos/filtered_records_filtered.csv', index=False)

        file_path = "graficos/filtered_records_filtered.csv"  # Substitua pelo caminho do arquivo
        Kmeans3_T = pd.read_csv(file_path)
        #Kmeans3_T = Kmeans3_T.drop(columns=['Unnamed: 0'])

        Final = pd.read_csv("processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_Masc.csv", sep=",")
        Final = Final.drop(columns=['Unnamed: 0'])
        #print(Final.head(3))
        # #Remove Zeros
        FinalSemZero = Final.loc[((Final['Valor_rend_bruto_M']!= 0))]
        FinalSemZero = Final.loc[((Final['Qtdade_Salario']> 0.0))]

        FinalSemZero = FinalSemZero.reset_index(drop=True)
        print(FinalSemZero.shape)
        # print(FinalSemZero.head(3))

        # # Filtra Zeros
        FinalZero = Final[(Final['Valor_rend_bruto_M'] == 0)]
        FinalZero.shape
        FinalZero = Final[(Final['Qtdade_Salario'] == 0)]
        # print(FinalZero.shape)

        # Adicionando os campos Min e Max
        resultados_T=[]
        minvalue =""
        maxvalue =""
        medianavalue = ""
        for i in range(len(Kmeans3_T['Curso'])):
              if Kmeans3_T['Genero'][i] == "M":
                 tupla=(Kmeans3_T['Ida'][i],Kmeans3_T['Volta'][i],Kmeans3_T['Cluster'][i], Kmeans3_T['Curso'][i],Kmeans3_T['Curso_Nome'][i],Kmeans3_T['Cbo'][i],Kmeans3_T['Cbo_Nome'][i],minvalue,maxvalue,medianavalue)
                 resultados_T.append(tupla)
    #     #...
        Kmeans3_Sal= pd.DataFrame(resultados_T)
        #...
        dict = {
                0:"Ida",
                1:"Volta",
                2:"Cluster",
                3:"Curso",
                4:"Curso_Nome",
                5:"Cbo",
                6:"Cbo_Nome",
                7:"Max",
                8:"Min",
                9:"Median"
        }
        Kmeans3_Sal.rename(columns=dict,inplace=True)

        # print(len(Kmeans3_Sal))
        #================================================================================================================================================
        
        # Achando Max e Min 
        for j in range(len(Kmeans3_T)):
            gênero                                  = []
            Idade_em_Anos                           = []
            Nível_instrução                         = []
            Curso_Superior_Graduação_Código	        = []
            Curso_Mestrado_Código                   = []
            Curso_Doutorado_Código                  = []
            Ocupação_Código                         = []
            Atividade_Código                        = []
            Valor_rend_bruto_M                      = []
            Qtdade_Salario                          = []
            #CNAE_Domiciliar                        = []
            #Sal_Novo                               = []
            QtdadeTemp                              = []
            for i in range(len(FinalSemZero)):
                # print('str(FinalSemZero.Ocupação_Código[i]):', str(FinalSemZero.Ocupação_Código[i]))
                # print('str(Kmeans3_T.Cbo[j]):', str(int(Kmeans3_T.Cbo[j])))
                # print('str(FinalSemZero.Curso_Superior_Graduação_Código[i]):', str(FinalSemZero.Curso_Superior_Graduação_Código[i]))
                # print(' str(Kmeans3_T.Curso[j])', str(int(Kmeans3_T.Curso[j])))
                # print('----')
                # from time import sleep
                # sleep(1)
                if (str(FinalSemZero.Ocupação_Código[i])== str(int(Kmeans3_T.Cbo[j]))) & (str(FinalSemZero.Curso_Superior_Graduação_Código[i]) == str(int(Kmeans3_T.Curso[j]))):
                    gênero.append(FinalSemZero.gênero[i])
                    Idade_em_Anos.append(FinalSemZero.Idade_em_Anos[i])
                    Nível_instrução.append(FinalSemZero.Nível_instrução[i])
                    Curso_Superior_Graduação_Código.append(FinalSemZero.Curso_Superior_Graduação_Código[i])
                    Curso_Mestrado_Código. append(FinalSemZero.Curso_Mestrado_Código[i])
                    Curso_Doutorado_Código.append(FinalSemZero.Curso_Doutorado_Código[i])
                    Ocupação_Código.append(FinalSemZero.Ocupação_Código[i])
                    Atividade_Código.append(FinalSemZero.Atividade_Código[i])
                    Valor_rend_bruto_M.append(FinalSemZero.Valor_rend_bruto_M[i])
                    Qtdade_Salario.append(FinalSemZero.Qtdade_Salario[i]/100)
                    #QtdadeTemp = FinalSemZero.Qtdade_Salario[i]/100
                    #if(QtdadeTemp >=1):
                    #   Qtdade_Salario.append(QtdadeTemp)
                    #CNAE_Domiciliar.append(Final.CNAE-Domiciliar[i])
                    #Sal_Novo.append(FinalSemZero.Valor_rend_bruto_M[i]/FinalSemZero.Qtdade_Salario[i])
            #============================================================================================================================================================
            Final_Filter=[]
            for i in range(len(Curso_Superior_Graduação_Código)):
                #tupla=(gênero[i],Idade_em_Anos[i],Nível_instrução[i],Curso_Superior_Graduação_Código[i],Curso_Mestrado_Código[i],Curso_Doutorado_Código[i],Ocupação_Código[i],Atividade_Código[i],Valor_rend_bruto_M[i],Qtdade_Salario[i],CNAE_Domiciliar[i])
                #tupla=(gênero[i],Idade_em_Anos[i],Nível_instrução[i],Curso_Superior_Graduação_Código[i],Curso_Mestrado_Código[i],Curso_Doutorado_Código[i],Ocupação_Código[i],Atividade_Código[i],Valor_rend_bruto_M[i],Qtdade_Salario[i],Sal_Novo[i])
                tupla=(gênero[i],Idade_em_Anos[i],Nível_instrução[i],Curso_Superior_Graduação_Código[i],Curso_Mestrado_Código[i],Curso_Doutorado_Código[i],Ocupação_Código[i],Atividade_Código[i],Valor_rend_bruto_M[i],Qtdade_Salario[i])
                Final_Filter.append(tupla)
            #print(len(Final_Filter))      
            #===============================================================================================================================================
            Final2 = pd.DataFrame(Final_Filter)
            # Final2.shape
            # print(Final2)
            dict = {
            0:"gênero",
            1:"Idade_em_Anos",
            2:"Nível_instrução",
            3:"Curso_Superior_Graduação_Código",
            4:"Curso_Mestrado_Código",
            5:"Curso_Doutorado_Código",
            6:"Ocupação_Código",
            7:"Atividade_Código",
            8:"Valor_rend_bruto_M",
            9:"Qtdade_Salario"
            #10:"Sal_Novo"
            }
            Final2.rename(columns=dict,inplace=True)
            #===============================================================================================================================================
            # Final2.head(2)
            #===============================================================================================================================================
            for i in range(len(Kmeans3_Sal)):
                if (str(Kmeans3_Sal.Cbo[i])== str(Kmeans3_T.Cbo[j])) & (str(Kmeans3_Sal.Curso[i]) == str(Kmeans3_T.Curso[j])):
                    #Kmeans5_Sal.Max[i] = Final2['Valor_rend_bruto_M'].max()
                    #Kmeans5_Sal.Min[i] = Final2['Valor_rend_bruto_M'].min()
                    #Kmeans5_Sal.Max[i] = round(Final2['Sal_Novo'].max(),0)
                    #Kmeans5_Sal.Min[i] = round(Final2['Sal_Novo'].min(),0)
                    Kmeans3_Sal.Max[i] = round(Final2['Qtdade_Salario'].max())
                    Kmeans3_Sal.Min[i] = Final2['Qtdade_Salario'].min()
                    Kmeans3_Sal.Median[i] = Final2['Qtdade_Salario'].median()
                    break
        
        Kmeans3_Sal2 = Kmeans3_Sal.sort_values(["Cluster","Median"], ascending=[True, True])
        Kmeans3_Sal2.to_csv(save_results_to +'Kmeans3_T_Salarios_certo_M.csv')   
        # print(Kmeans3_Sal2.head(3))           
        
    return

def separar_cursos_por_clusters():
        # Ler o arquivo CSV
        file_path = "graficos/Kmeans3_T_Salarios_certo.csv"
        data = pd.read_csv(file_path)
        
        # Obter os clusters únicos
        clusters_unicos = data['Cluster'].unique()
        
        # Salvar um arquivo para cada cluster
        for cluster in clusters_unicos:
            cluster_data = data[data['Cluster'] == cluster]
            cluster_file_path = f"graficos/Kmeans3_T_Salarios_cluster_{cluster}.csv"
            cluster_data.to_csv(cluster_file_path, index=False)
        
        return  
  
def medianas_por_clusters():
            clusters = [0.0, 1.0, 2.0]
            for cluster in clusters:
                file_path = f"graficos/Kmeans3_T_Salarios_cluster_{cluster}.csv"
                data = pd.read_csv(file_path)
                median_of_medians = data['Median'].median()
                print(f"Cluster {cluster}: Mediana das medianas = {median_of_medians}")        
            return
          
def Salarios(path1,name1,path2,name2):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    import pandas as pd
    import numpy as np
    from sklearn.cluster import KMeans
    import pandas as pd

    ##### ---------------------------------- Gerar o arquivo de empregabilidade
    # # Carregar o arquivo CSV
    # file_path = "graficos/Kmeans3_T.csv"  # Substitua pelo caminho do arquivo
    # data = pd.read_csv(file_path)
    # save_results_to = 'graficos/' 
    
    # # Filtrar as linhas com CR: 214, 342, 520, 721, 726
    # cr_values = [214, 342, 520, 721, 726]
    # filtered_data = data[data['Curso'].isin(cr_values)]
       
    # # Salvar o novo arquivo
    # filtered_file_path = save_results_to + 'Kmeans3_T.csv_Empregabilidade.csv'
    # filtered_data.to_csv(filtered_file_path, index=False)
    
    ##### -------------------------------- Usar um arquivo de teste para empregabilidade
    # Carregar o arquivo CSV
    # file_path = "graficos/Kmeans3_T_Empregabilidade.csv"  # Substitua pelo caminho do arquivo
    file_path = "graficos/Kmeans3_T_Salarios_certo.csv"  # Substitua pelo caminho do arquivo
    data = pd.read_csv(file_path)
    save_results_to = 'graficos/' 
    
    # Filtrar as linhas com CR: 214, 342, 520, 721, 726
    cr_values = [214, 342, 520, 721, 726]
    filtered_data = data[data['Curso'].isin(cr_values)]

    ##### -------------------------------- Gráfico separado por cursos 
    # Configurar o gráfico de dispersão usando as colunas 'Ida', 'Volta' e 'Cluster'
    plt.figure(figsize=(6, 4))    

    # # Lista de cores para os clusters
    cores_personalizadas = ['red', 'blue', 'green', 'black', 'pink']  # Adicione mais cores, se necessário

    # # Ordenar os clusters antes de criar o gráfico
    clusters_ordenados = sorted(filtered_data['Curso'].unique())


    # # Criar o scatter plot para os clusters com cores personalizadas
    for i, cluster in enumerate(clusters_ordenados):
          cluster_data = filtered_data[data['Curso'] == cluster]
          plt.scatter(
              cluster_data['Ida'], 
              cluster_data['Volta'], 
              label=f'Curso {int(cluster)}', 
              marker='.',  # Define o marcador como estrela
              color=cores_personalizadas[i % len(cores_personalizadas)],  # Escolhe a cor da lista
             #  s=100  # Define o tamanho dos marcadores
             #  s=cluster_data['Empregabilidade'] * 20,  # Define o tamanho dos pontos com base na empregabilidade (ajuste o fator de multiplicação conforme necessário)
              s=cluster_data['Median'] * 20,  # Define o tamanho dos pontos com base na empregabilidade (ajuste o fator de multiplicação conforme necessário)

          )     

    # ##### -------------------------------- Gráfico separado por Clusters
    # # Configurar o gráfico de dispersão usando as colunas 'Ida', 'Volta' e 'Cluster'
    # plt.figure(figsize=(6, 4))    

    # # Lista de cores para os clusters
    # cores_personalizadas = ['red', 'blue', 'green', 'black', 'pink']  # Adicione mais cores, se necessário

    # # Ordenar os clusters antes de criar o gráfico
    # clusters_ordenados = sorted(filtered_data['Cluster'].unique())


    # # Criar o scatter plot para os clusters com cores personalizadas
    # for i, cluster in enumerate(clusters_ordenados):
    #      cluster_data = filtered_data[data['Cluster'] == cluster]
    #      plt.scatter(
    #          cluster_data['Ida'], 
    #          cluster_data['Volta'], 
    #          label=f'Cluster {int(cluster)}', 
    #          marker='.',  # Define o marcador como estrela
    #          color=cores_personalizadas[i % len(cores_personalizadas)],  # Escolhe a cor da lista
    #         #  s=100  # Define o tamanho dos marcadores
    #         s=cluster_data['Empregabilidade'] * 20,  # Define o tamanho dos pontos com base na empregabilidade (ajuste o fator de multiplicação conforme necessário)
    #      )   

    # Personalizar o gráfico
    # plt.title('Salarios')
    plt.xlabel('Cursos')
    plt.ylabel('Profissões')
    plt.ylim(0, 100) # definir limite do eixo
    plt.xlim(0, 100) # definir limite do eixo
    plt.legend(title="Cursos", loc='lower right')
    plt.grid()

    # Mostrar o gráfico
    # plt.show()
    # string1 = "Cursos e Profissões que mudam de Clusters" +".png"
    string1 = "Salários: Cursos e Profissões que mudam de Clusters" +".png"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string1)  

    return

def  Salarios_cursos_commaisprofissoes(path1,name1,path2,name2):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    import pandas as pd
    import numpy as np
    from sklearn.cluster import KMeans
    import pandas as pd

    ##### ---------------------------------- Gerar o arquivo de empregabilidade
    # # Carregar o arquivo CSV
    # file_path = "graficos/Kmeans3_T.csv"  # Substitua pelo caminho do arquivo
    # data = pd.read_csv(file_path)
    # save_results_to = 'graficos/' 
    
    # # Filtrar as linhas com CR: 214, 342, 520, 721, 726
    # cr_values = [214, 342, 520, 721, 726]
    # filtered_data = data[data['Curso'].isin(cr_values)]
       
    # # Salvar o novo arquivo
    # filtered_file_path = save_results_to + 'Kmeans3_T.csv_Empregabilidade.csv'
    # filtered_data.to_csv(filtered_file_path, index=False)
    
    ##### -------------------------------- Usar um arquivo de teste para empregabilidade
    # Carregar o arquivo CSV
    # file_path = "graficos/Kmeans3_T_Empregabilidade.csv"  # Substitua pelo caminho do arquivo
    file_path = "graficos/Kmeans3_T_Salarios_certo.csv"  # Substitua pelo caminho do arquivo
    data = pd.read_csv(file_path)
    save_results_to = 'graficos/' 
    
    # Filtrar as linhas com CR: 214, 342, 520, 721, 726
    # cr_values = [214, 342, 520, 721, 726]
    # cr_values = [142, 145, 211, 212, 214, 223, 342, 520, 721, 726]
    cr_values = [142, 145, 211, 212, 223]
    filtered_data = data[data['Curso'].isin(cr_values)]

    ##### -------------------------------- Gráfico separado por cursos 
    # Configurar o gráfico de dispersão usando as colunas 'Ida', 'Volta' e 'Cluster'
    plt.figure(figsize=(6, 4))    

    # # Lista de cores para os clusters
    # cores_personalizadas = ['red', 'blue', 'green', 'black', 'pink']  # Adicione mais cores, se necessário
    # cores_personalizadas = ['DarkViolet', 'DarkMagenta', 'DeepPink', 'Crimson',
    #                        'red', 'Yellow','blue', 'brown', 'black', 'green']  # Adicione mais cores, se necessário
    cores_personalizadas = ['red','blue', 'brown', 'black', 'green']  # Adicione mais cores, se necessário
    # # Ordenar os clusters antes de criar o gráfico
    clusters_ordenados = sorted(filtered_data['Curso'].unique())


    # # Criar o scatter plot para os clusters com cores personalizadas
    for i, cluster in enumerate(clusters_ordenados):
          cluster_data = filtered_data[data['Curso'] == cluster]
          plt.scatter(
              cluster_data['Ida'], 
              cluster_data['Volta'], 
              label=f'Curso {int(cluster)}', 
              marker='.',  # Define o marcador como estrela
              color=cores_personalizadas[i % len(cores_personalizadas)],  # Escolhe a cor da lista
             #  s=100  # Define o tamanho dos marcadores
             #  s=cluster_data['Empregabilidade'] * 20,  # Define o tamanho dos pontos com base na empregabilidade (ajuste o fator de multiplicação conforme necessário)
              s=cluster_data['Median'] * 20,  # Define o tamanho dos pontos com base na empregabilidade (ajuste o fator de multiplicação conforme necessário)

          )     

    # ##### -------------------------------- Gráfico separado por Clusters
    # # Configurar o gráfico de dispersão usando as colunas 'Ida', 'Volta' e 'Cluster'
    # plt.figure(figsize=(6, 4))    

    # # Lista de cores para os clusters
    # cores_personalizadas = ['red', 'blue', 'green', 'black', 'pink']  # Adicione mais cores, se necessário

    # # Ordenar os clusters antes de criar o gráfico
    # clusters_ordenados = sorted(filtered_data['Cluster'].unique())


    # # Criar o scatter plot para os clusters com cores personalizadas
    # for i, cluster in enumerate(clusters_ordenados):
    #      cluster_data = filtered_data[data['Cluster'] == cluster]
    #      plt.scatter(
    #          cluster_data['Ida'], 
    #          cluster_data['Volta'], 
    #          label=f'Cluster {int(cluster)}', 
    #          marker='.',  # Define o marcador como estrela
    #          color=cores_personalizadas[i % len(cores_personalizadas)],  # Escolhe a cor da lista
    #         #  s=100  # Define o tamanho dos marcadores
    #         s=cluster_data['Empregabilidade'] * 20,  # Define o tamanho dos pontos com base na empregabilidade (ajuste o fator de multiplicação conforme necessário)
    #      )   

    # Personalizar o gráfico
    # plt.title('Salarios')
    plt.xlabel('Cursos')
    plt.ylabel('Profissões')
    plt.ylim(0, 100) # definir limite do eixo
    plt.xlim(0, 100) # definir limite do eixo
    plt.legend(title="Cursos", loc='lower right')
    plt.grid()

    # Mostrar o gráfico
    # plt.show()
    # string1 = "Cursos e Profissões que mudam de Clusters" +".png"
    # string1 = "Salários: cursos e profissões que tem profissionais atuando em mais de uma profissão" +".png"
    string1 = "Salários_cursos_profissões_profissionais_atuando_profissão" +".png"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string1)  

    return


def plot_selected_courses():
    # Read the Kmeans3_T.csv file
    file_path = "graficos/Kmeans3_T.csv"  # Replace with the actual file path
    Kmeans3_T = pd.read_csv(file_path)
    Kmeans3_T['Cluster'] = Kmeans3_T['Cluster'].astype(int)
    Kmeans3_T['Curso'] = Kmeans3_T['Curso'].astype(int)

        
    # Filter the data for the selected courses
    selected_courses = [214, 342, 520, 721, 726]
    selected_data = Kmeans3_T[Kmeans3_T['Curso'].isin(selected_courses)]

    # Plot the selected data
    clusters = selected_data['Cluster'].unique()
    colors = ['red', 'blue', 'green']
    for cluster in clusters:
        cluster_data = selected_data[selected_data['Cluster'] == cluster]
        color = colors[cluster]
        plt.scatter(cluster_data['Ida'], cluster_data['Volta'], label=f'Cluster {cluster}', marker='*', color=color)

    plt.xlabel('Cursos')
    plt.ylabel('Profissões')
    # plt.title('Selected Courses')
    plt.legend(loc='lower right')
    plt.ylim(0, 100) # definir limite do eixo
    plt.xlim(0, 100) # definir limite do eixo    
    plt.grid()
    # plt.savefig("graficos/selected_courses_plot.png")
    # plt.show()
    string1 = "selected_courses_plot" +".png"
    save_results_to = 'graficos/'  
    
    plt.savefig(save_results_to + string1)  
    return  



def plot_selected_courses_1(path1,name1,path2,name2):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    import pandas as pd
    import numpy as np
    from sklearn.cluster import KMeans
    import pandas as pd

    ##### ---------------------------------- Gerar o arquivo de empregabilidade
    # # Carregar o arquivo CSV
    # file_path = "graficos/Kmeans3_T.csv"  # Substitua pelo caminho do arquivo
    # data = pd.read_csv(file_path)
    # save_results_to = 'graficos/' 
    
    # # Filtrar as linhas com CR: 214, 342, 520, 721, 726
    # cr_values = [214, 342, 520, 721, 726]
    # filtered_data = data[data['Curso'].isin(cr_values)]
       
    # # Salvar o novo arquivo
    # filtered_file_path = save_results_to + 'Kmeans3_T.csv_Empregabilidade.csv'
    # filtered_data.to_csv(filtered_file_path, index=False)
    
    ##### -------------------------------- Usar um arquivo de teste para empregabilidade
    # Carregar o arquivo CSV
    # file_path = "graficos/Kmeans3_T_Empregabilidade.csv"  # Substitua pelo caminho do arquivo
    file_path = "graficos/Kmeans3_T_Salarios_certo.csv"  # Substitua pelo caminho do arquivo
    data = pd.read_csv(file_path)
    save_results_to = 'graficos/' 
    
    # Filtrar as linhas com CR: 214, 342, 520, 721, 726
    cr_values = [214, 342, 520, 721, 726]
    filtered_data = data[data['Curso'].isin(cr_values)]

    ##### -------------------------------- Gráfico separado por cursos 
    # Configurar o gráfico de dispersão usando as colunas 'Ida', 'Volta' e 'Cluster'
    plt.figure(figsize=(6, 4))    

    # # Lista de cores para os clusters
    cores_personalizadas = ['red', 'blue', 'green', 'black', 'pink']  # Adicione mais cores, se necessário

    # # Ordenar os clusters antes de criar o gráfico
    clusters_ordenados = sorted(filtered_data['Curso'].unique())


    # # Criar o scatter plot para os clusters com cores personalizadas
    for i, cluster in enumerate(clusters_ordenados):
          cluster_data = filtered_data[data['Curso'] == cluster]
          plt.scatter(
              cluster_data['Ida'], 
              cluster_data['Volta'], 
              label=f'Curso {int(cluster)}', 
              marker='*',  # Define o marcador como estrela
              color=cores_personalizadas[i % len(cores_personalizadas)],  # Escolhe a cor da lista
             #  s=100  # Define o tamanho dos marcadores
             #  s=cluster_data['Empregabilidade'] * 20,  # Define o tamanho dos pontos com base na empregabilidade (ajuste o fator de multiplicação conforme necessário)
             #  s=cluster_data['Median'] * 20,  # Define o tamanho dos pontos com base na empregabilidade (ajuste o fator de multiplicação conforme necessário)
              s=100 
          )     

    # ##### -------------------------------- Gráfico separado por Clusters
    # # Configurar o gráfico de dispersão usando as colunas 'Ida', 'Volta' e 'Cluster'
    # plt.figure(figsize=(6, 4))    

    # # Lista de cores para os clusters
    # cores_personalizadas = ['red', 'blue', 'green', 'black', 'pink']  # Adicione mais cores, se necessário

    # # Ordenar os clusters antes de criar o gráfico
    # clusters_ordenados = sorted(filtered_data['Cluster'].unique())


    # # Criar o scatter plot para os clusters com cores personalizadas
    # for i, cluster in enumerate(clusters_ordenados):
    #      cluster_data = filtered_data[data['Cluster'] == cluster]
    #      plt.scatter(
    #          cluster_data['Ida'], 
    #          cluster_data['Volta'], 
    #          label=f'Cluster {int(cluster)}', 
    #          marker='.',  # Define o marcador como estrela
    #          color=cores_personalizadas[i % len(cores_personalizadas)],  # Escolhe a cor da lista
    #         #  s=100  # Define o tamanho dos marcadores
    #         s=cluster_data['Empregabilidade'] * 20,  # Define o tamanho dos pontos com base na empregabilidade (ajuste o fator de multiplicação conforme necessário)
    #      )   

    # Personalizar o gráfico
    # plt.title('Salarios')
    plt.xlabel('Cursos')
    plt.ylabel('Profissões')
    plt.ylim(0, 100) # definir limite do eixo
    plt.xlim(0, 100) # definir limite do eixo
    plt.legend(title="Cursos", loc='lower right')
    plt.grid()

    # Mostrar o gráfico
    # plt.show()
    # string1 = "Cursos e Profissões que mudam de Clusters" +".png"
    string1 = "Cursos e Profissões que mudam de Clusters" +".png"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string1)  

    return

def correlacao_empregabilidade_salario():   
    
    # import pandas as pd
    # import matplotlib.pyplot as plt

    # # Dados de empregabilidade
    # empregabilidade_data = {
    #     "Curso": [214.0, 214.0, 342.0, 342.0, 520.0, 520.0, 721.0, 721.0, 726.0, 726.0],
    #     "Cbo": [2163.0, 2166.0, 2431.0, 1221.0, 2142.0, 2141.0, 2211.0, 2212.0, 2264.0, 2265.0],
    #     "Empregabilidade": [1367.65, 172.45, 278.1, 32.7, 4084.65, 181.3, 43.3, 79.7, 59.2, 23.8]
    # }

    # # Dados de salário
    # salario_data = {
    #     "Curso": [214.0, 214.0, 342.0, 342.0, 520.0, 520.0, 721.0, 721.0, 726.0, 726.0],
    #     "Cbo": [2163.0, 2166.0, 2431.0, 1221.0, 2141.0, 2142.0, 2211.0, 2212.0, 2264.0, 2265.0],
    #     "Salario_Mediano": [2.94, 3.14, 3.92, 6.86, 8.24, 9.8, 11.76, 12.16, 2.94, 2.94]
    # }

    # # Criando dataframes
    # df_empregabilidade = pd.DataFrame(empregabilidade_data)
    # df_salario = pd.DataFrame(salario_data)

    # # Mesclar os dataframes com base nos campos "Curso" e "Cbo"
    # df_merged = pd.merge(df_empregabilidade, df_salario, on=["Curso", "Cbo"])

    # # Criar gráfico de dispersão
    # plt.figure(figsize=(8, 6))
    # plt.scatter(df_merged["Empregabilidade"], df_merged["Salario_Mediano"], color="blue", alpha=0.6)
    # plt.xlabel("Empregabilidade")
    # plt.ylabel("Salário Mediano")
    # plt.title("Relação entre Empregabilidade e Salário Mediano")
    # plt.grid(True)
    # # Exibir gráfico
    # plt.show()
    
    ###########################################################################################################
    # import pandas as pd
    # import matplotlib.pyplot as plt

    # # Dados de empregabilidade
    # empregabilidade_data = {
    #     "Curso": [214.0, 214.0, 342.0, 342.0, 520.0, 520.0, 721.0, 721.0, 726.0, 726.0],
    #     "Cbo": [2163.0, 2166.0, 2431.0, 1221.0, 2142.0, 2141.0, 2211.0, 2212.0, 2264.0, 2265.0],
    #     "Empregabilidade": [1367.65, 172.45, 278.1, 32.7, 4084.65, 181.3, 43.3, 79.7, 59.2, 23.8],
    #     "Cbo_Nome": [
    #         "DESENHISTAS DE PRODUTOS E VESTUÁRIO",
    #         "DESENHISTAS GRÁFICOS E DE MULTIMÍDIA",
    #         "PROFISSIONAIS DA PUBLICIDADE",
    #         "DIRIGENTES DE VENDAS",
    #         "ENGENHEIROS CIVIS",
    #         "ENGENHEIROS INDUSTRIAIS",
    #         "MÉDICOS GERAIS",
    #         "MÉDICOS ESPECIALISTAS",
    #         "FISIOTERAPEUTAS",
    #         "DIETISTAS E NUTRICIONISTAS",
    #     ]
    # }

    # # Dados de salário
    # salario_data = {
    #     "Curso": [214.0, 214.0, 342.0, 342.0, 520.0, 520.0, 721.0, 721.0, 726.0, 726.0],
    #     "Cbo": [2163.0, 2166.0, 2431.0, 1221.0, 2141.0, 2142.0, 2211.0, 2212.0, 2264.0, 2265.0],
    #     "Salario_Mediano": [2.94, 3.14, 3.92, 6.86, 8.24, 9.8, 11.76, 12.16, 2.94, 2.94]
    # }

    # # Criando dataframes
    # df_empregabilidade = pd.DataFrame(empregabilidade_data)
    # df_salario = pd.DataFrame(salario_data)

    # # Mesclar os dataframes com base nos campos "Curso" e "Cbo"
    # df_merged = pd.merge(df_empregabilidade, df_salario, on=["Curso", "Cbo"])

    # # Criar gráfico de dispersão com nomes das profissões
    # plt.figure(figsize=(10, 6))
    # plt.scatter(df_merged["Empregabilidade"], df_merged["Salario_Mediano"], color="blue", alpha=0.6)

    # # Adicionar rótulos com os nomes das profissões
    # for i, row in df_merged.iterrows():
    #     plt.text(row["Empregabilidade"], row["Salario_Mediano"], row["Cbo_Nome"], fontsize=8, ha='left', va='bottom')

    # plt.xlabel("Empregabilidade")
    # plt.ylabel("Salário Mediano")
    # plt.title("Relação entre Empregabilidade e Salário Mediano (com Nomes das Profissões)")
    # plt.grid(True)
    # # Exibir gráfico
    # plt.show()
    
    ###########################################################################################################################
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    
    # # Dados de empregabilidade
    empregabilidade_data = {
         "Curso": [214.0, 214.0, 342.0, 342.0, 520.0, 520.0, 721.0, 721.0, 726.0, 726.0],
         "Cbo": [2163.0, 2166.0, 2431.0, 1221.0, 2142.0, 2141.0, 2211.0, 2212.0, 2264.0, 2265.0],
         "Empregabilidade": [1367.65, 172.45, 278.1, 32.7, 4084.65, 181.3, 43.3, 79.7, 59.2, 23.8],
         "Cbo_Nome": [
             "DESENHISTAS DE PRODUTOS E VESTUÁRIO",
             "DESENHISTAS GRÁFICOS E DE MULTIMÍDIA",
             "PROFISSIONAIS DA PUBLICIDADE",
             "DIRIGENTES DE VENDAS",
             "ENGENHEIROS CIVIS",
             "ENGENHEIROS INDUSTRIAIS",
             "MÉDICOS GERAIS",
             "MÉDICOS ESPECIALISTAS",
             "FISIOTERAPEUTAS",
             "DIETISTAS E NUTRICIONISTAS",
         ]
     }


    # # Dados de salário
    salario_data = {
        "Curso": [214.0, 214.0, 342.0, 342.0, 520.0, 520.0, 721.0, 721.0, 726.0, 726.0],
        "Cbo": [2163.0, 2166.0, 2431.0, 1221.0, 2141.0, 2142.0, 2211.0, 2212.0, 2264.0, 2265.0],
        "Salario_Mediano": [2.94, 3.14, 3.92, 6.86, 8.24, 9.8, 11.76, 12.16, 2.94, 2.94]
    }
    # Criando dataframes
    df_empregabilidade = pd.DataFrame(empregabilidade_data)
    df_salario = pd.DataFrame(salario_data)

    # Mesclar os dataframes com base nos campos "Curso" e "Cbo"
    df_merged = pd.merge(df_empregabilidade, df_salario, on=["Curso", "Cbo"])

    # Calcular correlação de Pearson
    correlacao = np.corrcoef(df_merged["Empregabilidade"], df_merged["Salario_Mediano"])[0, 1]

    # Criar gráfico de dispersão
    plt.figure(figsize=(10, 6))
    plt.scatter(df_merged["Empregabilidade"], df_merged["Salario_Mediano"], color="blue", alpha=0.6)

    # Adicionar rótulos com os nomes das profissões
    for i, row in df_merged.iterrows():
        plt.text(row["Empregabilidade"], row["Salario_Mediano"], row["Cbo_Nome"], fontsize=8, ha='left', va='bottom')

    # Exibir a correlação no gráfico
    # plt.text(
    #     max(df_merged["Empregabilidade"]) * 0.6,  # Posição X
    #     max(df_merged["Salario_Mediano"]) * 0.9,  # Posição Y
    #     f"Correlação: {correlacao:.2f}",
    #     fontsize=12,
    #     color="red",
    #     bbox=dict(facecolor="white", alpha=0.5)
    # )

    plt.xlabel("Empregabilidade")
    plt.ylabel("Salário Mediano")
    plt.title("Relação entre Empregabilidade e Salário Mediano ")
    plt.grid(True)

    # Exibir gráfico
    plt.show()




    return