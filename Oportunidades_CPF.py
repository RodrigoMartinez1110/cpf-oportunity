import streamlit as st
import pandas as pd

# Função para aplicar lógica específica ao convênio
def aplicar_logica_convenio(base, convenio):
    if convenio == 'govsp':
        usou_beneficio = base.loc[
            base['MG_Beneficio_Saque_Total'] - base['MG_Beneficio_Saque_Disponivel'] > 0, 'Matricula'
        ].tolist()
        usou_cartao = base.loc[
            base['MG_Cartao_Total'] - base['MG_Cartao_Disponivel'] > 0, 'Matricula'
        ].tolist()
        usou_novo = base.loc[
            base['MG_Emprestimo_Disponivel'] < 0, 'Matricula'
        ].tolist()

        base = base.loc[
            ((base['MG_Emprestimo_Disponivel'] >= 35) & (~base['Matricula'].isin(usou_novo))) |
            (((base['MG_Beneficio_Saque_Total'] == base['MG_Beneficio_Saque_Disponivel']) & 
             (base['MG_Beneficio_Saque_Disponivel'] >= 35)) |
             ((base['MG_Cartao_Total'] == base['MG_Cartao_Disponivel']) & 
             (base['MG_Cartao_Disponivel'] >= 35))) &
             (~base['CPF'].isin(usou_beneficio)) & (~base['CPF'].isin(usou_cartao))
        ]
    elif convenio == 'prefrj':
        base = base.loc[
            (base['MG_Emprestimo_Disponivel'] >= 30) |
            (base['MG_Beneficio_Saque_Disponivel'] >= 30) |
            (base['MG_Cartao_Disponivel'] >= 30)
        ]
    else:
        base = base.loc[
            (base['MG_Emprestimo_Disponivel'] >= 30) |
            ((base['MG_Beneficio_Saque_Total'] == base['MG_Beneficio_Saque_Disponivel']) & 
             (base['MG_Beneficio_Saque_Disponivel'] >= 30)) |
            ((base['MG_Cartao_Total'] == base['MG_Cartao_Disponivel']) & 
             (base['MG_Cartao_Disponivel'] >= 30))
        ]
    return base

# Função para juntar e processar os arquivos CSV
def juntar_arquivos(arquivos, convenio):
    dfs = []

    for arquivo in arquivos:
        try:
            df = pd.read_csv(arquivo)
            dfs.append(df)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo {arquivo.name}: {e}")
            return []

    # Verificação de colunas obrigatórias
    colunas_obrigatorias = [
        'CPF', 'Matricula', 'Vinculo_Servidor', 
        'MG_Emprestimo_Total', 'MG_Emprestimo_Disponivel', 
        'MG_Beneficio_Saque_Total', 'MG_Beneficio_Saque_Disponivel', 
        'MG_Cartao_Total', 'MG_Cartao_Disponivel'
    ]

    for df in dfs:
        if not all(col in df.columns for col in colunas_obrigatorias):
            st.error("Um ou mais arquivos não possuem as colunas necessárias.")
            return []

    base = pd.concat(dfs, ignore_index=True)
    base = base[colunas_obrigatorias]

    # Aplica lógica de convênio
    base = aplicar_logica_convenio(base, convenio)

    # Remove duplicados e limpa a coluna CPF
    base.drop_duplicates('CPF', inplace=True)
    base['CPF'] = base['CPF'].astype(str).str.replace(r"[.-]", "", regex=True)
    base = base[['CPF']].rename(columns={'CPF': 'cpf'})

    # Divide a base em arquivos menores
    arquivos_gerados = []
    num_linhas_por_arquivo = 45000

    for i in range(0, len(base), num_linhas_por_arquivo):
        csv_data = base.iloc[i:i + num_linhas_por_arquivo].to_csv(index=False, sep=';', header=True).encode('utf-8')
        arquivos_gerados.append(csv_data)

    return arquivos_gerados

# Configura o título do aplicativo
st.title("Processamento e Fatiamento de Base CSV")

# Upload de múltiplos arquivos
uploaded_files = st.file_uploader("Selecione os arquivos CSV", type="csv", accept_multiple_files=True)

# Seleção do convênio
convenio = st.selectbox("Escolha o convênio", ['govsp', 'prefrj', 'outros'])

if uploaded_files:
    # Juntar os arquivos e processá-los
    arquivos_gerados = juntar_arquivos(uploaded_files, convenio)
    
    if arquivos_gerados:
        st.success("Processamento concluído com sucesso!")
        for i, arquivo in enumerate(arquivos_gerados):
            st.download_button(
                label=f"Baixar Arquivo Parte {i + 1}",
                data=arquivo,
                file_name=f'{convenio}_CPF_OPORTUNIDADE_parte_{i + 1}.csv',
                mime="text/csv"
            )
    else:
        st.error("Nenhum arquivo foi processado. Verifique os arquivos carregados.")
else:
    st.info("Carregue os arquivos para começar.")
