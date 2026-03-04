if menu == "Notas":

    usuario = st.selectbox(
        "Seu nome",
        colaboradores
    )

    senha_digitada = st.text_input(
        "Senha",
        type="password"
    )

    senha_salva = usuarios.loc[
        usuarios["Colaborador"] == usuario,
        "Senha"
    ].values[0]


    # PRIMEIRO ACESSO
    if senha_salva == "":

        st.warning("Primeiro acesso. Crie sua senha.")

        nova_senha = st.text_input("Criar nova senha", type="password")

        if st.button("Cadastrar senha"):

            usuarios.loc[
                usuarios["Colaborador"] == usuario,
                "Senha"
            ] = nova_senha

            usuarios.to_csv(ARQUIVO_USUARIOS, index=False)

            st.success("Senha cadastrada com sucesso!")


    # LOGIN CORRETO
    elif senha_digitada == senha_salva:

        st.success("Login realizado")

        df_usuario = df[
            df["Colaborador"] == usuario
        ]

        if len(df_usuario) == 0:

            st.info("Nenhuma avaliação encontrada")

        else:

            mes_filtro = st.selectbox(
                "Mês",
                df_usuario["Mes"].unique()
            )

            df_mes = df_usuario[
                df_usuario["Mes"] == mes_filtro
            ]

            media = df_mes["Media"].mean()

            st.metric(
                "Média do mês",
                round(media,2)
            )

            st.write(
                "Classificação:",
                classificar_bonus(media)
            )

            st.dataframe(df_mes)


    # SENHA ERRADA
    elif senha_digitada != "":
        st.error("Senha incorreta")
