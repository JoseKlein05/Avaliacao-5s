import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ------------------------------
# CONFIGURAÇÃO
# ------------------------------

ARQUIVO = "avaliacoes.csv"
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

# ------------------------------
# ESTILO VISUAL AXEL
# ------------------------------

st.set_page_config(layout="wide")

st.markdown("""
<style>

.stApp{
background-color:#000000;
color:white;
}

h1,h2,h3{
color:white;
}

.stButton>button{
background-color:#25a550;
color:white;
border-radius:6px;
border:none;
}

.stSelectbox, .stTextInput{
color:white;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------
# LOGO
# ------------------------------

if os.path.exists("logo_axel.png"):
    st.image("logo_axel.png", width=350)
    
st.title("Sistema de Avaliação 5S")
st.caption("Departamento de Engenharia")

# ------------------------------
# FUNÇÃO BONUS
# ------------------------------

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

# ------------------------------
# CRIA ARQUIVOS
# ------------------------------

if not os.path.exists(ARQUIVO):

    df = pd.DataFrame(columns=[
        "Mes","Data","Colaborador",
        "Seiri","Seiton","Seiso","Seiketsu","Shitsuke",
        "Media","Comentario"
    ])

    df.to_csv(ARQUIVO,index=False)

if not os.path.exists(ARQUIVO_USUARIOS):

    df = pd.DataFrame({
        "Colaborador":colaboradores,
        "Senha":[""]*len(colaboradores)
    })

    df.to_csv(ARQUIVO_USUARIOS,index=False)

df = pd.read_csv(ARQUIVO)
usuarios = pd.read_csv(ARQUIVO_USUARIOS)

usuarios["Senha"] = usuarios["Senha"].fillna("")

# ------------------------------
# MENU
# ------------------------------

st.sidebar.title("Menu")

menu = st.sidebar.radio(
    "",
    ["Avaliar","Notas"]
)

# ------------------------------
# TELA AVALIAÇÃO
# ------------------------------

if menu == "Avaliar":

    senha = st.text_input("Senha para avaliar", type="password")

    if senha == SENHA_ADMIN:

        st.subheader("Nova Avaliação")

        colaborador = st.selectbox(
            "Colaborador",
            colaboradores
        )

        data = st.date_input(
            "Data da avaliação",
            datetime.today()
        )

        mes = meses[data.month-1]

        col1,col2,col3,col4,col5 = st.columns(5)

        with col1:
            seiri = st.number_input("Seiri",0.0,5.0,step=0.1)

        with col2:
            seiton = st.number_input("Seiton",0.0,5.0,step=0.1)

        with col3:
            seiso = st.number_input("Seiso",0.0,5.0,step=0.1)

        with col4:
            seiketsu = st.number_input("Seiketsu",0.0,5.0,step=0.1)

        with col5:
            shitsuke = st.number_input("Shitsuke",0.0,5.0,step=0.1)

        comentario = st.text_area("Comentário")

        media = round((seiri+seiton+seiso+seiketsu+shitsuke)/5,1)

        if st.button("Salvar Avaliação"):

            nova = pd.DataFrame([{
                "Mes":mes,
                "Data":data,
                "Colaborador":colaborador,
                "Seiri":seiri,
                "Seiton":seiton,
                "Seiso":seiso,
                "Seiketsu":seiketsu,
                "Shitsuke":shitsuke,
                "Media":media,
                "Comentario":comentario
            }])

            df = pd.concat([df,nova],ignore_index=True)

            df.to_csv(ARQUIVO,index=False)

            st.success("Avaliação registrada")

    elif senha != "":
        st.error("Senha incorreta")

# ------------------------------
# TELA NOTAS
# ------------------------------

if menu == "Notas":

    usuario = st.selectbox("Seu nome", colaboradores)

    senha_digitada = st.text_input("Digite sua senha", type="password")

    senha_salva = usuarios.loc[
        usuarios["Colaborador"] == usuario, "Senha"
    ].values[0]

    # PRIMEIRO ACESSO
    if senha_salva == "":

        st.warning("Primeiro acesso. Crie sua senha.")

        nova_senha = st.text_input("Nova senha", type="password")

        if st.button("Salvar senha"):

            usuarios.loc[
                usuarios["Colaborador"] == usuario, "Senha"
            ] = nova_senha

            usuarios.to_csv(ARQUIVO_USUARIOS,index=False)

            st.success("Senha cadastrada!")

            st.rerun()

    else:

        if st.button("Entrar"):

            if senha_digitada.strip() == senha_salva.strip():

                st.success("Login realizado")

                df_usuario = df[df["Colaborador"] == usuario]

                if len(df_usuario) == 0:

                    st.info("Sem avaliações ainda.")

                else:

                    st.subheader("Suas avaliações")

                    st.dataframe(df_usuario)

                    st.subheader("Média mensal")

                    media_mes = df_usuario.groupby("Mes")["Media"].mean().reset_index()

                    ordem = {mes:i for i,mes in enumerate(meses)}

                    media_mes["ordem"] = media_mes["Mes"].map(ordem)

                    media_mes = media_mes.sort_values("ordem")

                    media_mes["Classificação"] = media_mes["Media"].apply(classificar_bonus)

                    st.dataframe(
                        media_mes[["Mes","Media","Classificação"]]
                    )

            else:

                st.error("Senha incorreta")
