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
ftp_host = "ftp.mtps.gov.br"
ftp_base_path = "/pdet/microdados"

local_download_path = "data/bronze/tmp/caged_download_old/"
local_extracted_path = "data/bronze/tmp/caged_extracted_old/"
local_parquet_output = "data/bronze/tmp/caged_parquet_old/"

iceberg_warehouse_path = "/home/pedromurta/projects/observatorio/caged/data/bronze/tmp/iceberg_warehouse"
iceberg_table_name = "local.caged_table_partitioned_old"

def criar_tabela_iceberg_vazia(spark, tabela_nome):
    try:
        spark.read.table(tabela_nome)
        print(f"Tabela '{tabela_nome}' já existe, não precisa criar.")
    except Exception as e:
        print(f"Criando tabela '{tabela_nome}'...")
        spark.sql(f"""
            CREATE TABLE {tabela_nome} (
                competencia STRING,
                uf STRING,
                municipio STRING,
                subclasse_cnae STRING,
                saldo_movimentacao INT,
                codigo_cbo STRING,
                escolaridade STRING,
                idade INT,
                etnia STRING,
                sexo STRING,
                salario DOUBLE
            )
            USING iceberg
            PARTITIONED BY (competencia)
        """)



colunas_selecionadas = [
    "competência declarada", "uf", "município", "cnae 2.0 subclas",
    "saldo mov", "cbo 2002 ocupação", "grau instrução", "idade",
    "raça cor", "sexo", "salário mensal"
]

colunas_renomeadas = {
    "competência declarada": "competencia", "município": "municipio",
    "cnae 2.0 subclas": "subclasse_cnae", "saldo mov": "saldo_movimentacao",
    "cbo 2002 ocupação": "codigo_cbo", "grau instrução": "escolaridade",
    "raça cor": "etnia", "salário mensal": "salario"
}

# ========================== SPARK ==========================
spark = SparkSession.builder \
    .appName("CAGED Antigo Iceberg") \
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.local.type", "hadoop") \
    .config("spark.sql.catalog.local.warehouse", iceberg_warehouse_path) \
    .getOrCreate()

criar_tabela_iceberg_vazia(spark, iceberg_table_name)


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

def get_meses_antigos_disponiveis(ftp):
    meses_disponiveis = []
    try:
        ftp.cwd(f"{ftp_base_path}/CAGED")
        pastas_ano = ftp.nlst()

        for ano in pastas_ano:
            if not ano.isdigit() or not (2010 <= int(ano) <= 2019):
                continue

            try:
                ftp.cwd(f"{ftp_base_path}/CAGED/{ano}")
                arquivos = ftp.nlst()

                for arquivo in arquivos:
                    match = re.match(r"CAGEDEST_(\d{6})\.7z", arquivo)
                    if match:
                        competencia = match.group(1)
                        mes = competencia[:2]
                        ano_comp = competencia[2:]
                        meses_disponiveis.append(f"{ano_comp}{mes}")
            except Exception as e:
                tqdm.write(f"(Aviso) Erro ao acessar {ano}: {e}")
                continue

        return sorted(meses_disponiveis)
    except Exception as e:
        log(f"Erro ao listar meses antigos: {e}")
        return []

def baixar_arquivo_mes_antigo(ftp, ano_mes):
    mes = ano_mes[4:]
    ano = ano_mes[:4]
    filename = f"CAGEDEST_{mes}{ano}.7z"
    local_path = os.path.join(local_download_path, filename)

    if os.path.exists(local_path):
        tqdm.write(f"Já baixado: {filename}")
        return local_path

    try:
        ftp.cwd(f"{ftp_base_path}/CAGED/{ano}")
        with open(local_path, "wb") as f:
            ftp.retrbinary(f"RETR {filename}", f.write)
        tqdm.write(f"Download: {filename}")
        return local_path
    except Exception as e:
        tqdm.write(f"Erro ao baixar {filename}: {e}")
        return None

def extrair_arquivo_mes_antigo(caminho_7z, ano_mes):
    pasta_destino = os.path.join(local_extracted_path, ano_mes)
    os.makedirs(pasta_destino, exist_ok=True)

    try:
        with py7zr.SevenZipFile(caminho_7z, mode='r') as z:
            z.extractall(path=pasta_destino)
        arquivos_txt = [os.path.join(pasta_destino, f) for f in os.listdir(pasta_destino) if f.endswith('.txt')]
        if arquivos_txt:
            return arquivos_txt[0]
    except Exception as e:
        tqdm.write(f"Erro na extração {caminho_7z}: {e}")
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

        if "salario" in df.columns:
            df = df.withColumn("salario", regexp_replace(col("salario"), ",", ".").cast("double"))

        return df
    except Exception as e:
        tqdm.write(f"Erro ao processar: {e}")
        return None

def salvar_em_parquet(df, ano_mes):
    try:
        caminho_saida = os.path.join(local_parquet_output, ano_mes)
        df.write.mode("overwrite").parquet(caminho_saida)
        return True
    except Exception as e:
        tqdm.write(f"Erro ao salvar parquet: {e}")
        return False

def salvar_no_iceberg(df, ano_mes):
    try:
        # tenta ler a tabela
        spark.read.table(iceberg_table_name)
        df.writeTo(iceberg_table_name).append()
        tqdm.write(f"🧊 Append no Iceberg: {ano_mes}")
    except Exception as e:
        tqdm.write(f"🧊 Criando tabela Iceberg (primeira vez): {ano_mes}")
        df.writeTo(iceberg_table_name).partitionedBy("competencia").create()

def get_particoes_iceberg(spark):
    try:
        df_particoes = spark.sql(f"SELECT DISTINCT competencia FROM {iceberg_table_name}")
        valores = [row["competencia"] for row in df_particoes.collect()]
        return sorted([str(v) for v in valores if v is not None])
    except Exception as e:
        tqdm.write(f"Nenhuma partição encontrada: {e}")
        return []

# ========================== EXECUÇÃO ==========================
os.makedirs(local_download_path, exist_ok=True)
os.makedirs(local_extracted_path, exist_ok=True)
os.makedirs(local_parquet_output, exist_ok=True)

try:
    ftp = conectar_ftp()
    meses_antigos = get_meses_antigos_disponiveis(ftp)
    iceberg_meses = get_particoes_iceberg(spark)

    print(f"Meses disponíveis: {meses_antigos}")
    print(f"Mês já no Iceberg: {iceberg_meses}")

    meses_para_processar = sorted(set(meses_antigos) - set(iceberg_meses))
    print(f"Mês a processar   : {meses_para_processar}")

    for ano_mes in tqdm(meses_para_processar, desc="Processando CAGED Antigo", unit="mês"):
        caminho_7z = baixar_arquivo_mes_antigo(ftp, ano_mes)
        if not caminho_7z:
            continue

        caminho_txt = extrair_arquivo_mes_antigo(caminho_7z, ano_mes)
        if not caminho_txt:
            continue

        df = carregar_e_processar(spark, caminho_txt)
        if df:
            if salvar_em_parquet(df, ano_mes):
                salvar_no_iceberg(df, ano_mes)
                try:
                    os.remove(caminho_7z)
                    os.remove(caminho_txt)
                    pasta = os.path.dirname(caminho_txt)
                    if not os.listdir(pasta):
                        os.rmdir(pasta)
                except Exception as e:
                    tqdm.write(f"Erro na limpeza: {e}")

    ftp.quit()
except Exception as e:
    log(f"Erro geral: {e}")
finally:
    spark.stop()
