#Importing Libs
import pandas as pd
import numpy as np
import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go
# from streamlit_extras import addvertical_space as avs


#Changing the output format of numbers
def format(number):
    if number >= 1_000_000_000:
        formatted_number = f"{number / 1_000_000_000:.2f}B"
    elif number >= 1_000_000:
        formatted_number = f"{number / 1_000_000:.2f}M"
    elif number >= 1_000:
        formatted_number = f"{number / 1_000:.2f}K"
    else:
        formatted_number = f"{number:.2f}"

    # Add comma separation
    parts = formatted_number.split('.')
    integer_part = parts[0]
    decimal_part = parts[1] if len(parts) > 1 else ''
    
    if 'B' in integer_part:
        integer_part = integer_part.replace('B', '')
        suffix = 'B'
    elif 'M' in integer_part:
        integer_part = integer_part.replace('M', '')
        suffix = 'M'
    elif 'K' in integer_part:
        integer_part = integer_part.replace('K', '')
        suffix = 'K'
    else:
        suffix = ''
    
    integer_part = f"{int(integer_part):,}"

    return f"{integer_part}.{decimal_part}{suffix}"

st.set_page_config(page_title='Portfolio Analysis', page_icon=':mag:',layout='wide')

st.write("\n\n\n")
st.sidebar.write("\n\n\n")

#rad2 = st.radio("",["Data and Insights :mag:", "Sensitivity Analysis :chart_with_upwards_trend:"])

#Radio button to navigate between portfolios

rad = st.radio("Select portfolio to analyse : ",["PORT_USD", "PORT_EUR", "BOTH"], horizontal= True)
exchg_rt = 1.0668
#xls = pd.ExcelFile(r"C:\Users\ravis\Documents\GIT-GOOD\Portfolio_analysis\Portfolio_holdings.xlsx")
xls = pd.ExcelFile(r"Portfolio_holdings.xlsx")

port_eur = pd.read_excel(xls, 'PORT_EUR', skiprows=5)
port_usd = pd.read_excel(xls, 'PORT_USD', skiprows=5)





if rad == 'PORT_USD':
    grouping = st.sidebar.selectbox('Please select a grouping', ['None','Structure','MSCI ESG Rating','Fitch Rating','Moody\'s Rating','S&P Rating','Barclays Sub Sector','Barclays Industry','Barclays Sub Industry',	'Country Name'])
    st.write("All values are in ",":heavy_dollar_sign:")
    port_analyse = port_usd
    if grouping == 'None':
        #st.dataframe(port_analyse)
        st.write(port_analyse.head(5),f"Total Value:", format(port_analyse['Market Value'].sum()))
    else:
        fig = px.pie(port_analyse, values='Market Value', names=grouping, title='Market Value by each category')
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        st.plotly_chart(fig, use_container_width=True)
        for category in port_analyse[grouping].unique():
            st.write("\n", category, " : ",format(port_analyse[port_analyse[grouping]==category]['Market Value'].sum()))
        

if rad == 'PORT_EUR':
    grouping = st.sidebar.selectbox('Please select a grouping', ['None','Structure','MSCI ESG Rating','Fitch Rating','Moody\'s Rating','S&P Rating','Barclays Sub Sector','Barclays Industry','Barclays Sub Industry',	'Country Name'])
    st.write("All values are in Euro")
    port_analyse = port_eur
    if grouping == 'None':
        st.write(port_analyse.head(5),f"Total Value:", format(port_analyse['Market Value'].sum()))
    else:
        fig = px.pie(port_analyse, values='Market Value', names=grouping, title='Market Value by each category')
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        st.plotly_chart(fig, use_container_width=True)
        for category in port_analyse[grouping].unique():
            st.write("\n", category, " : ",format(port_analyse[port_analyse[grouping]==category]['Market Value'].sum()))
        

if rad == 'BOTH':
    grouping = st.sidebar.selectbox('Please select a grouping', ['None','Structure','MSCI ESG Rating','Fitch Rating','Moody\'s Rating','S&P Rating','Barclays Sub Sector','Barclays Industry','Barclays Sub Industry',	'Country Name'])
    st.write("All values are in ",":heavy_dollar_sign:")
    port_eur2 = port_eur
    port_eur2['Market Value'] = port_eur2['Market Value'] * exchg_rt
    port_analyse = pd.concat([port_eur2,port_usd], ignore_index=True)
    if grouping == 'None':
        st.write(port_analyse.head(5),f"Total Value:", format(port_analyse['Market Value'].sum()))
    else:
        fig = px.pie(port_analyse, values='Market Value', names=grouping, title='Market Value by each category')
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        st.plotly_chart(fig, use_container_width=True)
        for category in port_analyse[grouping].unique():
            st.write("\n", category, " : ",format(port_analyse[port_analyse[grouping]==category]['Market Value'].sum()))
        

# if rad == 'Compare':
#     st.write("All values are in ",":heavy_dollar_sign:")
#     port_eur2 = port_eur
#     port_usd2 = port_usd
#     port_eur2['Market Value'] = port_eur2['Market Value'] * exchg_rt
#     port_eur2['PORT'] = 'EUR'
#     port_usd2['PORT'] = 'USD'
#     port_analyse = pd.concat([port_eur2,port_usd2], ignore_index=True)
#     if grouping == 'None':
#         st.write(port_analyse.head(5), format(port_analyse['Market Value'].sum()))
#     else:
#         fig = px.pie(port_analyse, values='Market Value', names=grouping, title='Market Value by each category')
#         fig.update_traces(textposition='inside')
#         fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
#         st.plotly_chart(fig, use_container_width=True)
#         for portfolio in port_analyse['PORT'].unique():
#             st.write("\n", portfolio, " : ")
#             for category in port_analyse[grouping].unique():
#                 st.write("\n", category," : ",format(port_analyse[(port_analyse[grouping]==category)&(port_analyse['PORT']==portfolio)]['Market Value'].sum()))
        

#if rad2 == 'Data and Insights': TBC
    st.write("COMING UP!")

