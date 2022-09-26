import streamlit as st
import pandas as pd
import numpy as np
from matplotlib.pyplot import scatter
import plotly.express as px 
import plotly.graph_objects as go
from joblib import dump, load

st.set_page_config(layout="wide")

genre = st.sidebar.radio(
     "Select Page",
     ('Data Description', 'Data Visualizations'))

if genre=='Data Description':
    """
    Title      :Assignment 3 - Streamlit
    
    Author     :Jean-Pierre Sakr     
    
    Course     :MSBA 325 - Data Visualization
    
    Instructor :Dr. Krzysztof Fleszar
    
    Due Date   :Tuesday, September 27, 2022, at 18:00     
    """
    st.header('Hotel Booking Reservations')    
    
    """    
    Data is available on Kaggle: https://www.kaggle.com/code/sanjana08/hotel-booking-cancellation-prediction/data
    
    The size of this dataset is of 119,390 rows and 32 columns, and the target variable is is_canceled (y-target). 
    
    This dataset contains a single file which compares various booking information between two hotels: a city hotel and a resort hotel.
    
    The aim behind this analysis is to predicted whether a hotel reservation will be canceled or confirmed.
    
    I replicated some visualizations in Streamlit, that were used previously in my Plotly Assignment, and I generated new 'interactive'
    visualizations that are in the next slide.
    
    """
    st.markdown("""
                > ##  I used the following type of visualizations:
                - Pie Chart to show the repartition of Hotel Booking Cancelations (1) and Confirmations (0).
                - Box Plot using a select box to show whether there is a correlation / relationship between lead time and adr with the
                  target variable.
                - 
                
                """) 
    
if genre=='Data Visualizations':    
    
       #Adding a title
       st.title('Hotel Booking Cancelations')
       #Importing the data
       def load_data(nrows):
           data = pd.read_csv('hotel_bookings.csv', nrows=nrows)
           lowercase = lambda x: str(x).lower()
           data.rename(lowercase, axis='columns', inplace=True)
           return data

       # Create a text element and let the reader know the data is loading.
       data_load_state = st.text('Loading data...')

       # Load 10,000 rows of data into the dataframe.
       data = load_data(10000)

       # Notify the reader that the data was successfully loaded.
       data_load_state.text("Done loading the data, please click on the below check box to see it!")

       #you can see the data through a check box
       if st.checkbox('Show raw data'):
          st.subheader('Raw data')
          st.write(data)

       col1, col2 = st.columns(2)

       #Draw a Pie Chart
       with col1:
           st.subheader('Repartition of Hotel Cancelations')
           is_canceled_labels = data['is_canceled'].value_counts().sort_values().keys()
           is_canceled_values = data['is_canceled'].value_counts().sort_values().values
           fig1 = go.Figure(data=[go.Pie(labels=is_canceled_labels, values=is_canceled_values, pull=[0, 0, 0.2, 0])])
           fig1.update_layout(height=550)
           st.plotly_chart(fig1)  
    
       #Draw a Scatter Plot
       with col2:
           st.subheader('Checking Some Correlations')
           box_plot_options = st.selectbox('Select Varialble', ['lead_time', 'adr'])
           fig2 = px.box(data, x="is_canceled", y=box_plot_options, color='is_canceled')
           st.plotly_chart(fig2)

if genre=='Data Visualizations':
    #Draw a Map
    df_country = pd.DataFrame(data['country'].value_counts())
    st.subheader(f'Repartition of Hotel Bookings over all countries')
    map = px.choropleth(df_country, locations=df_country.index, 
                    color=df_country['country'],
                    hover_name=df_country.index,
                    color_continuous_scale=px.colors.sequential.Turbo)
    st.write(map)

if genre=='Data Visualizations':
    col3, col4 = st.columns(2)
    #Draw a Histogram
    with col3:
        st.subheader('Number of Bookings by Day of the Month')
        #Use NumPy to generate a histogram that breaks down pickup times binned by hour:
        hist_values = np.histogram(data['arrival_date_day_of_month'], bins=32, range=(0,31))[0]
        st.bar_chart(hist_values)
    
    #Draw a Scatter Plot
    with col4:
           st.subheader('Leadtime vs Average Daily Rate')
           fig3 = px.scatter(data,color='adr', y='lead_time', x='adr')
           st.plotly_chart(fig3)
      
    #Draw a Line Graph
       
Resort_hotel = data[data['hotel'] == 'Resort Hotel']
City_hotel = data[data['hotel'] == 'City Hotel']

Resort_arrival_month = pd.DataFrame(Resort_hotel['arrival_date_month'].value_counts())
City_arrival_month = pd.DataFrame(City_hotel['arrival_date_month'].value_counts())

new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
Resort_arrival_month = Resort_arrival_month.reindex(new_order, axis=0, copy=False)
City_arrival_month = City_arrival_month.reindex(new_order, axis=0, copy=False)
    
if genre=='Data Visualizations':
    st.subheader('Monthly Distribution of Guests')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Resort_arrival_month.index, y=Resort_arrival_month['arrival_date_month'], name="Resort Hotel",
                         hovertext=Resort_arrival_month['arrival_date_month']))
    fig.add_trace(go.Scatter(x=City_arrival_month.index, y=City_arrival_month['arrival_date_month'], name="City Hotel",
                         hovertext=City_arrival_month['arrival_date_month']))
    fig.update_layout(xaxis_title="Arrival Month",
                      yaxis_title="Number of Guests",
                     title_x=0.5, title_font=dict(size=30))
    st.plotly_chart(fig)


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    