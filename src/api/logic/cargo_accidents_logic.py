from typing import List, Optional, Dict, Any
from collections import Counter
from sqlalchemy.orm import Session
from src.database.repositories.cargo_accidents_repository import (
    CargoAccidentsRepository,
)

try:
    import h3
except ImportError:
    raise RuntimeError("Instale a dependência 'h3': pip install h3")


class CargoAccidentsLogic:
    H3_RESOLUTION = 8  # Resolução 8: ~0.7 km² por célula

    def __init__(self, db: Session):
        self.repository = CargoAccidentsRepository(db)

    def list(self, params) -> List[any]:
        return self.repository.list(params)

    def get_by_id(self, accident_id: int) -> Optional[any]:
        return self.repository.get(accident_id)

    def create(self, data) -> any:
        return self.repository.create(data)

    def get_heatmap_data(self, limit: int = 10000) -> Dict[str, Any]:
        """
        Retorna dados agregados por células H3 para visualização.
        Formato: { "cells": [{"h3_id": "...", "count": N, "intensity": X}, ...] }
        """
        accidents = self.repository.get_heatmap_data(limit=limit)

        # Converter coordenadas para H3 IDs
        h3_ids = []
        intensities = {}  # Armazena soma de intensidades por célula

        for accident in accidents:
            try:
                # Calcular H3 ID (versão 4.x usa latlng_to_cell)
                h3_id = h3.latlng_to_cell(
                    float(accident.latitude),
                    float(accident.longitude),
                    self.H3_RESOLUTION,
                )
                h3_ids.append(h3_id)

                # Calcular intensidade baseada na gravidade (mortes)
                intensity = 1.0
                if hasattr(accident, "deaths") and accident.deaths:
                    intensity = min(accident.deaths / 2.0 + 1.0, 5.0)

                # Acumular intensidade por célula
                if h3_id in intensities:
                    intensities[h3_id] += intensity
                else:
                    intensities[h3_id] = intensity

            except Exception as e:
                # Se falhar em algum ponto, apenas ignora
                print(f"Erro ao processar acidente: {e}")
                continue

        # Contar ocorrências por célula H3
        h3_counts = Counter(h3_ids)

        # Formatar resposta
        cells = []
        for h3_id, count in h3_counts.items():
            avg_intensity = intensities.get(h3_id, count) / count
            cells.append(
                {
                    "h3_id": h3_id,
                    "count": count,
                    "intensity": avg_intensity,
                    "type": "accident",
                }
            )

        return {
            "cells": cells,
            "total_cells": len(cells),
            "total_points": len(h3_ids),
            "resolution": self.H3_RESOLUTION,
        }

    def get_monthly_summary(self, limit: int = 10000):
        return self.repository.get_monthly_summary(limit=limit)
