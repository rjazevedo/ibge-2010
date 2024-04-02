
pip install ibge-parser


# inclua todos os demais imports aqui
import pandas as pd
import argparse
import sys

import ibgeparser
import pandas as pd
from pandas import DataFrame
import numpy as np

# import da classe principal
from ibgeparser.microdados import Microdados
# import dos enums para facilitar as buscas
from ibgeparser.enums import Anos, Estados, Modalidades

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

if fase >= 0:
    # Leia os dados do IBGE
    ibge_functions.function_obterdados_especificacao_coluna(ano_ac, estados_ac, modalidades_ac)
    pass

# Fase 1: Filtrar somente os dados relevantes. Aqui significa que 
# você precisa filtrar todos os dados que possam ser utilizados no futuro.

if fase >= 1:
    pass

# Fase 2: Limpeza dos dados. Agora começa a processar algo mais complexo desde que seja definitivo



# Fase 10: Essa é a primeira fase que você faz no dia a dia. Aqui você começa a fazer a análise dos dados
if fase >= 10:
    pass



# Fase 99: Aqui você pode explorar coisas novas que não afetam os dados anteriores.
