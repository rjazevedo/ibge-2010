
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
import ibge_functions_exploratory_analysis_1
import ibge_functions_descriptive_analysis_1
import ibge_variable
import ibge_functions_preprocessing
import ibge_functions_results
import ibge_functions_results_1
import QP6
import logging

# Modificando o comportamento do pandas para mostrar os erros de atribuição para eliminar os warnings - Rafael 20250413
# pd.options.mode.chained_assignment = 'raise'

# #Esse arquivo não pode conter código que não seja chamada de funções e verificação de parâmetros
# parser = argparse.ArgumentParser()
# parser.add_argument('-f', '--fase', type=int, help='Indica a fase do fluxo para começar a execução')
# args = parser.parse_args()
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fase', type=int, help='Descrição do argumento -f')
parser.add_argument('--plot', action='store_true', help='Descrição do argumento --plot')
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
    ibge_functions.ibge_cursos_profissoes()
   
    ## ibge_functions.ibge_relacionamentos_cursos_profissoes()

    ## ibge_functions.ibge_corte_CBO()

    ibge_functions.ibge_idas_voltas_cursos_profissoes()

    ibge_functions.ibge_trabalho_recenseados()
    pass

    

# Fase 20: Análise Exploratória ...
if fase == 20:  #QP1
    # Função para:
    # - clusterização com k=3, 
    # - geração do gráfico K-Means com K=3 (10% - Todos os Cursos - Clusterização) 
    # - geração do arquivo Kmeans3_T.csv   
    ################## ------------------------ 
    # ibge_functions.Profissoes_Cursos()    
    ## Empregabilidade x Salario
    # ibge_functions.median_salario() 
    # ibge_functions_exploratory_analysis.separar_cursos_por_clusters()
    # ibge_functions_exploratory_analysis.medianas_por_clusters()
    # ibge_functions.Salarios() 
    # 
    ibge_functions.Salarios_cursos_commaisprofissoes() 

    # ibge_functions.Soma_PivotTable()
    # ibge_functions.Coluna_Empregabilidade()
    
    # ibge_functions.Empregabilidade() 
    # ibge_functions.Empregabilidade_cursos_commaisprofissoes() 
    # ibge_functions_exploratory_analysis.correlacao_empregabilidade_salario() #...Gráfico 

    # ibge_functions_exploratory_analysis.plot_selected_courses()
    # ibge_functions.plot_selected_courses_1()
    pass

# Fase 30: Resultados da Análise ...
if fase == 30:  #QP2
    ## Funções para 10%  
    ## Geração do dataframes femininos e masculinos
    ibge_functions.Filtro_Masculino_Feminino() 
    ## Geração dos Arquivos de idas e voltas Femininas e Masculinas
    ibge_functions.Ida_Volta_Masculino_Feminino()
    ## Limpeza dos arquivos  de idas e voltas Femininas e Masculinas
    ibge_functions.Tabela_Ida_Volta_Masculino_Feminino() 
    ## Geração dos gráficos:
    ##  - Profissões e Cursos-Masculino (10%-Cursos e Profissões do Censo-Masculino)
    ##  - Profissões e Cursos-Feminino  (10%-Cursos e Profissões do Censo-Feminino)   
    ibge_functions.Profissoes_Cursos_Masculino_Feminino()     
    pass

if fase == 31:
    #QP1 é a fase 20
    pass 
if fase == 32:
    #QP2 é a fase 30
    pass 
if fase == 33:   
    ##QP3
    ################# -------------------------        
    ibge_functions.Ida_Volta_Masculino_Feminino_100()
    ################# -------------------------        
    ibge_functions.Tabela_Ida_Volta_Masculino_Feminino_100()
    # Funciona, mas salva csvs. Comentei para usar como dataframes!
    # ibge_functions.PlotOriginal_AdicionaColunaGenero_100()
    ################# -------------------------        
    ibge_functions.Juntar_10Porcento_Genero()
    ################# -------------------------        
    ibge_functions_results.Filtrar_Tabela_10Porcento_Genero()
    # geração do gráfico: 
    # - Pontos originais, masculinos e femininos (10%-Visualização dos três gráficos - Genero - Kmeans3)
    ################# -------------------------         
    ibge_functions_results.Kmeans3_T_Grafico_Genero()

    # Não utilizadas ...
    # ibge_functions.Profissoes_Cursos_Masculino_Feminino_100()  

    # Funções para 10% ... comentadas 
    # Funciona, mas salva csvs. Comentei para usar como dataframes!
    # ibge_functions.PlotOriginal_AdiciconaColunaGenero()
    # ibge_functions.JuntaTabelas() 
    
    
    pass

if fase == 34: #...
    # # QP3 continuação
    # #  Funções que faltam ...
    # #  1-  Gráfico dos gêneros separados por clusters
    #    https://colab.research.google.com/drive/1znpX4cXQTDgCsiZYS9kNl1UbgL3RudAB?authuser=1
    ################# -------------------------        
    ibge_functions.fill_cluster_column_Genero()
    ################# -------------------------       
    # ibge_functions_results.separate_clusters_Genero()
    # ibge_functions.Kmeans3_T_Grafico_Genero_Clusters()
    # ibge_functions_results.deslocamento()
    # ibge_functions_results.deslocamentos_maioresdistancias()
    # ibge_functions_results.deslocamento_clusters()
    # ibge_functions_results.deslocamentos_maioresdistancias_clusters()
    # ibge_functions_results.extract_courses_F()
    # ibge_functions_results.extract_courses_Cluster0()
    # ibge_functions_results_1.extract_courses_Cluster1()
    # ibge_functions_results_1.extract_courses_Cluster2()
    # ibge_functions_results. extract_courses_Cluster0_Correspondente()
    # ibge_functions_results.extract_courses_Correspondentes_F()
    # 
    ibge_functions_results_1.extract_courses_Correspondentes_F_1()
    # ibge_functions_results.extract_courses_M()
    # ibge_functions_results_1.extract_courses_M_1()
    # ibge_functions_results.extract_courses_Correspondentes_M()
    pass

if fase == 35:
    # ## QP3 continuação
    # #  2-  Profissões desequilibradas 
    #    # - Profissões desequilibradas - Pontos Selecionados(Grandes Desloamentos)  
    # # ...   
    #    # - Profissões desequilibradas - Quais as profissões onde homens e mulheres estão em clusters diferentes?
    # ibge_functions.dadosoriginais_resultados()
    # ibge_functions_results.resultados_filtragem_10_100()
    # ibge_functions_results.resultados_distancia()
    # ibge_functions_results.tabela_clusters_diferentes()
    # # - Profissões desequlibradas  - Gráfico com os pontos que mudaram de cluster e diagrama de Voronoi
    # ibge_functions_results.voronoi()
    # #  3-  Profissões equilibradas - 40%-60% ...
    #    # - Tabela com os pontos clusterizados contendo as porcentagens de masculinos e femininos
    # ibge_functions_results.Juntar_40_60Porcento_Genero()   
    ibge_functions_results.tabela() 
    # ibge_functions_results.separar_registros_por_cluster()
    #    # - Tabela com os pontos selecionados(40%-60%)
    # ibge_functions_results. pt_selecionados_40_60()
    # ibge_functions_results.tabela_40_60()
    #    # - Gráfico com os ponto selecionados(40%-60%)
    # ibge_functions_results.graf_selecionados_40_60()
    #    # - Plotar o gráfico das idades, usando o arquivo de femininos e masculinos! Com isso poderemos ver a distribuição das idades para o masculino e para o feminino!
    # ibge_functions.Ida_Volta_Idade_Gen()       
    # ibge_functions.Tabela_Ida_Volta_Idade_Gen()         
    # ibge_functions_results.Juntar_10Porcento_Idade_Gen() 
    # ibge_functions_results.Filtrar_Tabela_10Porcento_Idade_Gen()   
    # ibge_functions.Analise_Genero_FaixaEtaria()

    # # 4-  Gráfico dos vetores centrados em(0,0)    
    # # ibge_functions_results.vetores_Setas_Pontos()
    # ibge_functions_results.vetores_Setas_Masc_Fem()
    # ibge_functions_results.vetores_Setas_Setas_Masculino()
    # ibge_functions_results.vetores_Setas_Setas_Feminino()

    # #https://colab.research.google.com/drive/1znpX4cXQTDgCsiZYS9kNl1UbgL3RudAB?authuser=1#scrollTo=NTzZhdz0uo4g
    # #Kmeans3 - Copilot - Soma dos vetores(setas) femininos

    # ibge_functions_results.extract_courses_transicao()
    # ibge_functions_results.extract_courses_equidade()

    pass

if fase == 40:
    # #QP4
    # Funciona, mas salva csvs. Comentei para usar como dataframes!
    # ibge_functions.Filtro_Idade()  
    ibge_functions.Ida_Volta_Idade()
    ibge_functions.Tabela_Ida_Volta_Idade()   
    # Funciona, mas salva csvs. Comentei para usar como dataframes! 
    # ibge_functions.Adiciona_Coluna_Idade()     
    ibge_functions_results.Juntar_10Porcento_Idade() 
    ibge_functions_results.Filtrar_Tabela_10Porcento_Idade() 
    # Separar manualmente os clusters e depois rodar o codigo abaixo para gerar os gráficos de idades separados os clusters...
    # 11/04 ainda esta seperando manualmente? Não, ja foi automatizado!
    ibge_functions.fill_cluster_column()
    ibge_functions_results.separate_clusters()
    ibge_functions.Kmeans3_T_Grafico_Idade()     
    #  Funções que faltam ...
    # 1- Idade - Alguns pontos selecionados 
    # - Cluster 0
    # - Cluster 1
    # - Cluster 2
    ibge_functions.selecionados()  
    # Okay # 2- Idade - Selecionar somente os que tem mais de 80 anos
    # - Aposentados -  Formados em Medicina e com CBO (2211)  Médicos Gerais
    ibge_functions.Aposentados_maior80()
    # 3- Idade - Casos Administrativos: Descobrir quando alguém vira gerente gestor
    # - Olhar todos os médicos e ver na carreira deles, quando começam a pegar o código 1. Comparar com: 1342 - 1345 - 1348 - 1349
    # - Homens gestores e Mulheres gestoras (Homem e mulher, muda faixa de idade para virar gestores?)
    pass    
    
if fase == 50:
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
 
if fase == 100: # aqui é só de teste
    # #ibge_functions_results_1.plot_age_distribution_for_course_cbo()
    # QP3 ...
    # Análise de idade por CBO -  Gráficos de Cursos e CBOs ------------------------------------------------------------------------------------------
    # ibge_functions. plot_ida_volta_distribution_for_course_cbo()
    # #Análise de idade por CBO - Geração do Arquivo com as  idades  ---------------------------------------------------------------------------------
    # #ibge_functions_results_1.Analise_Genero_FaixaEtaria() 
    # ibge_functions_results_1.Analise_Genero_FaixaEtaria_1() 
    # #Análise de idade por CBO - Plot das idades para toda a base representativa  --------------------------------------------------------------------
    # ibge_functions_results_1.plot_gender_age_distribution() 
    # #Análise de idade por CBO - Plot das idades para toda os clusters  ------------------------------------------------------------------------------
    # ibge_functions_results_1.split_csv_by_cluster() 
    # ibge_functions.plot_gender_age_distribution_bycluster() 
    # #Análise de idade por CBO - Plot das idades para Curso/CBO  -------------------------------------------------------------------------------------
    # ibge_functions_results_1.extract_data_by_course_cbo()
    # ibge_functions_results_1.split_csv_by_cluster_1()
    # Geração de tabelas dos clusters -----------------------------------------------------------------------------------------------------------------
    # ibge_functions.save_csv_to_table()
    # # Diminuir Cursos e Cbos no Arquivo de Graduados e no Arquivo Pivot Table -----------------------------------------------------------------------
    # ibge_functions_results_1.diminuir_and_save_csv()
    # ibge_functions_results_1.transform_columns_to_int_and_save()
    # ibge_functions.ibge_cursos_filter_1()
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # #Idas e voltas para Cursos e CBOs Diminuidos ---------------------------------------------------------------------------------------------------
    # ibge_functions.ibge_idas_voltas_cursos_profissoes_1()
    # ibge_functions_results_1.voronoi_1()
    # -----------------------------------------------------
    # # ibge_functions_results_1.diminuir_and_save_csv_CBO()
    # # ibge_functions_results_1.transform_columns_to_int_and_save_CBO()
    #---------------------------------------------------------------
    # # ibge_functions_results_1.Ida_Volta_CBO()
    # # ibge_functions_results_1.Tabela_Ida_Volta_CBO()
    # -----------------------------------------------------
    # ibge_functions_results_1.diminuir_and_save_csv_CURSO()
    # # ibge_functions_results_1.Ida_Volta_Curso()
    # # ibge_functions_results_1.Tabela_Ida_Volta_Curso()
    


    # #Tem que ver se isso de ver de onde veio vai ser fácil: se todos os pontos que foram agrupados vieram do mesmo cluster, ok, sem problemas. -------
    # #Mas e se vieram de clusters diferentes? ---------------------------------------------------------------------------------------------------------
    # #Veja isso com umas duas tabelas, onde você tem os Cursos e CBOs e consegue comparar elas----------------------------------------------------------
    # ibge_functions_descriptive_analysis_1.process_kmeans_results()
    # ibge_functions_descriptive_analysis_1.transform_and_reduce_columns()
    # ibge_functions_descriptive_analysis_1.update_processed_kmeans_results()
    # ibge_functions_descriptive_analysis_1.fill_course_and_cbo_names()
    # ibge_functions_descriptive_analysis_1.split_clusters_to_files()

    # Clusterização - Diminuição dos digitos de cursos e cbos
    # ibge_functions_exploratory_analysis_1.clusterizacao_metodo_cotovelo_e_kmeans2() # somente teste, não será utilizada 
    # ibge_functions_exploratory_analysis_1.Profissoes_Cursos_Menor_CBO_Curso() # CBOs 3 - Cursos 2

    # #Caracterização dos Clusters
    ibge_functions.split_Kmeans3_T_Profissoes_Cursos_Menor_CBO_by_cluster()
    # ibge_functions_results_1.caracterizar_cluster0()

    #QP6
    # QP6.transform_categoria_emprego()
    # QP6.classify_employment_stability()
    # QP6.data_processed_groupby()
    # QP6.plot_employment_by_gender()

    pass
