from typing import List, Optional, Dict, Any
from collections import Counter
from sqlalchemy.orm import Session
from src.database.repositories.cargo_theft_repository import CargoTheftRepository

try:
    import h3
except ImportError:
    raise RuntimeError("Instale a dependência 'h3': pip install h3")


class CargoTheftLogic:
    H3_RESOLUTION = 8  # Resolução 8: ~0.7 km² por célula

    def __init__(self, db: Session):
        self.repository = CargoTheftRepository(db)

    def list(self, params) -> List[any]:
        return self.repository.list(params)

    def get_by_id(self, theft_id: int) -> Optional[any]:
        return self.repository.get(theft_id)

    def create(self, data) -> any:
        return self.repository.create(data)

    def get_heatmap_data(self, limit: int = 10000) -> Dict[str, Any]:
        """
        Retorna dados agregados por células H3 para visualização.
        Formato: { "cells": [{"h3_id": "...", "count": N, "intensity": X}, ...] }
        """

        thefts = self.repository.get_heatmap_data(limit=limit)

        # Converter coordenadas para H3 IDs
        h3_ids = []

        for theft in thefts:
            try:
                # Calcular H3 ID (versão 4.x usa latlng_to_cell)
                h3_id = h3.latlng_to_cell(
                    float(theft.lat), float(theft.lng), self.H3_RESOLUTION
                )
                h3_ids.append(h3_id)
            except Exception as e:
                # Se falhar em algum ponto, apenas ignora
                print(f"Erro ao processar roubo: {e}")
                continue

        # Contar ocorrências por célula H3
        h3_counts = Counter(h3_ids)

        # Formatar resposta
        cells = []
        for h3_id, count in h3_counts.items():
            cells.append(
                {
                    "h3_id": h3_id,
                    "count": count,
                    "intensity": float(count),  # Intensidade = contagem
                    "type": "theft",
                }
            )

        return {
            "cells": cells,
            "total_cells": len(cells),
            "total_points": len(h3_ids),
            "resolution": self.H3_RESOLUTION,
        }

    def get_monthly_summary(self):
        return self.repository.get_monthly_summary()
