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
import ibge_functions_descriptive_analysis_1




def Cursos_CBOs_selecionados(cluster):
    if cluster == 0:
        # Seleciona os arquivos do cluster 0
        csv_idade = "graficos/Resultados_T_Filtrados_Kmeans3_Idade_Cluster0.csv"
        Curso = "721"
        CBO =   "2212"
    # if cluster == 1:
    #     # Seleciona os arquivos do cluster 1
    #     # csv_idade = pd.read_csv("graficos/Kmeans3_T_Salarios_certo_F.csv")
    # if cluster == 2:
    #     # Seleciona os arquivos do cluster 2
    #     # arquivos = glob.glob('/home/andre/Downloads/ibge/cluster_2/*.csv') 

    Idade_Plot(csv_idade,CBO,Curso)
   
    return

def Idade_Plot(csv_idade,CBO,Curso):
    #Leitura de Arquivos CSVs ...
    X = pd.read_csv(csv_idade, sep=",")
    X = X.drop(columns=['Unnamed: 0'])
    #...

    I_25_29 = []
    I_30_39 = []
    I_40_49 = []
    I_50_59 = []
    I_60    = []
    orig    = []


    for i in range (len(X['Curso'])):
        if (str(X['Curso'][i]) == Curso and str(X['Cbo'][i]) == CBO):
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
            if(X['Idade'][i] == "O"):
                orig.append(X['Ida'][i])
                orig.append(X['Volta'][i])

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    ax.scatter([orig[0], I_25_29[0], I_30_39[0],I_40_49[0], I_50_59[0], I_60[0]], [orig[1], I_25_29[1], I_30_39[1],I_40_49[1], I_50_59[1], I_60[1]], color=['gray','blue','magenta','Darkgreen','red','black'])
    ax.annotate("", xy=(I_25_29[0], I_25_29[1]), xytext=(I_30_39[0], I_30_39[1]), arrowprops=dict(arrowstyle="<-", color='blue'))
    ax.annotate("", xy=(I_30_39[0], I_30_39[1]), xytext=(I_40_49[0], I_40_49[1]), arrowprops=dict(arrowstyle="<-", color='magenta'))
    ax.annotate("", xy=(I_40_49[0], I_40_49[1]), xytext=(I_50_59[0], I_50_59[1]), arrowprops=dict(arrowstyle="<-", color='Darkgreen'))
    ax.annotate("", xy=(I_50_59[0], I_50_59[1]), xytext=(I_60[0], I_60[1]), arrowprops=dict(arrowstyle="<-", color='red'))
    #ax.annotate("", xy=(I_60[0], I_60[1]), xytext=(I_60[0], I_60[1]), arrowprops=dict(arrowstyle="->", color='black'))
    ax.annotate("", xy=(orig[0], orig[1]), xytext=(orig[0], orig[1]), arrowprops=dict(arrowstyle="<-", color='gray'))

    #ax.scatter([ I_25_29[0], I_30_39[0],I_40_49[0], I_50_59[0], I_60[0]], [ I_25_29[1], I_30_39[1],I_40_49[1], I_50_59[1], I_60[1]], color=['blue','magenta','Darkgreen','red','black'])
    #ax.annotate("", xy=(I_25_29[0], I_25_29[1]), xytext=(I_30_39[0], I_30_39[1]), arrowprops=dict(arrowstyle="<-", color='blue'))
    #ax.annotate("", xy=(I_30_39[0], I_30_39[1]), xytext=(I_40_49[0], I_40_49[1]), arrowprops=dict(arrowstyle="<-", color='magenta'))
    #ax.annotate("", xy=(I_40_49[0], I_40_49[1]), xytext=(I_50_59[0], I_50_59[1]), arrowprops=dict(arrowstyle="<-", color='Darkgreen'))
    #ax.annotate("", xy=(I_50_59[0], I_50_59[1]), xytext=(I_60[0], I_60[1]), arrowprops=dict(arrowstyle="<-", color='red'))
    #ax.annotate("", xy=(I_60[0], I_60[1]), xytext=(I_60[0], I_60[1]), arrowprops=dict(arrowstyle="->", color='black'))



    plt.xlabel("Cursos")
    plt.ylabel("Profissões")
    #plt.title("10%  -  Visualização dos três gráficos - Idade - Ponto Separado")
    #plt.title("Idade - 721.0,MEDICINA,2211.0,MÉDICOS GERAIS")
    #plt.title("Idade - 724.0 ODONTOLOGIA - 2261.0 DENTISTAS")
    #plt.title("Idade -  723.0 ENFERMAGEM - 2221.0 PROFISSIONAIS DE ENFERMAGEM")

    #Cluster 2
    plt.title("Idade - 721.0,MEDICINA,2212.0,MÉDICOS ESPECIALISTAS")
    #plt.xlim(0.0, 100.0)
    #plt.ylim(0.0, 100.0)
    #plt.show()
    string = "Idade_721_MEDICINA_2212_MEDICOSESPECIALISTAS.png"
    save_results_to = 'graficos/'  
    plt.savefig(save_results_to + string) 

    return
def extract_courses_M_1():
    # Read the CSV file
    data = pd.read_csv("graficos/Kmeans3_T_Salarios_certo_M.csv")
    data = data.drop(columns=['Unnamed: 0'])
    # data = data.drop(columns=['Unnamed: 0.1'])
    # data = data.drop(columns=['Curso_Nome'])
    # data = data.drop(columns=['Cbo_Nome'])
    data = data.drop(columns=['Ida'])
    data = data.drop(columns=['Volta'])

    
    Curso = [142,  142,  726,  142,   214,   762,  725]
    Cbo   = [2341, 2342, 2265, 2351,  2163,  2635, 2266]


    # Filter the records based on the specified Courses and Cbos
    filtered_data = data[data['Curso'].isin(Curso) & data['Cbo'].isin(Cbo)]

    data_1 = pd.read_csv("graficos/Deslocamento_Geral_cluster 0.csv")
    filtered_1 = data_1[(data_1['Curso'] == 142) & (data_1['Cbo'] == 2342) & (data_1['Genero'] == 'M')]    
    filtered_2 = data_1[(data_1['Curso'] == 142) & (data_1['Cbo'] == 2351) & (data_1['Genero'] == 'M')]    
    filtered_3 = data_1[(data_1['Curso'] == 142) & (data_1['Cbo'] == 2341) & (data_1['Genero'] == 'M')]    
    filtered_4 = data_1[(data_1['Curso'] == 726) & (data_1['Cbo'] == 2265) & (data_1['Genero'] == 'M')]    
    filtered_5 = data_1[(data_1['Curso'] == 214) & (data_1['Cbo'] == 2163) & (data_1['Genero'] == 'M')]    
    data_2 = pd.read_csv("graficos/Deslocamento_Geral_cluster 1.csv")
    filtered_6 = data_2[(data_2['Curso'] == 762) & (data_2['Cbo'] == 2635) & (data_2['Genero'] == 'M')]     
    data_3 =     pd.read_csv("graficos/Deslocamento_Geral_cluster 2.csv")
    filtered_7 = data_3[(data_3['Curso'] == 725) & (data_3['Cbo'] == 2266) & (data_3['Genero'] == 'M')]      

    # Adicionar uma nova coluna em filtered_data
    filtered_data['Deslocamento'] = [filtered_1['Distance'].values[0],filtered_2['Distance'].values[0], filtered_3['Distance'].values[0] , filtered_4['Distance'].values[0], filtered_5['Distance'].values[0], filtered_6['Distance'].values[0],  filtered_7['Distance'].values[0]] 
    filtered_data['Cluster'] = [filtered_1['Cluster'].values[0],filtered_2['Cluster'].values[0], filtered_3['Cluster'].values[0] , filtered_4['Cluster'].values[0], filtered_5['Cluster'].values[0], filtered_6['Cluster'].values[0],  filtered_7['Cluster'].values[0]]  
    # filtered_data['Deslocamento'] = filtered_data['Deslocamento'].astype(int)
    filtered_data['Deslocamento'] = round(filtered_data['Deslocamento'],2)
    filtered_data['Cluster'] = filtered_data['Cluster'].astype(int)
    filtered_data['Curso'] = filtered_data['Curso'].astype(int)
    filtered_data['Cbo'] = filtered_data['Cbo'].astype(int)
    # filtered_data['Max'] = filtered_data['Max'].astype(int)
    # filtered_data['Min'] = filtered_data['Min'].astype(int)
    # filtered_data['Median'] = filtered_data['Median'].astype(int)
    filtered_data['Median'] = round(filtered_data['Median'],2)




    # Save the records in a LaTeX table
    latex_table = filtered_data.to_latex(index=False, caption="Deslocamentos signficativos Masculinos", label="tab:Salarios_Desequlibrio_M_2") 
    
    
    # Salvar em um arquivo .tex
    with open("tabelas/Kmeans3_T_Salarios_certo_M.tex", "w") as f:
        f.write(latex_table)

    return  

def extract_courses_Cluster1():
    # Read the CSV file
    data = pd.read_csv("graficos/Kmeans3_T_Salarios_certo_M.csv")
    data2 = pd.read_csv("graficos/Kmeans3_T_Salarios_certo_F.csv")

    data = data.drop(columns=['Unnamed: 0'])
    # data = data.drop(columns=['Curso_Nome'])
    # data = data.drop(columns=['Cbo_Nome'])
    data = data.drop(columns=['Ida'])
    data = data.drop(columns=['Volta'])
    data = data.drop(columns=['Cluster'])
    data = data.drop(columns=['Min'])
    data = data.drop(columns=['Max'])

    data2 = data2.drop(columns=['Unnamed: 0'])
    # data = data.drop(columns=['Curso_Nome'])
    # data = data.drop(columns=['Cbo_Nome'])
    data2 = data2.drop(columns=['Ida'])
    data2 = data2.drop(columns=['Volta'])
    data2 = data2.drop(columns=['Cluster'])
    data2 = data2.drop(columns=['Min'])
    data2 = data2.drop(columns=['Max'])

    
    Curso = [762]
    Cbo   = [2635]

    Curso2 = [221]
    Cbo2   = [2636]


    # Filter the records based on the specified Courses and Cbos
    filtered_data = data[data['Curso'].isin(Curso) & data['Cbo'].isin(Cbo)]
    filtered_data_2 = data2[data2['Curso'].isin(Curso2) & data2['Cbo'].isin(Cbo2)]


#     data_521 = pd.read_csv("graficos/Deslocamento_Geral_cluster 0.csv")
#     filtered_521 = data_521[(data_521['Curso'] == 521) & (data_521['Cbo'] == 2144) & (data_521['Genero'] == 'F')]      

   
#    # Adicionar uma nova coluna em filtered_data
#     filtered_data['Deslocamento'] = [filtered_863['Distance'].values[0],filtered_221['Distance'].values[0], filtered_521['Distance'].values[0]]  # Substitua [1, 2, 3] pelos valores desejados
#     filtered_data['Cluster'] = [filtered_863['Cluster'].values[0],filtered_221['Cluster'].values[0], filtered_521['Cluster'].values[0]]  # Substitua [1, 2, 3] pelos valores desejados
    
    # # filtered_data['Deslocamento'] = filtered_data['Deslocamento'].astype(int)
    # # filtered_data['Deslocamento'] = round(filtered_data['Deslocamento'],2)
    # # filtered_data['Cluster'] = filtered_data['Cluster'].astype(int)
    # filtered_data['Curso'] = filtered_data['Curso'].astype(int)
    # filtered_data['Cbo'] = filtered_data['Cbo'].astype(int)
    # # filtered_data['Max'] = filtered_data['Max'].astype(int)
    # # filtered_data['Min'] = filtered_data['Min'].astype(int)
    # #filtered_data['Median'] = filtered_data['Median'].astype(int)
    # filtered_data['Median'] = round(filtered_data['Median'],2)

 
    # # filtered_data['Deslocamento'] = filtered_data['Deslocamento'].astype(int)
    # # filtered_data['Deslocamento'] = round(filtered_data['Deslocamento'],2)
    # # filtered_data['Cluster'] = filtered_data['Cluster'].astype(int)
    # filtered_data_2['Curso'] = filtered_data_2['Curso'].astype(int)
    # filtered_data_2['Cbo'] = filtered_data_2['Cbo'].astype(int)
    # # filtered_data['Max'] = filtered_data['Max'].astype(int)
    # # filtered_data['Min'] = filtered_data['Min'].astype(int)
    # #filtered_data['Median'] = filtered_data['Median'].astype(int)
    # filtered_data_2['Median'] = round(filtered_data_2['Median'],2)

    filtered_data_all = pd.concat([filtered_data, filtered_data_2], ignore_index=True)

    data_3 = pd.read_csv("graficos/Deslocamento_Geral_cluster 1.csv")
    filtered_1 = data_3[(data_3['Curso'] == 762) & (data_3['Cbo'] == 2635) & (data_3['Genero'] == 'M')]  
    filtered_2 = data_3[(data_3['Curso'] == 221) & (data_3['Cbo'] == 2636) & (data_3['Genero'] == 'F')]      
    # filtered_3 = data_3[(data_3['Curso'] == 142) & (data_3['Cbo'] == 2351) & (data_3['Genero'] == 'M')]      
    # filtered_4 = data_3[(data_3['Curso'] == 726) & (data_3['Cbo'] == 2265) & (data_3['Genero'] == 'M')]      
    # filtered_5 = data_3[(data_3['Curso'] == 214) & (data_3['Cbo'] == 2163) & (data_3['Genero'] == 'M')]      
    # filtered_6 = data_3[(data_3['Curso'] == 520) & (data_3['Cbo'] == 2141) & (data_3['Genero'] == 'F')]      
    # filtered_7 = data_3[(data_3['Curso'] == 521) & (data_3['Cbo'] == 2144) & (data_3['Genero'] == 'F')]      

    # Adicionar uma nova coluna em filtered_data
    filtered_data_all['Deslocamento'] = [filtered_1['Distance'].values[0],filtered_2['Distance'].values[0]#, filtered_3['Distance'].values[0],
                                    #filtered_4['Distance'].values[0],filtered_5['Distance'].values[0], filtered_6['Distance'].values[0], 
                                    #filtered_7['Distance'].values[0]
                                     ] 
    filtered_data_all['Cluster'] = [filtered_1['Cluster'].values[0],filtered_2['Cluster'].values[0]#, filtered_3['Cluster'].values[0],
                                     #filtered_4['Cluster'].values[0],filtered_5['Cluster'].values[0], filtered_6['Cluster'].values[0], 
                                     #filtered_7['Cluster'].values[0]
                                     ] 

    filtered_data_all['Deslocamento'] = round(filtered_data_all['Deslocamento'],2)
    filtered_data_all['Cluster'] = filtered_data_all['Cluster'].astype(int)
    # filtered_data['Deslocamento'] = filtered_data['Deslocamento'].astype(int)
    # filtered_data['Deslocamento'] = round(filtered_data['Deslocamento'],2)
    # filtered_data['Cluster'] = filtered_data['Cluster'].astype(int)
    filtered_data_all['Curso'] = filtered_data_all['Curso'].astype(int)
    filtered_data_all['Cbo'] = filtered_data_all['Cbo'].astype(int)
    # filtered_data['Max'] = filtered_data['Max'].astype(int)
    # filtered_data['Min'] = filtered_data['Min'].astype(int)
    #filtered_data['Median'] = filtered_data['Median'].astype(int)
    filtered_data_all['Median'] = round(filtered_data_all['Median'],2)

    # Save the records in a LaTeX table
    latex_table = filtered_data_all.to_latex(index=False, caption="Cluster1 deslocamentos signficativos ", label="tab:Salarios_Cluster1") 
    
    
    # Salvar em um arquivo .tex
    with open("tabelas/Kmeans3_T_Salarios_Cluster1.tex", "w") as f:
        f.write(latex_table)
    return     

def extract_courses_Cluster2():
    # Read the CSV file
    data = pd.read_csv("graficos/Kmeans3_T_Salarios_certo_M.csv")
    data2 = pd.read_csv("graficos/Kmeans3_T_Salarios_certo_F.csv")

    data = data.drop(columns=['Unnamed: 0'])
    # data = data.drop(columns=['Curso_Nome'])
    # data = data.drop(columns=['Cbo_Nome'])
    data = data.drop(columns=['Ida'])
    data = data.drop(columns=['Volta'])
    data = data.drop(columns=['Cluster'])
    data = data.drop(columns=['Min'])
    data = data.drop(columns=['Max'])

    data2 = data2.drop(columns=['Unnamed: 0'])
    # data = data.drop(columns=['Curso_Nome'])
    # data = data.drop(columns=['Cbo_Nome'])
    data2 = data2.drop(columns=['Ida'])
    data2 = data2.drop(columns=['Volta'])
    data2 = data2.drop(columns=['Cluster'])
    data2 = data2.drop(columns=['Min'])
    data2 = data2.drop(columns=['Max'])

    
    Curso = [725]
    Cbo   = [2266]

    Curso2 = [863]
    Cbo2   = [110]


    # Filter the records based on the specified Courses and Cbos
    filtered_data = data[data['Curso'].isin(Curso) & data['Cbo'].isin(Cbo)]
    filtered_data_2 = data2[data2['Curso'].isin(Curso2) & data2['Cbo'].isin(Cbo2)]


#     data_521 = pd.read_csv("graficos/Deslocamento_Geral_cluster 0.csv")
#     filtered_521 = data_521[(data_521['Curso'] == 521) & (data_521['Cbo'] == 2144) & (data_521['Genero'] == 'F')]      

   
#    # Adicionar uma nova coluna em filtered_data
#     filtered_data['Deslocamento'] = [filtered_863['Distance'].values[0],filtered_221['Distance'].values[0], filtered_521['Distance'].values[0]]  # Substitua [1, 2, 3] pelos valores desejados
#     filtered_data['Cluster'] = [filtered_863['Cluster'].values[0],filtered_221['Cluster'].values[0], filtered_521['Cluster'].values[0]]  # Substitua [1, 2, 3] pelos valores desejados
    
    # # filtered_data['Deslocamento'] = filtered_data['Deslocamento'].astype(int)
    # # filtered_data['Deslocamento'] = round(filtered_data['Deslocamento'],2)
    # # filtered_data['Cluster'] = filtered_data['Cluster'].astype(int)
    # filtered_data['Curso'] = filtered_data['Curso'].astype(int)
    # filtered_data['Cbo'] = filtered_data['Cbo'].astype(int)
    # # filtered_data['Max'] = filtered_data['Max'].astype(int)
    # # filtered_data['Min'] = filtered_data['Min'].astype(int)
    # #filtered_data['Median'] = filtered_data['Median'].astype(int)
    # filtered_data['Median'] = round(filtered_data['Median'],2)

 
    # # filtered_data['Deslocamento'] = filtered_data['Deslocamento'].astype(int)
    # # filtered_data['Deslocamento'] = round(filtered_data['Deslocamento'],2)
    # # filtered_data['Cluster'] = filtered_data['Cluster'].astype(int)
    # filtered_data_2['Curso'] = filtered_data_2['Curso'].astype(int)
    # filtered_data_2['Cbo'] = filtered_data_2['Cbo'].astype(int)
    # # filtered_data['Max'] = filtered_data['Max'].astype(int)
    # # filtered_data['Min'] = filtered_data['Min'].astype(int)
    # #filtered_data['Median'] = filtered_data['Median'].astype(int)
    # filtered_data_2['Median'] = round(filtered_data_2['Median'],2)

    filtered_data_all = pd.concat([filtered_data, filtered_data_2], ignore_index=True)

    data_3 = pd.read_csv("graficos/Deslocamento_Geral_cluster 2.csv")
    filtered_1 = data_3[(data_3['Curso'] == 725) & (data_3['Cbo'] == 2266) & (data_3['Genero'] == 'M')]  
    filtered_2 = data_3[(data_3['Curso'] == 863) & (data_3['Cbo'] == 110) & (data_3['Genero'] == 'F')]      
    # filtered_3 = data_3[(data_3['Curso'] == 142) & (data_3['Cbo'] == 2351) & (data_3['Genero'] == 'M')]      
    # filtered_4 = data_3[(data_3['Curso'] == 726) & (data_3['Cbo'] == 2265) & (data_3['Genero'] == 'M')]      
    # filtered_5 = data_3[(data_3['Curso'] == 214) & (data_3['Cbo'] == 2163) & (data_3['Genero'] == 'M')]      
    # filtered_6 = data_3[(data_3['Curso'] == 520) & (data_3['Cbo'] == 2141) & (data_3['Genero'] == 'F')]      
    # filtered_7 = data_3[(data_3['Curso'] == 521) & (data_3['Cbo'] == 2144) & (data_3['Genero'] == 'F')]      

    # Adicionar uma nova coluna em filtered_data
    filtered_data_all['Deslocamento'] = [filtered_1['Distance'].values[0],filtered_2['Distance'].values[0]#, filtered_3['Distance'].values[0],
                                    #filtered_4['Distance'].values[0],filtered_5['Distance'].values[0], filtered_6['Distance'].values[0], 
                                    #filtered_7['Distance'].values[0]
                                     ] 
    filtered_data_all['Cluster'] = [filtered_1['Cluster'].values[0],filtered_2['Cluster'].values[0]#, filtered_3['Cluster'].values[0],
                                     #filtered_4['Cluster'].values[0],filtered_5['Cluster'].values[0], filtered_6['Cluster'].values[0], 
                                     #filtered_7['Cluster'].values[0]
                                     ] 

    filtered_data_all['Deslocamento'] = round(filtered_data_all['Deslocamento'],2)
    filtered_data_all['Cluster'] = filtered_data_all['Cluster'].astype(int)
    # filtered_data['Deslocamento'] = filtered_data['Deslocamento'].astype(int)
    # filtered_data['Deslocamento'] = round(filtered_data['Deslocamento'],2)
    # filtered_data['Cluster'] = filtered_data['Cluster'].astype(int)
    filtered_data_all['Curso'] = filtered_data_all['Curso'].astype(int)
    filtered_data_all['Cbo'] = filtered_data_all['Cbo'].astype(int)
    # filtered_data['Max'] = filtered_data['Max'].astype(int)
    # filtered_data['Min'] = filtered_data['Min'].astype(int)
    #filtered_data['Median'] = filtered_data['Median'].astype(int)
    filtered_data_all['Median'] = round(filtered_data_all['Median'],2)

    # Save the records in a LaTeX table
    latex_table = filtered_data_all.to_latex(index=False, caption="Cluster2 deslocamentos signficativos ", label="tab:Salarios_Cluster2") 
    
    
    # Salvar em um arquivo .tex
    with open("tabelas/Kmeans3_T_Salarios_Cluster2.tex", "w") as f:
        f.write(latex_table)
    return             

def extract_courses_Correspondentes_F_1():
    # Read the CSV file
    # data = pd.read_csv("graficos/Kmeans3_T_Salarios_certo_F.csv")
    # data2 = pd.read_csv("graficos/Kmeans3_T_Salarios_certo_M.csv")
    data = pd.read_csv("graficos/Kmeans3_T_Salarios_certo_M.csv")

    data = data.drop(columns=['Unnamed: 0'])
    # data = data.drop(columns=['Curso_Nome'])
    # data = data.drop(columns=['Cbo_Nome'])
    data = data.drop(columns=['Ida'])
    data = data.drop(columns=['Volta'])
    # data = data.drop(columns=['Cluster'])
    # data = data.drop(columns=['Min'])
    # data = data.drop(columns=['Max'])


    # data2 = data2.drop(columns=['Unnamed: 0'])
    # # data = data.drop(columns=['Curso_Nome'])
    # # data = data.drop(columns=['Cbo_Nome'])
    # data2 = data2.drop(columns=['Ida'])
    # data2 = data2.drop(columns=['Volta'])
    # data2 = data2.drop(columns=['Cluster'])
    # # data2 = data2.drop(columns=['Min'])
    # # data2 = data2.drop(columns=['Max'])

    
    # Curso = [142,  142,  726, 142, 214]
    # Cbo   = [2341, 2342, 2265,2351,2163]

    # Curso2 = [521,520]
    # Cbo2   = [2144,2141]

    Curso = [863, 221, 521]
    Cbo   = [110, 2636, 2144]


    # Filter the records based on the specified Courses and Cbos
    filtered_data = data[data['Curso'].isin(Curso) & data['Cbo'].isin(Cbo)]
    # filtered_data_2 = data2[data2['Curso'].isin(Curso2) & data2['Cbo'].isin(Cbo2)]


#     data_521 = pd.read_csv("graficos/Deslocamento_Geral_cluster 0.csv")
#     filtered_521 = data_521[(data_521['Curso'] == 521) & (data_521['Cbo'] == 2144) & (data_521['Genero'] == 'F')]      

   
#    # Adicionar uma nova coluna em filtered_data
#     filtered_data['Deslocamento'] = [filtered_863['Distance'].values[0],filtered_221['Distance'].values[0], filtered_521['Distance'].values[0]]  # Substitua [1, 2, 3] pelos valores desejados
#     filtered_data['Cluster'] = [filtered_863['Cluster'].values[0],filtered_221['Cluster'].values[0], filtered_521['Cluster'].values[0]]  # Substitua [1, 2, 3] pelos valores desejados
    
    # # filtered_data['Deslocamento'] = filtered_data['Deslocamento'].astype(int)
    # # filtered_data['Deslocamento'] = round(filtered_data['Deslocamento'],2)
    # filtered_data['Cluster'] = filtered_data['Cluster'].astype(int)
    # filtered_data['Curso'] = filtered_data['Curso'].astype(int)
    # filtered_data['Cbo'] = filtered_data['Cbo'].astype(int)
    # # filtered_data['Max'] = filtered_data['Max'].astype(int)
    # # filtered_data['Min'] = filtered_data['Min'].astype(int)
    # #filtered_data['Median'] = filtered_data['Median'].astype(int)
    # filtered_data['Median'] = round(filtered_data['Median'],2)

 
    # # filtered_data['Deslocamento'] = filtered_data['Deslocamento'].astype(int)
    # # filtered_data['Deslocamento'] = round(filtered_data['Deslocamento'],2)
    # # filtered_data['Cluster'] = filtered_data['Cluster'].astype(int)
    # filtered_data_2['Curso'] = filtered_data_2['Curso'].astype(int)
    # filtered_data_2['Cbo'] = filtered_data_2['Cbo'].astype(int)
    # # filtered_data['Max'] = filtered_data['Max'].astype(int)
    # # filtered_data['Min'] = filtered_data['Min'].astype(int)
    # #filtered_data['Median'] = filtered_data['Median'].astype(int)
    # filtered_data_2['Median'] = round(filtered_data_2['Median'],2)

    # filtered_data_all = pd.concat([filtered_data, filtered_data_2], ignore_index=True)

    # Save the records in a LaTeX table
    latex_table = filtered_data.to_latex(index=False, caption="Masculinos: correspondentes aos deslocamentos femininos", label="tab:Salarios_Desequlibrio_F")
    
   
    
    # Salvar em um arquivo .tex
    with open("tabelas/Kmeans3_T_Salarios_certo_Correspondentes_F_1.tex", "w") as f:
        f.write(latex_table)
    return    

# def plot_age_distribution_for_course_cbo():
#         import matplotlib.pyplot as plt

#         # Leitura do arquivo
#         file_path = 'graficos/Resultados_T_Filtrados_Kmeans3_Idade_M.csv'
#         df = pd.read_csv(file_path)

#         # Filtrar pelo curso 212 e CBO 2354
#         filtered_df = df[(df['Curso'] == 724) & (df['Cbo'] == 2261)]

#         # Contar a quantidade de pessoas por faixa etária
#         age_counts = filtered_df['Idade'].value_counts().reindex(['29', '30-39', '40-49', '50-59', '60'], fill_value=0)

#         # Criar o gráfico de barras
#         plt.figure(figsize=(8, 6))
#         age_counts.plot(kind='bar', color='skyblue', edgecolor='black')
#         plt.title('Distribuição de Idades para Curso 212 e CBO 2354', fontsize=14)
#         plt.xlabel('Faixa Etária', fontsize=12)
#         plt.ylabel('Quantidade de Pessoas', fontsize=12)
#         plt.xticks(rotation=0)
#         plt.grid(axis='y', linestyle='--', alpha=0.7)
#         plt.tight_layout()

#         # Salvar o gráfico
#         save_results_to = 'graficos/'
#         plt.savefig(save_results_to + 'Distribuicao_Idades_Curso212_CBO2354.png')
#         plt.show()
def plot_ida_volta_distribution_for_course_cbo(sx):
    import matplotlib.pyplot as plt

    if sx== "F":
        # Leitura do arquivo
        file_path = 'graficos/Resultados_T_Filtrados_Kmeans3_Idade_F.csv'
        df = pd.read_csv(file_path)

        # Filtrar pelo curso 724 e CBO 2261
        filtered_df = df[(df['Curso'] == 212) & (df['Cbo'] == 2354)]

        # Inicializar dicionários para ida e volta
        ida_counts = {'29': 0, '30-39': 0, '40-49': 0, '50-59': 0, '60': 0}
        volta_counts = {'29': 0, '30-39': 0, '40-49': 0, '50-59': 0, '60': 0}

        # Contar ida e volta por faixa etária
        for _, row in filtered_df.iterrows():
            if row['Idade'] in ida_counts:
                ida_counts[row['Idade']] += row['Ida']
                volta_counts[row['Idade']] += row['Volta']

        # Criar o gráfico de barras
        labels = list(ida_counts.keys())
        ida_values = list(ida_counts.values())
        volta_values = list(volta_counts.values())

        x = range(len(labels))
        width = 0.35

        plt.figure(figsize=(10, 6))
        plt.bar(x, ida_values, width, label='Ida', color='skyblue', edgecolor='black')
        plt.bar([p + width for p in x], volta_values, width, label='Volta', color='orange', edgecolor='black')

        plt.xlabel('Faixa Etária', fontsize=12)
        plt.ylabel('Quantidade', fontsize=12)
        plt.title('Distribuição de Ida e Volta para Curso 212 e CBO 2354 - Feminino', fontsize=14)
        plt.xticks([p + width / 2 for p in x], labels)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        # plt.xlim(0.0, 100.0)
        # plt.ylim(0.0, 100.0)

        # Salvar o gráfico
        save_results_to = 'graficos/'
        plt.savefig(save_results_to + 'Distribuicao_Ida_Volta_Curso212_CBO2354_F.png')
        # plt.show()

    if sx== "M":
        # Leitura do arquivo
        file_path = 'graficos/Resultados_T_Filtrados_Kmeans3_Idade_M.csv'
        df = pd.read_csv(file_path)

        # Filtrar pelo curso 724 e CBO 2261
        filtered_df = df[(df['Curso'] == 212) & (df['Cbo'] == 2354)]

        # Inicializar dicionários para ida e volta
        ida_counts = {'29': 0, '30-39': 0, '40-49': 0, '50-59': 0, '60': 0}
        volta_counts = {'29': 0, '30-39': 0, '40-49': 0, '50-59': 0, '60': 0}

        # Contar ida e volta por faixa etária
        for _, row in filtered_df.iterrows():
            if row['Idade'] in ida_counts:
                ida_counts[row['Idade']] += row['Ida']
                volta_counts[row['Idade']] += row['Volta']

        # Criar o gráfico de barras
        labels = list(ida_counts.keys())
        ida_values = list(ida_counts.values())
        volta_values = list(volta_counts.values())

        x = range(len(labels))
        width = 0.35

        plt.figure(figsize=(10, 6))
        plt.bar(x, ida_values, width, label='Ida', color='skyblue', edgecolor='black')
        plt.bar([p + width for p in x], volta_values, width, label='Volta', color='orange', edgecolor='black')

        plt.xlabel('Faixa Etária', fontsize=12)
        plt.ylabel('Quantidade', fontsize=12)
        plt.title('Distribuição de Ida e Volta para Curso 212 e CBO 2354 - Masculino', fontsize=14)
        plt.xticks([p + width / 2 for p in x], labels)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        # plt.xlim(0.0, 100.0)
        # plt.ylim(0.0, 100.0)

        # Salvar o gráfico
        save_results_to = 'graficos/'
        plt.savefig(save_results_to + 'Distribuicao_Ida_Volta_Curso212_CBO2354_M.png')
        # plt.show()

    return


def Analise_Genero_FaixaEtaria():
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
    Kmeans3_T['M29'] = ''
    Kmeans3_T['M30'] = ''
    Kmeans3_T['M40'] = ''
    Kmeans3_T['M50'] = ''
    Kmeans3_T['M60'] = ''
    Kmeans3_T['F29'] = ''
    Kmeans3_T['F30'] = ''
    Kmeans3_T['F40'] = ''
    Kmeans3_T['F50'] = ''
    Kmeans3_T['F60'] = ''
    
    # Feminino ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # for i in range(0,10): 
    for i in range(len(Kmeans3_T)): 
        Qtdade = 0
        for j in range(len(Final_Fem_CSV)):
            # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
            if ((str(Final_Fem_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i])))& Final_Fem_CSV.Idade_em_Anos[j] <=29:
                Qtdade = Qtdade + 1
            Kmeans3_T.F29[i] = int(Qtdade)      
    #         if ((str(Final_Fem_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Fem_CSV.Idade_em_Anos[j] >30 & Final_Fem_CSV.Idade_em_Anos[j] <=39:
    #             Qtdade = Qtdade + 1
    #         Kmeans3_T.F30[i] = int(Qtdade)  
    #         if ((str(Final_Fem_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Fem_CSV.Idade_em_Anos[j] >40 & Final_Fem_CSV.Idade_em_Anos[j] <=49:
    #             Qtdade = Qtdade + 1
    #         Kmeans3_T.F40[i] = int(Qtdade)    
    #         if ((str(Final_Fem_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Fem_CSV.Idade_em_Anos[j] >50 & Final_Fem_CSV.Idade_em_Anos[j] <=59:
    #             Qtdade = Qtdade + 1
    #         Kmeans3_T.F50[i] = int(Qtdade)    
    #         if ((str(Final_Fem_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Fem_CSV.Idade_em_Anos[j] >=60:
    #             Qtdade = Qtdade + 1
    #         Kmeans3_T.F60[i] = int(Qtdade)            
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')       
    # # -----------------------------------------------------------------------------------
    # # -------------------------------------------------------------------------------------     
    # # for i in range(0,10): 
    # for i in range(len(Kmeans3_T)): 
    #     Qtdade = 0
    #     for j in range(len(Final_Fem_CSV)):
    #         # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
    #         if ((str(Final_Fem_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Fem_CSV.Idade_em_Anos[j] >30 & Final_Fem_CSV.Idade_em_Anos[j] <=39:
    #             Qtdade = Qtdade + 1
    #     Kmeans3_T.F30[i] = int(Qtdade)            
    # Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')     
    # # -----------------------------------------------------------------------------------    
    # # ----------------------------------------------------------------------------------- 
    # # for i in range(0,10): 
    # for i in range(len(Kmeans3_T)): 
    #     Qtdade = 0
    #     for j in range(len(Final_Fem_CSV)):
    #         # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
    #         if ((str(Final_Fem_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Fem_CSV.Idade_em_Anos[j] >40 & Final_Fem_CSV.Idade_em_Anos[j] <=49:
    #             Qtdade = Qtdade + 1
    #     Kmeans3_T.F40[i] = int(Qtdade)            
    # Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')    
    # # -----------------------------------------------------------------------------------    
    # # ----------------------------------------------------------------------------------- 
    # # for i in range(0,10): 
    # for i in range(len(Kmeans3_T)): 
    #     Qtdade = 0
    #     for j in range(len(Final_Fem_CSV)):
    #         # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
    #         if ((str(Final_Fem_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Fem_CSV.Idade_em_Anos[j] >50 & Final_Fem_CSV.Idade_em_Anos[j] <=59:
    #             Qtdade = Qtdade + 1
    #     Kmeans3_T.F50[i] = int(Qtdade)            
    # Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')     
    # # ----------------------------------------------------------------------------------- 
    # # for i in range(0,10): 
    # for i in range(len(Kmeans3_T)): 
    #     Qtdade = 0
    #     for j in range(len(Final_Fem_CSV)):
    #         # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
    #         if ((str(Final_Fem_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Fem_CSV.Idade_em_Anos[j] >=60:
    #             Qtdade = Qtdade + 1
    #     Kmeans3_T.F60[i] = int(Qtdade)            
    # Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')     

    # # Masculino ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # # for i in range(0,10): 
    # for i in range(len(Kmeans3_T)): 
    #     Qtdade = 0
    #     for j in range(len(Final_Masc_CSV)):
    #         # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
    #         if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i])))& Final_Masc_CSV.Idade_em_Anos[j] <=29:
    #             Qtdade = Qtdade + 1
    #         Kmeans3_T.M29[i] = int(Qtdade)    
    #         # if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >30 & Final_Masc_CSV.Idade_em_Anos[j] <=39:
    #         #     Qtdade = Qtdade + 1
    #         # Kmeans3_T.M30[i] = int(Qtdade) 
    #         # if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >40 & Final_Masc_CSV.Idade_em_Anos[j] <=49:
    #         #     Qtdade = Qtdade + 1
    #         # Kmeans3_T.M40[i] = int(Qtdade)         
    #         # if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >50 & Final_Masc_CSV.Idade_em_Anos[j] <=59:
    #         #     Qtdade = Qtdade + 1
    #         # Kmeans3_T.M50[i] = int(Qtdade)    
    #         # if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >=60:
    #         #     Qtdade = Qtdade + 1
    #         # Kmeans3_T.M60[i] = int(Qtdade) 
    # Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')       
    # # # # -----------------------------------------------------------------------------------
    # # # -------------------------------------------------------------------------------------     
    # # for i in range(0,10): 
    # for i in range(len(Kmeans3_T)): 
    #     Qtdade = 0
    #     for j in range(len(Final_Masc_CSV)):
    #         # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
    #         if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >30 & Final_Masc_CSV.Idade_em_Anos[j] <=39:
    #             Qtdade = Qtdade + 1
    #     Kmeans3_T.M30[i] = int(Qtdade)            
    # Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')     
    # # -----------------------------------------------------------------------------------    
    # # # ----------------------------------------------------------------------------------- 
    # # for i in range(0,10): 
    # for i in range(len(Kmeans3_T)): 
    #     Qtdade = 0
    #     for j in range(len(Final_Masc_CSV)):
    #         # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
    #         if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >40 & Final_Masc_CSV.Idade_em_Anos[j] <=49:
    #             Qtdade = Qtdade + 1
    #     Kmeans3_T.M40[i] = int(Qtdade)            
    # Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')    
    # # -----------------------------------------------------------------------------------    
    # # ----------------------------------------------------------------------------------- 
    # # for i in range(0,10): 
    # for i in range(len(Kmeans3_T)): 
    #     Qtdade = 0
    #     for j in range(len(Final_Masc_CSV)):
    #         # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
    #         if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >50 & Final_Masc_CSV.Idade_em_Anos[j] <=59:
    #             Qtdade = Qtdade + 1
    #     Kmeans3_T.M50[i] = int(Qtdade)            
    # Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')     
    # # ----------------------------------------------------------------------------------- 
    # # for i in range(0,10): 
    # for i in range(len(Kmeans3_T)): 
    #     Qtdade = 0
    #     for j in range(len(Final_Masc_CSV)):
    #         # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
    #         if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >=60:
    #             Qtdade = Qtdade + 1
    #     Kmeans3_T.M60[i] = int(Qtdade)            
    # Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')    
    return   

def Analise_Genero_FaixaEtaria_1():
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
    Kmeans3_T['M29'] = ''
    Kmeans3_T['M30'] = ''
    Kmeans3_T['M40'] = ''
    Kmeans3_T['M50'] = ''
    Kmeans3_T['M60'] = ''
    Kmeans3_T['F29'] = ''
    Kmeans3_T['F30'] = ''
    Kmeans3_T['F40'] = ''
    Kmeans3_T['F50'] = ''
    Kmeans3_T['F60'] = ''
    
    # Feminino ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # for i in range(0,10): 
    for i in range(len(Kmeans3_T)): 
        Qtdade = 0
        for j in range(len(Final_Fem_CSV)):
            # Check if the current row matches the Cbo and Curso for the current index
            if ((str(Final_Fem_CSV.Ocupação_Código[j])) == (str(int(Kmeans3_T.Cbo[i])))) and \
               (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) and \
               (Final_Fem_CSV.Idade_em_Anos[j] <= 29):
               Qtdade += 1
        # Assign the final count to the corresponding row in Kmeans3_T
        Kmeans3_T.F29[i] = int(Qtdade)

        # Reset Qtdade for the next age range
        Qtdade = 0
        for j in range(len(Final_Fem_CSV)):
            # Check if the current row matches the Cbo and Curso for the current index and age range 30-39
            if ((str(Final_Fem_CSV.Ocupação_Código[j])) == (str(int(Kmeans3_T.Cbo[i])))) and \
               (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) and \
               (30 <= Final_Fem_CSV.Idade_em_Anos[j] <= 39):
               Qtdade += 1
        # Assign the final count to the corresponding row in Kmeans3_T
        Kmeans3_T.F30[i] = int(Qtdade)

        # Reset Qtdade for the next age range
        Qtdade = 0
        for j in range(len(Final_Fem_CSV)):
            # Check if the current row matches the Cbo and Curso for the current index and age range 40-49
            if ((str(Final_Fem_CSV.Ocupação_Código[j])) == (str(int(Kmeans3_T.Cbo[i])))) and \
               (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) and \
               (40 <= Final_Fem_CSV.Idade_em_Anos[j] <= 49):
               Qtdade += 1
        # Assign the final count to the corresponding row in Kmeans3_T
        Kmeans3_T.F40[i] = int(Qtdade)

        # Reset Qtdade for the next age range
        Qtdade = 0
        for j in range(len(Final_Fem_CSV)):
            # Check if the current row matches the Cbo and Curso for the current index and age range 50-59
            if ((str(Final_Fem_CSV.Ocupação_Código[j])) == (str(int(Kmeans3_T.Cbo[i])))) and \
               (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) and \
               (50 <= Final_Fem_CSV.Idade_em_Anos[j] <= 59):
               Qtdade += 1
        # Assign the final count to the corresponding row in Kmeans3_T
        Kmeans3_T.F50[i] = int(Qtdade)

        # Reset Qtdade for the next age range
        Qtdade = 0
        for j in range(len(Final_Fem_CSV)):
            # Check if the current row matches the Cbo and Curso for the current index and age range 60 or more
            if ((str(Final_Fem_CSV.Ocupação_Código[j])) == (str(int(Kmeans3_T.Cbo[i])))) and \
               (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) and \
               (Final_Fem_CSV.Idade_em_Anos[j] >= 60):
               Qtdade += 1
        # Assign the final count to the corresponding row in Kmeans3_T
        Kmeans3_T.F60[i] = int(Qtdade)

    # Masculino ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # for i in range(0,10): 
    for i in range(len(Kmeans3_T)): 
        Qtdade = 0
        for j in range(len(Final_Masc_CSV)):
            # Check if the current row matches the Cbo and Curso for the current index
            if ((str(Final_Masc_CSV.Ocupação_Código[j])) == (str(int(Kmeans3_T.Cbo[i])))) and \
               (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) and \
               (Final_Masc_CSV.Idade_em_Anos[j] <= 29):
               Qtdade += 1
        # Assign the final count to the corresponding row in Kmeans3_T
        Kmeans3_T.M29[i] = int(Qtdade)

        # Reset Qtdade for the next age range
        Qtdade = 0
        for j in range(len(Final_Masc_CSV)):
            # Check if the current row matches the Cbo and Curso for the current index and age range 30-39
            if ((str(Final_Masc_CSV.Ocupação_Código[j])) == (str(int(Kmeans3_T.Cbo[i])))) and \
               (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) and \
               (30 <= Final_Masc_CSV.Idade_em_Anos[j] <= 39):
               Qtdade += 1
        # Assign the final count to the corresponding row in Kmeans3_T
        Kmeans3_T.M30[i] = int(Qtdade)

        # Reset Qtdade for the next age range
        Qtdade = 0
        for j in range(len(Final_Masc_CSV)):
            # Check if the current row matches the Cbo and Curso for the current index and age range 40-49
            if ((str(Final_Masc_CSV.Ocupação_Código[j])) == (str(int(Kmeans3_T.Cbo[i])))) and \
               (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) and \
               (40 <= Final_Masc_CSV.Idade_em_Anos[j] <= 49):
               Qtdade += 1
        # Assign the final count to the corresponding row in Kmeans3_T
        Kmeans3_T.M40[i] = int(Qtdade)

        # Reset Qtdade for the next age range
        Qtdade = 0
        for j in range(len(Final_Masc_CSV)):
            # Check if the current row matches the Cbo and Curso for the current index and age range 50-59
            if ((str(Final_Masc_CSV.Ocupação_Código[j])) == (str(int(Kmeans3_T.Cbo[i])))) and \
               (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) and \
               (50 <= Final_Masc_CSV.Idade_em_Anos[j] <= 59):
               Qtdade += 1
        # Assign the final count to the corresponding row in Kmeans3_T
        Kmeans3_T.M50[i] = int(Qtdade)

        # Reset Qtdade for the next age range
        Qtdade = 0
        for j in range(len(Final_Masc_CSV)):
            # Check if the current row matches the Cbo and Curso for the current index and age range 60 or more
            if ((str(Final_Masc_CSV.Ocupação_Código[j])) == (str(int(Kmeans3_T.Cbo[i])))) and \
               (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) and \
               (Final_Masc_CSV.Idade_em_Anos[j] >= 60):
               Qtdade += 1
        # Assign the final count to the corresponding row in Kmeans3_T
        Kmeans3_T.M60[i] = int(Qtdade)
             
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO_Atualizado.csv')       
    
    return   



def plot_gender_age_distribution():
    import matplotlib.pyplot as plt

    # Leitura do arquivo
    # file_path = 'graficos/Kmeans3_T_IdadeCursoCBO.csv'
    file_path = 'graficos/Kmeans3_T_IdadeCursoCBO_Atualizado.csv'
    df = pd.read_csv(file_path)

    # Somar os valores por faixa etária e gênero
    age_groups = ['29', '30-39', '40-49', '50-59', '60-69']
    female_sums = [
        pd.to_numeric(df['F29'], errors='coerce').sum(),
        pd.to_numeric(df['F30'], errors='coerce').sum(),
        pd.to_numeric(df['F40'], errors='coerce').sum(),
        pd.to_numeric(df['F50'], errors='coerce').sum(),
        pd.to_numeric(df['F60'], errors='coerce').sum()
    ]
    male_sums = [
        pd.to_numeric(df['M29'], errors='coerce').sum(),
        pd.to_numeric(df['M30'], errors='coerce').sum(),
        pd.to_numeric(df['M40'], errors='coerce').sum(),
        pd.to_numeric(df['M50'], errors='coerce').sum(),
        pd.to_numeric(df['M60'], errors='coerce').sum()
    ]

    # Criar o gráfico de barras
    x = range(len(age_groups))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar(x, female_sums, width, label='Feminino', color='pink', edgecolor='black')
    plt.bar([p + width for p in x], male_sums, width, label='Masculino', color='blue', edgecolor='black')
    plt.yscale('log')  # Apply logarithmic scale to balance the values

    plt.xlabel('Faixa Etária', fontsize=12)
    plt.ylabel('Quantidade', fontsize=12)
    # plt.title('Distribuição por gênero e faixa etária para toda a base representativa', fontsize=14)
    plt.xticks([p + width / 2 for p in x], age_groups)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Salvar o gráfico
    save_results_to = 'graficos/'
    plt.savefig(save_results_to + 'Distribuicao_Genero_FaixaEtaria_BaseRepresentativa.png')
    # plt.show()

    return

def Analise_FaixaEtaria_Geral():
        save_results_to = 'graficos/'
        save_results_too = 'processados/CSVs_ArquivoFinalGraduados/'

        file_path = save_results_to + 'Kmeans3_T.csv'
        file_path1 = save_results_too + 'Brasil_Graduados.csv'

        Kmeans3_T = pd.read_csv(file_path)
        Final = pd.read_csv(file_path1)

        Kmeans3_T = Kmeans3_T.drop(columns=['Unnamed: 0'])
        Final = Final.drop(columns=['Unnamed: 0'])

        Kmeans3_T['E29'] = ''
        Kmeans3_T['E30'] = ''
        Kmeans3_T['E40'] = ''
        Kmeans3_T['E50'] = ''
        Kmeans3_T['E60'] = ''

        for i in range(len(Kmeans3_T)):
            Qtdade = 0
            for j in range(len(Final)):
                if ((str(Final.Ocupação_Código[j])) == (str(int(Kmeans3_T.Cbo[i])))) and \
                   (str(Final.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) and \
                   (Final.Idade_em_Anos[j] <= 29):
                    Qtdade += 1
            Kmeans3_T.E29[i] = int(Qtdade)

            Qtdade = 0
            for j in range(len(Final)):
                if ((str(Final.Ocupação_Código[j])) == (str(int(Kmeans3_T.Cbo[i])))) and \
                   (str(Final.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) and \
                   (30 <= Final.Idade_em_Anos[j] <= 39):
                    Qtdade += 1
            Kmeans3_T.E30[i] = int(Qtdade)

            Qtdade = 0
            for j in range(len(Final)):
                if ((str(Final.Ocupação_Código[j])) == (str(int(Kmeans3_T.Cbo[i])))) and \
                   (str(Final.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) and \
                   (40 <= Final.Idade_em_Anos[j] <= 49):
                    Qtdade += 1
            Kmeans3_T.E40[i] = int(Qtdade)

            Qtdade = 0
            for j in range(len(Final)):
                if ((str(Final.Ocupação_Código[j])) == (str(int(Kmeans3_T.Cbo[i])))) and \
                   (str(Final.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) and \
                   (50 <= Final.Idade_em_Anos[j] <= 59):
                    Qtdade += 1
            Kmeans3_T.E50[i] = int(Qtdade)

            Qtdade = 0
            for j in range(len(Final)):
                if ((str(Final.Ocupação_Código[j])) == (str(int(Kmeans3_T.Cbo[i])))) and \
                   (str(Final.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) and \
                   (Final.Idade_em_Anos[j] >= 60):
                    Qtdade += 1
            Kmeans3_T.E60[i] = int(Qtdade)

        Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO_Geral.csv')
        return    

def plot_age_distribution_geral():
    import matplotlib.pyplot as plt

    # Leitura do arquivo
    file_path = 'graficos/Kmeans3_T_IdadeCursoCBO_Geral.csv'
    df = pd.read_csv(file_path)

    # Somar os valores por faixa etária (sem separar por gênero)
    age_groups = ['29', '30-39', '40-49', '50-59', '60-69']
    sums = [
        pd.to_numeric(df['E29'], errors='coerce').sum(),
        pd.to_numeric(df['E30'], errors='coerce').sum(),
        pd.to_numeric(df['E40'], errors='coerce').sum(),
        pd.to_numeric(df['E50'], errors='coerce').sum(),
        pd.to_numeric(df['E60'], errors='coerce').sum()
    ]

    # Criar o gráfico de barras
    x = range(len(age_groups))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar(x, sums, width, color='pink', edgecolor='black')
    plt.yscale('log')  # Escala logarítmica para balancear os valores

    plt.xlabel('Faixa Etária', fontsize=12)
    plt.ylabel('Quantidade', fontsize=12)
    # plt.title('Distribuição por faixa etária para toda a base representativa', fontsize=14)
    plt.xticks([p for p in x], age_groups)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Salvar o gráfico
    save_results_to = 'graficos/'
    plt.savefig(save_results_to + 'Distribuicao_FaixaEtaria_BaseRepresentativa_Geral.png')
    # plt.show()

    return

def split_csv_by_cluster():
    # Read the CSV file
    # file_path = 'graficos/Kmeans3_T_IdadeCursoCBO.csv'
    file_path = 'graficos/Kmeans3_T_IdadeCursoCBO_Atualizado.csv'

    df = pd.read_csv(file_path)

    # Convert the 'Cluster' column to integer
    df['Cluster'] = df['Cluster'].astype(int)

    # Split the data into separate DataFrames based on the cluster
    cluster_0 = df[df['Cluster'] == 0]
    cluster_1 = df[df['Cluster'] == 1]
    cluster_2 = df[df['Cluster'] == 2]

    # Save each cluster to a separate CSV file
    cluster_0.to_csv('graficos/Kmeans3_T_IdadeCursoCBO_Cluster0.csv', index=False)
    cluster_1.to_csv('graficos/Kmeans3_T_IdadeCursoCBO_Cluster1.csv', index=False)
    cluster_2.to_csv('graficos/Kmeans3_T_IdadeCursoCBO_Cluster2.csv', index=False)

    return

def split_csv_by_cluster_geral():
    # Read the CSV file
    file_path = 'graficos/Kmeans3_T_IdadeCursoCBO_Geral.csv'
    df = pd.read_csv(file_path)

    # Convert the 'Cluster' column to integer
    df['Cluster'] = df['Cluster'].astype(int)

    # Split the data into separate DataFrames based on the cluster
    cluster_0 = df[df['Cluster'] == 0]
    cluster_1 = df[df['Cluster'] == 1]
    cluster_2 = df[df['Cluster'] == 2]

    # Save each cluster to a separate CSV file
    cluster_0.to_csv('graficos/Kmeans3_T_IdadeCursoCBO_Geral_Cluster0.csv', index=False)
    cluster_1.to_csv('graficos/Kmeans3_T_IdadeCursoCBO_Geral_Cluster1.csv', index=False)
    cluster_2.to_csv('graficos/Kmeans3_T_IdadeCursoCBO_Geral_Cluster2.csv', index=False)

    return


def plot_gender_age_distribution_bycluster(cluster):
    import matplotlib.pyplot as plt

    if cluster == 0:
        # Leitura do arquivo
        file_path = 'graficos/Kmeans3_T_IdadeCursoCBO_Cluster0.csv'
        df = pd.read_csv(file_path)

        # Somar os valores por faixa etária e gênero
        age_groups = ['29', '30-39', '40-49', '50-59', '60-69']
        female_sums = [
            pd.to_numeric(df['F29'], errors='coerce').sum(),
            pd.to_numeric(df['F30'], errors='coerce').sum(),
            pd.to_numeric(df['F40'], errors='coerce').sum(),
            pd.to_numeric(df['F50'], errors='coerce').sum(),
            pd.to_numeric(df['F60'], errors='coerce').sum()
        ]
        male_sums = [
            pd.to_numeric(df['M29'], errors='coerce').sum(),
            pd.to_numeric(df['M30'], errors='coerce').sum(),
            pd.to_numeric(df['M40'], errors='coerce').sum(),
            pd.to_numeric(df['M50'], errors='coerce').sum(),
            pd.to_numeric(df['M60'], errors='coerce').sum()
        ]

        # Criar o gráfico de barras
        x = range(len(age_groups))
        width = 0.35

        plt.figure(figsize=(10, 6))
        plt.bar(x, female_sums, width, label='Feminino', color='pink', edgecolor='black')
        plt.bar([p + width for p in x], male_sums, width, label='Masculino', color='blue', edgecolor='black')
        plt.yscale('log')  # Apply logarithmic scale to balance the values

        plt.xlabel('Faixa Etária', fontsize=12)
        plt.ylabel('Quantidade', fontsize=12)
        # plt.title('Distribuição por gênero e faixa etária para toda a base representativa', fontsize=14)
        plt.xticks([p + width / 2 for p in x], age_groups)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Salvar o gráfico
        save_results_to = 'graficos/'
        plt.savefig(save_results_to + 'Distribuicao_Genero_FaixaEtaria_Cluster0.png')
        # plt.show()

    if cluster == 1:
        # Leitura do arquivo
        file_path = 'graficos/Kmeans3_T_IdadeCursoCBO_Cluster1.csv'
        df = pd.read_csv(file_path)

        # Somar os valores por faixa etária e gênero
        age_groups = ['29', '30-39', '40-49', '50-59', '60-69']
        female_sums = [
            pd.to_numeric(df['F29'], errors='coerce').sum(),
            pd.to_numeric(df['F30'], errors='coerce').sum(),
            pd.to_numeric(df['F40'], errors='coerce').sum(),
            pd.to_numeric(df['F50'], errors='coerce').sum(),
            pd.to_numeric(df['F60'], errors='coerce').sum()
        ]
        male_sums = [
            pd.to_numeric(df['M29'], errors='coerce').sum(),
            pd.to_numeric(df['M30'], errors='coerce').sum(),
            pd.to_numeric(df['M40'], errors='coerce').sum(),
            pd.to_numeric(df['M50'], errors='coerce').sum(),
            pd.to_numeric(df['M60'], errors='coerce').sum()
        ]

        # Criar o gráfico de barras
        x = range(len(age_groups))
        width = 0.35

        plt.figure(figsize=(10, 6))
        plt.bar(x, female_sums, width, label='Feminino', color='pink', edgecolor='black')
        plt.bar([p + width for p in x], male_sums, width, label='Masculino', color='blue', edgecolor='black')
        plt.yscale('log')  # Apply logarithmic scale to balance the values

        plt.xlabel('Faixa Etária', fontsize=12)
        plt.ylabel('Quantidade', fontsize=12)
        # plt.title('Distribuição por gênero e faixa etária para toda a base representativa', fontsize=14)
        plt.xticks([p + width / 2 for p in x], age_groups)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Salvar o gráfico
        save_results_to = 'graficos/'
        plt.savefig(save_results_to + 'Distribuicao_Genero_FaixaEtaria_Cluster1.png')
        # plt.show()    


    if cluster == 2:
        # Leitura do arquivo
        file_path = 'graficos/Kmeans3_T_IdadeCursoCBO_Cluster2.csv'
        df = pd.read_csv(file_path)

        # Somar os valores por faixa etária e gênero
        age_groups = ['29', '30-39', '40-49', '50-59', '60-69']
        female_sums = [
            pd.to_numeric(df['F29'], errors='coerce').sum(),
            pd.to_numeric(df['F30'], errors='coerce').sum(),
            pd.to_numeric(df['F40'], errors='coerce').sum(),
            pd.to_numeric(df['F50'], errors='coerce').sum(),
            pd.to_numeric(df['F60'], errors='coerce').sum()
        ]
        male_sums = [
            pd.to_numeric(df['M29'], errors='coerce').sum(),
            pd.to_numeric(df['M30'], errors='coerce').sum(),
            pd.to_numeric(df['M40'], errors='coerce').sum(),
            pd.to_numeric(df['M50'], errors='coerce').sum(),
            pd.to_numeric(df['M60'], errors='coerce').sum()
        ]

        # Criar o gráfico de barras
        x = range(len(age_groups))
        width = 0.35

        plt.figure(figsize=(10, 6))
        plt.bar(x, female_sums, width, label='Feminino', color='pink', edgecolor='black')
        plt.bar([p + width for p in x], male_sums, width, label='Masculino', color='blue', edgecolor='black')
        plt.yscale('log')  # Apply logarithmic scale to balance the values

        plt.xlabel('Faixa Etária', fontsize=12)
        plt.ylabel('Quantidade', fontsize=12)
        # plt.title('Distribuição por gênero e faixa etária para toda a base representativa', fontsize=14)
        plt.xticks([p + width / 2 for p in x], age_groups)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Salvar o gráfico
        save_results_to = 'graficos/'
        plt.savefig(save_results_to + 'Distribuicao_Genero_FaixaEtaria_Cluster2.png')
        # plt.show()       

    return
# def plot_age_distribution_bycluster(cluster):
# def plot_age_distribution_bycluster():
#     import matplotlib.pyplot as plt

#     # if cluster == 0:
#     file_path = 'graficos/Kmeans3_T_IdadeCursoCBO_Geral_Cluster0.csv'
#     df = pd.read_csv(file_path)
#     age_groups = ['29', '30-39', '40-49', '50-59', '60-69']
#     sums = [
#         pd.to_numeric(df['E29'], errors='coerce').sum(),
#         pd.to_numeric(df['E30'], errors='coerce').sum(),
#         pd.to_numeric(df['E40'], errors='coerce').sum(),
#         pd.to_numeric(df['E50'], errors='coerce').sum(),
#         pd.to_numeric(df['E60'], errors='coerce').sum()
#     ]
#     x = range(len(age_groups))
#     width = 0.5
#     plt.figure(figsize=(10, 6))
#     plt.bar(x, sums, width, color='pink', edgecolor='black')
#     plt.yscale('log')
#     plt.xlabel('Faixa Etária', fontsize=12)
#     plt.ylabel('Quantidade', fontsize=12)
#     plt.xticks([p for p in x], age_groups)
#     plt.grid(axis='y', linestyle='--', alpha=0.7)
#     plt.tight_layout()
#     save_results_to = 'graficos/'
#     plt.savefig(save_results_to + 'Distribuicao_FaixaEtaria_Cluster0.png')

#     # if cluster == 1:
#     file_path = 'graficos/Kmeans3_T_IdadeCursoCBO_Geral_Cluster1.csv'
#     df = pd.read_csv(file_path)
#     age_groups = ['29', '30-39', '40-49', '50-59', '60-69']
#     sums = [
#         pd.to_numeric(df['E29'], errors='coerce').sum(),
#         pd.to_numeric(df['E30'], errors='coerce').sum(),
#         pd.to_numeric(df['E40'], errors='coerce').sum(),
#         pd.to_numeric(df['E50'], errors='coerce').sum(),
#         pd.to_numeric(df['E60'], errors='coerce').sum()
#     ]
#     x = range(len(age_groups))
#     width = 0.5
#     plt.figure(figsize=(10, 6))
#     plt.bar(x, sums, width, color='pink', edgecolor='black')
#     plt.yscale('log')
#     plt.xlabel('Faixa Etária', fontsize=12)
#     plt.ylabel('Quantidade', fontsize=12)
#     plt.xticks([p for p in x], age_groups)
#     plt.grid(axis='y', linestyle='--', alpha=0.7)
#     plt.tight_layout()
#     save_results_to = 'graficos/'
#     plt.savefig(save_results_to + 'Distribuicao_FaixaEtaria_Cluster1.png')

#     # if cluster == 2:
#     file_path = 'graficos/Kmeans3_T_IdadeCursoCBO_Geral_Cluster2.csv'
#     df = pd.read_csv(file_path)
#     age_groups = ['29', '30-39', '40-49', '50-59', '60-69']
#     sums = [
#         pd.to_numeric(df['E29'], errors='coerce').sum(),
#         pd.to_numeric(df['E30'], errors='coerce').sum(),
#         pd.to_numeric(df['E40'], errors='coerce').sum(),
#         pd.to_numeric(df['E50'], errors='coerce').sum(),
#         pd.to_numeric(df['E60'], errors='coerce').sum()
#     ]
#     x = range(len(age_groups))
#     width = 0.5
#     plt.figure(figsize=(10, 6))
#     plt.bar(x, sums, width, color='pink', edgecolor='black')
#     plt.yscale('log')
#     plt.xlabel('Faixa Etária', fontsize=12)
#     plt.ylabel('Quantidade', fontsize=12)
#     plt.xticks([p for p in x], age_groups)
#     plt.grid(axis='y', linestyle='--', alpha=0.7)
#     plt.tight_layout()
#     save_results_to = 'graficos/'
#     plt.savefig(save_results_to + 'Distribuicao_FaixaEtaria_Cluster2.png')

#     return

def plot_age_distribution_bycluster_1():
    import matplotlib.pyplot as plt

    # File paths for each cluster
    files = [
        ('graficos/Kmeans3_T_IdadeCursoCBO_Geral_Cluster0.csv', 'Cluster 0', 'red'),
        ('graficos/Kmeans3_T_IdadeCursoCBO_Geral_Cluster1.csv', 'Cluster 1', 'blue'),
        ('graficos/Kmeans3_T_IdadeCursoCBO_Geral_Cluster2.csv', 'Cluster 2', 'green')
    ]
    age_groups = ['29', '30-39', '40-49', '50-59', '60-69']
    width = 0.25
    x = range(len(age_groups))

    plt.figure(figsize=(10, 6))

    for idx, (file_path, label, color) in enumerate(files):
        df = pd.read_csv(file_path)
        sums = [
            pd.to_numeric(df['E29'], errors='coerce').sum(),
            pd.to_numeric(df['E30'], errors='coerce').sum(),
            pd.to_numeric(df['E40'], errors='coerce').sum(),
            pd.to_numeric(df['E50'], errors='coerce').sum(),
            pd.to_numeric(df['E60'], errors='coerce').sum()
        ]
        plt.bar([p + width * idx for p in x], sums, width=width, color=color, edgecolor='black', label=label)

    plt.yscale('log')
    plt.xlabel('Faixa Etária', fontsize=12)
    plt.ylabel('Quantidade', fontsize=12)
    plt.xticks([p + width for p in x], age_groups)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    save_results_to = 'graficos/'
    plt.savefig(save_results_to + 'Distribuicao_FaixaEtaria_Clusters_Juntos.png')
    # plt.show()
    return

def extract_data_by_course_cbo():
    # Read the CSV file
    df = pd.read_csv("graficos/Kmeans3_T_IdadeCursoCBO.csv")
    # Convert columns to integers
    df['Cbo'] = df['Cbo'].astype(int)
    df['Curso'] = df['Curso'].astype(int)
    df['Cluster'] = df['Cluster'].astype(int)

    Curso = [212,  724,  321,  342,   342,   344,  380,  581]
    Cbo   = [2354, 2261, 2642, 1221,  2431,  2411, 2611, 2161]


    # Filter by course and cbo
    # filtered_df = df[(df['Curso'] == Curso[0]) & (df['Cbo'] == Cbo[0])]
    for i in range(len(Curso)): 
        filtered_df = df[(df['Curso'] == Curso[i]) & (df['Cbo'] == Cbo[i])]
        save_results_to = 'graficos/'
        filtered_df.to_csv(save_results_to + "filtered_data.csv", index=False)
        plot_gender_age_distribution_cbo('filtered_data.csv', str(Cbo[i]))

    
    # Save the filtered dataframe to a new file
    # save_results_to = 'graficos/'
    # filtered_df.to_csv(save_results_to + "filtered_data.csv", index=False)
    # plot_gender_age_distribution_cbo('filtered_data.csv', str(Cbo[0]))



def plot_gender_age_distribution_cbo(path,Cbo):
    import matplotlib.pyplot as plt

    save_results_to = 'graficos/'
    # Leitura do arquivo
    file_path = save_results_to + path
    df = pd.read_csv(file_path)

    # Somar os valores por faixa etária e gênero
    age_groups = ['29', '30-39', '40-49', '50-59', '60-69']
    female_sums = [
        pd.to_numeric(df['F29'], errors='coerce').sum(),
        pd.to_numeric(df['F30'], errors='coerce').sum(),
        pd.to_numeric(df['F40'], errors='coerce').sum(),
        pd.to_numeric(df['F50'], errors='coerce').sum(),
        pd.to_numeric(df['F60'], errors='coerce').sum()
    ]
    male_sums = [
        pd.to_numeric(df['M29'], errors='coerce').sum(),
        pd.to_numeric(df['M30'], errors='coerce').sum(),
        pd.to_numeric(df['M40'], errors='coerce').sum(),
        pd.to_numeric(df['M50'], errors='coerce').sum(),
        pd.to_numeric(df['M60'], errors='coerce').sum()
    ]

    # Criar o gráfico de barras
    x = range(len(age_groups))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar(x, female_sums, width, label='Feminino', color='pink', edgecolor='black')
    plt.bar([p + width for p in x], male_sums, width, label='Masculino', color='blue', edgecolor='black')
    plt.yscale('log')  # Apply logarithmic scale to balance the values

    plt.xlabel('Faixa Etária', fontsize=12)
    plt.ylabel('Quantidade', fontsize=12)
    # plt.title('Distribuição por gênero e faixa etária para toda a base representativa', fontsize=14)
    plt.xticks([p + width / 2 for p in x], age_groups)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Salvar o gráfico
    save_results_to = 'graficos/'
    plt.savefig(save_results_to + "Distribuicao_Genero_FaixaEtaria" + Cbo + ".png")
    # plt.show()

    return 

def split_csv_by_cluster_1():
    # Read the CSV file
    file_path = 'graficos/Kmeans3_T.csv'
    df = pd.read_csv(file_path)

    # Convert columns to integer
    df['Cbo'] = df['Cbo'].astype(int)
    df['Curso'] = df['Curso'].astype(int)
    df['Cluster'] = df['Cluster'].astype(int)

    # Capitalize the first letter of each word in the columns
    df['Cbo_Nome'] = df['Cbo_Nome'].str.title()
    df['Curso_Nome'] = df['Curso_Nome'].str.title()

    # Split the data by cluster
    cluster_0 = df[df['Cluster'] == 0]
    cluster_1 = df[df['Cluster'] == 1]
    cluster_2 = df[df['Cluster'] == 2]

    # Save the data to separate files
    save_results_to = 'graficos/'
    cluster_0.to_csv(save_results_to + 'Kmeans3_T_cluster_0.csv', index=False)
    cluster_1.to_csv(save_results_to + 'Kmeans3_T_cluster_1.csv', index=False)
    cluster_2.to_csv(save_results_to + 'Kmeans3_T_cluster_2.csv', index=False)
    

def save_csv_to_table(cluster):
    # Read the CSV file
    if cluster == 0:
        df = pd.read_csv('graficos/Kmeans3_T_cluster_0.csv')

        # Remove the 'Unnamed: 0' column
        df = df.drop('Unnamed: 0', axis=1)
        df = df.drop('Ida', axis=1)
        df = df.drop('Volta', axis=1)

        # Save the records in a LaTeX table
        latex_table = df.to_latex(index=False, caption="Cluster 0 - Profissões e Cursos ", label="tab:Profissoes_Cluster0") 

        # Salvar em um arquivo .tex
        with open("tabelas/Kmeans3_T_cluster_0.tex", "w") as f:
            f.write(latex_table)

    if cluster ==1:
        df = pd.read_csv('graficos/Kmeans3_T_cluster_1.csv')

        # Remove the 'Unnamed: 0' column
        df = df.drop('Unnamed: 0', axis=1)
        df = df.drop('Ida', axis=1)
        df = df.drop('Volta', axis=1)

        # Save the records in a LaTeX table
        latex_table = df.to_latex(index=False, caption="Cluster 1 - Profissões e Cursos ", label="tab:Profissoes_Cluster1") 

        # Salvar em um arquivo .tex
        with open("tabelas/Kmeans3_T_cluster_1.tex", "w") as f:
            f.write(latex_table)

    if cluster == 2:
        df = pd.read_csv('graficos/Kmeans3_T_cluster_2.csv')

        # Remove the 'Unnamed: 0' column
        df = df.drop('Unnamed: 0', axis=1)
        df = df.drop('Ida', axis=1)
        df = df.drop('Volta', axis=1)

        # Save the records in a LaTeX table
        latex_table = df.to_latex(index=False, caption="Cluster 2 - Profissões e Cursos ", label="tab:Profissoes_Cluster2") 

        # Salvar em um arquivo .tex
        with open("tabelas/Kmeans3_T_cluster_2.tex", "w") as f:
            f.write(latex_table)        
    return

def diminuir_and_save_csv():
    # Process the first file
    file_path_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv'
    df_graduados = pd.read_csv(file_path_graduados)

    # Subtract one digit from the specified columns
    df_graduados['Curso_Superior_Graduação_Código'] = df_graduados['Curso_Superior_Graduação_Código'].astype(str).str[:-1].astype(int)
    df_graduados['Ocupação_Código'] = df_graduados['Ocupação_Código'].astype(str).str[:-1].astype(int)

    # Save the transformed DataFrame to a new file
    save_results_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_Diminuido.csv'
    df_graduados.to_csv(save_results_graduados, index=False)

    # Process the second file
    file_path_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal.csv'
    df_pivot = pd.read_csv(file_path_pivot)

    # Subtract one digit from the Ocupação_Código column
    df_pivot['Ocupação_Código'] = df_pivot['Ocupação_Código'].astype(str).str[:-1].astype(int)

    # Save the transformed DataFrame to a new file
    save_results_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_Diminuida.csv'
    df_pivot.to_csv(save_results_pivot, index=False)

    return
def diminuir_and_save_csv_CBO():
    # Process the first file
    file_path_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv'
    df_graduados = pd.read_csv(file_path_graduados)

    # Subtract one digit from the specified columns
    # df_graduados['Curso_Superior_Graduação_Código'] = df_graduados['Curso_Superior_Graduação_Código'].astype(str).str[:-1].astype(int)
    df_graduados['Ocupação_Código'] = df_graduados['Ocupação_Código'].astype(str).str[:-1].astype(int)

    # Save the transformed DataFrame to a new file
    save_results_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_Diminuido_CBO.csv'
    df_graduados.to_csv(save_results_graduados, index=False)

    # Process the second file
    file_path_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal.csv'
    df_pivot = pd.read_csv(file_path_pivot)

    # Subtract one digit from the Ocupação_Código column
    df_pivot['Ocupação_Código'] = df_pivot['Ocupação_Código'].astype(str).str[:-1].astype(int)

    # Save the transformed DataFrame to a new file
    save_results_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_Diminuida_CBO.csv'
    df_pivot.to_csv(save_results_pivot, index=False)

    return
# def ibge_cursos_filter_1(path,name):   
# def ibge_cursos_filter_1(path,name):   
def ibge_cursos_filter_1():  
    #...
    path ='documentacao/'
    name ='Curso_CSV.csv'
    file = os.path.join(path,name)
    cursos = pd.read_csv(file, dtype ='str')
    CURSO = []
    NOME  = []
    for i in range(len(cursos)):
        # print(len(cursos.Cod_Curso[i]))
        # if len(cursos.Cod_Curso[i]) >=5:
        if len(cursos.Cod_Curso[i]) ==2:
           CURSO.append(cursos.Cod_Curso[i])
           NOME.append(cursos.Nome_Curso[i])
           #print(cursos.Cod_Curso[i])     
              
    Cursos_Censo=[]
    for i in range(len(CURSO)):
        tupla=(CURSO[i],NOME[i])
        Cursos_Censo.append(tupla)
    #...
    CursosCenso = pd.DataFrame(Cursos_Censo)
    #Curso_Cbo_dir_curso_cbos.shape
    nomes = {0:"curso_num",
             1:"curso_nome",
            }
    CursosCenso.rename(columns=nomes,inplace=True)
    CursosCenso = CursosCenso.sort_values(by=['curso_num'])    
    CursosCenso['curso_num'] = CursosCenso['curso_num'].astype(int)   
    CursosCenso.to_csv(path + 'Curso_Censo_Diminuido.csv')       
    return CursosCenso


# def Ida_Volta_1(path,name,path1,name1):
def Ida_Volta_CBO():


    logging.info(" Gerando as idas e voltas")   
    # csv_estado = os.path.join(path[0],name[0]) # arquivo do censo do Brasil inteiro (somente graduados)
    # path1 = ibge_variable.paths(12)
    # name1 = ibge_variable.names(6)
    csv_estado = os.path.join('processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_Diminuido_CBO.csv') # arquivo do censo do Brasil inteiro (somente graduados)
    # csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
    # csv_CURSOS = os.path.join(path1[0],name1[2]) # Tabela de Cursos
    csv_CBO = os.path.join('documentacao/CBO_CSV.csv') # Tabela de CBOs
    # csv_CURSOS = os.path.join('documentacao/Curso_Censo_Diminuido.csv') # Tabela de Cursos
    csv_CURSOS = os.path.join('documentacao/Curso_Censo.csv') # Tabela de Cursos
    # path2 = ibge_variable.paths(8)
    # name2 = ibge_variable.names(8)         
    # csv_PivotTableFinal =  os.path.join(path2[0],name2[0]) #Pivo Table Final
    csv_PivotTableFinal =  os.path.join('processados/CSVs_PivotTableFinal/Brasil_PivotFinal_Diminuida_CBO.csv') #Pivo Table Final
    
    path ='documentacao/'
    name ='Curso_Censo.csv'
    file = os.path.join(path,name)
    CursosCenso = pd.read_csv(file, dtype ='str')
    # CursosCenso = ibge_cursos_filter_1()
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
    # for f in range(0,23):

       
        # curso_num= float(CursosCenso.curso_num.iloc[f])
        curso_num= CursosCenso.curso_num.iloc[f]
        # print(curso_num)
        curso_nome= CursosCenso.curso_nome.iloc[f]
        titulo10= "Course " + str( CursosCenso.curso_num.iloc[f])+ ": " + CursosCenso.curso_nome.iloc[f] + " - 10% "
        titulo3=  "Course " + str(CursosCenso.curso_num.iloc[f]) + ": " + CursosCenso.curso_nome.iloc[f] + " - 10%"
        print("curso_num:", curso_num, "curso_nome:",curso_nome)
        # print(f)
        # print("=================================================================================================")
        
        #======================================================Plotando os cbos de determinado curso, usando função ...
        primeirosCbos,primeirosCbos_Nome,Porcentagens,CURSO_NUM,CURSO_NOME=ibge_functions_descriptive_analysis_1.CBOs_Curso_v6_1(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0.1,save_results_to)
        print("primeirosCbos:", primeirosCbos)
        print("primeirosCbos_Nome:", primeirosCbos_Nome)
        print("CURSO_NUM:", CURSO_NUM)
        print("CURSO_NOME:", CURSO_NOME)
        print("=================================================================================================")

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
                    CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=ibge_functions_descriptive_analysis_1.Cursos_CBO_13_10_1(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],Graduados_Nao[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.1,save_results_to)
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
    df.to_csv(save_results_to + '10Porcent_DF_Diminuido_CBO.csv')
    return     

# def Tabela_Ida_Volta_1(path2,name2):
def Tabela_Ida_Volta_CBO():
    # df =  os.path.join(path2[0],name2[1])
    # df1 = pd.read_csv(df)    
    df1 = pd.read_csv('graficos/10Porcent_DF_Diminuido_CBO.csv')
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
    df1.to_csv(save_results_to + '10Porcent_DF_Limpo_Diminuido_CBO.csv')
    df1.to_excel(save_results_to + '10Porcent_DF_Limpo_Diminuido_CBO.xlsx')
    return    

def Ida_Volta_1():
    logging.info(" Gerando as idas e voltas")   
    # csv_estado = os.path.join(path[0],name[0]) # arquivo do censo do Brasil inteiro (somente graduados)
    # path1 = ibge_variable.paths(12)
    # name1 = ibge_variable.names(6)
    csv_estado = os.path.join('processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_Diminuido.csv') # arquivo do censo do Brasil inteiro (somente graduados)
    # csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
    # csv_CURSOS = os.path.join(path1[0],name1[2]) # Tabela de Cursos
    csv_CBO = os.path.join('documentacao/CBO_CSV.csv') # Tabela de CBOs
    csv_CURSOS = os.path.join('documentacao/Curso_Censo_Diminuido.csv') # Tabela de Cursos
    # path2 = ibge_variable.paths(8)
    # name2 = ibge_variable.names(8)         
    # csv_PivotTableFinal =  os.path.join(path2[0],name2[0]) #Pivo Table Final
    csv_PivotTableFinal =  os.path.join('processados/CSVs_PivotTableFinal/Brasil_PivotFinal_Diminuida.csv') #Pivo Table Final
    

    # CursosCenso = ibge_cursos_filter_1(path1[0],name1[2])
    CursosCenso = ibge_cursos_filter_1()
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
    #for f in range(0,89):
    for f in range(0,23):

       
        # curso_num= float(CursosCenso.curso_num.iloc[f])
        curso_num= CursosCenso.curso_num.iloc[f]
        # print(curso_num)
        curso_nome= CursosCenso.curso_nome.iloc[f]
        titulo10= "Course " + str( CursosCenso.curso_num.iloc[f])+ ": " + CursosCenso.curso_nome.iloc[f] + " - 10% "
        titulo3=  "Course " + str(CursosCenso.curso_num.iloc[f]) + ": " + CursosCenso.curso_nome.iloc[f] + " - 10%"
        print("curso_num:", curso_num, "curso_nome:",curso_nome)
        # print(f)
        # print("=================================================================================================")
        
        #======================================================Plotando os cbos de determinado curso, usando função ...
        primeirosCbos,primeirosCbos_Nome,Porcentagens,CURSO_NUM,CURSO_NOME=ibge_functions_descriptive_analysis_1.CBOs_Curso_v6_1(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0.1,save_results_to)
        print("primeirosCbos:", primeirosCbos)
        print("primeirosCbos_Nome:", primeirosCbos_Nome)
        print("CURSO_NUM:", CURSO_NUM)
        print("CURSO_NOME:", CURSO_NOME)
        print("=================================================================================================")

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
                    CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=ibge_functions_descriptive_analysis_1.Cursos_CBO_13_10_1(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],Graduados_Nao[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.1,save_results_to)
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
    df.to_csv(save_results_to + '10Porcent_DF_Diminuido.csv')
    return     

# def Tabela_Ida_Volta_1(path2,name2):
def Tabela_Ida_Volta_1():
    # df =  os.path.join(path2[0],name2[1])
    # df1 = pd.read_csv(df)    
    df1 = pd.read_csv('graficos/10Porcent_DF_Diminuido.csv')
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
    df1.to_csv(save_results_to + '10Porcent_DF_Limpo_Diminuido.csv')
    df1.to_excel(save_results_to + '10Porcent_DF_Limpo_Diminuido.xlsx')
    return    

    
def diminuir_and_save_csv_CURSO():
    # Process the first file
    file_path_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv'
    df_graduados = pd.read_csv(file_path_graduados)

    # Subtract one digit from the specified columns
    df_graduados['Curso_Superior_Graduação_Código'] = df_graduados['Curso_Superior_Graduação_Código'].astype(str).str[:-1].astype(int)
    # df_graduados['Ocupação_Código'] = df_graduados['Ocupação_Código'].astype(str).str[:-1].astype(int)

    # Save the transformed DataFrame to a new file
    save_results_graduados = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_Diminuido_Curso.csv'
    df_graduados.to_csv(save_results_graduados, index=False)

    # Process the second file
    # file_path_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal.csv'
    # df_pivot = pd.read_csv(file_path_pivot)

    # Subtract one digit from the Ocupação_Código column
    # df_pivot['Ocupação_Código'] = df_pivot['Ocupação_Código'].astype(str).str[:-1].astype(int)

    # Save the transformed DataFrame to a new file
    # save_results_pivot = 'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_Diminuida_CBO.csv'
    # df_pivot.to_csv(save_results_pivot, index=False)

    return

def Ida_Volta_Curso():
    logging.info(" Gerando as idas e voltas")   
    # csv_estado = os.path.join(path[0],name[0]) # arquivo do censo do Brasil inteiro (somente graduados)
    # path1 = ibge_variable.paths(12)
    # name1 = ibge_variable.names(6)
    csv_estado = os.path.join('processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_Diminuido_Curso.csv') # arquivo do censo do Brasil inteiro (somente graduados)
    # csv_CBO = os.path.join(path1[0],name1[1]) # Tabela de CBOs
    # csv_CURSOS = os.path.join(path1[0],name1[2]) # Tabela de Cursos
    csv_CBO = os.path.join('documentacao/CBO_CSV.csv') # Tabela de CBOs
    csv_CURSOS = os.path.join('documentacao/Curso_Censo_Diminuido.csv') # Tabela de Cursos
    # path2 = ibge_variable.paths(8)
    # name2 = ibge_variable.names(8)         
    # csv_PivotTableFinal =  os.path.join(path2[0],name2[0]) #Pivo Table Final
    csv_PivotTableFinal =  os.path.join('processados/CSVs_PivotTableFinal/Brasil_PivotFinal.csv') #Pivo Table Final
    

    # CursosCenso = ibge_cursos_filter_1(path1[0],name1[2])
    CursosCenso = ibge_cursos_filter_1()
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
    #for f in range(0,89):
    for f in range(0,1):

       
        # curso_num= float(CursosCenso.curso_num.iloc[f])
        curso_num= CursosCenso.curso_num.iloc[f]
        # print(curso_num)
        curso_nome= CursosCenso.curso_nome.iloc[f]
        titulo10= "Course " + str( CursosCenso.curso_num.iloc[f])+ ": " + CursosCenso.curso_nome.iloc[f] + " - 10% "
        titulo3=  "Course " + str(CursosCenso.curso_num.iloc[f]) + ": " + CursosCenso.curso_nome.iloc[f] + " - 10%"
        print("curso_num:", curso_num, "curso_nome:",curso_nome)
        # print(f)
        # print("=================================================================================================")
        
        #======================================================Plotando os cbos de determinado curso, usando função ...
        primeirosCbos,primeirosCbos_Nome,Porcentagens,CURSO_NUM,CURSO_NOME=ibge_functions_descriptive_analysis_1.CBOs_Curso_v6_1(csv_estado,csv_CBO,curso_num,curso_nome,titulo10,titulo3,0.1,save_results_to)
        print("primeirosCbos:", primeirosCbos)
        print("primeirosCbos_Nome:", primeirosCbos_Nome)
        print("CURSO_NUM:", CURSO_NUM)
        print("CURSO_NOME:", CURSO_NOME)
        print("=================================================================================================")

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
                    CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=ibge_functions_descriptive_analysis_1.Cursos_CBO_14_10_1(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.1)
                    if (cursos_vol!=0)&(nomes_vol!=0)&(porcentagens_vol!=0):
                        Intensidade.append(intensidade)
                        # print(intensidade)
                        Porcentagens_vol.append(porcentagens_vol)
                        CBO_vol.append(CBO)
                        Cursos_vol.append(cursos_vol)
                        Nomes_vol.append(nomes_vol)                        
                else:
                    print(primeirosCbos[i])
                    CBO,Curso,tresprimeirosCursos,intensidade,fig,string,cursos_vol, nomes_vol, porcentagens_vol=ibge_functions_descriptive_analysis_1.Cursos_CBO_13_10_1(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3,NaoGraduados[i],Graduados_Nao[i],curso_num,curso_nome,primeirosCbos_Nome,i,0.1,save_results_to)
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
    df.to_csv(save_results_to + '10Porcent_DF_Diminuido_Curso.csv')
    return    


# def Tabela_Ida_Volta_1(path2,name2):
def Tabela_Ida_Volta_Curso():
    # df =  os.path.join(path2[0],name2[1])
    # df1 = pd.read_csv(df)    
    df1 = pd.read_csv('graficos/10Porcent_DF_Diminuido_Curso.csv')
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
    df1.to_csv(save_results_to + '10Porcent_DF_Limpo_Diminuido_Curso.csv')
    df1.to_excel(save_results_to + '10Porcent_DF_Limpo_Diminuido_Curso.xlsx')
    return   

def transform_columns_to_int_and_save():
    # Define file paths
    files = [
        'documentacao/CBO_CSV.csv',
        # 'documentacao/Curso_CSV.csv',
        # 'documentacao/Curso_Censo.csv',
        'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv',
        'processados/CSVs_PivotTableFinal/Brasil_PivotFinal.csv',
        # 'documentacao/Curso_Censo_Diminuido.csv',
        'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_Diminuido_CBO.csv',
        'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_Diminuida_CBO.csv'
    ]

    # Define columns to transform
    columns_to_transform = ['Cod_CBO', 'curso_num', 'Cod_Curso']

    for file in files:
        try:
            # Read the CSV file
            df = pd.read_csv(file, dtype=str)

            # Transform specified columns to integers if they exist
            for column in columns_to_transform:
                if column in df.columns:
                    df[column] = df[column].astype(float).astype(int)

            # Save the transformed DataFrame back to the same file
            df.to_csv(file, index=False)
            print(f"Processed and saved file: {file}")
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    return
def transform_columns_to_int_and_save_CBO():
    # Define file paths
    files = [
        'documentacao/CBO_CSV.csv',
        # 'documentacao/Curso_CSV.csv',
        # 'documentacao/Curso_Censo.csv',
        'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv',
        'processados/CSVs_PivotTableFinal/Brasil_PivotFinal.csv',
        # 'documentacao/Curso_Censo_Diminuido.csv',
        'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_Diminuido_CBO.csv',
        'processados/CSVs_PivotTableFinal/Brasil_PivotFinal_Diminuida_CBO.csv'
    ]

    # Define columns to transform
    columns_to_transform = ['Cod_CBO', 'curso_num', 'Cod_Curso']

    for file in files:
        try:
            # Read the CSV file
            df = pd.read_csv(file, dtype=str)

            # Transform specified columns to integers if they exist
            for column in columns_to_transform:
                if column in df.columns:
                    df[column] = df[column].astype(float).astype(int)

            # Save the transformed DataFrame back to the same file
            df.to_csv(file, index=False)
            print(f"Processed and saved file: {file}")
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    return

def voronoi_1():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.spatial import Voronoi, voronoi_plot_2d
    import pandas as pd

    # Load data from CSV
    file_path = 'graficos/Filled_Updated_Processed_Kmeans_Results.csv'
    df = pd.read_csv(file_path)

    # Define Voronoi points
    points = np.array([[27.00526316, 21.78263158], [66.464375, 77.656875], [25.76357143, 62.88071429]])

    # Generate the Voronoi diagram for the points
    vor = Voronoi(points)

    # Plot the Voronoi diagram
    fig, ax = plt.subplots(figsize=(10, 10))
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange', line_width=2, line_alpha=0.6, point_size=2)

    # Plot the Voronoi points
    ax.scatter(points[:, 0], points[:, 1], color='yellow', s=150, label='Voronoi', edgecolor='black')

    # Classify and plot the points from the CSV
    for _, row in df.iterrows():
        x, y, cluster = row['Ida'], row['Volta'], row['Cluster']
        if cluster == 0:  # Cluster 0
            ax.scatter(x, y, color='red', label='Cluster 0', edgecolor='black')
        elif cluster == 1:  # Cluster 1
            ax.scatter(x, y, color='blue', label='Cluster 1', edgecolor='black')
        elif cluster == 2:  # Cluster 2
            ax.scatter(x, y, color='green', label='Cluster 2', edgecolor='black')

    # Remove duplicate labels in the legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    # Set plot limits and labels
    plt.xlim(0.0, 100.0)
    plt.ylim(0.0, 100.0)
    plt.xlabel('Cursos')
    plt.ylabel('Profissões')
    # plt.title('Voronoi Diagram with Points from CSV')

    # Save the plot
    save_results_to = 'graficos/'
    plt.savefig(save_results_to + 'voronoi_with_csv_points.png')

    return


def split_Kmeans3_T_Profissoes_Cursos_Menor_CBO_by_cluster(input_file, n_clusters):

    df = pd.read_csv(f'graficos/{input_file}')

    # Garante que a coluna Cluster está como float
    df['Cluster'] = df['Cluster'].astype(float)

    for i in range(n_clusters):
        cluster_df = df[df['Cluster'] == float(i)]
        output_path = f'graficos/{input_file.replace(".csv", "")}_Cluster{i}.csv'
        cluster_df.to_csv(output_path, index=False)

    return

def caracterizar_cluster0():

    # Leitura do arquivo
    file_path = 'graficos/Kmeans3_T_Profissoes_Cursos_Menor_CBO_Cluster0.csv'
    df = pd.read_csv(file_path)

    # Remover coluna 'Unnamed: 0' se existir
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    # Transformar coluna Cluster para inteiro
    if 'Cluster' in df.columns:
        df['Cluster'] = df['Cluster'].astype(int)

    # Mapeamentos simples para exemplo (ajuste conforme necessário)
    area_conhecimento_map = {
        'Matemática': 'Exatas',
        'Engenharia': 'Exatas',
        'Física': 'Exatas',
        'Química': 'Exatas',
        'Direito': 'Humanas',
        'Administração': 'Humanas',
        'Psicologia': 'Saúde',
        'Medicina': 'Saúde',
        'Enfermagem': 'Saúde',
        'Pedagogia': 'Humanas',
        'História': 'Humanas',
        'Biologia': 'Exatas',
        'Computação': 'Exatas',
        'Educação Física': 'Saúde',
        # Adicione mais conforme necessário
    }

    tipo_competencia_map = {
        'Programador': 'Programação',
        'Analista de Sistemas': 'Programação',
        'Gerente': 'Gestão',
        'Professor': 'Educação',
        'Médico': 'Atendimento à Saúde',
        'Enfermeiro': 'Atendimento à Saúde',
        'Psicólogo': 'Atendimento à Saúde',
        'Advogado': 'Gestão',
        'Vendedor': 'Atendimento ao Cliente',
        'Engenheiro': 'Gestão',
        # Adicione mais conforme necessário
    }

    setor_economico_map = {
        'Professor': 'Educação',
        'Médico': 'Saúde',
        'Enfermeiro': 'Saúde',
        'Psicólogo': 'Saúde',
        'Advogado': 'Serviços',
        'Engenheiro': 'Indústria',
        'Programador': 'Serviços',
        'Vendedor': 'Serviços',
        'Gerente': 'Serviços',
        # Adicione mais conforme necessário
    }

    # Funções auxiliares para mapear os valores
    def get_area_conhecimento(curso_nome):
        for key in area_conhecimento_map:
            if key.lower() in str(curso_nome).lower():
                return area_conhecimento_map[key]
        return 'Outro'

    def get_tipo_competencia(cbo_nome):
        for key in tipo_competencia_map:
            if key.lower() in str(cbo_nome).lower():
                return tipo_competencia_map[key]
        return 'Outro'

    def get_setor_economico(cbo_nome):
        for key in setor_economico_map:
            if key.lower() in str(cbo_nome).lower():
                return setor_economico_map[key]
        return 'Outro'

    # Aplicar as funções para criar as novas colunas
    df['area_conhecimento'] = df['Curso_Nome'].apply(get_area_conhecimento)
    df['tipo_Competencia_Tecnica'] = df['Cbo_Nome'].apply(get_tipo_competencia)
    df['Setor_Economico'] = df['Cbo_Nome'].apply(get_setor_economico)

    # Salvar o arquivo caracterizado
    output_path = 'graficos/Kmeans3_T_Profissoes_Cursos_Menor_CBO_Cluster0_Caracterizacao.csv'
    df.to_csv(output_path, index=False)

    # Nomear o cluster de acordo com a análise (exemplo: "Cluster de Saúde e Educação")
    cluster_nome = "Cluster de Saúde e Educação"

    # Salvar o nome do cluster em um arquivo
    with open('graficos/Kmeans3_T_Profissoes_Cursos_Menor_CBO_Cluster0_nome.txt', 'w') as f:
        f.write(cluster_nome)

    print(f"Arquivo salvo em: {output_path}")
    print(f"Nome do cluster salvo em: graficos/Kmeans3_T_Profissoes_Cursos_Menor_CBO_Cluster0_nome.txt")

    return
