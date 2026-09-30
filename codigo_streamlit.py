import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Cadastro de Pacientes",
    layout="centered"
)

st.title("Cadastro de Pacientes")

# Inicializa a lista de pacientes na sessão
if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(
        columns=[
            "timestamp",
            "nome",
            "idade",
            "convenio",
            "prioridade",
            "motivo"
        ]
    )

# Formulário de cadastro
with st.form("cadastro", clear_on_submit=True):

    nome = st.text_input(
        "Nome do paciente",
        placeholder="Digite o nome completo"
    )

    idade = st.number_input(
        "Idade",
        min_value=0,
        max_value=120,
        step=1
    )

    convenio = st.selectbox(
        "Convênio",
        [
            "Particular",
            "Unimed",
            "Bradesco Saúde",
            "SulAmérica",
            "Outro"
        ]
    )

    prioridade = st.selectbox(
        "Prioridade do atendimento",
        [1, 2, 3, 4, 5]
    )

    motivo = st.text_area(
        "Motivo da consulta / observações"
    )

    enviado = st.form_submit_button("Cadastrar")


# Cadastro do paciente
if enviado:

    # Validação do nome
    if not nome.strip():
        st.error("Informe o nome do paciente.")

    else:
        nova_linha = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nome": nome.strip(),
            "idade": int(idade),
            "convenio": convenio,
            "prioridade": prioridade,
            "motivo": motivo.strip()
        }

        # Adiciona o paciente à sessão
        st.session_state.pacientes = pd.concat(
            [
                st.session_state.pacientes,
                pd.DataFrame([nova_linha])
            ],
            ignore_index=True
        )

        st.success("Paciente cadastrado com sucesso!")


# Exibe os últimos 5 pacientes
st.subheader("Últimos pacientes cadastrados")

st.dataframe(
    st.session_state.pacientes.tail(5),
    use_container_width=True
)


# Botão para baixar o CSV
csv = st.session_state.pacientes.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Baixar CSV",
    data=csv,
    file_name="pacientes.csv",
    mime="text/csv"
)
