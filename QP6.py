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
import ibge_functions_descriptive_analysis_1
import ibge_variable
import ibge_functions_preprocessing
import ibge_functions_results
import ibge_functions_results_1
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder


def transform_categoria_emprego():
    # Load the dataset
    file_path = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv'
    output_path = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados_CategoriaEmprego_Binario.csv'
    
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return
    
    data = pd.read_csv(file_path)
    
    # Ensure the column exists
    if 'Categoria_Emprego' not in data.columns:
        logging.error("Column 'Categoria_Emprego' not found in the dataset.")
        return
    
    # Transform the column
    data['Categoria_Emprego'] = data['Categoria_Emprego'].apply(
        lambda x: 0 if x in [1, 2, 3] else (1 if x in [4, 5, 6] else x)
    )
    
    # Save the transformed dataset
    data.to_csv(output_path, index=False)
    logging.info(f"Transformed dataset saved to {output_path}")
    print(f"Transformed dataset saved to {output_path}")

# def classify_employment_stability():
#     # Load the dataset
#     file_path = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv'
#     if not os.path.exists(file_path):
#         logging.error(f"File not found: {file_path}")
#         return None
    
#     data = pd.read_csv(file_path)
    
#     # Ensure necessary columns exist
#     required_columns = ['gênero', 'Nível_instrução', 'Curso_Superior_Graduação_Código', 'Ocupação_Código', 'Categoria_Emprego']
#     if not all(col in data.columns for col in required_columns):
#         logging.error("Missing required columns in the dataset.")
#         return None
    
#     # Preprocess the data
#     data = data.dropna(subset=required_columns)
#     label_encoders = {col: LabelEncoder() for col in ['gênero', 'Nível_instrução', 'Curso_Superior_Graduação_Código', 'Ocupação_Código']}
#     for col, encoder in label_encoders.items():
#         data[col] = encoder.fit_transform(data[col])
    
#     X = data[['gênero', 'Nível_instrução', 'Curso_Superior_Graduação_Código', 'Ocupação_Código']]
#     y = data['Categoria_Emprego']
    
#     # Train Random Forest with cross-validation
#     model = RandomForestClassifier(random_state=42)
#     scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    
#     accuracy = scores.mean()
#     logging.info(f"Cross-validated accuracy: {accuracy:.4f}")
#     print(f"Cross-validated accuracy: {accuracy:.4f}")
    
#     return accuracy

# ------------------------------------------------------------------------------------------------------------------------------------------------

# # Call the function
# classify_employment_stability()

# // filepath: /home/elisangela.silva/ibge-2010/QP6.py
# // ...existing code...
# def classify_employment_stability():
#     # Load the dataset
#     file_path = 'processados/CSVs_ArquivoFinalGraduados/Brasil_Graduados.csv'
#     if not os.path.exists(file_path):
#         logging.error(f"File not found: {file_path}")
#         return None, None, None, None
    
#     data = pd.read_csv(file_path)
    
#     # Ensure necessary columns exist
#     required_columns = ['gênero', 'Nível_instrução', 'Curso_Superior_Graduação_Código', 'Ocupação_Código', 'Categoria_Emprego']
#     if not all(col in data.columns for col in required_columns):
#         logging.error("Missing required columns in the dataset.")
#         return None, None, None, None
    
#     # Preprocess the data
#     data_original_features = data[['gênero', 'Nível_instrução', 'Curso_Superior_Graduação_Código', 'Ocupação_Código']].copy()
#     data = data.dropna(subset=required_columns)
    
#     # !!! IMPORTANTE: Assumindo que 'Categoria_Emprego' já foi mapeada para Formal/Informal (ex: 0 ou 1)
#     # Se não, você precisa adicionar essa etapa de mapeamento aqui antes de definir y.
#     # Exemplo: data['Categoria_Emprego'] = data['Categoria_Emprego'].map({'Formal': 1, 'Informal': 0})

#     label_encoders = {col: LabelEncoder() for col in ['gênero', 'Nível_instrução', 'Curso_Superior_Graduação_Código', 'Ocupação_Código']}
#     data_encoded_features = data_original_features.copy() # Trabalhar em uma cópia para codificação
#     for col, encoder in label_encoders.items():
#         # Ajustar e transformar apenas nas linhas não-NaN que vão para o modelo
#         data_encoded_features[col] = encoder.fit_transform(data[col])
    
#     X = data_encoded_features[['gênero', 'Nível_instrução', 'Curso_Superior_Graduação_Código', 'Ocupação_Código']]
#     y = data['Categoria_Emprego'] # Esta deve ser a coluna mapeada Formal/Informal
    
#     # Train Random Forest with cross-validation
#     cv_model = RandomForestClassifier(random_state=42)
#     scores = cross_val_score(cv_model, X, y, cv=5, scoring='accuracy')
    
#     accuracy = scores.mean()
#     logging.info(f"Cross-validated accuracy: {accuracy:.4f}")
#     print(f"Cross-validated accuracy: {accuracy:.4f}")
    
#     # Treinar o modelo final em todos os dados para análise de features e previsões
#     final_model = RandomForestClassifier(random_state=42)
#     final_model.fit(X, y)
    
#     # Obter a importância das features
#     feature_names = X.columns
#     importances = final_model.feature_importances_
#     feature_importance_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
#     feature_importance_df = feature_importance_df.sort_values(by='importance', ascending=False)
    
#     logging.info(f"Feature Importances:\n{feature_importance_df}")
#     print("\nFeature Importances:")
#     print(feature_importance_df)
    
#     return accuracy, final_model, feature_importance_df, label_encoders, data # Retornar 'data' para análise posterior

# # # Call the function
# # accuracy, trained_model, importances, encoders, data_processed = classify_employment_stability()

# -----------------------------------------------------------------------------------------------------------------------------------------------

# Supondo que você chamou a função e obteve 'data_processed':
# accuracy, trained_model, importances, encoders, data_processed = classify_employment_stability()

# if data_processed is not None:
#     # Certifique-se que 'Categoria_Emprego' está no formato que você espera (ex: 0 e 1)
#     # Se 'Curso_Superior_Graduação_Código' for numérico e você tiver um mapeamento para nomes, use-o para melhor legibilidade.
#
#     # Calcular a proporção de cada categoria de emprego por gênero e código do curso
#     # Assumindo que 'Categoria_Emprego' foi mapeada para 0 (Informal) e 1 (Formal)
#     patterns = data_processed.groupby(['gênero', 'Curso_Superior_Graduação_Código'])['Categoria_Emprego'].value_counts(normalize=True).mul(100).unstack(fill_value=0)
#
#     print("\n--- Padrões de Emprego (Formal/Informal %) por Gênero e Código do Curso ---")
#     print(patterns)
#
#     # Para uma análise mais detalhada por gênero:
#     patterns_gender = data_processed.groupby(['gênero'])['Categoria_Emprego'].value_counts(normalize=True).mul(100).unstack(fill_value=0)
#     print("\n--- Padrões de Emprego (Formal/Informal %) por Gênero ---")
#     print(patterns_gender)

#     # Para uma análise mais detalhada por área de formação (código do curso):
#     patterns_curso = data_processed.groupby(['Curso_Superior_Graduação_Código'])['Categoria_Emprego'].value_counts(normalize=True).mul(100).unstack(fill_value=0)
#     print("\n--- Padrões de Emprego (Formal/Informal %) por Código do Curso ---")
#     print(patterns_curso)
#
#     # Você pode querer usar os 'encoders' para mapear de volta os valores codificados de 'gênero'
#     # e 'Curso_Superior_Graduação_Código' para seus rótulos originais se você os agrupou após a codificação.
#     # No entanto, o 'data_processed' retornado acima deve ter as colunas originais antes da codificação das features X,
#     # mas com 'Categoria_Emprego' já como alvo numérico.
#     # Se 'gênero' em data_processed ainda for string (ex: 'Masculino', 'Feminino'), o groupby funcionará diretamente.
#     # Se estiver codificado, você pode precisar mapeá-lo de volta para os nomes para melhor interpretação das tabelas.

# --------------------------------------------------------------------------------------------------------------------------------
# import matplotlib.pyplot as plt
# import seaborn as sns

# if data_processed is not None and not patterns.empty:
#     # Exemplo para visualizar 'patterns' (Gênero e Curso)
#     # Isso pode ser complexo se houver muitos cursos, então talvez filtre ou agrupe os cursos.
#     # Vamos focar em visualizar patterns_gender como exemplo mais simples:
#     if 1 in patterns_gender.columns: # Se a coluna para 'Formal' (ex: 1) existir
#         patterns_gender_formal = patterns_gender[[1]].reset_index() # Pegar a porcentagem de Formal
#         patterns_gender_formal.columns = ['gênero', 'Formal (%)']
#
#         plt.figure(figsize=(8, 6))
#         sns.barplot(x='gênero', y='Formal (%)', data=patterns_gender_formal)
#         plt.title('Porcentagem de Emprego Formal por Gênero')
#         plt.ylabel('Formal (%)')
#         plt.xlabel('Gênero')
#         plt.show()
#     else:
#         print("Coluna para emprego formal (ex: 1) não encontrada em patterns_gender para plotagem.")
