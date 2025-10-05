from __future__ import annotations
from pathlib import Path

import math
from datetime import datetime
from typing import Optional, Dict, Set, List, Tuple

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update

# === Importa infra do projeto ===
from src.config.database import engine
from src.database.entities.base import Base
from src.database.entities.hexagon import Hexagon
from src.database.entities.hexagon_occurrence_stats import HexagonOccurrenceStats
from src.database.entities.police_occurrence import PoliceOccurrence
from src.database.entities.police_occurrence_type import PoliceOccurrenceType

import h3

print(h3.__version__)


# H3 (Uber)
try:
    import h3
except ImportError:
    raise RuntimeError("Instale a dependência 'h3': pip install h3")


class DatabaseLogic:
    H3_RESOLUTION = 10
    MAX_BATCH = 1000  # Lote de commits

    @staticmethod
    def _coerce_str(x) -> Optional[str]:
        if x is None:
            return None
        if isinstance(x, float) and math.isnan(x):
            return None
        s = str(x).strip()
        if not s or s.upper() == "NULL":
            return None
        return s

    @staticmethod
    def _coerce_float_from_brazilian(x) -> Optional[float]:
        s = DatabaseLogic._coerce_str(x)
        if s is None:
            return None
        s = s.replace(",", ".")
        try:
            v = float(s)
            return None if v == 0.0 else v
        except ValueError:
            return None

    @staticmethod
    def _coerce_date_br(x) -> Optional[datetime.date]:
        s = DatabaseLogic._coerce_str(x)
        if s is None:
            return None
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d/%m/%y"):
            try:
                return datetime.strptime(s, fmt).date()
            except ValueError:
                continue
        return None

    @staticmethod
    def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = [c.strip().upper() for c in df.columns]
        return df

    @staticmethod
    def read_any(path: str) -> pd.DataFrame:
        if path.lower().endswith(".csv"):
            df = pd.read_csv(
                path,
                dtype=str,
                keep_default_na=False,
                na_values=["", "NULL"],
                encoding="latin1",  # <--- ADICIONADO
                sep=";",  # Tenta ponto e vírgula
                on_bad_lines="skip",  # Pula linhas com número de colunas diferente
            )

            print(df.head())
            print(df.columns)

        else:
            df = pd.read_excel(path, dtype=str)
        return DatabaseLogic.normalize_columns(df)

    @staticmethod
    def preload_types(session: Session) -> Dict[str, int]:
        """Cache: type_name -> type_id"""
        cache: Dict[str, int] = {}
        rows = session.execute(
            select(PoliceOccurrenceType.id, PoliceOccurrenceType.name)
        ).all()
        for rid, name in rows:
            cache[name] = rid
        return cache

    @staticmethod
    def preload_hexagons(session: Session) -> Set[str]:
        return {h_id for (h_id,) in session.execute(select(Hexagon.id)).all()}

    @staticmethod
    def ensure_type(session: Session, cache: Dict[str, int], name: str) -> int:
        """Garante que o tipo exista; se não, cria."""
        if name in cache:
            return cache[name]

        result = session.execute(
            insert(PoliceOccurrenceType)
            .values(name=name, description=name)
            .returning(PoliceOccurrenceType.id)
        )
        new_id = result.scalar_one()
        cache[name] = new_id
        return new_id

    @staticmethod
    def ensure_hexagon(session: Session, known_hex: Set[str], h3_id: str):
        """Garante que o hexágono exista; se não, cria."""
        if h3_id in known_hex:
            return
        session.execute(
            insert(Hexagon).values(
                id=h3_id, resolution=DatabaseLogic.H3_RESOLUTION, danger_percentage=0.0
            )
        )
        known_hex.add(h3_id)

    @staticmethod
    def compute_h3(lat: Optional[float], lng: Optional[float]) -> Optional[str]:
        if lat is None or lng is None:
            return None
        try:
            return h3.geo_to_h3(lat, lng, DatabaseLogic.H3_RESOLUTION)
        except Exception:
            return None

    @staticmethod
    def upsert_stats_bulk(session: Session, pairs: List[Tuple[str, int, int]]):
        """Upsert manual em HexagonOccurrenceStats."""
        for h3_id, type_id, cnt in pairs:
            result = session.execute(
                update(HexagonOccurrenceStats)
                .where(
                    HexagonOccurrenceStats.h3_id == h3_id,
                    HexagonOccurrenceStats.occurrence_type == "police",
                    HexagonOccurrenceStats.type_id == type_id,
                )
                .values(count=cnt)
            )
            if result.rowcount == 0:
                session.execute(
                    insert(HexagonOccurrenceStats).values(
                        h3_id=h3_id,
                        occurrence_type="police",
                        type_id=type_id,
                        count=cnt,
                    )
                )

    def import_file(path: str, update_stats: bool = True) -> None:
        print(f"[import] Lendo arquivo: {path}")
        df = DatabaseLogic.read_any(path)

        required = {
            "NATUREZA_APURADA",
            "RUBRICA",
            "DATA_OCORRENCIA_BO",
            "LATITUDE",
            "LONGITUDE",
        }
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"Colunas obrigatórias ausentes: {missing}")

        # Conversões
        df["__lat"] = df["LATITUDE"].apply(DatabaseLogic._coerce_float_from_brazilian)
        df["__lng"] = df["LONGITUDE"].apply(DatabaseLogic._coerce_float_from_brazilian)
        df["__date"] = df["DATA_OCORRENCIA_BO"].apply(DatabaseLogic._coerce_date_br)
        df["__type_name"] = df["NATUREZA_APURADA"].apply(
            lambda x: DatabaseLogic._coerce_str(x) or "N/A"
        )
        df["__desc"] = df["RUBRICA"].apply(lambda x: DatabaseLogic._coerce_str(x) or "")

        mask_valid = df["__lat"].notna() & df["__lng"].notna() & df["__date"].notna()
        dfv = df.loc[mask_valid].copy()
        dfv["__h3"] = [
            DatabaseLogic.compute_h3(la, ln)
            for la, ln in zip(dfv["__lat"], dfv["__lng"])
        ]
        dfv = dfv[dfv["__h3"].notna()].copy()

        with Session(bind=engine, expire_on_commit=False) as session:
            type_cache = DatabaseLogic.preload_types(session)
            known_hex = DatabaseLogic.preload_hexagons(session)

            to_insert: List[PoliceOccurrence] = []
            created_types = 0
            created_hex = 0

            for _, row in dfv.iterrows():
                type_name: str = row["__type_name"]
                desc: str = row["__desc"]
                occurred_at = row["__date"]
                h3_id = row["__h3"]

                # Garante tipo
                if type_name not in type_cache:
                    _ = DatabaseLogic.ensure_type(session, type_cache, type_name)
                    created_types += 1

                # Garante hexágono
                before = len(known_hex)
                DatabaseLogic.ensure_hexagon(session, known_hex, h3_id)
                if len(known_hex) > before:
                    created_hex += 1

                # Cria ocorrência
                po = PoliceOccurrence(
                    police_occurrence_type_id=type_cache[type_name],
                    description=desc,
                    lat=float(row["__lat"]),
                    lng=float(row["__lng"]),
                    occurred_at=occurred_at,
                    h3_id=h3_id,
                )
                to_insert.append(po)

                if len(to_insert) >= DatabaseLogic.MAX_BATCH:
                    session.add_all(to_insert)
                    session.commit()
                    to_insert.clear()

            if to_insert:
                session.add_all(to_insert)
                session.commit()

            print(f"[import] Tipos criados: {created_types}")
            print(f"[import] Hexágonos criados: {created_hex}")
            print(f"[import] Ocorrências inseridas: {len(dfv)}")

            if update_stats:
                print("[stats] Recomputando HexagonOccurrenceStats...")
                grp = (
                    dfv.groupby(["__h3", "__type_name"])
                    .size()
                    .reset_index(name="__count")
                )
                grp["__type_id"] = grp["__type_name"].map(type_cache.get)
                pairs = [
                    (row["__h3"], int(row["__type_id"]), int(row["__count"]))
                    for _, row in grp.iterrows()
                    if pd.notna(row["__type_id"])
                ]
                DatabaseLogic.upsert_stats_bulk(session, pairs)
                session.commit()
                print(f"[stats] Linhas afetadas (upsert): {len(pairs)}")
        print("[done] Import finalizado com sucesso.")

    @staticmethod
    def import_all_files_in_folder(folder_path: str, update_stats: bool = True):
        folder = Path(folder_path)
        if not folder.is_dir():
            raise ValueError(f"Pasta não existe: {folder_path}")

        # Seleciona apenas arquivos CSV ou Excel
        files = [f for f in folder.iterdir() if f.suffix.lower() in (".csv", ".xlsx")]
        if not files:
            print(f"Nenhum arquivo CSV/XLSX encontrado em {folder_path}")
            return

        print(f"{len(files)} arquivos encontrados. Iniciando importação...")

        for f in files:
            try:
                print(f"Processando arquivo: {f.name}")
                DatabaseLogic.import_file(str(f), update_stats=update_stats)
            except Exception as e:
                print(f"ERRO ao processar {f.name}: {e}")

        print("Importação de todos os arquivos finalizada.")
