"""
Script para importar dados dos CSVs para o banco de dados
"""
import os
import sys
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config.database import engine, SessionLocal
from src.database.entities.cargo_theft import CargoTheft
from src.database.entities.cargo_accidents import CargoAccidents
from src.database.entities.traffic import Traffic
from src.database.entities.routes import Routes
from src.database.entities.base import Base

# Criar todas as tabelas
Base.metadata.create_all(bind=engine)


def import_cargo_thefts(db: Session):
    """Importa dados de roubos de carga"""
    print("\n=== Importando Roubos de Carga ===")
    csv_path = "data/csv/roubos.csv"

    if not os.path.exists(csv_path):
        print(f"[ERRO] Arquivo {csv_path} não encontrado!")
        return

    df = pd.read_csv(csv_path)
    print(f"Total de linhas no CSV: {len(df)}")

    # Limpar dados existentes
    db.query(CargoTheft).delete()
    db.commit()
    print("Dados antigos removidos.")

    count = 0
    for _, row in df.iterrows():
        try:
            # Parsear a data
            date_str = str(row['DATA_OCORRENCIA'])
            occurred_at = datetime.strptime(date_str, '%Y-%m-%d').date()

            theft = CargoTheft(
                state='SP',  # Baseado nos dados de exemplo
                city=str(row['NOME_MUNICIPIO']),
                neighborhood=str(row['BAIRRO']) if pd.notna(row['BAIRRO']) else 'N/A',
                street=str(row['LOGRADOURO']) if pd.notna(row['LOGRADOURO']) else 'N/A',
                lat=float(row['LATITUDE']),
                lng=float(row['LONGITUDE']),
                occurred_at=occurred_at
            )
            db.add(theft)
            count += 1

            if count % 1000 == 0:
                db.commit()
                print(f"  {count} registros processados...")
        except Exception as e:
            print(f"[ERRO] Linha {count + 1}: {str(e)}")
            continue

    db.commit()
    print(f"[OK] {count} roubos de carga importados!")


def import_cargo_accidents(db: Session):
    """Importa dados de acidentes com carga"""
    print("\n=== Importando Acidentes com Carga ===")
    csv_path = "data/csv/acidentes.csv"

    if not os.path.exists(csv_path):
        print(f"[ERRO] Arquivo {csv_path} não encontrado!")
        return

    df = pd.read_csv(csv_path)
    print(f"Total de linhas no CSV: {len(df)}")

    # Limpar dados existentes
    db.query(CargoAccidents).delete()
    db.commit()
    print("Dados antigos removidos.")

    count = 0
    for _, row in df.iterrows():
        try:
            # Parsear a data
            date_str = str(row['data_inversa'])
            accident_date = datetime.strptime(date_str, '%Y-%m-%d').date()

            accident = CargoAccidents(
                date=accident_date,
                state=str(row['uf']),
                highway=str(row['br']),
                kilometer=int(float(row['km'])) if pd.notna(row['km']) else 0,
                city=str(row['municipio']),
                accident_cause=str(row['causa_acidente']),
                accident_type=str(row['tipo_acidente']),
                accident_classification=str(row['classificacao_acidente']),
                day_period=str(row['fase_dia']),
                road_direction=str(row['sentido_via']),
                weather_condition=str(row['condicao_metereologica']),
                road_type=str(row['tipo_pista']),
                road_layout=str(row['tracado_via']),
                land_use=str(row['uso_solo']),
                people=int(row['pessoas']),
                deaths=int(row['mortos']),
                minor_injuries=int(row['feridos_leves']),
                serious_injuries=int(row['feridos_graves']),
                unharmed=int(row['ilesos']),
                unknown=int(row['ignorados']),
                injured=int(row['feridos']),
                vehicles=int(row['veiculos']),
                latitude=float(row['latitude']),
                longitude=float(row['longitude'])
            )
            db.add(accident)
            count += 1

            if count % 1000 == 0:
                db.commit()
                print(f"  {count} registros processados...")
        except Exception as e:
            print(f"[ERRO] Linha {count + 1}: {str(e)}")
            continue

    db.commit()
    print(f"[OK] {count} acidentes importados!")


def import_traffic(db: Session):
    """Importa dados de tráfego"""
    print("\n=== Importando Dados de Tráfego ===")
    csv_path = "data/csv/trafego.csv"

    if not os.path.exists(csv_path):
        print(f"[ERRO] Arquivo {csv_path} não encontrado!")
        return

    df = pd.read_csv(csv_path)
    print(f"Total de linhas no CSV: {len(df)}")

    # Limpar dados existentes
    db.query(Traffic).delete()
    db.commit()
    print("Dados antigos removidos.")

    count = 0
    for _, row in df.iterrows():
        try:
            # Parsear a data
            date_str = str(row['Data'])
            traffic_date = datetime.strptime(date_str, '%Y-%m-%d').date()

            traffic = Traffic(
                date=traffic_date,
                direction=str(row['Sentido']),
                latitude=float(row['Latitude']),
                longitude=float(row['Longitude']),
                uf=int(row['UF']) if str(row['UF']).isdigit() else 0,
                highway=int(row['BR']),
                km=int(float(row['Km'])),
                total=int(row['Total'])
            )
            db.add(traffic)
            count += 1

            if count % 5000 == 0:
                db.commit()
                print(f"  {count} registros processados...")
        except Exception as e:
            print(f"[ERRO] Linha {count + 1}: {str(e)}")
            continue

    db.commit()
    print(f"[OK] {count} registros de tráfego importados!")


def main():
    """Função principal"""
    print("=" * 60)
    print("IMPORTAÇÃO DE DADOS PARA O BANCO DE DADOS")
    print("=" * 60)

    db = SessionLocal()

    try:
        import_cargo_thefts(db)
        import_cargo_accidents(db)
        import_traffic(db)

        print("\n" + "=" * 60)
        print("IMPORTAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
    except Exception as e:
        print(f"\n[ERRO FATAL] {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
