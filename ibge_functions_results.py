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
    import pandas as pd

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
      import pandas as pd
      import pandas as pd
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
       # Estado.to_csv(path[0] + 'Brasil_Graduados_Fem.csv')
    else: 
         if sx == "M":  
            # Novo Filtro
            #removendo pessoas do sexo feminino ...
            Estado.drop(Estado[(Estado['gênero'] ==2)].index, inplace=True)
            #print("")
            Estado = Estado.reset_index(drop=True)
            Estado = Estado.drop(columns=['Unnamed: 0'])
            # Estado.to_csv(path[0] + 'Brasil_Graduados_Masc.csv') 
             
    return Estado

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
    #plt.xlabel('Ida')
    #plt.ylabel('Volta')
    plt.xlabel('Courses')
    plt.ylabel('Professions')
    plt.ylim(0, 100) # definir limite do eixo
    plt.xlim(0, 100) # definir limite do eixo
    plt.grid()
    plt.scatter(X.iloc[:,0],X.iloc[:,1],marker = '*')
    # plt.show()
    # string = "10%  - Todos os Cursos - Dados Originais " +".pdf"
    # save_results_to = 'graficos/'  
    # plt.savefig(save_results_to + string) 
    if sx == 'F':
       # plt.title("10%  - Cursos e Profissões - Femininos ")
       #string = "10%  - Todos os Cursos - Dados Originais Femininos" +".pdf"
       # plt.title("10% - Courses and Professions - Female ")
       string = "10% - All Courses - Original Female Data" +".png"
       save_results_to = 'graficos/'  
       plt.savefig(save_results_to + string) 
    if sx == 'M':
       # plt.title("10%  - Cursos e Profissões - Masculinos ")
       #string = "10%  - Todos os Cursos - Dados Originais Masculinos" +".pdf"
       # plt.title("10% - Courses and Professions - Male ")
       string = "10% - All Courses - Original Male Data" +".png"
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
       # X.to_csv(save_results_to +'Resultados_T_Original.csv')  
       return X
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
            # Resultados_T.to_csv(save_results_to +'Resultados_T_Fem.csv')   
            return Resultados_T          
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
                # Resultados_T.to_csv(save_results_to +'Resultados_T_Masc.csv')   
                return Resultados_T       
                 
   
                         
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
        #Estado.to_csv(path[0] + 'Brasil_Graduados_29.csv')
    else: 
         if idade == "30-39":  
            # Novo Filtro
            Estado.drop(Estado[(Estado['Idade_em_Anos'] <=30)].index, inplace=True)
            Estado.drop(Estado[(Estado['Idade_em_Anos'] >=39)].index, inplace=True)
            Estado = Estado.reset_index(drop=True)
            Estado = Estado.drop(columns=['Unnamed: 0'])
            #Estado.to_csv(path[0] + 'Brasil_Graduados_30_39.csv') 
         else:   
           if idade == "40-49":  
                # Novo Filtro
                Estado.drop(Estado[(Estado['Idade_em_Anos'] <=40)].index, inplace=True)
                Estado.drop(Estado[(Estado['Idade_em_Anos'] >=49)].index, inplace=True)                
                Estado = Estado.reset_index(drop=True)
                Estado = Estado.drop(columns=['Unnamed: 0'])
                #Estado.to_csv(path[0] + 'Brasil_Graduados_40_49.csv') 
           else:
               if idade == "50-59":  
                    # Novo Filtro
                    Estado.drop(Estado[(Estado['Idade_em_Anos'] <=50)].index, inplace=True)
                    Estado.drop(Estado[(Estado['Idade_em_Anos'] >=59)].index, inplace=True)         
                    Estado = Estado.reset_index(drop=True)
                    Estado = Estado.drop(columns=['Unnamed: 0'])
                    #Estado.to_csv(path[0] + 'Brasil_Graduados_50_59.csv') 
               else: 
                    if idade == "60":  
                        # Novo Filtro
                        Estado.drop(Estado[(Estado['Idade_em_Anos'] <=60)].index, inplace=True)
                        Estado = Estado.reset_index(drop=True)
                        Estado = Estado.drop(columns=['Unnamed: 0'])
                        #Estado.to_csv(path[0] + 'Brasil_Graduados_60.csv')   
                   
    return Estado

# def Filtro_Idade(path, name, idade):
#     csv_estado = os.path.join(path[0],name[0]) # arquivo do censo do Brasil inteiro (somente graduados)
#     Estado = pd.read_csv(csv_estado)
#     # print(path[0])

#     if idade == "29":
#         # Novo Filtro
#         Estado.drop(Estado[(Estado['Idade_em_Anos'] >29)].index, inplace=True)
#         #print("")
#         Estado = Estado.reset_index(drop=True)
#         Estado = Estado.drop(columns=['Unnamed: 0'])
#         #Estado.to_csv(path[0] + 'Brasil_Graduados_29.csv')
#     else: 
#          if idade == "30-39":  
#             # Novo Filtro
#             Estado.drop(Estado[(Estado['Idade_em_Anos'] <=30)].index, inplace=True)
#             Estado.drop(Estado[(Estado['Idade_em_Anos'] >=39)].index, inplace=True)
#             Estado = Estado.reset_index(drop=True)
#             Estado = Estado.drop(columns=['Unnamed: 0'])
#             #Estado.to_csv(path[0] + 'Brasil_Graduados_30_39.csv') 
#          else:   
#            if idade == "40-49":  
#                 # Novo Filtro
#                 Estado.drop(Estado[(Estado['Idade_em_Anos'] <=40)].index, inplace=True)
#                 Estado.drop(Estado[(Estado['Idade_em_Anos'] >=49)].index, inplace=True)                
#                 Estado = Estado.reset_index(drop=True)
#                 Estado = Estado.drop(columns=['Unnamed: 0'])
#                 #Estado.to_csv(path[0] + 'Brasil_Graduados_40_49.csv') 
#            else:
#                if idade == "50-59":  
#                     # Novo Filtro
#                     Estado.drop(Estado[(Estado['Idade_em_Anos'] <=50)].index, inplace=True)
#                     Estado.drop(Estado[(Estado['Idade_em_Anos'] >=59)].index, inplace=True)         
#                     Estado = Estado.reset_index(drop=True)
#                     Estado = Estado.drop(columns=['Unnamed: 0'])
#                     #Estado.to_csv(path[0] + 'Brasil_Graduados_50_59.csv') 
#                else: 
#                     if idade == "60":  
#                         # Novo Filtro
#                         Estado.drop(Estado[(Estado['Idade_em_Anos'] <=60)].index, inplace=True)
#                         Estado = Estado.reset_index(drop=True)
#                         Estado = Estado.drop(columns=['Unnamed: 0'])
#                         #Estado.to_csv(path[0] + 'Brasil_Graduados_60.csv')   
                   
#     return Estado
# --------------------------------------------------------------------------------
def Filtro_Idade_Gen(path, name, idade, sx):
    # csv_estado = os.path.join(path[0],name[0]) # arquivo do censo do Brasil inteiro (somente graduados)
    # Estado = pd.read_csv(csv_estado)
    # # print(path[0])
    if sx == "M":
         logging.info(" Gerando o filtro de idade Masculino")   
         csv_estado = os.path.join(path[0],name[3]) # arquivo do censo do Brasil inteiro - Masculinos(somente graduados)
         Estado = pd.read_csv(csv_estado)
         if idade == "29":
            # Novo Filtro
            Estado.drop(Estado[(Estado['Idade_em_Anos'] >29)].index, inplace=True)
            #print("")
            Estado = Estado.reset_index(drop=True)
            Estado = Estado.drop(columns=['Unnamed: 0'])
            #Estado.to_csv(path[0] + 'Brasil_Graduados_29.csv')
         else: 
                if idade == "30-39":  
                    # Novo Filtro
                    Estado.drop(Estado[(Estado['Idade_em_Anos'] <=30)].index, inplace=True)
                    Estado.drop(Estado[(Estado['Idade_em_Anos'] >=39)].index, inplace=True)
                    Estado = Estado.reset_index(drop=True)
                    Estado = Estado.drop(columns=['Unnamed: 0'])
                    #Estado.to_csv(path[0] + 'Brasil_Graduados_30_39.csv')
                else:   
                    if idade == "40-49":  
                            # Novo Filtro
                            Estado.drop(Estado[(Estado['Idade_em_Anos'] <=40)].index, inplace=True)
                            Estado.drop(Estado[(Estado['Idade_em_Anos'] >=49)].index, inplace=True)                
                            Estado = Estado.reset_index(drop=True)
                            Estado = Estado.drop(columns=['Unnamed: 0'])
                            #Estado.to_csv(path[0] + 'Brasil_Graduados_40_49.csv')  
                    else:
                        if idade == "50-59":  
                                # Novo Filtro
                                Estado.drop(Estado[(Estado['Idade_em_Anos'] <=50)].index, inplace=True)
                                Estado.drop(Estado[(Estado['Idade_em_Anos'] >=59)].index, inplace=True)         
                                Estado = Estado.reset_index(drop=True)
                                Estado = Estado.drop(columns=['Unnamed: 0'])
                                #Estado.to_csv(path[0] + 'Brasil_Graduados_50_59.csv') 
                        else: 
                                if idade == "60":  
                                    # Novo Filtro
                                    Estado.drop(Estado[(Estado['Idade_em_Anos'] <=60)].index, inplace=True)
                                    Estado = Estado.reset_index(drop=True)
                                    Estado = Estado.drop(columns=['Unnamed: 0'])
                                    #Estado.to_csv(path[0] + 'Brasil_Graduados_60.csv')     
    else: 
         if sx == "F": 
            logging.info(" Gerando o filtro de idade Feminino")
            csv_estado = os.path.join(path[0],name[2]) # arquivo do censo do Brasil inteiro - Femininos(somente graduados)
            Estado = pd.read_csv(csv_estado)
            if idade == "29":
                # Novo Filtro
                Estado.drop(Estado[(Estado['Idade_em_Anos'] >29)].index, inplace=True)
                #print("")
                Estado = Estado.reset_index(drop=True)
                Estado = Estado.drop(columns=['Unnamed: 0'])
                #Estado.to_csv(path[0] + 'Brasil_Graduados_29.csv')
            else: 
                if idade == "30-39":  
                    # Novo Filtro
                    Estado.drop(Estado[(Estado['Idade_em_Anos'] <=30)].index, inplace=True)
                    Estado.drop(Estado[(Estado['Idade_em_Anos'] >=39)].index, inplace=True)
                    Estado = Estado.reset_index(drop=True)
                    Estado = Estado.drop(columns=['Unnamed: 0'])
                    #Estado.to_csv(path[0] + 'Brasil_Graduados_30_39.csv') 
                else:   
                    if idade == "40-49":  
                            # Novo Filtro
                            Estado.drop(Estado[(Estado['Idade_em_Anos'] <=40)].index, inplace=True)
                            Estado.drop(Estado[(Estado['Idade_em_Anos'] >=49)].index, inplace=True)                
                            Estado = Estado.reset_index(drop=True)
                            Estado = Estado.drop(columns=['Unnamed: 0'])
                            #Estado.to_csv(path[0] + 'Brasil_Graduados_40_49.csv') 
                    else:
                        if idade == "50-59":  
                                # Novo Filtro
                                Estado.drop(Estado[(Estado['Idade_em_Anos'] <=50)].index, inplace=True)
                                Estado.drop(Estado[(Estado['Idade_em_Anos'] >=59)].index, inplace=True)         
                                Estado = Estado.reset_index(drop=True)
                                Estado = Estado.drop(columns=['Unnamed: 0'])
                                #Estado.to_csv(path[0] + 'Brasil_Graduados_50_59.csv') 
                        else: 
                                if idade == "60":  
                                    # Novo Filtro
                                    Estado.drop(Estado[(Estado['Idade_em_Anos'] <=60)].index, inplace=True)
                                    Estado = Estado.reset_index(drop=True)
                                    Estado = Estado.drop(columns=['Unnamed: 0'])
                                    #Estado.to_csv(path[0] + 'Brasil_Graduados_60.csv')   
                    
    return Estado

def Ida_Volta_Idade_Gen(df,path1,name1,idade, sx):   
    
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
    if sx == "M": 
       name2 = ibge_variable.names(8) 
       csv_PivotTableFinal =  os.path.join(path2[0],name2[0]) #Pivo Table Final      
    else:
        if sx == "F":
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
                #print("============================================================================================================================================")


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
    if sx == "M":
        if idade == '29':
            df.to_csv(save_results_to + '100Porcent_DF_29_F.csv')
        if idade == '30-39':
            df.to_csv(save_results_to + '100Porcent_DF_30-39_F.csv')    
        if idade == '40-49':
            df.to_csv(save_results_to + '100Porcent_DF_40-49_F.csv')  
        if idade == '50-59':
            df.to_csv(save_results_to + '100Porcent_DF_50-59_F.csv') 
        if idade == '60':
            df.to_csv(save_results_to + '100Porcent_DF_60_F.csv')     
    else:
        if sx == "F":
            if idade == '29':
                df.to_csv(save_results_to + '100Porcent_DF_29_M.csv')
            if idade == '30-39':
                df.to_csv(save_results_to + '100Porcent_DF_30-39_M.csv')
            if idade == '40-49':    
                df.to_csv(save_results_to + '100Porcent_DF_40-49_M.csv')
            if idade == '50-59':    
                df.to_csv(save_results_to + '100Porcent_DF_50-59_M.csv')
            if idade == '60':
                df.to_csv(save_results_to + '100Porcent_DF_60_M.csv')            
    return

# --------------------------------------------------------------------------------
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
                #print("============================================================================================================================================")


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
    if idade == '30-39':
       df.to_csv(save_results_to + '100Porcent_DF_30-39.csv')    
    if idade == '40-49':
       df.to_csv(save_results_to + '100Porcent_DF_40-49.csv')  
    if idade == '50-59':
       df.to_csv(save_results_to + '100Porcent_DF_50-59.csv') 
    if idade == '60':
       df.to_csv(save_results_to + '100Porcent_DF_60.csv')       
    return

def JuntaTabelas(Original,Masc,Fem):

    save_results_to = 'graficos/'  
    df_row = pd.concat([Original, Masc, Fem])
    # print(df_row)
    df_row = pd.concat([Original, Masc, Fem], ignore_index=True)
    df_row1 = df_row.sort_values(["Curso", "Cbo"], ascending=True)
    # print(df_row1)
    # df_row2 = df_row1.sort_values(["Curso", "Cbo"], ascending=True)
    # print(df_row2)
    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)
    # print(df_row2)
    df_row1.to_csv(save_results_to +'Tabela_Orig_Masc_Fem_10Porcento.csv')  
    return

def Ida_Volta_Masculino_Feminino_100(df,path1,name1,sx):

    # if sx == 'F':
       # logging.info(" Gerando as idas e voltas Femininas")   
       # csv_estado = os.path.join(path[0],name[2]) # arquivo do censo do Brasil inteiro (somente graduados)
    # if sx == 'M':
       # logging.info(" Gerando as idas e voltas Masculinas")   
       # csv_estado = os.path.join(path[0],name[3]) # arquivo do censo do Brasil inteiro (somente graduados)       
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
        #primeirosCbos,primeirosCbos_Nome,Porcentagens,CURSO_NUM,CURSO_NOME=ibge_functions_descriptive_analysis.CBOs_Curso_v6(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0.1,save_results_to)
        primeirosCbos,primeirosCbos_Nome,Porcentagens,CURSO_NUM,CURSO_NOME=CBOs_Curso_v6_sn2(df,csv_CBO,curso_num,curso_nome,titulo10,titulo3,1)
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
                    #CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=ibge_functions_descriptive_analysis.Cursos_CBO_14_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.1)
                    CBO,Curso,tresprimeirosCursos,intensidade,fig,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_14_10_sn(df,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],curso_num,curso_nome,primeirosCbos_Nome,i,1)
                    Intensidade.append(intensidade)
                    # print(intensidade)
                    Porcentagens_vol.append(porcentagens_vol)
                    CBO_vol.append(CBO)
                    Cursos_vol.append(cursos_vol)
                    Nomes_vol.append(nomes_vol)
                else:
                    print(primeirosCbos[i])
                    #CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=ibge_functions_descriptive_analysis.Cursos_CBO_13_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],Graduados_Nao[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.1,save_results_to)
                    CBO,Curso,tresprimeirosCursos,intensidade,fig,cursos_vol, nomes_vol, porcentagens_vol=Cursos_CBO_13_10_sn(df,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],Graduados_Nao[i],curso_num,curso_nome,primeirosCbos_Nome,i,1)
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
       # df['CR'] = pd.to_numeric(df['CR'])
       # df['CR'] = df['CR'].astype(float)
       # df['CR'] = df['CR'].values.astype(int)
       df.to_csv(save_results_to + '100Porcent_DF_Fem.csv')
    if sx == 'M':
       # df['CR'] = pd.to_numeric(df['CR'])
       # df['CR'] = df['CR'].astype(float)
       # df['CR'] = df['CR'].values.astype(int)
       df.to_csv(save_results_to + '100Porcent_DF_Masc.csv')
    return  

def Tabela_Ida_Volta_Masculino_Feminino_100(path2,name2,sx):

    if sx == 'F':
       logging.info(" Gerando a Tabela de idas e voltas Femininas")   
       df =  os.path.join(path2[0],name2[8])
       df1 = pd.read_csv(df)  
    if sx == 'M':
       logging.info(" Gerando a Tabela de idas e voltas Masculinas")   
       df =  os.path.join(path2[0],name2[9])
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
    #df1['CR'] = pd.to_numeric(df1['CR'])
    #df1['CR'] = df1['CR'].values.astype(np.int64)


    # Salvar_Tabela
    # df1.to_csv(save_results_to + '10Porcent_DF_Limpo.csv')
    # df1.to_excel(save_results_to + '10Porcent_DF_Limpo.xlsx')
    if sx == 'F':
       # df.to_csv(save_results_to + '10Porcent_DF_Fem.csv')
       # Transformar as colunas( Cluster, Curso e Cbo) para inteiro ...
       # df1['CR'] = df1['CR'].astype(float)
       # df1['CR'] = df1['CR'].values.astype(int)
       df1.to_csv(save_results_to + '100Porcent_DF_Fem_Limpo.csv')
       df1.to_excel(save_results_to + '100Porcent_DF_Fem_Limpo.xlsx')
    if sx == 'M':
       # df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')
       # df1['CR'] = df1['CR'].astype(float)
       # df1['CR'] = df1['CR'].values.astype(int)
       df1.to_csv(save_results_to + '100Porcent_DF_Masc_Limpo.csv')
       df1.to_excel(save_results_to + '100Porcent_DF_Masc_Limpo.xlsx')
    return   


# def Profissoes_Cursos_Masculino_Feminino_100(path1,name1,path2,name2,sx): 
#     # Leitura
#     if sx == 'F':
#        logging.info(" Gerando o gráfico de profissões e cursos Femininos")   
#        df =  os.path.join(path2[0],name2[10])
#        X = pd.read_csv(df)    
#        X = X.drop(columns=['Unnamed: 0'])
#        X = X.drop(columns=['Unnamed: 0.1'])  
#     if sx == 'M':
#        logging.info(" Gerando o gráfico de profissões e cursos Masculinos")   
#        df =  os.path.join(path2[0],name2[11])
#        X = pd.read_csv(df)    
#        X = X.drop(columns=['Unnamed: 0'])
#        X = X.drop(columns=['Unnamed: 0.1'])
#     save_results_to = 'graficos/'   
#     # Remoção de Features 
#     X = X.drop(columns=['CB'])
#     X = X.drop(columns=['CR'])
#     CursosCenso = ibge_functions_descriptive_analysis.ibge_cursos_filter(path1[0],name1[2])
#     csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
#     CBO = pd.read_csv(csv_CBO)
#     # Plotagem dos Dados Originais
#     # print(X.iloc[:,0])
#     plt.figure(figsize=(6, 4))
#     # plt.title("10%  - Todos os Cursos - Clusterização ")
#     plt.xlabel('Ida')
#     plt.ylabel('Volta')
#     plt.ylim(0, 100) # definir limite do eixo
#     plt.xlim(0, 100) # definir limite do eixo
#     plt.grid()
#     plt.scatter(X.iloc[:,0],X.iloc[:,1],marker = '*')
#     # plt.show()
#     # string = "10%  - Todos os Cursos - Dados Originais " +".pdf"
#     # save_results_to = 'graficos/'  
#     # plt.savefig(save_results_to + string) 
#     if sx == 'F':
#        plt.title("100%  - Cursos e Profissões - Femininos ")
#        string = "100%  - Todos os Cursos - Dados Originais Femininos" +".pdf"
#        save_results_to = 'graficos/'  
#        plt.savefig(save_results_to + string) 
#     if sx == 'M':
#        plt.title("100%  - Cursos e Profissões - Masculinos ")
#        string = "100%  - Todos os Cursos - Dados Originais Masculinos" +".pdf"
#        save_results_to = 'graficos/'  
#        plt.savefig(save_results_to + string)      
#     return

def PlotOriginal_AdicionaColunaGenero_100(path1,name1,path2,name2,G):
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
           df =  os.path.join(path2[0],name2[10])
           X = pd.read_csv(df)    
           X = X.drop(columns=['Unnamed: 0'])
           X = X.drop(columns=['Unnamed: 0.1'])
        else:
            if G == 'M':
               logging.info(" Adicionando a coluna Gênero ao arquivo masculino")   
               df =  os.path.join(path2[0],name2[11])
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
       # X.to_csv(save_results_to +'Resultados_T_Original.csv')  
       return X
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
            # Resultados_T.to_csv(save_results_to +'Resultados_T_Fem.csv')   
            return Resultados_T          
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
                # Resultados_T.to_csv(save_results_to +'Resultados_T_Masc.csv')   
                return Resultados_T            
    return 


def Juntar_10Porcento_Genero(path1,name1, path2,name2):
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)
    path2 = ibge_variable.paths(13)
    name2 = ibge_variable.names(9)
    Porcent_DF_Limpo =       PlotOriginal_AdicionaColunaGenero_100(path1,name1,path2,name2,'O') # name2[2]/[7]
    Porcent_DF_Fem_Limpo  =  PlotOriginal_AdicionaColunaGenero_100(path1,name1,path2,name2,'F') # name2[5]
    Porcent_DF_Masc_Limpo =  PlotOriginal_AdicionaColunaGenero_100(path1,name1,path2,name2,'M') # name2[6]
    save_results_to = 'graficos/'  
     
    df_limpo = Porcent_DF_Limpo
    df_fem_limpo = Porcent_DF_Fem_Limpo
    df_masc_limpo = Porcent_DF_Masc_Limpo  

    df_row = pd.concat([df_limpo, df_fem_limpo, df_masc_limpo], ignore_index=True)
    df_row1 = df_row.sort_values(["Curso", "Cbo"], ascending=True)
    df_row2 = df_row1.sort_values(["Curso", "Cbo"], ascending=True)
    df_row2.to_csv(save_results_to + 'Resultados_T_Fem_Masc_Kmeans3_Genero.csv') 
    return    

def Filtrar_Tabela_10Porcento_Genero(): 
    path2 = ibge_variable.paths(13)
    name2 = ibge_variable.names(9)
    save_results_to = 'graficos/'  
    Kmeans3_T =  os.path.join(path2[0],name2[7])
    X = pd.read_csv(Kmeans3_T) 
    Resultados_T_Fem_Masc_Kmeans3_Genero =  os.path.join(path2[0],name2[12])
    df_row2 = pd.read_csv(Resultados_T_Fem_Masc_Kmeans3_Genero) 

    resultados_T=[]
    for j in range(len(df_row2)):
        for i in range(len(X)):        
            if (int(float(X['Curso'][i])) == int(float(df_row2['Curso'][j])))&(int(float(X['Cbo'][i])) == int(float(df_row2['Cbo'][j]))):
                tupla=(df_row2['Ida'][j],df_row2['Volta'][j],df_row2['Cluster'][j], df_row2['Curso'][j],df_row2['Curso_Nome'][j],df_row2['Cbo'][j],df_row2['Cbo_Nome'][j],df_row2['Genero'][j])
                resultados_T.append(tupla)
                # ...         
         
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
    Resultados_T.to_csv(save_results_to +'Resultados_T_Filtrados_Kmeans3_T.csv')   
    return

#https://colab.research.google.com/drive/1znpX4cXQTDgCsiZYS9kNl1UbgL3RudAB?authuser=1#scrollTo=mmz2Gysd900H
def Kmeans3_T_Grafico_Genero():
    path2 = ibge_variable.paths(13)
    name2 = ibge_variable.names(9)
    save_results_to = 'graficos/'
    df =  os.path.join(path2[0],name2[13])
    Resultados_T = pd.read_csv(df) 

    Resultados_T = Resultados_T.drop(columns=['Unnamed: 0'])
    # print(len(Resultados_T['Genero']))

    fem   = []
    masc  = []
    orig  = []
    for i in range(0, 150):
        if(str(Resultados_T['Genero'][i]) == 'F'):
            fem.append(Resultados_T['Ida'][i])
            fem.append(Resultados_T['Volta'][i])
        if(str(Resultados_T['Genero'][i]) == 'M'):
            masc.append(Resultados_T['Ida'][i])
            masc.append(Resultados_T['Volta'][i])
        if(str(Resultados_T['Genero'][i]) == 'O'):
            orig.append(Resultados_T['Ida'][i])
            orig.append(Resultados_T['Volta'][i])
    # print(len(fem))
    # print(len(masc))
    # print(len(orig))   

    i=0
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()


    while i<98:
        j = i+1
        #print(i)
        ax.scatter([orig[i], fem[i], masc[i]], [orig[j], fem[j], masc[j]], color=['black', 'pink', 'blue'])
        ax.annotate("", xy=(fem[i], fem[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='pink'))
        ax.annotate("", xy=(masc[i], masc[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='blue'))
        #print(fem[i],fem[j])
        #print(masc[i],masc[j])
        #print(orig[i],orig[j])
        #print("")
        i = i+2
    #plt.xlabel("Cursos")
    #plt.ylabel("Profissões")
    #plt.title("10%  -  Visualização dos três gráficos - Genero - Kmeans3")
    plt.xlabel("Courses")
    plt.ylabel("Professions")
    # plt.title("10% - View of the three graphs - Gender - Kmeans3")
    plt.xlim(0.0, 100.0)
    plt.ylim(0.0, 100.0)
    # plt.show()    
    #string1 = "10%  -  Visualização dos três gráficos - Genero - Kmeans3_" + ".pdf"
    string1 = "10% - View of the three graphs - Gender - Kmeans3_" + ".png"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string1)          
    return

def Tabela_Ida_Volta_Idade(path2,name2,id):

    if id == '29':
       logging.info(" Gerando a Tabela de idas e voltas idade 29")   
       df =  os.path.join(path2[0],name2[0])
       df1 = pd.read_csv(df)  
    if id == '30-39':
       logging.info(" Gerando a Tabela de idas e voltas idade 30-39")   
       df =  os.path.join(path2[0],name2[1])
       df1 = pd.read_csv(df)   
    if id == '40-49':
       logging.info(" Gerando a Tabela de idas e voltas idade 40-49")   
       df =  os.path.join(path2[0],name2[2])
       df1 = pd.read_csv(df)  
    if id == '50-59':
       logging.info(" Gerando a Tabela de idas e voltas idade 50-59")   
       df =  os.path.join(path2[0],name2[3])
       df1 = pd.read_csv(df)   
    if id == '60':
       logging.info(" Gerando a Tabela de idas e voltas idade 60")   
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
    if id == '29':
       # df.to_csv(save_results_to + '10Porcent_DF_Fem.csv')
       # Transformar as colunas( Cluster, Curso e Cbo) para inteiro ...
       df1.to_csv(save_results_to + '100Porcent_DF_29_Limpo.csv')
       df1.to_excel(save_results_to + '100Porcent_DF_29_Limpo.xlsx')
    if id == '30-39':
       # df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')
       df1.to_csv(save_results_to + '100Porcent_DF_30-39_Limpo.csv')
       df1.to_excel(save_results_to + '100Porcent_DF_30-39_Limpo.xlsx')
    if id == '40-49':
       # df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')
       df1.to_csv(save_results_to + '100Porcent_DF_40-49_Limpo.csv')
       df1.to_excel(save_results_to + '100Porcent_DF_40-49_Limpo.xlsx') 
    if id == '50-59':
       # df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')
       df1.to_csv(save_results_to + '100Porcent_DF_50-59_Limpo.csv')
       df1.to_excel(save_results_to + '100Porcent_DF_50-59_Limpo.xlsx')  
    if id == '60':
       # df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')
       df1.to_csv(save_results_to + '100Porcent_DF_60_Limpo.csv')
       df1.to_excel(save_results_to + '100Porcent_DF_60_Limpo.xlsx')         
    return   
#----------------------------------------------------------------------------------------
#def Tabela_Ida_Volta_Idade_Gen(path2,name2,id):
def Tabela_Ida_Volta_Idade_Gen(id,sx):

    if sx =='F':   
        if id == '29':
            logging.info(" Gerando a Tabela de idas e voltas idade 29")   
            df =  os.path.join('graficos/','100Porcent_DF_29_F.csv')
            df1 = pd.read_csv(df)  
        if id == '30-39':
            logging.info(" Gerando a Tabela de idas e voltas idade 30-39")   
            df =  os.path.join('graficos/','100Porcent_DF_30-39_F.csv')
            df1 = pd.read_csv(df)   
        if id == '40-49':
            logging.info(" Gerando a Tabela de idas e voltas idade 40-49")   
            df =  os.path.join('graficos/','100Porcent_DF_40-49_F.csv')
            df1 = pd.read_csv(df)  
        if id == '50-59':
            logging.info(" Gerando a Tabela de idas e voltas idade 50-59")   
            df =  os.path.join('graficos/','100Porcent_DF_50-59_F.csv')
            df1 = pd.read_csv(df)   
        if id == '60':
            logging.info(" Gerando a Tabela de idas e voltas idade 60")   
            df =  os.path.join('graficos/' ,'100Porcent_DF_60_F.csv')
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
        if id == '29':
        # df.to_csv(save_results_to + '10Porcent_DF_Fem.csv')
        # Transformar as colunas( Cluster, Curso e Cbo) para inteiro ...
            df1.to_csv(save_results_to + '100Porcent_DF_29_Limpo_F.csv')
            df1.to_excel(save_results_to + '100Porcent_DF_29_Limpo_F.xlsx')
        if id == '30-39':
        # df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')
            df1.to_csv(save_results_to + '100Porcent_DF_30-39_Limpo_F.csv')
            df1.to_excel(save_results_to + '100Porcent_DF_30-39_Limpo_F.xlsx')
        if id == '40-49':
        # df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')
            df1.to_csv(save_results_to + '100Porcent_DF_40-49_Limpo_F.csv')
            df1.to_excel(save_results_to + '100Porcent_DF_40-49_Limpo_F.xlsx') 
        if id == '50-59':
        # df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')
            df1.to_csv(save_results_to + '100Porcent_DF_50-59_Limpo_F.csv')
            df1.to_excel(save_results_to + '100Porcent_DF_50-59_Limpo_F.xlsx')  
        if id == '60':
        # df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')
            df1.to_csv(save_results_to + '100Porcent_DF_60_Limpo_F.csv')
            df1.to_excel(save_results_to + '100Porcent_DF_60_Limpo_F.xlsx')     
    else:
        if sx=='M':
           if id == '29':
                logging.info(" Gerando a Tabela de idas e voltas idade 29")   
                df =  os.path.join('graficos/','100Porcent_DF_29_M.csv')
                df1 = pd.read_csv(df)  
           if id == '30-39':
                logging.info(" Gerando a Tabela de idas e voltas idade 30-39")   
                df =  os.path.join('graficos/','100Porcent_DF_30-39_M.csv')
                df1 = pd.read_csv(df)   
           if id == '40-49':
                logging.info(" Gerando a Tabela de idas e voltas idade 40-49")   
                df =  os.path.join('graficos/','100Porcent_DF_40-49_M.csv')
                df1 = pd.read_csv(df)  
           if id == '50-59':
                logging.info(" Gerando a Tabela de idas e voltas idade 50-59")   
                df =  os.path.join('graficos/','100Porcent_DF_50-59_M.csv')
                df1 = pd.read_csv(df)   
           if id == '60':
                logging.info(" Gerando a Tabela de idas e voltas idade 60")   
                df =  os.path.join('graficos/' ,'100Porcent_DF_60_M.csv')
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
           if id == '29':
                # df.to_csv(save_results_to + '10Porcent_DF_Fem.csv')
                # Transformar as colunas( Cluster, Curso e Cbo) para inteiro ...
                df1.to_csv(save_results_to + '100Porcent_DF_29_Limpo_M.csv')
                df1.to_excel(save_results_to + '100Porcent_DF_29_Limpo_M.xlsx')
           if id == '30-39':
                # df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')
                df1.to_csv(save_results_to + '100Porcent_DF_30-39_Limpo_M.csv')
                df1.to_excel(save_results_to + '100Porcent_DF_30-39_Limpo_M.xlsx')
           if id == '40-49':
                # df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')
                df1.to_csv(save_results_to + '100Porcent_DF_40-49_Limpo_M.csv')
                df1.to_excel(save_results_to + '100Porcent_DF_40-49_Limpo_M.xlsx') 
           if id == '50-59':
               # df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')
                df1.to_csv(save_results_to + '100Porcent_DF_50-59_Limpo_M.csv')
                df1.to_excel(save_results_to + '100Porcent_DF_50-59_Limpo_M.xlsx')  
           if id == '60':
                # df.to_csv(save_results_to + '10Porcent_DF_Masc.csv')
                df1.to_csv(save_results_to + '100Porcent_DF_60_Limpo_M.csv')
                df1.to_excel(save_results_to + '100Porcent_DF_60_Limpo_M.xlsx')    
    return   

def Adiciona_Coluna_Idade_Gen(path1,name1,path2,name2,name3,id, sx):
    if sx=='F':
        # Leitura do arquivo df original, masculino ou feminino
        if id == 'O':
            logging.info(" Adicionando a coluna Idade ao arquivo original")   
            # df =  os.path.join(path2[0],name2[2])
            df =  os.path.join('graficos/','Kmeans3_T.csv')
            X = pd.read_csv(df)    
            # X = X.drop(columns=['Unnamed: 0'])
            # X = X.drop(columns=['Unnamed: 0.1'])
        else:
            if id == '29':
                logging.info(" Adicionando a coluna Idade ao arquivo Idade 29")   
                # df =  os.path.join(path2[0],name2[2])
                df =  os.path.join('graficos/','100Porcent_DF_29_Limpo_F.csv')
                X = pd.read_csv(df)    
                # X = X.drop(columns=['Unnamed: 0'])
                # X = X.drop(columns=['Unnamed: 0.1'])
            else:
                if id == '30-39':
                    logging.info(" Adicionando a coluna Idade ao arquivo Idade 30-39")   
                    df =  os.path.join('graficos/','100Porcent_DF_30-39_Limpo_F.csv')
                    X = pd.read_csv(df)    
                    X = X.drop(columns=['Unnamed: 0'])
                    # X = X.drop(columns=['Unnamed: 0.1'])
                else:
                    if id == '40-49':
                        logging.info(" Adicionando a coluna Idade ao arquivo Idade 40-49")   
                        df =  os.path.join('graficos/','100Porcent_DF_40-49_Limpo_F.csv')
                        X = pd.read_csv(df)    
                        X = X.drop(columns=['Unnamed: 0'])
                        # X = X.drop(columns=['Unnamed: 0.1'])
                    else: 
                        if id == '50-59':
                            logging.info(" Adicionando a coluna Idade ao arquivo Idade 50-59")   
                            df =  os.path.join('graficos/','100Porcent_DF_50-59_Limpo_F.csv')
                            X = pd.read_csv(df)    
                            X = X.drop(columns=['Unnamed: 0'])
                            # X = X.drop(columns=['Unnamed: 0.1'])  
                        else: 
                            if id == '60':
                                logging.info(" Adicionando a coluna Idade ao arquivo Idade 60")   
                                df =  os.path.join('graficos/','100Porcent_DF_60_Limpo_F.csv')
                                X = pd.read_csv(df)    
                                X = X.drop(columns=['Unnamed: 0'])
                                # X = X.drop(columns=['Unnamed: 0.1'])  
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
        # x= X['Ida']
        # y= X['Volta']
        # plt.xlabel("Cursos")
        # plt.ylabel("Profissões")
        # plt.title("10%  - Cursos e Profissões do Censo_" + G)
        # plt.ylim(0, 100) # definir limite do eixo
        # plt.xlim(0, 100) # definir limite do eixo
        # plt.grid()
        # plt.scatter(x,y,marker = '*')
        # string1 = "10%  - Cursos e Profissões do Censo_" + G + ".pdf"
        # save_results_to = 'graficos/'  
        # plt.savefig(save_results_to + string1)  
        # Leitura do arquivo df original, masculino ou feminino
        if id == 'O':
            X['Idade'] = "O"    
            # X.to_csv(save_results_to +'Resultados_T_Original_Idade.csv')  
            return X
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
            if id == '29':
                # Adicionando coluna
                resultados_T=[]
                cluster=""
                # X['Cluster'][i]
                for i in range(len(X['CR'])):
                    tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"29")
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
                        7:"Idade"
                }
                Resultados_T.rename(columns=dict,inplace=True)   
                # Resultados_T.to_csv(save_results_to +'Resultados_T_29.csv')   
                return Resultados_T          
            else:
                if id == '30-39':
                    # Adicionando coluna
                    resultados_T=[]
                    cluster=""
                    # X['Cluster'][i]
                    for i in range(len(X['CR'])):
                        tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"30-39")
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
                            7:"Idade"
                    }
                    Resultados_T.rename(columns=dict,inplace=True)   
                    # Resultados_T.to_csv(save_results_to +'Resultados_T_30_39.csv')   
                    return Resultados_T      
                else:  
                    if id == '40-49':
                        # Adicionando coluna
                        resultados_T=[]
                        cluster=""
                        # X['Cluster'][i]
                        for i in range(len(X['CR'])):
                            tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"40-49")
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
                                7:"Idade"
                        }
                        Resultados_T.rename(columns=dict,inplace=True)   
                        # Resultados_T.to_csv(save_results_to +'Resultados_T_40_49.csv')   
                        return Resultados_T   
                    else:
                            if id == '50-59':
                                # Adicionando coluna
                                resultados_T=[]
                                cluster=""
                                # X['Cluster'][i]
                                for i in range(len(X['CR'])):
                                    tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"50-59")
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
                                        7:"Idade"
                                }
                                Resultados_T.rename(columns=dict,inplace=True)   
                                # Resultados_T.to_csv(save_results_to +'Resultados_T_50_59.csv')   
                                return Resultados_T 
                            else:  
                                if id == '60':
                                    # Adicionando coluna
                                    resultados_T=[]
                                    cluster=""
                                    # X['Cluster'][i]
                                    for i in range(len(X['CR'])):
                                        tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"60")
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
                                            7:"Idade"
                                    }
                                    Resultados_T.rename(columns=dict,inplace=True)   
                                    # Resultados_T.to_csv(save_results_to +'Resultados_T_60.csv')   
                                    return Resultados_T 

    if sx=='M':
        # Leitura do arquivo df original, masculino ou feminino
        if id == 'O':
            logging.info(" Adicionando a coluna Idade ao arquivo original")   
            # df =  os.path.join(path2[0],name2[2])
            df =  os.path.join('graficos/','Kmeans3_T.csv')
            X = pd.read_csv(df)    
            # X = X.drop(columns=['Unnamed: 0'])
            # X = X.drop(columns=['Unnamed: 0.1'])
        else:
            if id == '29':
                logging.info(" Adicionando a coluna Idade ao arquivo Idade 29")   
                # df =  os.path.join(path2[0],name2[2])
                df =  os.path.join('graficos/','100Porcent_DF_29_Limpo_M.csv')
                X = pd.read_csv(df)    
                # X = X.drop(columns=['Unnamed: 0'])
                # X = X.drop(columns=['Unnamed: 0.1'])
            else:
                if id == '30-39':
                    logging.info(" Adicionando a coluna Idade ao arquivo Idade 30-39")   
                    df =  os.path.join('graficos/','100Porcent_DF_30-39_Limpo_M.csv')
                    X = pd.read_csv(df)    
                    X = X.drop(columns=['Unnamed: 0'])
                    # X = X.drop(columns=['Unnamed: 0.1'])
                else:
                    if id == '40-49':
                        logging.info(" Adicionando a coluna Idade ao arquivo Idade 40-49")   
                        df =  os.path.join('graficos/','100Porcent_DF_40-49_Limpo_M.csv')
                        X = pd.read_csv(df)    
                        X = X.drop(columns=['Unnamed: 0'])
                        # X = X.drop(columns=['Unnamed: 0.1'])
                    else: 
                        if id == '50-59':
                            logging.info(" Adicionando a coluna Idade ao arquivo Idade 50-59")   
                            df =  os.path.join('graficos/','100Porcent_DF_50-59_Limpo_M.csv')
                            X = pd.read_csv(df)    
                            X = X.drop(columns=['Unnamed: 0'])
                            # X = X.drop(columns=['Unnamed: 0.1'])  
                        else: 
                            if id == '60':
                                logging.info(" Adicionando a coluna Idade ao arquivo Idade 60")   
                                df =  os.path.join('graficos/','100Porcent_DF_60_Limpo_M.csv')
                                X = pd.read_csv(df)    
                                X = X.drop(columns=['Unnamed: 0'])
                                # X = X.drop(columns=['Unnamed: 0.1'])  
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
        # x= X['Ida']
        # y= X['Volta']
        # plt.xlabel("Cursos")
        # plt.ylabel("Profissões")
        # plt.title("10%  - Cursos e Profissões do Censo_" + G)
        # plt.ylim(0, 100) # definir limite do eixo
        # plt.xlim(0, 100) # definir limite do eixo
        # plt.grid()
        # plt.scatter(x,y,marker = '*')
        # string1 = "10%  - Cursos e Profissões do Censo_" + G + ".pdf"
        # save_results_to = 'graficos/'  
        # plt.savefig(save_results_to + string1)  
        # Leitura do arquivo df original, masculino ou feminino
        if id == 'O':
            X['Idade'] = "O"    
            # X.to_csv(save_results_to +'Resultados_T_Original_Idade.csv')  
            return X
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
            if id == '29':
                # Adicionando coluna
                resultados_T=[]
                cluster=""
                # X['Cluster'][i]
                for i in range(len(X['CR'])):
                    tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"29")
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
                        7:"Idade"
                }
                Resultados_T.rename(columns=dict,inplace=True)   
                # Resultados_T.to_csv(save_results_to +'Resultados_T_29.csv')   
                return Resultados_T          
            else:
                if id == '30-39':
                    # Adicionando coluna
                    resultados_T=[]
                    cluster=""
                    # X['Cluster'][i]
                    for i in range(len(X['CR'])):
                        tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"30-39")
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
                            7:"Idade"
                    }
                    Resultados_T.rename(columns=dict,inplace=True)   
                    # Resultados_T.to_csv(save_results_to +'Resultados_T_30_39.csv')   
                    return Resultados_T      
                else:  
                    if id == '40-49':
                        # Adicionando coluna
                        resultados_T=[]
                        cluster=""
                        # X['Cluster'][i]
                        for i in range(len(X['CR'])):
                            tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"40-49")
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
                                7:"Idade"
                        }
                        Resultados_T.rename(columns=dict,inplace=True)   
                        # Resultados_T.to_csv(save_results_to +'Resultados_T_40_49.csv')   
                        return Resultados_T   
                    else:
                            if id == '50-59':
                                # Adicionando coluna
                                resultados_T=[]
                                cluster=""
                                # X['Cluster'][i]
                                for i in range(len(X['CR'])):
                                    tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"50-59")
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
                                        7:"Idade"
                                }
                                Resultados_T.rename(columns=dict,inplace=True)   
                                # Resultados_T.to_csv(save_results_to +'Resultados_T_50_59.csv')   
                                return Resultados_T 
                            else:  
                                if id == '60':
                                    # Adicionando coluna
                                    resultados_T=[]
                                    cluster=""
                                    # X['Cluster'][i]
                                    for i in range(len(X['CR'])):
                                        tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"60")
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
                                            7:"Idade"
                                    }
                                    Resultados_T.rename(columns=dict,inplace=True)   
                                    # Resultados_T.to_csv(save_results_to +'Resultados_T_60.csv')   
                                    return Resultados_T                             
                          
                           
    return 
def Juntar_10Porcento_Idade_Gen():
    # Feminino
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)
    path2 = ibge_variable.paths(13)
    name2 = ibge_variable.names(9)
    name3 = ibge_variable.names(10)
    Porcent_DF_Limpo_Idade = Adiciona_Coluna_Idade_Gen(path1,name1,path2,name2,name3,'O','F') 
    Porcent_DF_29_Limpo    = Adiciona_Coluna_Idade_Gen(path1,name1,path2,name2,name3,'29','F') 
    Porcent_DF_30_39_Limpo = Adiciona_Coluna_Idade_Gen(path1,name1,path2,name2,name3,'30-39','F') 
    Porcent_DF_40_49_Limpo = Adiciona_Coluna_Idade_Gen(path1,name1,path2,name2,name3,'40-49','F')  
    Porcent_DF_50_59_Limpo = Adiciona_Coluna_Idade_Gen(path1,name1,path2,name2,name3,'50-59','F') 
    Porcent_DF_60_Limpo    = Adiciona_Coluna_Idade_Gen(path1,name1,path2,name2,name3,'60','F') 
    save_results_to = 'graficos/'  
     
    df_limpo = Porcent_DF_Limpo_Idade
    df_29_limpo = Porcent_DF_29_Limpo
    df_30_39_limpo = Porcent_DF_30_39_Limpo  
    df_40_49_limpo = Porcent_DF_40_49_Limpo
    df_50_59_limpo = Porcent_DF_50_59_Limpo
    df_60_limpo = Porcent_DF_60_Limpo


    df_row = pd.concat([df_limpo, df_29_limpo,df_30_39_limpo, df_40_49_limpo,df_50_59_limpo,df_60_limpo], ignore_index=True)
    df_row1 = df_row.sort_values(["Curso", "Cbo"], ascending=True)
    df_row2 = df_row1.sort_values(["Curso", "Cbo"], ascending=True)
    df_row2.to_csv(save_results_to + 'Resultados_T_29_30-39_40-49_50-59_60Kmeans3_Idade_F.csv')   

    # Masculino
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)
    path2 = ibge_variable.paths(13)
    name2 = ibge_variable.names(9)
    name3 = ibge_variable.names(10)
    Porcent_DF_Limpo_Idade = Adiciona_Coluna_Idade_Gen(path1,name1,path2,name2,name3,'O','M') 
    Porcent_DF_29_Limpo    = Adiciona_Coluna_Idade_Gen(path1,name1,path2,name2,name3,'29','M') 
    Porcent_DF_30_39_Limpo = Adiciona_Coluna_Idade_Gen(path1,name1,path2,name2,name3,'30-39','M') 
    Porcent_DF_40_49_Limpo = Adiciona_Coluna_Idade_Gen(path1,name1,path2,name2,name3,'40-49','M') 
    Porcent_DF_50_59_Limpo = Adiciona_Coluna_Idade_Gen(path1,name1,path2,name2,name3,'50-59','M') 
    Porcent_DF_60_Limpo    = Adiciona_Coluna_Idade_Gen(path1,name1,path2,name2,name3,'60','M') 
    save_results_to = 'graficos/'  
     
    df_limpo = Porcent_DF_Limpo_Idade
    df_29_limpo = Porcent_DF_29_Limpo
    df_30_39_limpo = Porcent_DF_30_39_Limpo  
    df_40_49_limpo = Porcent_DF_40_49_Limpo
    df_50_59_limpo = Porcent_DF_50_59_Limpo
    df_60_limpo = Porcent_DF_60_Limpo


    df_row = pd.concat([df_limpo, df_29_limpo,df_30_39_limpo, df_40_49_limpo,df_50_59_limpo,df_60_limpo], ignore_index=True)
    df_row1 = df_row.sort_values(["Curso", "Cbo"], ascending=True)
    df_row2 = df_row1.sort_values(["Curso", "Cbo"], ascending=True)
    df_row2.to_csv(save_results_to + 'Resultados_T_29_30-39_40-49_50-59_60Kmeans3_Idade_M.csv')   
    return

def Filtrar_Tabela_10Porcento_Idade_Gen(): 
    # Feminino
    path2 = ibge_variable.paths(13)
    name2 = ibge_variable.names(9)
    name3 = ibge_variable.names(10)
    save_results_to = 'graficos/'  
    Kmeans3_T =  os.path.join(path2[0],name2[7])
    X = pd.read_csv(Kmeans3_T) 
    Resultados_T_29_30_39_40_49_50_59_60Kmeans3_Idade =  os.path.join('graficos/','Resultados_T_29_30-39_40-49_50-59_60Kmeans3_Idade_F.csv')
    df_row2 = pd.read_csv(Resultados_T_29_30_39_40_49_50_59_60Kmeans3_Idade) 

    resultados_T=[]
    for j in range(len(df_row2)):
        if pd.isnull(df_row2['Cluster'][j]):
            df_row2['Cluster'][j] = ''   
        else:    
            df_row2['Cluster'][j] = int(float(df_row2['Cluster'][j]))  
        for i in range(len(X)):        
            if (int(float(X['Curso'][i])) == int(float(df_row2['Curso'][j]))) & (int(float(X['Cbo'][i])) == int(float(df_row2['Cbo'][j]))):
                tupla=(df_row2['Ida'][j],df_row2['Volta'][j],df_row2['Cluster'][j], df_row2['Curso'][j].astype(int),df_row2['Curso_Nome'][j],df_row2['Cbo'][j].astype(int),df_row2['Cbo_Nome'][j],df_row2['Idade'][j])
                resultados_T.append(tupla)
                # ...         
         
    Resultados_T= pd.DataFrame(resultados_T)
    #...
    dict = {0:"Ida",
            1:"Volta",
            2:"Cluster",
            3:"Curso",
            4:"Curso_Nome",
            5:"Cbo",
            6:"Cbo_Nome",
            7:"Idade"
            }
    Resultados_T.rename(columns=dict,inplace=True)   
    Resultados_T.to_csv(save_results_to +'Resultados_T_Filtrados_Kmeans3_Idade_F.csv')   

    # Masculino
    path2 = ibge_variable.paths(13)
    name2 = ibge_variable.names(9)
    name3 = ibge_variable.names(10)
    save_results_to = 'graficos/'  
    Kmeans3_T =  os.path.join(path2[0],name2[7])
    X = pd.read_csv(Kmeans3_T) 
    Resultados_T_29_30_39_40_49_50_59_60Kmeans3_Idade =  os.path.join('graficos/','Resultados_T_29_30-39_40-49_50-59_60Kmeans3_Idade_M.csv')
    df_row2 = pd.read_csv(Resultados_T_29_30_39_40_49_50_59_60Kmeans3_Idade) 

    resultados_T=[]
    for j in range(len(df_row2)):
        if pd.isnull(df_row2['Cluster'][j]):
            df_row2['Cluster'][j] = ''   
        else:    
            df_row2['Cluster'][j] = int(float(df_row2['Cluster'][j]))  
        for i in range(len(X)):        
            if (int(float(X['Curso'][i])) == int(float(df_row2['Curso'][j]))) & (int(float(X['Cbo'][i])) == int(float(df_row2['Cbo'][j]))):
                tupla=(df_row2['Ida'][j],df_row2['Volta'][j],df_row2['Cluster'][j], df_row2['Curso'][j].astype(int),df_row2['Curso_Nome'][j],df_row2['Cbo'][j].astype(int),df_row2['Cbo_Nome'][j],df_row2['Idade'][j])
                resultados_T.append(tupla)
                # ...         
         
    Resultados_T= pd.DataFrame(resultados_T)
    #...
    dict = {0:"Ida",
            1:"Volta",
            2:"Cluster",
            3:"Curso",
            4:"Curso_Nome",
            5:"Cbo",
            6:"Cbo_Nome",
            7:"Idade"
            }
    Resultados_T.rename(columns=dict,inplace=True)   
    Resultados_T.to_csv(save_results_to +'Resultados_T_Filtrados_Kmeans3_Idade_M.csv') 

    return
# https://colab.research.google.com/drive/1Oxj69ukEFJ-lxw09fqGi-k5ym1uKJoXP?authuser=1#scrollTo=AG_wj961fUbc
def Analise_Genero_FaixaEtaria(sx):
    if sx == 'M':
       import pandas as pd

       # df_row2 = pd.read_csv("/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/df_row2_Feminino.csv", sep=",")
       # df_row2 = df_row2.drop(columns=['Unnamed: 0'])
       # df_row2.drop(df_row2[(df_row2['Curso'] !=342)].index, inplace=True)
       # df_row2.drop(df_row2[(df_row2['Cbo'] !=1221)].index, inplace=True)
       # # df_row2.shape
       # df_row2 = df_row2.reset_index(drop=True)
       # # df_row2
       
       # csv_idade = "/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/Resultados_Idades.csv"
       # csv_idade = "/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/Resultados_Idades_Kmeans3_T_Idade.csv"
       # csv_idade = "/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/df_row2_Feminino.csv"
       # csv_idade = "/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/df_row2_Masculino.csv"
       csv_idade = "graficos/Resultados_T_Filtrados_Kmeans3_Idade_M.csv"
       # Curso = "212","724" "581" "380" #"344" #"342"  #"342"  #"321" #"214"  
       # CBO = "2354", "2261" "2161" #"2611" #"2411"  #"1221" #2431" #"2642"#"2166.0" 
       

       # Criando lista
       Curso = ["212",  "724",  "581",  "380",  "344",  "342",  "342",  "321"]#,  "214"]
       CBO =   ["2354", "2261", "2161", "2611", "2411", "1221", "2431", "2642"]#, "2166"]

       # Iterando
       # https://colab.research.google.com/drive/1Oxj69ukEFJ-lxw09fqGi-k5ym1uKJoXP?authuser=1#scrollTo=AG_wj961fUbc
       for i in range(len(Curso)):       
           Idade_Plot(csv_idade,CBO[i],Curso[i], sx)
       # Idade_Plot(csv_idade,CBO[0],Curso[0])
    if sx == 'F':    
       import pandas as pd

       # df_row2 = pd.read_csv("/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/df_row2_Feminino.csv", sep=",")
       # df_row2 = df_row2.drop(columns=['Unnamed: 0'])
       # df_row2.drop(df_row2[(df_row2['Curso'] !=342)].index, inplace=True)
       # df_row2.drop(df_row2[(df_row2['Cbo'] !=1221)].index, inplace=True)
       # # df_row2.shape
       # df_row2 = df_row2.reset_index(drop=True)
       # # df_row2
       
       # csv_idade = "/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/Resultados_Idades.csv"
       # csv_idade = "/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/Resultados_Idades_Kmeans3_T_Idade.csv"
       # csv_idade = "/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/df_row2_Feminino.csv"
       # csv_idade = "/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/df_row2_Masculino.csv"
       csv_idade = "graficos/Resultados_T_Filtrados_Kmeans3_Idade_F.csv"
       # Curso = "212","724" "581" "380" #"344" #"342"  #"342"  #"321" #"214"  
       # CBO = "2354", "2261" "2161" #"2611" #"2411"  #"1221" #2431" #"2642"#"2166.0" 
       

       # Criando lista
       Curso = ["212",  "724",  "581",  "380",  "344",  "342",  "342",  "321"]#,  "214"]
       CBO =   ["2354", "2261", "2161", "2611", "2411", "1221", "2431", "2642"]#, "2166"]

       # Iterando
       # https://colab.research.google.com/drive/1Oxj69ukEFJ-lxw09fqGi-k5ym1uKJoXP?authuser=1#scrollTo=AG_wj961fUbc
       for i in range(len(Curso)):       
           Idade_Plot(csv_idade,CBO[i],Curso[i], sx)
       # Idade_Plot(csv_idade,CBO[0],Curso[0])   
    return


def Idade_Plot(csv_idade,CBO,Curso,sx):
    import pandas as pd

    if sx == 'M':
        #Leitura de Arquivos CSVs ...
        X = pd.read_csv(csv_idade, sep=",")
        X = X.drop(columns=['Unnamed: 0'])
        #...

        I_25_29 = []
        I_30_39 = []
        I_40_49 = []
        I_50_59 = []
        I_60    = []
        #orig    = []


        for i in range (len(X['Curso'])):
            if (X['Curso'][i] == float(Curso) and X['Cbo'][i] == float(CBO)):
                if(X['Idade'][i] == "29"):
                    I_25_29.append(X['Ida'][i])
                    I_25_29.append(X['Volta'][i])
                if(X['Idade'][i] == "30-39"):
                    I_30_39.append(X['Ida'][i])
                    I_30_39.append(X['Volta'][i])
                if(X['Idade'][i] == "40-49"):
                    I_40_49.append(X['Ida'][i])
                    I_40_49.append(X['Volta'][i])
                if(X['Idade'][i] == "50-59"):
                    I_50_59.append(X['Ida'][i])
                    I_50_59.append(X['Volta'][i])
                if(X['Idade'][i] == "60"):
                    I_60.append(X['Ida'][i])
                    I_60.append(X['Volta'][i])
                #if(X['Idade'][i] == "O"):
                #    orig.append(X['Ida'][i])
                #    orig.append(X['Volta'][i]),'black'

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        # Se não tiver pessoas com 60 anos ...
        # ax.scatter([ I_25_29[0], I_30_39[0],I_40_49[0], I_50_59[0]], [ I_25_29[1], I_30_39[1],I_40_49[1], I_50_59[1]], color=['blue','magenta','Darkgreen','red'])
        # ...
        ax.scatter([ I_25_29[0], I_30_39[0],I_40_49[0], I_50_59[0], I_60[0]], [ I_25_29[1], I_30_39[1],I_40_49[1], I_50_59[1], I_60[1]], color=['blue','magenta','Darkgreen','red','black'])
        ax.annotate("", xy=(I_25_29[0], I_25_29[1]), xytext=(I_30_39[0], I_30_39[1]), arrowprops=dict(arrowstyle="<-", color='blue'))
        ax.annotate("", xy=(I_30_39[0], I_30_39[1]), xytext=(I_40_49[0], I_40_49[1]), arrowprops=dict(arrowstyle="<-", color='magenta'))
        ax.annotate("", xy=(I_40_49[0], I_40_49[1]), xytext=(I_50_59[0], I_50_59[1]), arrowprops=dict(arrowstyle="<-", color='Darkgreen'))
        ax.annotate("", xy=(I_50_59[0], I_50_59[1]), xytext=(I_60[0], I_60[1]), arrowprops=dict(arrowstyle="<-", color='red'))
        # ax.annotate("", xy=(I_60[0], I_60[1]), xytext=(I_60[0], I_60[1]), arrowprops=dict(arrowstyle="->", color='black'))



        # plt.xlabel("Cursos")
        # plt.ylabel("Profissões")
        # plt.title("Idade - Feminino -   212/2354")
        # plt.title("Idade - Feminino -   214/2166")
        # plt.title("Idade - Feminino -   321/2642")
        # plt.title("Idade - Feminino -   342/2431")
        # plt.title("Idade - Feminino -   344/2411")
        # plt.title("Idade - Feminino -   380/2611")
        # plt.title("Idade - Feminino -   581/2161")
        # plt.title("Idade - Feminino -   724/2261")
        # plt.legend(['blue','magenta','Darkgreen','red','black'])
        plt.xlim(0.0, 100.0)
        plt.ylim(0.0, 100.0)
        # plt.show()
        string1 = "Analise_Genero_FaixaEtaria_M" + "_" + Curso + "_" + CBO + ".png"
        save_results_to = 'graficos/'  
        plt.savefig(save_results_to + string1)  

    if sx == 'F':
        #Leitura de Arquivos CSVs ...
        X = pd.read_csv(csv_idade, sep=",")
        X = X.drop(columns=['Unnamed: 0'])
        #...

        I_25_29 = []
        I_30_39 = []
        I_40_49 = []
        I_50_59 = []
        I_60    = []
        #orig    = []


        for i in range (len(X['Curso'])):
            if (X['Curso'][i] == float(Curso) and X['Cbo'][i] == float(CBO)):
                if(X['Idade'][i] == "29"):
                    I_25_29.append(X['Ida'][i])
                    I_25_29.append(X['Volta'][i])
                if(X['Idade'][i] == "30-39"):
                    I_30_39.append(X['Ida'][i])
                    I_30_39.append(X['Volta'][i])
                if(X['Idade'][i] == "40-49"):
                    I_40_49.append(X['Ida'][i])
                    I_40_49.append(X['Volta'][i])
                if(X['Idade'][i] == "50-59"):
                    I_50_59.append(X['Ida'][i])
                    I_50_59.append(X['Volta'][i])
                if(X['Idade'][i] == "60"):
                    I_60.append(X['Ida'][i])
                    I_60.append(X['Volta'][i])
                #if(X['Idade'][i] == "O"):
                #    orig.append(X['Ida'][i])
                #    orig.append(X['Volta'][i]),'black'

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        # Se não tiver pessoas com 60 anos ...
        # ax.scatter([ I_25_29[0], I_30_39[0],I_40_49[0], I_50_59[0]], [ I_25_29[1], I_30_39[1],I_40_49[1], I_50_59[1]], color=['blue','magenta','Darkgreen','red'])
        # ...
        ax.scatter([ I_25_29[0], I_30_39[0],I_40_49[0], I_50_59[0], I_60[0]], [ I_25_29[1], I_30_39[1],I_40_49[1], I_50_59[1], I_60[1]], color=['blue','magenta','Darkgreen','red','black'])
        ax.annotate("", xy=(I_25_29[0], I_25_29[1]), xytext=(I_30_39[0], I_30_39[1]), arrowprops=dict(arrowstyle="<-", color='blue'))
        ax.annotate("", xy=(I_30_39[0], I_30_39[1]), xytext=(I_40_49[0], I_40_49[1]), arrowprops=dict(arrowstyle="<-", color='magenta'))
        ax.annotate("", xy=(I_40_49[0], I_40_49[1]), xytext=(I_50_59[0], I_50_59[1]), arrowprops=dict(arrowstyle="<-", color='Darkgreen'))
        ax.annotate("", xy=(I_50_59[0], I_50_59[1]), xytext=(I_60[0], I_60[1]), arrowprops=dict(arrowstyle="<-", color='red'))
        #ax.annotate("", xy=(I_60[0], I_60[1]), xytext=(I_60[0], I_60[1]), arrowprops=dict(arrowstyle="->", color='black'))



        # plt.xlabel("Cursos")
        # plt.ylabel("Profissões")
        # plt.title("Idade - Feminino -   212/2354")
        # plt.title("Idade - Feminino -   214/2166")
        # plt.title("Idade - Feminino -   321/2642")
        # plt.title("Idade - Feminino -   342/2431")
        # plt.title("Idade - Feminino -   344/2411")
        # plt.title("Idade - Feminino -   380/2611")
        # plt.title("Idade - Feminino -   581/2161")
        # plt.title("Idade - Feminino -   724/2261")
        # plt.legend(['blue','magenta','Darkgreen','red','black'])
        plt.xlim(0.0, 100.0)
        plt.ylim(0.0, 100.0)
        # plt.show()
        string1 = "Analise_Genero_FaixaEtaria_F" + "_" + Curso + "_" + CBO + ".png"
        save_results_to = 'graficos/'  
        plt.savefig(save_results_to + string1)      

    return
       

    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Terminar ...
def Adiciona_Coluna_Idade(path1,name1,path2,name2,name3,id):
    # Leitura do arquivo df original, masculino ou feminino
    if id == 'O':
       logging.info(" Adicionando a coluna Idade ao arquivo original")   
       # df =  os.path.join(path2[0],name2[2])
       df =  os.path.join(path2[0],name2[7])
       X = pd.read_csv(df)    
       # X = X.drop(columns=['Unnamed: 0'])
       # X = X.drop(columns=['Unnamed: 0.1'])
    else:
        if id == '29':
            logging.info(" Adicionando a coluna Idade ao arquivo Idade 29")   
            # df =  os.path.join(path2[0],name2[2])
            df =  os.path.join(path2[0],name3[5])
            X = pd.read_csv(df)    
            # X = X.drop(columns=['Unnamed: 0'])
            # X = X.drop(columns=['Unnamed: 0.1'])
        else:
            if id == '30-39':
                logging.info(" Adicionando a coluna Idade ao arquivo Idade 30-39")   
                df =  os.path.join(path2[0],name3[6])
                X = pd.read_csv(df)    
                X = X.drop(columns=['Unnamed: 0'])
                # X = X.drop(columns=['Unnamed: 0.1'])
            else:
                if id == '40-49':
                    logging.info(" Adicionando a coluna Idade ao arquivo Idade 40-49")   
                    df =  os.path.join(path2[0],name3[7])
                    X = pd.read_csv(df)    
                    X = X.drop(columns=['Unnamed: 0'])
                    # X = X.drop(columns=['Unnamed: 0.1'])
                else: 
                    if id == '50-59':
                        logging.info(" Adicionando a coluna Idade ao arquivo Idade 50-59")   
                        df =  os.path.join(path2[0],name3[8])
                        X = pd.read_csv(df)    
                        X = X.drop(columns=['Unnamed: 0'])
                        # X = X.drop(columns=['Unnamed: 0.1'])  
                    else: 
                        if id == '60':
                            logging.info(" Adicionando a coluna Idade ao arquivo Idade 60")   
                            df =  os.path.join(path2[0],name3[9])
                            X = pd.read_csv(df)    
                            X = X.drop(columns=['Unnamed: 0'])
                            # X = X.drop(columns=['Unnamed: 0.1'])  
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
    # x= X['Ida']
    # y= X['Volta']
    # plt.xlabel("Cursos")
    # plt.ylabel("Profissões")
    # plt.title("10%  - Cursos e Profissões do Censo_" + G)
    # plt.ylim(0, 100) # definir limite do eixo
    # plt.xlim(0, 100) # definir limite do eixo
    # plt.grid()
    # plt.scatter(x,y,marker = '*')
    # string1 = "10%  - Cursos e Profissões do Censo_" + G + ".pdf"
    # save_results_to = 'graficos/'  
    # plt.savefig(save_results_to + string1)  
    # Leitura do arquivo df original, masculino ou feminino
    if id == 'O':
       X['Idade'] = "O"    
       # X.to_csv(save_results_to +'Resultados_T_Original_Idade.csv')  
       return X
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
        if id == '29':
             # Adicionando coluna
            resultados_T=[]
            cluster=""
            # X['Cluster'][i]
            for i in range(len(X['CR'])):
                tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"29")
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
                    7:"Idade"
            }
            Resultados_T.rename(columns=dict,inplace=True)   
            # Resultados_T.to_csv(save_results_to +'Resultados_T_29.csv')   
            return Resultados_T          
        else:
              if id == '30-39':
                # Adicionando coluna
                resultados_T=[]
                cluster=""
                # X['Cluster'][i]
                for i in range(len(X['CR'])):
                    tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"30-39")
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
                        7:"Idade"
                }
                Resultados_T.rename(columns=dict,inplace=True)   
                # Resultados_T.to_csv(save_results_to +'Resultados_T_30_39.csv')   
                return Resultados_T      
              else:  
                   if id == '40-49':
                    # Adicionando coluna
                    resultados_T=[]
                    cluster=""
                    # X['Cluster'][i]
                    for i in range(len(X['CR'])):
                        tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"40-49")
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
                            7:"Idade"
                    }
                    Resultados_T.rename(columns=dict,inplace=True)   
                    # Resultados_T.to_csv(save_results_to +'Resultados_T_40_49.csv')   
                    return Resultados_T   
                   else:
                         if id == '50-59':
                            # Adicionando coluna
                            resultados_T=[]
                            cluster=""
                            # X['Cluster'][i]
                            for i in range(len(X['CR'])):
                                tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"50-59")
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
                                    7:"Idade"
                            }
                            Resultados_T.rename(columns=dict,inplace=True)   
                            # Resultados_T.to_csv(save_results_to +'Resultados_T_50_59.csv')   
                            return Resultados_T 
                         else:  
                            if id == '60':
                                # Adicionando coluna
                                resultados_T=[]
                                cluster=""
                                # X['Cluster'][i]
                                for i in range(len(X['CR'])):
                                    tupla=(X['Ida'][i],X['Volta'][i],cluster, X['CR'][i],CursoNome[i],X['CB'][i],CboNome[i],"60")
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
                                        7:"Idade"
                                }
                                Resultados_T.rename(columns=dict,inplace=True)   
                                # Resultados_T.to_csv(save_results_to +'Resultados_T_60.csv')   
                                return Resultados_T 
                          
                           
    return 

def Juntar_10Porcento_Idade():
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)
    path2 = ibge_variable.paths(13)
    name2 = ibge_variable.names(9)
    name3 = ibge_variable.names(10)
    Porcent_DF_Limpo_Idade = Adiciona_Coluna_Idade(path1,name1,path2,name2,name3,'O') 
    Porcent_DF_29_Limpo    = Adiciona_Coluna_Idade(path1,name1,path2,name2,name3,'29')
    Porcent_DF_30_39_Limpo = Adiciona_Coluna_Idade(path1,name1,path2,name2,name3,'30-39') 
    Porcent_DF_40_49_Limpo = Adiciona_Coluna_Idade(path1,name1,path2,name2,name3,'40-49') 
    Porcent_DF_50_59_Limpo = Adiciona_Coluna_Idade(path1,name1,path2,name2,name3,'50-59') 
    Porcent_DF_60_Limpo    = Adiciona_Coluna_Idade(path1,name1,path2,name2,name3,'60') 
    save_results_to = 'graficos/'  
     
    df_limpo = Porcent_DF_Limpo_Idade
    df_29_limpo = Porcent_DF_29_Limpo
    df_30_39_limpo = Porcent_DF_30_39_Limpo  
    df_40_49_limpo = Porcent_DF_40_49_Limpo
    df_50_59_limpo = Porcent_DF_50_59_Limpo
    df_60_limpo = Porcent_DF_60_Limpo


    df_row = pd.concat([df_limpo, df_29_limpo,df_30_39_limpo, df_40_49_limpo,df_50_59_limpo,df_60_limpo], ignore_index=True)
    df_row1 = df_row.sort_values(["Curso", "Cbo"], ascending=True)
    df_row2 = df_row1.sort_values(["Curso", "Cbo"], ascending=True)
    df_row2.to_csv(save_results_to + 'Resultados_T_29_30-39_40-49_50-59_60Kmeans3_Idade.csv')   
    return



def Filtrar_Tabela_10Porcento_Idade(): 
    path2 = ibge_variable.paths(13)
    name2 = ibge_variable.names(9)
    name3 = ibge_variable.names(10)
    save_results_to = 'graficos/'  
    Kmeans3_T =  os.path.join(path2[0],name2[7])
    X = pd.read_csv(Kmeans3_T) 
    Resultados_T_29_30_39_40_49_50_59_60Kmeans3_Idade =  os.path.join(path2[0],name2[14])
    df_row2 = pd.read_csv(Resultados_T_29_30_39_40_49_50_59_60Kmeans3_Idade) 

    resultados_T=[]
    for j in range(len(df_row2)):
        if pd.isnull(df_row2['Cluster'][j]):
            df_row2['Cluster'][j] = ''   
        else:    
            df_row2['Cluster'][j] = int(float(df_row2['Cluster'][j]))  
        for i in range(len(X)):        
            if (int(float(X['Curso'][i])) == int(float(df_row2['Curso'][j]))) & (int(float(X['Cbo'][i])) == int(float(df_row2['Cbo'][j]))):
                tupla=(df_row2['Ida'][j],df_row2['Volta'][j],df_row2['Cluster'][j], df_row2['Curso'][j].astype(int),df_row2['Curso_Nome'][j],df_row2['Cbo'][j].astype(int),df_row2['Cbo_Nome'][j],df_row2['Idade'][j])
                resultados_T.append(tupla)
                # ...         
         
    Resultados_T= pd.DataFrame(resultados_T)
    #...
    dict = {0:"Ida",
            1:"Volta",
            2:"Cluster",
            3:"Curso",
            4:"Curso_Nome",
            5:"Cbo",
            6:"Cbo_Nome",
            7:"Idade"
            }
    Resultados_T.rename(columns=dict,inplace=True)   
    Resultados_T.to_csv(save_results_to +'Resultados_T_Filtrados_Kmeans3_Idade.csv')   
    return

import pandas as pd

def fill_cluster_column(path,name):
    save_results_to = 'graficos/'  
    file_path = os.path.join(path[0],name[10])
    df = pd.read_csv(file_path)
    
    cluster_values = df['Cluster'].values
    filled_cluster_values = []

    current_cluster = None
    for value in cluster_values:
        if pd.notnull(value):
            current_cluster = int(value)
        filled_cluster_values.append(current_cluster)

    df['Cluster'] = filled_cluster_values
    df.to_csv(save_results_to +'Resultados_T_Filtrados_Kmeans3_Idade_Preenchido.csv')

def fill_cluster_column_Genero(path,name):
    save_results_to = 'graficos/'  
    file_path = os.path.join(path[0],name[13])
    df = pd.read_csv(file_path)
    
    cluster_values = df['Cluster'].values
    filled_cluster_values = []

    current_cluster = None
    for value in cluster_values:
        if pd.notnull(value):
            current_cluster = int(value)
        filled_cluster_values.append(current_cluster)

    df['Cluster'] = filled_cluster_values
    df.to_csv(save_results_to +'Resultados_T_Filtrados_Kmeans3_T_Preenchido.csv')
   
import pandas as pd

def separate_clusters():
    file_path = 'graficos/Resultados_T_Filtrados_Kmeans3_Idade_Preenchido.csv'
    df = pd.read_csv(file_path)
    
    cluster0 = df[df['Cluster'] == 0]
    cluster1 = df[df['Cluster'] == 1]
    cluster2 = df[df['Cluster'] == 2]
    
    cluster0.to_csv('graficos/Resultados_T_Filtrados_Kmeans3_Idade_Cluster0.csv', index=False)
    cluster1.to_csv('graficos/Resultados_T_Filtrados_Kmeans3_Idade_Cluster1.csv', index=False)
    cluster2.to_csv('graficos/Resultados_T_Filtrados_Kmeans3_Idade_Cluster2.csv', index=False)

def separate_clusters_Genero():
    file_path = 'graficos/Resultados_T_Filtrados_Kmeans3_T_Preenchido.csv'
    df = pd.read_csv(file_path)
    
    cluster0 = df[df['Cluster'] == 0]
    cluster1 = df[df['Cluster'] == 1]
    cluster2 = df[df['Cluster'] == 2]
    
    cluster0.to_csv('graficos/Resultados_T_Filtrados_Kmeans3_T_Preenchido_Cluster0.csv', index=False)
    cluster1.to_csv('graficos/Resultados_T_Filtrados_Kmeans3_T_Preenchido_Cluster1.csv', index=False)
    cluster2.to_csv('graficos/Resultados_T_Filtrados_Kmeans3_T_Preenchido_Cluster2.csv', index=False)

def Kmeans3_T_Grafico_Genero_Clusters(path2,name3,cluster):
    if cluster==0:
       
       #import pandas as pd

        # X = pd.read_csv("/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/Cluster1_Pontos_100_Genero_df_row2.csv", sep=",")
        # X = pd.read_csv("/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/Kmeans3_T_100_Genero_df_row2_49_alt - Cluster1_Kmeans3_T_100_Genero_df_row2_49.csv", sep=",")
        # X = pd.read_csv("/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/Cluster1_Kmeans3_T_100_Genero_df_row2_49.csv", sep=",")
        save_results_to = 'graficos/'
        file_path = os.path.join(path2[0],name3[15])
        df = pd.read_csv(file_path)
        X = df.drop(columns=['Unnamed: 0'])

        # x

        # print(len(X))

        fem  = []
        masc = []
        orig = []

        for i in range(0,len(X)):
            if(X['Genero'][i] == 'F'):
                 fem.append(X['Ida'][i])
                 fem.append(X['Volta'][i])
            if(X['Genero'][i] == 'M'):
                 masc.append(X['Ida'][i])
                 masc.append(X['Volta'][i])
            if(X['Genero'][i] == 'O'):
                 orig.append(X['Ida'][i])
                 orig.append(X['Volta'][i])
	  
        print(len(fem))
        print(len(masc))
        print(len(orig))	  

        print(len(X))

        i=0

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()

        while i<len(fem):
            j = i+1
            print(i)
            ax.scatter([orig[i], fem[i], masc[i]], [orig[j], fem[j], masc[j]], color=['black', 'pink', 'blue'])
            ax.annotate("", xy=(fem[i], fem[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='pink'))
            ax.annotate("", xy=(masc[i], masc[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='blue'))
            #print(fem[i],fem[j])
            #print(masc[i],masc[j])
            #print(orig[i],orig[j])
            #print("")
            i = i+2
        # plt.xlabel("Cursos")
        # plt.ylabel("Profissões")
        #plt.title("10%  -  Visualização dos três gráficos - Genero - Cluster 0 - Kmeans3")
        plt.xlabel("Courses")
        plt.ylabel("Professions")
        # plt.title("10% - View of the three graphs - Gender - Cluster 0 - Kmeans3")
        plt.xlim(0.0, 100.0)
        plt.ylim(0.0, 100.0)
        ##plt.show()
        string1 = "10% - View of the three graphs - Gender - Cluster 0 - Kmeans3_" + ".png"
        save_results_to = 'graficos/'  
        plt.savefig(save_results_to + string1)           

    else:
         if cluster==1:
            save_results_to = 'graficos/'
            #import pandas as pd

            # X = pd.read_csv("/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/Cluster1_Pontos_100_Genero_df_row2.csv", sep=",")
            # X = pd.read_csv("/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/Kmeans3_T_100_Genero_df_row2_49_alt - Cluster1_Kmeans3_T_100_Genero_df_row2_49.csv", sep=",")
            # X = pd.read_csv("/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/Cluster1_Kmeans3_T_100_Genero_df_row2_49.csv", sep=",")
            save_results_to = 'graficos/'
            file_path = os.path.join(path2[0],name3[16])
            df = pd.read_csv(file_path)
            X = df.drop(columns=['Unnamed: 0'])

            # x

            # print(len(X))

            fem  = []
            masc = []
            orig = []

            for i in range(0,len(X)):
                if(X['Genero'][i] == 'F'):
                    fem.append(X['Ida'][i])
                    fem.append(X['Volta'][i])
                if(X['Genero'][i] == 'M'):
                    masc.append(X['Ida'][i])
                    masc.append(X['Volta'][i])
                if(X['Genero'][i] == 'O'):
                    orig.append(X['Ida'][i])
                    orig.append(X['Volta'][i])
        
            print(len(fem))
            print(len(masc))
            print(len(orig))	  

            print(len(X))

            i=0

            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()

            while i<len(fem):
                j = i+1
                print(i)
                ax.scatter([orig[i], fem[i], masc[i]], [orig[j], fem[j], masc[j]], color=['black', 'pink', 'blue'])
                ax.annotate("", xy=(fem[i], fem[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='pink'))
                ax.annotate("", xy=(masc[i], masc[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='blue'))
                #print(fem[i],fem[j])
                #print(masc[i],masc[j])
                #print(orig[i],orig[j])
                #print("")
                i = i+2
            # plt.xlabel("Cursos")
            # plt.ylabel("Profissões")
            #plt.title("10%  -  Visualização dos três gráficos - Genero - Cluster 0 - Kmeans3")
            plt.xlabel("Courses")
            plt.ylabel("Professions")
            # plt.title("10% - View of the three graphs - Gender - Cluster 1 - Kmeans3")
            plt.xlim(0.0, 100.0)
            plt.ylim(0.0, 100.0)
            ## plt.show()
            string1 = "10% - View of the three graphs - Gender - Cluster 1 - Kmeans3_" + ".png"
            save_results_to = 'graficos/'  
            plt.savefig(save_results_to + string1)  
         else:
                if cluster==2:
                    #import pandas as pd

                    # X = pd.read_csv("/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/Cluster1_Pontos_100_Genero_df_row2.csv", sep=",")
                    # X = pd.read_csv("/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/Kmeans3_T_100_Genero_df_row2_49_alt - Cluster1_Kmeans3_T_100_Genero_df_row2_49.csv", sep=",")
                    # X = pd.read_csv("/content/drive/MyDrive/Orientacao_Rodolfo/Doutorado_Elisangela/Experimentos/11_12_23_a_22_01_24/Cluster1_Kmeans3_T_100_Genero_df_row2_49.csv", sep=",")
                    save_results_to = 'graficos/'
                    file_path = os.path.join(path2[0],name3[17])
                    df = pd.read_csv(file_path)
                    X = df.drop(columns=['Unnamed: 0'])

                    # x

                    # print(len(X))

                    fem  = []
                    masc = []
                    orig = []

                    for i in range(0,len(X)):
                        if(X['Genero'][i] == 'F'):
                            fem.append(X['Ida'][i])
                            fem.append(X['Volta'][i])
                        if(X['Genero'][i] == 'M'):
                            masc.append(X['Ida'][i])
                            masc.append(X['Volta'][i])
                        if(X['Genero'][i] == 'O'):
                            orig.append(X['Ida'][i])
                            orig.append(X['Volta'][i])
                
                    print(len(fem))
                    print(len(masc))
                    print(len(orig))	  

                    print(len(X))

                    i=0

                    import matplotlib.pyplot as plt
                    fig, ax = plt.subplots()

                    while i<len(fem):
                        j = i+1
                        print(i)
                        ax.scatter([orig[i], fem[i], masc[i]], [orig[j], fem[j], masc[j]], color=['black', 'pink', 'blue'])
                        ax.annotate("", xy=(fem[i], fem[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='pink'))
                        ax.annotate("", xy=(masc[i], masc[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='blue'))
                        #print(fem[i],fem[j])
                        #print(masc[i],masc[j])
                        #print(orig[i],orig[j])
                        #print("")
                        i = i+2
                    # plt.xlabel("Cursos")
                    # plt.ylabel("Profissões")
                    #plt.title("10%  -  Visualização dos três gráficos - Genero - Cluster 0 - Kmeans3")
                    plt.xlabel("Courses")
                    plt.ylabel("Professions")
                    # plt.title("10% - View of the three graphs - Gender - Cluster 2 - Kmeans3")
                    plt.xlim(0.0, 100.0)
                    plt.ylim(0.0, 100.0)
                    ## plt.show()
                    string1 = "10% - View of the three graphs - Gender - Cluster 2 - Kmeans3_" + ".png"
                    save_results_to = 'graficos/'  
                    plt.savefig(save_results_to + string1)  

    return

def Kmeans3_T_Grafico_Idade(path2,name3,cluster):  
    if cluster==0:
        save_results_to = 'graficos/'
        df =  os.path.join(path2[0],name3[11])
        Resultados_T = pd.read_csv(df) 
        # Resultados_T = Resultados_T.drop(columns=['Unnamed: 0'])
        # print(len(Resultados_T['Idade']))
 
        #CursoNome =[]
        I_25_29 = []
        I_30_39 = []
        I_40_49 = []
        I_50_59 = []
        I_60    = []
        orig    = []

        for i in range(0, 90):
            if(Resultados_T['Idade'][i] == "29"):
                I_25_29.append(Resultados_T['Ida'][i])
                I_25_29.append(Resultados_T['Volta'][i])
            if(Resultados_T['Idade'][i] == "30-39"):
                I_30_39.append(Resultados_T['Ida'][i])
                I_30_39.append(Resultados_T['Volta'][i])
            if(Resultados_T['Idade'][i] == "40-49"):
                I_40_49.append(Resultados_T['Ida'][i])
                I_40_49.append(Resultados_T['Volta'][i])
            if(Resultados_T['Idade'][i] == "50-59"):
                I_50_59.append(Resultados_T['Ida'][i])
                I_50_59.append(Resultados_T['Volta'][i])
            if(Resultados_T['Idade'][i] == "60"):
                I_60.append(Resultados_T['Ida'][i])
                I_60.append(Resultados_T['Volta'][i])


        # print(len(I_25_29))
        # print(len(I_30_39))
        # print(len(I_40_49))
        # print(len(I_50_59))
        # print(len(I_60))

        i=0    
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()   

        while i<30:
            j = i+1
            ax.scatter([I_25_29[i], I_30_39[i],I_40_49[i], I_50_59[i], I_60[i]], [I_25_29[j], I_30_39[j],I_40_49[j], I_50_59[j], I_60[j]], color=['blue','magenta','Darkgreen','red','black'])
            ax.annotate("", xy=(I_25_29[i], I_25_29[j]), xytext=(I_30_39[i], I_30_39[j]), arrowprops=dict(arrowstyle="<-", color='blue'))
            ax.annotate("", xy=(I_30_39[i], I_30_39[j]), xytext=(I_40_49[i], I_40_49[j]), arrowprops=dict(arrowstyle="<-", color='magenta'))
            ax.annotate("", xy=(I_40_49[i], I_40_49[j]), xytext=(I_50_59[i], I_50_59[j]), arrowprops=dict(arrowstyle="<-", color='Darkgreen'))
            ax.annotate("", xy=(I_50_59[i], I_50_59[j]), xytext=(I_60[i], I_60[j]), arrowprops=dict(arrowstyle="<-", color='red'))
            i = i+2


        plt.xlabel("Cursos")
        plt.ylabel("Profissões")
        # plt.title("10%  -  Visualização dos três gráficos - Idade - Cluster 0")
        # plt.xlabel("Courses")
        # plt.ylabel("Professions")
        # plt.title("10% - View of the three graphs - Age - Cluster 0")    
        plt.xlim(0.0, 100.0)
        plt.ylim(0.0, 100.0)
        # plt.show()
        # string1 = "10%  -  Visualização dos três gráficos - Idade - Cluster 0" + ".pdf"
        string1 = "10% - View of the three graphs - Age - Cluster 0" + ".png"
        save_results_to = 'graficos/'  
        plt.savefig(save_results_to + string1)   
    else:   
         if cluster==1:
            save_results_to = 'graficos/'
            df =  os.path.join(path2[0],name3[12])
            Resultados_T = pd.read_csv(df) 
            # Resultados_T = Resultados_T.drop(columns=['Unnamed: 0'])
            # print(len(Resultados_T['Idade']))
    
            #CursoNome =[]
            I_25_29 = []
            I_30_39 = []
            I_40_49 = []
            I_50_59 = []
            I_60    = []
            orig    = []

            for i in range(0, 90):
                if(Resultados_T['Idade'][i] == "29"):
                    I_25_29.append(Resultados_T['Ida'][i])
                    I_25_29.append(Resultados_T['Volta'][i])
                if(Resultados_T['Idade'][i] == "30-39"):
                    I_30_39.append(Resultados_T['Ida'][i])
                    I_30_39.append(Resultados_T['Volta'][i])
                if(Resultados_T['Idade'][i] == "40-49"):
                    I_40_49.append(Resultados_T['Ida'][i])
                    I_40_49.append(Resultados_T['Volta'][i])
                if(Resultados_T['Idade'][i] == "50-59"):
                    I_50_59.append(Resultados_T['Ida'][i])
                    I_50_59.append(Resultados_T['Volta'][i])
                if(Resultados_T['Idade'][i] == "60"):
                    I_60.append(Resultados_T['Ida'][i])
                    I_60.append(Resultados_T['Volta'][i])


            # print(len(I_25_29))
            # print(len(I_30_39))
            # print(len(I_40_49))
            # print(len(I_50_59))
            # print(len(I_60))

            i=0    
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()   

            while i<30:
                j = i+1
                ax.scatter([I_25_29[i], I_30_39[i],I_40_49[i], I_50_59[i], I_60[i]], [I_25_29[j], I_30_39[j],I_40_49[j], I_50_59[j], I_60[j]], color=['blue','magenta','Darkgreen','red','black'])
                ax.annotate("", xy=(I_25_29[i], I_25_29[j]), xytext=(I_30_39[i], I_30_39[j]), arrowprops=dict(arrowstyle="<-", color='blue'))
                ax.annotate("", xy=(I_30_39[i], I_30_39[j]), xytext=(I_40_49[i], I_40_49[j]), arrowprops=dict(arrowstyle="<-", color='magenta'))
                ax.annotate("", xy=(I_40_49[i], I_40_49[j]), xytext=(I_50_59[i], I_50_59[j]), arrowprops=dict(arrowstyle="<-", color='Darkgreen'))
                ax.annotate("", xy=(I_50_59[i], I_50_59[j]), xytext=(I_60[i], I_60[j]), arrowprops=dict(arrowstyle="<-", color='red'))
                i = i+2


            plt.xlabel("Cursos")
            plt.ylabel("Profissões")
            # plt.title("10%  -  Visualização dos três gráficos - Idade - Cluster 1")
            # plt.xlabel("Courses")
            # plt.ylabel("Professions")
            # plt.title("10% - View of the three graphs - Age - Cluster 1")
            plt.xlim(0.0, 100.0)
            plt.ylim(0.0, 100.0)
            # plt.show()
            # string1 = "10%  -  Visualização dos três gráficos - Idade - Cluster 1" + ".pdf"
            string1 = "10% - View of the three graphs - Age - Cluster 1" + ".png"
            save_results_to = 'graficos/'  
            plt.savefig(save_results_to + string1)     
         else:   
              if cluster==2:
                    save_results_to = 'graficos/'
                    df =  os.path.join(path2[0],name3[13])
                    Resultados_T = pd.read_csv(df) 
                    # Sequência desejada
                    sequencia_desejada = ["O", "29", "30-39", "40-49", "50-59", "60"]

                    # Identificar blocos válidos
                    indices_validos = []
                    for i in range(len(Resultados_T) - len(sequencia_desejada) + 1):
                        if list(Resultados_T['Idade'].iloc[i:i + len(sequencia_desejada)]) == sequencia_desejada:
                            indices_validos.extend(range(i, i + len(sequencia_desejada)))

                    # Criar um novo DataFrame com apenas as linhas válidas
                    novo_df = Resultados_T.iloc[indices_validos].copy()
                    # Salvar o resultado em um novo arquivo CSV
                    novo_df.to_csv('graficos/Resultados_T_Filtrados_Kmeans3_Idade_Cluster2_Filtrados.csv', index=False)     

                    df =  os.path.join(path2[0],name3[14])
                    Resultados_T = pd.read_csv(df)                 
                    #CursoNome =[]
                    I_25_29 = []
                    I_30_39 = []
                    I_40_49 = []
                    I_50_59 = []
                    I_60    = []
                    orig    = []

                    for i in range(0, 90):
                        if(Resultados_T['Idade'][i] == "29"):
                            I_25_29.append(Resultados_T['Ida'][i])
                            I_25_29.append(Resultados_T['Volta'][i])
                        if(Resultados_T['Idade'][i] == "30-39"):
                            I_30_39.append(Resultados_T['Ida'][i])
                            I_30_39.append(Resultados_T['Volta'][i])
                        if(Resultados_T['Idade'][i] == "40-49"):
                            I_40_49.append(Resultados_T['Ida'][i])
                            I_40_49.append(Resultados_T['Volta'][i])
                        if(Resultados_T['Idade'][i] == "50-59"):
                            I_50_59.append(Resultados_T['Ida'][i])
                            I_50_59.append(Resultados_T['Volta'][i])
                        if(Resultados_T['Idade'][i] == "60"):
                            I_60.append(Resultados_T['Ida'][i])
                            I_60.append(Resultados_T['Volta'][i])


                    # print(len(I_25_29))
                    # print(len(I_30_39))
                    # print(len(I_40_49))
                    # print(len(I_50_59))
                    # print(len(I_60))

                    i=0    
                    import matplotlib.pyplot as plt
                    fig, ax = plt.subplots()   

                    while i<30:
                        j = i+1
                        ax.scatter([I_25_29[i], I_30_39[i],I_40_49[i], I_50_59[i], I_60[i]], [I_25_29[j], I_30_39[j],I_40_49[j], I_50_59[j], I_60[j]], color=['blue','magenta','Darkgreen','red','black'])
                        ax.annotate("", xy=(I_25_29[i], I_25_29[j]), xytext=(I_30_39[i], I_30_39[j]), arrowprops=dict(arrowstyle="<-", color='blue'))
                        ax.annotate("", xy=(I_30_39[i], I_30_39[j]), xytext=(I_40_49[i], I_40_49[j]), arrowprops=dict(arrowstyle="<-", color='magenta'))
                        ax.annotate("", xy=(I_40_49[i], I_40_49[j]), xytext=(I_50_59[i], I_50_59[j]), arrowprops=dict(arrowstyle="<-", color='Darkgreen'))
                        ax.annotate("", xy=(I_50_59[i], I_50_59[j]), xytext=(I_60[i], I_60[j]), arrowprops=dict(arrowstyle="<-", color='red'))
                        i = i+2


                    plt.xlabel("Cursos")
                    plt.ylabel("Profissões")
                    # plt.title("10%  -  Visualização dos três gráficos - Idade - Cluster 2")
                    # plt.xlabel("Courses")
                    # plt.ylabel("Professions")
                    # plt.title("10% - View of the three graphs - Age - Cluster 2")    
                    plt.xlim(0.0, 100.0)
                    plt.ylim(0.0, 100.0)
                    # plt.show()   
                    # string1 = "10%  -  Visualização dos três gráficos - Idade - Cluster 2" + ".pdf"
                    string1 = "10% - View of the three graphs - Age - Cluster 2" + ".png"
                    save_results_to = 'graficos/'  
                    plt.savefig(save_results_to + string1)                                      
    return

# https://colab.research.google.com/drive/1TQdNxD0AM4_3Dr-En_qAXbYBUzTLSCie?authuser=1#scrollTo=UhKVZtPjJhj8
def Aposentados_maior80(path,name):
    save_results_to = 'graficos/'
    df =  os.path.join(path[0],name[0])
    Final = pd.read_csv(df) 

    Final = Final.drop(columns=['Unnamed: 0'])
     
    # Removendo todos que tem menos de 80 anos
    Final.drop(Final[(Final['Idade_em_Anos'] <=80)].index, inplace=True)
    # removendo todos que tem o campo aposentaria igual 0
    Final.drop(Final[(Final['rendimento_aposentadoria_pensao'] !=1)].index, inplace=True)
    # Removendo todos que sao aposentados mas nao são graduados em Medicina
    Final.drop(Final[(Final['Curso_Superior_Graduação_Código'] !=721)].index, inplace=True)
    # Aposentados que são formados em Medicina e são Médicos Gerais
    # Removendo todos que sao aposentados mas nao são graduados em Medicina
    Final.drop(Final[(Final['Ocupação_Código'] !=2211)].index, inplace=True)    
    
    # Filtrar apenas as colunas desejadas
    Final = Final[['gênero', 'Idade_em_Anos', 'Nível_instrução', 'Curso_Superior_Graduação_Código', 'Ocupação_Código', 'rendimento_aposentadoria_pensao']]
    Final_Filtrado = Final.head(10)
    # print(Final_Filtrado)
    # Final_Filtrado.to_excel(save_results_to + 'Final_Filtrado_Aposentados_maior80.xlsx')
    Final_Filtrado.to_csv(save_results_to + 'Final_Filtrado_Aposentados_maior80.csv', index=False)
    return

# Fase 35
#https://colab.research.google.com/drive/1_SXpQ6j3mwa8EjlHT3jYgcE7cY08WvJF?authuser=1#scrollTo=uo_mK_xg8jMW#
def Salarios_CBO_Idade(path,name,path1,name1,cluster):
    # Final sem Zeros
    save_results_to = 'graficos/'
    df =  os.path.join(path[0],name[0])
    Final = pd.read_csv(df) 
    Final = Final.drop(columns=['Unnamed: 0'])
    FinalSemZero = Final.loc[((Final['Valor_rend_bruto_M']!= 0))]
    FinalSemZero = FinalSemZero.reset_index(drop=True)

    if cluster == 0:  
        #Filtrados ... Cluster 0 ... Ciência da Computação/Analistas de Sistemas(481/2511)
        save_results_to = 'graficos/'
        # df =  os.path.join(path1[0],name1[0])
        df =  os.path.join(path1[0],name1[1])
        Resultados_T_Filtrados_Kmeans3_Idade_Editado = pd.read_csv(df) 
        filtrados = Resultados_T_Filtrados_Kmeans3_Idade_Editado.query('Cluster == 0.0')
        filtrados = Resultados_T_Filtrados_Kmeans3_Idade_Editado.query('Curso == 481')
        Resultados_T_Filtrados_Kmeans3_Idade_Editado = filtrados
        Resultados_T_Filtrados_Kmeans3_Idade_Editado = Resultados_T_Filtrados_Kmeans3_Idade_Editado.reset_index(drop=True) 
        Resultados_T_Filtrados_Kmeans3_Idade_Editado = Resultados_T_Filtrados_Kmeans3_Idade_Editado.drop(5)
        CBO = []
        CURSO = []
        IDADE = []
        for i in range(len(Resultados_T_Filtrados_Kmeans3_Idade_Editado)):
            CBO.append(Resultados_T_Filtrados_Kmeans3_Idade_Editado.Cbo[i])
            CURSO.append(Resultados_T_Filtrados_Kmeans3_Idade_Editado.Curso[i])
            IDADE.append(Resultados_T_Filtrados_Kmeans3_Idade_Editado.Idade[i])
        # print(CBO)    
        # print(CURSO)
        # print(IDADE)
        dados_1 = []
        dados_2 = []
        dados_3 = []
        dados_4 = []
        dados_5 = []
        dados = [dados_1,dados_2,dados_3,dados_4,dados_5] 
        for i in range(len(CBO)):
            for j in range(len(FinalSemZero)):
                if str(IDADE[i]) == '29':
                   # print(str(FinalSemZero.Ocupação_Código[j]), str(int(float(CBO[i]))),str(FinalSemZero.Curso_Superior_Graduação_Código[j]),str(int(float(CURSO[i]))),(FinalSemZero.Idade_em_Anos[j]))  
                    if((str(FinalSemZero.Ocupação_Código[j])==str(int(float(CBO[i]))))&(str(FinalSemZero.Curso_Superior_Graduação_Código[j])== str(int(float(CURSO[i]))))& (FinalSemZero.Idade_em_Anos[j]) <= 29):
                        dados[i].append(FinalSemZero.Qtdade_Salario[j]/100)
                if str(IDADE[i]) == '30-39':
                    if (str(FinalSemZero.Ocupação_Código[j])==str(int(float(CBO[i]))))&(str(FinalSemZero.Curso_Superior_Graduação_Código[j])== str(int(float(CURSO[i]))))& (FinalSemZero.Idade_em_Anos[j] >=30)& (FinalSemZero.Idade_em_Anos[j] <=39):
                        dados[i].append(FinalSemZero.Qtdade_Salario[j]/100)
                if str(IDADE[i]) == '40-49':
                    if (str(FinalSemZero.Ocupação_Código[j])==str(int(float(CBO[i]))))&(str(FinalSemZero.Curso_Superior_Graduação_Código[j])== str(int(float(CURSO[i]))))& (FinalSemZero.Idade_em_Anos[j] >=40)& (FinalSemZero.Idade_em_Anos[j] <=49):
                        dados[i].append(FinalSemZero.Qtdade_Salario[j]/100)
                if str(IDADE[i]) == '50-59':
                    if (str(FinalSemZero.Ocupação_Código[j])==str(int(float(CBO[i]))))&(str(FinalSemZero.Curso_Superior_Graduação_Código[j])== str(int(float(CURSO[i]))))& (FinalSemZero.Idade_em_Anos[j] >=50)& (FinalSemZero.Idade_em_Anos[j] <=59):
                        dados[i].append(FinalSemZero.Qtdade_Salario[j]/100)
                if str(IDADE[i]) == '60':
                    if (str(FinalSemZero.Ocupação_Código[j])==str(int(float(CBO[i]))))&(str(FinalSemZero.Curso_Superior_Graduação_Código[j])== str(int(float(CURSO[i]))))& (FinalSemZero.Idade_em_Anos[j] >= 60):
                        dados[i].append(FinalSemZero.Qtdade_Salario[j]/100)
        # print(dados)                
        xticks = []
        for z in range(len(IDADE)):
            xticks.append(str(IDADE[z]))
        # for i in range(len(CBO)):
        #     print(xticks[i])
        import matplotlib.pyplot as plt
        import numpy as np
        plt.rcParams.update({'font.size':20})      
        DADOS = dados
        fig, ax = plt.subplots(figsize=(20,10))
        ax.boxplot(DADOS)
        ax.set_yscale('log')
        #ax.set_title('Gráfico de Boxplot - Salários: Ciência da Computação/Analistas de Sistemas(481/2511) - Cluster 0 - KMeans3')
        #ax.set_xlabel('Idade')
        #ax.set_ylabel('Quantidade de Salários')
        ax.set_title('Boxplot Chart - Salaries: Ciência da Computação/Analistas de Sistemas(481/2511) - Cluster 0 - KMeans3')
        ax.set_xlabel('Age')
        ax.set_ylabel('Number of Salaries')
        ax.set_xticklabels(xticks)
        #string1 = "Grafico_Boxplot_Salarios_CienciaComputacao_AnalistasSistemas_481_2511_Cluster0_KMeans3" + ".pdf"
        string1 = "Grafico_Boxplot_Salarios_CienciaComputacao_AnalistasSistemas_481_2511_Cluster0_KMeans3" + ".png"
        plt.savefig(save_results_to + string1)   
        # plt.show()        
    if cluster == 1:       
        #Filtrados ... Cluster 0 ... Ciência da Computação/Analistas de Sistemas(481/2511)
        save_results_to = 'graficos/'
        df =  os.path.join(path1[0],name1[1])
        Resultados_T_Filtrados_Kmeans3_Idade_Editado = pd.read_csv(df) 
        filtrados = Resultados_T_Filtrados_Kmeans3_Idade_Editado.query('Cluster == 1.0')
        filtrados = Resultados_T_Filtrados_Kmeans3_Idade_Editado.query('Curso == 721 & Cbo == 2211')
        Resultados_T_Filtrados_Kmeans3_Idade_Editado = filtrados
        Resultados_T_Filtrados_Kmeans3_Idade_Editado = Resultados_T_Filtrados_Kmeans3_Idade_Editado.reset_index(drop=True) 
        Resultados_T_Filtrados_Kmeans3_Idade_Editado = Resultados_T_Filtrados_Kmeans3_Idade_Editado.drop(5)
        CBO = []
        CURSO = []
        IDADE = []
        for i in range(len(Resultados_T_Filtrados_Kmeans3_Idade_Editado)):
            CBO.append(Resultados_T_Filtrados_Kmeans3_Idade_Editado.Cbo[i])
            CURSO.append(Resultados_T_Filtrados_Kmeans3_Idade_Editado.Curso[i])
            IDADE.append(Resultados_T_Filtrados_Kmeans3_Idade_Editado.Idade[i])
        # print(CBO)    
        # print(CURSO)
        # print(IDADE)
        dados_1 = []
        dados_2 = []
        dados_3 = []
        dados_4 = []
        dados_5 = []
        dados = [dados_1,dados_2,dados_3,dados_4,dados_5] 
        for i in range(len(CBO)):
            for j in range(len(FinalSemZero)):
                if str(IDADE[i]) == '29':
                   # print(str(FinalSemZero.Ocupação_Código[j]), str(int(float(CBO[i]))),str(FinalSemZero.Curso_Superior_Graduação_Código[j]),str(int(float(CURSO[i]))),(FinalSemZero.Idade_em_Anos[j]))  
                    if((str(FinalSemZero.Ocupação_Código[j])==str(int(float(CBO[i]))))&(str(FinalSemZero.Curso_Superior_Graduação_Código[j])== str(int(float(CURSO[i]))))& (FinalSemZero.Idade_em_Anos[j]) <= 29):
                        dados[i].append(FinalSemZero.Qtdade_Salario[j]/100)
                if str(IDADE[i]) == '30-39':
                    if (str(FinalSemZero.Ocupação_Código[j])==str(int(float(CBO[i]))))&(str(FinalSemZero.Curso_Superior_Graduação_Código[j])== str(int(float(CURSO[i]))))& (FinalSemZero.Idade_em_Anos[j] >=30)& (FinalSemZero.Idade_em_Anos[j] <=39):
                        dados[i].append(FinalSemZero.Qtdade_Salario[j]/100)
                if str(IDADE[i]) == '40-49':
                    if (str(FinalSemZero.Ocupação_Código[j])==str(int(float(CBO[i]))))&(str(FinalSemZero.Curso_Superior_Graduação_Código[j])== str(int(float(CURSO[i]))))& (FinalSemZero.Idade_em_Anos[j] >=40)& (FinalSemZero.Idade_em_Anos[j] <=49):
                        dados[i].append(FinalSemZero.Qtdade_Salario[j]/100)
                if str(IDADE[i]) == '50-59':
                    if (str(FinalSemZero.Ocupação_Código[j])==str(int(float(CBO[i]))))&(str(FinalSemZero.Curso_Superior_Graduação_Código[j])== str(int(float(CURSO[i]))))& (FinalSemZero.Idade_em_Anos[j] >=50)& (FinalSemZero.Idade_em_Anos[j] <=59):
                        dados[i].append(FinalSemZero.Qtdade_Salario[j]/100)
                if str(IDADE[i]) == '60':
                    if (str(FinalSemZero.Ocupação_Código[j])==str(int(float(CBO[i]))))&(str(FinalSemZero.Curso_Superior_Graduação_Código[j])== str(int(float(CURSO[i]))))& (FinalSemZero.Idade_em_Anos[j] >= 60):
                        dados[i].append(FinalSemZero.Qtdade_Salario[j]/100)
        # print(dados)                
        xticks = []
        for z in range(len(IDADE)):
            xticks.append(str(IDADE[z]))
        # for i in range(len(CBO)):
        #     print(xticks[i])
        import matplotlib.pyplot as plt
        import numpy as np
        plt.rcParams.update({'font.size':20})      
        DADOS = dados
        fig, ax = plt.subplots(figsize=(20,10))
        ax.boxplot(DADOS)
        ax.set_yscale('log')
        #ax.set_title('Gráfico de Boxplot - Salários: Medicina/Médicos Gerais(721/2211) - Cluster 1 - KMeans3 ')
        #ax.set_xlabel('Idade')
        #ax.set_ylabel('Quantidade de Salários')
        ax.set_title('Boxplot Chart - Salaries: Medicina/Médicos Gerais(721/2211) - Cluster 1 - KMeans3 ')
        ax.set_xlabel('Age')
        ax.set_ylabel('Number of Salaries')
        ax.set_xticklabels(xticks)
        #string1 = "Grafico_Boxplot_Salarios_Medicina_MédicosGerais_721_2511_Cluster1_KMeans3" + ".pdf"
        string1 = "Grafico_Boxplot_Salarios_Medicina_MédicosGerais_721_2511_Cluster1_KMeans3" + ".png"
        plt.savefig(save_results_to + string1)   
        # plt.show()  
    if cluster == 2:
       #Filtrados ... Cluster 0 ... Ciência da Computação/Analistas de Sistemas(481/2511)
        save_results_to = 'graficos/'
        df =  os.path.join(path1[0],name1[1])
        Resultados_T_Filtrados_Kmeans3_Idade_Editado = pd.read_csv(df) 
        filtrados = Resultados_T_Filtrados_Kmeans3_Idade_Editado.query('Cluster == 2.0')
        filtrados = Resultados_T_Filtrados_Kmeans3_Idade_Editado.query('Curso == 721 & Cbo == 2212')
        Resultados_T_Filtrados_Kmeans3_Idade_Editado = filtrados
        Resultados_T_Filtrados_Kmeans3_Idade_Editado = Resultados_T_Filtrados_Kmeans3_Idade_Editado.reset_index(drop=True) 
        Resultados_T_Filtrados_Kmeans3_Idade_Editado = Resultados_T_Filtrados_Kmeans3_Idade_Editado.drop(5)
        CBO = []
        CURSO = []
        IDADE = []
        for i in range(len(Resultados_T_Filtrados_Kmeans3_Idade_Editado)):
            CBO.append(Resultados_T_Filtrados_Kmeans3_Idade_Editado.Cbo[i])
            CURSO.append(Resultados_T_Filtrados_Kmeans3_Idade_Editado.Curso[i])
            IDADE.append(Resultados_T_Filtrados_Kmeans3_Idade_Editado.Idade[i])
        # print(CBO)    
        # print(CURSO)
        # print(IDADE)
        dados_1 = []
        dados_2 = []
        dados_3 = []
        dados_4 = []
        dados_5 = []
        dados = [dados_1,dados_2,dados_3,dados_4,dados_5] 
        for i in range(len(CBO)):
            for j in range(len(FinalSemZero)):
                if str(IDADE[i]) == '29':
                   # print(str(FinalSemZero.Ocupação_Código[j]), str(int(float(CBO[i]))),str(FinalSemZero.Curso_Superior_Graduação_Código[j]),str(int(float(CURSO[i]))),(FinalSemZero.Idade_em_Anos[j]))  
                    if((str(FinalSemZero.Ocupação_Código[j])==str(int(float(CBO[i]))))&(str(FinalSemZero.Curso_Superior_Graduação_Código[j])== str(int(float(CURSO[i]))))& (FinalSemZero.Idade_em_Anos[j]) <= 29):
                        dados[i].append(FinalSemZero.Qtdade_Salario[j]/100)
                if str(IDADE[i]) == '30-39':
                    if (str(FinalSemZero.Ocupação_Código[j])==str(int(float(CBO[i]))))&(str(FinalSemZero.Curso_Superior_Graduação_Código[j])== str(int(float(CURSO[i]))))& (FinalSemZero.Idade_em_Anos[j] >=30)& (FinalSemZero.Idade_em_Anos[j] <=39):
                        dados[i].append(FinalSemZero.Qtdade_Salario[j]/100)
                if str(IDADE[i]) == '40-49':
                    if (str(FinalSemZero.Ocupação_Código[j])==str(int(float(CBO[i]))))&(str(FinalSemZero.Curso_Superior_Graduação_Código[j])== str(int(float(CURSO[i]))))& (FinalSemZero.Idade_em_Anos[j] >=40)& (FinalSemZero.Idade_em_Anos[j] <=49):
                        dados[i].append(FinalSemZero.Qtdade_Salario[j]/100)
                if str(IDADE[i]) == '50-59':
                    if (str(FinalSemZero.Ocupação_Código[j])==str(int(float(CBO[i]))))&(str(FinalSemZero.Curso_Superior_Graduação_Código[j])== str(int(float(CURSO[i]))))& (FinalSemZero.Idade_em_Anos[j] >=50)& (FinalSemZero.Idade_em_Anos[j] <=59):
                        dados[i].append(FinalSemZero.Qtdade_Salario[j]/100)
                if str(IDADE[i]) == '60':
                    if (str(FinalSemZero.Ocupação_Código[j])==str(int(float(CBO[i]))))&(str(FinalSemZero.Curso_Superior_Graduação_Código[j])== str(int(float(CURSO[i]))))& (FinalSemZero.Idade_em_Anos[j] >= 60):
                        dados[i].append(FinalSemZero.Qtdade_Salario[j]/100)
        # print(dados)                
        xticks = []
        for z in range(len(IDADE)):
            xticks.append(str(IDADE[z]))
        # for i in range(len(CBO)):
        #     print(xticks[i])
        import matplotlib.pyplot as plt
        import numpy as np
        plt.rcParams.update({'font.size':20})      
        DADOS = dados
        fig, ax = plt.subplots(figsize=(20,10))
        ax.boxplot(DADOS)
        ax.set_yscale('log')
        #ax.set_title('Gráfico de Boxplot - Salários: Medicina/Médicos Especialistas(721/2212) - Cluster 2 - KMeans3 ')
        #ax.set_xlabel('Idade')
        #ax.set_ylabel('Quantidade de Salários')
        ax.set_title('Boxplot Chart - Salaries: Medicina/Médicos Especialistas(721/2212) - Cluster 2 - KMeans3 ')
        ax.set_xlabel('Age')
        ax.set_ylabel('Number of Salaries')
        ax.set_xticklabels(xticks)
        #string1 = "Grafico_Boxplot_Salarios_Medicina_Médicos Especialistas_721_2512_Cluster2_KMeans3" + ".pdf"
        string1 = "Grafico_Boxplot_Salarios_Medicina_Médicos Especialistas_721_2512_Cluster2_KMeans3" + ".png"
        plt.savefig(save_results_to + string1)   
        # plt.show()    
    return


def deslocamento():
    from math import sqrt
    # save_results_to = 'graficos/'
    # file_path = save_results_to + 'Resultados_T_Filtrados_Kmeans3_T_Preenchido.csv'
    # df = pd.read_csv(file_path)

    # distances = []

    # for i in range(0, len(df), 3):
    #     if i + 2 < len(df):
    #         x1, y1 = df.iloc[i]['Ida'], df.iloc[i]['Volta']
    #         x2, y2 = df.iloc[i + 1]['Ida'], df.iloc[i + 1]['Volta']
    #         x3, y3 = df.iloc[i + 2]['Ida'], df.iloc[i + 2]['Volta']

    #         distance1 = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    #         distance2 = sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)

    #         distances.append([x1, y1, x2, y2, distance1])
    #         distances.append([x1, y1, x3, y3, distance2])

    # distances_df = pd.DataFrame(distances, columns=['x1', 'y1', 'x2', 'y2', 'Distance'])
    # distances_df.to_csv(save_results_to + 'Deslocamento_Geral.csv', index=False)
    save_results_to = 'graficos/'
    file_path = save_results_to + 'Resultados_T_Filtrados_Kmeans3_T_Preenchido.csv'
    df = pd.read_csv(file_path)

    distances = []

    for i in range(0, len(df), 3):
        if i + 2 < len(df):
            x1, y1 = df.iloc[i]['Ida'], df.iloc[i]['Volta']
            x2, y2 = df.iloc[i + 1]['Ida'], df.iloc[i + 1]['Volta']
            x3, y3 = df.iloc[i + 2]['Ida'], df.iloc[i + 2]['Volta']

            distance1 = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            distance2 = sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)

            distances.append([x1, y1, x2, y2, distance1])
            distances.append([x1, y1, x3, y3, distance2])

    distances_df = pd.DataFrame(distances, columns=['x1', 'y1', 'x2', 'y2', 'Distance'])
    distances_df.to_csv(save_results_to + 'Deslocamento_Geral.csv', index=False)

    # Adicionar coluna de distância ao DataFrame original
    df['Distance'] = None
    for i in range(0, len(df), 3):
        if i + 2 < len(df):
            x1, y1 = df.iloc[i]['Ida'], df.iloc[i]['Volta']
            x2, y2 = df.iloc[i + 1]['Ida'], df.iloc[i + 1]['Volta']
            x3, y3 = df.iloc[i + 2]['Ida'], df.iloc[i + 2]['Volta']

            distance1 = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            distance2 = sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)

            df.at[i + 1, 'Distance'] = distance1
            df.at[i + 2, 'Distance'] = distance2

    df.to_csv(save_results_to + 'Resultados_T_Filtrados_Kmeans3_T_Preenchido_com_Distancia.csv', index=False)
    
    return

def  deslocamentos_maioresdistancias():
        save_results_to = 'graficos/'
        file_path = save_results_to + 'Resultados_T_Filtrados_Kmeans3_T_Preenchido_com_Distancia.csv'
        df = pd.read_csv(file_path)
 
        # Encontrar as maiores distâncias
        max_distances = df.nlargest(10, 'Distance')

        # Salvar as maiores distâncias em um novo arquivo CSV
        max_distances.to_csv(save_results_to + 'Maiores_Distancias.csv', index=False)

        return
   
def deslocamento_clusters():
    save_results_to = 'graficos/'
    # file_path = save_results_to + 'Deslocamento_Geral.csv'
    file_path = save_results_to + 'Resultados_T_Filtrados_Kmeans3_T_Preenchido_com_Distancia.csv'
    df = pd.read_csv(file_path)
    
    
    cluster_0 = df[df['Cluster'] == 0]
    cluster_0.to_csv(save_results_to + 'Deslocamento_Geral_cluster 0.csv', index=False)

    cluster_1 = df[df['Cluster'] == 1]
    cluster_1.to_csv(save_results_to + 'Deslocamento_Geral_cluster 1.csv', index=False)

    cluster_2 = df[df['Cluster'] == 2]
    cluster_2.to_csv(save_results_to + 'Deslocamento_Geral_cluster 2.csv', index=False)
    
    return

def  deslocamentos_maioresdistancias_clusters():
     save_results_to = 'graficos/'
     # file_path = save_results_to + 'Deslocamento_Geral.csv'
     file_path = save_results_to + 'Maiores_Distancias.csv'
     df = pd.read_csv(file_path)
     
    
     cluster_0 = df[df['Cluster'] == 0]
     cluster_0.to_csv(save_results_to + 'Maiores_Distancias_cluster 0.csv', index=False)

     cluster_1 = df[df['Cluster'] == 1]
     cluster_1.to_csv(save_results_to + 'Maiores_Distancias_cluster 1.csv', index=False)

     cluster_2 = df[df['Cluster'] == 2]
     cluster_2.to_csv(save_results_to + 'Maiores_Distancias_cluster 2.csv', index=False)
    
     return

def dadosoriginais_resultados(sx):
    #https://colab.research.google.com/drive/1iLmL2_RNZNwhhYxoKEYwgy0LWoh7ri-g?authuser=1#scrollTo=RXn_W3SM374X
        if sx == 'F':
            save_results_to = 'graficos/'
            file_path = save_results_to + '100Porcent_DF_Fem_Limpo.csv'
            file_path1 = 'documentacao/' + 'Curso_Censo.csv'
            file_path2 = 'documentacao/' + 'CBO_CSV.csv'


            X_Original = pd.read_csv(file_path)
            X_Original = X_Original.drop(columns=['Unnamed: 0'])

            CursosCenso = pd.read_csv(file_path1)
            CursosCenso = CursosCenso.drop(columns=['Unnamed: 0'])

            CursoNome =[]
            for i in range (len(X_Original['CR'])):
                for index, row in CursosCenso.iterrows():
                    if (X_Original['CR'][i] == CursosCenso['curso_num'][index]):
                        CursoNome.append(CursosCenso['curso_nome'][index])

            CBO = pd.read_csv(file_path2)
            CBO = CBO.drop(columns=['Unnamed: 0'])
            
            CboNome =[]
            for i in range (len(X_Original['CB'])):
                for index, row in CBO.iterrows():
                    if (int(X_Original['CB'][i]) == CBO['Cod_CBO'][index]):
                        CboNome.append(CBO['Nome_CBO'][index])

            # print(len(X_Original))             
            # print(len(CursoNome)) 
            # print(len(CboNome))

            resultados_T=[]
            cluster=""
            for i in range(len(X_Original)):
                tupla=(X_Original['Ida'][i],X_Original['Volta'][i],cluster, X_Original['CR'][i],CursoNome[i],X_Original['CB'][i],CboNome[i],"F")
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
            Resultados_T.to_csv(save_results_to + 'Resultados_T_Fem_100.csv', index=False)
        if sx == 'M':
            save_results_to = 'graficos/'
            file_path = save_results_to + '100Porcent_DF_Masc_Limpo.csv'
            file_path1 = 'documentacao/' + 'Curso_Censo.csv'
            file_path2 = 'documentacao/' + 'CBO_CSV.csv'


            X_Original = pd.read_csv(file_path)
            X_Original = X_Original.drop(columns=['Unnamed: 0'])

            CursosCenso = pd.read_csv(file_path1)
            CursosCenso = CursosCenso.drop(columns=['Unnamed: 0'])

            CursoNome =[]
            for i in range (len(X_Original['CR'])):
                for index, row in CursosCenso.iterrows():
                    if (X_Original['CR'][i] == CursosCenso['curso_num'][index]):
                        CursoNome.append(CursosCenso['curso_nome'][index])

            CBO = pd.read_csv(file_path2)
            CBO = CBO.drop(columns=['Unnamed: 0'])
            
            CboNome =[]
            for i in range (len(X_Original['CB'])):
                for index, row in CBO.iterrows():
                    if (int(X_Original['CB'][i]) == CBO['Cod_CBO'][index]):
                        CboNome.append(CBO['Nome_CBO'][index])

            # print(len(X_Original))             
            # print(len(CursoNome)) 
            # print(len(CboNome))

            resultados_T=[]
            cluster=""
            for i in range(len(X_Original)):
                tupla=(X_Original['Ida'][i],X_Original['Volta'][i],cluster, X_Original['CR'][i],CursoNome[i],X_Original['CB'][i],CboNome[i],"M")
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
            Resultados_T.to_csv(save_results_to + 'Resultados_T_Masc_100.csv', index=False)    
        return

def resultados_filtragem_10_100():
    save_results_to = 'graficos/'
    file_path = save_results_to + 'Kmeans3_T.csv'
    file_path1 =  save_results_to + 'Resultados_T_Masc_100.csv'
    file_path2 =  save_results_to + 'Resultados_T_Fem_100.csv'

    Kmeans3_T = pd.read_csv(file_path)
    Kmeans3_T = Kmeans3_T.drop(columns=['Unnamed: 0'])
    Resultados_T_Masc_100 = pd.read_csv(file_path1)
    # Resultados_T_Masc_100 = Resultados_T_Masc_100.drop(columns=['Unnamed: 0'])
    Resultados_T_Fem_100  = pd.read_csv(file_path2)
    # Resultados_T_Fem_100 = Resultados_T_Fem_100.drop(columns=['Unnamed: 0'])


    Kmeans3_T['Genero'] = 'O'
    Kmeans3_T['C0'] = ''
    Kmeans3_T['C1'] = ''
    Kmeans3_T['C2'] = ''
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_O.csv', index=False) 

    file_path3 = save_results_to + 'Kmeans3_T_O.csv'
    Kmeans3_T_O = pd.read_csv(file_path3)
    # Kmeans3_T_O = Kmeans3_T_O.drop(columns=['Unnamed: 0'])

    ## 10% de 100% Masculino
    ## https://colab.research.google.com/drive/1cZx_GBJ-z18Ji4JrTZGTqzmfw-PuAcZl?authuser=1#scrollTo=kY71WzkoNmGS
    Resultados_T_Masc_100['C0'] = ''
    Resultados_T_Masc_100['C1'] = ''
    Resultados_T_Masc_100['C2'] = ''

    Ida          = []
    Volta        = []
    Cluster      = []
    Curso        = []
    Curso_Nome   = []
    Cbo          = []
    Cbo_Nome     = []
    Genero       = []
    C1           = []
    C2           = []
    C3           = []

    #for i in range(0,1):
    for i in range(len(Kmeans3_T_O)):
        for j in range(len(Resultados_T_Masc_100)):
            #if ((str(Resultados_T_Masc_100.Cbo[j])== '2341') & ( str(Resultados_T_Masc_100.Curso[j])== '142.0')):
            if ((str(Resultados_T_Masc_100.Cbo[j])== str(int(Kmeans3_T_O.Cbo[i]))) & ( str(Resultados_T_Masc_100.Curso[j])== str(Kmeans3_T_O.Curso[i]))):
                Ida.append(Resultados_T_Masc_100.Ida[j])
                Volta.append(Resultados_T_Masc_100.Volta[j])
                Cluster.append(Resultados_T_Masc_100.Cluster[j])
                Curso.append(Resultados_T_Masc_100.Curso[j])
                Curso_Nome. append(Resultados_T_Masc_100.Curso_Nome[j])
                Cbo.append(Resultados_T_Masc_100.Cbo[j])
                Cbo_Nome.append(Resultados_T_Masc_100.Cbo_Nome[j])
                Genero.append(Resultados_T_Masc_100.Genero[j])
                C1.append(Resultados_T_Masc_100.C0[j])
                C2.append(Resultados_T_Masc_100.C1[j])
                C3.append(Resultados_T_Masc_100.C2[j])

    Resultados_T_Masc_100_F = []
    for i in range(len(Ida)):
        tupla=(Ida[i],Volta[i],Cluster[i], Curso[i],Curso_Nome[i],Cbo[i],Cbo_Nome[i], Genero[i],C1[i],C2[i],C3[i])

        Resultados_T_Masc_100_F.append(tupla)
    #...
    Resultados_T_Masc_100_49 = pd.DataFrame(Resultados_T_Masc_100_F)

    #...
    dict = {0:"Ida",
            1:"Volta",
            2:"Cluster",
            3:"Curso",
            4:"Curso_Nome",
            5:"Cbo",
            6:"Cbo_Nome",
            7:"Genero",
            8:"C0",
            9:"C1",
            10:"C2"
    }
    Resultados_T_Masc_100_49.rename(columns=dict,inplace=True)     
    Resultados_T_Masc_100_49.to_csv(save_results_to + 'Resultados_T_Masc_100_49.csv', index=False) 
       
    ## 10% de 100% Feminino
    Resultados_T_Fem_100['C0'] = ''
    Resultados_T_Fem_100['C1'] = ''
    Resultados_T_Fem_100['C2'] = ''

    Ida          = []
    Volta        = []
    Cluster      = []
    Curso        = []
    Curso_Nome   = []
    Cbo          = []
    Cbo_Nome     = []
    Genero       = []
    C1           = []
    C2           = []
    C3           = []

    #for i in range(0,1):
    for i in range(len(Kmeans3_T_O)):
        for j in range(len(Resultados_T_Fem_100)):
            #if ((str(Resultados_T_Masc_100.Cbo[j])== '2341') & ( str(Resultados_T_Masc_100.Curso[j])== '142.0')):
            if ((str(Resultados_T_Fem_100.Cbo[j])== str(int(Kmeans3_T_O.Cbo[i]))) & ( str(Resultados_T_Fem_100.Curso[j])== str(Kmeans3_T_O.Curso[i]))):
                Ida.append(Resultados_T_Fem_100.Ida[j])
                Volta.append(Resultados_T_Fem_100.Volta[j])
                Cluster.append(Resultados_T_Fem_100.Cluster[j])
                Curso.append(Resultados_T_Fem_100.Curso[j])
                Curso_Nome. append(Resultados_T_Fem_100.Curso_Nome[j])
                Cbo.append(Resultados_T_Fem_100.Cbo[j])
                Cbo_Nome.append(Resultados_T_Fem_100.Cbo_Nome[j])
                Genero.append(Resultados_T_Fem_100.Genero[j])
                C1.append(Resultados_T_Fem_100.C0[j])
                C2.append(Resultados_T_Fem_100.C1[j])
                C3.append(Resultados_T_Fem_100.C2[j])

    Resultados_T_Fem_100_F = []
    for i in range(len(Ida)):
        tupla=(Ida[i],Volta[i],Cluster[i], Curso[i],Curso_Nome[i],Cbo[i],Cbo_Nome[i], Genero[i],C1[i],C2[i],C3[i])

        Resultados_T_Fem_100_F.append(tupla)
    #...
    Resultados_T_Fem_100_49 = pd.DataFrame(Resultados_T_Fem_100_F)

    #...
    dict = {0:"Ida",
            1:"Volta",
            2:"Cluster",
            3:"Curso",
            4:"Curso_Nome",
            5:"Cbo",
            6:"Cbo_Nome",
            7:"Genero",
            8:"C0",
            9:"C1",
            10:"C2"
    }
    Resultados_T_Fem_100_49.rename(columns=dict,inplace=True)      
    Resultados_T_Fem_100_49.to_csv(save_results_to + 'Resultados_T_Fem_100_49.csv', index=False) 
    return

import math
# função que permite calcular a distância  entre dois pontos
def distancia2d(x1, y1, x2, y2):
  a = x2 - x1
  b = y2 - y1
  c = math.sqrt(math.pow(a, 2) + math.pow(b, 2))
  return c



def resultados_distancia():
    # https://colab.research.google.com/drive/1cZx_GBJ-z18Ji4JrTZGTqzmfw-PuAcZl?authuser=1#scrollTo=WOd24Bbxa4kI

    # https://colab.research.google.com/drive/1cZx_GBJ-z18Ji4JrTZGTqzmfw-PuAcZl?authuser=1#scrollTo=jV2mGZbHZp3N
    # https://colab.research.google.com/drive/1cTpvuIkd7FGZbzEkScU4xKGFb6sSbGog?authuser=1#scrollTo=QXtm_sUoN3nB
    # https://colab.research.google.com/drive/1a-okMAgV1-pdXjzSq4y83SJjhnpAiVP2?authuser=1#scrollTo=bRvFa5Coi222

    save_results_to = 'graficos/'
    file_path = save_results_to + 'Kmeans3_T_O.csv'
    file_path1 =  save_results_to + 'Resultados_T_Masc_100_49.csv'
    file_path2 =  save_results_to + 'Resultados_T_Fem_100_49.csv'

    Kmeans3_T_O = pd.read_csv(file_path)
    Resultados_T_Masc_100_49 = pd.read_csv(file_path1)
    Resultados_T_Fem_100_49  = pd.read_csv(file_path2)

    # Kmeans3_T_O = Kmeans3_T_O.drop(columns=['Unnamed: 0'])
    # Resultados_T_Fem_100_49 = Resultados_T_Fem_100_49.drop(columns=['Unnamed: 0'])
    # Resultados_T_Masc_100_49 = Resultados_T_Masc_100_49.drop(columns=['Unnamed: 0'])

    file_path3 =  save_results_to + 'centroids.csv'

    centroids = pd.read_csv(file_path3)
    x0 = centroids.iloc[0, 0]
    y0 = centroids.iloc[0, 1]
    x1 = centroids.iloc[1, 0]
    y1 = centroids.iloc[1, 1]
    x2 = centroids.iloc[2, 0]
    y2 = centroids.iloc[2, 1]

    # print("Centroid 0: ", x0, y0)
    # print("Centroid 0: ", x1, y1)
    # print("Centroid 0: ", x2, y2)
    # Feminino =============================================================================
    # Cluster 1 ...
    # x1 = 27.00526316
    # y1 = 21.78263158
    for j in range(len(Resultados_T_Fem_100_49)):
        x = Resultados_T_Fem_100_49.Ida[j]
        y = Resultados_T_Fem_100_49.Volta[j]
        # vamos obter a distância entre eles
        distancia = distancia2d(x0, y0, x, y)
        #print("Distância entre os dois pontos: %0.2f" % distancia);
        Resultados_T_Fem_100_49.C0[j] = distancia

    # Cluster 2 ...
    # x1 = 66.464375
    # y1 = 77.656875    
    for j in range(len(Resultados_T_Fem_100_49)):
        x = Resultados_T_Fem_100_49.Ida[j]
        y = Resultados_T_Fem_100_49.Volta[j]
        # vamos obter a distância entre eles
        distancia = distancia2d(x1, y1, x, y)
        #print("Distância entre os dois pontos: %0.2f" % distancia);
        Resultados_T_Fem_100_49.C1[j] = distancia    

    # Cluster 3 ...
    # x1 = 25.76357143
    # y1 = 62.88071429
    for j in range(len(Resultados_T_Fem_100_49)):
        x = Resultados_T_Fem_100_49.Ida[j]
        y = Resultados_T_Fem_100_49.Volta[j]
        # vamos obter a distância entre eles
        distancia = distancia2d(x2, y2, x, y)
        #print("Distância entre os dois pontos: %0.2f" % distancia);
        Resultados_T_Fem_100_49.C2[j] = distancia    

    # Masculino =============================================================================
    # Cluster 1 ...
    # x1 = 27.00526316
    # y1 = 21.78263158
    for j in range(len(Resultados_T_Masc_100_49)):
        x = Resultados_T_Masc_100_49.Ida[j]
        y = Resultados_T_Masc_100_49.Volta[j]
        # vamos obter a distância entre eles
        distancia = distancia2d(x0, y0, x, y)
        #print("Distância entre os dois pontos: %0.2f" % distancia);
        Resultados_T_Masc_100_49.C0[j] = distancia

    # Cluster 2 ...
    # x1 = 66.464375
    # y1 = 77.656875    
    for j in range(len(Resultados_T_Masc_100_49)):
        x = Resultados_T_Masc_100_49.Ida[j]
        y = Resultados_T_Masc_100_49.Volta[j]
        # vamos obter a distância entre eles
        distancia = distancia2d(x1, y1, x, y)
        #print("Distância entre os dsave_results_to = 'graficos/'  ois pontos: %0.2f" % distancia);
        Resultados_T_Masc_100_49.C1[j] = distancia    

    # Cluster 3 ...
    # x1 = 25.76357143
    # y1 = 62.88071429
    for j in range(len(Resultados_T_Masc_100_49)):
        x = Resultados_T_Masc_100_49.Ida[j]
        y = Resultados_T_Masc_100_49.Volta[j]
        # vamos obter a distância entre eles
        distancia = distancia2d(x2, y2, x, y)
        #print("Distância entre os dois pontos: %0.2f" % distancia);
        Resultados_T_Masc_100_49.C2[j] = distancia    
    
    
    distancia_mudanca_clusters = pd.concat([Resultados_T_Fem_100_49, Resultados_T_Masc_100_49, Kmeans3_T_O])
    distancia_mudanca_clusters = pd.concat([Resultados_T_Fem_100_49, Resultados_T_Masc_100_49, Kmeans3_T_O], ignore_index=True)
    distancia_mudanca_clusters = distancia_mudanca_clusters.sort_values(["Curso", "Cbo"], ascending=True)

    distancia_mudanca_clusters.to_csv(save_results_to + 'distancia_mudanca_clusters.csv', index=False)

    return
def tabela_clusters_diferentes():
    # import pandas as pd

    # Carregar o CSV
    df = pd.read_csv("graficos/distancia_mudanca_clusters.csv")
    # df = df.drop(columns=['Unnamed: 0'])
    # df = df.drop(columns=['Unnamed: 0.1'])
    # df = df.drop(columns=['Unnamed: 0.1.1'])
    # df = df.drop(columns=['Unnamed: 0.1.1.1'])
    # df = df.drop(columns=['index'])
    df = df.drop(columns=['Curso_Nome'])
    df = df.drop(columns=['Cbo_Nome'])

    # Converter para código LaTeX
    latex_code = df.to_latex(index=False, caption="Profissões onde homens e mulheres estão em clusters diferentes", label="tab:Clusters_Diferentes")

    # Salvar em um arquivo .tex
    with open("distancia_mudanca_clusters_filtrados.tex", "w") as f:
        f.write(latex_code)
    return
def voronoi():
    # https://colab.research.google.com/drive/1ZP-z62wJWWM3zr52MYMjO_-brdvThb88?authuser=1#scrollTo=-oDzCfNi5PK0
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.spatial import Voronoi, voronoi_plot_2d
    # Create a set of points for the example:
    # rng = np.random.default_rng()
    # points = rng.random((10,2))

    # plot
    # Generate the Voronoi diagram for the points:
    # cluster 1 : 27.00526316,21.78263158  ... Vermelho
    # cluster 2 : 66.464375,  77.656875    ... Azul
    # cluster 3:  25.76357143,62.88071429  ... Verde
    # xpoints = np.array([20.09, 34.66, 28.31])
    # ypoints = np.array([32.74, 43.11, 39.27])
    fem=  [20.09, 32.74,49.52, 52.32,18.86, 62.32,11.87,71.31,41.75,47.08,13.23,37.01,73.32, 43.39,27.49, 39.83,34.08, 70.54,31.97, 69.25,77.99, 69.72]
    masc= [34.66, 43.11,42.23, 21.82,11.40, 24.06, 8.58, 35.28,25.13,25.90,68.44,64.93,50.82, 45.37,44.66, 67.29,48.45, 77.56,48.40, 81.73,46.05, 25.99]
    orig= [28.31, 39.27,49.00, 48.17,18.42, 58.22,11.63, 67.67,36.51,39.98,53.81,61.88,68.94, 43.67,43.95, 66.11,47.35, 77.14,45.94, 80.22,76.28, 66.06]

    points = np.array([[27.00526316,21.78263158], [66.464375,77.656875], [25.76357143,62.88071429]])
    vor = Voronoi(points)

    #Use voronoi_plot_2d to plot the diagram:
    #fig = voronoi_plot_2d(vor)
    # fig, ax = plt.subplots(20,10)
    voronoi_plot_2d(vor)
    #plt.plot(xpoints[0], ypoints[1], 'o', color='pink')
    #plt.plot(xpoints[0], ypoints[1], 'o', color='blue')
    #plt.plot(xpoints[0], ypoints[1], 'o', color='black')
    # 442: Química  / 2113: Químicos
    plt.scatter([orig[0], fem[0], masc[0]], [orig[1], fem[1], masc[1]], color=['black', 'pink', 'blue'])
    plt.annotate("", xy=(fem[0], fem[1]), xytext=(orig[0], orig[1]),arrowprops=dict(arrowstyle="->", color='pink'))
    plt.annotate("", xy=(masc[0], masc[1]), xytext=(orig[0], orig[1]),arrowprops=dict(arrowstyle="->", color='blue'))
    # 142: Ciências da Educação / 2341: Professores do Ensino Fundamental
    plt.scatter([orig[2], fem[2], masc[2]], [orig[3], fem[3], masc[3]], color=['black', 'pink', 'blue'])
    plt.annotate("", xy=(fem[2], fem[3]), xytext=(orig[2], orig[3]),arrowprops=dict(arrowstyle="->", color='pink'))
    plt.annotate("", xy=(masc[2], masc[3]), xytext=(orig[2], orig[3]),arrowprops=dict(arrowstyle="->", color='blue'))
    #142: Ciências da Educação / 2342: Professores do Ensino Pré-Escolar
    plt.scatter([orig[4], fem[4], masc[4]], [orig[5], fem[5], masc[5]], color=['black', 'pink', 'blue'])
    plt.annotate("", xy=(fem[4], fem[5]), xytext=(orig[4], orig[5]),arrowprops=dict(arrowstyle="->", color='pink'))
    plt.annotate("", xy=(masc[4], masc[5]), xytext=(orig[4], orig[5]),arrowprops=dict(arrowstyle="->", color='blue'))
    #142: Ciências da Educação / 2351: Especialistas em Métodos Pedagógicos
    plt.scatter([orig[6], fem[6], masc[6]], [orig[7], fem[7], masc[7]], color=['black', 'pink', 'blue'])
    plt.annotate("", xy=(fem[6], fem[7]), xytext=(orig[6], orig[7]),arrowprops=dict(arrowstyle="->", color='pink'))
    plt.annotate("", xy=(masc[6], masc[7]), xytext=(orig[6], orig[7]),arrowprops=dict(arrowstyle="->", color='blue'))
    #214: Design e estilismo / 2163: Desenhistas de Produtos e Vestuário
    plt.scatter([orig[8], fem[8], masc[8]], [orig[9], fem[9], masc[9]], color=['black', 'pink', 'blue'])
    plt.annotate("", xy=(fem[8], fem[9]), xytext=(orig[8], orig[9]),arrowprops=dict(arrowstyle="->", color='pink'))
    plt.annotate("", xy=(masc[8], masc[9]), xytext=(orig[8], orig[9]),arrowprops=dict(arrowstyle="->", color='blue'))
    #221: Religião /  2636: Ministros de Cultos Religiosos, Missionários e
    plt.scatter([orig[10], fem[10], masc[10]], [orig[11], fem[11], masc[11]], color=['black', 'pink', 'blue'])
    plt.annotate("", xy=(fem[10], fem[11]), xytext=(orig[10], orig[11]),arrowprops=dict(arrowstyle="->", color='pink'))
    plt.annotate("", xy=(masc[10], masc[11]), xytext=(orig[10], orig[11]),arrowprops=dict(arrowstyle="->", color='blue'))
    #322:Biblioteconomia, informação, arquivos 2622: Bibliotecários, documentaristas e Afins
    plt.scatter([orig[12], fem[12], masc[12]], [orig[13], fem[13], masc[13]], color=['black', 'pink', 'blue'])
    plt.annotate("", xy=(fem[12], fem[13]), xytext=(orig[12], orig[13]),arrowprops=dict(arrowstyle="->", color='pink'))
    plt.annotate("", xy=(masc[12], masc[13]), xytext=(orig[12], orig[13]),arrowprops=dict(arrowstyle="->", color='blue'))
    #521: Engenharia Mecânica e Metalurgia / 2144:Engenheiros Mecânicos
    plt.scatter([orig[14], fem[14], masc[14]], [orig[15], fem[15], masc[15]], color=['black', 'pink', 'blue'])
    plt.annotate("", xy=(fem[14], fem[15]), xytext=(orig[14], orig[15]),arrowprops=dict(arrowstyle="->", color='pink'))
    plt.annotate("", xy=(masc[14], masc[15]), xytext=(orig[14], orig[15]),arrowprops=dict(arrowstyle="->", color='blue'))
    #522: Elericidade e Energia / 2151:Engenheiros Eletricistas
    plt.scatter([orig[16], fem[16], masc[16]], [orig[17], fem[17], masc[17]], color=['black', 'pink', 'blue'])
    plt.annotate("", xy=(fem[16], fem[17]), xytext=(orig[16], orig[17]),arrowprops=dict(arrowstyle="->", color='pink'))
    plt.annotate("", xy=(masc[16], masc[17]), xytext=(orig[16], orig[17]),arrowprops=dict(arrowstyle="->", color='blue'))
    #621: Produção Agrícola e Pecuária / 2132:Agrônomos e Afins
    plt.scatter([orig[18], fem[18], masc[18]], [orig[19], fem[19], masc[19]], color=['black', 'pink', 'blue'])
    plt.annotate("", xy=(fem[18], fem[19]), xytext=(orig[18], orig[19]),arrowprops=dict(arrowstyle="->", color='pink'))
    plt.annotate("", xy=(masc[18], masc[19]), xytext=(orig[18], orig[19]),arrowprops=dict(arrowstyle="->", color='blue'))
    #762: Serviço Social e Orientação / 2635: Assistentes Sociais
    plt.scatter([orig[20], fem[20], masc[20]], [orig[21], fem[21], masc[21]], color=['black', 'pink', 'blue'])
    plt.annotate("", xy=(fem[20], fem[21]), xytext=(orig[20], orig[21]),arrowprops=dict(arrowstyle="->", color='pink'))
    plt.annotate("", xy=(masc[20], masc[21]), xytext=(orig[20], orig[21]),arrowprops=dict(arrowstyle="->", color='blue'))

    plt.xlim(0.0, 100.0)
    plt.ylim(0.0, 100.0)
    # plt.show()
    string1 = "voronoi" + ".png"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string1)  

    #fig, ax = plt.subplots()
    ##Use voronoi_plot_2d to plot the diagram again, with some settings customized:
    ##fig = voronoi_plot_2d(vor, show_vertices=False, line_colors='orange', line_width=2, line_alpha=0.6, point_size=2)
    #voronoi_plot_2d(vor, show_vertices=False, line_colors='orange', line_width=2, line_alpha=0.6, point_size=2)
    #plt.plot(xpoints[0], ypoints[0], 'o', color='pink')
    #plt.plot(xpoints[1], ypoints[1], 'o', color='blue')
    #plt.plot(xpoints[2], ypoints[2], 'o', color='black')
    #plt.xlim(0.0, 100.0)
    #plt.ylim(0.0, 100.0)
    #plt.show()    
    
    return

def Juntar_40_60Porcento_Genero():
    # https://colab.research.google.com/drive/1y-78aFKxXgt60VIyjhBmM6pn6XzcXZUC?authuser=1#scrollTo=1s_bOT2Q6QTU
    save_results_to = 'graficos/'
    save_results_too = 'processados/CSVs_ArquivoFinalGraduados/'

    save_results_to = 'graficos/'
    file_path = save_results_to + 'Kmeans3_T.csv'
    file_path1 =  save_results_too + 'Brasil_Graduados_Fem.csv'
    file_path2 =  save_results_too + 'Brasil_Graduados_Masc.csv'
    file_path3 =  save_results_too + 'Brasil_Graduados.csv'

    
    Kmeans3_T         = pd.read_csv(file_path)
    Final_Fem_CSV     = pd.read_csv(file_path1)
    Final_Masc_CSV    = pd.read_csv(file_path2 )
    Final             = pd.read_csv(file_path3)

    #...
    Kmeans3_T       = Kmeans3_T.drop(columns=['Unnamed: 0'])
    Final_Fem_CSV   = Final_Fem_CSV.drop(columns=['Unnamed: 0'])
    Final_Masc_CSV  = Final_Masc_CSV.drop(columns=['Unnamed: 0'])
    Final           = Final.drop(columns=['Unnamed: 0'])

    # ...    
    Kmeans3_T['M'] = ''
    Kmeans3_T['F'] = ''
    Kmeans3_T['Total'] = ''
    Kmeans3_T['MP'] = ''
    Kmeans3_T['FP'] = ''

    # for i in range(0,1): 
    for i in range(len(Kmeans3_T)): 
        Qtdade = 0
        for j in range(len(Final_Fem_CSV)):
            # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
            if ((str(Final_Fem_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))):
                Qtdade = Qtdade + 1
        Kmeans3_T.F[i] = int(Qtdade)            
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_F_45_55.csv')       
    # -----------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------

    Kmeans3_T  = pd.read_csv(save_results_to + 'Kmeans3_T_F_45_55.csv')
    for i in range(len(Kmeans3_T)):
        Qtdade = 0
        for j in range(len(Final_Masc_CSV)):
            if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))):
                Qtdade = Qtdade + 1
        Kmeans3_T.M[i] = int(Qtdade)
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_FM_45_55.csv')      
    # -----------------------------------------------------------------------------------    
    # -----------------------------------------------------------------------------------

    Kmeans3_T  = pd.read_csv(save_results_to + 'Kmeans3_T_FM_45_55.csv')
    for i in range(len(Kmeans3_T)):
        Qtdade = 0
        for j in range(len(Final)):
            if ((str(Final.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))):
                Qtdade = Qtdade + 1
        Kmeans3_T.Total[i] = int(Qtdade)
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_TFM_45_55.csv')  
    # -----------------------------------------------------------------------------------    
    # -----------------------------------------------------------------------------------   

    Kmeans3_T  = pd.read_csv(save_results_to + 'Kmeans3_T_TFM_45_55.csv')
    for i in range(len(Kmeans3_T)):
        Kmeans3_T.MP[i] = round(Kmeans3_T.M[i]/Kmeans3_T.Total[i],2)
        Kmeans3_T.FP[i] = round(Kmeans3_T.F[i]/Kmeans3_T.Total[i],2)
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_FMT_MPFP_45_55.csv')     
    # -----------------------------------------------------------------------------------    
    # -----------------------------------------------------------------------------------   
    return

def tabela():
    import pandas as pd

    # Carregar o CSV
    df = pd.read_csv("graficos/Kmeans3_T_FMT_MPFP_45_55.csv")
    df = df.drop(columns=['Unnamed: 0'])
    df = df.drop(columns=['Unnamed: 0.1'])
    df = df.drop(columns=['Unnamed: 0.1.1'])
    df = df.drop(columns=['Unnamed: 0.1.1.1'])
    df = df.drop(columns=['Ida'])
    df = df.drop(columns=['Volta'])
    df['Cluster'] = df['Cluster'].astype(int)
    df['Curso'] = df['Curso'].astype(int)
    df['Cbo'] = df['Cbo'].astype(int)
    df['M'] = df['M'].astype(int)
    df['F'] = df['F'].astype(int)
    df['Total'] = df['Total'].astype(int)


    # Converter para código LaTeX
    latex_code = df.to_latex(index=False, caption="Porcentagens de Masculinos e Femininos", label="tab:Fem_Masc")

    # Salvar em um arquivo .tex
    with open("tabelas/tabela.tex", "w") as f:
        f.write(latex_code)
    return

def separar_registros_por_cluster():
    import pandas as pd

    # Carregar o CSV
    df = pd.read_csv("graficos/Kmeans3_T_FMT_MPFP_45_55.csv")
    df = df.drop(columns=['Unnamed: 0'])
    df = df.drop(columns=['Unnamed: 0.1'])
    df = df.drop(columns=['Unnamed: 0.1.1'])
    df = df.drop(columns=['Unnamed: 0.1.1.1'])
    df = df.drop(columns=['Ida'])
    df = df.drop(columns=['Volta'])
    df['Cluster'] = df['Cluster'].astype(int)
    df['Curso'] = df['Curso'].astype(int)
    df['Cbo'] = df['Cbo'].astype(int)
    df['M'] = df['M'].astype(int)
    df['F'] = df['F'].astype(int)
    df['Total'] = df['Total'].astype(int)

    # Separate the DataFrame into three parts
    part1 = df[df['Cluster'] == 0]
    part2 = df[df['Cluster'] == 1]
    part3 = df[df['Cluster'] == 2]

    # Save each part into a separate .tex file
    part1.to_latex("tabelas/tabela_part0.tex", index=False)
    part2.to_latex("tabelas/tabela_part1.tex", index=False)
    part3.to_latex("tabelas/tabela_part2.tex", index=False)

    # # # Converter para código LaTeX
    # # latex_code = df.to_latex(index=False, caption="Porcentagens de Masculinos e Femininos", label="tab:Fem_Masc")

    # # # Salvar em um arquivo .tex
    # # with open("tabela.tex", "w") as f:
    # #     f.write(latex_code)
   
    # # # Read the tabela.tex file
    # # df = pd.read_csv("tabelas/cluster0.tex")

    # # Separate the records based on the cluster
    # cluster0 = df[df['Cluster'] == 0]
    # cluster1 = df[df['Cluster'] == 1]
    # cluster2 = df[df['Cluster'] == 2]

    # # Save the records into separate files  
    # cluster0 = cluster0.to_latex(index=False)  
    # cluster1 = cluster1.to_latex(index=False)  
    # cluster =  cluster2.to_latex(index=False)  
    # # cluster0.to_latex("tabelas/cluster0.tex", index=False)
    # # cluster1.to_latex("tabelas/cluster1.tex", index=False)
    # # cluster2.to_latex("tabelas/cluster2.tex", index=False) # Salvar em um arquivo .tex
    
    # with open("tabelas/cluster0.tex", "w") as f:
    #     f.write(cluster0)
    
    #  # Salvar em um arquivo .tex
    # with open("tabelas/cluster1.tex", "w") as f:
    #     f.write(cluster1)

    #  # Salvar em um arquivo .tex
    # with open("tabelas/cluster2.tex", "w") as f:
    #     f.write(cluster2)    

    return

# https://colab.research.google.com/drive/1y-78aFKxXgt60VIyjhBmM6pn6XzcXZUC?authuser=1
# Pontos selecionados(40% á 60%) 
def pt_selecionados_40_60():
    save_results_to = 'graficos/'
    file_path = save_results_to + 'Kmeans3_T_FMT_MPFP_45_55.csv'     
    Kmeans3_T         = pd.read_csv(file_path)
   
    # for i in range(len(Kmeans3_T)):
    #     if ((Kmeans3_T.MP[i]>= 0.40) & (Kmeans3_T.MP[i]<= 0.60)) & ((Kmeans3_T.FP[i]>= 0.40) & (Kmeans3_T.FP[i]<= 0.60)):
    #         print(Kmeans3_T.index[i], Kmeans3_T.Ida[i],Kmeans3_T.Volta[i],Kmeans3_T.Cluster[i],Kmeans3_T.Curso[i],Kmeans3_T.Curso_Nome[i],Kmeans3_T.Cbo[i],Kmeans3_T.Cbo_Nome[i],Kmeans3_T.M[i],Kmeans3_T.F[i],Kmeans3_T.Total[i],Kmeans3_T.MP[i],Kmeans3_T.FP[i])
    #         print("")

    # import pandas as pd

    # Lista para armazenar os dados filtrados
    filtered_data = []

    for i in range(len(Kmeans3_T)):
        if ((Kmeans3_T.MP[i] >= 0.40) & (Kmeans3_T.MP[i] <= 0.60) & (Kmeans3_T.FP[i] >= 0.40) & (Kmeans3_T.FP[i] <= 0.60)):
            # Adiciona os dados à lista
            filtered_data.append({
                "index": Kmeans3_T.index[i],
                "Ida": Kmeans3_T.Ida[i],
                "Volta": Kmeans3_T.Volta[i],
                "Cluster": Kmeans3_T.Cluster[i],
                "Curso": Kmeans3_T.Curso[i],
                "Curso_Nome": Kmeans3_T.Curso_Nome[i],
                "Cbo": Kmeans3_T.Cbo[i],
                "Cbo_Nome": Kmeans3_T.Cbo_Nome[i],
                "M": Kmeans3_T.M[i],
                "F": Kmeans3_T.F[i],
                "Total": Kmeans3_T.Total[i],
                "MP": Kmeans3_T.MP[i],
                "FP": Kmeans3_T.FP[i]
            })  
    df_filtered = pd.DataFrame(filtered_data)
    df_filtered.to_csv(save_results_to + 'Kmeans3_T_FMT_MPFP_40_60.csv')     

          
    return

def tabela_40_60():
    # import pandas as pd

    # Carregar o CSV
    df = pd.read_csv("graficos/Kmeans3_T_FMT_MPFP_40_60.csv")
    df = df.drop(columns=['Unnamed: 0'])
    # df = df.drop(columns=['Unnamed: 0.1'])
    # df = df.drop(columns=['Unnamed: 0.1.1'])
    # df = df.drop(columns=['Unnamed: 0.1.1.1'])
    df = df.drop(columns=['index'])
    df = df.drop(columns=['Curso_Nome'])
    df = df.drop(columns=['Cbo_Nome'])

    # Converter para código LaTeX
    latex_code = df.to_latex(index=False, caption="Porcentagens de Masculinos e Femininos entre 40\\% e 60\%", label="tab:Fem_Masc")

    # Salvar em um arquivo .tex
    with open("tabela_40_60.tex", "w") as f:
        f.write(latex_code)
    return

def graf_selecionados_40_60():
# https://colab.research.google.com/drive/1nMcfas4gH8ci_Rwb96xAqQOW65bCw_oK?authuser=1#scrollTo=9v3iLoWpJIRk
# Gráfico com os pontos selecionados(40% á 60%)     
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    fem = [23.55,35.32,6.28,19.0,40.62,76.53,24.26,46.14,13.23,14.61,58.08,65.4,67.71,90.34,74.96,89.98,93.47,89.51]
    masc= [22.81,36.36,19.52,13.08,42.89,71.77,25.66,51.68,15.32,10.76,59.42,64.88,69.18,92.22,68.2,87.3,92.88,88.84]
    orig = [23.21,35.79,10.46,15.01,41.63,74.28,24.99,48.96,14.32,12.17,58.87,65.09,68.58,91.44,72.02,88.86,93.2,89.21]

    #212.0 MÚSICA E ARTES CÊNICAS 2354.0 OUTROS PROFESSORES DE MÚSICA
    ax.scatter([orig[0], fem[0], masc[0]], [orig[1], fem[1], masc[1]], color=['black', 'pink', 'blue'])
    ax.annotate("", xy=(fem[0], fem[1]), xytext=(orig[0], orig[1]),arrowprops=dict(arrowstyle="->", color='pink'))
    ax.annotate("", xy=(masc[0], masc[1]), xytext=(orig[0], orig[1]),arrowprops=dict(arrowstyle="->", color='blue'))

    #214.0 DESIGN E ESTILISMO 2166.0 DESENHISTAS GRÁFICOS E DE MULTIMÍDIA
    ax.scatter([orig[2], fem[2], masc[2]], [orig[3], fem[3], masc[3]], color=['black', 'pink', 'blue'])
    ax.annotate("", xy=(fem[2], fem[3]), xytext=(orig[2], orig[3]),arrowprops=dict(arrowstyle="->", color='pink'))
    ax.annotate("", xy=(masc[2], masc[3]), xytext=(orig[2], orig[3]),arrowprops=dict(arrowstyle="->", color='blue'))

    #321.0 JORNALISMO E REPORTAGEM 2642.0 JORNALISTAS
    ax.scatter([orig[4], fem[4], masc[4]], [orig[5], fem[5], masc[5]], color=['black', 'pink', 'blue'])
    ax.annotate("", xy=(fem[4], fem[5]), xytext=(orig[4], orig[5]),arrowprops=dict(arrowstyle="->", color='pink'))
    ax.annotate("", xy=(masc[4], masc[5]), xytext=(orig[4], orig[5]),arrowprops=dict(arrowstyle="->", color='blue'))

    #342.0 MARKETING E PUBLICIDADE 2431.0 PROFISSIONAIS DA PUBLICIDADE E DA COMERCIALIZAÇÃO
    ax.scatter([orig[6], fem[6], masc[6]], [orig[7], fem[7], masc[7]], color=['black', 'pink', 'blue'])
    ax.annotate("", xy=(fem[6], fem[7]), xytext=(orig[6], orig[7]),arrowprops=dict(arrowstyle="->", color='pink'))
    ax.annotate("", xy=(masc[6], masc[7]), xytext=(orig[6], orig[7]),arrowprops=dict(arrowstyle="->", color='blue'))

    #342.0 MARKETING E PUBLICIDADE 1221.0 DIRIGENTES DE VENDAS E  COMERCIALIZAÇÃO
    ax.scatter([orig[8], fem[8], masc[8]], [orig[9], fem[9], masc[9]], color=['black', 'pink', 'blue'])
    ax.annotate("", xy=(fem[8], fem[9]), xytext=(orig[8], orig[9]),arrowprops=dict(arrowstyle="->", color='pink'))
    ax.annotate("", xy=(masc[8], masc[9]), xytext=(orig[8], orig[9]),arrowprops=dict(arrowstyle="->", color='blue'))

    #344.0 CONTABILIDADE E TRIBUTAÇÃO 2411.0 CONTADORES
    ax.scatter([orig[10], fem[10], masc[10]], [orig[11], fem[11], masc[11]], color=['black', 'pink', 'blue'])
    ax.annotate("", xy=(fem[10], fem[11]), xytext=(orig[10], orig[11]),arrowprops=dict(arrowstyle="->", color='pink'))
    ax.annotate("", xy=(masc[10], masc[11]), xytext=(orig[10], orig[11]),arrowprops=dict(arrowstyle="->", color='blue'))

    #380.0 DIREITO 2611.0 ADVOGADOS E JURISTAS
    ax.scatter([orig[12], fem[12], masc[12]], [orig[13], fem[13], masc[13]], color=['black', 'pink', 'blue'])
    ax.annotate("", xy=(fem[12], fem[13]), xytext=(orig[12], orig[13]),arrowprops=dict(arrowstyle="->", color='pink'))
    ax.annotate("", xy=(masc[12], masc[13]), xytext=(orig[12], orig[13]),arrowprops=dict(arrowstyle="->", color='blue'))

    #581.0 ARQUITETURA E URBANISMO 2161.0 ARQUITETOS DE EDIFICAÇÕES
    ax.scatter([orig[14], fem[14], masc[14]], [orig[15], fem[15], masc[15]], color=['black', 'pink', 'blue'])
    ax.annotate("", xy=(fem[14], fem[15]), xytext=(orig[14], orig[15]),arrowprops=dict(arrowstyle="->", color='pink'))
    ax.annotate("", xy=(masc[14], masc[15]), xytext=(orig[14], orig[15]),arrowprops=dict(arrowstyle="->", color='blue'))

    #724.0 ODONTOLOGIA 2261.0 DENTISTAS
    ax.scatter([orig[16], fem[16], masc[16]], [orig[17], fem[17], masc[17]], color=['black', 'pink', 'blue'])
    ax.annotate("", xy=(fem[16], fem[17]), xytext=(orig[16], orig[17]),arrowprops=dict(arrowstyle="->", color='pink'))
    ax.annotate("", xy=(masc[16], masc[17]), xytext=(orig[16], orig[17]),arrowprops=dict(arrowstyle="->", color='blue'))

    plt.xlabel("Cursos")
    plt.ylabel("Profissões")
    plt.title("10%  -  Visualização dos três gráficos - Gênero - 40-60%")
    plt.xlim(0.0, 100.0)
    plt.ylim(0.0, 100.0)
    # plt.show()
    string1 = "Pontos_Selecionados_40_60" + ".png"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string1)  

    return
 
# def genero_faixa_etaria():
#     return

# def  vetores_Setas_Pontos():
#      X = 'graficos/Resultados_T_Filtrados_Kmeans3_T_Preenchido.csv'
#      X = pd.read_csv(X, sep=",")

#      # len(X['Genero'])
#      fem   = []
#      masc  = []
#      orig  = []
#      # for i in range(0, 150):
#      for i in range(len(X['Genero'])):
#         if(str(X['Genero'][i]) == 'F'):
#             fem.append(X['Ida'][i])
#             fem.append(X['Volta'][i])
#             #print(i)
#         if(str(X['Genero'][i]) == 'M'):
#             masc.append(X['Ida'][i])
#             masc.append(X['Volta'][i])
#             #print(i)
#         if(str(X['Genero'][i]) == 'O'):
#             orig.append(X['Ida'][i])
#             orig.append(X['Volta'][i])
#             #print(X['Ida'][i],X['Volta'][i])

#      print(len(fem))
#      print(len(masc))
#      print(len(orig))    

#      i=0

#      #Kmeans3 - Copilot - Setas + Pontos    
#      import matplotlib.pyplot as plt

#      fig, ax = plt.subplots()
#      #while i<12:
#      while i<98:
#         j = i+1
#         ##print(i)
#         #ax.scatter([orig[i], fem[i], masc[i]], [orig[j], fem[j], masc[j]], color=['black', 'pink', 'blue'])
#         #ax.annotate("", xy=(fem[i], fem[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='pink'))
#         #ax.annotate("", xy=(masc[i], masc[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='blue'))

#         #ax.scatter([0, fem[i], masc[i]], [0, fem[j], masc[j]], color=['black', 'pink', 'blue'])
#         #ax.annotate("", xy=(fem[i],fem[j] ), xytext=(0, 0),arrowprops=dict(arrowstyle="->", color='pink'))
#         #ax.annotate("", xy=(masc[i], masc[j]), xytext=(0, 0),arrowprops=dict(arrowstyle="->", color='blue'))

#         #a= fem[i]-orig[i]
#         #b= fem[j]- orig[j]
#         #c= masc[i]-orig[i]
#         #d= masc[j]- orig[j]
#         #ax.scatter([0, fem[i], masc[i]], [0, fem[j], masc[j]], color=['black', 'pink', 'blue'])
#         #ax.annotate("", xy=(a,b), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='pink'))
#         #ax.annotate("", xy=(c,d), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='blue'))


#         a= fem[i]-orig[i]
#         b= fem[j]- orig[j]
#         c= masc[i]-orig[i]
#         d= masc[j]- orig[j]
#         ax.scatter([0, fem[i], masc[i]], [0, fem[j], masc[j]], color=['black', 'pink', 'blue'])
#         #ax.scatter([0, 0, 0], [0, 0, 0], color=['black', 'pink', 'blue'])
#         ax.annotate("", xy=(a,b), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='pink'))
#         ax.annotate("", xy=(c,d), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='blue'))

#         ##print(fem[i],fem[j])
#         ##print(masc[i],masc[j])
#         ##print(orig[i],orig[j])
#         ##print("")
#         i = i+2

#      plt.xlabel("Cursos")
#      plt.ylabel("Profissões")
#      plt.title("Gráfico dos vetores centrados em zero(0,0)_Setas_Pontos")
#      plt.xlim(-50.0, 100.0)
#      plt.ylim(-50.0, 100.0)
#      plt.show()  


#      return


def  vetores_Setas_Masc_Fem():
    X = 'graficos/Resultados_T_Filtrados_Kmeans3_T_Preenchido.csv'
    X = pd.read_csv(X, sep=",")

    # len(X['Genero'])
    fem   = []
    masc  = []
    orig  = []
    # for i in range(0, 150):
    for i in range(len(X['Genero'])):
        if(str(X['Genero'][i]) == 'F'):
            fem.append(X['Ida'][i])
            fem.append(X['Volta'][i])
            #print(i)
        if(str(X['Genero'][i]) == 'M'):
            masc.append(X['Ida'][i])
            masc.append(X['Volta'][i])
            #print(i)
        if(str(X['Genero'][i]) == 'O'):
            orig.append(X['Ida'][i])
            orig.append(X['Volta'][i])
            #print(X['Ida'][i],X['Volta'][i])

    print(len(fem))
    print(len(masc))
    print(len(orig))    

    i=0

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    #while i<12:
    while i<98:
        j = i+1
        ##print(i)
        #ax.scatter([orig[i], fem[i], masc[i]], [orig[j], fem[j], masc[j]], color=['black', 'pink', 'blue'])
        #ax.annotate("", xy=(fem[i], fem[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='pink'))
        #ax.annotate("", xy=(masc[i], masc[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='blue'))

        #ax.scatter([0, fem[i], masc[i]], [0, fem[j], masc[j]], color=['black', 'pink', 'blue'])
        #ax.annotate("", xy=(fem[i],fem[j] ), xytext=(0, 0),arrowprops=dict(arrowstyle="->", color='pink'))
        #ax.annotate("", xy=(masc[i], masc[j]), xytext=(0, 0),arrowprops=dict(arrowstyle="->", color='blue'))

        #a= fem[i]-orig[i]
        #b= fem[j]- orig[j]
        #c= masc[i]-orig[i]
        #d= masc[j]- orig[j]
        #ax.scatter([0, fem[i], masc[i]], [0, fem[j], masc[j]], color=['black', 'pink', 'blue'])
        #ax.annotate("", xy=(a,b), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='pink'))
        #ax.annotate("", xy=(c,d), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='blue'))


        a= fem[i]-orig[i]
        b= fem[j]- orig[j]
        c= masc[i]-orig[i]
        d= masc[j]- orig[j]
        #ax.scatter([0, fem[i], masc[i]], [0, fem[j], masc[j]], color=['black', 'pink', 'blue'])
        ax.scatter([0, 0, 0], [0, 0, 0], color=['black', 'pink', 'blue'])
        ax.annotate("", xy=(a,b), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='pink'))
        ax.annotate("", xy=(c,d), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='blue'))

        ##print(fem[i],fem[j])
        ##print(masc[i],masc[j])
        ##print(orig[i],orig[j])
        ##print("")
        i = i+2

    plt.xlabel("Cursos")
    plt.ylabel("Profissões")
    plt.title("Gráfico dos vetores centrados em zero(0,0)")
    plt.xlim(-40.0, 40.0)
    plt.ylim(-40.0, 40.0)
    # plt.show()
    string1 = "vetores_Setas_Masc_Fem" + ".png"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string1)  

     
    return

def vetores_Setas_Setas_Masculino():
    X = 'graficos/Resultados_T_Filtrados_Kmeans3_T_Preenchido.csv'
    X = pd.read_csv(X, sep=",")

    # len(X['Genero'])
    fem   = []
    masc  = []
    orig  = []
    # for i in range(0, 150):
    for i in range(len(X['Genero'])):
        if(str(X['Genero'][i]) == 'F'):
            fem.append(X['Ida'][i])
            fem.append(X['Volta'][i])
            #print(i)
        if(str(X['Genero'][i]) == 'M'):
            masc.append(X['Ida'][i])
            masc.append(X['Volta'][i])
            #print(i)
        if(str(X['Genero'][i]) == 'O'):
            orig.append(X['Ida'][i])
            orig.append(X['Volta'][i])
            #print(X['Ida'][i],X['Volta'][i])

    print(len(fem))
    print(len(masc))
    print(len(orig))    

    i=0

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    #while i<12:
    while i<98:
        j = i+1
        ##print(i)
        #ax.scatter([orig[i], fem[i], masc[i]], [orig[j], fem[j], masc[j]], color=['black', 'pink', 'blue'])
        #ax.annotate("", xy=(fem[i], fem[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='pink'))
        #ax.annotate("", xy=(masc[i], masc[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='blue'))

        #ax.scatter([0, fem[i], masc[i]], [0, fem[j], masc[j]], color=['black', 'pink', 'blue'])
        #ax.annotate("", xy=(fem[i],fem[j] ), xytext=(0, 0),arrowprops=dict(arrowstyle="->", color='pink'))
        #ax.annotate("", xy=(masc[i], masc[j]), xytext=(0, 0),arrowprops=dict(arrowstyle="->", color='blue'))

        #a= fem[i]-orig[i]
        #b= fem[j]- orig[j]
        #c= masc[i]-orig[i]
        #d= masc[j]- orig[j]
        #ax.scatter([0, fem[i], masc[i]], [0, fem[j], masc[j]], color=['black', 'pink', 'blue'])
        #ax.annotate("", xy=(a,b), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='pink'))
        #ax.annotate("", xy=(c,d), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='blue'))


        a= fem[i]-orig[i]
        b= fem[j]- orig[j]
        c= masc[i]-orig[i]
        d= masc[j]- orig[j]
        #ax.scatter([0, fem[i], masc[i]], [0, fem[j], masc[j]], color=['black', 'pink', 'blue'])
        ax.scatter([0, 0, 0], [0, 0, 0], color=['black', 'pink', 'blue'])
        #ax.annotate("", xy=(a,b), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='pink'))
        ax.annotate("", xy=(c,d), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='blue'))

        ##print(fem[i],fem[j])
        ##print(masc[i],masc[j])
        ##print(orig[i],orig[j])
        ##print("")
        i = i+2

    plt.xlabel("Cursos")
    plt.ylabel("Profissões")
    plt.title("Gráfico dos vetores centrados em zero(0,0)")
    plt.xlim(-40.0, 40.0)
    plt.ylim(-40.0, 40.0)
    # plt.show()
    string1 = "vetores_Setas_Setas_Masculino" + ".png"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string1)  
    return

def vetores_Setas_Setas_Feminino():
    X = 'graficos/Resultados_T_Filtrados_Kmeans3_T_Preenchido.csv'
    X = pd.read_csv(X, sep=",")

    # len(X['Genero'])
    fem   = []
    masc  = []
    orig  = []
    # for i in range(0, 150):
    for i in range(len(X['Genero'])):
        if(str(X['Genero'][i]) == 'F'):
            fem.append(X['Ida'][i])
            fem.append(X['Volta'][i])
            #print(i)
        if(str(X['Genero'][i]) == 'M'):
            masc.append(X['Ida'][i])
            masc.append(X['Volta'][i])
            #print(i)
        if(str(X['Genero'][i]) == 'O'):
            orig.append(X['Ida'][i])
            orig.append(X['Volta'][i])
            #print(X['Ida'][i],X['Volta'][i])

    print(len(fem))
    print(len(masc))
    print(len(orig))    

    i=0

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    #while i<12:
    while i<98:
        j = i+1
        ##print(i)
        #ax.scatter([orig[i], fem[i], masc[i]], [orig[j], fem[j], masc[j]], color=['black', 'pink', 'blue'])
        #ax.annotate("", xy=(fem[i], fem[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='pink'))
        #ax.annotate("", xy=(masc[i], masc[j]), xytext=(orig[i], orig[j]),arrowprops=dict(arrowstyle="->", color='blue'))

        #ax.scatter([0, fem[i], masc[i]], [0, fem[j], masc[j]], color=['black', 'pink', 'blue'])
        #ax.annotate("", xy=(fem[i],fem[j] ), xytext=(0, 0),arrowprops=dict(arrowstyle="->", color='pink'))
        #ax.annotate("", xy=(masc[i], masc[j]), xytext=(0, 0),arrowprops=dict(arrowstyle="->", color='blue'))

        #a= fem[i]-orig[i]
        #b= fem[j]- orig[j]
        #c= masc[i]-orig[i]
        #d= masc[j]- orig[j]
        #ax.scatter([0, fem[i], masc[i]], [0, fem[j], masc[j]], color=['black', 'pink', 'blue'])
        #ax.annotate("", xy=(a,b), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='pink'))
        #ax.annotate("", xy=(c,d), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='blue'))


        a= fem[i]-orig[i]
        b= fem[j]- orig[j]
        c= masc[i]-orig[i]
        d= masc[j]- orig[j]
        #ax.scatter([0, fem[i], masc[i]], [0, fem[j], masc[j]], color=['black', 'pink', 'blue'])
        ax.scatter([0, 0, 0], [0, 0, 0], color=['black', 'pink', 'blue'])
        ax.annotate("", xy=(a,b), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='pink'))
        #ax.annotate("", xy=(c,d), xytext=(0,0),arrowprops=dict(arrowstyle="->", color='blue'))

        ##print(fem[i],fem[j])
        ##print(masc[i],masc[j])
        ##print(orig[i],orig[j])
        ##print("")
        i = i+2

    plt.xlabel("Cursos")
    plt.ylabel("Profissões")
    plt.title("Gráfico dos vetores centrados em zero(0,0)")
    plt.xlim(-40.0, 40.0)
    plt.ylim(-40.0, 40.0)
    # plt.show()
    string1 = "vetores_Setas_Setas_Feminino" + ".png"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string1) 
    return
def extract_courses_Cluster0():
    # Read the CSV file
    data = pd.read_csv("graficos/Kmeans3_T_Salarios_certo_F.csv")
    data2 = pd.read_csv("graficos/Kmeans3_T_Salarios_certo_F.csv")

    data = data.drop(columns=['Unnamed: 0'])
    # data = data.drop(columns=['Curso_Nome'])
    # data = data.drop(columns=['Cbo_Nome'])
    data = data.drop(columns=['Ida'])
    data = data.drop(columns=['Volta'])
    data = data.drop(columns=['Cluster'])


    data2 = data2.drop(columns=['Unnamed: 0'])
    # data = data.drop(columns=['Curso_Nome'])
    # data = data.drop(columns=['Cbo_Nome'])
    data2 = data2.drop(columns=['Ida'])
    data2 = data2.drop(columns=['Volta'])
    data2 = data2.drop(columns=['Cluster'])

    
    Curso = [142,  142,  726, 142, 214]
    Cbo   = [2341, 2342, 2265,2351,2163]

    Curso2 = [521,520]
    Cbo2   = [2144,2141]


    # Filter the records based on the specified Courses and Cbos
    filtered_data = data[data['Curso'].isin(Curso) & data['Cbo'].isin(Cbo)]
    filtered_data_2 = data2[data2['Curso'].isin(Curso2) & data2['Cbo'].isin(Cbo2)]


#     data_521 = pd.read_csv("graficos/Deslocamento_Geral_cluster 0.csv")
#     filtered_521 = data_521[(data_521['Curso'] == 521) & (data_521['Cbo'] == 2144) & (data_521['Genero'] == 'F')]      

   
#    # Adicionar uma nova coluna em filtered_data
#     filtered_data['Deslocamento'] = [filtered_863['Distance'].values[0],filtered_221['Distance'].values[0], filtered_521['Distance'].values[0]]  # Substitua [1, 2, 3] pelos valores desejados
#     filtered_data['Cluster'] = [filtered_863['Cluster'].values[0],filtered_221['Cluster'].values[0], filtered_521['Cluster'].values[0]]  # Substitua [1, 2, 3] pelos valores desejados
    
    # filtered_data['Deslocamento'] = filtered_data['Deslocamento'].astype(int)
    # filtered_data['Deslocamento'] = round(filtered_data['Deslocamento'],2)
    # filtered_data['Cluster'] = filtered_data['Cluster'].astype(int)
    filtered_data['Curso'] = filtered_data['Curso'].astype(int)
    filtered_data['Cbo'] = filtered_data['Cbo'].astype(int)
    # filtered_data['Max'] = filtered_data['Max'].astype(int)
    # filtered_data['Min'] = filtered_data['Min'].astype(int)
    #filtered_data['Median'] = filtered_data['Median'].astype(int)
    filtered_data['Median'] = round(filtered_data['Median'],2)

 
    # filtered_data['Deslocamento'] = filtered_data['Deslocamento'].astype(int)
    # filtered_data['Deslocamento'] = round(filtered_data['Deslocamento'],2)
    # filtered_data['Cluster'] = filtered_data['Cluster'].astype(int)
    filtered_data_2['Curso'] = filtered_data_2['Curso'].astype(int)
    filtered_data_2['Cbo'] = filtered_data_2['Cbo'].astype(int)
    # filtered_data['Max'] = filtered_data['Max'].astype(int)
    # filtered_data['Min'] = filtered_data['Min'].astype(int)
    #filtered_data['Median'] = filtered_data['Median'].astype(int)
    filtered_data_2['Median'] = round(filtered_data_2['Median'],2)

    filtered_data_all = pd.concat([filtered_data, filtered_data_2], ignore_index=True)

    # Save the records in a LaTeX table
    latex_table = filtered_data_all.to_latex(index=False, caption="Cluster0 deslocamentos signficativos ", label="tab:Salarios_Cluster0") 
    
    
    # Salvar em um arquivo .tex
    with open("tabelas/Kmeans3_T_Salarios_Cluster0.tex", "w") as f:
        f.write(latex_table)
    return

def extract_courses_F():
    # Read the CSV file
    data = pd.read_csv("graficos/Kmeans3_T_Salarios_certo_F.csv")
    data = data.drop(columns=['Unnamed: 0'])
    # data = data.drop(columns=['Curso_Nome'])
    # data = data.drop(columns=['Cbo_Nome'])
    data = data.drop(columns=['Ida'])
    data = data.drop(columns=['Volta'])

    
    Curso = [863, 221, 521]
    Cbo   = [110, 2636, 2144]


    # Filter the records based on the specified Courses and Cbos
    filtered_data = data[data['Curso'].isin(Curso) & data['Cbo'].isin(Cbo)]

    data_863 = pd.read_csv("graficos/Deslocamento_Geral_cluster 2.csv")
    filtered_863 = data_863[(data_863['Curso'] == 863) & (data_863['Cbo'] == 110) & (data_863['Genero'] == 'F')]      
    data_221 = pd.read_csv("graficos/Deslocamento_Geral_cluster 1.csv")
    filtered_221 = data_221[(data_221['Curso'] == 221) & (data_221['Cbo'] == 2636) & (data_221['Genero'] == 'F')]     
    data_521 = pd.read_csv("graficos/Deslocamento_Geral_cluster 0.csv")
    filtered_521 = data_521[(data_521['Curso'] == 521) & (data_521['Cbo'] == 2144) & (data_521['Genero'] == 'F')]      

   
   # Adicionar uma nova coluna em filtered_data
    filtered_data['Deslocamento'] = [filtered_863['Distance'].values[0],filtered_221['Distance'].values[0], filtered_521['Distance'].values[0]]  # Substitua [1, 2, 3] pelos valores desejados
    filtered_data['Cluster'] = [filtered_863['Cluster'].values[0],filtered_221['Cluster'].values[0], filtered_521['Cluster'].values[0]]  # Substitua [1, 2, 3] pelos valores desejados
    
    # filtered_data['Deslocamento'] = filtered_data['Deslocamento'].astype(int)
    filtered_data['Deslocamento'] = round(filtered_data['Deslocamento'],2)
    filtered_data['Cluster'] = filtered_data['Cluster'].astype(int)
    filtered_data['Curso'] = filtered_data['Curso'].astype(int)
    filtered_data['Cbo'] = filtered_data['Cbo'].astype(int)
    # filtered_data['Max'] = filtered_data['Max'].astype(int)
    # filtered_data['Min'] = filtered_data['Min'].astype(int)
    #filtered_data['Median'] = filtered_data['Median'].astype(int)
    filtered_data['Median'] = round(filtered_data['Median'],2)




    # Save the records in a LaTeX table
    latex_table = filtered_data.to_latex(index=False, caption="Deslocamentos signficativos femininos", label="tab:Salarios_Desequlibrio_F") 
    
    
    # Salvar em um arquivo .tex
    with open("tabelas/Kmeans3_T_Salarios_certo_F.tex", "w") as f:
        f.write(latex_table)

    return 

def extract_courses_Correspondentes_F():
    # Read the CSV file
    data = pd.read_csv("graficos/Kmeans3_T_Salarios_certo_M.csv")
    data = data.drop(columns=['Unnamed: 0'])
    data = data.drop(columns=['Curso_Nome'])
    data = data.drop(columns=['Cbo_Nome'])

    Curso = [863, 221, 521]
    Cbo   = [110, 2636, 2144]

    # Filter the records based on the specified Courses and Cbos
    filtered_data = data[data['Curso'].isin(Curso) & data['Cbo'].isin(Cbo)]

    # Save the records in a LaTeX table
    latex_table = filtered_data.to_latex(index=False, caption="Masculinos: correspondentes aos deslocamentos femininos", label="tab:Salarios_Desequlibrio_F")
    
    # Salvar em um arquivo .tex
    with open("Kmeans3_T_Salarios_certo_Correspondentes_F.tex", "w") as f:
        f.write(latex_table)

    return 


def extract_courses_M():
    # Read the CSV file
    data = pd.read_csv("graficos/Kmeans3_T_Salarios_certo_M.csv")
    data = data.drop(columns=['Unnamed: 0'])
    data = data.drop(columns=['Curso_Nome'])
    data = data.drop(columns=['Cbo_Nome'])

    Curso = [762, 142, 142, 725, 142, 726, 214]
    Cbo   = [2635, 2342, 2351, 2226, 2341, 2265, 2163]

    # Filter the records based on the specified Courses and Cbos
    filtered_data = data[data['Curso'].isin(Curso) & data['Cbo'].isin(Cbo)]

    # Save the records in a LaTeX table
    latex_table = filtered_data.to_latex(index=False, caption="Deslocamentos signficativos masculinos", label="tab:Salarios_Desequlibrio_M")
    
    # Salvar em um arquivo .tex
    with open("Kmeans3_T_Salarios_certo_M.tex", "w") as f:
        f.write(latex_table)

    return	

def extract_courses_Correspondentes_M():
    # Read the CSV file
    data = pd.read_csv("graficos/Kmeans3_T_Salarios_certo_F.csv")
    data = data.drop(columns=['Unnamed: 0'])
    data = data.drop(columns=['Curso_Nome'])
    data = data.drop(columns=['Cbo_Nome'])

    Curso = [762, 142, 142, 725, 142, 726, 214]
    Cbo   = [2635, 2342, 2351, 2226, 2341, 2265, 2163]

    # Filter the records based on the specified Courses and Cbos
    filtered_data = data[data['Curso'].isin(Curso) & data['Cbo'].isin(Cbo)]

    # Save the records in a LaTeX table
    latex_table = filtered_data.to_latex(index=False, caption="Femininos: correspondentes aos deslocamentos masculinos", label="tab:Salarios_Desequlibrio_F")
    
    # Salvar em um arquivo .tex
    with open("Kmeans3_T_Salarios_certo_Correspondentes_M.tex", "w") as f:
        f.write(latex_table)

    return 


def extract_courses_transicao():
    # Read the CSV file
    data = pd.read_csv("graficos/Kmeans3_T_FMT_MPFP_45_55.csv")
    data = data.drop(columns=['Unnamed: 0'])
    data = data.drop(columns=['Unnamed: 0.1'])
    data = data.drop(columns=['Unnamed: 0.1.1'])
    data = data.drop(columns=['Unnamed: 0.1.1.1'])
    data = data.drop(columns=['Curso_Nome'])
    data = data.drop(columns=['Cbo_Nome'])

    Curso = [481, 483, 723]
    Cbo   = [2511, 2611, 2221]

    # Filter the records based on the specified Courses and Cbos
    filtered_data = data[data['Curso'].isin(Curso) & data['Cbo'].isin(Cbo)]

    # Save the records in a LaTeX table
    latex_table = filtered_data.to_latex(index=False, caption="Profissôes em transição de gênero", label="tab:Salarios_transicao")
    
    # Salvar em um arquivo .tex
    with open("Kmeans3_T_Salarios_certo_MF_transição.tex", "w") as f:
        f.write(latex_table)

    return  
   
def extract_courses_equidade():
    # Read the CSV file
    data = pd.read_csv("graficos/Kmeans3_T_FMT_MPFP_45_55.csv")
    data = data.drop(columns=['Unnamed: 0'])
    data = data.drop(columns=['Unnamed: 0.1'])
    data = data.drop(columns=['Unnamed: 0.1.1'])
    data = data.drop(columns=['Unnamed: 0.1.1.1'])
    data = data.drop(columns=['Ida'])
    data = data.drop(columns=['Volta'])
    data['Cluster'] = data['Cluster'].astype(int)
    data['Curso'] = data['Curso'].astype(int)
    data['Cbo'] = data['Cbo'].astype(int)
    data['M'] = data['M'].astype(int)
    data['F'] = data['F'].astype(int)
    data['Total'] = data['Total'].astype(int)

    Curso = [520, 520, 721, 721]
    Cbo   = [2142, 2141, 2211, 2212]
   

    # Filter the records based on the specified Courses and Cbos
    filtered_data = data[data['Curso'].isin(Curso) & data['Cbo'].isin(Cbo)]

    # Save the records in a LaTeX table
    latex_table = filtered_data.to_latex(index=False, caption="Equilibrio de Gênero versus Equidade de Oportunidades", label="tab:Salarios_Equidade")
    
    # Salvar em um arquivo .tex
    with open("Kmeans3_T_Salarios_certo_MF_equidade.tex", "w") as f:
        f.write(latex_table)

    return  
