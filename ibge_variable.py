from ibgeparser.enums import Anos, Estados, Modalidades

def estados():
    estados = [Estados.PARANA], [Estados.SANTA_CATARINA], [Estados.RIO_GRANDE_DO_SUL], [Estados.MATO_GROSSO_DO_SUL], [Estados.MATO_GROSSO], [Estados.GOIAS], [Estados.DISTRITO_FEDERAL], [Estados.RONDONIA],[Estados.ACRE], [Estados.AMAZONAS], [Estados.RORAIMA], [Estados.PARA], [Estados.AMAPA],[Estados.TOCANTINS]
    #estados= [Estados.PARANA], [Estados.SANTA_CATARINA], [Estados.RIO_GRANDE_DO_SUL], [Estados.ESPIRITO_SANTO],  [Estados.RIO_DE_JANEIRO],  [Estados.SAO_PAULO_SP2_RM], [Estados.SAO_PAULO_SP1],  [Estados.MINAS_GERAIS], [Estados.MATO_GROSSO_DO_SUL], [Estados.MATO_GROSSO], [Estados.GOIAS], [Estados.DISTRITO_FEDERAL], [Estados.RONDONIA],[Estados.ACRE], [Estados.AMAZONAS], [Estados.RORAIMA], [Estados.PARA], [Estados.AMAPA],[Estados.TOCANTINS],[Estados.BAHIA],  [Estados.MARANHAO],  [Estados.CEARA],  [Estados.RIO_GRANDE_DO_NORTE],  [Estados.PARAIBA], [Estados.PERNAMBUCO], [Estados.ALAGOAS],  [Estados.SERGIPE]
    return estados

def names(fase,opcao):
    if fase ==1:
       if opcao == 1:
          #names = ['Amostra_Pessoas_41_PR.csv','Amostra_Pessoas_42_SC.csv','Amostra_Pessoas_43_RS.csv'],['Amostra_Pessoas_32_ES.csv','Amostra_Pessoas_33_RJ.csv','Amostra_Pessoas_35_RMSP_SP2_RM.csv','Amostra_Pessoas_35_outras_SP1.csv', 'Amostra_Pessoas_31_MG.csv'], ['Amostra_Pessoas_50_MS.csv',  'Amostra_Pessoas_51_MT.csv',  'Amostra_Pessoas_52_GO.csv', 'Amostra_Pessoas_53_DF.csv'], ['Amostra_Pessoas_11_RO.csv', 'Amostra_Pessoas_12_AC.csv', 'Amostra_Pessoas_13_AM.csv', 'Amostra_Pessoas_14_RR.csv','Amostra_Pessoas_15_PA.csv','Amostra_Pessoas_16_AP.csv','Amostra_Pessoas_17_TO.csv'], ['Amostra_Pessoas_29_BA.csv','Amostra_Pessoas_21_MA.csv',  'Amostra_Pessoas_23_CE.csv',  'Amostra_Pessoas_24_RN.csv','Amostra_Pessoas_25_PB.csv',  'Amostra_Pessoas_26_PE.csv', 'Amostra_Pessoas_27_AL.csv',  'Amostra_Pessoas_28_SE.csv']
          names = ['Amostra_Pessoas_41_PR.csv','Amostra_Pessoas_42_SC.csv','Amostra_Pessoas_43_RS.csv'], ['Amostra_Pessoas_50_MS.csv',  'Amostra_Pessoas_51_MT.csv','Amostra_Pessoas_52_GO.csv','Amostra_Pessoas_53_DF.csv'], ['Amostra_Pessoas_11_RO.csv', 'Amostra_Pessoas_12_AC.csv', 'Amostra_Pessoas_13_AM.csv', 'Amostra_Pessoas_14_RR.csv','Amostra_Pessoas_15_PA.csv','Amostra_Pessoas_16_AP.csv','Amostra_Pessoas_17_TO.csv'], ['Amostra_Pessoas_29_BA.csv','Amostra_Pessoas_21_MA.csv',  'Amostra_Pessoas_23_CE.csv',  'Amostra_Pessoas_24_RN.csv','Amostra_Pessoas_25_PB.csv',  'Amostra_Pessoas_26_PE.csv', 'Amostra_Pessoas_27_AL.csv',  'Amostra_Pessoas_28_SE.csv'], ['Amostra_Pessoas_32_ES.csv','Amostra_Pessoas_33_RJ.csv','Amostra_Pessoas_35_RMSP_SP2_RM.csv','Amostra_Pessoas_35_outras_SP1.csv', 'Amostra_Pessoas_31_MG.csv'],
    else:
       if fase ==2:
         if opcao == 1:
            names = ['Amostra_Pessoas_41_PR_Fase1.csv','Amostra_Pessoas_42_SC_Fase1.csv','Amostra_Pessoas_43_RS_Fase1.csv'], ['Amostra_Pessoas_50_MS_Fase1.csv',  'Amostra_Pessoas_51_MT_Fase1.csv','Amostra_Pessoas_52_GO_Fase1.csv','Amostra_Pessoas_53_DF_Fase1.csv'], ['Amostra_Pessoas_11_RO_Fase1.csv', 'Amostra_Pessoas_12_AC_Fase1.csv', 'Amostra_Pessoas_13_AM_Fase1.csv', 'Amostra_Pessoas_14_RR_Fase1.csv','Amostra_Pessoas_15_PA_Fase1.csv','Amostra_Pessoas_16_AP_Fase1.csv','Amostra_Pessoas_17_TO_Fase1.csv'],['Amostra_Pessoas_21_MA_Fase1.csv', 'Amostra_Pessoas_29_BA_Fase1.csv', 'Amostra_Pessoas_26_PE_Fase1.csv', 'Amostra_Pessoas_27_AL_Fase1.csv', 'Amostra_Pessoas_24_RN_Fase1.csv', 'Amostra_Pessoas_25_PB_Fase1.csv', 'Amostra_Pessoas_28_SE_Fase1.csv', 'Amostra_Pessoas_23_CE_Fase1.csv'],['Amostra_Pessoas_33_RJ_Fase1.csv', 'Amostra_Pessoas_32_ES_Fase1.csv', 'Amostra_Pessoas_35_outras_SP1_Fase1.csv', 'Amostra_Pessoas_31_MG_Fase1.csv', 'Amostra_Pessoas_35_RMSP_SP2_RM_Fase1.csv']
         if opcao == 2:
            names = ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_43_RS_Fase1_Graduados_NaoGraduados.csv'], ['Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_52_GO_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_53_DF_Fase1_Graduados_NaoGraduados.csv'], ['Amostra_Pessoas_11_RO_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_14_RR_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_17_TO_Fase1_Graduados_NaoGraduados.csv','Amostra_Pessoas_12_AC_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_15_PA_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_13_AM_Fase1_Graduados_NaoGraduados.csv',  'Amostra_Pessoas_16_AP_Fase1_Graduados_NaoGraduados.csv'], ['Amostra_Pessoas_21_MA_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_29_BA_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_26_PE_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_27_AL_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_24_RN_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_25_PB_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_28_SE_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_23_CE_Fase1_Graduados_NaoGraduados.csv'],['Amostra_Pessoas_33_RJ_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_32_ES_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_35_outras_SP1_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_31_MG_Fase1_Graduados_NaoGraduados.csv', 'Amostra_Pessoas_35_RMSP_SP2_RM_Fase1_Graduados_NaoGraduados.csv']
         if opcao == 3:
            names = ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_43_RS_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv'], ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv','Amostra_Pessoas_43_RS_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv'], ['Amostra_Pessoas_41_PR_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_42_SC_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_43_RS_Fase1_Graduados_NaoGraduados_PivotTablet.csv'], ['Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_52_GO_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_53_DF_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv'], ['Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv','Amostra_Pessoas_52_GO_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv','Amostra_Pessoas_53_DF_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv'], ['Amostra_Pessoas_50_MS_Fase1_Graduados_NaoGraduados_PivotTablet.csv',  'Amostra_Pessoas_51_MT_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_52_GO_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_53_DF_Fase1_Graduados_NaoGraduados_PivotTablet.csv'], ['Amostra_Pessoas_11_RO_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_12_AC_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_13_AM_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_14_RR_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_15_PA_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_16_AP_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv','Amostra_Pessoas_17_TO_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv'], ['Amostra_Pessoas_11_RO_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv',  'Amostra_Pessoas_12_AC_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_13_AM_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv' ,'Amostra_Pessoas_14_RR_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_15_PA_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', ' Amostra_Pessoas_16_AP_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv','Amostra_Pessoas_17_TO_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv'], ['Amostra_Pessoas_11_RO_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_12_AC_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_13_AM_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_14_RR_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_15_PA_Fase1_Graduados_NaoGraduados_PivotTablet.csv','Amostra_Pessoas_16_AP_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_17_TO_Fase1_Graduados_NaoGraduados_PivotTablet.csv' ],     ['Amostra_Pessoas_21_MA_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_29_BA_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_26_PE_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_27_AL_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_24_RN_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_25_PB_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_28_SE_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_23_CE_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv'], ['Amostra_Pessoas_21_MA_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_29_BA_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_26_PE_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_27_AL_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_24_RN_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_25_PB_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_28_SE_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_23_CE_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv'],['Amostra_Pessoas_21_MA_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_29_BA_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_26_PE_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_27_AL_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_24_RN_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_25_PB_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_28_SE_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_23_CE_Fase1_Graduados_NaoGraduados_PivotTablet.csv'],['Amostra_Pessoas_33_RJ_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_32_ES_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_35_outras_SP1_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_31_MG_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv', 'Amostra_Pessoas_35_RMSP_SP2_RM_Fase1_Graduados_NaoGraduados_PivotTabletMasculina.csv'], ['Amostra_Pessoas_33_RJ_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_32_ES_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_35_outras_SP1_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_31_MG_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv', 'Amostra_Pessoas_35_RMSP_SP2_RM_Fase1_Graduados_NaoGraduados_PivotTabletFeminina.csv'],['Amostra_Pessoas_33_RJ_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_32_ES_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_35_outras_SP1_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_31_MG_Fase1_Graduados_NaoGraduados_PivotTablet.csv', 'Amostra_Pessoas_35_RMSP_SP2_RM_Fase1_Graduados_NaoGraduados_PivotTablet.csv']
         if opcao == 4:
            names =['Sul_PivotFinalMasculina.csv','Norte_PivotFinalMasculina.csv', 'Centro_Oeste_PivotFinalMasculina.csv', 'Nordeste_PivotFinalMasculina.csv', 'Sudeste_PivotFinalMasculina.csv'], ['Sul_PivotFinalFeminina.csv','Norte_PivotFinalFeminina.csv', 'Centro_Oeste_PivotFinalFeminina.csv', 'Nordeste_PivotFinalFeminina.csv', 'Sudeste_PivotFinalFeminina.csv'],['Sul_PivotFinal.csv','Norte_PivotFinal.csv', 'Centro_Oeste_PivotFinal.csv','Nordeste_PivotFinal.csv', 'Sudeste_PivotFinal.csv']
    return names

def paths(fase,opcao):
    if fase ==1:
       if opcao == 1:
          path = ['original/Sul/', 'original/Centro_Oeste/', 'original/Norte/','original/Nordeste/', 'original/Sudeste/']
       if opcao == 2:
          path = ['processados/Sul/', 'processados/Centro_Oeste/', 'processados/Norte/', 'processados/Nordeste/','processados/Sudeste/']
    else:
        if fase ==2:
           if opcao == 2:
              path = ['processados/Sul/', 'processados/Centro_Oeste/', 'processados/Norte/', 'processados/Nordeste/', 'processados/Sudeste/']
           if opcao == 3:  
               path = ['processados/Sul/Graduados_NaoGraduados/', 'processados/Centro_Oeste/Graduados_NaoGraduados/', 'processados/Norte/Graduados_NaoGraduados/', 'processados/Nordeste/Graduados_NaoGraduados/', 'processados/Sudeste/Graduados_NaoGraduados/']
           if opcao == 4:
              path = ['processados/Sul/PivotTablet/Feminino/', 'processados/Centro_Oeste/PivotTablet/Feminino/', 'processados/Norte/PivotTablet/Feminino/', 'processados/Nordeste/PivotTablet/Feminino/','processados/Sudeste/PivotTablet/Feminino/']
           if opcao == 5:
              path = ['processados/Sul/PivotTablet/Masculino/', 'processados/Centro_Oeste/PivotTablet/Masculino/',  'processados/Norte/PivotTablet/Masculino/', 'processados/Nordeste/PivotTablet/Masculino/', 'processados/Sudeste/PivotTablet/Masculino/']
           if opcao ==6:
              path = ['processados/Sul/PivotTablet/', 'processados/Centro_Oeste/PivotTablet/', 'processados/Norte/PivotTablet/', 'processados/Nordeste/PivotTablet/', 'processados/Sudeste/PivotTablet/']
           if opcao ==7:  
              path = ["processados/Sul/PivotTablet/Masculino/", "processados/Sul/PivotTablet/Feminino/", "processados/Sul/PivotTablet/"], ["processados/Centro_Oeste/PivotTablet/Masculino/", "processados/Centro_Oeste/PivotTablet/Feminino/", "processados/Centro_Oeste/PivotTablet/"], ["processados/Norte/PivotTablet/Masculino/", "processados/Norte/PivotTablet/Feminino/", "processados/Norte/PivotTablet/"],  ["processados/Nordeste/PivotTablet/Masculino/", "processados/Nordeste/PivotTablet/Feminino/", "processados/Nordeste/PivotTablet/"], ["processados/Sudeste/PivotTablet/Masculino/", "processados/Sudeste/PivotTablet/Feminino/", "processados/Sudeste/PivotTablet/"]                                                      
           if opcao ==8:
              path = ['processados/CSVs_PivotTableFinal/']
           if opcao ==9:
              path = ['processados/Sul/Clean_Graduados/', 'processados/Centro_Oeste/Clean_Graduados/', 'processados/Norte/Clean_Graduados/', 'processados/Nordeste/Clean_Graduados/', 'processados/Sudeste/Clean_Graduados/']
           if opcao ==10:
              path = ['/processados/Sul/Clean_Graduados/', '/processados/Sul/Graduados_NaoGraduados/'], ['/processados/Centro_Oeste/Clean_Graduados/', '/processados/Centro_Oeste/Graduados_NaoGraduados/'], ['/processados/Norte/Clean_Graduados/', '/processados/Norte/Graduados_NaoGraduados/'], ['/processados/Nordeste/Clean_Graduados/', '/processados/Nordeste/Graduados_NaoGraduados/'],['/processados/Sudeste/Clean_Graduados/', '/processados/Sudeste/Graduados_NaoGraduados/'], ['/processados/CSVs_ArquivoFinalGraduados/', '/processados/CSVs_ArquivoFinalGraduados_NaoGraduados/']
           if opcao ==11:
              path = ['/processados/CSVs_ArquivoFinalGraduados/','/processados/CSVs_ArquivoFinalGraduados_NaoGraduados/','/processados/CSVs_Brasil/']
           if opcao ==12:  
              path = ["processados/CSVs_PivotTableFinal/Masculino/", "processados/CSVs_PivotTableFinal/Feminino/", "processados/CSVs_PivotTableFinal/Geral/"]
           if opcao ==13:
              path = ['processados/CSVs_Brasil/']   
    return path
