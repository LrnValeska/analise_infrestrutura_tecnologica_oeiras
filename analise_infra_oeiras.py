import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. CONFIGURAÇÃO DE CAMINHOS E ARQUIVOS
# ==========================================
diretorio = r"C:\Users\lored\baixa_infrestrutura_oeiras\microdados_censo_escolar_2025_"

caminho_escola = os.path.join(diretorio, "Tabela_Escola_2025.csv")
caminho_docente = os.path.join(diretorio, "Tabela_Docente_2025.csv")

if not os.path.exists(caminho_escola):
    raise FileNotFoundError(f"Arquivo não encontrado: {caminho_escola}")

print("Carregando Tabela_Escola_2025.csv...")

# Lendo os dados de Escola (CÓDIGO IBGE de Oeiras do Pará = 1505304)
df_escola = pd.read_csv(caminho_escola, sep=';', encoding='latin1', low_memory=False)
df_oeiras_escola = df_escola[df_escola['CO_MUNICIPIO'] == 1505304].copy()

total_escolas = len(df_oeiras_escola)
print(f"\nTotal de escolas registradas em Oeiras do Pará: {total_escolas}")

# ==========================================
# 2. ANÁLISE DE INFRAESTRUTURA TECNOLÓGICA (Tabela Escola)
# ==========================================
indicadores_infra = {
    'IN_LABORATORIO_INFORMATICA': 'Possui Lab. de Informática',
    'IN_EQUIP_LOUCA': 'Lousa Digital / Multimídia',
    'IN_DESKTOP_ALUNO': 'Computadores para Alunos',
    'IN_INTERNET': 'Possui Acesso à Internet',
    'IN_INTERNET_BANDA_LARGA': 'Internet Banda Larga',
    'IN_INTERNET_ALUNOS': 'Internet Acessível a Alunos',
    'IN_ENERGIA_INEXISTENTE': 'Sem Energia Elétrica'
}

colunas_disponiveis = [col for col in indicadores_infra.keys() if col in df_oeiras_escola.columns]

resumo_infra = []
for col in colunas_disponiveis:
    qtd_sim = (df_oeiras_escola[col] == 1).sum()
    pct = (qtd_sim / total_escolas) * 100 if total_escolas > 0 else 0
    resumo_infra.append({
        'Indicador': indicadores_infra[col],
        'Quantidade': qtd_sim,
        'Porcentagem (%)': round(pct, 2)
    })

df_resumo_infra = pd.DataFrame(resumo_infra)

print("\n" + "="*55)
print("  INFRAESTRUTURA TECNOLÓGICA - OEIRAS DO PARÁ (2025)  ")
print("="*55)
print(df_resumo_infra.to_string(index=False))

# Salvar tabela formatada
df_resumo_infra.to_csv("tabela_infraestrutura_oeiras.csv", index=False, encoding='utf-8-sig')

# ==========================================
# 3. ANÁLISE COMPLEMENTAR DE DOCENTES (Opcional - Tabela Docente)
# ==========================================
if os.path.exists(caminho_docente):
    print("\nCarregando Tabela_Docente_2025.csv...")
    df_docente = pd.read_csv(caminho_docente, sep=';', encoding='latin1', low_memory=False)
    df_oeiras_docente = df_docente[df_docente['CO_MUNICIPIO'] == 1505304].copy()
    
    total_docentes = len(df_oeiras_docente)
    print(f"Total de registros docentes em Oeiras do Pará: {total_docentes}")

# ==========================================
# 4. GERAÇÃO DE GRÁFICO DA INFRAESTRUTURA
# ==========================================
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

ax = sns.barplot(
    data=df_resumo_infra, 
    x='Porcentagem (%)', 
    y='Indicador', 
    palette='Blues_r'
)

plt.title("Infraestrutura Tecnológica nas Escolas de Oeiras do Pará", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Porcentagem de Escolas com o Recurso (%)", fontsize=11)
plt.ylabel("", fontsize=11)
plt.xlim(0, 100)

# Inserir percentual nas barras
for p in ax.patches:
    width = p.get_width()
    ax.annotate(
        f'{width:.1f}%', 
        (width + 1.5, p.get_y() + p.get_height() / 2.),
        ha='left', va='center', fontsize=10, color='black', fontweight='bold'
    )

plt.tight_layout()
plt.savefig("grafico_infraestrutura_oeiras.png", dpi=300)
print("\nGráfico salvo como 'grafico_infraestrutura_oeiras.png'")
plt.show()