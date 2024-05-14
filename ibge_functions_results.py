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
import logging
import ibge_functions_descriptive_analysis



# https://colab.research.google.com/drive/1iLmL2_RNZNwhhYxoKEYwgy0LWoh7ri-g?authuser=1#scrollTo=8qssn8eI1s9a
def Filtro_Masculino_Feminino(path, name, sx):
    csv_estado = os.path.join(path[0],name[0]) # arquivo do censo do Brasil inteiro (somente graduados)
    Estado = pd.read_csv(csv_estado)
    # print(path[0])

    if sx == "F":
       # Novo Filtro
       #removendo pessoas do sexo masculino ...
       Estado.drop(Estado[(Estado['gênero'] ==1)].index, inplace=True)
       #print("")
       Estado = Estado.reset_index(drop=True)
       Estado = Estado.drop(columns=['Unnamed: 0'])
       Estado.to_csv(path[0] + 'Brasil_Graduados_Fem.csv')
    else: 
         if sx == "M":  
            # Novo Filtro
            #removendo pessoas do sexo feminino ...
            Estado.drop(Estado[(Estado['gênero'] ==2)].index, inplace=True)
            #print("")
            Estado = Estado.reset_index(drop=True)
            Estado = Estado.drop(columns=['Unnamed: 0'])
            Estado.to_csv(path[0] + 'Brasil_Graduados_Masc.csv') 
             
    return

def Ida_Volta_Masculino_Feminino(path,name,path1,name1,sx):

    if sx == 'F':
       logging.info(" Gerando as idas e voltas Femininas")   
       csv_estado = os.path.join(path[0],name[2]) # arquivo do censo do Brasil inteiro (somente graduados)
    if sx == 'M':
       logging.info(" Gerando as idas e voltas Masculinas")   
       csv_estado = os.path.join(path[0],name[3]) # arquivo do censo do Brasil inteiro (somente graduados)
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)
    csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
    csv_CURSOS = os.path.join(path1[0],name1[2]) # Tabela de Cursos
    path2 = ibge_variable.paths(8)
    name2 = ibge_variable.names(8)         
    csv_PivotTableFinal =  os.path.join(path2[0],name2[0]) #Pivo Table Final

    CursosCenso = ibge_functions_descriptive_analysis.ibge_cursos_filter(path1[0],name1[2])
    # print(len(CursosCenso))
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

# Testar curso 79,80,85...
    for f in range(0,89):

        curso_num= float(CursosCenso.curso_num.iloc[f])
        curso_nome= CursosCenso.curso_nome.iloc[f]
        titulo10= "Curso " +  CursosCenso.curso_num.iloc[f] + ": " + CursosCenso.curso_nome.iloc[f] + " - 10% "
        titulo3=  "Curso " +  CursosCenso.curso_num.iloc[f] + ": " + CursosCenso.curso_nome.iloc[f] + " - 10%"
        print("curso_num:", curso_num, "curso_nome:",curso_nome)
        print(f)
        print("=================================================================================================")
        
        #======================================================Plotando os cbos de determinado curso, usando função ...
        primeirosCbos,primeirosCbos_Nome,Porcentagens,CURSO_NUM,CURSO_NOME=ibge_functions_descriptive_analysis.CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0.1,save_results_to)
        if (primeirosCbos!=0)&(primeirosCbos!=0)&(Porcentagens!=0):
            #======================================================Achando a quantidade de Não-Graduados na PivotTable
            primeirosCbos,NaoGraduados,Graduados_Nao,Graduados = ibge_functions_descriptive_analysis.NaoGraduados_PivotTable_2(primeirosCbos, csv_PivotTableFinal)
            #=====================================================Plotando os cursos de determinado cbo, sem função e salvando os plots ...
            Intensidade = []
            Porcentagens_vol = []
            CBO_vol = []
            Cursos_vol = []
            Nomes_vol  = []
            for i in range (len(primeirosCbos)):
                titulo3=primeirosCbos_Nome[i]
                if(int(float(primeirosCbos[i]))>=2000):
                    CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=ibge_functions_descriptive_analysis.Cursos_CBO_14_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.1)
                    Intensidade.append(intensidade)
                    # print(intensidade)
                    Porcentagens_vol.append(porcentagens_vol)
                    CBO_vol.append(CBO)
                    Cursos_vol.append(cursos_vol)
                    Nomes_vol.append(nomes_vol)
                else:
                    print(primeirosCbos[i])
                    CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=ibge_functions_descriptive_analysis.Cursos_CBO_13_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],Graduados_Nao[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.1,save_results_to)
                    if (cursos_vol!=0)&(nomes_vol!=0)&(porcentagens_vol!=0):
                        Intensidade.append(intensidade)
                        Porcentagens_vol.append(porcentagens_vol)
                        CBO_vol.append(CBO)
                        Cursos_vol.append(cursos_vol)
                        Nomes_vol.append(nomes_vol)
                    else:
                        print("Não existe cursos para esse CBO")  

            # ======================================================Plotando os cbos de determinado curso, usando função ...
        
            # ==================================================================Colocando Ida e Volta no mesmo grafico
            if(f==0):
                # Se for a primeira execução, tem que criar as listas ... e o paramentro da ida é 1
                #Recuperando as idas e voltas ...
                x_ = []
                y_ = []
                z_ = []
                v_ = []
                X_,Y_,Z_,V_= ibge_functions_descriptive_analysis.Ida(primeirosCbos,CURSO_NUM,Porcentagens,1,x_,y_,z_,v_)
                x_= X_
                y_= Y_
                z_= Z_
                v_= V_
                for i in range(len(primeirosCbos)):
                    X_,Y_,Z_,V_= ibge_functions_descriptive_analysis.Volta(Cursos_vol[i],primeirosCbos[i],Porcentagens_vol[i], 0,x_,y_,z_,v_)

                x_= X_
                y_= Y_
                z_= Z_
                v_= V_
                #df1 = x_y_z_v_df(X_,Y_,Z_,V_)
                #print(df1)
                #Juntando as idas e voltas ...
                for l in range(len(CBO_vol)):
                    ibge_functions_descriptive_analysis.Jun_Ida_Volta(X_,Y_,Z_,V_, CBO_vol[l],CURSO_NUM)
                #atribuição
                x_= X_
                y_= Y_
                z_= Z_
                v_= V_
            else:
                #Recuperando as idas e voltas ...
                X_,Y_,Z_,V_= ibge_functions_descriptive_analysis.Ida(primeirosCbos,CURSO_NUM,Porcentagens,0,x_,y_,z_,v_)
                x_= X_
                y_= Y_
                z_= Z_
                v_= V_
                for i in range(len(primeirosCbos)):
                    X_,Y_,Z_,V_= ibge_functions_descriptive_analysis.Volta(Cursos_vol[i],primeirosCbos[i],Porcentagens_vol[i], 0,x_,y_,z_,v_)

                x_= X_
                y_= Y_
                z_= Z_
                v_= V_
                #df1 = x_y_z_v_df(X_,Y_,Z_,V_)
                #print(df1)
                #Juntando as idas e voltas ...
                for l in range(len(CBO_vol)):
                    ibge_functions_descriptive_analysis.Jun_Ida_Volta(X_,Y_,Z_,V_, CBO_vol[l],CURSO_NUM)
                #atribuição
                x_= X_
                y_= Y_
                z_= Z_
                v_= V_

    df = ibge_functions_descriptive_analysis.x_y_z_v_df(x_,y_,z_,v_)    
    # df.to_csv(save_results_to + '10Porcent_DF.csv')
    if sx == 'F':
       df.to_csv(save_results_to + '10Porcent_DF_Fem.csv')
    if sx == 'M':
       df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')
    return      

def Tabela_Ida_Volta_Masculino_Feminino(path2,name2,sx):

    if sx == 'F':
       logging.info(" Gerando a Tabela de idas e voltas Femininas")   
       df =  os.path.join(path2[0],name2[3])
       df1 = pd.read_csv(df)  
    if sx == 'M':
       logging.info(" Gerando a Tabela de idas e voltas Masculinas")   
       df =  os.path.join(path2[0],name2[4])
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
    # df1.to_csv(save_results_to + '10Porcent_DF_Limpo.csv')
    # df1.to_excel(save_results_to + '10Porcent_DF_Limpo.xlsx')
    if sx == 'F':
       # df.to_csv(save_results_to + '10Porcent_DF_Fem.csv')
       df1.to_csv(save_results_to + '10Porcent_DF_Fem_Limpo.csv')
       df1.to_excel(save_results_to + '10Porcent_DF_Fem_Limpo.xlsx')
    if sx == 'M':
       # df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')
       df1.to_csv(save_results_to + '10Porcent_DF_Masc_Limpo.csv')
       df1.to_excel(save_results_to + '10Porcent_DF_Masc_Limpo.xlsx')
    return     

def Profissoes_Cursos_Masculino_Feminino(path1,name1,path2,name2,sx): 

    # Leitura
    if sx == 'F':
       logging.info(" Gerando o gráfico de profissões e cursos Femininos")   
       df =  os.path.join(path2[0],name2[5])
       X = pd.read_csv(df)    
       X = X.drop(columns=['Unnamed: 0'])
       X = X.drop(columns=['Unnamed: 0.1'])  
    if sx == 'M':
       logging.info(" Gerando o gráfico de profissões e cursos Masculinos")   
       df =  os.path.join(path2[0],name2[6])
       X = pd.read_csv(df)    
       X = X.drop(columns=['Unnamed: 0'])
       X = X.drop(columns=['Unnamed: 0.1'])
    save_results_to = 'graficos/'    

    # Remoção de Features 
    X = X.drop(columns=['CB'])
    X = X.drop(columns=['CR'])

    CursosCenso = ibge_functions_descriptive_analysis.ibge_cursos_filter(path1[0],name1[2])
    csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
    CBO = pd.read_csv(csv_CBO)


    # Plotagem dos Dados Originais
    # print(X.iloc[:,0])
    plt.figure(figsize=(6, 4))
    # plt.title("10%  - Todos os Cursos - Clusterização ")
    plt.xlabel('Ida')
    plt.ylabel('Volta')
    plt.ylim(0, 100) # definir limite do eixo
    plt.xlim(0, 100) # definir limite do eixo
    plt.grid()
    plt.scatter(X.iloc[:,0],X.iloc[:,1],marker = '*')
    # plt.show()
    # string = "10%  - Todos os Cursos - Dados Originais " +".pdf"
    # save_results_to = 'graficos/'  
    # plt.savefig(save_results_to + string) 
    if sx == 'F':
       plt.title("10%  - Todos os Cursos - Dados Originais Femininos ")
       string = "10%  - Todos os Cursos - Dados Originais Femininos" +".pdf"
       save_results_to = 'graficos/'  
       plt.savefig(save_results_to + string) 
    if sx == 'M':
       plt.title("10%  - Todos os Cursos - Dados Originais Masculinos ")
       string = "10%  - Todos os Cursos - Dados Originais Masculinos" +".pdf"
       save_results_to = 'graficos/'  
       plt.savefig(save_results_to + string)      
    return

def PlotOriginal_AdicionaColunaGenero(path1,name1,path2,name2,G):

    # Leitura do arquivo df original, masculino ou feminino
    if G == 'O':
       logging.info(" Adicionando a coluna Gênero ao arquivo original")   
       # df =  os.path.join(path2[0],name2[2])
       df =  os.path.join(path2[0],name2[7])
       X = pd.read_csv(df)    
       # X = X.drop(columns=['Unnamed: 0'])
       # X = X.drop(columns=['Unnamed: 0.1'])
    else:
        if G == 'F':
           logging.info(" Adicionando a coluna Gênero ao arquivo feminino")   
           df =  os.path.join(path2[0],name2[5])
           X = pd.read_csv(df)    
           X = X.drop(columns=['Unnamed: 0'])
           X = X.drop(columns=['Unnamed: 0.1'])
        else:
            if G == 'M':
               logging.info(" Adicionando a coluna Gênero ao arquivo masculino")   
               df =  os.path.join(path2[0],name2[6])
               X = pd.read_csv(df)    
               X = X.drop(columns=['Unnamed: 0'])
               X = X.drop(columns=['Unnamed: 0.1'])
    # df =  os.path.join(path2[0],name2[2])
    # X = pd.read_csv(df)    
    save_results_to = 'graficos/' 
    # X = X.drop(columns=['Unnamed: 0'])
    # X = X.drop(columns=['Unnamed: 0.1'])

    # # Remoção de Features 
    # X = X.drop(columns=['CB'])
    # X = X.drop(columns=['CR'])

    CursosCenso = ibge_functions_descriptive_analysis.ibge_cursos_filter(path1[0],name1[2])
    csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
    CBO = pd.read_csv(csv_CBO)

    # Pontos do Gráfico na côr Preta (c = 'k')
    x= X['Ida']
    y= X['Volta']
    plt.xlabel("Cursos")
    plt.ylabel("Profissões")
    plt.title("10%  - Cursos e Profissões do Censo_" + G)
    plt.ylim(0, 100) # definir limite do eixo
    plt.xlim(0, 100) # definir limite do eixo
    plt.grid()
    plt.scatter(x,y,marker = '*')
    string1 = "10%  - Cursos e Profissões do Censo_" + G + ".pdf"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string1)  


    # Leitura do arquivo df original, masculino ou feminino
    if G == 'O':
       X['Genero'] = "O"    
       X.to_csv(save_results_to +'Resultados_T_Original.csv')  
    else:
          # ...
        CursoNome =[]
        for i in range (len(X['CR'])):
            for index, row in CursosCenso.iterrows():
                if (str(X['CR'][i]) == CursosCenso['curso_num'][index]):
                    CursoNome.append(CursosCenso['curso_nome'][index])

        # CursoNome
        CboNome =[]
        for i in range (len(X['CB'])):
            for index, row in CBO.iterrows():
                if (int(X['CB'][i]) == CBO['Cod_CBO'][index]):
                    CboNome.append(CBO['Nome_CBO'][index])  
        if G == 'F':
             # Adicionando coluna
            resultados_T=[]
            cluster=""
            # X['Cluster'][i]
            for i in range(len(X['CR'])):
                tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"F")
                resultados_T.append(tupla)
            #...
            Resultados_T= pd.DataFrame(resultados_T)
            #...
            dict = {0:"Ida",
                    1:"Volta",
                    2:"Cluster",
                    3:"Curso",
                    4:"Curso_Nome",
                    5:"Cbo",
                    6:"Cbo_Nome",
                    7:"Genero"
            }
            Resultados_T.rename(columns=dict,inplace=True)   
            Resultados_T.to_csv(save_results_to +'Resultados_T_Fem.csv')         
        else:
              if G == 'M':
                  # Adicionando coluna
                resultados_T=[]
                cluster=""
                # X['Cluster'][i]
                for i in range(len(X['CR'])):
                    tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"M")
                    resultados_T.append(tupla)
                #...
                Resultados_T= pd.DataFrame(resultados_T)
                #...
                dict = {0:"Ida",
                        1:"Volta",
                        2:"Cluster",
                        3:"Curso",
                        4:"Curso_Nome",
                        5:"Cbo",
                        6:"Cbo_Nome",
                        7:"Genero"
                }
                Resultados_T.rename(columns=dict,inplace=True)   
                Resultados_T.to_csv(save_results_to +'Resultados_T_Masc.csv')          
                 
   
                         
    return
