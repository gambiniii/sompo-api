"""
AccidentRiskUseCase - Predição de Risco de Acidentes em Rotas
"""

import dill as pickle
import os
from datetime import datetime
from typing import List, Tuple, Dict, Optional, Union
from pathlib import Path
import traceback


class AccidentRiskUseCase:
    """Caso de uso para predição de risco de acidentes em rotas"""

    def __init__(self, base_path: str = "src/shared/machine_learning"):
        """
        Inicializa e carrega o modelo

        Args:
            base_path: Caminho onde está o accident_risk_model.pkl
        """
        self.base_path = Path(base_path)
        self.model_filename = "accident_risk_model.pkl"
        self.model_path = self.base_path / self.model_filename
        self.predictor = None

        print(f"🔍 Inicializando AccidentRiskUseCase...")
        print(f"   Buscando modelo em: {self.model_path}")

        # Carregar modelo
        self._load_model()

    def _load_model(self):
        """Carrega o modelo .pkl"""
        try:
            # Verificar se arquivo existe
            if not self.model_path.exists():
                raise FileNotFoundError(
                    f"❌ Modelo não encontrado: {self.model_path}\n"
                    f"   Certifique-se que {self.model_filename} está em {self.base_path}"
                )

            print(f"📦 Carregando modelo de acidentes...")

            # Carregar com dill (melhor para objetos complexos)
            with open(self.model_path, 'rb') as f:
                self.predictor = pickle.load(f)

            # Validações
            if not hasattr(self.predictor, 'predict_route_risk'):
                raise ValueError("Modelo não possui método 'predict_route_risk'")

            print(f"✅ Modelo de acidentes carregado com sucesso!")
            if hasattr(self.predictor, 'cargo_risk_factors'):
                print(f"   • Tipos de carga: {len(self.predictor.cargo_risk_factors)}")
            if hasattr(self.predictor, 'weather_multipliers'):
                print(f"   • Condições climáticas: {len(self.predictor.weather_multipliers)}")

        except Exception as e:
            print(f"❌ ERRO ao carregar modelo de acidentes: {e}")
            print(traceback.format_exc())
            raise

    def predict_route_risk(
        self,
        route_coords: Union[List[List[float]], List[Tuple[float, float]]],
        departure_datetime: Union[str, datetime],
        cargo_type: str,
        weather_condition: Optional[str] = None
    ) -> Dict:
        """
        Predição de risco de acidentes para uma rota

        Args:
            route_coords: Lista de coordenadas
                Aceita: [[-23.55, -46.63], [-23.54, -46.62], ...]
                ou: [(-23.55, -46.63), (-23.54, -46.62), ...]

            departure_datetime: Data/hora de partida
                Aceita string: "2025-10-15 18:00:00" ou datetime object

            cargo_type: Tipo de carga

            weather_condition: Condição climática (opcional)
                Valores esperados: "Céu Claro", "Chuva", "Nevoeiro/Neblina", etc.

        Returns:
            Dict com resultado da predição

        Raises:
            ValueError: Dados inválidos
            Exception: Erros durante predição
        """

        print("\n" + "="*70)
        print("🚗 INICIANDO PREDIÇÃO DE ACIDENTES")
        print("="*70)

        try:
            # 1. Validar modelo carregado
            if self.predictor is None:
                raise RuntimeError("Modelo não carregado")

            # 2. Processar e validar inputs
            print("\n1️⃣ Processando inputs...")

            # Processar coordenadas
            print(f"   📍 Rota recebida: {len(route_coords)} pontos")
            route_tuples = self._process_coordinates(route_coords)
            print(f"   ✅ Coordenadas processadas: {len(route_tuples)} pontos")

            # Processar data/hora
            print(f"\n   📅 Data recebida: {departure_datetime}")
            dt = self._process_datetime(departure_datetime)
            print(f"   ✅ Data processada: {dt}")

            # Processar tipo de carga
            print(f"\n   📦 Carga recebida: '{cargo_type}'")
            print(f"   ✅ Carga: '{cargo_type}'")

            # Processar condição climática
            if weather_condition:
                print(f"\n   🌦️  Clima recebido: '{weather_condition}'")
                weather_validated = self._validate_weather(weather_condition)
                print(f"   ✅ Clima validado: '{weather_validated}'")
            else:
                weather_validated = None
                print(f"\n   🌦️  Clima: Não especificado")

            # 3. Fazer predição
            print("\n2️⃣ Executando predição no modelo...")

            result = self.predictor.predict_route_risk(
                route_coords=route_tuples,
                departure_datetime=dt,
                cargo_type=cargo_type,
                weather_condition=weather_validated
            )

            print(f"   ✅ Predição concluída!")
            print(f"      Risco: {result.get('risk_category', 'N/A')}")
            print(f"      Score: {result.get('risk_score', 0):.4f}")

            print("\n" + "="*70)
            print("✅ PREDIÇÃO DE ACIDENTES FINALIZADA COM SUCESSO")
            print("="*70 + "\n")

            return result

        except ValueError as e:
            print(f"\n❌ ERRO DE VALIDAÇÃO: {e}")
            raise
        except Exception as e:
            print(f"\n❌ ERRO DURANTE PREDIÇÃO: {e}")
            print(traceback.format_exc())
            raise

    def _process_coordinates(
        self,
        coords: Union[List[List[float]], List[Tuple[float, float]]]
    ) -> List[Tuple[float, float]]:
        """Processa e valida coordenadas"""

        if not isinstance(coords, list):
            raise ValueError(f"route_coords deve ser lista, recebido: {type(coords)}")

        if len(coords) < 2:
            raise ValueError(f"Rota deve ter pelo menos 2 pontos, recebido: {len(coords)}")

        processed = []
        for i, coord in enumerate(coords):
            if isinstance(coord, tuple):
                coord = list(coord)

            if not isinstance(coord, list) or len(coord) != 2:
                raise ValueError(f"Coordenada {i} inválida: deve ser [lat, lon], recebido: {coord}")

            lat, lon = coord

            if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
                raise ValueError(f"Coordenada {i}: lat e lon devem ser numéricos")

            if not (-90 <= lat <= 90):
                raise ValueError(f"Coordenada {i}: latitude {lat} fora do range [-90, 90]")

            if not (-180 <= lon <= 180):
                raise ValueError(f"Coordenada {i}: longitude {lon} fora do range [-180, 180]")

            processed.append((float(lat), float(lon)))

        return processed

    def _process_datetime(
        self,
        dt: Union[str, datetime]
    ) -> datetime:
        """Processa e valida data/hora"""

        if isinstance(dt, datetime):
            return dt

        if isinstance(dt, str):
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%dT%H:%M',
                '%d/%m/%Y %H:%M:%S',
                '%d/%m/%Y %H:%M'
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(dt, fmt)
                except ValueError:
                    continue

            raise ValueError(f"Formato de data/hora inválido: '{dt}'")

        raise ValueError(f"departure_datetime deve ser string ou datetime, recebido: {type(dt)}")

    def _validate_weather(self, weather: Optional[str]) -> Optional[str]:
        """Valida condição climática"""

        if weather is None:
            return None

        if not isinstance(weather, str):
            raise ValueError(f"weather_condition deve ser string, recebido: {type(weather)}")

        weather_clean = weather.strip()

        if not weather_clean:
            return None

        # Condições aceitas pelo modelo
        valid_conditions = [
            'Céu Claro', 'Chuva', 'Nevoeiro/Neblina', 'Nublado',
            'Garoa/Chuvisco', 'Sol', 'Granizo', 'Neve', 'Vento'
        ]

        # Tentar encontrar match case-insensitive
        for valid in valid_conditions:
            if weather_clean.lower() == valid.lower():
                return valid

        # Se não encontrou, retornar original (modelo pode aceitar)
        print(f"   ⚠️  Condição '{weather_clean}' não está na lista padrão, usando mesmo assim")
        return weather_clean

    def get_available_cargo_types(self) -> List[str]:
        """Retorna tipos de carga disponíveis"""
        if self.predictor is None:
            raise RuntimeError("Modelo não carregado")

        if hasattr(self.predictor, 'cargo_risk_factors'):
            return list(self.predictor.cargo_risk_factors.keys())
        return []

    def get_model_info(self) -> Dict:
        """Retorna informações do modelo"""
        if self.predictor is None:
            raise RuntimeError("Modelo não carregado")

        return {
            'model_file': str(self.model_path),
            'model_size_mb': round(os.path.getsize(self.model_path) / (1024*1024), 2),
            'is_loaded': True,
            'model_type': 'accident_risk',
            'cargo_types': self.get_available_cargo_types(),
        }
