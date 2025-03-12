
#pip install ibge-parser

# inclua todos os demais imports aqui
import argparse
import sys
import os
import numpy as np
import ibgeparser
import pandas as pd
from pandas import DataFrame
import glob
from functools import reduce
#import da classe principal
from ibgeparser.microdados import Microdados
#import dos enums para facilitar as buscas
from ibgeparser.enums import Anos, Estados, Modalidades
#import original.ibge_functions
import ibge_functions
import ibge_functions_exploratory_analysis
import ibge_functions_descriptive_analysis
import ibge_variable
import ibge_functions_preprocessing
import ibge_functions_results
import logging

# Esse arquivo não pode conter código que não seja chamada de funções e verificação de parâmetros
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fase', type=int, help='Indica a fase do fluxo para começar a execução')
args = parser.parse_args()

# Setup do pacote logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if args.fase is None:
     fase = 10
else:
     fase = args.fase

# Fase 0: Download dos dados do IBGE da web
#if fase >= 0:
if fase == 0:
    # for p in ["microdados-ibge/original", "microdados-ibge/processados", "microdados-ibge/graficos"]:
    #   if not os.path.exists(p):
    #       os.makedirs(p)
    for p in ["microdados-ibge/original", "processados", "graficos"]:
      if not os.path.exists(p):
          os.makedirs(p)

    ibge_functions.ibge_download() 

# Fase 1: Filtrar somente os dados relevantes. Aqui significa que 
# você precisa filtrar todos os dados que possam ser utilizados no futuro.
#if fase >= 1:
if fase == 1:
    ibge_functions.ibge_filter()

# Fase 2: Limpeza dos dados. Agora começa a processar algo mais complexo desde que seja definitivo
# Pré-Processamento
#if fase >= 2:
if fase == 2:

    ibge_functions.ibge_Graduados_NaoGraduados()

    ibge_functions.ibge_Pivot_Feminino()

    ibge_functions.ibge_Pivot_Masculino()

    ibge_functions.ibge_Pivot_Geral()          

    ibge_functions.ibge_PivotTableFinal()

    ibge_functions.ibge_Graduados()
    
    ibge_functions.ibge_JuntarCSVs()    
      
    ibge_functions_preprocessing.filtrar_por_genero()    
    
# Fase 10: Essa é a primeira fase que você faz no dia a dia. Aqui você começa a fazer a análise dos dados
# Fase 10: Análise Descritiva ... ...
#if fase >= 10:
if fase == 10:
    #https://colab.research.google.com/drive/1_Nx4oOzrgCQvSolh9XG-UgWTQ508Md1M?authuser=1#scrollTo=o9GsbqjctkkL
    ################# ------------------------- 
    ibge_functions.ibge_cursos_profissoes()
   
    ## ibge_functions.ibge_relacionamentos_cursos_profissoes()

    ## 
    ibge_functions.ibge_corte_CBO()

    ################# ------------------------- 
    ibge_functions.ibge_idas_voltas_cursos_profissoes()

    ################# ------------------------- 
    ibge_functions.ibge_trabalho_recenseados()
    pass

    

# Fase 20: Análise Exploratória ...
if fase == 20:  #QP1
    # Função para:
    # - clusterização com k=3, 
    # - geração do gráfico K-Means com K=3 (10% - Todos os Cursos - Clusterização) 
    # - geração do arquivo Kmeans3_T.csv   
    ################## ------------------------ 
    ibge_functions.Profissoes_Cursos()    
    # ## Empregabilidade x Salario
    ibge_functions.median_salario() 
    ibge_functions_exploratory_analysis.separar_cursos_por_clusters()
    ibge_functions_exploratory_analysis.medianas_por_clusters()
    ibge_functions.Salarios() 
    ibge_functions.Salarios_cursos_commaisprofissoes() 

    ibge_functions.Soma_PivotTable()
    ibge_functions.Coluna_Empregabilidade()
    
    ibge_functions.Empregabilidade() 
    ibge_functions.Empregabilidade_cursos_commaisprofissoes() 
    # ibge_functions_exploratory_analysis.correlacao_empregabilidade_salario() ...Gráfico 

    ibge_functions_exploratory_analysis.plot_selected_courses()
    ibge_functions.plot_selected_courses_1()
    pass

# Fase 30: Resultados da Análise ...
if fase == 30:  #QP2
    ## Funções para 10%  
    ## Geração do dataframes femininos e masculinos
    #
    ibge_functions.Filtro_Masculino_Feminino() 
    ## Geração dos Arquivos de idas e voltas Femininas e Masculinas
    # 
    ibge_functions.Ida_Volta_Masculino_Feminino()
    ## Limpeza dos arquivos  de idas e voltas Femininas e Masculinas
    # 
    ibge_functions.Tabela_Ida_Volta_Masculino_Feminino() 
    ## Geração dos gráficos:
    ##  - Profissões e Cursos-Masculino (10%-Cursos e Profissões do Censo-Masculino)
    ##  - Profissões e Cursos-Feminino  (10%-Cursos e Profissões do Censo-Feminino)   
    # 
    ibge_functions.Profissoes_Cursos_Masculino_Feminino()     
    pass

if fase == 31:
    #QP1 é a fase 20
    pass 
if fase == 32:
    #QP2 é a fase 30
    pass 
if fase == 33:   
    # ##QP3
    # ################# -------------------------        
    # ibge_functions.Ida_Volta_Masculino_Feminino_100()
    # ################# -------------------------        
    # ibge_functions.Tabela_Ida_Volta_Masculino_Feminino_100()
    # # Funciona, mas salva csvs. Comentei para usar como dataframes!
    # # ibge_functions.PlotOriginal_AdicionaColunaGenero_100()
    # ################# -------------------------        
    # ibge_functions.Juntar_10Porcento_Genero()
    # ################# -------------------------        
    # ibge_functions_results.Filtrar_Tabela_10Porcento_Genero()
    # # geração do gráfico: 
    # # - Pontos originais, masculinos e femininos (10%-Visualização dos três gráficos - Genero - Kmeans3)
    # ################# -------------------------         
    # ibge_functions_results.Kmeans3_T_Grafico_Genero()

    # # Não utilizadas ...
    # # ibge_functions.Profissoes_Cursos_Masculino_Feminino_100()  

    # # Funções para 10% ... comentadas 
    # # Funciona, mas salva csvs. Comentei para usar como dataframes!
    # # ibge_functions.PlotOriginal_AdiciconaColunaGenero()
    # # ibge_functions.JuntaTabelas()
    
    # #  Funções que faltam ...
    # #  1-  Gráfico dos gêneros separados por clusters
    #    # https://colab.research.google.com/drive/1znpX4cXQTDgCsiZYS9kNl1UbgL3RudAB?authuser=1
    # ################# -------------------------        
    # ibge_functions.fill_cluster_column_Genero()
    # ################# -------------------------       
    # ibge_functions_results.separate_clusters_Genero()
    # ibge_functions.Kmeans3_T_Grafico_Genero_Clusters()
    # 
    ibge_functions_results.deslocamento_clusters()
    # #  2-  Profissões desequilibradas 
    #    # - Profissões desequilibradas - Pontos Selecionados(Grandes Desloamentos) 
    #    # - Profissões desequilibradas - Quais as profissões onde homens e mulheres estão em clusters diferentes?
    #    # - Profissões desequlibradas  - Gráfico com os pontos que mudaram de cluster e diagrama de Voronoi
    # #  3-  Profissões equilibradas - 40%-60% ...
    #    # - Tabela com os pontos clusterizados contendo as porcentagens de masculinos e femininos
    #    # - Tabela com os pontos selecionados(40%-60%)
    #    # - Gráfico com os ponto selecionados(40%-60%)
    #    # - Plotar o gráfico das idades, usando o arquivo de femininos e masculinos! Com isso poderemos ver a distribuição das idades para o masculino e para o feminino!
    # #  4-  Gráfico dos vetores centrados em(0,0)
    
    # # pass

if fase == 34:
    # #QP4
    # Funciona, mas salva csvs. Comentei para usar como dataframes!
    # ibge_functions.Filtro_Idade()

    ################# -------------------------     
    ibge_functions.Ida_Volta_Idade()
    ################# -------------------------     
    ibge_functions.Tabela_Ida_Volta_Idade()   
    # Funciona, mas salva csvs. Comentei para usar como dataframes! 
    # ibge_functions.Adiciona_Coluna_Idade()     
    ################# -------------------------     
    ibge_functions_results.Juntar_10Porcento_Idade() 
    ################# ------------------------- 
    ibge_functions_results.Filtrar_Tabela_10Porcento_Idade() 
    # Separar manualmente os clusters e depois rodar o codigo abaixo para gerar os gráficos de idades separados os clusters...
    ################# -------------------------     
    ibge_functions.fill_cluster_column()
    ################# -------------------------     
    ibge_functions_results.separate_clusters()
    ibge_functions.Kmeans3_T_Grafico_Idade()       
    
     #  Funções que faltam ...
     # 1- Idade - Alguns pontos selecionados 
       # - Cluster 1
       # - Cluster 2
     # Okay # 2- Idade - Selecionar somente os que tem mais de 80 anos
       # - Aposentados -  Formados em Medicina e com CBO (2211)  Médicos Gerais
    ################# -------------------------     
    ibge_functions.Aposentados_maior80()
     # 3- Idade - Casos Administrativos: Descobrir quando alguém vira gerente gestor
       # - Olhar todos os médicos e ver na carreira deles, quando começam a pegar o código 1. Comparar com: 1342 - 1345 - 1348 - 1349
       # - Homens gestores e Mulheres gestoras (Homem e mulher, muda faixa de idade para virar gestores?)
    pass    
    
if fase == 35:
   # #QP5
   # Funções que faltam ...
   # 1- BoxPlot de salários separados por clusters
   # 2- BoxPlot de salários separados por faixa etária (idades)  - Idades por Cluster (Grupos)
   # 3- BoxPlot de salários separados por gênero                 - Gênero por Clusters (Grupos)	
   # 4- Tabela: O maior e o menor de cada um dos pontos dentro de cada cluster	
     # Tabela: Mediana de cada um dos pontos dentro de cada cluster  
   # Okay # 5- BoxPlot de salários para um determinado CBO por idade	
   # Preencher o arquivo Resultados_T_Filtrados_Kmeans3_Idade.csv manualmente ...
   ibge_functions.Salarios_CBO_Idade()
   # 6- Análise  de salário por gênero (Ser homem ou mulher implica em diferença salarial?)
     # Tabela - Mediana  Feminina 
     # Tabela - Mediana Masculina 	
     # BoxPlot da Mediana de três  profissões 
   # 7- Platô 
   # 8- 20% ida e 80% volta 


   pass
# Fase 99: Aqui você pode explorar coisas novas que não afetam os dados anteriores.
#if fase >= 99:
#if fase == 99:
#     pass
