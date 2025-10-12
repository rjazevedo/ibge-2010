import pandas as pd

# # Lendo com zeros à esquerda preservados
# df = pd.read_csv("cbo2002_familia.csv", dtype=str)
# # df = pd.read_csv("cbo2002_familia_saida.csv", dtype=str)
# df1 = pd.read_csv("cbo2002_subgrupo.csv", dtype=str)
# # df1 = pd.read_csv("cbo2002_subgrupo_saida.csv", dtype=str)
# df2 = pd.read_csv("cbo2002_subgrupo_principal.csv", dtype=str)
# df2 = pd.read_csv("cbo2002_subgrupo_principal_saida.csv", dtype=str)
# df3 = pd.read_csv("CBO_CSV.csv", dtype=str)
# df4 = pd.read_csv("CBO_CSV_TabelaAuxiliar.csv", dtype=str)
# testes ...
df_brasil = pd.read_csv(
    "processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CBO_DiminuidoCBO3_Curso2.csv",
    dtype={"CBO-Domiciliar": str}
)


# Exibindo as primeiras linhas para verificação
# print(df.head(10))
# print("-----")
# print(df1.head(10))
# print("-----")
# print(df2.head(10))
# print("-----")
# print(df3.head(10))
# print("-----")
# print(df4.head(10))
# print("-----")

# # Salvando de volta mantendo zeros à esquerda
# df.to_csv("cbo2002_familia_saida.csv", index=False)
# df1.to_csv("cbo2002_subgrupo_saida.csv", index=False)
# df2.to_csv("cbo2002_subgrupo_principal_saida.csv", index=False)

# # Faz suas transformações...
# print("Transformações...")
# df3["Cod_CBO"] = df3["Cod_CBO"].str[:-1]
# print(df3.head(10))
# df3.to_csv("CBO_CSV_modificado.csv", index=False)
# print("-----")
# df4["Cod_CBO"] = df4["Cod_CBO"].str[:-1]
# print(df4.head(10))
# df4.to_csv("CBO_CSV_TabelaAuxiliar_modificado.csv", index=False)


# testes
print(
    df_brasil["CBO-Domiciliar"]
    .drop_duplicates()
    .sort_values()
    .loc[lambda x: x.str.startswith("0")]
    .to_string(index=False)
)