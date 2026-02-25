import py7zr
import duckdb
import pandas as pd
import os
import ftplib
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from datetime import datetime

# ── Configurações ──────────────────────────────────────────────────────────────
FTP_HOST             = "ftp.mtps.gov.br"
FTP_BASE_PATH        = "/pdet/microdados/RAIS"
ANOS                 = [2022, 2023, 2024]
DIR_DOWNLOAD         = "./rais_downloads"
DIR_EXTRACAO         = "./rais_extraido"
DIR_PARCIAL          = "./rais_parcial"
DIR_SAIDA            = "./rais_parquet"
CAMINHO_EXCEL        = "dicionario_rais.xlsx"
MAX_WORKERS_DOWNLOAD = 6
MAX_WORKERS_PROCESSO = 2
DUCKDB_THREADS       = 8
DUCKDB_MEMORY        = '32GB'

subclasses_alvo = (
    '3600602','4930201','4930202','4930203','4930204','5212500','5229002','5320201','5320202',
    '4681801','4681802','4681803','4681804','4681805','4682600',
    '4921301','4921302','4922101','4922102','4922103','4923001','4924800',
    '4929901','4929902','4929903','4929904','4929999','5229099','8622400',
    '4911600','4912401','4912402','4912403',
    '8012900',
    '4923002','7711000',
    '5011401','5011402','5012201','5012202',
    '5021101','5021102','5022001','5022002',
    '5091201','5091202','5099801','5099899',
    '5111100','5112901','5112999','5120000'
)

COLUNAS_LAYOUT = {
    'novo': {
        'subclasse':     '"CNAE 2.0 Subclasse - Código"',
        'cbo':           '"CBO 2002 Ocupação - Código"',
        'nat_juridica':  '"Natureza Jurídica - Código"',
        'vinculo_ativo': '"Ind Vínculo Ativo 31/12 - Código"',
        'municipio':     '"Município - Código"',
        'rem_media':     '"Vl Rem Média Nom"',
        'rem_dez':       '"Vl Rem Dezembro Nom"',
        'idade':         '"Idade"',
        'sexo':          '"Sexo - Código"',
        'etnia':         '"Raça Cor - Código"',
        'escolaridade':  '"Escolaridade Após 2005 - Código"',
    },
    'antigo': {
        'subclasse':     '"CNAE 2.0 Subclasse"',
        'cbo':           '"CBO Ocupação 2002"',
        'nat_juridica':  '"Natureza Jurídica"',
        'vinculo_ativo': '"Vínculo Ativo 31/12"',
        'municipio':     '"Município"',
        'rem_media':     '"Vl Remun Média Nom"',
        'rem_dez':       '"Vl Remun Dezembro Nom"',
        'idade':         '"Idade"',
        'sexo':          '"Sexo Trabalhador"',
        'etnia':         '"Raça Cor"',
        'escolaridade':  '"Escolaridade após 2005"',
    }
}

for d in [DIR_DOWNLOAD, DIR_EXTRACAO, DIR_PARCIAL, DIR_SAIDA]:
    os.makedirs(d, exist_ok=True)

def log(msg):
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)

# ── Dicionários (carrega uma vez) ──────────────────────────────────────────────
log("Carregando dicionários...")
df_cbo = pd.read_excel(CAMINHO_EXCEL, sheet_name='cbo')
df_sub = pd.read_excel(CAMINHO_EXCEL, sheet_name='subclasse2.0')

# ── Funções ────────────────────────────────────────────────────────────────────
def detectar_csv(txt_path):
    con = duckdb.connect()
    con.execute("SET threads=2")
    con.execute("SET memory_limit='4GB'")
    try:
        colunas = con.execute(f"""
            SELECT * FROM read_csv('{txt_path}',
                                   sep=';', header=True, encoding='latin-1',
                                   quote='"', all_varchar=True, sample_size=1)
            LIMIT 0
        """).description
        nomes = [c[0] for c in colunas]
        sep = ';' if len(nomes) > 1 else None
    except:
        nomes = []
        sep = None

    if not sep:
        colunas = con.execute(f"""
            SELECT * FROM read_csv('{txt_path}',
                                   sep=',', header=True, encoding='latin-1',
                                   quote='"', all_varchar=True, sample_size=1)
            LIMIT 0
        """).description
        nomes = [c[0] for c in colunas]
        sep = ','

    con.close()
    layout = 'novo' if 'CNAE 2.0 Subclasse - Código' in nomes else 'antigo'
    log(f"  🗂️  Layout: {layout} | Separador: '{sep}'")
    return sep, layout


def baixar_arquivo(nome_arquivo, ftp_path, ano):
    caminho_local = os.path.join(DIR_DOWNLOAD, f"{ano}_{nome_arquivo}")
    try:
        ftp = ftplib.FTP(FTP_HOST, encoding='latin-1')
        ftp.login()
        ftp.cwd(ftp_path)
        with open(caminho_local, 'wb') as f:
            ftp.retrbinary(f"RETR {nome_arquivo}", f.write)
        ftp.quit()
        log(f"  ✅ Download: {nome_arquivo} ({os.path.getsize(caminho_local)/1024**2:.2f} MB)")
        return caminho_local
    except Exception as e:
        log(f"  ❌ Erro download {nome_arquivo}: {e}")
        return None


def processar_arquivo(args):
    caminho_7z, nome_arquivo, ano = args
    slug            = nome_arquivo.replace(".7z", "")
    caminho_extr    = os.path.join(DIR_EXTRACAO, f"{ano}_{slug}")
    caminho_parcial = os.path.join(DIR_PARCIAL,  f"rais_{ano}_{slug}.parquet")
    os.makedirs(caminho_extr, exist_ok=True)

    try:
        log(f"  📦 Extraindo {nome_arquivo}...")
        with py7zr.SevenZipFile(caminho_7z, mode='r') as z:
            z.extractall(path=caminho_extr)

        todos = [
            os.path.join(r, f)
            for r, _, files in os.walk(caminho_extr) for f in files
        ]
        txt_path = max(todos, key=os.path.getsize)
        log(f"  📄 {os.path.basename(txt_path)} ({os.path.getsize(txt_path)/1024**2:.2f} MB)")

        sep, layout = detectar_csv(txt_path)
        col = COLUNAS_LAYOUT[layout]

        con = duckdb.connect()
        con.execute(f"SET threads={DUCKDB_THREADS}")
        con.execute(f"SET memory_limit='{DUCKDB_MEMORY}'")
        con.execute(f"""
            COPY (
                SELECT
                    {ano}                                    AS ano,
                    {col['subclasse']}                       AS subclasse,
                    {col['cbo']}                             AS cbo,
                    {col['nat_juridica']}                    AS nat_juridica,
                    {col['vinculo_ativo']}                   AS vinculo_ativo,
                    {col['municipio']}                       AS cod_mun,
                    SUBSTRING({col['municipio']}, 1, 2)      AS uf,
                    {col['rem_media']}                       AS rem_media,
                    {col['rem_dez']}                         AS rem_dez,
                    {col['idade']}                           AS idade,
                    {col['sexo']}                            AS sexo,
                    {col['etnia']}                           AS etnia,
                    {col['escolaridade']}                    AS escolaridade
                FROM read_csv('{txt_path}',
                              sep='{sep}', header=True, encoding='latin-1',
                              quote='"', all_varchar=True,
                              sample_size=-1, parallel=True, ignore_errors=True)
                WHERE
                    {col['subclasse']}        IN {subclasses_alvo}
                    AND {col['nat_juridica']}  NOT IN ('3999', '2143')
                    AND {col['vinculo_ativo']} = '1'
            ) TO '{caminho_parcial}' (FORMAT 'PARQUET', COMPRESSION 'ZSTD')
        """)
        con.close()
        log(f"  💾 Parcial: {os.path.basename(caminho_parcial)} ({os.path.getsize(caminho_parcial)/1024**2:.2f} MB)")
        return caminho_parcial

    except Exception as e:
        log(f"  ❌ Erro processando {nome_arquivo}: {e}")
        return None

    finally:
        if os.path.exists(caminho_7z):
            os.remove(caminho_7z)
        for f in [os.path.join(r, fi) for r, _, files in os.walk(caminho_extr) for fi in files]:
            os.remove(f)
        log(f"  🗑️  Temporários removidos: {slug}")


def transformar_ano(ano, parciais):
    log(f"⚙️  Transformando {ano} ({len(parciais)} regionais)...")

    con = duckdb.connect(database=':memory:')
    con.execute(f"SET threads={DUCKDB_THREADS * 2}")
    con.execute(f"SET memory_limit='{DUCKDB_MEMORY}'")
    con.register('dic_cbo',       df_cbo)
    con.register('dic_subclasse', df_sub)

    lista_parciais = str(parciais).replace("'", '"')

    df_final = con.execute(f"""
        WITH calculado AS (
            SELECT
                ano,
                TRIM(REPLACE(vinculo_ativo, '"', '')) AS vinculo_ativo,
                TRIM(REPLACE(subclasse,     '"', '')) AS codigo_subclasse,
                TRIM(REPLACE(cbo,           '"', '')) AS codigo_cbo,
                uf                                    AS cod_uf,
                CAST(REPLACE(NULLIF(TRIM(REPLACE(rem_media, '"', '')), ''), ',', '.') AS DOUBLE) AS salario,
                CAST(REPLACE(NULLIF(TRIM(REPLACE(rem_dez,   '"', '')), ''), ',', '.') AS DOUBLE) AS salario_fixo,
                TRIM(REPLACE(idade,         '"', '')) AS idade,
                TRIM(REPLACE(etnia,         '"', '')) AS cod_etnia,
                TRIM(REPLACE(escolaridade,  '"', '')) AS cod_escolaridade,
                CASE WHEN sexo LIKE '%1%' THEN 'Masculino' ELSE 'Feminino' END AS sexo,
                CASE
                    WHEN TRIM(REPLACE(subclasse,'"','')) IN ('4681801','4681802','4681803','4681804','4681805','4682600')
                         AND TRIM(REPLACE(cbo,'"','')) IN ('782310','782110','782205','782220','782405','782410','782415',
                                                           '782505','782510','782515','782610','782615','782625')
                         THEN 'Distribuição de Petróleo'
                    WHEN TRIM(REPLACE(subclasse,'"','')) IN ('3600602','4930201','4930202','4930203','4930204','5212500','5229002','5320201','5320202')
                         THEN 'Transporte de Cargas'
                    WHEN TRIM(REPLACE(subclasse,'"','')) IN ('4921301','4921302','4922101','4922102','4922103','4923001','4924800',
                                                             '4929901','4929902','4929903','4929904','4929999','5229099','8622400')
                         THEN 'Transporte de Passageiros'
                    WHEN TRIM(REPLACE(subclasse,'"','')) IN ('4911600','4912401','4912402') THEN 'Transporte Ferroviário'
                    WHEN TRIM(REPLACE(subclasse,'"','')) = '4912403'                        THEN 'Metroviário'
                    WHEN TRIM(REPLACE(subclasse,'"','')) = '8012900'                        THEN 'Transporte de Valores'
                    WHEN TRIM(REPLACE(subclasse,'"','')) IN ('4923002','7711000')           THEN 'Locação de Serviços'
                    WHEN TRIM(REPLACE(subclasse,'"','')) IN ('5011401','5011402','5012201','5012202',
                                                             '5021101','5021102','5022001','5022002',
                                                             '5091201','5091202','5099801','5099899')
                         THEN 'Transporte Aquaviário'
                    WHEN TRIM(REPLACE(subclasse,'"','')) IN ('5111100','5112901','5112999','5120000')
                         THEN 'Transporte Aeroviário'
                    ELSE 'Outro'
                END AS segmento
            FROM read_parquet({lista_parciais})
        )
        SELECT
            c.ano,
            c.vinculo_ativo,
            c.codigo_subclasse, ds.descricao_subclasse,
            c.codigo_cbo,       dc.descricao_cbo,
            c.segmento,
            c.salario, c.salario_fixo,
            CASE
                WHEN c.salario <= 522  THEN 'Classe E'
                WHEN c.salario <= 1305 THEN 'Classe D'
                WHEN c.salario <= 3130 THEN 'Classe C'
                WHEN c.salario <= 9310 THEN 'Classe B'
                ELSE 'Classe A'
            END AS classe_social,
            c.idade, c.sexo,
            CASE c.cod_etnia
                WHEN '1' THEN 'Indígena' WHEN '2' THEN 'Branca'  WHEN '4' THEN 'Preta'
                WHEN '6' THEN 'Amarela'  WHEN '8' THEN 'Parda'   ELSE 'Não Informado'
            END AS etnia,
            CASE c.cod_escolaridade
                WHEN '1'  THEN 'Analfabeto'              WHEN '2'  THEN 'Até 5ª incompleto'
                WHEN '3'  THEN '5ª completo fundamental' WHEN '4'  THEN '6ª a 9ª fundamental'
                WHEN '5'  THEN 'Fundamental completo'    WHEN '6'  THEN 'Médio incompleto'
                WHEN '7'  THEN 'Médio completo'          WHEN '8'  THEN 'Superior incompleto'
                WHEN '9'  THEN 'Superior completo'       WHEN '10' THEN 'Mestrado'
                WHEN '11' THEN 'Doutorado'               ELSE 'Não Informado'
            END AS escolaridade,
            CASE c.cod_uf
                WHEN '12' THEN 'AC' WHEN '27' THEN 'AL' WHEN '13' THEN 'AM' WHEN '16' THEN 'AP'
                WHEN '29' THEN 'BA' WHEN '23' THEN 'CE' WHEN '53' THEN 'DF' WHEN '32' THEN 'ES'
                WHEN '52' THEN 'GO' WHEN '21' THEN 'MA' WHEN '31' THEN 'MG' WHEN '50' THEN 'MS'
                WHEN '51' THEN 'MT' WHEN '15' THEN 'PA' WHEN '25' THEN 'PB' WHEN '26' THEN 'PE'
                WHEN '22' THEN 'PI' WHEN '41' THEN 'PR' WHEN '33' THEN 'RJ' WHEN '24' THEN 'RN'
                WHEN '43' THEN 'RS' WHEN '11' THEN 'RO' WHEN '14' THEN 'RR' WHEN '42' THEN 'SC'
                WHEN '35' THEN 'SP' WHEN '28' THEN 'SE' WHEN '17' THEN 'TO'
            END AS uf_sigla,
            CASE
                WHEN c.cod_uf IN ('12','13','16','15','11','14','17')           THEN 'Norte'
                WHEN c.cod_uf IN ('27','29','23','21','25','26','22','24','28') THEN 'Nordeste'
                WHEN c.cod_uf IN ('53','52','51','50')                          THEN 'Centro-Oeste'
                WHEN c.cod_uf IN ('32','31','33','35')                          THEN 'Sudeste'
                WHEN c.cod_uf IN ('41','43','42')                               THEN 'Sul'
            END AS regiao
        FROM calculado c
        LEFT JOIN dic_subclasse ds ON c.codigo_subclasse = CAST(ds.id_subclasse AS VARCHAR)
        LEFT JOIN dic_cbo        dc ON c.codigo_cbo       = CAST(dc.id_cbo       AS VARCHAR)
        WHERE c.segmento != 'Outro'
    """).df()[['ano','vinculo_ativo','codigo_subclasse','descricao_subclasse',
               'codigo_cbo','descricao_cbo','segmento','salario','salario_fixo',
               'classe_social','idade','sexo','etnia','escolaridade','uf_sigla','regiao']]

    con.close()

    caminho_final = os.path.join(DIR_SAIDA, f"rais_{ano}.parquet")
    df_final.to_parquet(caminho_final, index=False, compression='zstd')
    log(f"✅ rais_{ano}.parquet — {len(df_final):,} registros | {os.path.getsize(caminho_final)/1024**2:.2f} MB")

    for p in parciais:
        os.remove(p)
    log(f"🗑️  Parciais {ano} removidos")


# ── Pipeline principal ─────────────────────────────────────────────────────────
for ano in ANOS:
    log(f"{'='*60}")
    log(f"ANO {ano}")

    caminho_final = os.path.join(DIR_SAIDA, f"rais_{ano}.parquet")
    if os.path.exists(caminho_final):
        log(f"⏭️  rais_{ano}.parquet já existe — pulando.")
        continue

    ftp_path = f"{FTP_BASE_PATH}/{ano}"

    try:
        ftp = ftplib.FTP(FTP_HOST, encoding='latin-1')
        ftp.login()
        ftp.cwd(ftp_path)
        arquivos_7z = [f for f in ftp.nlst() if f.startswith("RAIS_VINC_PUB") and f.endswith(".7z")]
        ftp.quit()
        log(f"{len(arquivos_7z)} regionais: {arquivos_7z}")

        log("Iniciando downloads paralelos...")
        baixados = {}
        with ThreadPoolExecutor(max_workers=MAX_WORKERS_DOWNLOAD) as executor:
            futures = {
                executor.submit(baixar_arquivo, nome, ftp_path, ano): nome
                for nome in arquivos_7z
            }
            for future in as_completed(futures):
                nome   = futures[future]
                result = future.result()
                if result:
                    baixados[nome] = result

        log("Iniciando processamento paralelo de regionais...")
        parciais = []
        args_list = [(caminho_7z, nome, ano) for nome, caminho_7z in baixados.items()]
        with ProcessPoolExecutor(max_workers=MAX_WORKERS_PROCESSO) as executor:
            futures = {executor.submit(processar_arquivo, args): args[1] for args in args_list}
            for future in as_completed(futures):
                resultado = future.result()
                if resultado:
                    parciais.append(resultado)

        if parciais:
            transformar_ano(ano, parciais)
        else:
            log(f"⚠️  Nenhum parcial gerado para {ano}")

    except Exception as e:
        log(f"❌ Erro no ano {ano}: {e}")

log("🏁 Pipeline concluído!")
