
import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
from collections import OrderedDict
from datetime import datetime, timedelta
import calendar
import plotly.express as px


st.set_page_config(layout='wide', page_title='Dashboard')

st.runtime.legacy_caching.clear_cache()


r = requests.get("https://docs.google.com/spreadsheets/d/1BM5cfa6jNYM8W9_tDczEt50VefeoVAlgtWFC8e2SHKI/export?format=xlsx&id=1BM5cfa6jNYM8W9_tDczEt50VefeoVAlgtWFC8e2SHKI")
open('clientes.xlsx', 'wb').write(r.content)



dataHoje = datetime.today()
dataOntem = dataHoje - timedelta(days=1)
dataAmanha = dataHoje + timedelta(days=1)

data_inicial_mes = dataHoje.replace(day=1)
data_final_mes = dataHoje.replace(day=calendar.monthrange(dataHoje.year, dataHoje.month)[1])

mes_anterior = dataHoje.replace(day=1) - timedelta(days=1)
primeiro_dia_mes_anterior = mes_anterior.replace(day=1)
ultimo_dia_mes_anterior = mes_anterior.replace(day=calendar.monthrange(mes_anterior.year, mes_anterior.month)[1])
dias31atras = dataHoje - timedelta(days=31)

segundo_mes_anterior = primeiro_dia_mes_anterior - timedelta(days=1)
primeiro_dia_segundo_mes_anterior = segundo_mes_anterior.replace(day=1)
ultimo_dia_segundo_mes_anterior = segundo_mes_anterior.replace(day=calendar.monthrange(segundo_mes_anterior.year, segundo_mes_anterior.month)[1])

terceiro_mes_anterior = primeiro_dia_segundo_mes_anterior - timedelta(days=1)
primeiro_dia_terceiro_mes_anterior = terceiro_mes_anterior.replace(day=1)
ultimo_dia_terceiro_mes_anterior = terceiro_mes_anterior.replace(day=calendar.monthrange(terceiro_mes_anterior.year, terceiro_mes_anterior.month)[1])

mesAtual = dataHoje.month
anoAtual = dataHoje.year



corGraficos = '#78b865'
corLinhasGraficos = '#375680'



nome_meses = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}



#r = requests.get("https://docs.google.com/spreadsheets/d/1BsFhkBI0fAKxfo6iMegsqk3RjKWSczlWvBnfnysq0DA/export?format=xlsx&id=1BsFhkBI0fAKxfo6iMegsqk3RjKWSczlWvBnfnysq0DA")
#open('karaoke.xlsx', 'wb').write(r.content)

escolherIndicador = st.sidebar.radio('Visualizar', ('Movimento - Cadastros'.upper(),
                                                    'Base'.upper()))

baseClientes = pd.read_excel('clientes.xlsx')


if escolherIndicador == 'Movimento - Cadastros'.upper():
    st.title(escolherIndicador.upper())
    
    baseMovimentoCadastros = pd.read_excel('clientes.xlsx')
    baseMovimentoCadastros['Cadastrado em'] = baseMovimentoCadastros['Cadastrado em'].dt.strftime('%Y-%m-%d')
    baseMovimentoCadastros['Cadastrado em'] = pd.to_datetime(baseMovimentoCadastros['Cadastrado em'], format='%Y-%m-%d')
    baseMovimentoCadastros['nomeMês'] = baseMovimentoCadastros['Mês'].apply(lambda x: nome_meses[x])

    
    col1, col2 = st.columns(2)
    data_inicio = col1.date_input('Selecione a data de início', datetime.strptime(data_inicial_mes.strftime('%Y-%m-%d'), '%Y-%m-%d'))
    data_fim = col2.date_input('Selecione a data de fim', datetime.strptime(data_final_mes.strftime('%Y-%m-%d'), '%Y-%m-%d'))

    # Filtrando o dataframe de acordo com as datas selecionadas
    filtro_data = (baseMovimentoCadastros['Cadastrado em'] >= data_inicio.strftime('%Y-%m-%d')) & (baseMovimentoCadastros['Cadastrado em'] <= data_fim.strftime('%Y-%m-%d'))
    baseMovimentoCadastros_filtrado = baseMovimentoCadastros[filtro_data]

    movimentoPorDia = baseMovimentoCadastros_filtrado.groupby(['Cadastrado em'], as_index=False).agg({'ID': 'count'})
    movimentoPorDia['Cadastrado em'] = movimentoPorDia['Cadastrado em'].dt.strftime('%d/%m/%Y')

    movimentoPorMes = baseMovimentoCadastros_filtrado.groupby(['Ano', 'Mês', 'nomeMês'], as_index=False).agg({'ID': 'count'})
    movimentoPorMes['nomeMês'] = movimentoPorMes['nomeMês'].str[:3] + ' ' + movimentoPorMes['Ano'].astype(str)
    

    movimentoPorDiaOrigem = baseMovimentoCadastros_filtrado.groupby(['Cadastrado em', 'Origem'], as_index=False).agg({'ID': 'count'})
    movimentoPorDiaOrigem['Cadastrado em'] = movimentoPorDiaOrigem['Cadastrado em'].dt.strftime('%d/%m/%Y')

    movimentoPorMesOrigem = baseMovimentoCadastros_filtrado.groupby(['Ano', 'Mês', 'nomeMês', 'Origem'], as_index=False).agg({'ID': 'count'})
    movimentoPorMesOrigem['nomeMês'] = movimentoPorMesOrigem['nomeMês'].str[:3] + ' ' + movimentoPorMesOrigem['Ano'].astype(str)


    guia1, guia2, guia3 = st.tabs(['Geral', 'Por origem', 'Sobre'])

    with guia1: 
        fig = px.bar(movimentoPorDia, x='Cadastrado em', y='ID', barmode='group', text_auto=True, title=f'CADASTROS POR DIA')
        fig.update_layout(xaxis_title='Data', yaxis_title='Quantidade')
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(movimentoPorMes, x='nomeMês', y='ID', barmode='group', text_auto=True, title='MOVIMENTO POR MÊS')
        fig2.update_layout(xaxis_title='Meses', yaxis_title='Quantidade', yaxis_gridcolor=corLinhasGraficos)
        st.plotly_chart(fig2, use_container_width=True)

    with guia2:
        col1Checkbox, col2Checkbox, col3Checkbox = st.columns([1,3,1])
        alterarBarmode = col1Checkbox.checkbox('Agrupado', value=True)
        visualizarNumeros = col2Checkbox.checkbox('Números', value=True)

        if alterarBarmode:
            barmodeGrafico = 'group'
        else:
            barmodeGrafico = 'relative'
        
        if visualizarNumeros:
            verNumeros = True
        else:
            verNumeros = False

        fig3 = px.bar(movimentoPorDiaOrigem, x='Cadastrado em', y='ID', barmode=barmodeGrafico, category_orders={'Origem': ['Spotify', 'Facebook', 'Twitter', 'Youtube']}, color_discrete_sequence=['#1fc275', '#32548a', '#32c4cf','#c44037'], text_auto=verNumeros, color='Origem', title=f'CADASTROS POR DIA')
        fig3.update_layout(legend_title='Origem', xaxis_title='Data', yaxis_title='Quantidade')
        st.plotly_chart(fig3, use_container_width=True)

        fig4 = px.bar(movimentoPorMesOrigem, x='nomeMês', y='ID', barmode=barmodeGrafico, color='Origem', category_orders={'Origem': ['Spotify', 'Facebook', 'Twitter', 'Youtube']}, color_discrete_sequence=['#1fc275', '#32548a', '#32c4cf','#c44037'], text_auto=verNumeros, title='MOVIMENTO POR MÊS')
        fig4.update_layout(legend_title='Origem', xaxis_title='Meses', yaxis_title='Quantidade', yaxis_gridcolor=corLinhasGraficos)
        st.plotly_chart(fig4, use_container_width=True)


if escolherIndicador == 'Base'.upper():
    st.title(escolherIndicador.upper())
   
    baseGeral = pd.read_excel('clientes.xlsx')
    baseGeral['Cadastrado em'] = baseGeral['Cadastrado em'].dt.strftime('%Y-%m-%d')
    baseGeral['Cadastrado em'] = pd.to_datetime(baseGeral['Cadastrado em'], format='%Y-%m-%d')
    baseGeral['nomeMês'] = baseGeral['Mês'].apply(lambda x: nome_meses[x])
    baseGeral['Dia da Semana'] = baseGeral['Mês'].apply(lambda x: nome_meses[x])


    # col1, col2 = st.columns(2)
    # data_inicio = col1.date_input('Selecione a data de início', datetime.strptime(data_inicial_mes.strftime('%Y-%m-%d'), '%Y-%m-%d'))
    # data_fim = col2.date_input('Selecione a data de fim', datetime.strptime(data_final_mes.strftime('%Y-%m-%d'), '%Y-%m-%d'))

    # Filtrando o dataframe de acordo com as datas selecionadas
    # filtro_data = (baseGeral['Cadastrado em'] >= data_inicio.strftime('%Y-%m-%d')) & (baseGeral['Cadastrado em'] <= data_fim.strftime('%Y-%m-%d'))
    # baseGeral_filtrado = baseGeral[filtro_data]

    clientesTotalPorOrigem = baseGeral.groupby(['Origem'], as_index=False).agg({'ID': 'count'})
    clientesTotalPorDono = baseGeral.groupby(['Dono'], as_index=False).agg({'ID': 'count'})


    print(clientesTotalPorDono)

    guia1, guia2 = st.tabs(['Geral', 'Sobre'])

    with guia1: 
        col1Guia, col2Guia = st.columns(2)
        
        fig = px.bar(clientesTotalPorOrigem, x='Origem', y='ID', barmode='group', category_orders={'Origem': ['Spotify', 'Facebook', 'Twitter', 'Youtube']}, color_discrete_sequence=['#1fc275', '#32548a', '#32c4cf','#c44037'], text_auto=True, color='Origem', title=f'TOTAL DE CLIENTES POR ORIGEM')
        fig.update_layout(legend_title='Origem', xaxis_title='Origem', yaxis_title='Quantidade')
        fig.update_traces(width=1)
        col1Guia.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(clientesTotalPorDono, x='Dono', y='ID', barmode='group', text_auto=True, color='Dono', title=f'TOTAL DE CLIENTES POR DONO')
        fig2.update_layout(legend_title='Origem', xaxis_title='Dono', yaxis_title='Quantidade')
        fig2.update_traces(width=1)
        col2Guia.plotly_chart(fig2, use_container_width=True)

        
