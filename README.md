# Aplicativo de Processamento e Fatiamento de Bases CSV

## Sobre
Este aplicativo, desenvolvido em **Streamlit**, tem como objetivo processar e fatiar arquivos CSV de dados de servidores públicos, aplicando lógicas específicas de acordo com o convênio selecionado. Ele gera arquivos CSV menores contendo apenas os servidores com oportunidades financeiras, otimizando o uso de robôs de higienização.

---

## Funcionalidades
- **Carregamento de Arquivos**: Permite o upload de múltiplos arquivos CSV.
- **Processamento por Convênio**: Aplica regras específicas de filtragem com base no convênio selecionado.
- **Divisão em Arquivos Menores**: Divide a base filtrada em arquivos de até 45.000 linhas.
- **Download de Arquivos Gerados**: Disponibiliza os arquivos processados para download.

---

## Como Funciona

1. **Configuração Inicial**
   O aplicativo permite o upload de múltiplos arquivos CSV contendo informações sobre servidores públicos e suas margens de empréstimo, benefício e cartão.

   ```python
   # Upload de múltiplos arquivos
   uploaded_files = st.file_uploader("Selecione os arquivos CSV", type="csv", accept_multiple_files=True)
