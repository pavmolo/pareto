import streamlit as st
import pandas as pd
import plotly.express as px

def pareto_df(df):
    # Группируем по классам и суммируем значения
    df = df.groupby(df.columns[0]).sum().reset_index()
    
    # Сортируем данные по убыванию
    df = df.sort_values(by=df.columns[1], ascending=False)
    
    # Рассчитываем кумулятивный процент
    df['Cumulative Percentage'] = df[df.columns[1]].cumsum() / df[df.columns[1]].sum() * 100
    
    return df

def pareto_chart(df):
    fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Pareto Chart")
    
    # Добавляем линию кумулятивного процента
    fig.add_scatter(x=df[df.columns[0]], y=df['Cumulative Percentage'], mode='lines+markers', name='Cumulative Percentage')
    
    return fig

st.title("Pareto Analysis with Streamlit")

uploaded_file = st.file_uploader("Upload an excel file", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    
    if df.shape[1] != 2:
        st.error("Please ensure the Excel file has exactly two columns.")
    else:
        st.write("Uploaded Data:")
        st.write(df)
        
        pareto_data = pareto_df(df)
        
        st.write("Pareto Table:")
        st.write(pareto_data)
        
        st.write("Pareto Chart:")
        st.plotly_chart(pareto_chart(pareto_data))
