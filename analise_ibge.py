
#pip install ibge-parser
#pip install ibge-parser



# inclua todos os demais imports aqui
import argparse
import sys
import os
import pandas as pd 
import numpy as np

import ibgeparser
import pandas as pd
from pandas import DataFrame
import numpy as np

import os
import glob
import pandas as pd

from functools import reduce


# import da classe principal
from ibgeparser.microdados import Microdados
# import dos enums para facilitar as buscas
from ibgeparser.enums import Anos, Estados, Modalidades

#import original.ibge_functions
import ibge_functions

# Esse arquivo não pode conter código que não seja chamada de funções e verificação de parâmetros
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fase', type=int, help='Indica a fase do fluxo para começar a execução')
args = parser.parse_args()

if args.fase is None:
    fase = 10
else:
    fase = args.fase

# Fase 0: Download dos dados do IBGE da web
#if fase >= 0:
if fase == 0:
    
    # Leia os dados do IBGE
    ano_ac = Anos.DEZ
    modalidades_ac = [Modalidades.PESSOAS]
    estados = [Estados.PARANA], [Estados.SANTA_CATARINA], [Estados.RIO_GRANDE_DO_SUL], [Estados.MATO_GROSSO_DO_SUL], [Estados.MATO_GROSSO], [Estados.GOIAS], [Estados.DISTRITO_FEDERAL], 
    
    for i in range(len(estados)):
        estados_ac = estados[i]
        #original.ibge_functions.function_obterdados_especificacao_coluna(ano_ac, estados_ac, modalidades_ac)
        ibge_functions.function_obterdados_especificacao_coluna(ano_ac, estados_ac, modalidades_ac)

# Fase 1: Filtrar somente os dados relevantes. Aqui significa que 
# você precisa filtrar todos os dados que possam ser utilizados no futuro.
#if fase >= 1:
if fase == 1:
    path = ['/home/essantos/Downloads/ibge-2010/original/Sul/', '/home/essantos/Downloads/ibge-2010/original/Centro_Oeste/']
    names = ['Amostra_Pessoas_41_PR.csv','Amostra_Pessoas_42_SC.csv','Amostra_Pessoas_43_RS.csv'], ['Amostra_Pessoas_50_MS.csv',  'Amostra_Pessoas_51_MT.csv','Amostra_Pessoas_52_GO.csv','Amostra_Pessoas_53_DF.csv']

    for i in range(len(names)):
       namess = len(names[i])
       for j in range(namess):
           name = str(names[i][j])
           ibge_functions.Filtrar_Dados_Censo(path[i],name,i)
    pass


# Fase 2: Limpeza dos dados. Agora começa a processar algo mais complexo desde que seja definitivo
# Pré-Processamento
#if fase >= 2:
if fase == 2:
   #Limpeza_Arquivo_Censo_Graduados_NaoGraduados_1_2 ...
   #Limpar um arquivo do censo, deixando graduados e não-graduados para fazer a PivotTablet ...
   path = ['/home/essantos/Downloads/ibge-2010/processados/Sul/', '/home/essantos/Downloads/ibge-2010/processados/Centro_Oeste/']
   ##names = ['Amostra_Pessoas_41_PR_Fase1.csv','Amostra_Pessoas_42_SC_Fase1.csv'], ['Amostra_Pessoas_50_MS_Fase1.csv',  'Amostra_Pessoas_51_MT_Fase1.csv']
   names = ['Amostra_Pessoas_41_PR_Fase1.csv','Amostra_Pessoas_42_SC_Fase1.csv','Amostra_Pessoas_43_RS_Fase1.csv'], ['Amostra_Pessoas_50_MS_Fase1.csv',  'Amostra_Pessoas_51_MT_Fase1.csv','Amostra_Pessoas_52_GO_Fase1.csv','Amostra_Pessoas_53_DF_Fase1.csv']
   for i in range(len(names)):
       namess = len(names[i])
       for j in range(namess):
           name = str(names[i][j])
           ibge_functions.Limpeza_Arquivo_Censo_Graduados_NaoGraduados_1_2(path[i],name,i)
           
   #Pivot_Table_Censo - Feminino
   #Criar uma PivotTablet para o ensino superior, usando o arquivo do Censo 
   path = ['/home/essantos/Downloads/ibge-2010/processados/Sul/Graduados_NaoGraduados/', '/home/essantos/Downloads/ibge-2010/processados/Centro_Oeste/Graduados_NaoGraduados/']
   #names = ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados.csv'], ['Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados.csv']
   names = ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_43_RS_Fase1_Graduados_NaoGraduados.csv'], ['Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_52_GO_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_53_DF_Fase1_Graduados_NaoGraduados.csv']
   gender = "F"
   for i in range(len(names)):
       namess = len(names[i])
       for j in range(namess):
           name = str(names[i][j])
           ibge_functions.Pivot_Table_Censo(path[i],name,gender,i)

   #Pivot_Table_Censo - Masculino
   #Criar uma PivotTablet para o ensino superior, usando o arquivo do Censo 
   path = ['/home/essantos/Downloads/ibge-2010/processados/Sul/Graduados_NaoGraduados/', '/home/essantos/Downloads/ibge-2010/processados/Centro_Oeste/Graduados_NaoGraduados/']
   #names = ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados.csv'], ['Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados.csv']
   names = ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_43_RS_Fase1_Graduados_NaoGraduados.csv'], ['Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_52_GO_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_53_DF_Fase1_Graduados_NaoGraduados.csv']
   gender = "M"
   for i in range(len(names)):
       namess = len(names[i])
       for j in range(namess):
           name = str(names[i][j])
           ibge_functions.Pivot_Table_Censo(path[i],name,gender,i)
           

   #Pivot_Table_Censo - Geral( Feminino + Masculino)
   #Criar uma PivotTablet para o ensino superior, usando o arquivo do Censo 
   path = ['/home/essantos/Downloads/ibge-2010/processados/Sul/Graduados_NaoGraduados/', '/home/essantos/Downloads/ibge-2010/processados/Centro_Oeste/Graduados_NaoGraduados/']
   #names = ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados.csv'], ['Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados.csv']
   names = ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_43_RS_Fase1_Graduados_NaoGraduados.csv'], ['Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_52_GO_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_53_DF_Fase1_Graduados_NaoGraduados.csv']
   gender = "G"
   for i in range(len(names)):
       namess = len(names[i])
       for j in range(namess):
           name = str(names[i][j])
           ibge_functions.Pivot_Table_Censo(path[i],name,gender,i)
           

   #Função para mover arquivos para as pastas desejadas ...  
   estado = ['Sul']
   opcao =[1] 
   for i in range(len(estado)):
       ibge_functions.move_temp(estado[i],opcao[i])     
 
   #PivotTableFinal para todos os estados ...
   pivotfinal = []
   estado = ['Sul','Centro_Oeste']
   gender = [1,2,3]
   path = ["/home/essantos/Downloads/ibge-2010/processados/Sul/PivotTablet/Masculino/", "/home/essantos/Downloads/ibge-2010/processados/Sul/PivotTablet/Feminino/", "/home/essantos/Downloads/ibge-2010/processados/Sul/PivotTablet/"], ["/home/essantos/Downloads/ibge-2010/processados/Centro_Oeste/PivotTablet/Masculino/", "/home/essantos/Downloads/ibge-2010/processados/Centro_Oeste/PivotTablet/Feminino/", "/home/essantos/Downloads/ibge-2010/processados/Centro_Oeste/PivotTablet/"]
   name = ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv'], ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv'], ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados_PivotTablet.csv'], ['Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv'], ['Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv'], ['Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados_PivotTablet.csv',  'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados_PivotTablet.csv']
   linha = 0
   for x in range(len(estado)):
        for i in range(len(path[x])):
            #print(path[x][i])
            coluna = 0
            for j in range(len(name[i])):
                #print("linha/coluna", linha,coluna)
                #print('j:',j)
                pivotfinal.append(ibge_functions.SomaPivotTable(str(path[x][i]),str(name[linha][coluna]),i))
                #print(str(path[x][i]),str(name[linha][coluna]),i)
                coluna = coluna + 1
            ibge_functions.Reduzir(pivotfinal,estado[x],gender[i])   
            #print(estado[x],gender[i])   
            linha = linha +1    
            #print("...")
        #print("...")        
        #print(estado[x])   
   
       
   # Limpeza_Arquivo_Censo_Graduados_2
   path = ['/home/essantos/Downloads/ibge-2010/processados/Sul/Graduados_NaoGraduados/', '/home/essantos/Downloads/ibge-2010/processados/Centro_Oeste/Graduados_NaoGraduados/']
   ##names = ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados.csv'], ['Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados.csv']
   names = ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_43_RS_Fase1_Graduados_NaoGraduados.csv'], ['Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_52_GO_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_53_DF_Fase1_Graduados_NaoGraduados.csv']
   for i in range(len(names)):
       namess = len(names[i])
       for j in range(namess):
           name = str(names[i][j])
           ibge_functions.Limpeza_Arquivo_Censo_Graduados_2(path[i],name,i)    
   
   #Função para juntar CSVs
   path = ['/home/essantos/Downloads/ibge-2010/processados/Sul/Clean_Graduados', '/home/essantos/Downloads/ibge-2010/processados/Sul/Graduados_NaoGraduados'], ['/home/essantos/Downloads/ibge-2010/processados/Centro_Oeste/Clean_Graduados', '/home/essantos/Downloads/ibge-2010/processados/Centro_Oeste/Graduados_NaoGraduados'], ['/home/essantos/Downloads/ibge-2010/processados/CSVs_ArquivoFinalGraduados', '/home/essantos/Downloads/ibge-2010/processados/CSVs_ArquivoFinalGraduados_NaoGraduados']
   estados = ['Sul', 'Centro_Oeste','Brasil']  
   opcao = ['Graduados', 'Não-Graduados']
   coluna = 0
   for i in range(len(opcao)):   
       for j in range(len(estados)):    
            ibge_functions.JuntarCSVs(path[j][coluna],estados[j],opcao[i])  
            #print(path[j][coluna],estados[j],opcao[i])             
       coluna = coluna + 1     

pass     


# Fase 10: Essa é a primeira fase que você faz no dia a dia. Aqui você começa a fazer a análise dos dados
# Fase 10: Análise Descritiva ... ...
#if fase >= 10:
if fase == 10:
    pass

# Fase 11: Análise Exploratória ...
if fase == 11:
    pass

# Fase 12: Resultados da Análise ...
if fase == 12: 
    pass

# Fase 99: Aqui você pode explorar coisas novas que não afetam os dados anteriores.
#if fase >= 99:
#if fase == 99:
#    path = '/home/essantos/Downloads/ibge-2010/processados/teste/'
#    pass
