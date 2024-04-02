#python3 /home/essantos/Downloads/IBGE/Codigos/28_08/ibge_functions.py
import pandas as pd 
import numpy as np

#=====================================================================================================================================================================================================    
#=====================================================================================================================================================================================================    
# 14/08/2023
# Função 1: Descobrir informações básicas sobre cada cluster.
  # Quais CBOs?
  # Quantos CBOs?
  # Quantidade de CBOs repetidos em cada cluster ...
  # Quantos CBOs Diferentes? Ou seja, quantos CBOs diferentes em cada cluster?

def Cluster_Infos(cluster_index, y_Treino, CBOs_cluster, qtdade_cbos, CBOs_Repet, CBOs_Diff):
    cluster_index.index

    ## Quais ...
    for row in cluster_index.index:
        CBOs_cluster.append(y_Treino.loc[row,'Ocupação_Código'])

    ## Quantos ...
    qtdade_cbos = cluster_index.cluster.count()

    ## CBOs Repetidos
    CBOs_Repet  = pd.DataFrame(CBOs_cluster)
    CBOs_Repet  = CBOs_Repet.value_counts()

    #Quantos CBOs Diferentes? Ou seja, quantos CBOs diferentes em cada cluster?
    CBOs_Diff = CBOs_Repet.value_counts()
    CBOs_Diff = CBOs_Repet.count()

    return CBOs_cluster,qtdade_cbos,CBOs_Repet, CBOs_Diff
    #return CBOs_cluster, qtdade_cbos
#=====================================================================================================================================================================================================    
#=====================================================================================================================================================================================================    
# 14/08/2023
#Função  2: Descobrir as intersecções entre cada cluster
def Cluster_Interseccao(Interseccao, num_total_cluster):
    keys = list(cluster_name.keys())
    inc = 1
    inter = 0
    comparacoes = num_total_cluster - inc

    for name in cluster_name:
        #name = "cluster2"
        print("Numero do Cluster-------------------------------", name)
        #for chave in cluster_name:
        for i in range(comparacoes):
            print("cluster:", name + "  x  " + "cluster:", keys[i+inc])
            #print(Quais[cluster_name[nome]])
            #print(Quais[cluster_name[keys[i+1]]])
            Interseccao[inter][cluster_name[keys[i+inc]]] = np.intersect1d(Quais[cluster_name[name]],Quais[cluster_name[keys[i+inc]]])
            print(Interseccao[inter][cluster_name[keys[i+inc]]])
            #Interseccao2[cluster_name[keys[i+inc]]] = np.intersect1d(Quais[cluster_name[name]],Quais[cluster_name[keys[i+inc]]])
            #print(Interseccao2[cluster_name[keys[i+inc]]])
            print("\n")
        inc = inc + 1
        comparacoes = num_total_cluster - inc
        inter = inter + 1
    return Interseccao

#=====================================================================================================================================================================================================    
#=====================================================================================================================================================================================================    
# 28/08/2023
#Função 3: Limpar um arquivo do censo, deixando somemte as pessoas graduada
def Limpeza_Arquivo_Censo(name):
    X = pd.read_csv(name,usecols=["V6036", "V6400", "V6352", "V6354", "V6356", "V6461", "V6471", "V6462", "V6472","V6511","V6514"],sep=",")


    #print("shape:",X.shape)
    #print("columns",X.columns)
    dict = {"V6036":"Idade_em_Anos",
    "V6400":"Nível_instrução",
    "V6352":"Curso_Superior_Graduação_Código",
    "V6354":"Curso_Mestrado_Código",
    "V6356":"Curso_Doutorado_Código",
    "V6461":"Ocupação_Código",
    "V6471":"Atividade_Código",
    "V6462":"CBO-Domiciliar",
    "V6472":"CNAE-Domiciliar",
    "V6511": "Valor_rend_bruto_M",
    "V6514": "Qtdade_Salario"
    }
    X.rename(columns=dict,inplace=True)
    #print("")
    #print("shape Original:",X.shape)
    #print("columns",X.columns)


    # removendo que não tem graduação
    X.drop(X[(X['Nível_instrução'] <=2) | (X['Nível_instrução'] ==5)].index, inplace=True)
    #print("")
    #print("shape apoś remover quem não tem graduação:",X.shape)
    #print("columns",X.columns)
    #print(X.head(10))


    #removendo quem tem menos de 25 anos
    X.drop(X[(X['Idade_em_Anos'] <=24)].index, inplace=True)
    #print("")
    #print("shape apoś remover pessoas com menos de 25 anos:",X.shape)


    #verificando linhas falatantes
    #print("")
    #print("Linhas faltantes:==============================")
    #print(X.isnull().sum())


    #removendo quem não tem ocupação
    X = X.dropna(subset=['Ocupação_Código'])
    #print("")
    #print("shape apoś remover quem não tem ocupação:",X.shape)


    #removendo pessoas com ocupações mal-definidas
    X.drop(X[(X['Ocupação_Código'] <1)].index, inplace=True)
    #print("")
    #print("shape apoś remover pessoas com ocupações mal-definidas:",X.shape)


    #Listando os NANs que ainda restam
    #print("")
    #print("Listando os NANs que ainda restam:==============================")
    #print(X.isnull().sum())


    #Tratando Valores Faltantes - Substituindo todos os nulos(NAN) por zero
    #print("")
    #print("Tratando Valores Faltantes - Substituindo todos os nulos(NAN) por zero")
    X.fillna(0, inplace = True)
    #print(X.isnull().sum())


    #Removendo CBO-Domiciliar
    # drop the 'CBO-Domiciliar' column
    X = X.drop(columns=['CBO-Domiciliar'])
    #print("")
    #print("shape apoś remover pessoas a coluna CBO-Domiciliar:",X.shape)


    # Deixando somente os graduados ...
    #Delect rows based on multiple column value
    X.drop(X[(X['Curso_Superior_Graduação_Código'] ==0)].index, inplace=True) #Essa condição, deixa o dataset somente com as pessoas graduadas ...
    #print("")
    #print("shape apoś remover todas as pessoas nã-graduadas:",X.shape)


    #X.to_csv('/home/essantos/Downloads/IBGE/Codigos/28_08/Amostra_Pessoas_32_ES_QtdadeSal_SoGraduados.csv')
    name_path = name.split(".csv")
    name_path = name_path[0] + "_clean_QtdadeSal_SoGraduados.csv"


    #print(name_path)
    X.to_csv(name_path)
    #X.to_csv('/home/essantos/Downloads/IBGE/Codigos/Soltos/33_RJ_QtdadeSal_SoGraduados.csv')


    #return name_path
    return

#========================================================================================================================================================================
#========================================================================================================================================================================
# 23/08/2023
#Função 3.1:  Limpar um arquivo do censo, deixando graduados e não-graduados para fazer a PivotTablet ...
def Limpeza_Arquivo_Censo_Graduados_NaoGraduados(name):
    X = pd.read_csv(name,usecols=["V6036", "V6400", "V6352", "V6354", "V6356", "V6461",  "V6471", "V6462", "V6472","V6511","V6514"],sep=",")

    #print("shape:",X.shape)
    #print("columns",X.columns)
    dict = {"V6036":"Idade_em_Anos",
        "V6400":"Nível_instrução",
        "V6352":"Curso_Superior_Graduação_Código",
        "V6354":"Curso_Mestrado_Código",
        "V6356":"Curso_Doutorado_Código",
        "V6461":"Ocupação_Código",
        "V6471":"Atividade_Código",
        "V6462":"CBO-Domiciliar",
        "V6472":"CNAE-Domiciliar",
        "V6511": "Valor_rend_bruto_M",
        "V6514": "Qtdade_Salario"
        }
    X.rename(columns=dict,inplace=True)
    #print("")
    #print("shape Original:",X.shape)
    #print("columns",X.columns)

    # removendo que não tem graduação   ## alterado 23/09/2023 #=============================
    #X.drop(X[(X['Nível_instrução'] <=2) | (X['Nível_instrução'] ==5)].index, inplace=True) ## alterado 23/09/2023 #=============================
    #print("")
    #print("shape apoś remover quem não tem graduação:",X.shape)
    #print("columns",X.columns)
    #print(X.head(10))

    #removendo quem tem menos de 25 anos
    X.drop(X[(X['Idade_em_Anos'] <=24)].index, inplace=True)
    #print("")
    #print("shape apoś remover pessoas com menos de 25 anos:",X.shape)

    #verificando linhas falatantes
    #print("")
    print("Linhas faltantes:==============================")
    print(X.isnull().sum())

    #removendo quem não tem ocupação
    X = X.dropna(subset=['Ocupação_Código'])
    #print("")
    #print("shape apoś remover quem não tem ocupação:",X.shape)

    #removendo pessoas com ocupações mal-definidas
    X.drop(X[(X['Ocupação_Código'] <1)].index, inplace=True)
    #print("")
    #print("shape apoś remover pessoas com ocupações mal-definidas:",X.shape)

    #Listando os NANs que ainda restam
    #print("")
    print("Listando os NANs que ainda restam:==============================")
    print(X.isnull().sum())

    #Tratando Valores Faltantes - Substituindo todos os nulos(NAN) por zero
    #print("")
    #print("Tratando Valores Faltantes - Substituindo todos os nulos(NAN) por zero")
    X.fillna(0, inplace = True)
    #print(X.isnull().sum())

    #Removendo CBO-Domiciliar
    # drop the 'CBO-Domiciliar' column
    X = X.drop(columns=['CBO-Domiciliar'])
    #print("")
    #print("shape apoś remover pessoas a coluna CBO-Domiciliar:",X.shape)

    # Deixando somente os graduados ... ## alterado 23/09/2023 #=============================
    #Delect rows based on multiple column value
    #X.drop(X[(X['Curso_Superior_Graduação_Código'] ==0)].index, inplace=True) #Essa condição, deixa o dataset somente com as pessoas graduadas ... ## alterado 23/09/2023 #=============================
    #print("")
    #print("shape apoś remover todas as pessoas não-graduadas:",X.shape)

    #X.to_csv('/home/essantos/Downloads/IBGE/Codigos/28_08/Amostra_Pessoas_32_ES_QtdadeSal_SoGraduados.csv')
    name_path = name.split(".csv")
    name_path = name_path[0] + "_clean_QtdadeSal_Graduados_NaoGraduados.csv"

    #print(name_path)
    X.to_csv(name_path)
    #X.to_csv('/home/essantos/Downloads/IBGE/Codigos/Soltos/33_RJ_QtdadeSal_SoGraduados.csv')

    #return name_path
    return

#========================================================================================================================================================================
#========================================================================================================================================================================
# 23/08/2023
#Função 3.1.1:  Limpar um arquivo do censo, deixando graduados e não-graduados para fazer a PivotTablet ...
def Limpeza_Arquivo_Censo_Graduados_NaoGraduados_1(name):
    X = pd.read_csv(name,usecols=["V6036", "V6400", "V6352", "V6354", "V6356", "V6461",  "V6471", "V6462", "V6472","V6511","V6514"],sep=",")

    #print("shape:",X.shape)
    #print("columns",X.columns)
    dict = {"V6036":"Idade_em_Anos",
        "V6400":"Nível_instrução",
        "V6352":"Curso_Superior_Graduação_Código",
        "V6354":"Curso_Mestrado_Código",
        "V6356":"Curso_Doutorado_Código",
        "V6461":"Ocupação_Código",
        "V6471":"Atividade_Código",
        "V6462":"CBO-Domiciliar",
        "V6472":"CNAE-Domiciliar",
        "V6511": "Valor_rend_bruto_M",
        "V6514": "Qtdade_Salario"
        }
    X.rename(columns=dict,inplace=True)
    #print("")
    #print("shape Original:",X.shape)
    #print("columns",X.columns)

    # removendo que não tem graduação   ## alterado 23/09/2023 #=============================
    #X.drop(X[(X['Nível_instrução'] <=2) | (X['Nível_instrução'] ==5)].index, inplace=True) ## alterado 23/09/2023 #=============================
    #print("")
    #print("shape apoś remover quem não tem graduação:",X.shape)
    #print("columns",X.columns)
    #print(X.head(10))

    #removendo quem tem menos de 25 anos
    X.drop(X[(X['Idade_em_Anos'] <=24)].index, inplace=True)
    #print("")
    #print("shape apoś remover pessoas com menos de 25 anos:",X.shape)

    #verificando linhas falatantes
    #print("")
    print("Linhas faltantes:==============================")
    print(X.isnull().sum())

    #removendo quem não tem ocupação
    X = X.dropna(subset=['Ocupação_Código'])
    #print("")
    #print("shape apoś remover quem não tem ocupação:",X.shape)

    #removendo pessoas com ocupações mal-definidas
    X.drop(X[(X['Ocupação_Código'] <1)].index, inplace=True)
    #print("")
    #print("shape apoś remover pessoas com ocupações mal-definidas:",X.shape)

    #Listando os NANs que ainda restam
    #print("")
    print("Listando os NANs que ainda restam:==============================")
    print(X.isnull().sum())

    #Tratando Valores Faltantes - Substituindo todos os nulos(NAN) por zero
    #print("")
    #print("Tratando Valores Faltantes - Substituindo todos os nulos(NAN) por zero")
    X.fillna(0, inplace = True)
    #print(X.isnull().sum())

    #Removendo CBO-Domiciliar
    # drop the 'CBO-Domiciliar' column
    X = X.drop(columns=['CBO-Domiciliar'])
    #print("")
    #print("shape apoś remover pessoas a coluna CBO-Domiciliar:",X.shape)

    # Deixando somente os graduados ... ## alterado 23/09/2023 #=============================
    #Delect rows based on multiple column value
    #X.drop(X[(X['Curso_Superior_Graduação_Código'] ==0)].index, inplace=True) #Essa condição, deixa o dataset somente com as pessoas graduadas ... ## alterado 23/09/2023 #=============================
    #print("")
    #print("shape apoś remover todas as pessoas não-graduadas:",X.shape)

    # Novo Filtro
    # removendo que tem graduação, mas o curso superior é igual  a Zero
    X.drop(X[(X['Nível_instrução'] ==4) & (X['Curso_Superior_Graduação_Código'] ==0)].index, inplace=True) ## alterado 23/09/2023 #=============================
    #print("")
    #print("shape apoś remover quem não tem graduação:",X.shape)
    #print("columns",X.columns)
    #print(X.head(10))

    #X.to_csv('/home/essantos/Downloads/IBGE/Codigos/28_08/Amostra_Pessoas_32_ES_QtdadeSal_SoGraduados.csv')
    name_path = name.split(".csv")
    name_path = name_path[0] + "_clean_QtdadeSal_Graduados_NaoGraduados.csv"

    #print(name_path)
    X.to_csv(name_path)
    #X.to_csv('/home/essantos/Downloads/IBGE/Codigos/Soltos/33_RJ_QtdadeSal_SoGraduados.csv')

    #return name_path
    return


#=====================================================================================================================================================================================================    
#=====================================================================================================================================================================================================    
# 28/08/2023
#Função 3.2:  Limpar um arquivo do censo, deixando somemte as pessoas graduada 
def Limpeza_Arquivo_Censo_Graduados(name):
    #X = pd.read_csv(name,usecols=["V6036", "V6400", "V6352", "V6354", "V6356", "V6461",  "V6471", "V6462", "V6472","V6511","V6514"],sep=",")
    X = pd.read_csv(name,usecols=["Idade_em_Anos", "Nível_instrução", "Curso_Superior_Graduação_Código", "Curso_Mestrado_Código", "Curso_Doutorado_Código", "Ocupação_Código",  
                                   "Atividade_Código", "CNAE-Domiciliar","Valor_rend_bruto_M","Qtdade_Salario"],sep=",")
    #                              "Atividade_Código", "CBO-Domiciliar", "CNAE-Domiciliar","Valor_rend_bruto_M","Qtdade_Salario"],sep=",")

    #print("shape:",X.shape)
    #print("columns",X.columns)
    #dict = {"V6036":"Idade_em_Anos",
    #    "V6400":"Nível_instrução",
    #    "V6352":"Curso_Superior_Graduação_Código",
    #    "V6354":"Curso_Mestrado_Código",
    #    "V6356":"Curso_Doutorado_Código",
    #    "V6461":"Ocupação_Código",
    #    "V6471":"Atividade_Código",
    #    "V6462":"CBO-Domiciliar",
    #    "V6472":"CNAE-Domiciliar",
    #    "V6511": "Valor_rend_bruto_M",
    #    "V6514": "Qtdade_Salario"
    #    }
    #X.rename(columns=dict,inplace=True)
    #print("")
    #print("shape Original:",X.shape)
    #print("columns",X.columns)

    # removendo que não tem graduação
    #X.drop(X[(X['Nível_instrução'] <=2) | (X['Nível_instrução'] ==5)].index, inplace=True)
    #print("")
    #print("shape apoś remover quem não tem graduação:",X.shape)
    #print("columns",X.columns)
    #print(X.head(10))

    #removendo quem tem menos de 25 anos
    #X.drop(X[(X['Idade_em_Anos'] <=24)].index, inplace=True)
    #print("")
    #print("shape apoś remover pessoas com menos de 25 anos:",X.shape)

    #verificando linhas falatantes
    #print("")
    #print("Linhas faltantes:==============================")
    #print(X.isnull().sum())

    #removendo quem não tem ocupação
    #X = X.dropna(subset=['Ocupação_Código'])
    #print("")
    #print("shape apoś remover quem não tem ocupação:",X.shape)

    #removendo pessoas com ocupações mal-definidas
    #X.drop(X[(X['Ocupação_Código'] <1)].index, inplace=True)
    #print("")
    #print("shape apoś remover pessoas com ocupações mal-definidas:",X.shape)

    #Listando os NANs que ainda restam
    #print("")
    #print("Listando os NANs que ainda restam:==============================")
    #print(X.isnull().sum())

    #Tratando Valores Faltantes - Substituindo todos os nulos(NAN) por zero
    #print("")
    #print("Tratando Valores Faltantes - Substituindo todos os nulos(NAN) por zero")
    #X.fillna(0, inplace = True)
    #print(X.isnull().sum())

    #Removendo CBO-Domiciliar
    # drop the 'CBO-Domiciliar' column
    #X = X.drop(columns=['CBO-Domiciliar'])
    #print("")
    #print("shape apoś remover pessoas a coluna CBO-Domiciliar:",X.shape)

    # Deixando somente os graduados ...
    #Delect rows based on multiple column value
    X.drop(X[(X['Curso_Superior_Graduação_Código'] ==0)].index, inplace=True) #Essa condição, deixa o dataset somente com as pessoas graduadas ...
    #print("")
    #print("shape apoś remover todas as pessoas não-graduadas:",X.shape)

    #X.to_csv('/home/essantos/Downloads/IBGE/Codigos/28_08/Amostra_Pessoas_32_ES_QtdadeSal_SoGraduados.csv')
    name_path = name.split(".csv")
    name_path = name_path[0] + "_clean_QtdadeSal_SoGraduados.csv"

    #print(name_path)
    X.to_csv(name_path)
    #X.to_csv('/home/essantos/Downloads/IBGE/Codigos/Soltos/33_RJ_QtdadeSal_SoGraduados.csv')

    #return name_path
    return

#=====================================================================================================================================================================================================    
#=====================================================================================================================================================================================================    
#28/08/2023
# Função 4: Criar uma PivotTablet para o ensino superior, usando o arquivo do Censo 
def Pivot_Table_Censo(name):
       
    #X= pd.read_csv(name,usecols=["V6400", "V6461"], sep=",")   
    X= pd.read_csv(name,usecols=["Nível_instrução", "Ocupação_Código"], sep=",")   


    #dict = {"V6400":"Nível_instrução", "V6461":"Ocupação_Código",}
    #X.rename(columns=dict,inplace=True)
    #X.shape
    #X.columns

    # Método que verifica, e soma os valores nulos em todo dataset---------------------------------------------------------------------------------------------------------------
    X.isnull().sum()


    #Remover todas as linhas que tem CBO = Nan ---------------------------------------------------------------------------------------------------------------------------------
    #Dropping Rows or Columns for Specific subsets
    X = X.dropna(subset=['Ocupação_Código'])
    #X.shape

    #Gerando a Pivot table
    X['Ensino Superior']=1
    X_Pivot=pd.pivot_table(X, values=['Ensino Superior'], index=['Ocupação_Código'],columns=['Nível_instrução'],aggfunc='count',fill_value=0) 
    #X_CBO_Intrucao + X_CBO_Intrucao
    #print(X_Pivot)

    #X_Pivot.to_csv('/home/essantos/Downloads/IBGE/Codigos/28_08/PivotTable/SP1_Clean_PivoTable.csv')
    name_path = name.split(".csv")
    name_path = name_path[0] + "_PivotTablet.csv"
    X_Pivot.to_csv(name_path)
    
    return  X_Pivot
     

#=====================================================================================================================================================================================================    
#=====================================================================================================================================================================================================    
# ../../..
# Função 5: ...
#sum_of_pivot_tables -->>> Passar a função para cá
#https://drive.google.com/file/d/15Wa5j5pb0aPpT2u9SG5blolFITUwDHzg/view?usp=sharing
# Passar os names como uma lista de names? Depois fazer um for do tamanho da lista? # Isso pra soma de PivotTable 
# e para a Table Final? daria pra passar uma lista de names também?

#=====================================================================================================================================================================================================    
#=====================================================================================================================================================================================================    
# ../../..
# Função 6: ...
# Plot_Cbos_PivotTableFinal -->> criar função para fazer isso
# https://drive.google.com/file/d/1aaVbecjGwRlbQPsonFDET8EOhKMih-BW/view?usp=sharing

#=====================================================================================================================================================================================================    
#=====================================================================================================================================================================================================    
#01/09/2023
#Função 7: Achar CBOs por Curso 
def CBOs_Curso(csv_estado,csv_CBO,curso_num,titulo10,titulo3):
    #Leitura de Arquivos CSVs ...
    X = pd.read_csv(csv_estado)
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    #CURSOS = pd.read_csv(csv_CURSOS, dtype ='str')
    # drop the 'Unnamed:0' column
    CBO = CBO.drop(columns=['Unnamed: 0'])
    #CURSOS = CURSOS.drop(columns=['Unnamed: 0'])

    #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
    X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']]
    X_CURSO_CBO.shape

    #...
    #CBOs por curso
    #Indice ===========================================================================================================
    #print (X_CURSO_CBO.index[X_CURSO_CBO['Curso_Superior_Graduação_Código'] == 380].tolist())
    dir = X_CURSO_CBO.index[X_CURSO_CBO['Curso_Superior_Graduação_Código'] == curso_num].tolist()
    #dir
    # ...
    Curso_dir = []
    Cbo_dir = []
    for i in range(len(dir)):
        #print(direito[i])
        curso = X_CURSO_CBO._get_value(dir[i],'Curso_Superior_Graduação_Código')
        cbo = X_CURSO_CBO._get_value(dir[i],'Ocupação_Código')
        #print("Curso:",curso,"CBO:",str(int(cbo)))
        Curso_dir.append(curso)
        Cbo_dir.append(cbo)
        #...
    resultados_dir=[]
    for i in range(len(Curso_dir)):
      tupla=(Curso_dir[i],Cbo_dir[i])
      resultados_dir.append(tupla)
    #...
    Curso_Cbo_dir = pd.DataFrame(resultados_dir)
    #Curso_Cbo_dir.shape
    #...
    #Curso_Cbo_dir.columns
    dict = {0:"Curso",
    1:"Cbo",
    }
    Curso_Cbo_dir.rename(columns=dict,inplace=True)
    #type(Curso_Cbo_dir)
    #CBOs Unicos ============================================================
    Curso_Cbo_dir_unique = np.unique(Curso_Cbo_dir.Cbo)
    #Curso_Cbo_dir_unique
    #len(Curso_Cbo_dir_unique)
    #Plot====================================================================
    Cbo_Unique = Curso_Cbo_dir['Cbo'].astype(int).tolist()
    Cbo_Unique = np.unique(Cbo_Unique)
    Cbo_Unique
    #...
    Curso_Cbo_dir['Cbo'].value_counts().sort_index()
    #Curso_Cbo_dir['Cbo'].value_counts().sort_index().tolist()
    #...
    from numpy.ma.core import sort
    A = Curso_Cbo_dir['Cbo'].value_counts().sort_index()
    #...
    #Curso_Cbo_dir.loc[1:3, ['Cbo']]
    A = pd.DataFrame(A)
    #print(A.shape)
    #A
    A_cbo = A.sort_values("Cbo",ascending=False)
    A_cbo_10 = A_cbo.head(10)
    #passando o CBO para string, para poder plotar o nome
    #str(int(A_cbo_10.index[0]))
    #...
    #Coletando o nome do CBOs ...
    NomeCbo = []
    for i in range(len(A_cbo_10)):
        cbo=str(int(A_cbo_10.index[i]))
        for indexx, row in CBO.iterrows():
            if (row['Cod_CBO'] == cbo):
                NomeCbo.append(row['Nome_CBO'])
                #print(row['Cod_CBO'],":",row['Nome_CBO'])
    #import pandas as pd
    #list_name = ['item_1', 'item_2', 'item_3', ...]
    NomeCbo = pd.DataFrame(NomeCbo, columns=['Nome_CBO'])
    #print(NomeCbo.shape)
    #print(NomeCbo.columns)
    #NomeCbo.Nome_CBO[0]
    #...
    A_cbo_10["Nome"] = 1
    #...
    import warnings
    for i in range(len(A_cbo_10)):
        A_cbo_10['Nome'][i] = NomeCbo.Nome_CBO[i]
    #A_cbo_10
    A_cbo_10.reset_index(inplace=True)
    A_cbo_10 = A_cbo_10.rename(columns = {'index':'Cod_CBO'})
    #A_cbo_10
    #...
    A_cbo_10['Cod_CBO'] = A_cbo_10['Cod_CBO'].astype("float").astype('str')
    A_cbo_10['CBO_Nome'] = A_cbo_10['Cod_CBO'].str.cat(A_cbo_10['Nome'], sep =" ")
    #print(A_cbo_10)
    #
    tresprimeiros = []
    for i in range(3):
        tresprimeiros.append(int(float(A_cbo_10.Cod_CBO[i])))
    #...
    #Deletar coluna
    del A_cbo_10["Cod_CBO"]
    del A_cbo_10["Nome"]
    #A_cbo_10
    #...
    tresnomes = []
    for i in range(3):
        tresnomes.append(A_cbo_10.CBO_Nome[i])
    #...
    A_cbo_10 = A_cbo_10.set_index('CBO_Nome')
    #...
    #Plotando ...
    #A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
    A_cbo_10_sort = A_cbo_10.sort_values("Cbo",ascending=True)
    #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
    A_cbo_10_sort.plot(kind='barh',title=titulo10)
    plt.xlabel("")
    plt.show()
    #...
    #A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
    A_cbo_10_sort = A_cbo_10.iloc[0:3].sort_values("Cbo",ascending=True)
    #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
    A_cbo_10_sort.plot(kind='barh',title=titulo3)
    plt.xlabel("")
    plt.show()

    return tresprimeiros,tresnomes
    #return A_cbo_10.iloc[0:3].sort_values("Cbo",ascending=False)
#=====================================================================================================================================================================================================    
#=====================================================================================================================================================================================================    
#01/09/2023
#Função 8 -
#Cursos por CBO
#def Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo10,titulo3):#===comentando essa parte do grafico dos 10 maiores cursos
def Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo3):
    #Leitura de Arquivos CSVs ...
    X = pd.read_csv(csv_estado)
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    CURSOS = pd.read_csv(csv_CURSOS, dtype ='str')
    # drop the 'Unnamed:0' column
    CBO = CBO.drop(columns=['Unnamed: 0'])
    CURSOS = CURSOS.drop(columns=['Unnamed: 0'])

    #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
    X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']]
    X_CURSO_CBO.shape

    #Cursos por CBO
    #Indice =================================================================================================
    dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['Ocupação_Código'] == cbo_num].tolist()
    # ...
    Curso_dir_curso_cbos = []
    Cbo_dir_curso_cbos = []
    for i in range(len(dir_curso_cbos)):
        #print(direito[i])
        curso = X_CURSO_CBO._get_value(dir_curso_cbos[i],'Curso_Superior_Graduação_Código')
        cbo = X_CURSO_CBO._get_value(dir_curso_cbos[i],'Ocupação_Código')
        #print("Curso:",curso,"CBO:",str(int(cbo)))
        Curso_dir_curso_cbos.append(curso)
        Cbo_dir_curso_cbos.append(cbo)
    #..
    resultados_dir_curso_cbos=[]
    for i in range(len(Curso_dir_curso_cbos)):
      tupla=(Curso_dir_curso_cbos[i],Cbo_dir_curso_cbos[i])
      resultados_dir_curso_cbos.append(tupla)
    #...
    Curso_Cbo_dir_curso_cbos = pd.DataFrame(resultados_dir_curso_cbos)
    #Curso_Cbo_dir_curso_cbos.shape
    dict = {0:"Curso_Repet",
        1:"Cbo_Repet",
        }
    Curso_Cbo_dir_curso_cbos.rename(columns=dict,inplace=True)
    #Cursos Únicos por CBO ====================================================================================
    Curso_Cbo_dir_curso_cbos_unique = np.unique(Curso_Cbo_dir_curso_cbos.Curso_Repet)
    #Curso_Cbo_dir_curso_cbos_unique
    #len(Curso_Cbo_dir_curso_cbos_unique)
    #Plot======================================================================================================
    Curso_Unique = Curso_Cbo_dir_curso_cbos['Curso_Repet'].astype(int).tolist()
    #Curso_Unique = np.unique(Curso_Unique)
    #Curso_Unique
    #...
    Curso_Cbo_dir_curso_cbos['Curso_Repet'].value_counts().sort_index()
    #Curso_Cbo_dir['Cbo'].value_counts().sort_index().tolist()
    #Curso_Cbo_dir_curso_cbos.sort_values("Curso",ascending=True)
    #...
    from numpy.ma.core import sort
    A_dir_curso_cbos = Curso_Cbo_dir_curso_cbos['Curso_Repet'].value_counts().sort_index()
    #...
    #Curso_Cbo_dir.loc[1:3, ['Cbo']]
    A_dir_curso_cbos_sort = pd.DataFrame(A_dir_curso_cbos)
    #print(A_dir_curso_cbos_sort.shape)
    #A_dir_curso_cbos_sort
    #...
    A_Curso = A_dir_curso_cbos_sort.sort_values("Curso_Repet",ascending=False)
    #...
    A_Curso_11 = A_Curso.head(11)
    #A_Curso_11
    #...
    #passando o CBO para string, para poder plotar o nome
    #str(int(A_Curso_11.index[0]))
    #...
    #Coletando o nome dos Cursos ...
    NomeCurso = []
    for i in range(len(A_Curso_11)):
        curso=str(float(A_Curso_11.index[i]))
        for indexx, row in CURSOS.iterrows():
            if (row['Cod_Curso'] == curso):
            #if(row['Cod_Curso'] == A_Curso_10.index[i]):
                NomeCurso.append(row['Nome_Curso'])
                #print(row['Cod_Curso'],":",row['Nome_Curso'])
    #...
    #import pandas as pd
    #list_name = ['item_1', 'item_2', 'item_3', ...]
    NomeCurso = pd.DataFrame(NomeCurso, columns=['Nome_Curso'])
    #print(NomeCurso.shape)
    #print(NomeCurso.columns)
    #NomeCurso
    # ...
    #NomeCurso=NomeCurso.drop(3)
    #print(type(CURSOS.Cod_Curso[0]))
    #print(type(A_Curso_11.index[0]))
    # ...
    A_Curso_11["Nome"] = 1
    import warnings
    for i in range(len(A_Curso_11)):
        A_Curso_11['Nome'][i] = NomeCurso.Nome_Curso[i]
        #if (i>=3):
        #    A_Curso_11['Nome'][i] = NomeCurso.Nome_Curso[i+1]
        #else:
        #    A_Curso_11['Nome'][i] = NomeCurso.Nome_Curso[i]
    #A_Curso_11
    #A_Curso_11.columns
    #...
    A_Curso_11.reset_index(inplace=True)
    A_Curso_11 = A_Curso_11.rename(columns = {'index':'Curso'})
    #A_Curso_11
    A_Curso_11['Curso'] = A_Curso_11['Curso'].astype("float").astype('str')
    #type(A_Curso_11.Curso )
    A_Curso_11['Curso_Nome'] = A_Curso_11['Curso'].str.cat(A_Curso_11['Nome'], sep =" ")
    #A_Curso_11
    #...
    tresprimeiros = []
    for i in range(3):
        tresprimeiros.append(int(float(A_Curso_11.Curso[i])))
    #...
    #Deletar coluna
    del A_Curso_11["Curso"]
    del A_Curso_11["Nome"]
    #A_Curso_11
    A_Curso_11 = A_Curso_11.set_index('Curso_Nome')
    #A_Curso_11
    ## ...  Plotando o gráfico ... comentando essa parte do grafico dos 10 maiores cursos ======================================================
    ##A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
    #A_Curso_11_sort = A_Curso_11.sort_values("Curso_Repet",ascending=True)
    ##A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
    #A_Curso_11_sort.plot(kind='barh',title=titulo10)
    #plt.xlabel("")
    #plt.show()
    #...
    #A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
    A_Curso_11_sort = A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=True)
    #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
    #A_Curso_11_sort.plot(kind='barh',title="CBO 2611: Advogados e Juristas -  Os 3 maiores Cursos")
    A_Curso_11_sort.plot(kind='barh',title=titulo3)
    plt.xlabel("")
    plt.show()
    #return A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=False)
    return tresprimeiros

#=====================================================================================================================================================================================================    
#=====================================================================================================================================================================================================    
#03/09/2023
#Função 8.1: Achar cursos por CBO - 03/09/2023 - Versão Melhorada
#Cursos por CBO
#def Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo10,titulo3):#===comentando essa parte do grafico dos 10 maiores cursos
def Cursos_CBO_10(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo3):
    #Leitura de Arquivos CSVs ...
    X = pd.read_csv(csv_estado)
    CBO = pd.read_csv(csv_CBO, dtype ='str')
    CURSOS = pd.read_csv(csv_CURSOS, dtype ='str')
    # drop the 'Unnamed:0' column
    CBO = CBO.drop(columns=['Unnamed: 0'])
    CURSOS = CURSOS.drop(columns=['Unnamed: 0'])

    #Cbos -> Cursos ... criar um novo dataframe somente com cursos e cbos para facilitar
    X_CURSO_CBO = X[['Curso_Superior_Graduação_Código','Ocupação_Código']]
    X_CURSO_CBO.shape

    #Cursos por CBO
    #Indice =================================================================================================
    dir_curso_cbos = X_CURSO_CBO.index[X_CURSO_CBO['Ocupação_Código'] == cbo_num].tolist()
    # ...
    Curso_dir_curso_cbos = []
    Cbo_dir_curso_cbos = []
    for i in range(len(dir_curso_cbos)):
        #print(direito[i])
        curso = X_CURSO_CBO._get_value(dir_curso_cbos[i],'Curso_Superior_Graduação_Código')
        cbo = X_CURSO_CBO._get_value(dir_curso_cbos[i],'Ocupação_Código')
        #print("Curso:",curso,"CBO:",str(int(cbo)))
        Curso_dir_curso_cbos.append(curso)
        Cbo_dir_curso_cbos.append(cbo)
    #..
    resultados_dir_curso_cbos=[]
    for i in range(len(Curso_dir_curso_cbos)):
      tupla=(Curso_dir_curso_cbos[i],Cbo_dir_curso_cbos[i])
      resultados_dir_curso_cbos.append(tupla)
    #...
    Curso_Cbo_dir_curso_cbos = pd.DataFrame(resultados_dir_curso_cbos)
    #Curso_Cbo_dir_curso_cbos.shape
    dict = {0:"Curso_Repet",
        1:"Cbo_Repet",
        }
    Curso_Cbo_dir_curso_cbos.rename(columns=dict,inplace=True)
    #Cursos Únicos por CBO ====================================================================================
    Curso_Cbo_dir_curso_cbos_unique = np.unique(Curso_Cbo_dir_curso_cbos.Curso_Repet)
    #Curso_Cbo_dir_curso_cbos_unique
    #len(Curso_Cbo_dir_curso_cbos_unique)
    #Plot======================================================================================================
    Curso_Unique = Curso_Cbo_dir_curso_cbos['Curso_Repet'].astype(int).tolist()
    #Curso_Unique = np.unique(Curso_Unique)
    #Curso_Unique
    #...
    Curso_Cbo_dir_curso_cbos['Curso_Repet'].value_counts().sort_index()
    #Curso_Cbo_dir['Cbo'].value_counts().sort_index().tolist()
    #Curso_Cbo_dir_curso_cbos.sort_values("Curso",ascending=True)
    #...
    from numpy.ma.core import sort
    A_dir_curso_cbos = Curso_Cbo_dir_curso_cbos['Curso_Repet'].value_counts().sort_index()
    #...
    #Curso_Cbo_dir.loc[1:3, ['Cbo']]
    A_dir_curso_cbos_sort = pd.DataFrame(A_dir_curso_cbos)
    #print(A_dir_curso_cbos_sort.shape)
    #A_dir_curso_cbos_sort
    #...
    A_Curso = A_dir_curso_cbos_sort.sort_values("Curso_Repet",ascending=False)
    #...
    A_Curso_11 = A_Curso.head(10)
    print(A_Curso_11) # Apagando daqui pra baixo, da pra ver o erro ...================================================================================
     #...
    #passando o CBO para string, para poder plotar o nome
    #str(int(A_Curso_11.index[0]))
    #...
    #Coletando o nome dos Cursos ...
    NomeCurso = []
    for i in range(len(A_Curso_11)):
        curso=str(float(A_Curso_11.index[i]))
        for indexx, row in CURSOS.iterrows():
            if (row['Cod_Curso'] == curso):
            #if(row['Cod_Curso'] == A_Curso_10.index[i]):
                NomeCurso.append(row['Nome_Curso'])
                #print(row['Cod_Curso'],":",row['Nome_Curso'])
    #...
    #import pandas as pd
    #list_name = ['item_1', 'item_2', 'item_3', ...]
    NomeCurso = pd.DataFrame(NomeCurso, columns=['Nome_Curso'])
    #print(NomeCurso.shape)
    #print(NomeCurso.columns)
    #NomeCurso
    # ...
    #NomeCurso=NomeCurso.drop(3)
    #print(type(CURSOS.Cod_Curso[0]))
    #print(type(A_Curso_11.index[0]))
    # ...
    A_Curso_11["Nome"] = 1
    import warnings
    for i in range(len(A_Curso_11)):
        A_Curso_11['Nome'][i] = NomeCurso.Nome_Curso[i]
        #if (i>=3):
        #    A_Curso_11['Nome'][i] = NomeCurso.Nome_Curso[i+1]
        #else:
        #    A_Curso_11['Nome'][i] = NomeCurso.Nome_Curso[i]
    #A_Curso_11
    #A_Curso_11.columns
    #...
    A_Curso_11.reset_index(inplace=True)
    A_Curso_11 = A_Curso_11.rename(columns = {'index':'Curso'})
    #A_Curso_11
    A_Curso_11['Curso'] = A_Curso_11['Curso'].astype("float").astype('str')
    #type(A_Curso_11.Curso )
    A_Curso_11['Curso_Nome'] = A_Curso_11['Curso'].str.cat(A_Curso_11['Nome'], sep =" ")
    #A_Curso_11
    #...
    tresprimeiros = []
    if (len(A_Curso_11)<3):
        for i in range(len(A_Curso_11)):
            tresprimeiros.append(int(float(A_Curso_11.Curso[i])))
    else:
        for i in range(3):
            tresprimeiros.append(int(float(A_Curso_11.Curso[i])))

    #...
    #Deletar coluna
    del A_Curso_11["Curso"]
    del A_Curso_11["Nome"]
    #A_Curso_11
    A_Curso_11 = A_Curso_11.set_index('Curso_Nome')
    #A_Curso_11
    ## ...  Plotando o gráfico ... comentando essa parte do grafico dos 10 maiores cursos ======================================================
    ##A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
    #A_Curso_11_sort = A_Curso_11.sort_values("Curso_Repet",ascending=True)
    ##A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
    #A_Curso_11_sort.plot(kind='barh',title=titulo10)
    #plt.xlabel("")
    #plt.show()
    #...
    #A_cbo_10.plot(kind='bar',title="Curso 380: Direito -  Os 10 maiores",rot=92)
    if (len(A_Curso_11)<3):
       A_Curso_11_sort = A_Curso_11.iloc[0:len(A_Curso_11)].sort_values("Curso_Repet",ascending=True)
       #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
       #A_Curso_11_sort.plot(kind='barh',title="CBO 2611: Advogados e Juristas -  Os 3 maiores Cursos")
       A_Curso_11_sort.plot(kind='barh',title=titulo3)
       plt.xlabel("")
       plt.show()
    else:
        A_Curso_11_sort = A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=True)
        #A_cbo_10_sort.plot(kind='barh',title="Curso 380: Direito -  Os 10 maiores",rot=45)
        #A_Curso_11_sort.plot(kind='barh',title="CBO 2611: Advogados e Juristas -  Os 3 maiores Cursos")
        A_Curso_11_sort.plot(kind='barh',title=titulo3)
        plt.xlabel("")
        plt.show()
        #return A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=False)
        #return A_Curso_11.iloc[0:3].sort_values("Curso_Repet",ascending=False)
    return tresprimeiros
    #return
#=====================================================================================================================================================================================================    
#=====================================================================================================================================================================================================    
#01/09/2023
#Função 9: Plotar os três primeiros cursos dos três primeiros CBOs - 01/09/2023
#Função para plotar os três primeiros cursos dos três primeiros CBOs ...
def Plot_Cursos_CBOs(csv_estado,csv_CBO,csv_CURSOS,primeirosCursos,primeirosCbos):
    for i in range (len(primeirosCbos)):
          #tresprimeiros=Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo10,titulo3)
          #tresprimeirosCursos=Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo10,titulo3)
          titulo3= primeirosCursos[i] + " -  Os 3 maiores Cursos"
          #print(titulo3)
          #print(primeirosCbos[i])
          tresprimeirosCursos=Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3)
          #print(tresprimeirosCursos)
          print("============================================================================================================================================")
    return
#=====================================================================================================================================================================================================    
#=====================================================================================================================================================================================================    
#03/09/2023
#Função 9.1: Plotar os três primeiros cursos dos três primeiros CBOs - 03/09/2023 - Versão Melhorada
#Função para plotar os três primeiros cursos dos três primeiros CBOs ...
def Plot_Cursos_CBOs_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCursos,primeirosCbos):
    for i in range (len(primeirosCbos)):
          #tresprimeiros=Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,cbo_num,titulo10,titulo3)
          #tresprimeirosCursos=Cursos_CBO(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo10,titulo3)
          titulo3= primeirosCursos[i] + " -  Os 3 maiores Cursos"
          #print(titulo3)
          #print(primeirosCbos[i])
          tresprimeirosCursos=Cursos_CBO_10(csv_estado,csv_CBO,csv_CURSOS,primeirosCbos[i],titulo3)
          #print(tresprimeirosCursos)
          print("============================================================================================================================================")
    return
#=====================================================================================================================================================================================================    
#=====================================================================================================================================================================================================    
