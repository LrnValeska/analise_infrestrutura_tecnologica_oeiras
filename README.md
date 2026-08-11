# Diagnóstico de Infraestrutura Tecnológica — Oeiras do Pará

Painel interativo para visualização e análise dos gargalos de conectividade e infraestrutura tecnológica no município de Oeiras do Pará.

---

## 📌 Sobre o Projeto

A aplicação apresenta indicadores focados nos desafios do acesso à internet e estabilidade de rede em diferentes setores locais (escolas públicas, unidades de saúde, prédios administrativos e residências).

A interface prioriza clareza visual e facilidade de leitura, sem distrações ou excesso de elementos gráficos, permitindo a compreensão imediata do déficit estrutural da região.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **Streamlit** (Visualização e interface)
* **Plotly** (Gráficos interativos)
* **Pandas** (Manipulação de dados)
* **Vercel** (Hospedagem e deploy contínuo)

---

## 📁 Estrutura do Repositório

```text
├── .streamlit/
│   └── config.toml         # Configuração visual do Streamlit
├── analise_infra_oeiras.py # Módulo de processamento/dados
├── app.py                  # Aplicação principal Streamlit
├── index.py                # Ponto de entrada para Serverless na Vercel
├── vercel.json             # Configuração de rotas do deploy
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação
