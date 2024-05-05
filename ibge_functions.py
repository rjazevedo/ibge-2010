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
import ibge_functions_preprocessing
import ibge_functions_descriptiveanalysis
import ibge_functions_results
import logging
import io
import shutil

# Fase 0: Download dos dados do IBGE da web
def ibge_download():
    # Leia os dados do IBGE
    logging.info("Fazendo download dos dados do IBGE")    
    ano_ac = Anos.DEZ
    modalidades_ac = [Modalidades.PESSOAS]
    estados = ibge_variable.estados()

    for estados_ac in estados:
        logging.info("Acessando o estado {} dos dados do IBGE".format(estados_ac))
        # original.ibge_functions.function_obterdados_especificacao_coluna(ano_ac, estados_ac, modalidades_ac)
        ibge_functions_preprocessing.function_obterdados_especificacao_coluna(ano_ac, estados_ac, modalidades_ac)

    source_dir = "microdados-ibge"
    destination_dir = "microdados-ibge/original"

    # Crie o diretório de destino se ele não existir
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Obtenha uma lista de todos os arquivos .csv no diretório de origem
    csv_files = glob.glob(os.path.join(source_dir, "Amostra_Pessoas_*.csv"))

    # Copie cada arquivo .csv para o diretório de destino
    for file in csv_files:
        shutil.copy(file, destination_dir)

    logging.info("Todos os arquivos .csv copiados para microdados-ibge/original")

    return

# Fase 1: Filtrar somente os dados relevantes. Aqui significa que 
# você precisa filtrar todos os dados que possam ser utilizados no futuro.
def ibge_filter():
    logging.info("Filtrando as colunas necessárias")    
    # path  = ibge_variable.paths(1,1)
    path  = ibge_variable.paths(1)
    for n in ibge_variable.names(1):
        ibge_functions_preprocessing.Filtrar_Dados_Censo(path[0],n,0)    
        # print(path[0])         
    return

def ibge_Graduados_NaoGraduados():
    logging.info("Salvando os arquivos de Graduados e Não-Graduados")    
    path  = ibge_variable.paths(2)
    names = ibge_variable.names(2)
    for j in range(len(names)):      
        ibge_functions_preprocessing.Limpeza_Arquivo_Censo_Graduados_NaoGraduados_1_2(path[0],names[j],0)
    return

# def ibge_Pivot_Feminino():
#     pivotfinal = []
#     logging.info("Gerando a Pivot Table Feminina")    
#     gender = "F"
#     path = ibge_variable.paths(3)
#     names = ibge_variable.names(3)
#     for i in range(len(names)):
#         #ibge_functions_preprocessing.Pivot_Table_Censo(path[0],names[i],gender,i)
#         #X =  ibge_functions_preprocessing.Pivot_Table_Censo(path[0],names[i],gender,i)
#         #print(X)
#         #pivotfinal.append(ibge_functions_preprocessing.SomaPivotTable(X))
#         X = ibge_functions_preprocessing.Pivot_Table_Censo(path[0],names[i],gender,i)
#         print(i, X)
#         pivotfinal.append(X)
#     ibge_functions_preprocessing.Reduzir(pivotfinal,"Brasil",2)     
#     return

def ibge_Pivot_Feminino():
    pivotfinal = []
    logging.info("Gerando a Pivot Table Feminina")    
    gender = "F"
    path = ibge_variable.paths(3)
    names = ibge_variable.names(3)
    for i in range(len(names)):
        ibge_functions_preprocessing.Pivot_Table_Censo(path[0],names[i],gender,i)        
    return

def ibge_Pivot_Masculino():
    logging.info("Gerando a Pivot Table Masculina")    
    gender = "M"
    path = ibge_variable.paths(3)
    names = ibge_variable.names(3)
    for i in range(len(names)):
        ibge_functions_preprocessing.Pivot_Table_Censo(path[0],names[i],gender,i)
    return

def ibge_Pivot_Geral():
    logging.info("Gerando a Pivot Table Geral")    
    gender = "G"
    path = ibge_variable.paths(3)    
    names = ibge_variable.names(3)
    for i in range(len(names)):
        ibge_functions_preprocessing.Pivot_Table_Censo(path[0],names[i],gender,i)
    return

def ibge_PivotTableFinal():
    logging.info("Gerando a Pivot Table Final")   
    pivotfinal = []
    estado = ['Brasil']
    gender = [1,2,3]
    path = ibge_variable.paths(7)
    name = ibge_variable.names(4)
    for i in range(len(gender)):
        for x in range(len(name[i])):
            pivotfinal.append(ibge_functions_preprocessing.SomaPivotTable(path[i],name[i][x],i))
        ibge_functions_preprocessing.Reduzir(pivotfinal,estado[0],gender[i])   
    return

def ibge_Graduados():
     logging.info("Salvando os arquivos de Graduados ")   
     path = ibge_variable.paths(3)
     names = ibge_variable.names(3)
     for i in range(len(names)):
     #for state_name in names:
         ibge_functions_preprocessing.Limpeza_Arquivo_Censo_Graduados_2(path[0],names[i],0)   
     return

def ibge_JuntarCSVs():
     logging.info("Gerando Arquivos Finais")  
     opcao = ['Graduados', 'Não-Graduados']
     path = ibge_variable.paths(10)
     for i in range(len(opcao)):   
        #  ibge_functions_preprocessing.JuntarCSVs(path[i],opcao[i],dir)
         ibge_functions_preprocessing.JuntarCSVs(path[i],opcao[i])
     return


## Fase 10: Essa é a primeira fase que você faz no dia a dia. Aqui você começa a fazer a análise dos dados
#  Fase 10: Análise Descritiva ... ...
def ibge_cursos_profissoes():
    
    # Cursos e Profissões do Censo ...
    path = ibge_variable.paths(12)
    name = ibge_variable.names(5)
    ibge_functions_descriptiveanalysis.ibge_cnae(path[0],name[0],0)
    ibge_functions_descriptiveanalysis.ibge_cbo(path[0],name[1],0)
    ibge_functions_descriptiveanalysis.ibge_cursos(path[0],name[2],0)
    name  = ibge_variable.names(6)
    QuantidadeCursosCenso = ibge_functions_descriptiveanalysis.ibge_qtdadeCursos(path[0],name[2])
    print(" Quantidade de Cursos do Censo:", QuantidadeCursosCenso) 
    QuantidadeProfissoesCenso = ibge_functions_descriptiveanalysis.ibge_qtdadeProfissoes(path[0],name[1])
    print(" Quantidade de Profissões do Censo:", QuantidadeProfissoesCenso)
    print(" ")

    # Cursos e Profissões das pessoas recenseadas ...
    path1 = ibge_variable.paths(11)
    name1 = ibge_variable.names(7)
    # QuantidadeCursosRecenseados= ibge_functions_descriptiveanalysis.ibge_qtdadeCursos_recenseados(path[0],name[2],0,path1[0],name1[0])
    QuantidadeCursosRecenseados = ibge_functions_descriptiveanalysis.ibge_qtdadeCursos_recenseados(path1[0],name1[0])
    print(" Quantidade de Cursos associados a população Recenseada e graduada:",QuantidadeCursosRecenseados)
    QuantidadeProfissoesRecenseados = ibge_functions_descriptiveanalysis.ibge_qtdadeProfissoes_recenseados(path1[0],name1[0])
    print(" Quantidade de Profissões associadas a população Recenseada e graduada:",QuantidadeProfissoesRecenseados)
    print(" ")
    # Cursos e Profissões associadas ao Gênero Feminino
    QuantidadeCursosRecenseadosFemininos = ibge_functions_descriptiveanalysis.ibge_qtdadeCursos_recenseados_feminino(path1[0],name1[0])
    print(" Quantidade de Cursos associadas a população Feminina Recenseada e graduada:",QuantidadeCursosRecenseadosFemininos)
    QuantidadeProfissoesRecenseadosFemininos =  ibge_functions_descriptiveanalysis.ibge_qtdadeProfissoes_recenseados_feminino(path1[0],name1[0])
    print(" Quantidade de Profissões associadas a população Feminina Recenseada e graduada:",QuantidadeProfissoesRecenseadosFemininos)
    # Cursos e Profissões associadas ao Gênero Masculino
    QuantidadeCursosRecenseadosMasculinos = ibge_functions_descriptiveanalysis.ibge_qtdadeCursos_recenseados_masculino(path1[0],name1[0])
    print(" Quantidade de Cursos associadas a população Masculina Recenseada e graduada:",QuantidadeCursosRecenseadosMasculinos)
    QuantidadeProfissoesRecenseadosMasculinos =  ibge_functions_descriptiveanalysis.ibge_qtdadeProfissoes_recenseados_masculino(path1[0],name1[0])
    print(" Quantidade de Profissões associadas a população Masculina Recenseada e graduada:",QuantidadeProfissoesRecenseadosMasculinos)
    return


def ibge_relacionamentos_cursos_profissoes():
    path = ibge_variable.paths(11)
    name = ibge_variable.names(7)
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)

    # Usar essa função para obter os primeiros plots sem porcentagem
    # ibge_functions_descriptiveanalysis.relacionamentos_fortes_naofortes_cursos_profissoes_plot1(path,name,path1,name1)

    # Usar essa função para obter os primeiros plots com porcentagem (7% ou 10%)     
    # ibge_functions_descriptiveanalysis.relacionamentos_fortes_naofortes_cursos_profissoes_plot2(path,name,path1,name1)
    return

def ibge_corte_CBO():
    path = ibge_variable.paths(11)
    name = ibge_variable.names(7)
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)

    # Usar essa função para obter os primeiros plots com porcentagem ( 10%)     
    ibge_functions_descriptiveanalysis.relacionamentos_fortes_naofortes_cursos_profissoes_plot10(path,name,path1,name1)
    return

def ibge_idas_voltas_cursos_profissoes():
    path = ibge_variable.paths(11)
    name = ibge_variable.names(7)
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)
    # ...
    ibge_functions_descriptiveanalysis.Ida_Volta(path,name,path1,name1)
    
    return

def ibge_trabalho_recenseados():
    path = ibge_variable.paths(11)
    name = ibge_variable.names(7)
    path1 = ibge_variable.paths(12)
    name1 = ibge_variable.names(6)
    # ...
    ibge_functions_descriptiveanalysis.Tabela_Censo_CbosFortes_Fracos_Familia1_Familia2(path,name,path1,name1)
    return


# Fase 20: Análise Exploratória ...

# def Profissoes_Cursos():
#     return



# Fase 30: Resultados da Análise ...    
def Profissoes_Cursos_Masculino():
    return
def Profissoes_Cursos_Feminino():  
    return
# Fase 31
# ...

# Fase 32
# ...

# Fase 33
# QP3
# def Genero_Profissoes_Masc_Fem_Grupos():
#     # Ler dataframes
#     # Chamar funções com os dataframes como parâmetros
#     ibge_functions_results.Genero_Profissoes_Masc_Fem_Grupo1()
#     ibge_functions_results.Genero_Profissoes_Masc_Fem_Grupo2()
#     ibge_functions_results.Genero_Profissoes_Masc_Fem_Grupo3()
#     return

# def Genero_Profissoes_Desequilibradas():
#     ibge_functions_results.Genero_Profissoes_Desequilibradas_Deslocamentos()
#     ibge_functions_results.Genero_Profissoes_Desequilibradas_Mudanca_Voronoi()
#     return

# def Genero_Profissoes_Equilibradas():
#     ibge_functions_results.Genero_Profissoes_Equilibradas_tabela()
#     ibge_functions_results.Genero_Profissoes_Equilibradas_Tab_Sel()
#     ibge_functions_results.Genero_Profissoes_Equilibradas_Graf_Sel()
#     ibge_functions_results.Genero_Profissoes_Equilibradas_Gen_Idade_Fem()
#     ibge_functions_results.Genero_Profissoes_Equilibradas_Gen_Idade_Masc()
#     return
 
# Fase 34
# ...

# Fase 35
# ...