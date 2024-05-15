#pip install ibge-parser

import string
import sys
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

def CBOs_Curso_v6_sn2(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,porcent_param):
    # X = pd.read_csv(csv_estado)
    X = csv_estado
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    # CURSOS = pd.read_csv(csv_CURSOS, dtype ='str')
    CBO = CBO.drop(columns=['Unnamed: 0'])
    # CURSOS = CURSOS.drop(columns=['Unnamed: 0'])

    X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']]

    # for i in range(len(X_CURSO_CBO)):
    #     X_CURSO_CBO.Ocupação_Código[i] = str(X_CURSO_CBO.Ocupação_Código[i])

    # ...
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
    # ...
    X_CURSO_CBO = pd.DataFrame(X_CURSO_CBO_Filter)
    # ...
    # ...
    dict = {0:"Curso_Superior_Graduação_Código",
    1:"Ocupação_Código",
    }
    X_CURSO_CBO.rename(columns=dict,inplace=True)

    dir = X_CURSO_CBO.index[X_CURSO_CBO['Curso_Superior_Graduação_Código'] == curso_num].tolist()
    if(len(dir)>=1):
        #dir
        # ...
        Curso_dir = []
        Cbo_dir = []
        for i in range(len(dir)):
            curso = X_CURSO_CBO._get_value(dir[i],'Curso_Superior_Graduação_Código')
            cbo = X_CURSO_CBO._get_value(dir[i],'Ocupação_Código')
            Curso_dir.append(curso)
            Cbo_dir.append(cbo)
            #...
        resultados_dir=[]
        for i in range(len(Curso_dir)):
            tupla=(Curso_dir[i],Cbo_dir[i])
            resultados_dir.append(tupla)
        #...
        Curso_Cbo_dir = pd.DataFrame(resultados_dir)

        dict = {0:"Curso",
        1:"Cbo",
        }
        Curso_Cbo_dir.rename(columns=dict,inplace=True)

        Curso_Cbo_dir_unique = np.unique(Curso_Cbo_dir.Cbo)

        #...
        Curso_Cbo_dir['Cbo'].value_counts().sort_index()

        #...
        from numpy.ma.core import sort
        A = Curso_Cbo_dir['Cbo'].value_counts().sort_index()
        #...

        A = pd.DataFrame(A)

        A_cbo = A.sort_values("Cbo",ascending=False)
        Total = A_cbo["Cbo"].sum() #=====================================================
        #porcento = Total*0.1
        porcento = Total*porcent_param
        porcento_10 = round(porcento/Total * 100, 2)

        # ...
        Porcentagem = []
        for i in range(len(A_cbo)):
            Porcentagem = round(A_cbo['Cbo']/Total * 100, 2)
        A_cbo['Porcentagem'] = Porcentagem

        qtdade = 0
        # for i in range(len(A_cbo)):
        #     #if (A_cbo.Porcentagem[i]>= porcento_10):
        #     if (A_cbo.Porcentagem[i]<= porcento_10):
        #         qtdade = qtdade+1
        for i in A_cbo.index:
                    if (A_cbo.Porcentagem[i]<= porcento_10):
                        qtdade = qtdade+1        
        #print(A_cbo)
        #print("")
        #print(qtdade)
        A_cbo_10 = A_cbo.head(qtdade) #Alterado 29/09/2023   =========================
        #print("")
        #print(A_cbo_10)
        #sys.exit()

        # Validação =======================================================================
        if(len(A_cbo_10>=1)):
            ##Coletando o nome do CBOs ... #============================= linha 106 até 128 ... versão antiga
            #NomeCbo = []
            #for i in range(len(A_cbo_10)):
            #    cbo=str(int(float(str(A_cbo_10.index[i])))) #Comentei pra ver se corrige o erro
            #    for indexx, row in CBO.iterrows():
            #        if (row['Cod_CBO'] == cbo):
            #            NomeCbo.append(row['Nome_CBO'])

            #NomeCbo = pd.DataFrame(NomeCbo, columns=['Nome_CBO'])

            #...
            #A_cbo_10["Nome"] = 1
            #...

            #for i in range(len(A_cbo_10)):
            #    A_cbo_10['Nome'][i] = NomeCbo.Nome_CBO[i]

            #A_cbo_10.reset_index(inplace=True)
            #A_cbo_10 = A_cbo_10.rename(columns = {'index':'Cod_CBO'})

            #...
            #A_cbo_10['Cod_CBO'] = A_cbo_10['Cod_CBO'].astype("float").astype('str')
            #A_cbo_10['CBO_Nome'] = A_cbo_10['Cod_CBO'].str.cat(A_cbo_10['Nome'], sep =" ")

            ##Coletando o nome do CBOs ... #============================= linha 130 até 148 ... versão nova
            A_cbo_10["Nome"] = 1
            for i in range(len(A_cbo_10)):
                cbo=str(int(float(str(A_cbo_10.index[i]))))
                for indexx, row in CBO.iterrows():
                    if (row['Cod_CBO'] == cbo):
                        A_cbo_10['Nome'][i] = row['Nome_CBO']
                        break

            #print(A_cbo_10)
            #print("")
            #print("")

            A_cbo_10['Cod_CBO'] = 1
            A_cbo_10['CBO_Nome'] = 1
            A_cbo_10['Cod_CBO'] = A_cbo_10.index
            #A_cbo_10['CBO_Nome'] = A_cbo_10['Cod_CBO'].str.cat(A_cbo_10['Nome'], sep =" ")
            A_cbo_10['CBO_Nome'] = A_cbo_10['Cod_CBO'].map(str) + '-' + A_cbo_10['Nome'].map(str)
            #print(A_cbo_10)

            primeiros = [] # Alterado em 29/09/2023
            if (len(A_cbo_10)<1):
                #for i in range(len(A_cbo_10)):
                #    tresprimeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
                print("Não existe CBOs para este curso")
                sys.exit() #===============================================================================================
            else:
                for i in range(len(A_cbo_10)):
                    primeiros.append(str(int(float(A_cbo_10['Cod_CBO'].iloc[i]))))
                    # primeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
            #...
            #Deletar coluna
            del A_cbo_10["Cod_CBO"]
            del A_cbo_10["Nome"]

            nomes = [] # Alterado em 26/09/2023
            if (len(A_cbo_10)<1):
                print("Não existe CBOs para este curso")
                sys.exit() #===============================================================================================
            else:
                for i in range(len(A_cbo_10)):
                    # nomes.append(A_cbo_10.CBO_Nome[i])
                    nomes.append(A_cbo_10['CBO_Nome'].iloc[i])
            porcentagens = []
            if (len(A_cbo_10)<1):
                print("Não existe CBOs para este curso")
                sys.exit() #===============================================================================================
            else:
                for i in range(len(A_cbo_10)):
                    # porcentagens.append(A_cbo_10.Porcentagem[i])
                    porcentagens.append(A_cbo_10['Porcentagem'].iloc[i])
            #####================================================= ate aqui =======================================================================================
            #...
            #x='CBO_Nome'
            #y='Porcentagem'
            #Plotando ...
            #A_cbo_10_sort = A_cbo_10.iloc[0:3].sort_values("Porcentagem",ascending=True)
            #plt.rcParams["figure.figsize"] = (18, 8)
            #plt.rcParams["figure.autolayout"] = True
            #ax = A_cbo_10_sort.plot(x,y,kind='barh',title=titulo3,legend=False)
            #ax.bar_label(ax.containers[0])
            #plt.xlabel("Porcentagem")
            #string = str(curso_num) + " - " + curso_nome + ".pdf"
            #save_results_to = '/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/Experimentos_25_09_a_02_09/SemPorcentagem-Todos-IdaVolta/Ida/'
            #plt.savefig(save_results_to + string)
            #plt.show()
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

def Cursos_CBO_13_10_sn(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo3,NaoGraduados_qtdade,Graduados_Nao_Total,curso_num,curso_nome,primeirosCbos_Nome,i,porcent_param):
    numero = i
    # X = pd.read_csv(csv_estado)
    X = csv_estado
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    CURSOS = pd.read_csv(csv_CURSOS, dtype ='str')
    CBO = CBO.drop(columns=['Unnamed: 0'])
    CURSOS = CURSOS.drop(columns=['Unnamed: 0'])


    #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
    X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']]
    X_CURSO_CBO.shape

    #Cursos por CBO
    #Indice =================================================================================================
    # dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['Ocupação_Código'] == cbo_num].tolist()
    X_CURSO_CBO['Ocupação_Código'] = X_CURSO_CBO['Ocupação_Código'].astype(int)
    dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['Ocupação_Código'] == int(str(cbo_num))].tolist()
    # ...
    Curso_dir_curso_cbos = []
    Cbo_dir_curso_cbos = []
    for i in range(len(dir_curso_cbos)):
        #print(direito[i])
        curso = X_CURSO_CBO._get_value(dir_curso_cbos[i],'Curso_Superior_Graduação_Código')
        cbo = X_CURSO_CBO._get_value(dir_curso_cbos[i],'Ocupação_Código')
        Curso_dir_curso_cbos.append(curso)
        Cbo_dir_curso_cbos.append(cbo)
    #..
    resultados_dir_curso_cbos=[]
    for i in range(len(Curso_dir_curso_cbos)):
      tupla=(Curso_dir_curso_cbos[i],Cbo_dir_curso_cbos[i])
      resultados_dir_curso_cbos.append(tupla)
    #...
    Curso_Cbo_dir_curso_cbos = pd.DataFrame(resultados_dir_curso_cbos)
    dict = {0:"Curso_Repet",
        1:"Cbo_Repet",
        }
    Curso_Cbo_dir_curso_cbos.rename(columns=dict,inplace=True)

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

    Total = A_Curso['Curso_Repet'].sum()
    #porcento = Total*0.1
    porcento = Total*porcent_param
    porcento_10 = round(porcento/Total * 100, 2)

    Porcentagem = []
    for i in range(len(A_Curso)):
        Porcentagem = round(A_Curso['Curso_Repet']/Total * 100, 2)
    A_Curso['Porcentagem'] = Porcentagem

    #...
    qtdade = 0

    A_Curso.index = A_Curso.index.astype(str)

    for i in range(len(A_Curso)):
        #if (A_Curso.Porcentagem[i]>= porcento_10):
        if (A_Curso.Porcentagem[i]<= porcento_10):  #pegar todos ...
            qtdade = qtdade+1
    #print(A_Curso)
    #print("")
    #print(qtdade)

    A_Curso_11 = A_Curso.head(qtdade) #Alterado 29/09/2023   =========================
    #print("")
    #print(A_Curso_11)
    #sys.exit() #======================================================================

    if(len(A_Curso_11)>=1):
        NomeCurso = []
        for i in range(len(A_Curso_11)):
            curso=str(float(A_Curso_11.index[i]))
            for indexx, row in CURSOS.iterrows():
                if (row['Cod_Curso'] == curso):
                    NomeCurso.append(row['Nome_Curso'])

        #...
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

        A_Curso_11['Curso'] = A_Curso_11['Curso'].astype("float").astype('str')

        A_Curso_11['Curso_Nome'] = A_Curso_11['Curso'].str.cat(A_Curso_11['Nome'], sep =" ")

        qtdadenv=qtdade

        A_Curso_11.loc[qtdade] = [0,0,0,0,0]

        A_Curso_11['Curso'].iloc[qtdade]= 0
        A_Curso_11['Curso_Repet'].iloc[qtdade]= NaoGraduados_qtdade
        A_Curso_11['Nome'].iloc[qtdade]= "Não-Graduados"
        A_Curso_11['Curso_Nome'].iloc[qtdade]= "Não-Graduados"

        A_Curso_11['Porcentagem'].iloc[qtdade]= round(NaoGraduados_qtdade/Graduados_Nao_Total * 100, 2) #26/09

        primeiros = []
        if (len(A_Curso_11)<1):
            print("Não existem cursos para este CBO")
        else:
            for i in range(len(A_Curso_11)): #Alterado em 09/09/2023 para pegar o 4º Elemento
                primeiros.append(int(float(A_Curso_11.Curso[i])))

        A_Curso_11_sort = A_Curso_11.iloc[0:qtdadenv+1].sort_values("Porcentagem",ascending=True)  #26/09

        index =  A_Curso_11_sort.index

        colors = []
        for i in range(len(index)):
            if (A_Curso_11_sort['Curso'].iloc[i]==0):
                colors.append('red')
            else:
                colors.append('black')

        tituloalterado = titulo3 + " : " + "Cbo fraco"
        curso_num = str(float(curso_num))

        intensidade = 'Fraco'
        for i in range(len(index)):
            if ((A_Curso_11_sort.index[i]==0)and(A_Curso_11_sort['Curso'].iloc[i]==str(curso_num))): #curso_num
                tituloalterado = titulo3 + " : " + "Cbo forte"
                intensidade ='Forte'
                break

        cursos = [] # Alterado em 26/09/2023
        if (len(A_Curso_11)<1):
          print("Não existe CBOs para este curso")
          sys.exit() #===============================================================================================
        else:
            for i in range(len(A_Curso_11)):
                cursos.append(A_Curso_11.Curso[i])
        nomes = [] # Alterado em 26/09/2023
        if (len(A_Curso_11)<1):
            print("Não existe CBOs para este curso")
            sys.exit() #===============================================================================================
        else:
            for i in range(len(A_Curso_11)):
                nomes.append(A_Curso_11.Nome[i])

        porcentagens = []
        if (len(A_Curso_11)<1):
            print("Não existe CBOs para este curso")
            sys.exit() #===============================================================================================
        else:
            for i in range(len(A_Curso_11)):
                porcentagens.append(A_Curso_11.Porcentagem[i])


        #x='Curso_Nome'
        #y='Porcentagem'
        #ax = A_Curso_11_sort.plot(x,y,kind='barh',title=tituloalterado,color=colors,legend=False)
        #ax.bar_label(ax.containers[0])
        #plt.xlabel("Porcentagem")
        #string = str(curso_num) + " - " + curso_nome + " : " + primeirosCbos_Nome[numero] +".pdf"
        #save_results_to = '/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/Experimentos_25_09_a_02_09/SemPorcentagem-Todos-IdaVolta/Volta/'
        #plt.savefig(save_results_to + string)

    else:
       print("Não existe cursos para esse CBO")
    #return cbo_num,curso_nome,primeirosCbos_Nome,intensidade,plt,string, cursos, nomes, porcentagens
    return cbo_num,curso_nome,primeirosCbos_Nome,intensidade,plt, cursos, nomes, porcentagens

def Cursos_CBO_14_10_sn(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo3,NaoGraduados_qtdade,curso_num,curso_nome,primeirosCbos_Nome,i,porcent_param):
    numero = i

    # X = pd.read_csv(csv_estado)
    X = csv_estado
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    CURSOS = pd.read_csv(csv_CURSOS, dtype ='str')

    CBO = CBO.drop(columns=['Unnamed: 0'])
    CURSOS = CURSOS.drop(columns=['Unnamed: 0'])


    #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
    X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']]
    X_CURSO_CBO.shape

    #Cursos por CBO
    #Indice =================================================================================================
    # dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['Ocupação_Código'] == cbo_num].tolist()
    X_CURSO_CBO['Ocupação_Código'] = X_CURSO_CBO['Ocupação_Código'].astype(int)
    dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['Ocupação_Código'] == int(str(cbo_num))].tolist()
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

    #Plot======================================================================================================
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

    Total = A_Curso['Curso_Repet'].sum()
    #porcento = Total*0.1
    porcento = Total*porcent_param
    porcento_10 = round(porcento/Total * 100, 2)

    Porcentagem = []
    for i in range(len(A_Curso)):
        Porcentagem = round(A_Curso['Curso_Repet']/Total * 100, 2)
    A_Curso['Porcentagem'] = Porcentagem

    #...
    qtdade = 0

    A_Curso.index = A_Curso.index.astype(str)

    for i in range(len(A_Curso)):
        #if (A_Curso.Porcentagem[i]>= porcento_10):
        if (A_Curso.Porcentagem[i]<= porcento_10):
            qtdade = qtdade+1
    #print(A_Curso)
    #print("")
    #print(qtdade)
    A_Curso_11 = A_Curso.head(qtdade)
    #print("")
    #print(A_Curso_11)
    #sys.exit() #==============================================================

    if(len(A_Curso_11)>=1):
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
      A_Curso_11["Nome"] = 1
      import warnings
      for i in range(len(A_Curso_11)):
        #   A_Curso_11['Nome'][i] = NomeCurso.Nome_Curso[i]
          A_Curso_11['Nome'].iloc[i]= NomeCurso['Nome_Curso'].iloc[i]

      #...
      A_Curso_11.reset_index(inplace=True)
      A_Curso_11 = A_Curso_11.rename(columns = {'index':'Curso'})

      A_Curso_11['Curso'] = A_Curso_11['Curso'].astype("float").astype('str')

      A_Curso_11['Curso_Nome'] = A_Curso_11['Curso'].str.cat(A_Curso_11['Nome'], sep =" ")

      #...
      primeiros = []
      if (len(A_Curso_11)<1):
          print("Não existem cursos para este CBO")
      else:
          for i in range(len(A_Curso_11)): #Alterado em 09/09/2023 para pegar o 4º Elemento
              primeiros.append(int(float(A_Curso_11.Curso[i])))

      A_Curso_11_sort = A_Curso_11.iloc[0:qtdade].sort_values("Porcentagem",ascending=True)  #26/09

      index =  A_Curso_11_sort.index

      colors = []
      for i in range(len(index)):
          colors.append('black')

      tituloalterado = titulo3 + " : " + "Cbo fraco"
      curso_num = str(float(curso_num))
      intensidade = 'Fraco'

      for i in range(len(index)):
          if ((A_Curso_11_sort.index[i]==0)and(A_Curso_11_sort['Curso'].iloc[i]==str(curso_num))): #curso_num
              tituloalterado = titulo3 + " : " + "Cbo forte"
              intensidade ='Forte'
              break


      cursos = [] # Alterado em 26/09/2023
      if (len(A_Curso_11)<1):
        print("Não existe CBOs para este curso")
        sys.exit() #===============================================================================================
      else:
          for i in range(len(A_Curso_11)):
              cursos.append(A_Curso_11.Curso[i])

      nomes = [] # Alterado em 26/09/2023
      if (len(A_Curso_11)<1):
          print("Não existe CBOs para este curso")
          sys.exit() #===============================================================================================
      else:
          for i in range(len(A_Curso_11)):
              nomes.append(A_Curso_11.Nome[i])

      porcentagens = []
      if (len(A_Curso_11)<1):
          print("Não existe CBOs para este curso")
          sys.exit() #===============================================================================================
      else:
          for i in range(len(A_Curso_11)):
              porcentagens.append(A_Curso_11.Porcentagem[i])

      #x='Curso_Nome'
      #y='Porcentagem'
      #plt.rcParams["figure.figsize"] = (18, 8)
      #plt.rcParams["figure.autolayout"] = True
      #ax = A_Curso_11_sort.plot(x,y,kind='barh',title=tituloalterado,color=colors,legend=False)
      #ax.bar_label(ax.containers[0])
      #plt.xlabel("Porcentagem")
      #string = str(curso_num) + " - " + curso_nome + " : " + primeirosCbos_Nome[numero] +".pdf"
      #save_results_to = '/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/Experimentos_25_09_a_02_09/SemPorcentagem-Todos-IdaVolta/Volta/'
      #plt.savefig(save_results_to + string)
      #volta = 'Volta'
    else:
       print("Não existe cursos para esse CBO")

    #return cbo_num,curso_nome,primeirosCbos_Nome,intensidade,plt,string,cursos,nomes,porcentagens
    return cbo_num,curso_nome,primeirosCbos_Nome,intensidade,plt,cursos,nomes,porcentagens

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
       # Transformar as colunas( Cluster, Curso e Cbo) para inteiro ...
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
       plt.title("10%  - Cursos e Profissões - Femininos ")
       string = "10%  - Todos os Cursos - Dados Originais Femininos" +".pdf"
       save_results_to = 'graficos/'  
       plt.savefig(save_results_to + string) 
    if sx == 'M':
       plt.title("10%  - Cursos e Profissões - Masculinos ")
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

def Filtro_Idade(path, name, idade):
    csv_estado = os.path.join(path[0],name[0]) # arquivo do censo do Brasil inteiro (somente graduados)
    Estado = pd.read_csv(csv_estado)
    # print(path[0])

    if idade == "29":
        # Novo Filtro
        Estado.drop(Estado[(Estado['Idade_em_Anos'] >29)].index, inplace=True)
        #print("")
        Estado = Estado.reset_index(drop=True)
        Estado = Estado.drop(columns=['Unnamed: 0'])
        # Estado.to_csv(path[0] + 'Brasil_Graduados_29.csv')
    else: 
         if idade == "30-39":  
            # Novo Filtro
            Estado.drop(Estado[(Estado['Idade_em_Anos'] <=30)].index, inplace=True)
            Estado.drop(Estado[(Estado['Idade_em_Anos'] >=39)].index, inplace=True)
            Estado = Estado.reset_index(drop=True)
            Estado = Estado.drop(columns=['Unnamed: 0'])
            # Estado.to_csv(path[0] + 'Brasil_Graduados_30_39.csv') 
         else:   
           if idade == "40-49":  
                # Novo Filtro
                Estado.drop(Estado[(Estado['Idade_em_Anos'] <=40)].index, inplace=True)
                Estado.drop(Estado[(Estado['Idade_em_Anos'] >=49)].index, inplace=True)                
                Estado = Estado.reset_index(drop=True)
                Estado = Estado.drop(columns=['Unnamed: 0'])
                # Estado.to_csv(path[0] + 'Brasil_Graduados_40_49.csv') 
           else:
               if idade == "50-59":  
                    # Novo Filtro
                    Estado.drop(Estado[(Estado['Idade_em_Anos'] <=50)].index, inplace=True)
                    Estado.drop(Estado[(Estado['Idade_em_Anos'] >=59)].index, inplace=True)         
                    Estado = Estado.reset_index(drop=True)
                    Estado = Estado.drop(columns=['Unnamed: 0'])
                    # Estado.to_csv(path[0] + 'Brasil_Graduados_50_59.csv') 
               else: 
                    if idade == "60":  
                        # Novo Filtro
                        Estado.drop(Estado[(Estado['Idade_em_Anos'] <=60)].index, inplace=True)
                        Estado = Estado.reset_index(drop=True)
                        Estado = Estado.drop(columns=['Unnamed: 0'])
                        # Estado.to_csv(path[0] + 'Brasil_Graduados_60.csv')   
                   
    return Estado

def Ida_Volta_Idade(df,path1,name1,idade):   
    
    # if idade == '29':
    #    logging.info(" Gerando as idas e voltas Femininas")   
    #    csv_estado = os.path.join(path[0],name[2]) # arquivo do censo do Brasil inteiro (somente graduados)
    # if sx == 'M':
    #    logging.info(" Gerando as idas e voltas Masculinas")   
    #    csv_estado = os.path.join(path[0],name[3]) # arquivo do censo do Brasil inteiro (somente graduados)
    # path1 = ibge_variable.paths(12)
    # name1 = ibge_variable.names(6)
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
    # print(df.head(5)) 
    # print("")
    for f in range(0,89):
    

        curso_num= float(CursosCenso.curso_num.iloc[f])
        curso_nome= CursosCenso.curso_nome.iloc[f]
        titulo10= "Curso " +  CursosCenso.curso_num.iloc[f] + ": " + CursosCenso.curso_nome.iloc[f] + " - 100% "
        titulo3=  "Curso " +  CursosCenso.curso_num.iloc[f] + ": " + CursosCenso.curso_nome.iloc[f] + " - 100%"
        print("curso_num:", curso_num, "curso_nome:",curso_nome)
        print(f)
        print("=================================================================================================")
        #======================================================Plotando os cbos de determinado curso, usando função ...
        #primeirosCbos,primeirosCbos_Nome,CURSO_NUM,CURSO_NOME=CBOs_Curso_v5(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3)
        #primeirosCbos,primeirosCbos_Nome,CURSO_NUM,CURSO_NOME=CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3)
        #primeirosCbos,primeirosCbos_Nome,Porcentagens,CURSO_NUM,CURSO_NOME=CBOs_Curso_v6_sn(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0.07)
        primeirosCbos,primeirosCbos_Nome,Porcentagens,CURSO_NUM,CURSO_NOME=CBOs_Curso_v6_sn2(df,csv_CBO,curso_num,curso_nome,titulo10,titulo3,1)
        if (primeirosCbos!=0)&(primeirosCbos!=0)&(Porcentagens!=0):
            #======================================================Achando a quantidade de Não-Graduados na PivotTable
            #NaoGraduados = NaoGraduados_PivotTable(primeirosCbos, csv_PivotTableFinal)
            primeirosCbos,NaoGraduados,Graduados_Nao,Graduados = ibge_functions_descriptive_analysis.NaoGraduados_PivotTable_2(primeirosCbos, csv_PivotTableFinal)
            #primeirosCbos,NaoGraduados,Graduados_Nao,Graduados = NaoGraduados_PivotTable(primeirosCbos, csv_PivotTableFinalFem)
            #=====================================================Plotando os cursos de determinado cbo, sem função e salvando os plots ...
            Intensidade = []
            Porcentagens_vol = []
            CBO_vol = []
            Cursos_vol = []
            Nomes_vol  = []
            for i in range (len(primeirosCbos)):
                #if(i==1):
                #   break
                #titulo3= primeirosCursos[i] #Alterado em 09/09/2023 para plotar os Não-Graduados
                titulo3=primeirosCbos_Nome[i]
                #print(type(int(float(primeirosCbos[i]))))
                #sys.exit() #=======================================================================================================
                #tresprimeirosCursos=Cursos_CBO_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3)
                #tresprimeirosCursos=Cursos_CBO_12(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],curso_num)
                if(int(float(primeirosCbos[i]))>=2000):
                    #CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_14_10_sn(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.07)
                    CBO,Curso,tresprimeirosCursos,intensidade,fig,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_14_10_sn(df,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],curso_num,curso_nome,primeirosCbos_Nome,i,1)
                    Intensidade.append(intensidade)
                    #print(intensidade)
                    Porcentagens_vol.append(porcentagens_vol)
                    #print(porcentagens_vol)
                    CBO_vol.append(CBO)
                    Cursos_vol.append(cursos_vol)
                    Nomes_vol.append(nomes_vol)
                    #fig.savefig(string)
                else:
                    #CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_13_10_sn(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],Graduados_Nao[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.07)
                    CBO,Curso,tresprimeirosCursos,intensidade,fig,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_13_10_sn(df,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],Graduados_Nao[i],curso_num,curso_nome,primeirosCbos_Nome,i,1)
                    Intensidade.append(intensidade)
                    Porcentagens_vol.append(porcentagens_vol)
                    CBO_vol.append(CBO)
                    Cursos_vol.append(cursos_vol)
                    Nomes_vol.append(nomes_vol)
                    #fig.savefig(string)
                #print(tresprimeirosCursos)
                #print(NaoGraduados[i])
                print("============================================================================================================================================")


            #==================================================================Colocando Ida e Volta no mesmo grafico
            #print(primeirosCbos)
            #print("")
            #print(primeirosCbos_Nome)
            #print("")
            #print(Porcentagens)
            #print("")
            #print(CURSO_NUM)
            #print("")
            #print(CURSO_NOME)
            #print("")
            #primeirosCursos[0] + " -  Os 3 maiores Cursos"

            ##print(CBO)
            ##print(CBO_vol)
            #print(Curso)
            #print(tresprimeirosCursos)
            #print(Intensidade)
            #print("")
            #print(CBO_vol)
            #print(cursos_vol)
            #print(nomes_vol)
            #print(Porcentagens_vol)

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
    if idade == '29':
       df.to_csv(save_results_to + '100Porcent_DF_29.csv')
    # if idade == 'M':
    #    df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')    
    return