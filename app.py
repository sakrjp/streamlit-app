from matplotlib.pyplot import scatter
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import plotly.graph_objects as go
from joblib import dump, load


st.set_page_config(layout="wide")

genre = st.sidebar.radio(
     "Select Page",
     ('Data Description', 'EDA', 'Predictions'))


if genre=='Data Description':
    st.header('Liver Cirrhosis Stage Prediction')
    st.image('logo.jpg')
    st.subheader('Data Source & Description') 
    """
    Data is available on Kaggle: https://www.kaggle.com/fedesoriano/cirrhosis-prediction-dataset

    Cirrhosis is a late stage of scarring (fibrosis) of the liver caused by many forms of liver diseases and conditions, such as hepatitis and chronic alcoholism. The following data contains the information collected from the Mayo Clinic trial in primary biliary cirrhosis (PBC) of the liver conducted between 1974 and 1984. A description of the clinical background for the trial and the covariates recorded here is in Chapter 0, especially Section 0.2 of Fleming and Harrington, Counting
    Processes and Survival Analysis, Wiley, 1991. A more extended discussion can be found in Dickson, et al., Hepatology 10:1-7 (1989) and in Markus, et al., N Eng J of Med 320:1709-13 (1989).

    A total of 424 PBC patients, referred to Mayo Clinic during that ten-year interval, met eligibility criteria for the randomized placebo-controlled trial of the drug D-penicillamine. The first 312 cases in the dataset participated in the randomized trial and contain largely complete data. The additional 112 cases did not participate in the clinical trial but consented to have basic measurements recorded and to be followed for survival. Six of those cases were lost to follow-up shortly after diagnosis, so the data here are on an additional 106 cases as well as the 312 randomized participants.

    Attribute Information
    1) ID: unique identifier
    2) N_Days: number of days between registration and the earlier of death, transplantation, or study analysis time in July 1986
    3) Status: status of the patient C (censored), CL (censored due to liver tx), or D (death)
    4) Drug: type of drug D-penicillamine or placebo
    5) Age: age in [days]
    6) Sex: M (male) or F (female)
    7) Ascites: presence of ascites N (No) or Y (Yes)
    8) Hepatomegaly: presence of hepatomegaly N (No) or Y (Yes)
    9) Spiders: presence of spiders N (No) or Y (Yes)
    10) Edema: presence of edema N (no edema and no diuretic therapy for edema), S (edema present without diuretics, or edema resolved by diuretics), or Y (edema despite diuretic therapy)
    11) Bilirubin: serum bilirubin in [mg/dl]
    12) Cholesterol: serum cholesterol in [mg/dl]
    13) Albumin: albumin in [gm/dl]
    14) Copper: urine copper in [ug/day]
    15) Alk_Phos: alkaline phosphatase in [U/liter]
    16) SGOT: SGOT in [U/ml]
    17) Triglycerides: triglicerides in [mg/dl]
    18) Platelets: platelets per cubic [ml/1000]
    19) Prothrombin: prothrombin time in seconds [s]
    20) Stage: histologic stage of disease (1, 2, 3, or 4)
    """


if genre=='EDA':
    df = pd.read_csv('df_cleaned.csv')

    col1, col2 = st.columns(2)

    with col1:
        # stage distribution
        st.subheader('Distribution by Stage')
        stage_labels = df['Stage'].value_counts().sort_values().keys()
        stage_values = df['Stage'].value_counts().sort_values().values
        fig1 = go.Figure(data=[go.Pie(labels=stage_labels, values=stage_values, pull=[0, 0, 0.2, 0])])
        fig1.update_layout(height=550)
        st.plotly_chart(fig1)

    with col2:
        st.subheader('Patients\' Age over Stages')
        box_plot_options = st.selectbox('Select Varialble', ['Age', 'N_Days'])
        fig2 = px.box(df, x="Stage", y=box_plot_options, color='Stage')
        st.plotly_chart(fig2)

    st.subheader('Repartition of Censored and Dead Patients in Each Stage')
    col7, col8, col9 = st.columns(3)

    with col8:
        ## status x stage
        
        df1 = df[['Stage', 'Status', 'ID']].groupby(['Stage', 'Status']).count().reset_index()
        df1['Stage'] = df1['Stage'].astype(str)

        fig3 = px.bar(df1, x="Status", y="ID",
                    color='Stage', barmode='group',
                    height=400)
        fig3.update_layout(
    margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig3)


    col5, col6 = st.columns(2)

    with col5:
        ## scatter plot 1: Cholesterol, Copper and Albumin over stages
        st.subheader('Distribution of Cholesterol, Copper and Albumin Over Stages')
        scatter_plot_options_1 = st.selectbox('Select Variable', ['Cholesterol', 'Copper', 'Albumin'])
        fig4 = px.scatter(df,color='Stage', y=scatter_plot_options_1, x='Stage')
        st.plotly_chart(fig4)
    with col6:
        ## scatter plot 2: Albumin vs N_Days
        st.subheader('Variation of Albumin over Time')
        fig5 = px.scatter(df, y='Albumin', x='N_Days', trendline='lowess', trendline_color_override='white', color='Albumin')

        fig5.update_layout(height=600)

        st.plotly_chart(fig5)

    st.title('Comparing Stage 1 to Stage 4')

    col3, col4 = st.columns(2)

    with col3:
        st.subheader('Volume of SGOT in Stage 1 and Stage 4')
        # bubble chart
        dff = df[(df['Stage']==1) | (df['Stage']==4)]
        dff['Stage'] = dff['Stage'].astype(str)
        dff = dff[['SGOT', 'Stage']].groupby('Stage').mean().reset_index()
        dff['Stage'] = dff['Stage'].rename({'1':'Stage 1', '4':'Stage 4'})

        fig6 = go.Figure(data=[go.Scatter(
            x=dff['Stage'], y=[10, 15],
            mode='markers',
            marker=dict(
                color=['rgb(106, 13, 173)', 'rgb(255, 255, 0)'],
                size=dff['SGOT'],
            )
        )])
        fig6.update_layout(height=550)
        st.plotly_chart(fig6)
    with col4:
        ## status x stage
        st.subheader('Presence of Ascites, Spiders and Hepatomegaly for Stage 1 and Stage 4 Patients')
        options = st.selectbox('Select Variable', ['Ascites','Spiders', 'Hepatomegaly'])
        df4 = df[['Stage', options, 'ID']][(df['Stage']==1) | (df['Stage']==4)].groupby([options,'Stage']).count().reset_index()
        df4['Stage'] = df4['Stage'].astype(str)

        fig3 = px.bar(df4, x="Stage", y="ID",
                    color=options, barmode='group',
                    height=400)
        st.plotly_chart(fig3)

    
if genre=='Predictions':
    st.header('Random Forest Classifier to Predict the Stage')
    ## prediction models
    uploaded_files = st.file_uploader("Choose a CSV file")

    if uploaded_files:
        dfp = pd.read_csv(uploaded_files)

        # binary encoding
        dfp['Ascites'] = dfp['Ascites'].map({'Y':1, 'N':0})
        dfp['Hepatomegaly'] = dfp['Hepatomegaly'].map({'Y':1, 'N':0})
        dfp['Spiders'] = dfp['Spiders'].map({'Y':1, 'N':0})
        dfp['Drug'] = dfp['Drug'].map({'D-penicillamine':1, 'Placebo':0})
        dfp['Sex'] = dfp['Sex'].map({'M':1, 'F':0})

        #one hot encoding
        dfp = dfp.join(pd.get_dummies(dfp['Edema'], prefix='Edema'))
        dfp = dfp.join(pd.get_dummies(dfp['Status'], prefix='Status'))
        dfp = dfp.drop(columns = ['Edema', 'Status'])

        features = ['N_Days', 'Drug', 'Age', 'Sex', 'Ascites', 'Hepatomegaly', 'Spiders',
        'Bilirubin', 'Cholesterol', 'Albumin', 'Copper', 'Alk_Phos', 'SGOT',
        'Tryglicerides', 'Platelets', 'Prothrombin', 'Edema_N', 'Edema_S',
        'Edema_Y', 'Status_C', 'Status_CL', 'Status_D']

        for elem in features:
            if elem not in dfp.columns:
                dfp[elem]=0
            else:
                pass

        clf = load('model.joblib') 

        predictions = clf.predict(dfp)

        st.write("Your Cirrhosis Stage is: ", predictions[0])
    """
    Model 1 is a Random Forest Classifier built on all clinical features with a accuracy of 50%. Let's try to predict the cyrrhosis stage of a anonymous patient.
    """
        