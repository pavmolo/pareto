import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def pareto_df(df):
    # Группируем по классам и суммируем значения
    df = df.groupby(df.columns[0]).sum().reset_index()
    
    # Сортируем данные по убыванию
    df = df.sort_values(by=df.columns[1], ascending=False)
    
    # Если классов больше 20, группируем оставшиеся в "Прочее"
    if len(df) > 20:
        other = df.iloc[20:].sum(numeric_only=True)
        other[df.columns[0]] = "Прочее"
        df = df.iloc[:20].append(other, ignore_index=True)
    
    # Рассчитываем кумулятивный процент
    df['Cumulative Percentage'] = df[df.columns[1]].cumsum() / df[df.columns[1]].sum() * 100
    
    return df

def pareto_chart(df):
    # Создаем фигуру с двумя осями Y
    fig = go.Figure()

    # Добавляем столбцы для основных данных
    fig.add_trace(go.Bar(x=df[df.columns[0]], y=df[df.columns[1]], name=df.columns[1]))

    # Добавляем линию кумулятивного процента на альтернативной оси Y
    fig.add_trace(go.Scatter(x=df[df.columns[0]], y=df['Cumulative Percentage'], mode='lines+markers', name='Cumulative Percentage', yaxis='y2'))

    # Настройка макета для использования двух осей Y
    fig.update_layout(
        yaxis=dict(title=df.columns[1]),
        yaxis2=dict(title='Cumulative Percentage', overlaying='y', side='right')
    )

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
