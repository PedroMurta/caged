import os
import shutil
from datetime import datetime

# Caminhos base
local_download_path = "data/bronze/tmp/caged_download/"
local_extracted_path = "data/bronze/tmp/caged_extracted/"
local_parquet_output = "data/bronze/tmp/caged_parquet/"

def log(msg):
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}")

def deletar_arquivos_recursivo(caminho_base, extensoes):
    total_apagados = 0
    log(f"🔍 Procurando arquivos em: {caminho_base}")
    
    for raiz, dirs, arquivos in os.walk(caminho_base, topdown=False):
        for nome in arquivos:
            if any(nome.endswith(ext) for ext in extensoes):
                caminho_arquivo = os.path.join(raiz, nome)
                try:
                    os.remove(caminho_arquivo)
                    log(f"🧹 Removido: {caminho_arquivo}")
                    total_apagados += 1
                except Exception as e:
                    log(f"⚠️ Erro ao remover {caminho_arquivo}: {e}")

        # Remove pastas vazias
        if not os.listdir(raiz):
            try:
                os.rmdir(raiz)
                log(f"📁 Pasta vazia removida: {raiz}")
            except Exception as e:
                log(f"⚠️ Erro ao remover pasta {raiz}: {e}")

    return total_apagados

def deletar_parquet(caminho_base):
    total_apagados = 0
    log(f"🔍 Removendo diretórios Parquet em: {caminho_base}")
    for raiz, dirs, arquivos in os.walk(caminho_base, topdown=False):
        for d in dirs:
            caminho_dir = os.path.join(raiz, d)
            try:
                shutil.rmtree(caminho_dir)
                log(f"🧹 Diretório Parquet removido: {caminho_dir}")
                total_apagados += 1
            except Exception as e:
                log(f"⚠️ Erro ao remover diretório {caminho_dir}: {e}")

    return total_apagados

if __name__ == "__main__":
    log("🚀 Iniciando limpeza de arquivos temporários...\n")

    total_removidos = 0
    total_removidos += deletar_arquivos_recursivo(local_download_path, [".7z"])
    total_removidos += deletar_arquivos_recursivo(local_extracted_path, [".txt"])
    total_removidos += deletar_parquet(local_parquet_output)

    log(f"\n✅ Limpeza concluída. Total de itens apagados: {total_removidos}")
