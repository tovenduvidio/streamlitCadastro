
import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
from collections import OrderedDict
from datetime import datetime


st.set_page_config(layout='wide', page_title='Inicial')


r = requests.get("https://docs.google.com/spreadsheets/d/1BM5cfa6jNYM8W9_tDczEt50VefeoVAlgtWFC8e2SHKI/export?format=xlsx&id=1BM5cfa6jNYM8W9_tDczEt50VefeoVAlgtWFC8e2SHKI")
open('clientes.xlsx', 'wb').write(r.content)



baseClientes = pd.read_excel('clientes.xlsx')


listaNomeClientes = baseClientes[['Nome']].values.tolist()
listaNomeClientes = str(listaNomeClientes).replace('[', '').replace(']', '').replace("'",'')
listaNomeClientes = listaNomeClientes.split(sep=', ')
listaNomeClientes = list(OrderedDict.fromkeys(listaNomeClientes))



st.title('Cadastro'.upper())


guia1, guia2 = st.tabs(['Clientes', 'Cadastrar'])


with guia1:
    filtrarClientes = st.selectbox('Pesquisar clientes', listaNomeClientes)

    indexCliente = baseClientes[baseClientes['Nome'] == filtrarClientes].index


    emailClienteFiltrado = baseClientes['E-mail'].loc[baseClientes['Nome'] == filtrarClientes].values[0]
    telefoneClienteFiltrado = baseClientes['Telefone'].loc[baseClientes['Nome'] == filtrarClientes].values[0]
    origemClienteFiltrado = baseClientes['Origem'].loc[baseClientes['Nome'] == filtrarClientes].values[0]
    donoClienteFiltrado = baseClientes['Dono'].loc[baseClientes['Nome'] == filtrarClientes].values[0]
    cadastradoEmClienteFiltrado = baseClientes['Cadastrado em'].loc[baseClientes['Nome'] == filtrarClientes].values[0]
    cadastradoEmClienteFiltrado = datetime.strptime(str(cadastradoEmClienteFiltrado).split('T')[0], '%Y-%m-%d').strftime('%d/%m/%Y')




    # print(cadastradoEmClienteFiltrado)

    coluna1Imagem, coluna2Imagem = st.columns(2)
    coluna1, coluna2 = st.columns(2)

    coluna1Imagem.image('imagens/iconeUser.png', width=115)

    edicaoDesabilitada = True

    coluna1.text_input('Nome', filtrarClientes, disabled=edicaoDesabilitada)
    coluna2.text_input('E-mail', emailClienteFiltrado, disabled=edicaoDesabilitada)
    coluna1.text_input('Telefone', telefoneClienteFiltrado, disabled=edicaoDesabilitada)
    coluna2.text_input('Origem', origemClienteFiltrado, disabled=edicaoDesabilitada)
    coluna1.text_input('Dono', donoClienteFiltrado, disabled=edicaoDesabilitada)
    coluna2.text_input('Cadastrado em', cadastradoEmClienteFiltrado, disabled=edicaoDesabilitada)



with guia2:
    components.iframe("https://docs.google.com/spreadsheets/d/1BM5cfa6jNYM8W9_tDczEt50VefeoVAlgtWFC8e2SHKI", height=670, scrolling=True)
