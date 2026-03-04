import streamlit as st
import pandas as pd
from datetime import datetime
import os


ARQUIVO_AVALIACOES = "avaliacoes.csv"
ARQUIVO_USUARIOS = "usuarios.csv"

SENHA_ADMIN = "Axel7070**#"


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


if not os.path.exists(ARQUIVO_AVALIACOES):

    df = pd.DataFrame(columns=[
        "Mes","Data","Colaborador",
        "Seiri","Seiton","Seiso","Seiketsu","Shitsuke",
        "Media","Comentario"
    ])

    df.to_csv(ARQUIVO_AVALIACOES,index=False)


if not os.path.exists(ARQUIVO_USUARIOS):

    df_users = pd.DataFrame({
        "Colaborador": colaboradores,
        "Senha": ["" for _ in colaboradores]
    })

    df_users.to_csv(ARQUIVO_USUARIOS,index=False)



df = pd.read_csv(ARQUIVO_AVALIACOES)
usuarios = pd.read_csv(ARQUIVO_USUARIOS).fillna("")



def classificar_bonus(media):

    if media >= 4.5:
        return "100% Bônus"

    elif media >= 3.5:
        return "75% Bônus"

    elif media >= 3.0:
        return "50% Bônus"

    elif media >= 2.0:
        return "25% Bônus"

    else:
        return "Sem Bônus"



st.markdown("""
<style>
.stApp{background-color:black;color:white}
h1,h2,h3,h4{color:white}
.stButton>button{background-color:#25a550;color:white}
</style>
""", unsafe_allow_html=True)



st.image("logo_axel.png", width=350)

st.title("Sistema de Avaliação 5S")



menu = st.radio("Menu",["Avaliar","Notas"])



# -------------------
# TELA AVALIAR
# -------------------

if menu == "Avaliar":

    senha = st.text_input("Senha administrador", type="password")

    if senha == SENHA_ADMIN:

        colaborador = st.selectbox("Colaborador",colaboradores)

        mes = st.selectbox("Mês",meses)

        seiri = st.number_input("Seiri",0.0,5.0,step=0.1)
        seiton = st.number_input("Seiton",0.0,5.0,step=0.1)
        seiso = st.number_input("Seiso",0.0,5.0,step=0.1)
        seiketsu = st.number_input("Seiketsu",0.0,5.0,step=0.1)
        shitsuke = st.number_input("Shitsuke",0.0,5.0,step=0.1)

        comentario = st.text_area("Comentário")

        if st.button("Salvar avaliação"):

            media = (seiri+seiton+seiso+seiketsu+shitsuke)/5

            nova_linha = pd.DataFrame([{

                "Mes":mes,
                "Data":datetime.now().strftime("%Y-%m-%d"),
                "Colaborador":colaborador,

                "Seiri":seiri,
                "Seiton":seiton,
                "Seiso":seiso,
                "Seiketsu":seiketsu,
                "Shitsuke":shitsuke,

                "Media":round(media,2),

                "Comentario":comentario

            }])

            df2 = pd.concat([df,nova_linha],ignore_index=True)

            df2.to_csv(ARQUIVO_AVALIACOES,index=False)

            st.success("Avaliação salva!")

    elif senha != "":
        st.error("Senha incorreta")



# -------------------
# TELA NOTAS
# -------------------

if menu == "Notas":

    usuario = st.selectbox("Seu nome", colaboradores)

    senha_digitada = st.text_input("Senha", type="password")

    senha_salva = usuarios.loc[
        usuarios["Colaborador"] == usuario, "Senha"
    ].values[0]


    # PRIMEIRO ACESSO
    if pd.isna(senha_salva) or senha_salva == "":

        st.warning("Primeiro acesso. Crie sua senha.")

        nova_senha = st.text_input("Nova senha", type="password")

        if st.button("Salvar senha"):

            usuarios.loc[
                usuarios["Colaborador"] == usuario, "Senha"
            ] = nova_senha

            usuarios.to_csv(ARQUIVO_USUARIOS, index=False)

            st.success("Senha cadastrada!")


    # LOGIN
    elif senha_digitada == senha_salva:

        st.success("Login realizado")

        df_usuario = df[df["Colaborador"] == usuario]

        st.dataframe(df_usuario)


    elif senha_digitada != "":
        st.error("Senha incorreta")
