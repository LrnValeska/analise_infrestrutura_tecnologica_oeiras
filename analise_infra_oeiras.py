import os
import pandas as pd

# ==========================================
# 1. CONFIGURAÇÃO DE CAMINHOS E ARQUIVOS
# ==========================================
# Uso de caminho relativo ou fallback para flexibilidade
DIRETORIO_PADRAO = r"C:\Users\lored\baixa_infrestrutura_oeiras\microdados_censo_escolar_2025_"

if os.path.exists(DIRETORIO_PADRAO):
    diretorio = DIRETORIO_PADRAO
else:
    diretorio = "."  # Procura no mesmo diretório do script caso mude de máquina

caminho_escola = os.path.join(diretorio, "Tabela_Escola_2025.csv")
caminho_docente = os.path.join(diretorio, "Tabela_Docente_2025.csv")

if not os.path.exists(caminho_escola):
    raise FileNotFoundError(f"Arquivo não localizado: {caminho_escola}")

print("Carregando Tabela_Escola_2025.csv...")

# Lendo os dados de Escola (CÓDIGO IBGE de Oeiras do Pará = 1505304)
df_escola = pd.read_csv(caminho_escola, sep=';', encoding='latin1', low_memory=False)
df_oeiras_escola = df_escola[df_escola['CO_MUNICIPIO'] == 1505304].copy()

total_escolas = len(df_oeiras_escola)
print(f"Total de escolas analisadas em Oeiras do Pará: {total_escolas}")

# ==========================================
# 2. MAPEAMENTO DE INDICADORES DE INFRAESTRUTURA
# ==========================================
# Mapeamos o nome direto que o dashboard de UI/UX usará
indicadores_infra = {
    'IN_LABORATORIO_INFORMATICA': 'Laboratório de Informática',
    'IN_EQUIP_LOUCA': 'Lousa Digital / Multimídia',
    'IN_DESKTOP_ALUNO': 'Computadores para Alunos',
    'IN_INTERNET': 'Acesso à Internet',
    'IN_INTERNET_BANDA_LARGA': 'Internet Banda Larga',
    'IN_INTERNET_ALUNOS': 'Internet para Alunos',
    'IN_ENERGIA_INEXISTENTE': 'Sem Energia Elétrica'
}

colunas_disponiveis = [col for col in indicadores_infra.keys() if col in df_oeiras_escola.columns]

resumo_infra = []

for col in colunas_disponiveis:
    # Para IN_ENERGIA_INEXISTENTE, a lógica de ausência é invertida no censo
    if col == 'IN_ENERGIA_INEXISTENTE':
        qtd_sem = (df_oeiras_escola[col] == 1).sum()
        qtd_com = total_escolas - qtd_sem
    else:
        qtd_com = (df_oeiras_escola[col] == 1).sum()
        qtd_sem = total_escolas - qtd_com

    pct_com = (qtd_com / total_escolas) * 100 if total_escolas > 0 else 0
    pct_sem = (qtd_sem / total_escolas) * 100 if total_escolas > 0 else 0

    resumo_infra.append({
        'Indicador': indicadores_infra[col],
        'Qtd_Com': qtd_com,
        'Qtd_Sem': qtd_sem,
        'Pct_Atendido': f"{round(pct_com, 1)}%",
        'Pct_Deficit': f"{round(pct_sem, 1)}%",
        'Valor_Deficit_Num': round(pct_sem, 1)
    })

df_resumo_infra = pd.DataFrame(resumo_infra)

# ==========================================
# 3. EXPORTAÇÃO COMPATÍVEL COM O APP.PY
# ==========================================
# Criamos a estrutura exata exigida pela interface de UI/UX
# O app.py consome primariamente o indicador e a porcentagem formatada
df_exportacao = pd.DataFrame({
    'Indicador': df_resumo_infra['Indicador'],
    'Porcentagem': df_resumo_infra['Pct_Deficit']  # Foco na vulnerabilidade/déficit
})

arquivo_saida = "tabela_infraestrutura_oeiras.csv"
df_exportacao.to_csv(arquivo_saida, index=False, encoding='utf-8-sig')

print("\n" + "="*55)
print("  TABELA PROCESSADA COM SUCESSO PARA O APP.PY  ")
print("="*55)
print(df_exportacao.to_string(index=False))
print(f"\nArquivo salvo como '{arquivo_saida}' para consumo imediato do Streamlit.")