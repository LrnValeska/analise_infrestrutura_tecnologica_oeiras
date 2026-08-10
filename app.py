import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuração da página
st.set_page_config(
    page_title="Diagnóstico de Infraestrutura - Oeiras do Pará",
    page_icon="⚠️",
    layout="wide"
)

# Estilo CSS personalizado para alertas
st.markdown("""
    <style>
    .stMetric {
        background-color: #fff5f5;
        border-left: 5px solid #e53e3e;
        padding: 10px;
        border-radius: 5px;
    }
    .warning-box {
        background-color: #fffaf0;
        border-left: 5px solid #dd6b20;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚠️ Diagnóstico de Infraestrutura e Dificuldades Tecnológicas")
st.subheader("Análise Crítica do Censo Escolar — Oeiras do Pará (PA)")

st.markdown("""
<div class="warning-box">
<strong>Contexto de Vulnerabilidade:</strong> Este painel evidencia a grave carência de infraestrutura tecnológica e conectividade 
nas escolas do município de Oeiras do Pará. Os dados comprovam a urgência e a necessidade de adoção de metodologias como a 
<strong>Computação Desplugada</strong> no ecossistema educacional local.
</div>
""", unsafe_allow_html=True)

csv_file = "tabela_infraestrutura_oeiras.csv"

if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    
    # Exibir primeiras métricas e tabela
    st.write("### 🚨 Visão Geral dos Indicadores")
    
    # Se a tabela tiver colunas reconhecíveis
    cols = df.columns.tolist()
    
    col_indicator = cols[0]
    col_value = cols[1] if len(cols) > 1 else cols[0]

    # Gráfico 1: Gráfico de Barras Horizontal Dinâmico
    fig_bar = px.bar(
        df,
        x=col_value,
        y=col_indicator,
        orientation='h',
        text=col_value,
        title="<b>Deficit de Infraestrutura por Categoria</b>",
        labels={col_value: "Percentual / Quantidade", col_indicator: "Indicador Avaliado"},
        color=col_value,
        color_continuous_scale="Reds_r" # Escala de cor destacando carência
    )
    
    fig_bar.update_traces(texttemplate='%{text}', textposition='outside')
    fig_bar.update_layout(
        height=450,
        yaxis=dict(autorange="reversed"),
        font=dict(size=13),
        plot_bgcolor="rgba(0,0,0,0)"
    )

    # Layout em colunas
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        st.write("### 📊 Dados Detalhados")
        st.dataframe(df, use_container_width=True, height=380)

    st.divider()

    # Seção Interativa: Seleção de Filtro por Indicador
    st.write("### 🔍 Detalhamento por Indicador Selecionado")
    selected_item = st.selectbox("Selecione um indicador para analisar a discrepância:", df[col_indicator].unique())
    
    item_row = df[df[col_indicator] == selected_item].iloc[0]
    val = item_row[col_value]

    # Tenta calcular ou estimar o valor complementar para gráfico de Rosca (Com vs Sem)
    try:
        val_num = float(str(val).replace('%', '').replace(',', '.'))
        val_sem = max(0, 100 - val_num) if val_num <= 100 else 0
        
        donut_data = pd.DataFrame({
            'Condição': ['Possui / Atende', 'NÃO Possui / Sem Acesso'],
            'Percentual': [val_num, val_sem]
        })

        fig_donut = px.pie(
            donut_data,
            values='Percentual',
            names='Condição',
            hole=0.6,
            title=f"<b>Acesso x Exclusão: {selected_item}</b>",
            color='Condição',
            color_discrete_map={'Possui / Atende': '#2b6cb0', 'NÃO Possui / Sem Acesso': '#e53e3e'}
        )
        fig_donut.update_traces(textinfo='percent+label')
        
        st.plotly_chart(fig_donut, use_container_width=True)

    except Exception:
        st.info(f"Valor do indicador: **{val}**")

else:
    st.error(f"O arquivo `{csv_file}` não foi encontrado na pasta.")
    st.warning("Certifique-se de que o script `analise_infra_oeiras.py` foi executado primeiro.")