from ibgeparser.enums import Estados

def estados():
    estados = [[Estados.TODOS]]
    return estados
def paths(opcao):
    if opcao == 1:
       path = ['microdados-ibge/original/']
    if opcao == 2:
       path = ['processados/']
    if opcao == 3:
       path = ['processados/Graduados_NaoGraduados/']
    if opcao == 4:
       path = ['processados/PivotTable/Feminino/']
    if opcao == 5:
       path = ['processados/PivotTable/Masculino/']
    if opcao ==6:
       path = ['processados/PivotTable/']
    if opcao ==7:  
       path = ['processados/PivotTable/Masculino/', 'processados/PivotTable/Feminino/', 'processados/PivotTable/']
    if opcao ==8:
       path = ['processados/CSVs_PivotTableFinal/']
    if opcao ==9:
       path = ['processados/Graduados/']
    if opcao ==10:
       path = ['processados/Graduados/','processados/Graduados_NaoGraduados/']
    if opcao ==11:
       path = ['processados/CSVs_ArquivoFinalGraduados/','processados/CSVs_ArquivoFinalGraduados_NaoGraduados/']
    if opcao == 12: 
       path = ['documentacao/']      
    if opcao == 13: 
       path = ['graficos/']        
    return path

def names(opcao):
   if opcao == 1:       
      names = ['Amostra_Pessoas_41_PR.csv','Amostra_Pessoas_42_SC.csv','Amostra_Pessoas_43_RS.csv','Amostra_Pessoas_50_MS.csv',  'Amostra_Pessoas_51_MT.csv','Amostra_Pessoas_52_GO.csv','Amostra_Pessoas_53_DF.csv','Amostra_Pessoas_11_RO.csv', 'Amostra_Pessoas_12_AC.csv', 'Amostra_Pessoas_13_AM.csv', 'Amostra_Pessoas_14_RR.csv','Amostra_Pessoas_15_PA.csv','Amostra_Pessoas_16_AP.csv','Amostra_Pessoas_17_TO.csv','Amostra_Pessoas_29_BA.csv','Amostra_Pessoas_21_MA.csv','Amostra_Pessoas_22_PI.csv','Amostra_Pessoas_23_CE.csv',  'Amostra_Pessoas_24_RN.csv','Amostra_Pessoas_25_PB.csv',  'Amostra_Pessoas_26_PE.csv', 'Amostra_Pessoas_27_AL.csv',  'Amostra_Pessoas_28_SE.csv','Amostra_Pessoas_32_ES.csv','Amostra_Pessoas_33_RJ.csv','Amostra_Pessoas_35_RMSP_SP2_RM.csv','Amostra_Pessoas_35_outras_SP1.csv', 'Amostra_Pessoas_31_MG.csv']
   if opcao == 2:       
      names = ['Amostra_Pessoas_41_PR_Fase1.csv','Amostra_Pessoas_42_SC_Fase1.csv','Amostra_Pessoas_43_RS_Fase1.csv','Amostra_Pessoas_50_MS_Fase1.csv',  'Amostra_Pessoas_51_MT_Fase1.csv','Amostra_Pessoas_52_GO_Fase1.csv','Amostra_Pessoas_53_DF_Fase1.csv','Amostra_Pessoas_11_RO_Fase1.csv', 'Amostra_Pessoas_12_AC_Fase1.csv', 'Amostra_Pessoas_13_AM_Fase1.csv', 'Amostra_Pessoas_14_RR_Fase1.csv','Amostra_Pessoas_15_PA_Fase1.csv','Amostra_Pessoas_16_AP_Fase1.csv','Amostra_Pessoas_17_TO_Fase1.csv','Amostra_Pessoas_21_MA_Fase1.csv', 'Amostra_Pessoas_22_PI_Fase1.csv', 'Amostra_Pessoas_29_BA_Fase1.csv', 'Amostra_Pessoas_26_PE_Fase1.csv', 'Amostra_Pessoas_27_AL_Fase1.csv', 'Amostra_Pessoas_24_RN_Fase1.csv', 'Amostra_Pessoas_25_PB_Fase1.csv', 'Amostra_Pessoas_28_SE_Fase1.csv', 'Amostra_Pessoas_23_CE_Fase1.csv','Amostra_Pessoas_33_RJ_Fase1.csv', 'Amostra_Pessoas_32_ES_Fase1.csv', 'Amostra_Pessoas_35_outras_SP1_Fase1.csv', 'Amostra_Pessoas_31_MG_Fase1.csv', 'Amostra_Pessoas_35_RMSP_SP2_RM_Fase1.csv']
   if opcao == 3:       
      names = ['Amostra_Pessoas_41_PR_Todos.csv',  'Amostra_Pessoas_42_SC_Todos.csv',  'Amostra_Pessoas_43_RS_Todos.csv','Amostra_Pessoas_50_MS_Todos.csv',  'Amostra_Pessoas_51_MT_Todos.csv', 'Amostra_Pessoas_52_GO_Todos.csv','Amostra_Pessoas_53_DF_Todos.csv','Amostra_Pessoas_11_RO_Todos.csv',  'Amostra_Pessoas_14_RR_Todos.csv',  'Amostra_Pessoas_17_TO_Todos.csv','Amostra_Pessoas_12_AC_Todos.csv',  'Amostra_Pessoas_15_PA_Todos.csv', 'Amostra_Pessoas_13_AM_Todos.csv',  'Amostra_Pessoas_16_AP_Todos.csv','Amostra_Pessoas_21_MA_Todos.csv', 'Amostra_Pessoas_22_PI_Todos.csv','Amostra_Pessoas_29_BA_Todos.csv', 'Amostra_Pessoas_26_PE_Todos.csv', 'Amostra_Pessoas_27_AL_Todos.csv', 'Amostra_Pessoas_24_RN_Todos.csv', 'Amostra_Pessoas_25_PB_Todos.csv', 'Amostra_Pessoas_28_SE_Todos.csv', 'Amostra_Pessoas_23_CE_Todos.csv','Amostra_Pessoas_33_RJ_Todos.csv', 'Amostra_Pessoas_32_ES_Todos.csv', 'Amostra_Pessoas_35_outras_SP1_Todos.csv', 'Amostra_Pessoas_31_MG_Todos.csv', 'Amostra_Pessoas_35_RMSP_SP2_RM_Todos.csv']
   if opcao == 4:
      names = ['Amostra_Pessoas_41_PR_PivotTabletMasculina.csv', 'Amostra_Pessoas_42_SC_PivotTabletMasculina.csv', 'Amostra_Pessoas_43_RS_PivotTabletMasculina.csv', 'Amostra_Pessoas_50_MS_PivotTabletMasculina.csv', 'Amostra_Pessoas_51_MT_PivotTabletMasculina.csv', 'Amostra_Pessoas_52_GO_PivotTabletMasculina.csv', 'Amostra_Pessoas_53_DF_PivotTabletMasculina.csv', 'Amostra_Pessoas_11_RO_PivotTabletMasculina.csv', 'Amostra_Pessoas_12_AC_PivotTabletMasculina.csv', 'Amostra_Pessoas_13_AM_PivotTabletMasculina.csv', 'Amostra_Pessoas_14_RR_PivotTabletMasculina.csv',  'Amostra_Pessoas_15_PA_PivotTabletMasculina.csv', 'Amostra_Pessoas_16_AP_PivotTabletMasculina.csv', 'Amostra_Pessoas_17_TO_PivotTabletMasculina.csv', 'Amostra_Pessoas_21_MA_PivotTabletMasculina.csv', 'Amostra_Pessoas_22_PI_PivotTabletMasculina.csv', 'Amostra_Pessoas_29_BA_PivotTabletMasculina.csv',  'Amostra_Pessoas_26_PE_PivotTabletMasculina.csv', 'Amostra_Pessoas_27_AL_PivotTabletMasculina.csv', 'Amostra_Pessoas_24_RN_PivotTabletMasculina.csv', 'Amostra_Pessoas_25_PB_PivotTabletMasculina.csv', 'Amostra_Pessoas_28_SE_PivotTabletMasculina.csv', 'Amostra_Pessoas_23_CE_PivotTabletMasculina.csv', 'Amostra_Pessoas_33_RJ_PivotTabletMasculina.csv', 'Amostra_Pessoas_32_ES_PivotTabletMasculina.csv', 'Amostra_Pessoas_35_outras_SP1_PivotTabletMasculina.csv', 'Amostra_Pessoas_31_MG_PivotTabletMasculina.csv', 'Amostra_Pessoas_35_RMSP_SP2_RM_PivotTabletMasculina.csv'], ['Amostra_Pessoas_41_PR_PivotTabletFeminina.csv', 'Amostra_Pessoas_42_SC_PivotTabletFeminina.csv', 'Amostra_Pessoas_43_RS_PivotTabletFeminina.csv', 'Amostra_Pessoas_50_MS_PivotTabletFeminina.csv', 'Amostra_Pessoas_51_MT_PivotTabletFeminina.csv', 'Amostra_Pessoas_52_GO_PivotTabletFeminina.csv', 'Amostra_Pessoas_53_DF_PivotTabletFeminina.csv', 'Amostra_Pessoas_11_RO_PivotTabletFeminina.csv',  'Amostra_Pessoas_12_AC_PivotTabletFeminina.csv',  'Amostra_Pessoas_13_AM_PivotTabletFeminina.csv', 'Amostra_Pessoas_14_RR_PivotTabletFeminina.csv', 'Amostra_Pessoas_15_PA_PivotTabletFeminina.csv', 'Amostra_Pessoas_16_AP_PivotTabletFeminina.csv', 'Amostra_Pessoas_17_TO_PivotTabletFeminina.csv',  'Amostra_Pessoas_21_MA_PivotTabletFeminina.csv',  'Amostra_Pessoas_22_PI_PivotTabletFeminina.csv', 'Amostra_Pessoas_29_BA_PivotTabletFeminina.csv', 'Amostra_Pessoas_26_PE_PivotTabletFeminina.csv', 'Amostra_Pessoas_27_AL_PivotTabletFeminina.csv', 'Amostra_Pessoas_24_RN_PivotTabletFeminina.csv',  'Amostra_Pessoas_25_PB_PivotTabletFeminina.csv',  'Amostra_Pessoas_28_SE_PivotTabletFeminina.csv', 'Amostra_Pessoas_23_CE_PivotTabletFeminina.csv', 'Amostra_Pessoas_33_RJ_PivotTabletFeminina.csv', 'Amostra_Pessoas_32_ES_PivotTabletFeminina.csv', 'Amostra_Pessoas_35_outras_SP1_PivotTabletFeminina.csv', 'Amostra_Pessoas_31_MG_PivotTabletFeminina.csv', 'Amostra_Pessoas_35_RMSP_SP2_RM_PivotTabletFeminina.csv'], ['Amostra_Pessoas_41_PR_PivotTablet.csv',  'Amostra_Pessoas_42_SC_PivotTablet.csv', 'Amostra_Pessoas_43_RS_PivotTablet.csv', 'Amostra_Pessoas_50_MS_PivotTablet.csv', 'Amostra_Pessoas_51_MT_PivotTablet.csv', 'Amostra_Pessoas_52_GO_PivotTablet.csv', 'Amostra_Pessoas_53_DF_PivotTablet.csv', 'Amostra_Pessoas_11_RO_PivotTablet.csv', 'Amostra_Pessoas_12_AC_PivotTablet.csv',   'Amostra_Pessoas_13_AM_PivotTablet.csv', 'Amostra_Pessoas_14_RR_PivotTablet.csv', 'Amostra_Pessoas_15_PA_PivotTablet.csv', 'Amostra_Pessoas_16_AP_PivotTablet.csv', 'Amostra_Pessoas_17_TO_PivotTablet.csv', 'Amostra_Pessoas_21_MA_PivotTablet.csv', 'Amostra_Pessoas_22_PI_PivotTablet.csv', 'Amostra_Pessoas_29_BA_PivotTablet.csv',   'Amostra_Pessoas_26_PE_PivotTablet.csv', 'Amostra_Pessoas_27_AL_PivotTablet.csv', 'Amostra_Pessoas_24_RN_PivotTablet.csv', 'Amostra_Pessoas_25_PB_PivotTablet.csv', 'Amostra_Pessoas_28_SE_PivotTablet.csv', 'Amostra_Pessoas_23_CE_PivotTablet.csv',  'Amostra_Pessoas_33_RJ_PivotTablet.csv', 'Amostra_Pessoas_32_ES_PivotTablet.csv',   'Amostra_Pessoas_35_outras_SP1_PivotTablet.csv', 'Amostra_Pessoas_31_MG_PivotTablet.csv', 'Amostra_Pessoas_35_RMSP_SP2_RM_PivotTablet.csv']  
   if opcao == 5:       
      names = ['Atividade CNAE_DOM 2.0 2010.xls','Ocupaç╞o COD 2010.xls','Cursos Superiores_Estrutura 2010.xls']
   if opcao == 6:       
      names = ['CNAE_CSV.csv','CBO_CSV.csv','Curso_CSV.csv']
   if opcao == 7:       
      names = ['Brasil_Graduados.csv','Brasil_Não-Graduados.csv','Brasil_Graduados_Fem.csv', 'Brasil_Graduados_Masc.csv']   
   if opcao == 8:       
      names = ['Brasil_PivotFinal.csv','Brasil_PivotFinalMasculina.csv','Brasil_PivotFinalFeminina.csv']   
   if opcao == 9:       
      names = ['OndeTrabalhamAsPessoasDeCadaCursoDoCenso.xlsx','10Porcent_DF.csv','10Porcent_DF_Limpo.csv', '10Porcent_DF_Fem.csv', '10Porcent_DF_Masc.csv','10Porcent_DF_Fem_Limpo.csv', '10Porcent_DF_Masc_Limpo.csv','Kmeans3_T.csv','100Porcent_DF_Fem.csv','100Porcent_DF_Masc.csv','100Porcent_DF_Fem_Limpo.csv','100Porcent_DF_Masc_Limpo.csv','Resultados_T_Fem_Masc_Kmeans3_Genero.csv','Resultados_T_Filtrados_Kmeans3_T.csv','Resultados_T_29_30-39_40-49_50-59_60Kmeans3_Idade.csv','Resultados_T_Filtrados_Kmeans3_T_Preenchido_Cluster0.csv','Resultados_T_Filtrados_Kmeans3_T_Preenchido_Cluster1.csv','Resultados_T_Filtrados_Kmeans3_T_Preenchido_Cluster2.csv']       
   if opcao == 10:       
   #   names = ['100Porcent_DF_29.csv','100Porcent_DF_30-39.csv','100Porcent_DF_40-49.csv','100Porcent_DF_50-59.csv','100Porcent_DF_60.csv','100Porcent_DF_29_Limpo.csv','100Porcent_DF_30-39_Limpo.csv','100Porcent_DF_40-49_Limpo.csv','100Porcent_DF_50-59_Limpo.csv','100Porcent_DF_60_Limpo.csv','Resultados_T_Filtrados_Kmeans3_Idade.csv','Resultados_T_Filtrados_Kmeans3_Idade_Cluster0.csv','Resultados_T_Filtrados_Kmeans3_Idade_Cluster1.csv','Resultados_T_Filtrados_Kmeans3_Idade_Cluster2_I.csv']       
       names = ['100Porcent_DF_29.csv','100Porcent_DF_30-39.csv','100Porcent_DF_40-49.csv','100Porcent_DF_50-59.csv','100Porcent_DF_60.csv','100Porcent_DF_29_Limpo.csv','100Porcent_DF_30-39_Limpo.csv','100Porcent_DF_40-49_Limpo.csv','100Porcent_DF_50-59_Limpo.csv','100Porcent_DF_60_Limpo.csv','Resultados_T_Filtrados_Kmeans3_Idade.csv','Resultados_T_Filtrados_Kmeans3_Idade_Cluster0.csv','Resultados_T_Filtrados_Kmeans3_Idade_Cluster1.csv','Resultados_T_Filtrados_Kmeans3_Idade_Cluster2.csv','Resultados_T_Filtrados_Kmeans3_Idade_Cluster2_Filtrados.csv']       
   if opcao == 11:
      names = ['Resultados_T_Filtrados_Kmeans3_Idade_Editado.csv', 'Resultados_T_Filtrados_Kmeans3_Idade_Preenchido.csv']
   return names
                                                                                                                                     
