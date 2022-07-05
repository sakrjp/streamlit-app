from matplotlib.pyplot import scatter
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import plotly.graph_objects as go


df = pd.read_csv('df_cleaned.csv')

st.header('Liver Cirrhosis Stage Prediction')
st.subheader('Distribution by Stage')

# stage distribution
stage_labels = df['Stage'].value_counts().sort_values().keys()
stage_values = df['Stage'].value_counts().sort_values().values
fig1 = go.Figure(data=[go.Pie(labels=stage_labels, values=stage_values, pull=[0, 0, 0.2, 0])])
st.plotly_chart(fig1)

st.subheader('Patients\' Age over Stages')
box_plot_options = st.selectbox('Select Varialble', ['Age', 'N_Days'])

fig2 = px.box(df, x="Stage", y=box_plot_options, color='Stage')
st.plotly_chart(fig2)

## status x stage
st.subheader('Repartition of Censored and Dead Patients in Each Stage')
df1 = df[['Stage', 'Status', 'ID']].groupby(['Stage', 'Status']).count().reset_index()
df1['Stage'] = df1['Stage'].astype(str)

fig3 = px.bar(df1, x="Status", y="ID",
             color='Stage', barmode='group',
             height=400)
st.plotly_chart(fig3)

## scatter plot 1: Cholesterol, Copper and Albumin over stages
st.subheader('Distribution of Cholesterol, Copper and Albumin Over Stages')
scatter_plot_options_1 = st.selectbox('Select Variable', ['Cholesterol', 'Copper', 'Albumin'])
fig4 = px.scatter(df,color='Stage', y=scatter_plot_options_1, x='Stage')
st.plotly_chart(fig4)

## scatter plot 2: Albumin vs N_Days
st.subheader('Variation of Albumin over Time')
fig5 = px.scatter(df, y='Albumin', x='N_Days', trendline='lowess', trendline_color_override='black', color='Albumin')
st.plotly_chart(fig5)

st.header('Comparing Stage 1 to Stage 4')
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

st.plotly_chart(fig6)

## status x stage
st.subheader('Presence of Ascites, Spiders and Hepatomegaly for Stage 1 and Stage 4 Patients')
options = st.selectbox('Select Variable', ['Ascites','Spiders', 'Hepatomegaly'])
df4 = df[['Stage', options, 'ID']][(df['Stage']==1) | (df['Stage']==4)].groupby([options,'Stage']).count().reset_index()
df4['Stage'] = df4['Stage'].astype(str)

fig3 = px.bar(df4, x="Stage", y="ID",
             color=options, barmode='group',
             height=400)
st.plotly_chart(fig3)

