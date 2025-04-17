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
        