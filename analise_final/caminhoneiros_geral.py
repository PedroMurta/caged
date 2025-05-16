# %% [markdown]
# # Importações e Carregamento dos dados

# %%
# 📌 Bibliotecas Padrão do Python
from tqdm import tqdm
import pandas as pd
import numpy as np
import warnings
from dotenv import load_dotenv
load_dotenv()

# 📌 Visualização
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import linregress
from scipy.stats import pearsonr
import statsmodels.api as sm
from statsmodels.tsa.stattools import grangercausalitytests


# 📌 Bibliotecas Padrão do PySpark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round, date_format, to_date, create_map, lit, when, lower, regexp_replace, substring, concat_ws
from pyspark.sql import functions as F
from pyspark.sql import Window
from itertools import chain


from datetime import datetime
def log(msg):
    tqdm.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}")
    
    

# 📌 Configurações Globais para Melhor Exibição dos Dados
warnings.simplefilter(action="ignore", category=UserWarning)  # Ignorar avisos gerais do usuário
warnings.simplefilter(action="ignore", category=FutureWarning)  # Ignorar avisos de futuras mudanças

# Exibição de ponto flutuante sem notação científica
pd.options.display.float_format = "{:.2f}".format
# Configuração do número máximo de colunas e linhas exibidas
pd.set_option("display.max_columns", 500)
pd.set_option("display.max_rows", 65)

# Configuração do backend de gráficos
pd.options.plotting.backend = "plotly"
pd.options.display.colheader_justify = "center"

# %%
# Caminhos das camadas
silver_warehouse_path = "/home/pedromurta/projects/observatorio/caged/data/observatorio_caged/silver"
gold_warehouse_path   = "/home/pedromurta/projects/observatorio/caged/data/observatorio_caged/gold"

# Inicialização da SparkSession
spark = SparkSession.builder \
    .appName("Análise Caminhoneiros") \
    .config("spark.sql.catalog.silver", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.silver.type", "hadoop") \
    .config("spark.sql.catalog.silver.warehouse", silver_warehouse_path) \
    .config("spark.sql.catalog.gold", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.gold.type", "hadoop") \
    .config("spark.sql.catalog.gold.warehouse", gold_warehouse_path) \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.memory.fraction", "0.6") \
    .config("spark.memory.storageFraction", "0.3") \
    .config("spark.driver.memory", "8g") \
    .config("spark.executor.memory", "8g") \
    .config("spark.driver.memoryOverhead", "2g") \
    .config("spark.executor.memoryOverhead", "2g") \
    .getOrCreate()


# %%
df_silver = spark.read.table("silver.default.caged_silver")

# %%
from pyspark.sql import functions as F
from pyspark.sql.functions import col, when, substring, round
from pyspark.sql.window import Window

# 1. Adiciona coluna de faixa etária
df_silver = df_silver.withColumn(
    "faixa_etaria",
    when(col("idade") <= 17, "até 17")
    .when(col("idade").between(18, 24), "18-24")
    .when(col("idade").between(25, 29), "25-29")
    .when(col("idade").between(30, 39), "30-39")
    .when(col("idade").between(40, 49), "40-49")
    .when(col("idade").between(50, 64), "50-64")
    .otherwise("65+")
)


# 3. Adiciona coluna de ano
df_ano = df_silver.withColumn("ano", substring("competencia", 1, 4))

# 4. Filtra apenas motoristas da seção 'H'
df_motoristas = df_ano.filter(
    (col("codigo_cbo").cast("int").isin(782510)) & (col("secao") == "H")
)

# 5. Mapeamento do salário mínimo por ano
df_motoristas = df_motoristas.withColumn("salario_minimo", 
    when(col("ano") == "2010", 510.00)
    .when(col("ano") == "2011", 545.00)
    .when(col("ano") == "2012", 622.00)
    .when(col("ano") == "2013", 678.00)
    .when(col("ano") == "2014", 724.00)
    .when(col("ano") == "2015", 788.00)
    .when(col("ano") == "2016", 880.00)
    .when(col("ano") == "2017", 937.00)
    .when(col("ano") == "2018", 954.00)
    .when(col("ano") == "2019", 998.00)
    .when(col("ano") == "2020", 1045.00)
    .when(col("ano") == "2021", 1100.00)
    .when(col("ano") == "2022", 1212.00)
    .when(col("ano") == "2023", 1320.00)
    .when(col("ano") == "2024", 1412.00)
    .when(col("ano") == "2025", 1518.00)
)

# 6. Agregações principais
agregacoes = df_motoristas.groupBy("ano").agg(
    F.round(F.avg("salario"), 2).alias("salario_medio"),
    F.first("salario_minimo").alias("salario_minimo"),
    F.round(F.avg("salario") / F.first("salario_minimo"), 2).alias("poder_compra"),
    F.round(F.sum("admissao"), -2).alias("admissao"),
    F.round(F.sum("demissao"), -2).alias("demissao"),
    F.round(F.sum("admissao") - F.sum("demissao"), -2).alias("saldo_total"),
    F.round(F.avg("idade"), 2).alias("idade_media")
)

# 7. Admissões por faixa etária (pivot)
admissoes_faixa = df_motoristas.groupBy("ano", "faixa_etaria") \
    .agg(F.round(F.sum("admissao"), -2).alias("admissoes"))

admissoes_pivot = admissoes_faixa.groupBy("ano").pivot("faixa_etaria") \
    .agg(F.first("admissoes"))

# 8. Demissões por faixa etária (pivot)
demissoes_faixa = df_motoristas.groupBy("ano", "faixa_etaria") \
    .agg(F.round(F.sum("demissao"), -2).alias("demissoes"))

demissoes_pivot = demissoes_faixa.groupBy("ano").pivot("faixa_etaria") \
    .agg(F.first("demissoes"))

# 9. Garantir todas as faixas presentes em ambos os pivôs
ordem_faixas = ["até 17", "18-24", "25-29", "30-39", "40-49", "50-64", "65+"]
for faixa in ordem_faixas:
    if faixa not in admissoes_pivot.columns:
        admissoes_pivot = admissoes_pivot.withColumn(faixa, F.lit(None))
    if faixa not in demissoes_pivot.columns:
        demissoes_pivot = demissoes_pivot.withColumn(faixa, F.lit(None))
    else:
        demissoes_pivot = demissoes_pivot.withColumnRenamed(faixa, f"dem_{faixa}")

# 10. Unir resultados finais
resultado_formatado_caminhoneiros = agregacoes.join(admissoes_pivot, on="ano", how="left") \
    .join(demissoes_pivot, on="ano", how="left") \
    .select(
        "ano", "salario_medio", "salario_minimo", "poder_compra",
        "admissao", "demissao", "saldo_total", "idade_media",
        *ordem_faixas,
        *[f"dem_{faixa}" for faixa in ordem_faixas]
    ) \
    .orderBy("ano")

# 11. Mostrar resultado
resultado_formatado_caminhoneiros.show(truncate=False)

# %%
resultado_formatado_caminhoneiros.cache()

# %%
df = resultado_formatado_caminhoneiros.toPandas()

# %%
anotacao = [
    dict(
        text="*Valores aproximados para fins ilustrativos.</br></br>",
        showarrow=False,
        xref="paper", yref="paper",
        x=0, y=1.05,
        xanchor='left', yanchor='top',
        font=dict(size=12, color="gray")
    )
]


# %% [markdown]
# # Saldo idade x Tempo - ADMISSÕES

# %%
pivot = (
    df[['ano', 'até 17', '18-24', '25-29', '30-39', '40-49', '50-64', '65+']]
    .groupby(['ano'])
    .sum()
).reset_index()
pivot

# %%
# Garante que os dados estão como strings antes de limpar
pivot_str = pivot.reset_index(drop=False).copy()
colunas_numericas = ['18-24', '25-29', '30-39', '40-49', '50-64', '65+']

# Remove '.' e converte para int
for col in colunas_numericas:
    pivot_str[col] = pivot_str[col].astype(str).str.replace('.', '', regex=False).astype(int)

pivot_str['ano'] = pivot_str['ano'].astype(int)

# Estiliza a tabela com destaque no maior valor
styled_values = []
for _, row in pivot_str.iterrows():
    valores = row[colunas_numericas]
    max_val = valores.max()

    styled_row = [str(row['ano'])]
    for val in valores:
        if val == max_val:
            formatted = f"<b><span style='color:blue'>{val:,}</span></b>"
        else:
            formatted = f"{val:,}"
        styled_row.append(formatted.replace(",", "."))  # separador

    styled_values.append(styled_row)

# Cabeçalhos
headers = ['Ano'] + colunas_numericas

# Gera gráfico tipo tabela
fig = go.Figure(data=[go.Table(
    header=dict(values=headers, fill_color='lightgrey', align='center'),
    cells=dict(values=list(zip(*styled_values)), align='center', height=10)
)])

fig.update_layout(
    title="📊 Distribuição de Admissões por Faixa Etária",
    margin=dict(l=10, r=10, t=60, b=5),
    height=620,
    width=1800,
    annotations=anotacao
)

fig.show()


# %%
# Calcula totais por ano
pivot_pct = pivot_str.copy()
pivot_pct['total'] = pivot_pct[colunas_numericas].sum(axis=1)

# Converte para porcentagem com duas casas decimais
for col in colunas_numericas:
    pivot_pct[col] = pivot_pct[col] / pivot_pct['total'] * 100

# Gráfico 100% empilhado horizontal com porcentagem
fig = go.Figure()

for col in colunas_numericas:
    fig.add_trace(go.Bar(
        y=pivot_pct['ano'],
        x=pivot_pct[col],
        name=col,
        orientation='h',
        text=pivot_pct[col].apply(lambda x: f"{x:.2f}%"),
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white'),
        hovertemplate=f"{col}<br>%{{x:.2f}}%",
    ))

fig.update_layout(
    barmode='stack',
    title="Distribuição Percentual de Admissões por Faixa Etária",
    xaxis_title="Proporção",
    yaxis_title="Ano",
    template="plotly_white",
    height=620,
    width=1800,
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5
    )
)

fig.show()

# %% [markdown]
# ---------------

# %% [markdown]
# # Saldo idade x Tempo - DEMISSÕES

# %%
pivot_d = (
    df[['ano','dem_até 17', 'dem_18-24',
       'dem_25-29', 'dem_30-39', 'dem_40-49', 'dem_50-64', 'dem_65+']]
    .groupby(['ano'])
    .sum()
).reset_index()
pivot_d

# %%
pivot_d.rename(columns={
    'dem_até 17': 'até 17',
    'dem_18-24': '18-24',
    'dem_25-29': '25-29', 
    'dem_30-39': '30-39', 
    'dem_40-49': '40-49', 
    'dem_50-64': '50-64', 
    'dem_65+': '65+'
}, inplace=True)

# %%
# Garante que os dados estão como strings antes de limpar
pivot_str = pivot_d.reset_index(drop=False).copy()
colunas_numericas = ['18-24',
                    '25-29', '30-39', '40-49', '50-64', '65+']

# Remove '.' e converte para int
for col in colunas_numericas:
    pivot_str[col] = pivot_str[col].astype(str).str.replace('.', '', regex=False).astype(int)

pivot_str['ano'] = pivot_str['ano'].astype(int)

# Estiliza a tabela com destaque no maior valor
styled_values = []
for _, row in pivot_str.iterrows():
    valores = row[colunas_numericas]
    max_val = valores.max()

    styled_row = [str(row['ano'])]
    for val in valores:
        if val == max_val:
            formatted = f"<b><span style='color:blue'>{val:,}</span></b>"
        else:
            formatted = f"{val:,}"
        styled_row.append(formatted.replace(",", "."))  # separador

    styled_values.append(styled_row)

# Cabeçalhos
headers = ['Ano'] + colunas_numericas

# Gera gráfico tipo tabela
fig = go.Figure(data=[go.Table(
    header=dict(values=headers, fill_color='lightgrey', align='center'),
    cells=dict(values=list(zip(*styled_values)), align='center', height=30)
)])

fig.update_layout(
    title="📊 Distribuição de Demissões por Faixa Etária",
    margin=dict(l=10, r=10, t=60, b=10),
    height=620,
    width=1800,
    annotations=anotacao
)

fig.show()

# %%
# Calcula totais por ano
pivot_pct = pivot_str.copy()
pivot_pct['total'] = pivot_pct[colunas_numericas].sum(axis=1)

# Converte para porcentagem com duas casas decimais
for col in colunas_numericas:
    pivot_pct[col] = pivot_pct[col] / pivot_pct['total'] * 100

# Gráfico 100% empilhado horizontal com porcentagem
fig = go.Figure()

for col in colunas_numericas:
    fig.add_trace(go.Bar(
        y=pivot_pct['ano'],
        x=pivot_pct[col],
        name=col,
        orientation='h',
        text=pivot_pct[col].apply(lambda x: f"{x:.2f}%"),
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white'),
        hovertemplate=f"{col}<br>%{{x:.2f}}%",
    ))

fig.update_layout(
    barmode='stack',
    title="Distribuição Percentual de Demissões por Faixa Etária",
    xaxis_title="Proporção",
    yaxis_title="Ano",
    template="plotly_white",
    height=620,
    width=1800,
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    annotations=anotacao
)

fig.show()

# %% [markdown]
# ## Evolução Acumulada

# %% [markdown]
# ----------------

# %%
df.ano = df.ano.astype(int)

df_evolucao = df.groupby('ano').agg(
    idade=('idade_media', 'first'),
    admissoes=("admissao", "sum"),
    demissoes=("demissao", "sum"),
    saldo_final=("saldo_total", "sum"),
).reset_index()

# Calcula a variação percentual com base no ano anterior
df_evolucao["evolucao_percentual"] = df_evolucao["idade"].pct_change().fillna(0) * 100
df_evolucao["evolucao_percentual_idade"] = df_evolucao["evolucao_percentual"]


# Dados do seu DataFrame já calculado
df_evolucao["texto_legenda"] = df_evolucao["evolucao_percentual_idade"].apply(
    lambda x: f"<span style='color:green;font-weight:bold'>↑ {x:.2f}%</span>" if x > 0
    else (f"<span style='color:red;font-weight:bold'>↓ {abs(x):.2f}%</span>" if x < 0 else "")
)

# Texto com variação percentual formatada
df_evolucao["texto_legenda"] = df_evolucao["evolucao_percentual_idade"].apply(
    lambda x: f"<span style='color:green;font-weight:bold'>↑ {x:.2f}%</span>" if x > 0
    else (f"<span style='color:red;font-weight:bold'>↓ {abs(x):.2f}%</span>" if x < 0 else "")
)

# Gráfico de barras com idade média dentro da barra
fig = go.Figure()

fig.add_trace(go.Bar(
    x=df_evolucao["ano"],
    y=df_evolucao["idade"].round(2),
    name="Idade Média",
    marker_color="royalblue",
    text=df_evolucao["idade"].round(2),
    textposition="inside",
    insidetextanchor="middle",
    textangle=0,
    texttemplate="%{text:.2f}"
))

# Adicionar texto da variação percentual acima da barra
for i, row in df_evolucao.iterrows():
    if i == 0:
        continue  # pula o primeiro ano
    fig.add_annotation(
        x=row["ano"],
        y=row["idade"] + 1.05,  # ajusta altura da anotação
        text=row["texto_legenda"],
        showarrow=False,
        align="center",
        font=dict(size=12),
        xanchor='center'
    )

fig.update_layout(
    title="<b>📊 Evolução da Idade Média - Caminhoneiros</b><br>",
    xaxis_title="Ano",
    yaxis_title="Idade Média",
    template="plotly_white",
    height=620,
    width=1800,
    
)

fig.show()


# %% [markdown]
# 

# %%
# Gráfico 3: Saldo Total vs Idade Média
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=df["ano"], y=df["saldo_total"], mode='lines+markers', name="Saldo Total",
                          marker=dict(size=9), line=dict(width=4)))
fig3.add_trace(go.Scatter(x=df["ano"], y=df["idade_media"], mode='lines+markers', name="Idade Média",
                          marker=dict(size=9), line=dict(width=4), yaxis="y2"))
fig3.update_layout(
    title="<b>📊 Saldo Total vs. Idade Média - Caminhoneiros</b>",
    xaxis_title="Ano",
    yaxis=dict(title="Saldo Total", tickfont=dict(color="blue")),
    yaxis2=dict(title="Idade Média", tickfont=dict(color="red"), overlaying="y", side="right"),
    template="plotly_white",
    height=620,
    width=1800,
    annotations=anotacao
)

# %% [markdown]
# ## Saldo Acumulado de Caminhoneiros

# %%
df.head()

# %%
df['saldo_acumulado'] = df['saldo_total'].cumsum()

# %%
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["ano"],
    y=df["saldo_acumulado"],
    mode="lines+markers",
    name="Saldo Acumulado",
    line=dict(color="royalblue", width=4)
))

# Anotações ajustadas
fig.add_annotation(
    x=2014,
    y=df[df["ano"] == 2014]["saldo_acumulado"].values[0],
    text=(
        "🔻 Queda no saldo acumulado (2014–2016)<br>"
        "Possível reflexo da crise econômica nacional."
    ),
    showarrow=True,
    arrowhead=1,
    ax=-130,
    ay=-30,
    bgcolor="rgba(255,255,255,0.6)",
    bordercolor="red",
    font=dict(size=12)
)

fig.add_annotation(
    x=2016,
    y=df[df["ano"] == 2016]["saldo_acumulado"].values[0],
    text=(
        "📉 Estagnação após queda;<br>"
        "Baixo dinamismo econômico no período; <br>"
        "Chegada do Uber e outros aplicativos."
    ),
    showarrow=True,
    arrowhead=1,
    ax=70,
    ay=80,
    bgcolor="rgba(255,255,255,0.6)",
    bordercolor="red",
    font=dict(size=12)
)

fig.add_annotation(
    x=2019,
    y=df[df["ano"] == 2019]["saldo_acumulado"].values[0],
    text=(
        "📈 Início da recuperação (2018–2020)<br>"
        "Alta demanda por logística e transporte."
    ),
    showarrow=True,
    arrowhead=1,
    ax=-60,
    ay=-100,
    bgcolor="rgba(255,255,255,0.6)",
    bordercolor="green",
    font=dict(size=12)
)

fig.add_annotation(
    x=2022,
    y=df[df["ano"] == 2022]["saldo_acumulado"].values[0],
    text=(
        "🚀 Aceleração (2023–)<br>"
        "Retomada econômica (pós-pandemia) + crescimento do e-commerce."
    ),
    showarrow=True,
    arrowhead=1,
    ax=70,
    ay=-130,
    bgcolor="rgba(255,255,255,0.7)",
    bordercolor="green",
    font=dict(size=12)
)

fig.update_layout(
    title="📈 Saldo Acumulado de Motoristas de Caminhão",
    xaxis_title="Ano",
    yaxis_title="Saldo Acumulado",
    template="plotly_white",
    height=620,
    width=1800,
    annotations=anotacao
)

fig.show()

# %%
fig = px.line(
    df[df.ano <= 2024],
    x='ano',
    y='poder_compra',
    markers=True,
    title='Evolução do Poder de Compra dos Motoristas',
    labels={'ano': 'Ano', 'poder_compra': 'Poder de Compra (Salário / Salário Mínimo)'}
)
fig.update_traces(line=dict(width=2, color='darkblue'))
fig.show()

# %%
df.info()

# %%
import plotly.graph_objects as go

df_plot = df[df['ano'] <= 2024].copy()
df_plot["idade"] = df_plot["idade_media"].round(2)

fig = go.Figure()

# Barras de Idade Média
fig.add_trace(go.Bar(
    x=df_plot["ano"],
    y=df_plot["saldo_total"],
    name="Saldo",
    marker_color="lightblue",
    text=df_plot["saldo_total"],
    textposition="inside",
    insidetextanchor="middle",
    texttemplate="%{text:.2f}",
    yaxis="y1"
))

# Linha de Poder de Compra
fig.add_trace(go.Scatter(
    x=df_plot["ano"],
    y=df_plot["poder_compra"],
    name="Poder de Compra",
    mode="lines+markers",
    line=dict(color="red", width=2, dash="solid"),
    yaxis="y2"
))

# Layout com dois eixos
fig.update_layout(
    title="<b>📊 Evolução do saldo vs Poder de Compra - Caminhoneiros</b><br>",
    xaxis=dict(title="Ano"),
    yaxis=dict(
        title="",  # remove título do eixo esquerdo
        side="left",
        showgrid=False
    ),
    yaxis2=dict(
        title="",  # remove título do eixo direito
        overlaying="y",
        side="right",
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ),
    bargap=0.2,
    template="plotly_white",
    height=620,
    width=1800,
    annotations=anotacao
)

fig.show()


# %% [markdown]
# ## Evolução por ano

# %%
df_saldo_anual = df[df.ano <= 2024][['ano', 'admissao', 'demissao']].copy()
df_saldo_anual['saldo'] = df_saldo_anual['admissao'] - df_saldo_anual['demissao']


fig = px.bar(
    df_saldo_anual,
    x='ano',
    y='saldo',
    text='saldo',
    title='📊 Evolução do Saldo de Caminhoneiros por Ano',
    labels={'ano': 'Ano', 'saldo': 'Saldo'},
    color='saldo',  # coloração automática (positivo/negativo)
    color_continuous_scale='RdBu'
)

fig.update_traces(texttemplate='%{text:,}', textposition='outside')
fig.update_layout(
    yaxis_tickformat=',.0f',
    template='plotly_white',
    height=620,
    width=1800,
    annotations=anotacao
)

fig.show()

# %% [markdown]
# # TESTES

# %%


# %%


# %%
https://economia.ig.com.br/2019-05-12/brasileiro-tem-primeiro-emprego-com-carteira-assinada-em-media-apos-os-28-anos.html? - O ingresso do jovem brasileiro no mercado de trabalho formal acontece cada vez mais tarde. Em média, 
a primeira carteira assinada só acontece aos 28,6 anos, segundo levantamento da consultoria iDados a partir dos dados de 2017 da Relação Anual de Informações Sociais (Rais), os mais recentes. 
Antes da crise, entre 2006 e 2014, a idade média d o primeiroemprego formal girava em torno de 25 anos.

Estatísticas do IBGE mostram que a taxa de desemprego na faixa etária entre 18 e 24 anos é mais que o dobro do índice geral, que abrange todos os mais de 13 milhões de trabalhadores sem ocupação no país .

# %%
📊 Admissões por Faixa Etária – Principais Insights
1. Entrada de jovens (18–24) caiu drasticamente entre 2010 e 2018
De 12.400 (2010) para 4.300 (2018) → Queda de quase 65%.

Recuperação gradual a partir de 2020, mas queda abrupta em 2025 (3.200).

🔎 Interpretação: menor entrada de jovens no setor, com possível desinteresse ou falta de incentivo/formação.

2. Admissões nas faixas 30–39 e 40–49 são as maiores
30–39 lidera em praticamente todos os anos.

Em 2024, admissão recorde em 40–49: 104.300 (mais do que todas as faixas jovens somadas).

🔎 Interpretação: o mercado está contratando mais trabalhadores experientes e, ao mesmo tempo, rejeitando ou não atraindo os mais jovens.

3. Admissões 65+ triplicaram entre 2010 e 2024
2010: 500

2024: 3.500

Mesmo que o volume seja menor, a tendência de aumento nas admissões em faixas mais idosas é preocupante do ponto de vista de renovação da força de trabalho.

📌 Interpretação para o relatório:
“Os dados de admissões reforçam a hipótese de envelhecimento da categoria. Desde 2010, a participação dos jovens (18–24) 
sofreu queda acentuada, enquanto as admissões nas faixas de 40 a 49 anos cresceram significativamente, atingindo o maior patamar em 2024.
Além disso, chama atenção o aumento nas admissões de pessoas com 65 anos ou mais, revelando uma possível postergação da aposentadoria.
O setor parece não estar conseguindo renovar sua base de profissionais.”

# %% [markdown]
# 📊 Insights do Gráfico de Saldo de Caminhoneiros (2010–2024)
# ✅ 1. Período de estabilidade e crescimento (2010–2014)
# Saldo positivo e relativamente estável entre 12 mil e 22 mil.
# 
# O setor ainda conseguia contratar mais do que demitir, mesmo com envelhecimento inicial da força de trabalho.
# 
# ⚠️ 2. Crise de saldo negativo (2015–2016)
# 2015: saldo de –14.100
# 
# 2016: saldo de –21.000 (pior da série)
# 
# Essa queda coincide com a recessão econômica brasileira e já mostra sinais de saída em massa sem reposição equivalente, especialmente entre os jovens (como vimos nos gráficos de faixas etárias).
# 
# 🔎 Conexão: as admissões de jovens caíram fortemente nesses anos, e os trabalhadores mais velhos começaram a dominar a categoria.
# 
# 📈 3. Recuperação gradual (2017–2020)
# Saldo volta a ficar positivo, mas com patamares menores (~15 mil a 18 mil).
# 
# Indica que o setor se recuperou parcialmente, mas sem recompor plenamente a força de trabalho jovem.
# 
# 🚛 4. Picos de saldo em 2021–2022
# 2021: 29.700
# 
# 2022: 28.500
# 
# Possivelmente impulsionado por:
# 
# Reaquecimento pós-pandemia
# 
# Alta demanda por transporte rodoviário
# 
# Mas como vimos nos outros gráficos, o aumento de admissões se concentrou nas faixas de 40+, e não houve renovação geracional real.
# 
# 🔻 5. Queda recente em 2023–2024
# 2023: 17.200
# 
# 2024: 11.600
# 
# Embora o saldo ainda seja positivo, há tendência de desaceleração, o que reforça a hipótese de esgotamento da base de contratação, especialmente se a oferta jovem continuar baixa.
# 
# 
# O saldo positivo geral entre 2017 e 2024 esconde uma fragilidade estrutural: ele foi sustentado pela contratação de trabalhadores mais velhos, com a base jovem cada vez menor. A queda no saldo em 2024 pode indicar que até mesmo essa estratégia de manter profissionais mais experientes está se esgotando, tornando iminente a escassez de caminhoneiros.

# %% [markdown]
# 📊 Insights combinados – Idade Média vs Poder de Compra
# 📈 1. Tendência clara de envelhecimento
# A idade média aumentou de 37,27 anos (2010) para 40,95 anos (2024).
# 
# Isso confirma com dados objetivos a hipótese de envelhecimento da categoria.
# 
# 💡 Mesmo nos anos de crise (2015–2016), a idade média continua subindo.
# 
# 📉 2. Poder de compra caiu nos últimos anos
# O poder de compra era ~2,03 em 2010 e caiu para ~1,82 em 2024.
# 
# Mesmo com salários nominais maiores, os reajustes do salário mínimo e a inflação reduziram o poder de compra real.
# 
# 🔧 Isso pode explicar por que os jovens não estão entrando na profissão: menos atratividade financeira e aumento do custo de vida.
# 
# 🔄 3. Divergência entre envelhecimento e remuneração
# Enquanto a idade média sobe, o poder de compra cai.
# 
# Isso sugere que a permanência dos profissionais mais velhos pode estar associada à falta de alternativas, e os jovens podem estar buscando ocupações com maior retorno financeiro ou menor desgaste físico.
# 
# 🧠 Conclusão para seu relatório
# Entre 2010 e 2024, observou-se um envelhecimento constante dos motoristas de caminhão, cuja idade média passou de 37 para quase 41 anos. Paralelamente, houve redução do poder de compra, o que pode ter afetado negativamente a atratividade da profissão entre os mais jovens. A combinação desses dois fatores ajuda a explicar a escassez de novos profissionais e a permanência dos mais velhos no setor, mesmo em idade próxima à aposentadoria.

# %% [markdown]
# 🔍 1. Falta de Renovação Geracional
# Admissões na faixa 18–24 caíram de 12.400 (2010) para 13.000 (2024), mas com forte queda entre 2010 e 2018. A recuperação recente não acompanha o volume de demissões, que ficou entre 7.900 e 9.300 nos últimos anos.
# 
# Mesmo em 2024, mais de 9 mil jovens saíram do setor, enquanto só 13 mil foram contratados. Isso mal compensa as perdas naturais, e não expande a base.
# 
# 🎯 Conclusão: há uma base jovem pequena, instável e insuficiente para garantir sucessão no setor.
# 
# 📈 2. Crescimento de Faixas Etárias Elevadas
# Faixas de 40–49 e 50–64 anos tiveram aumento expressivo nas admissões e nas demissões:
# 
# 40–49: de 43.200 (admissões em 2010) para 104.300 em 2024
# 
# 50–64: de 21.300 para 55.700
# 
# Demissões acompanharam esse crescimento, o que mostra que esses trabalhadores sustentam o setor, mas estão mais perto da saída do mercado.
# 
# 📌 Conclusão: o setor está apoiado em profissionais mais velhos, que estão cada vez mais saindo.
# 
# ⚠️ 3. Aumento consistente da faixa 65+
# Admissões e demissões na faixa 65+ mais do que sextuplicaram:
# 
# Admissões: 500 (2010) → 3.500 (2024)
# 
# Demissões: 600 (2010) → 5.400 (2024)
# 
# 🔧 Interpretação: há postergamento da aposentadoria ou recontratação de aposentados para preencher lacunas — um sinal claro de escassez de mão de obra jovem.
# 
# Entre 2010 e 2024, observa-se um envelhecimento progressivo da força de trabalho no setor de transporte, com crescimento significativo nas admissões e demissões de trabalhadores acima dos 40 anos, especialmente entre 50 e 64 anos. A entrada de jovens (18–24) não cresce de forma proporcional às saídas, o que compromete a renovação da categoria. Esse cenário indica que o setor está cada vez mais dependente de profissionais em idade avançada, o que pode agravar a escassez de motoristas no curto e médio prazo.

# %% [markdown]
# 📊 Insights adicionais – Variação da Idade Média
# 📈 1. Crescimento contínuo da idade média
# De 37,48 anos em 2010 para 41,56 anos em 2024.
# 
# Crescimento percentual consistente ao longo da série, com picos em:
# 
# 2016 (+2,08%)
# 
# 2015 (+1,54%)
# 
# 2017 (+1,39%)
# 
# 🧠 Isso sugere que o envelhecimento não é pontual, mas sim uma tendência estrutural.
# 
# 📉 2. Quedas pontuais não sustentam reversão
# As únicas quedas foram em 2021 e 2023 (–0,43% e –0,19%).
# 
# Mas logo após, a idade média volta a crescer.
# 
# 🔎 Isso mostra que qualquer rejuvenescimento foi pontual e insuficiente para reverter a tendência de envelhecimento.
# 
# 🧩 Conclusão integrada:
# A trajetória da idade média reforça a conclusão de que o setor está envelhecendo de forma contínua e progressiva. A ausência de uma renovação geracional robusta, combinada com a permanência de trabalhadores mais velhos, indica que o mercado de motoristas pode enfrentar uma escassez severa se medidas de incentivo à entrada de jovens não forem adotadas.

# %% [markdown]
# 


