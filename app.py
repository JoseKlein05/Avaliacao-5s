import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

conn = sqlite3.connect("avaliacoes_5s.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS avaliacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    colaborador TEXT,
    data DATE,
    seiri REAL,
    seiton REAL,
    seiso REAL,
    seiketsu REAL,
    shitsuke REAL,
    nota_final REAL,
    classificacao TEXT
)
""")
conn.commit()

st.title("Sistema de Avaliação 5S")

colaboradores = ["Lucas","João","Maria","Carlos"]

colaborador = st.selectbox("Colaborador", colaboradores)
data_avaliacao = st.date_input("Data da avaliação", date.today())

st.subheader("Avaliação dos Sensos")

seiri = st.slider("Seiri",0.0,5.0,3.0)
seiton = st.slider("Seiton",0.0,5.0,3.0)
seiso = st.slider("Seiso",0.0,5.0,3.0)
seiketsu = st.slider("Seiketsu",0.0,5.0,3.0)
shitsuke = st.slider("Shitsuke",0.0,5.0,3.0)

nota = (
    seiri*0.10 +
    seiton*0.25 +
    seiso*0.15 +
    seiketsu*0.40 +
    shitsuke*0.10
)

st.metric("Nota Final", round(nota,2))

if nota >= 4.5:
    classificacao="100%"
    st.success("Classificação: 100%")
elif nota >=3.5:
    classificacao="75%"
    st.warning("Classificação: 75%")
else:
    classificacao="Retido"
    st.error("Classificação: Retido")

if st.button("Salvar Avaliação"):

    c.execute("""
    INSERT INTO avaliacoes
    (colaborador,data,seiri,seiton,seiso,seiketsu,shitsuke,nota_final,classificacao)
    VALUES (?,?,?,?,?,?,?,?,?)
    """,(colaborador,data_avaliacao,seiri,seiton,seiso,seiketsu,shitsuke,nota,classificacao))

    conn.commit()

    st.success("Avaliação salva!")

st.divider()

df = pd.read_sql_query("SELECT * FROM avaliacoes", conn)

if not df.empty:

    df['data']=pd.to_datetime(df['data'])
    df['mes']=df['data'].dt.to_period("M")

    st.subheader("Histórico")
    st.dataframe(df)

    st.subheader("Média Mensal")

    media=df.groupby("mes")["nota_final"].mean().reset_index()

    st.line_chart(media.set_index("mes"))
