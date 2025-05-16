# %% [markdown]
# # Importações 

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
    .appName("Análise motoristas") \
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

# 2. Lista de CBOs de motoristas
cbos_motoristas = [
    782310, 782315, 782305, 782405, 782410, 782415, 782320, 782510
]

# 3. Adiciona coluna de ano
df_ano = df_silver.withColumn("ano", substring("competencia", 1, 4))

# 4. Filtra apenas motoristas da seção 'H'
df_motoristas = df_ano.filter(
    (col("codigo_cbo").cast("int").isin(cbos_motoristas)) & (col("secao") == "H")
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
    F.round(F.sum("admissao"), -1).alias("admissao"),
    F.round(F.sum("demissao"), -1).alias("demissao"),
    F.round(F.sum("admissao") - F.sum("demissao"), -1).alias("saldo_total"),
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
resultado_formatado = agregacoes.join(admissoes_pivot, on="ano", how="left") \
    .join(demissoes_pivot, on="ano", how="left") \
    .select(
        "ano", "salario_medio", "salario_minimo", "poder_compra",
        "admissao", "demissao", "saldo_total", "idade_media",
        *ordem_faixas,
        *[f"dem_{faixa}" for faixa in ordem_faixas]
    ) \
    .orderBy("ano")

# 11. Mostrar resultado
resultado_formatado.show(truncate=False)


# %%
resultado_formatado.cache()

# %%
df = resultado_formatado.toPandas()

# %%
df.head()

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
# # Saldo idade x Tempo - Admissões

# %%
pivot = (
    df[['ano', '18-24', '25-29', '30-39', '40-49', '50-64', '65+']]
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
    cells=dict(values=list(zip(*styled_values)), align='center', height=30)
)])

fig.update_layout(
    title="📊 Distribuição de Admissões por Faixa Etária (Motoristas)",
    margin=dict(l=20, r=20, t=60, b=20),
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
    title="Distribuição de Admissões por Faixa Etária (Motoristas)",
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
# # Saldo idade x Tempo - Demissões

# %%
pivot_d = (
    df[['ano', 'dem_18-24',
       'dem_25-29', 'dem_30-39', 'dem_40-49', 'dem_50-64', 'dem_65+']]
    .groupby(['ano'])
    .sum()
).reset_index()

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
    title="📊 Distribuição de Demissões por Faixa Etária (Motoristas)",
    margin=dict(l=20, r=20, t=60, b=20),
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
# # Evolução Acumulada

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
    title="<b>📊 Evolução da Idade Média - Motoristas</b><br>",
    xaxis_title="Ano",
    yaxis_title="Idade Média",
    template="plotly_white",
    height=620,
    width=1800,
    
)

fig.show()

# %%
# Gráfico 3: Saldo Total vs Idade Média
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=df["ano"], y=df["saldo_total"], mode='lines+markers', name="Saldo Total",
                          marker=dict(size=10), line=dict(width=3)))
fig3.add_trace(go.Scatter(x=df["ano"], y=df["idade_media"], mode='lines+markers', name="Idade Média",
                          marker=dict(size=10), line=dict(width=3), yaxis="y2"))
fig3.update_layout(
    title="<b>📊 Saldo Total vs. Média de Idade - Motoristas</b>",
    xaxis_title="Ano",
    yaxis=dict(title="Saldo Total", tickfont=dict(color="blue")),
    yaxis2=dict(title="Idade Média", tickfont=dict(color="red"), overlaying="y", side="right"),
    template="plotly_white",
    height=620,
    width=1800,
    annotations=anotacao
)

# %% [markdown]
# # Saldo Acumulado x Poder de Compra

# %%
df_plot = df[df['ano'] <= 2024].copy()
df_plot["idade"] = df_plot["idade_media"].round(2)

fig = go.Figure()

# Barras de Idade Média
fig.add_trace(go.Bar(
    x=df_plot["ano"],
    y=df_plot["idade"],
    name="Idade Média",
    marker_color="lightblue",
    text=df_plot["idade"],
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
    line=dict(color="tomato", width=2, dash="solid"),
    yaxis="y2"
))

# Layout com dois eixos
fig.update_layout(
    title="<b>📊 Evolução da Idade Média vs Poder de Compra - Motoristas</b><br>",
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


# %%
df_saldo_anual = df[df.ano <= 2024][['ano', 'admissao', 'demissao']].copy()
df_saldo_anual['saldo'] = df_saldo_anual['admissao'] - df_saldo_anual['demissao']


fig = px.bar(
    df_saldo_anual,
    x='ano',
    y='saldo',
    text='saldo',
    title='📊 Evolução do Saldo de Motoristas por Ano',
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


# %%



