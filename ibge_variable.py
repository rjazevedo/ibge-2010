from ibgeparser.enums import Anos, Estados, Modalidades

def estados():
    estados = [Estados.PARANA], [Estados.SANTA_CATARINA], [Estados.RIO_GRANDE_DO_SUL], [Estados.MATO_GROSSO_DO_SUL], [Estados.MATO_GROSSO], [Estados.GOIAS], [Estados.DISTRITO_FEDERAL], [Estados.RONDONIA],[Estados.ACRE], [Estados.AMAZONAS], [Estados.RORAIMA], [Estados.PARA], [Estados.AMAPA],[Estados.TOCANTINS]
    return estados

def names(fase,opcao):
    if fase ==1:
       if opcao == 1:
          names = ['Amostra_Pessoas_41_PR.csv','Amostra_Pessoas_42_SC.csv','Amostra_Pessoas_43_RS.csv','Amostra_Pessoas_50_MS.csv',  'Amostra_Pessoas_51_MT.csv','Amostra_Pessoas_52_GO.csv','Amostra_Pessoas_53_DF.csv','Amostra_Pessoas_11_RO.csv', 'Amostra_Pessoas_12_AC.csv', 'Amostra_Pessoas_13_AM.csv', 'Amostra_Pessoas_14_RR.csv','Amostra_Pessoas_15_PA.csv','Amostra_Pessoas_16_AP.csv','Amostra_Pessoas_17_TO.csv','Amostra_Pessoas_29_BA.csv','Amostra_Pessoas_21_MA.csv',  'Amostra_Pessoas_23_CE.csv',  'Amostra_Pessoas_24_RN.csv','Amostra_Pessoas_25_PB.csv',  'Amostra_Pessoas_26_PE.csv', 'Amostra_Pessoas_27_AL.csv',  'Amostra_Pessoas_28_SE.csv','Amostra_Pessoas_32_ES.csv','Amostra_Pessoas_33_RJ.csv','Amostra_Pessoas_35_RMSP_SP2_RM.csv','Amostra_Pessoas_35_outras_SP1.csv', 'Amostra_Pessoas_31_MG.csv']
    if fase == 2:
       if opcao == 1:
          names = ['Amostra_Pessoas_41_PR_Fase1.csv','Amostra_Pessoas_42_SC_Fase1.csv','Amostra_Pessoas_43_RS_Fase1.csv','Amostra_Pessoas_50_MS_Fase1.csv',  'Amostra_Pessoas_51_MT_Fase1.csv','Amostra_Pessoas_52_GO_Fase1.csv','Amostra_Pessoas_53_DF_Fase1.csv','Amostra_Pessoas_11_RO_Fase1.csv', 'Amostra_Pessoas_12_AC_Fase1.csv', 'Amostra_Pessoas_13_AM_Fase1.csv', 'Amostra_Pessoas_14_RR_Fase1.csv','Amostra_Pessoas_15_PA_Fase1.csv','Amostra_Pessoas_16_AP_Fase1.csv','Amostra_Pessoas_17_TO_Fase1.csv','Amostra_Pessoas_21_MA_Fase1.csv', 'Amostra_Pessoas_29_BA_Fase1.csv', 'Amostra_Pessoas_26_PE_Fase1.csv', 'Amostra_Pessoas_27_AL_Fase1.csv', 'Amostra_Pessoas_24_RN_Fase1.csv', 'Amostra_Pessoas_25_PB_Fase1.csv', 'Amostra_Pessoas_28_SE_Fase1.csv', 'Amostra_Pessoas_23_CE_Fase1.csv','Amostra_Pessoas_33_RJ_Fase1.csv', 'Amostra_Pessoas_32_ES_Fase1.csv', 'Amostra_Pessoas_35_outras_SP1_Fase1.csv', 'Amostra_Pessoas_31_MG_Fase1.csv', 'Amostra_Pessoas_35_RMSP_SP2_RM_Fase1.csv']
       if opcao == 2:
          names = ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_43_RS_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_52_GO_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_53_DF_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_11_RO_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_14_RR_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_17_TO_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_12_AC_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_15_PA_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_13_AM_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_16_AP_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_21_MA_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_29_BA_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_26_PE_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_27_AL_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_24_RN_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_25_PB_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_28_SE_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_23_CE_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_33_RJ_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_32_ES_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_35_outras_SP1_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_31_MG_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_35_RMSP_SP2_RM_Fase1_Graduados_NaoGraduados.csv']
       if opcao == 3:
          names = ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_43_RS_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_52_GO_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_53_DF_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_11_RO_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_12_AC_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_13_AM_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_14_RR_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_15_PA_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_16_AP_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_17_TO_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_21_MA_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_29_BA_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_26_PE_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_27_AL_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_24_RN_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_25_PB_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_28_SE_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_23_CE_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_33_RJ_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_32_ES_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_35_outras_SP1_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_31_MG_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_35_RMSP_SP2_RM_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv'], ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv','Amostra_Pessoas_43_RS_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv','Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv','Amostra_Pessoas_52_GO_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv','Amostra_Pessoas_53_DF_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv','Amostra_Pessoas_11_RO_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv',  'Amostra_Pessoas_12_AC_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_13_AM_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv' ,'Amostra_Pessoas_14_RR_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_15_PA_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_16_AP_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv','Amostra_Pessoas_17_TO_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv','Amostra_Pessoas_21_MA_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_29_BA_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_26_PE_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_27_AL_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_24_RN_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_25_PB_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_28_SE_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_23_CE_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv','Amostra_Pessoas_33_RJ_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_32_ES_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_35_outras_SP1_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_31_MG_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_35_RMSP_SP2_RM_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv'], ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_43_RS_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados_PivotTablet.csv',  'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_52_GO_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_53_DF_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_11_RO_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_12_AC_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_13_AM_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_14_RR_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_15_PA_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_16_AP_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_17_TO_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_21_MA_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_29_BA_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_26_PE_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_27_AL_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_24_RN_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_25_PB_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_28_SE_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_23_CE_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_33_RJ_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_32_ES_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_35_outras_SP1_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_31_MG_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_35_RMSP_SP2_RM_Fase1_Graduados_NaoGraduados_PivotTablet.csv']
    if fase == 3:
       if opcao == 1:
          names = ['Atividade CNAE_DOM 2.0 2010.xls','Ocupaç╞o COD 2010.xls','Cursos Superiores_Estrutura 2010.xls']
       if opcao == 2:
          names = ['CNAE_CSV.csv','CBO_CSV.csv','Curso_CSV.csv']
       if opcao == 3:
          names = ['Brasil_Graduados.csv','Brasil_Não-Graduados.csv']   

    return names

#def paths(fase,opcao):
def paths(opcao):
   #  if fase ==1:
    if opcao == 1:
       path = ['microdados-ibge/original/']
    if opcao == 2:
       path = ['microdados-ibge/processados/']
   #  if fase ==2:
   #  if opcao == 2:
       # path =['microdados-ibge/processados/']
    if opcao == 3:
       path = ['microdados-ibge/processados/Graduados_NaoGraduados/']
    if opcao == 4:
       path = ['microdados-ibge/processados/PivotTable/Feminino/']
    if opcao == 5:
       path = ['microdados-ibge/processados/PivotTable/Masculino/']
    if opcao ==6:
       path = ['microdados-ibge/processados/PivotTable/']
    if opcao ==7:  
       path = ['microdados-ibge/processados/PivotTable/Masculino/', 'microdados-ibge/processados/PivotTable/Feminino/', 'microdados-ibge/processados/PivotTable/']
    if opcao ==8:
       path = ['microdados-ibge/processados/CSVs_PivotTableFinal/']
    if opcao ==9:
       path = ['microdados-ibge/processados/Graduados/']
    if opcao ==10:
       path = ['microdados-ibge/processados/Graduados/','microdados-ibge/processados/Graduados_NaoGraduados/']
    if opcao ==11:
       path = ['microdados-ibge/processados/CSVs_ArquivoFinalGraduados/','microdados-ibge/processados/CSVs_ArquivoFinalGraduados_NaoGraduados/']
    #if fase ==3:   
   #  if opcao == 1: 
    if opcao == 12: 
       path = ['microdados-ibge/documentacao/']      
   #  if opcao == 2: 
   #     path = ['microdados-ibge/processados/CSVs_ArquivoFinalGraduados/', 'microdados-ibge/processados/CSVs_ArquivoFinalGraduados_NaoGraduados/']       
    return path
