# IBGE Parser
from ibgeparser.enums import Estados

amostras = [
    'Amostra_Pessoas_41_PR.csv','Amostra_Pessoas_42_SC.csv','Amostra_Pessoas_43_RS.csv',
    'Amostra_Pessoas_32_ES.csv','Amostra_Pessoas_33_RJ.csv','Amostra_Pessoas_35_RMSP_SP2_RM.csv','Amostra_Pessoas_35_outras_SP1.csv', 'Amostra_Pessoas_31_MG.csv',
    'Amostra_Pessoas_50_MS.csv',  'Amostra_Pessoas_51_MT.csv',  'Amostra_Pessoas_52_GO.csv', 'Amostra_Pessoas_53_DF.csv',
    'Amostra_Pessoas_11_RO.csv', 'Amostra_Pessoas_12_AC.csv', 'Amostra_Pessoas_13_AM.csv', 'Amostra_Pessoas_14_RR.csv','Amostra_Pessoas_15_PA.csv','Amostra_Pessoas_16_AP.csv','Amostra_Pessoas_17_TO.csv',
    'Amostra_Pessoas_29_BA.csv','Amostra_Pessoas_21_MA.csv',  'Amostra_Pessoas_23_CE.csv',  'Amostra_Pessoas_24_RN.csv','Amostra_Pessoas_25_PB.csv',  'Amostra_Pessoas_26_PE.csv', 'Amostra_Pessoas_27_AL.csv',  'Amostra_Pessoas_28_SE.csv']


estados = [Estados.ACRE, Estados.AMAPA, Estados.AMAZONAS, Estados.PARA, Estados.RONDONIA,
           Estados.RORAIMA, Estados.TOCANTINS, # Norte
           Estados.ALAGOAS, Estados.BAHIA, Estados.CEARA,  Estados.MARANHAO, Estados.PARAIBA,
           Estados.PERNAMBUCO, Estados.RIO_GRANDE_DO_NORTE, Estados.SERGIPE, #Nordeste
           Estados.ESPIRITO_SANTO, Estados.MINAS_GERAIS, Estados.RIO_DE_JANEIRO,
           Estados.SAO_PAULO_SP1, Estados.SAO_PAULO_SP2_RM, # Sudeste
           Estados.PARANA, Estados.RIO_GRANDE_DO_SUL, Estados.SANTA_CATARINA, # Sul
           Estados.DISTRITO_FEDERAL, Estados.GOIAS, Estados.MATO_GROSSO, Estados.MATO_GROSSO_DO_SUL] #Centro-Oeste

ibge_columns = ["V6036", "V6400", "V6352", "V6354", "V6356", "V6461",  "V6471", "V6462", "V6472", "V6511", "V6514", "V0601", "V0656"]
ibge_rename_columns = {
    "V6036" : "Idade_em_Anos",
    "V6400" : "Nível_instrução",
    "V6352" : "Curso_Superior_Graduação_Código",
    "V6354" : "Curso_Mestrado_Código",
    "V6356" : "Curso_Doutorado_Código",
    "V6461" : "Ocupação_Código",
    "V6471" : "Atividade_Código",
    "V6462" : "CBO-Domiciliar",
    "V6472" : "CNAE-Domiciliar",
    "V6511" : "Valor_rend_bruto_M",
    "V6514" : "Qtdade_Salario",
    "V0601" : "gênero",
    "V0656" : "rendimento_aposentadoria_pensao"
}
