import pandas as pd
import streamlit as st
import time
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Índice Futuro - Posições", layout="wide")

st.title("📊 Evolução no Tempo - Índice Futuro (WINFUT / INDFUT)")

# Caminho do Excel conectado
ARQUIVO = "dados.xlsx"   # coloque o caminho do seu arquivo
ABA = "Historico"        # troque pelo nome correto da aba

# Loop de atualização automática
placeholder = st.empty()

while True:
    try:
        # Lê os dados
        df = pd.read_excel(ARQUIVO, sheet_name=ABA)

        # Ajusta hora no índice (se tiver a coluna Hora)
        if "Hora" in df.columns:
            df["Hora"] = pd.to_datetime(df["Hora"])
            df = df.set_index("Hora")

        # Colunas que você pediu
        colunas = ["ÍNDICE -ESTRANGEIRO", "ÍNDICE-Bancos", "ÍNDICE-CPF",
                   "Juros DI’s", "WINFUT", "INDFUT"]

        df_plot = df[colunas]

        # Gráfico interativo com cores fixas
        fig = px.line(df_plot, x=df_plot.index, y=df_plot.columns,
                      title="Posições no Índice Futuro",
                      color_discrete_map={
                          "ÍNDICE -ESTRANGEIRO": "red",
                          "ÍNDICE-Bancos": "blue",
                          "ÍNDICE-CPF": "orange",
                          "Juros DI’s": "green",
                          "WINFUT": "purple",
                          "INDFUT": "brown"
                      })

        fig.update_layout(xaxis_title="Hora",
                          yaxis_title="Posição",
                          legend_title="Categoria",
                          template="plotly_white")

        # Atualiza o gráfico na tela
        with placeholder.container():
            st.plotly_chart(fig, use_container_width=True)

        time.sleep(30)  # atualiza a cada 30 segundos

    except Exception as e:
        st.error(f"Erro ao ler os dados: {e}")
        time.sleep(30)
