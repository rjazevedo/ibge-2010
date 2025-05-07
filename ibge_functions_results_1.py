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
    # Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')       
    # -----------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------     
    # for i in range(0,10): 
    for i in range(len(Kmeans3_T)): 
        Qtdade = 0
        for j in range(len(Final_Fem_CSV)):
            # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
            if ((str(Final_Fem_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Fem_CSV.Idade_em_Anos[j] >30 & Final_Fem_CSV.Idade_em_Anos[j] <=39:
                Qtdade = Qtdade + 1
        Kmeans3_T.F30[i] = int(Qtdade)            
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')     
    # -----------------------------------------------------------------------------------    
    # ----------------------------------------------------------------------------------- 
    # for i in range(0,10): 
    for i in range(len(Kmeans3_T)): 
        Qtdade = 0
        for j in range(len(Final_Fem_CSV)):
            # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
            if ((str(Final_Fem_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Fem_CSV.Idade_em_Anos[j] >40 & Final_Fem_CSV.Idade_em_Anos[j] <=49:
                Qtdade = Qtdade + 1
        Kmeans3_T.F40[i] = int(Qtdade)            
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')    
    # -----------------------------------------------------------------------------------    
    # ----------------------------------------------------------------------------------- 
    # for i in range(0,10): 
    for i in range(len(Kmeans3_T)): 
        Qtdade = 0
        for j in range(len(Final_Fem_CSV)):
            # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
            if ((str(Final_Fem_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Fem_CSV.Idade_em_Anos[j] >50 & Final_Fem_CSV.Idade_em_Anos[j] <=59:
                Qtdade = Qtdade + 1
        Kmeans3_T.F50[i] = int(Qtdade)            
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')     
    # ----------------------------------------------------------------------------------- 
    # for i in range(0,10): 
    for i in range(len(Kmeans3_T)): 
        Qtdade = 0
        for j in range(len(Final_Fem_CSV)):
            # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
            if ((str(Final_Fem_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Fem_CSV.Idade_em_Anos[j] >=60:
                Qtdade = Qtdade + 1
        Kmeans3_T.F60[i] = int(Qtdade)            
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')     

    # Masculino ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # for i in range(0,10): 
    for i in range(len(Kmeans3_T)): 
        Qtdade = 0
        for j in range(len(Final_Masc_CSV)):
            # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
            if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i])))& Final_Masc_CSV.Idade_em_Anos[j] <=29:
                Qtdade = Qtdade + 1
            Kmeans3_T.M29[i] = int(Qtdade)    
            # if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >30 & Final_Masc_CSV.Idade_em_Anos[j] <=39:
            #     Qtdade = Qtdade + 1
            # Kmeans3_T.M30[i] = int(Qtdade) 
            # if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >40 & Final_Masc_CSV.Idade_em_Anos[j] <=49:
            #     Qtdade = Qtdade + 1
            # Kmeans3_T.M40[i] = int(Qtdade)         
            # if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >50 & Final_Masc_CSV.Idade_em_Anos[j] <=59:
            #     Qtdade = Qtdade + 1
            # Kmeans3_T.M50[i] = int(Qtdade)    
            # if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >=60:
            #     Qtdade = Qtdade + 1
            # Kmeans3_T.M60[i] = int(Qtdade) 
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')       
    # # # -----------------------------------------------------------------------------------
    # # -------------------------------------------------------------------------------------     
    # for i in range(0,10): 
    for i in range(len(Kmeans3_T)): 
        Qtdade = 0
        for j in range(len(Final_Masc_CSV)):
            # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
            if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >30 & Final_Masc_CSV.Idade_em_Anos[j] <=39:
                Qtdade = Qtdade + 1
        Kmeans3_T.M30[i] = int(Qtdade)            
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')     
    # -----------------------------------------------------------------------------------    
    # # ----------------------------------------------------------------------------------- 
    # for i in range(0,10): 
    for i in range(len(Kmeans3_T)): 
        Qtdade = 0
        for j in range(len(Final_Masc_CSV)):
            # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
            if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >40 & Final_Masc_CSV.Idade_em_Anos[j] <=49:
                Qtdade = Qtdade + 1
        Kmeans3_T.M40[i] = int(Qtdade)            
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')    
    # -----------------------------------------------------------------------------------    
    # ----------------------------------------------------------------------------------- 
    # for i in range(0,10): 
    for i in range(len(Kmeans3_T)): 
        Qtdade = 0
        for j in range(len(Final_Masc_CSV)):
            # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
            if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >50 & Final_Masc_CSV.Idade_em_Anos[j] <=59:
                Qtdade = Qtdade + 1
        Kmeans3_T.M50[i] = int(Qtdade)            
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')     
    # ----------------------------------------------------------------------------------- 
    # for i in range(0,10): 
    for i in range(len(Kmeans3_T)): 
        Qtdade = 0
        for j in range(len(Final_Masc_CSV)):
            # if (str(Final_Fem_CSV.Ocupação_Código[i])== '2341.0') & (str(Final_Fem_CSV.Curso_Superior_Graduação_Código[i]) == '142.0'):
            if ((str(Final_Masc_CSV.Ocupação_Código[j]))== (str(int(Kmeans3_T.Cbo[i])))) & (str(Final_Masc_CSV.Curso_Superior_Graduação_Código[j]) == str(int(Kmeans3_T.Curso[i]))) & Final_Masc_CSV.Idade_em_Anos[j] >=60:
                Qtdade = Qtdade + 1
        Kmeans3_T.M60[i] = int(Qtdade)            
    Kmeans3_T.to_csv(save_results_to + 'Kmeans3_T_IdadeCursoCBO.csv')    
    return   



def plot_gender_age_distribution():
    import matplotlib.pyplot as plt

    # Leitura do arquivo
    file_path = 'graficos/Kmeans3_T_IdadeCursoCBO.csv'
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

def split_csv_by_cluster():
    # Read the CSV file
    file_path = 'graficos/Kmeans3_T_IdadeCursoCBO.csv'
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
