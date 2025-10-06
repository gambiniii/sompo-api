"""
Script para converter arquivos XLSX para CSV
"""
import pandas as pd
import os

# Diretório dos dados
data_dir = "data"
output_dir = "data/csv"

# Criar diretório de saída se não existir
os.makedirs(output_dir, exist_ok=True)

# Arquivos XLSX para converter
files = {
    "ACIDENTES.xlsx": "acidentes.csv",
    "ROUBOS.xlsx": "roubos.csv",
    "TRÁFEGO.xlsx": "trafego.csv"
}

for xlsx_file, csv_file in files.items():
    xlsx_path = os.path.join(data_dir, xlsx_file)
    csv_path = os.path.join(output_dir, csv_file)

    if os.path.exists(xlsx_path):
        print(f"Convertendo {xlsx_file} para {csv_file}...")
        df = pd.read_excel(xlsx_path)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"[OK] {csv_file} criado com sucesso! ({len(df)} linhas)")
    else:
        print(f"[ERRO] Arquivo {xlsx_file} não encontrado!")

print("\nConversão concluída!")
