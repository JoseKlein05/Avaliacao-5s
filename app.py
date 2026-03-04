st.image("Marca Axel__Principal.png", width=350)

st.title("Avaliação 5S")
st.subheader("Departamento de Engenharia")

st.markdown("""
<style>

.stApp {
    background-color: black;
    color: white;
}

h1, h2, h3, h4 {
    color: white;
}

.stButton>button {
    background-color: #25a550;
    color: white;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from datetime import datetime
import os


# ==============================
# CONFIGURAÇÕES
# ==============================

ARQUIVO = "avaliacoes.csv"
SENHA = "Axel7070**#"


# ==============================
# LISTAS
# ==============================

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


# ==============================
# FUNÇÃO CLASSIFICAÇÃO BÔNUS
# ==============================

def classificar_bonus(media):

    if media >= 4.5:
        return "100% Bônus"

    elif media >= 3.5:
        return "75% Bônus"

    else:
        return "Sem Bônus"


# ==============================
# CRIAR ARQUIVO SE NÃO EXISTIR
# ==============================

if not os.path.exists(ARQUIVO):

    df = pd.DataFrame(columns=[
        "Mes",
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


# ==============================
# TÍTULO
# ==============================

st.title("Sistema de Avaliação 5S")


menu = st.radio(
    "Menu",
    ["Avaliar", "Notas"]
)


# ==============================
# TELA AVALIAR
# ==============================

if menu == "Avaliar":

    senha = st.text_input("Digite a senha", type="password")

    if senha == SENHA:

        st.header("Nova Avaliação")

        colaborador = st.selectbox(
            "Colaborador",
            colaboradores
        )

        mes = st.selectbox(
            "Mês da Avaliação",
            meses
        )

        col1, col2 = st.columns(2)

        with col1:

            seiri = st.number_input(
                "Seiri",
                min_value=0.0,
                max_value=5.0,
                step=0.1,
                format="%.1f"
            )

            seiton = st.number_input(
                "Seiton",
                min_value=0.0,
                max_value=5.0,
                step=0.1,
                format="%.1f"
            )

            seiso = st.number_input(
                "Seiso",
                min_value=0.0,
                max_value=5.0,
                step=0.1,
                format="%.1f"
            )

        with col2:

            seiketsu = st.number_input(
                "Seiketsu",
                min_value=0.0,
                max_value=5.0,
                step=0.1,
                format="%.1f"
            )

            shitsuke = st.number_input(
                "Shitsuke",
                min_value=0.0,
                max_value=5.0,
                step=0.1,
                format="%.1f"
            )

        if st.button("Salvar Avaliação"):

            media = (
                seiri +
                seiton +
                seiso +
                seiketsu +
                shitsuke
            ) / 5

            nova_linha = pd.DataFrame([{

                "Mes": mes,

                "Data": datetime.now().strftime("%Y-%m-%d"),

                "Colaborador": colaborador,

                "Seiri": seiri,
                "Seiton": seiton,
                "Seiso": seiso,
                "Seiketsu": seiketsu,
                "Shitsuke": shitsuke,

                "Media": round(media, 2)

            }])

            df2 = pd.concat([df, nova_linha], ignore_index=True)

            df2.to_csv(ARQUIVO, index=False)

            st.success("Avaliação salva com sucesso!")

    elif senha != "":
        st.error("Senha incorreta")


# ==============================
# TELA NOTAS
# ==============================

if menu == "Notas":

    st.header("Resultados")

    if len(df) == 0:

        st.warning("Nenhuma avaliação registrada")

    else:

        meses_disponiveis = [
            m for m in meses
            if m in df["Mes"].unique()
        ]

        mes_filtro = st.selectbox(
            "Selecionar mês",
            meses_disponiveis
        )

        df_mes = df[df["Mes"] == mes_filtro]


        # ==============================
        # MÉDIA POR COLABORADOR
        # ==============================

        media_mes = (
            df_mes
            .groupby("Colaborador")["Media"]
            .mean()
            .reset_index()
        )

        media_mes["Classificação Bônus"] = media_mes["Media"].apply(classificar_bonus)


        st.subheader("Média mensal por colaborador")

        st.dataframe(media_mes)


        # ==============================
        # TABELA COMPLETA
        # ==============================

        st.subheader("Avaliações registradas")

        st.dataframe(df_mes)


        # ==============================
        # MÉDIA DOS SENSOS
        # ==============================

        st.subheader("Média dos Sensos")

        medias = {

            "Seiri": df_mes["Seiri"].mean(),

            "Seiton": df_mes["Seiton"].mean(),

            "Seiso": df_mes["Seiso"].mean(),

            "Seiketsu": df_mes["Seiketsu"].mean(),

            "Shitsuke": df_mes["Shitsuke"].mean()

        }

        st.bar_chart(medias)
