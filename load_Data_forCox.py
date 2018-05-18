def load_Data_forCox():

    """ Function that loads data for the three matrix needed:
        X containing the clinical, images, Immunoscore DATA
        Y the survival time
        delta the censure status
        open the file for precision about the clinical data available,drop the not-needed ones in the notebook
        cleaning of data consists of deleting the clinical data having only one level when categorical
        """

    import os
    import pandas
    import numpy

        #pathway to the folder containing all the datas
    SAVE_CLI_PATH=os.path.join('..')

        #List of usable patients
    data_ID=pandas.read_csv(os.path.join('..','List_Patient_HEGP.csv'),sep=",")

    #### GENERATING THE X MATRIX ####

    # Data theoreticaly available can be found in file : Immunoscore Clinical Data and Formating Requirements 10.2.2015.xlsx

    # In practice not all the columns are filled, for different reason, one is that the information does not apply to the cohort, so the whole of the column is empty.

    # And for ethical reason, the column race is always ignored.
    # Other columns ignored are the ones pertaining to:
    #    the dates of possible undergone surgeries
    #    the Survival data
    #    the additional markers, text not usable in a survival study

    # Some of the data is categorical, from 2 to 6 different categories (not counting missing information)
    # Missing data is represented by an empty cell in the original file

                    #the immunoscore
    Data_IS_MDT=pandas.read_csv(os.path.join('../Data_output','HEGP_Immunoscore_mean.csv'),sep=',')
                    #Clinical data, only requested columns
    data_cl=pandas.read_csv(os.path.join('../Data_output','data_HEGP_Clinical.txt'),sep=';')
    col_names=['OfficialID','gender','age','t_stage_mod_6is4_7is1','n_stage','plnode','m_stage','UICC_TNM','preop_chemo','postop_chemo','postop_biotherapy','surg_pt_type','nlnode','plnode','colon','sidedness','cecum','ascending','splenflex','transverse','hepflex','descending','sigmoid','immuno_tx','differentiation','mucinous_colloide','occlusion','perforation','venous_emboli','lymphatic_invasion','perineural_invasion','msi_ihc','msi_gen','lynch_syndrome','fap','ibs','tumor_budding','cimp','p53_status','kras_status','apc_status','braf_status','pi3k_status','MSI_NBP','CD3_Tumor_Density','CD3_IM_Density','CD8_Tumor_Density','CD8_IM_Density','Immunoscore']
    df_final=pandas.DataFrame(data=data_cl[['OfficialID','gender','age','t_stage_mod_6is4_7is1','n_stage','plnode','m_stage','UICC_TNM','preop_chemo','postop_chemo','postop_biotherapy',
        'surg_pt_type','nlnode','plnode','colon','sidedness','cecum','ascending','splenflex','transverse','hepflex','descending',
        'sigmoid','immuno_tx','differentiation','mucinous_colloide','occlusion','perforation','venous_emboli','lymphatic_invasion','perineural_invasion',
        'msi_ihc','msi_gen','lynch_syndrome','fap','ibs','tumor_budding','cimp','p53_status','kras_status','apc_status','braf_status','pi3k_status','MSI_NBP']])

    df_final.set_index('OfficialID',inplace=True,drop=False)
    Data_IS_MDT.set_index('OfficialID',drop=False,inplace=True)


        #Clinical data for the usable patient, other are droped
    data_ID['OfficialID']
    df_final=df_final.merge(data_ID,on='OfficialID')
    df_final.set_index('OfficialID',inplace=True,drop=False)

        #getting the density and immunoscore of the usable patients in their own dataFrame, with always the OfficialID for safety
    df_CD3_CT=pandas.DataFrame(columns=['OfficialID','CD3_Tumor_Density'])
    df_CD3_IM=pandas.DataFrame(columns=['OfficialID','CD3_IM_Density'])
    df_CD8_CT=pandas.DataFrame(columns=['OfficialID','CD8_Tumor_Density'])
    df_CD8_IM=pandas.DataFrame(columns=['OfficialID','CD8_IM_Density'])
    df_IS=pandas.DataFrame(columns=['OfficialID','Immunoscore'])
    for patient_id in list(data_ID['OfficialID']):

        CD3PATH=os.path.join(SAVE_CLI_PATH,'Data_output','cache_HEGP','cd3',patient_id)
        CD8PATH=os.path.join(SAVE_CLI_PATH,'Data_output','cache_HEGP','cd8',patient_id)

        df=pandas.DataFrame(data=[[patient_id,[pandas.read_csv(os.path.join(CD3PATH,'Ratio_Cells_per_Tumor'),sep=' ',header=None)]]],columns=['OfficialID','CD3_Tumor_Density'])
        df_CD3_CT=df_CD3_CT.append(df)
        df=pandas.DataFrame(data=[[patient_id,[pandas.read_csv(os.path.join(CD3PATH,'Ratio_Cells_per_InvasiveFront'),sep=' ',header=None)]]],columns=['OfficialID','CD3_IM_Density'])
        df_CD3_IM=df_CD3_IM.append(df)

        df=pandas.DataFrame(data=[[patient_id,[pandas.read_csv(os.path.join(CD8PATH,'Ratio_Cells_per_Tumor'),sep=' ',header=None)]]],columns=['OfficialID','CD8_Tumor_Density'])
        df_CD8_CT=df_CD8_CT.append(df)
        df=pandas.DataFrame(data=[[patient_id,[pandas.read_csv(os.path.join(CD8PATH,'Ratio_Cells_per_InvasiveFront'),sep=' ',header=None)]]],columns=['OfficialID','CD8_IM_Density'])
        df_CD8_IM=df_CD8_IM.append(df)
        df=pandas.DataFrame(data=[[patient_id,Data_IS_MDT.at[patient_id,'IS_MDT']]],columns=['OfficialID','Immunoscore'])
        df_IS=df_IS.append(df)

        # Merging the dataFrame, based on OfficialID
    df_final=df_final.merge(df_CD3_CT,on='OfficialID')
    df_final=df_final.merge(df_CD3_IM,on='OfficialID')
    df_final=df_final.merge(df_CD8_CT,on='OfficialID')

    df_final=df_final.merge(df_CD8_IM,on='OfficialID')
    df_final=df_final.merge(df_IS,on='OfficialID')

        #Setting the index on the final DataFrame, patient id.
    df_final.set_index('OfficialID',inplace=True,drop=True)
    colTypes = pandas.read_csv('datatypes.csv',sep=',')
    #Iterate through each row and assign variable type.
    #Note: astype is used to assign types

    for i, row in colTypes.iterrows():  #i: dataframe index; row: each row in series format
        if row['type']=="categorical":
            df_final[row['feature']]=df_final[row['feature']].astype(numpy.object)
        elif row['type']=="continuous":
            df_final[row['feature']]=df_final[row['feature']].astype(numpy.float)


    #### GENERATING Y and Delta ####

        #Survival data
    data_Survival=pandas.read_csv(os.path.join('../Data_output','data_HEGP_Survival.txt'),sep=";")

    # We are looking here at the TTR, Time To Relapse.
    # The event is the relapse.
    # In the file,rc_stat: 1 means relapse has occured
    # time in TTR_2012_Days.
    #    output: time dataframe index on OfficialID time in TTR_2012_Days.

    #    output: censure dataframe index on Official ID


    data_TTR=pandas.DataFrame(data=data_Survival[['OfficialID','TTR_2012_Days','rc_stat']])
    data_TTR.set_index('OfficialID',inplace=True,drop=False)
    #Selecting only usable patients
    data_ID['OfficialID']
    data_TTR=data_TTR.merge(data_ID,on='OfficialID')
    data_TTR.set_index('OfficialID',inplace=True,drop=False)

    data_time=pandas.DataFrame(data=data_TTR[['OfficialID','TTR_2012_Days']])
    data_time.set_index('OfficialID',inplace=True,drop=True)

    data_cens=pandas.DataFrame(data=data_TTR[['OfficialID','rc_stat']])
    data_cens.set_index('OfficialID',inplace=True,drop=True)


    return df_final,data_time,data_cens
