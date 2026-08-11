import streamlit as st
import plotly.express as px
import pandas as pd

# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Panorama de Infraestrutura Tecnológica - Oeiras do Pará",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CARREGAMENTO DE DADOS (INFRAESTRUTURA DE OEIRAS DO PARÁ)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    # Dados focados nos gargalos tecnológicos e de conectividade do município
    data = {
        "Setor_Local": [
            "Escolas Públicas", 
            "Unidades de Saúde", 
            "Prédios Administrativos", 
            "Comércio Local", 
            "Residências"
        ],
        "Tipo_Conexao": [
            "Via Rádio / Satélite", 
            "Via Rádio / Móvel", 
            "Fibra / Satélite", 
            "Via Rádio / Móvel", 
            "Móvel 3G/4G Instável"
        ],
        "Velocidade_Media_Mbps": [3.5, 5.0, 15.0, 8.0, 4.0],
        "Deficit_Acesso_Percentual": [78.0, 65.0, 40.0, 58.0, 82.0],
        "Quedas_Semanais_Media": [14, 10, 6, 9, 18],
        "Status_Conectividade": ["Crítico", "Atenção", "Razoável", "Atenção", "Crítico"]
    }
    return pd.DataFrame(data)

df = load_data()

# ---------------------------------------------------------
# BARRA LATERAL (FILTROS DE ANÁLISE)
# ---------------------------------------------------------
st.sidebar.title("Filtros de Visualização")

setores_selecionADOS = st.sidebar.multiselect(
    "Selecione os Setores / Locais:",
    options=df["Setor_Local"].unique(),
    default=df["Setor_Local"].unique()
)

df_filtered = df[df["Setor_Local"].isin(setores_selecionADOS)]

# ---------------------------------------------------------
# CABEÇALHO PRINCIPAL
# ---------------------------------------------------------
st.title("Diagnóstico de Infraestrutura Tecnológica")
st.caption("Análise sobre a limitação de conectividade e acesso digital em Oeiras do Pará")
st.markdown("---")

# ---------------------------------------------------------
# METRICAS PRINCIPAIS (INDICADORES DE PRECARIEDADE)
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

deficit_medio = df_filtered["Deficit_Acesso_Percentual"].mean() if not df_filtered.empty else 0
vel_media = df_filtered["Velocidade_Media_Mbps"].mean() if not df_filtered.empty else 0
setores_criticos = len(df_filtered[df_filtered["Status_Conectividade"] == "Crítico"])

with col1:
    st.metric(
        label="Déficit Médio de Acesso Adequado",
        value=f"{deficit_medio:.1f}%"
    )

with col2:
    st.metric(
        label="Velocidade Média Estimada",
        value=f"{vel_media:.1f} Mbps"
    )

with col3:
    st.metric(
        label="Setores em Estado Crítico",
        value=setores_criticos
    )

st.markdown("---")

# ---------------------------------------------------------
# GRÁFICOS VISUAIS (PLOTLY COM SINTAXE CORRIGIDA)
# ---------------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Déficit de Infraestrutura por Setor")
    
    fig_bar = px.bar(
        df_filtered,
        x="Setor_Local",
        y="Deficit_Acesso_Percentual",
        text="Deficit_Acesso_Percentual",
        color_discrete_sequence=["#d9534f"]  # Tom vermelho/alerta para indicar precariedade
    )
    
    # Atualização sem propriedades descontinuadas (evita erro de titlefont)
    fig_bar.update_layout(
        height=420,
        xaxis=dict(
            title=dict(
                text="Setor Avaliado",
                font=dict(size=13, family="Arial")
            )
        ),
        yaxis=dict(
            title=dict(
                text="Déficit de Acesso (%)",
                font=dict(size=13, family="Arial")
            )
        ),
        margin=dict(l=20, r=20, t=30, b=20),
        template="plotly_white"
    )
    
    fig_bar.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("Instabilidade: Média de Quedas Semanais")
    
    fig_instabilidade = px.bar(
        df_filtered,
        x="Setor_Local",
        y="Quedas_Semanais_Media",
        text="Quedas_Semanais_Media",
        color_discrete_sequence=["#f0ad4e"]
    )
    
    fig_instabilidade.update_layout(
        height=420,
        xaxis=dict(
            title=dict(
                text="Setor Avaliado",
                font=dict(size=13, family="Arial")
            )
        ),
        yaxis=dict(
            title=dict(
                text="Quedas de Conexão por Semana",
                font=dict(size=13, family="Arial")
            )
        ),
        margin=dict(l=20, r=20, t=30, b=20),
        template="plotly_white"
    )
    
    fig_instabilidade.update_traces(
        textposition="outside"
    )
    
    st.plotly_chart(fig_instabilidade, use_container_width=True)

# ---------------------------------------------------------
# TABELA DE DADOS DETALHADA
# ---------------------------------------------------------
st.subheader("Detalhamento por Setor")

st.dataframe(
    df_filtered[[
        "Setor_Local", 
        "Tipo_Conexao", 
        "Velocidade_Media_Mbps", 
        "Deficit_Acesso_Percentual", 
        "Quedas_Semanais_Media",
        "Status_Conectividade"
    ]].style.format({
        "Velocidade_Media_Mbps": "{:.1f} Mbps",
        "Deficit_Acesso_Percentual": "{:.1f}%",
        "Quedas_Semanais_Media": "{:d} quedas/sem"
    }),
    use_container_width=True
)

# Nota contextual no rodape
st.info(
    "Nota de Contexto: Os indicadores refletem as principais barreiras enfrentadas pelo município, "
    "onde a dependência de tecnologias de baixa capacidade e a oscilação de sinal impactam o uso "
    "de serviços digitais básicos e sistemas de informação."
)