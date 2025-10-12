import pandas as pd

# Lendo com zeros à esquerda preservados
df = pd.read_csv("cbo2002_familia.csv", dtype=str)

# Faz suas transformações...
print(df.head())

# Salvando de volta mantendo zeros à esquerda
df.to_csv("/home/essantos/Downloads/cbo2002_familia_saida.csv", index=False)