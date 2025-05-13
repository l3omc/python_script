# ---------------------------------------------
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go 

# streamlit run dashboard.py
# ----------------------------

# utilizando funcao para separar os arquivos em dias semanas, mes e ano 
def agrupando_dia_semana_mes_ano(dados):
    # verificando se o arquivo esta vazio
    if dados.empty:
        print("Nenhum dado disponível para agrupar.")
        return None, None, None,None


    # convertendo a coluna 'data' para datetime 
    dados['data'] = pd.to_datetime(dados['data'], errors='coerce', dayfirst=True)
    # Definindo o nome das colunas 
    operacoes = {
        "precipitacao_mm": "sum",  # Soma total da precipitação
        "pressao_estacao_mb": "mean",  # Média da pressão atmosférica
        "pressao_max_ant_mb": "max",  # Máxima pressão registrada
        "pressao_min_ant_mb": "min",  # Mínima pressão registrada
        "radiacao_global_kj": "sum",  # Radiação total acumulada
        "radiacao_global_wm2": "mean",  # Média da radiação
        "temp_bulbo_seco_c": "mean",  # Média da temperatura do ar
        "temp_orvalho_c": "mean",  # Média do ponto de orvalho
        "temp_max_ant_c": "max",  # Máxima temperatura registrada
        "temp_min_ant_c": "min",  # Mínima temperatura registrada
        "temp_orvalho_max_ant_c": "max",  # Máximo do ponto de orvalho
        "temp_orvalho_min_ant_c": "min",  # Mínimo do ponto de orvalho
        "umidade_max_ant": "max",  # Máxima umidade do ar
        "umidade_min_ant": "min",  # Mínima umidade do ar
        "umidade_relativa": "mean",  # Média da umidade do ar
        "vento_direcao": "median",  # Mediana da direção do vento
        "vento_rajada_max_ms": "max",  # Máxima rajada de vento
        "vento_velocidade_ms": "mean",  # Média da velocidade do vento
    }
    
    # realizando os groupby 
    dados_diarios = dados.groupby(dados['data'].dt.date).agg(operacoes).reset_index()
    dados_semana = dados.groupby(dados["data"].dt.strftime('%Y-%U')).agg(operacoes).reset_index() # dt.strftime('%Y-%U')
    dados_mes = dados.groupby(dados["data"].dt.to_period("M")).agg(operacoes).reset_index()
    dados_mes['data'] = dados_mes['data'].dt.start_time 

    dados_anuais = dados.groupby(dados["data"].dt.to_period("Y")).agg(operacoes).reset_index()
    dados_anuais['data'] = dados_anuais['data'].dt.start_time


  # Formatando para 2 casas decimais
    dados_diarios = dados_diarios.round(2)
    dados_anuais = dados_anuais.round(2)
    dados_semana = dados_semana.round(2)
    dados_mes = dados_mes.round(2)

    return dados_diarios, dados_semana, dados_mes, dados_anuais

# arrumar pelo nome que está no arquivo. 
arquivos = pd.read_csv('A882_TEUTONIA.csv', sep = ';', encoding='latin1', skiprows=8, header = 0 )
# arquivos.head()

diario,semanal, mensal, anual = agrupando_dia_semana_mes_ano(arquivos)

# ALTERANDO NOME E TIPO DE LAYOYT DO STREAMLIT
st.set_page_config( 
    page_title ="Dashboard dados estações do municipio",
    layout ="wide",
    initial_sidebar_state = "expanded"    

    )
# Streamlit layout
st.title(":blue[Dashboard]")
st.header(f"dados meteorologicos :red[Teutonia]")

# Criando 3 colunas
col1, col2, col3 = st.columns(3)

#  criando colunas  para os dados, fica parecendo um carrossel 
tab1, tab2, tab3,tab4 = st.tabs(["Diário", "Semanal", "Mensal", "Anual"])
# tab1.write("Média Diária")
# tab2.write("Média Semanal")
# tab3.write("Média Mensal")
# tab4.write("Média Anual")

# GERANDO OS PLOTS EM CADA MEDIA DE DADO METEOROLOGICO
with tab1: # DIÁRIO 
# --------------------------------------------------------------
     # GRAFICO 1
    st.header("Dados Diários - Temperatura do Ar")
    diario['data'] = pd.to_datetime(diario['data'])
    
    fig = go.Figure()  # 0

    fig.add_trace(go.Scatter(
        x=diario['data'],
        y=diario['temp_bulbo_seco_c'],
        name='Temperatura Média',
        mode='lines+markers'
    ))
    fig.add_trace(go.Scatter(
        x=diario['data'],
        y=diario['temp_max_ant_c'],
        name='Temperatura Máxima',
        mode='markers'
    ))
    fig.add_trace(go.Scatter(
        x=diario['data'],
        y=diario['temp_min_ant_c'],
        name='Temperatura Minima',
        mode='markers'
    ))

    # layout:
    fig.update_layout(
        title="Variação Diária da Temperatura",
        xaxis_title="Data",
        yaxis_title="Temperatura (°C)",
        legend_title="Variáveis"
    )

    st.plotly_chart(fig, use_container_width=True)      
# --------------------------------------------------------------    
    
# --------------------------------------------------------------
    # GRAFICO 2 
    st.header("Precipitação acumulada diária")
   
    #  diario['data'] = pd.to_datetime(diario['data'])
        
    # Criando gráfico 
    fig = px.line(
        diario, 
        x='data', 
        y="precipitacao_mm", 
        markers=True,
        title="Precipitação acumulada (mm)"
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="precipitacao_mm",
        xaxis=dict(tickangle=45)
    )
         # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------------------
# --------------------------------------------------------------
    # GRAFICO 3 
    st.header("Temperatura do orvalho (°C)")
    #  diario['data'] = pd.to_datetime(diario['data'])
    
    fig = px.line(
        diario, 
        x='data', 
        y="temp_orvalho_c", 
        markers=True,
        title=" Temperatura Orvalho(°C)"
    )
        # Ajustar layout
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="temp_orvalho_c",
        xaxis=dict(tickangle=45)
    )
         # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------------------
# --------------------------------------------------------------
    # GRAFICO 4
    st.header(" Umidade Relativa (%)")
    #  diario['data'] = pd.to_datetime(diario['data'])
    
    fig = px.line(
        diario, 
        x='data', 
        y="umidade_relativa", 
        markers=True,
        title="Umidade Relativa (%)"
    )
        # Ajustar layout
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="umidade_relativa",
        xaxis=dict(tickangle=45)
    )
         # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------------------
# --------------------------------------------------------------
     # GRAFICO 4
    st.header("Umidade relativa do Ar")
    # diario['data'] = pd.to_datetime(diario['data'])
    
    fig = go.Figure()  # 0
    fig.add_trace(go.Scatter(
        x=diario['data'],
        y=diario["umidade_relativa"],
        name='Umidade relativa Média',
        mode='lines+markers'
    ))
    fig.add_trace(go.Scatter(
        x=diario['data'],
        y=diario["umidade_max_ant"],
        name="umidade_maxima",
        mode='markers'
    ))
    fig.add_trace(go.Scatter(
        x=diario['data'],
        y=diario["umidade_min_ant"],
        name="umidade_minima",
        mode='markers'
    ))
    fig.update_layout(
        title="umidade relativa ",
        xaxis_title="Data",
        yaxis_title=" (%)",
        legend_title="Variáveis"
    )

    st.plotly_chart(fig, use_container_width=True)      
# --------------------------------------------------------------  
with tab2: # SEMANAL 
    # --------------------------------------------------------------  
    # grafico 1     
    st.header("Dados medias semanais - Temperatura do Ar")
    fig = px.line(
        semanal, 
        x='data', 
        y='temp_bulbo_seco_c', 
        markers=True,
        title="Variação Diária da Temperatura"
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Temperatura (°C)",
        xaxis=dict(tickangle=45)
    )
    
    st.plotly_chart(fig, use_container_width=True)
        
# --------------------------------------------------------------
    # GRAFICO 2 
    st.header("Precipitação acumulada diária")
    fig = px.line(
        semanal, 
        x='data', 
        y="precipitacao_mm", 
        markers=True,
        title="Precipitação acumulada (mm)"
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="precipitacao_mm",
        xaxis=dict(tickangle=45)
    )
         # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------------------
# --------------------------------------------------------------
    # GRAFICO 3 
    st.header("Temperatura do orvalho (°C)")
    fig = px.line(
        semanal, 
        x='data', 
        y="temp_orvalho_c", 
        markers=True,
        title=" Temperatura Orvalho(°C)"
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="temp_orvalho_c",
        xaxis=dict(tickangle=45)
    )
         # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------------------
# --------------------------------------------------------------
    # GRAFICO 4
    st.header(" Umidade Relativa (%)")
    fig = px.line(
        semanal, 
        x='data', 
        y="umidade_relativa", 
        markers=True,
        title="Umidade Relativa (%)"
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="umidade_relativa",
        xaxis=dict(tickangle=45)
    )
    st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------------------
# --------------------------------------------------------------
     # GRAFICO 5
    st.header("Umidade relativa do Ar")
    fig = go.Figure()  # 0
    fig.add_trace(go.Scatter(
        x=semanal['data'],
        y=semanal["umidade_relativa"],
        name='Umidade relativa Média',
        mode='lines+markers'
    ))
    fig.add_trace(go.Scatter(
        x=semanal['data'],
        y=semanal["umidade_max_ant"],
        name="umidade_maxima",
        mode='markers'
    ))
    fig.add_trace(go.Scatter(
        x=semanal['data'],
        y=semanal["umidade_min_ant"],
        name="umidade_minima",
        mode='markers'
    ))
    fig.update_layout( # criando titulos do grafico e eixos
        title="umidade relativa ",
        xaxis_title="Data",
        yaxis_title=" (%)",
        legend_title="Variáveis"
    )

    st.plotly_chart(fig, use_container_width=True)      
# --------------------------------------------------------------  
with tab3: # MENSAL 
# --------------------------------------------------------------
    st.header("Médias Mensal - Temperatura do Ar")
    fig = px.line(
        mensal, 
        x='data', 
        y='temp_bulbo_seco_c', 
        markers=True,
        title="Variação Diária da Temperatura"
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Temperatura (°C)",
        xaxis=dict(tickangle=45)
    )
    st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------------------
    # GRAFICO 2 
    st.header("Precipitação acumulada diária")
    fig = px.line(
        mensal, 
        x='data', 
        y="precipitacao_mm", 
        markers=True,
        title="Precipitação acumulada (mm)"
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="precipitacao_mm",
        xaxis=dict(tickangle=45)
    )
         # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------------------
# --------------------------------------------------------------
    # GRAFICO 3 
    st.header("Temperatura do orvalho (°C)")
    fig = px.line(
        mensal, 
        x='data', 
        y="temp_orvalho_c", 
        markers=True,
        title=" Temperatura Orvalho(°C)"
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="temp_orvalho_c",
        xaxis=dict(tickangle=45)
    )
         # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------------------
# --------------------------------------------------------------
    # GRAFICO 4
    st.header(" Umidade Relativa (%)")
    fig = px.line(
        mensal, 
        x='data', 
        y="umidade_relativa", 
        markers=True,
        title="Umidade Relativa (%)"
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="umidade_relativa",
        xaxis=dict(tickangle=45)
    )
    st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------------------
# --------------------------------------------------------------
     # GRAFICO 5
    st.header("Umidade relativa do Ar")
    fig = go.Figure()  # 0
    fig.add_trace(go.Scatter(
        x=mensal['data'],
        y=mensal["umidade_relativa"],
        name='Umidade relativa Média',
        mode='lines+markers'
    ))
    fig.add_trace(go.Scatter(
        x=mensal['data'],
        y=mensal["umidade_max_ant"],
        name="umidade_maxima",
        mode='markers'
    ))
    fig.add_trace(go.Scatter(
        x=mensal['data'],
        y=mensal["umidade_min_ant"],
        name="umidade_minima",
        mode='markers'
    ))
    fig.update_layout( # criando titulos do grafico e eixos
        title="umidade relativa ",
        xaxis_title="Data",
        yaxis_title=" (%)",
        legend_title="Variáveis"
    )

    st.plotly_chart(fig, use_container_width=True)      
# -------------------------------------------------------------- 
with tab4: # ANUAL 
    st.header("Dados medias semanais - Temperatura do Ar")
    fig = px.line(
        anual, 
        x='data', 
        y='temp_bulbo_seco_c', 
        markers=True,
        title="Variação Diária da Temperatura"
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Temperatura (°C)",
        xaxis=dict(tickangle=45)
    )
        
        # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)
   # --------------------------------------------------------------
    # GRAFICO 2 
    st.header("Precipitação acumulada diária")
    fig = px.line(
        anual, 
        x='data', 
        y="precipitacao_mm", 
        markers=True,
        title="Precipitação acumulada (mm)"
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="precipitacao_mm",
        xaxis=dict(tickangle=45)
    )
         # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------------------
# --------------------------------------------------------------
    # GRAFICO 3 
    st.header("Temperatura do orvalho (°C)")
    fig = px.line(
        anual, 
        x='data', 
        y="temp_orvalho_c", 
        markers=True,
        title=" Temperatura Orvalho(°C)"
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="temp_orvalho_c",
        xaxis=dict(tickangle=45)
    )
         # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------------------
# --------------------------------------------------------------
    # GRAFICO 4
    st.header(" Umidade Relativa (%)")
    fig = px.line(
        anual, 
        x='data', 
        y="umidade_relativa", 
        markers=True,
        title="Umidade Relativa (%)"
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="umidade_relativa",
        xaxis=dict(tickangle=45)
    )
    st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------------------
# --------------------------------------------------------------
     # GRAFICO 5
    st.header("Umidade relativa do Ar")
    fig = go.Figure()  # 0
    fig.add_trace(go.Scatter(
        x=anual['data'],
        y=anual["umidade_relativa"],
        name='Umidade relativa Média',
        mode='lines+markers'
    ))
    fig.add_trace(go.Scatter(
        x=anual['data'],
        y=anual["umidade_max_ant"],
        name="umidade_maxima",
        mode='markers'
    ))
    fig.add_trace(go.Scatter(
        x=anual['data'],
        y=anual["umidade_min_ant"],
        name="umidade_minima",
        mode='markers'
    ))
    fig.update_layout( # criando titulos do grafico e eixos
        title="umidade relativa ",
        xaxis_title="Data",
        yaxis_title=" (%)",
        legend_title="Variáveis"
    )

    st.plotly_chart(fig, use_container_width=True)      
# -------------------------------------------------------------- 