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


def selecionados(cluster):
    if cluster == 0:
        # Seleciona os arquivos do cluster 0
        arquivos = glob.glob('/home/andre/Downloads/ibge/cluster_0/*.csv')
    if cluster == 1:
        # Seleciona os arquivos do cluster 1
        arquivos = glob.glob('/home/andre/Downloads/ibge/cluster_1/*.csv')
    if cluster == 2:
        # Seleciona os arquivos do cluster 2
        arquivos = glob.glob('/home/andre/Downloads/ibge/cluster_2/*.csv')    
    return