import streamlit as st
import pandas as pd
from datetime import datetime
import os

ARQUIVO = "avaliacoes.csv"
SENHA = "Axel7070**#"

colaboradores = [
    "Gabrieli",
    "João",
    "Lucas",
    "Luiz",
    "Maurício"
]

meses = [
    "Janeiro","Fevereiro","Março","Abril","Maio","Junho",
    "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
]

# criar arquivo se não existir
if not os.path.exists(ARQUIVO):
    df = pd.DataFrame(columns=[
        "Mes","Data","Colaborador",
        "Seiri","Seiton","Seiso","Seiketsu","Shitsuke",
        "Media"
    ])
    df.to_csv(ARQUIVO, index=False)

df = pd.read_csv(ARQUIVO)

st.title("Sistema de Avaliação 5S")

menu = st.radio(
    "Menu",
    ["Avaliar","Notas"]
)

# =============================
# TELA AVALIAR
# =============================

if menu == "Avaliar":

    senha = st.text_input("Digite a senha", type="password")

    if senha == SENHA:

        st.header("Nova Avaliação")

        colaborador = st.selectbox("Colaborador", colaboradores)

        mes = st.selectbox("Mês da Avaliação", meses)

        col1, col2 = st.columns(2)

        with col1:
            seiri = st.number_input("Seiri", min_value=0.0, max_value=5.0, step=0.1, format="%.1f")
            seiton = st.number_input("Seiton", min_value=0.0, max_value=5.0, step=0.1, format="%.1f")
            seiso = st.number_input("Seiso", min_value=0.0, max_value=5.0, step=0.1, format="%.1f")

        with col2:
            seiketsu = st.number_input("Seiketsu", min_value=0.0, max_value=5.0, step=0.1, format="%.1f")
            shitsuke = st.number_input("Shitsuke", min_value=0.0, max_value=5.0, step=0.1, format="%.1f")

        if st.button("Salvar Avaliação"):

            media = (seiri + seiton + seiso + seiketsu + shitsuke) / 5

            nova_linha = pd.DataFrame([{
                "Mes": mes,
                "Data": datetime.now().strftime("%Y-%m-%d"),
                "Colaborador": colaborador,
                "Seiri": seiri,
                "Seiton": seiton,
                "Seiso": seiso,
                "Seiketsu": seiketsu,
                "Shitsuke": shitsuke,
                "Media": round(media,2)
            }])

            df2 = pd.concat([df, nova_linha], ignore_index=True)
            df2.to_csv(ARQUIVO, index=False)

            st.success("Avaliação salva com sucesso!")

    elif senha != "":
        st.error("Senha incorreta")

# =============================
# TELA NOTAS
# =============================

if menu == "Notas":

    st.header("Resultados")

    if len(df) == 0:
        st.warning("Nenhuma avaliação registrada")

    else:

        mes_filtro = st.selectbox(
            "Selecionar mês",
            df["Mes"].unique()
        )

        df_mes = df[df["Mes"] == mes_filtro]

        media_mes = df_mes.groupby("Colaborador")["Media"].mean().reset_index()

        st.subheader("Média mensal por colaborador")

        st.dataframe(media_mes)

        st.subheader("Tabela de avaliações")

        st.dataframe(df_mes)

        st.subheader("Média dos Sensos")

        medias = {
            "Seiri": df_mes["Seiri"].mean(),
            "Seiton": df_mes["Seiton"].mean(),
            "Seiso": df_mes["Seiso"].mean(),
            "Seiketsu": df_mes["Seiketsu"].mean(),
            "Shitsuke": df_mes["Shitsuke"].mean()
        }

        st.bar_chart(medias)
