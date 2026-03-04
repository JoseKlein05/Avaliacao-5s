import streamlit as st
import pandas as pd
from datetime import datetime
import os

ARQUIVO = "avaliacoes.csv"
SENHA = "Axel7070**#"

# -------------------------------
# criar arquivo se não existir
# -------------------------------

if not os.path.exists(ARQUIVO):
    df = pd.DataFrame(columns=[
        "Data",
        "Colaborador",
        "Seiri",
        "Seiton",
        "Seiso",
        "Seiketsu",
        "Shitsuke",
        "Media"
    ])
    df.to_csv(ARQUIVO, index=False)

df = pd.read_csv(ARQUIVO)

# -------------------------------
# título
# -------------------------------

st.title("Sistema de Avaliação 5S")

menu = st.radio(
    "Menu",
    ["Avaliar", "Notas"]
)

# =============================
# TELA AVALIAR
# =============================

if menu == "Avaliar":

    senha = st.text_input("Digite a senha", type="password")

    if senha == SENHA:

        st.header("Nova Avaliação")

        colaborador = st.text_input("Colaborador")

        col1, col2 = st.columns(2)

        with col1:
            seiri = st.number_input("Seiri", min_value=0, max_value=5)
            seiton = st.number_input("Seiton", min_value=0, max_value=5)
            seiso = st.number_input("Seiso", min_value=0, max_value=5)

        with col2:
            seiketsu = st.number_input("Seiketsu", min_value=0, max_value=5)
            shitsuke = st.number_input("Shitsuke", min_value=0, max_value=5)

        if st.button("Salvar Avaliação"):

            media = (seiri + seiton + seiso + seiketsu + shitsuke) / 5

            nova_linha = pd.DataFrame([{
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

        media_geral = df["Media"].mean()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Média Geral", round(media_geral,2))

        with col2:
            st.metric("Total Avaliações", len(df))

        st.subheader("Tabela de Avaliações")

        st.dataframe(df)

        st.subheader("Média por Colaborador")

        media_colaborador = df.groupby("Colaborador")["Media"].mean().reset_index()

        st.dataframe(media_colaborador)

        st.subheader("Média dos Sensos")

        medias = {
            "Seiri": df["Seiri"].mean(),
            "Seiton": df["Seiton"].mean(),
            "Seiso": df["Seiso"].mean(),
            "Seiketsu": df["Seiketsu"].mean(),
            "Shitsuke": df["Shitsuke"].mean()
        }

        st.bar_chart(medias)
