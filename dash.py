import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from query import *
from datetime import datetime
from streamlit_modal import Modal

# Consultas iniciais nas duas tabelas do banco
query = "SELECT * FROM tb_registro"
memoria = ("SELECT * FROM tb_memoria")

df = conexao(query)
df_memoria = conexao(memoria)

df['tempo_registro'] = pd.to_datetime(df['tempo_registro'])  # Converter para datetime

if st.button("Atualizar dados"):     # Botão para atualização dos dados.
    df = conexao(query)

# Configuração do modal
modal = Modal(
    "Análise Inteligente",
    key="gemini-modal",
    padding=40,
    max_width=744
)

# Botão para abrir o modal
open_modal = st.button("Análise inteligente", icon='🤖')
if open_modal:
    modal.open()

# Configuração do conteúdo do modal
if modal.is_open():
    with modal.container():
        st.write("Digite sua pergunta sobre a base de dados...")
        user_input = st.text_area("Escreva algo aqui...", "")

        # Geração de conteúdo ao clicar em "Enviar"
        if st.button("Gerar análise"):
            if user_input.strip():
                try:
                    
                    prompt = user_input
                    
                    resposta_gemini = gerar_resposta_gemini(df, df_memoria, prompt)
                    
                    st.write("Resposta da análise:")
                    st.write(resposta_gemini) 
                              
                    # Armazena o novo prompt e resposta na memória
                    save_to_memory(prompt, resposta_gemini)

                    print("Resposta gerada pelo Gemini:")
                    print(resposta_gemini)
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro ao acessar gerar resposta: {e}")
            else:
                st.warning("Por favor, insira uma pergunta válida.")
        
        if st.button('Fechar'):
            modal.close()
            
# -------------------FIM DA APLICAÇÃO GEMINI ---------------------------------------------

# ****************************** MENU LATERAL ******************************

st.sidebar.image("images/logo.jpg", width=150)

st.sidebar.markdown(f'<h1 style="text-transform: uppercase;">{'Selecione a informação para gerar o gráfico'}</h1>', unsafe_allow_html=True)  

# Seleção da coluna X  |  selectbox ==> Cria uma caixa de seleção na barra lateral. 
colunaX = st.sidebar.selectbox(
    "Eixo X",
    options = ["umidade", "temperatura", "pressao", "altitude", "co2", "poeira", "tempo_registro"],
    index = 0
)

# Seleção da coluna Y  |  selectbox ==> Cria uma caixa de seleção na barra lateral. 
colunaY = st.sidebar.selectbox(
    "Eixo Y",
    options = ["umidade", "temperatura", "pressao", "altitude", "co2", "poeira", "tempo_registro"],
    index = 1
)

st.sidebar.subheader("Região")
SP = st.sidebar.checkbox("São Paulo", value=True)
ABC = st.sidebar.checkbox("Grade ABC", value=True)

if SP == False and ABC == False:
    st.sidebar.markdown(f'<p style="font-size:16px;font-weight:bold;background-color:#950606;display:flex;justify-content:center;padding:10px;border-radius:10px;">{"SELECIONE UMA REGIÃO!"}<p>', unsafe_allow_html=True)
    #st.sidebar.warning("Selecione uma região!")

# Lista de regiões selecionadas
regioes_selecionadas = []
if SP:
    regioes_selecionadas.append("São Paulo")
if ABC:
    regioes_selecionadas.append("Grande ABC")

# Filtrando o DataFrame com base nas regiões selecionadas
if regioes_selecionadas:
    df = df[df["regiao"].isin(regioes_selecionadas)]

# Verificar quais os atributos do filtro. 
def filtros(atributo):
    return atributo in [colunaX, colunaY]

# Filtro de RANGE ==> SLIDER
st.sidebar.header("Selecione o filtro")

# UMIDADE
if filtros("umidade"):
    umidade_range = st.sidebar.slider(
        "Umidade",
        min_value = float(df["umidade"].min()),  # Valor Mínimo.
        max_value = float(df["umidade"].max()),  # Valor Máximo.
        value = (float(df["umidade"].min()), float(df["umidade"].max())),  # Faixa de Valores selecionado.
        step = 0.1   # Incremento para cada movimento do slider.  
    )

# TEMPERATURA
if filtros("temperatura"):
    temperatura_range = st.sidebar.slider(
        "Temperatura (°C)",
        min_value = float(df["temperatura"].min()),  # Valor Mínimo.
        max_value = float(df["temperatura"].max()),  # Valor Máximo.
        value = (float(df["temperatura"].min()), float(df["temperatura"].max())),  # Faixa de Valores selecionado.
        step = 0.1   # Incremento para cada movimento do slider. 
    )

# PRESSÃO
if filtros("pressao"):
    pressao_range = st.sidebar.slider(
        "Pressao",
        min_value = float(df["pressao"].min()),  # Valor Mínimo.
        max_value = float(df["pressao"].max()),  # Valor Máximo.
        value = (float(df["pressao"].min()), float(df["pressao"].max())),  # Faixa de Valores selecionado.
        step = 0.1   # Incremento para cada movimento do slider. 
    )

# ALTITUDE
if filtros("altitude"):
    altitude_range = st.sidebar.slider(
        "Altitude",
        min_value = float(df["altitude"].min()),  # Valor Mínimo.
        max_value = float(df["altitude"].max()),  # Valor Máximo.
        value = (float(df["altitude"].min()), float(df["altitude"].max())),  # Faixa de Valores selecionado.
        step = 0.1   # Incremento para cada movimento do slider. 
    )

# CO2
if filtros("co2"):
    co2_range = st.sidebar.slider(
        "CO2",
        min_value = float(df["co2"].min()),  # Valor Mínimo.
        max_value = float(df["co2"].max()),  # Valor Máximo.
        value = (float(df["co2"].min()), float(df["co2"].max())),  # Faixa de Valores selecionado.
        step = 0.1   # Incremento para cada movimento do slider. 
    )

# POEIRA
if filtros("poeira"):
    poeira_range = st.sidebar.slider(
        "Poeira",
        min_value = float(df["poeira"].min()),  # Valor Mínimo.
        max_value = float(df["poeira"].max()),  # Valor Máximo.
        value = (float(df["poeira"].min()), float(df["poeira"].max())),  # Faixa de Valores selecionado.
        step = 0.1   # Incremento para cada movimento do slider. 
    )
## ************************************ FILTROS TEMPO_REGISTRO *************************************
if filtros("tempo_registro"):
    # Extrair as datas mínimas e máximas em formato de datetime
    min_data = df["tempo_registro"].min()
    max_data = df["tempo_registro"].max()

    # Exibir dois campos de data para seleção de intervalo no sidebar
    data_inicio = st.sidebar.date_input(
        "Data de Início", 
        min_data.date(), 
        min_value=min_data.date(), 
        max_value=max_data.date(),
        format= "DD-MM-YYYY"
    )
    
    data_fim = st.sidebar.date_input(
        "Data de Fim", 
        max_data.date(), 
        min_value=min_data.date(), 
        max_value=max_data.date(),
        format= "DD-MM-YYYY"
    )

    # Converter as datas selecionadas para datetime, incluindo hora
    tempo_registro_range = (
        pd.to_datetime(data_inicio),
        pd.to_datetime(data_fim) + pd.DateOffset(days=1) - pd.Timedelta(seconds=1)
    )

df_selecionado = df.copy()   # Cria uma copia do df original.:


if filtros("umidade"):
    df_selecionado = df_selecionado[
        (df_selecionado["umidade"] >= umidade_range[0]) &
        (df_selecionado["umidade"] <= umidade_range[1])
    ]

if filtros("temperatura"):
    df_selecionado = df_selecionado[
        (df_selecionado["temperatura"] >= temperatura_range[0]) &
        (df_selecionado["temperatura"] <= temperatura_range[1])
    ]

if filtros("pressao"):
    df_selecionado = df_selecionado[
        (df_selecionado["pressao"] >= pressao_range[0]) &
        (df_selecionado["pressao"] <= pressao_range[1])
    ]
    
if filtros("altitude"):
    df_selecionado = df_selecionado[
        (df_selecionado["altitude"] >= altitude_range[0]) &
        (df_selecionado["altitude"] <= altitude_range[1])
    ]

if filtros("co2"):
    df_selecionado = df_selecionado[
        (df_selecionado["co2"] >= co2_range[0]) &
        (df_selecionado["co2"] <= co2_range[1])
    ]

if filtros("poeira"):
    df_selecionado = df_selecionado[
        (df_selecionado["poeira"] >= poeira_range[0]) &
        (df_selecionado["poeira"] <= poeira_range[1])
    ] 

if filtros("tempo_registro"):
    df_selecionado = df_selecionado[
        (df_selecionado["tempo_registro"] >= tempo_registro_range[0]) &
        (df_selecionado["tempo_registro"] <= tempo_registro_range[1])
    ] 


# **************************** GRÁFICOS ****************************
    
def Home():
    with st.expander("Tabela"):
        mostrarDados = st.multiselect(
            "Filtro: ",
            df_selecionado.columns,
            default=[],
            key = "showData_home"
        )
        
        if mostrarDados:
            st.write(df_selecionado[mostrarDados])
    
    # Cálculos estatísticos
    if not df_selecionado.empty:
        media_umidade = df_selecionado["umidade"].mean()
        media_temperatura = df_selecionado["temperatura"].mean()
        media_co2 = df_selecionado["co2"].mean()\
        
        media1, media2, media3 = st.columns(3, gap="large")
        
        with media1: 
            st.info("Média de registros de Umidade", icon="📌")
            st.metric(label="Média", value=f"{media_umidade:.2f}")
        
        with media2:
            st.info("Média de registros de Temperatura (°C)", icon="📌")
            st.metric(label="Média", value=f"{media_temperatura:.2f}")
        
        with media3:
            st.info("Média de registros de CO2", icon="📌")
            st.metric(label="Média", value=f"{media_co2:.2f}")

# **************************** PLOTANDO GRÁFICOS ****************************
def graficos():
    st.title("Dashboard Monitoramento")
       
    aba1, aba2, aba3, aba4, aba5  = st.tabs(
        ["Gráfico de Barras",
        "Gráfico de Linhas",
        "Gráfico de Dispersão",
        "Gráfico de Área",
        "Gráfico de Barras Agrupado"]
        )
    
    with aba1:
        if df_selecionado.empty:
            st.write("Nenhum dado está disponível para gerar gráficos")
            return
        
        if colunaX == colunaY:
            st.warning("Selecione uma opção diferente para os eixos X e Y")
            return
        
        try:           
            grupo_dados1 = df_selecionado.groupby(by=[colunaX]).size().reset_index(name="contagem")
            fig_valores = px.bar(
                grupo_dados1,       # De onde vem os dados.
                x = colunaX,        # Eixo X
                y = "contagem",     # Eixo Y com o nome que nós renomeamos no GrupBy
                orientation = "v",  # Orientação do Gráfico
                title = f"Contagem de Registros por {colunaX.capitalize()}", # Titulo do gráfico => A função capitalize() deixa tudo em maiúsculo. 
                color_discrete_sequence = ["#0083b8"],       # Altera a cor 
                template = "plotly_white"
            )
            
        except Exception as e:
            st.error(f"Erro ao criar gráfico de barras:  {e}")
        st.plotly_chart(fig_valores, use_container_width=True)

    with aba2:
        if df_selecionado.empty:
            st.write("Nenhum dado está disponível para gerar gráficos")
            return

        if colunaX == colunaY:
            st.warning("Selecione uma opção diferente para os eixos X e Y")
            return

        try:
            grupo_dados2 = df_selecionado.groupby(by=[colunaX])[colunaY].mean().reset_index(name=colunaY)
            fig_valores2 = px.line(
                grupo_dados2,
                x=colunaX,
                y=colunaY,
                title=f"Gráfico de Linhas: {colunaX.capitalize()} vs {colunaY.capitalize()}",
                line_shape='linear',  # Tipo de linha
                markers=True  # Para mostrar marcadores nos pontos
            )
        except Exception as e:
            st.error(f"Erro ao criar gráfico de linhas: {e}")
        st.plotly_chart(fig_valores2, use_container_width=True)
 
    with aba3:
        if df_selecionado.empty:
            st.write("Nenhum dado está disponível para gerar gráficos")
            return

        if colunaX == colunaY:
            st.warning("Selecione uma opção diferente para os eixos X e Y")
            return

        try:
            grupo_dados3 = df_selecionado.groupby(by=[colunaX]).size().reset_index(name=colunaY)
            fig_valores3 = px.scatter(grupo_dados3, x = colunaX, y = colunaY)    
            
            st.plotly_chart(fig_valores3, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro ao criar gráfico de dispersão: {e}")
    
    with aba4:
        if df_selecionado.empty:
            st.write("Nenhum dado está disponível para gerar gráficos")
            return
        
        if colunaX == colunaY:
            st.warning("Selecione uma opção diferente para os eixos X e Y")
            return
        
        try:
            grupo_dados4 = df_selecionado.groupby(by=[colunaX]).size().reset_index(name=colunaY)
            st.area_chart(grupo_dados4, x = colunaX, y = colunaY, color= ["#0083b8"], stack="center" )

        except Exception as e:
            st.error(f"Erro ao criar gráfico de dispersão: {e}")
        
    with aba5:
        if df_selecionado.empty:
            st.write('Nenhum dado está disponível para gerar o gráfico')
            return
        
        if colunaX == colunaY:
            st.warning('Selecione uma opção diferente para os eixos X e Y')
            return
        
        try:
            grupo_dados5 = df_selecionado
            
            fig_barra = px.bar(grupo_dados5, 
                               x=colunaX,
                               y=colunaY,
                               color='regiao',
                               barmode='group',
                               title='Comparação entre regiões'
                               )
            
            st.plotly_chart(fig_barra, use_container_width=True)
            
        except Exception as e:
            print(f'Erro ao criar o gráfico: {e}')

# **************************** CHAMANDO A FUNÇÃO ****************************
Home()
if SP == ABC == False:
    st.warning("Nenhum dado encontrado para os filtros selecionados!")
else:
    graficos()