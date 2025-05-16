# Script para processar os arquivos FOR do Novo CAGED
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, col
from tqdm import tqdm
import ftplib
import os
import py7zr
from datetime import datetime
import unicodedata
import re
from dotenv import load_dotenv
load_dotenv()

# ========================== CONFIG ==========================
tipo_arquivo = "for"

base_dir = "/home/pedromurta/projects/observatorio/caged/data/observatorio_caged"
raw_base = os.path.join(base_dir, "raw")
bronze_base = os.path.join(base_dir, "bronze")

# FTP
ftp_host = "ftp.mtps.gov.br"
ftp_base_path = "/pdet/microdados"

# RAW diretórios
raw_7z_path       = os.path.join(raw_base, "7z", tipo_arquivo)
raw_txt_path      = os.path.join(raw_base, "txt", tipo_arquivo)
raw_parquet_path  = os.path.join(raw_base, "parquet", tipo_arquivo)

# Iceberg (camada bronze)
iceberg_warehouse_path = os.path.join(bronze_base, "warehouse")
iceberg_table_name     = "local.caged_raw_table"

colunas_selecionadas = [
    "competênciamov", "uf", "município", "seção", "subclasse",
    "saldomovimentação", "cbo2002ocupação", "graudeinstrução", "idade",
    "raçacor", "sexo", "salário", "valorsaláriofixo"
]

colunas_renomeadas = {
    "competênciamov": "competencia", "município": "municipio",
    "seção": "secao", "subclasse": "sub_classe", "saldomovimentacao": "saldo_movimentacao",
    "cbo2002ocupacao": "codigo_cbo", "graudeinstrução": "escolaridade",
    "raçacor": "etnia", "salário": "salario", "valorsaláriofixo": "salario_fixo"
}

# ========================== SPARK ==========================
spark = SparkSession.builder \
    .appName("CAGED Iceberg + Parquet") \
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.local.type", "hadoop") \
    .config("spark.sql.catalog.local.warehouse", iceberg_warehouse_path) \
    .getOrCreate()

spark.sparkContext.setLogLevel("FATAL")

# ========================== UTILS ==========================
def log(msg):
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}")

def normalizar_nome_coluna(nome):
    try:
        nome_corrigido = nome.encode('latin1').decode('utf-8')
    except:
        nome_corrigido = nome
    nome_corrigido = unicodedata.normalize('NFKD', nome_corrigido).encode('ASCII', 'ignore').decode('utf-8')
    nome_corrigido = re.sub(r'[^a-z0-9]+', '_', nome_corrigido.lower().strip())
    nome_corrigido = re.sub(r'_+', '_', nome_corrigido).strip('_')
    return nome_corrigido

# ========================== FTP ==========================
def conectar_ftp():
    ftp = ftplib.FTP(ftp_host)
    ftp.encoding = "latin-1"
    ftp.login()
    return ftp

def get_meses_ftp_disponiveis(ftp):
    meses_disponiveis = []

    try:
        ftp.cwd(ftp_base_path)
        pastas = ftp.nlst()

        if "NOVO CAGED" in pastas:
            caged_path = f"{ftp_base_path}/NOVO CAGED"
            ftp.cwd(caged_path)
        else:
            raise Exception("❌ Pasta 'NOVO CAGED' não encontrada no FTP.")

        anos = ftp.nlst()
        for ano in anos:
            if not ano.isdigit() or int(ano) < 2020:
                continue

            try:
                ftp.cwd(f"{caged_path}/{ano}")
                meses = ftp.nlst()
                for mes in meses:
                    if len(mes) == 6 and mes.isdigit():
                        meses_disponiveis.append(mes)
            except Exception as e:
                tqdm.write(f"(Aviso) Erro ao acessar {ano}: {e}")
                continue

        return sorted(meses_disponiveis)

    except Exception as e:
        log(f"❌ Erro ao listar meses no FTP: {e}")
        return []

def baixar_arquivo(ftp, ano_mes):
    filename = f"CAGEDFOR{ano_mes}.7z"
    destino = os.path.join(raw_7z_path, ano_mes)
    os.makedirs(destino, exist_ok=True)
    local_path = os.path.join(destino, filename)

    if os.path.exists(local_path):
        tqdm.write(f"📦 Arquivo já baixado: {filename}")
        return local_path

    try:
        ftp.cwd(f"{ftp_base_path}/NOVO CAGED/{ano_mes[:4]}/{ano_mes}")
        with open(local_path, "wb") as f:
            ftp.retrbinary(f"RETR {filename}", f.write)
        tqdm.write(f"✅ Download completo: {filename}")
        return local_path
    except Exception as e:
        tqdm.write(f"❌ Erro ao baixar {filename}: {e}")
        return None

def extrair_arquivo(caminho_7z, ano_mes):
    pasta_destino = os.path.join(raw_txt_path, ano_mes)
    os.makedirs(pasta_destino, exist_ok=True)
    caminho_txt = os.path.join(pasta_destino, f"CAGEDFOR{ano_mes}.txt")

    if os.path.exists(caminho_txt):
        tqdm.write(f"📂 Já extraído: {caminho_txt}")
        return caminho_txt

    try:
        with py7zr.SevenZipFile(caminho_7z, mode='r') as z:
            z.extractall(path=pasta_destino)
        tqdm.write(f"✅ Extração completa: {caminho_txt}")
        return caminho_txt
    except Exception as e:
        tqdm.write(f"❌ Erro ao extrair {caminho_7z}: {e}")
        return None

# ========================== DATAFRAME ==========================
def carregar_e_processar(spark, caminho_txt):
    try:
        df = spark.read.csv(
            caminho_txt,
            sep=';',
            header=True,
            inferSchema=True,
            encoding='latin1'
        )
        colunas_normalizadas = [normalizar_nome_coluna(c) for c in df.columns]
        df = df.toDF(*colunas_normalizadas)

        mapa_colunas = {normalizar_nome_coluna(k): v for k, v in colunas_renomeadas.items()}
        colunas_necessarias = [normalizar_nome_coluna(c) for c in colunas_selecionadas]
        colunas_disponiveis = [c for c in colunas_necessarias if c in df.columns]
        df = df.select(*colunas_disponiveis)

        for antiga in colunas_disponiveis:
            if antiga in mapa_colunas:
                df = df.withColumnRenamed(antiga, mapa_colunas[antiga])

        for col_decimal in ["salario", "salario_fixo"]:
            if col_decimal in df.columns:
                df = df.withColumn(col_decimal, regexp_replace(col(col_decimal), ",", ".").cast("double"))

        return df
    except Exception as e:
        tqdm.write(f"❌ Erro ao processar arquivo: {e}")
        return None

def salvar_em_parquet(df, ano_mes):
    try:
        caminho_saida = os.path.join(raw_parquet_path, ano_mes)
        os.makedirs(caminho_saida, exist_ok=True)
        df.write.mode("overwrite").parquet(caminho_saida)
        tqdm.write(f"💾 Salvo .parquet em: {caminho_saida}")
        return True
    except Exception as e:
        tqdm.write(f"❌ Erro ao salvar parquet: {e}")
        return False

def salvar_no_iceberg(df, ano_mes):
    try:
        spark.read.table(iceberg_table_name)
        df.writeTo(iceberg_table_name).append()
        tqdm.write(f"🧊 Append no Iceberg: {ano_mes}")
    except:
        df.writeTo(iceberg_table_name).partitionedBy("competencia").createOrReplace()
        tqdm.write(f"🧊 Criada tabela Iceberg com {ano_mes}")

# ========================== ICEBERG ==========================
def get_particoes_iceberg(spark):
    try:
        df_particoes = spark.sql(f"SELECT DISTINCT competencia FROM {iceberg_table_name}")
        valores = [row["competencia"] for row in df_particoes.collect()]
        return sorted([str(v) for v in valores if v is not None])
    except Exception as e:
        tqdm.write(f"(Aviso) Nenhuma partição encontrada: {e}")
        return []

# ========================== EXECUÇÃO ==========================
try:
    ftp = conectar_ftp()
    ftp_meses = get_meses_ftp_disponiveis(ftp)
    iceberg_meses = get_particoes_iceberg(spark)
    meses_para_processar = sorted(list(set(ftp_meses) - set(iceberg_meses)))

    log(f"🛰️  Meses no FTP: {len(ftp_meses)}")
    log(f"❄️  Meses no Iceberg: {len(iceberg_meses)}")
    log(f"🚀 Meses a processar: {len(meses_para_processar)}")

    for ano_mes in tqdm(meses_para_processar, desc="🔄 Processando meses FOR", unit="mês"):
        caminho_7z = baixar_arquivo(ftp, ano_mes)
        if not caminho_7z:
            continue

        caminho_txt = extrair_arquivo(caminho_7z, ano_mes)
        if not caminho_txt:
            continue

        df = carregar_e_processar(spark, caminho_txt)
        if df:
            if salvar_em_parquet(df, ano_mes):
                salvar_no_iceberg(df, ano_mes)

    ftp.quit()

except Exception as e:
    log(f"❌ Erro geral: {e}")

finally:
    spark.stop()
