"""
RiskUseCase - Predição de Risco em Rotas com Debug Detalhado
"""

import dill as pickle  # Use dill ao invés de pickle
import os
from datetime import datetime
from typing import List, Tuple, Dict, Optional, Union
from pathlib import Path
import traceback


class RiskUseCase:
    """Caso de uso para predição de risco em rotas"""
    
    def __init__(self, base_path: str = "src/shared/machine_learning"):
        """
        Inicializa e carrega o modelo
        
        Args:
            base_path: Caminho onde está o route_risk_model.pkl
        """
        self.base_path = Path(base_path)
        self.model_filename = "route_risk_model.pkl"
        self.model_path = self.base_path / self.model_filename
        self.predictor = None
        
        print(f"🔍 Inicializando RiskUseCase...")
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
            
            print(f"📦 Carregando modelo...")
            
            # Carregar com dill (melhor para objetos complexos)
            with open(self.model_path, 'rb') as f:
                self.predictor = pickle.load(f)
            
            # Validações
            if not hasattr(self.predictor, 'predict_route_risk'):
                raise ValueError("Modelo não possui método 'predict_route_risk'")
            
            if not hasattr(self.predictor, 'is_fitted'):
                raise ValueError("Modelo não possui atributo 'is_fitted'")
            
            if not self.predictor.is_fitted:
                raise ValueError("Modelo não está treinado (is_fitted=False)")
            
            print(f"✅ Modelo carregado com sucesso!")
            print(f"   • Tipos de carga: {len(self.predictor.cargo_risk_factors)}")
            print(f"   • Registros históricos: {len(self.predictor.historical_data):,}")
            
        except Exception as e:
            print(f"❌ ERRO ao carregar modelo: {e}")
            print(traceback.format_exc())
            raise
    
    def predict_route_risk(
        self,
        route_coords: Union[List[List[float]], List[Tuple[float, float]]],
        departure_datetime: Union[str, datetime],
        cargo_type: str
    ) -> Dict:
        """
        Predição de risco para uma rota
        
        Args:
            route_coords: Lista de coordenadas
                Aceita: [[-23.55, -46.63], [-23.54, -46.62], ...]
                ou: [(-23.55, -46.63), (-23.54, -46.62), ...]
            
            departure_datetime: Data/hora de partida
                Aceita string: "2025-10-15 18:00:00" ou datetime object
            
            cargo_type: Tipo de carga (string)
        
        Returns:
            Dict com resultado da predição
        
        Raises:
            ValueError: Dados inválidos
            Exception: Erros durante predição
        """
        
        print("\n" + "="*70)
        print("🎯 INICIANDO PREDIÇÃO")
        print("="*70)
        
        try:
            # 1. Validar modelo carregado
            if self.predictor is None:
                raise RuntimeError("Modelo não carregado")
            
            # 2. Processar e validar inputs
            print("\n1️⃣ Processando inputs...")
            
            # Processar coordenadas
            print(f"   📍 Rota recebida: {len(route_coords)} pontos")
            print(f"      Tipo: {type(route_coords)}")
            print(f"      Primeira coord: {route_coords[0] if route_coords else 'N/A'}")
            
            route_tuples = self._process_coordinates(route_coords)
            print(f"   ✅ Coordenadas processadas: {len(route_tuples)} pontos")
            
            # Processar data/hora
            print(f"\n   📅 Data recebida: {departure_datetime}")
            print(f"      Tipo: {type(departure_datetime)}")
            
            dt = self._process_datetime(departure_datetime)
            print(f"   ✅ Data processada: {dt}")
            
            # Processar tipo de carga
            print(f"\n   📦 Carga recebida: '{cargo_type}'")
            print(f"      Tipo: {type(cargo_type)}")
            
            cargo_validated = self._validate_cargo_type(cargo_type)
            print(f"   ✅ Carga validada: '{cargo_validated}'")
            
            # 3. Fazer predição
            print("\n2️⃣ Executando predição no modelo...")
            
            result = self.predictor.predict_route_risk(
                route_coords=route_tuples,
                departure_datetime=dt,
                cargo_type=cargo_validated
            )
            
            print(f"   ✅ Predição concluída!")
            print(f"      Risco: {result['risk_category']}")
            print(f"      Score: {result['risk_score']:.4f}")
            
            print("\n" + "="*70)
            print("✅ PREDIÇÃO FINALIZADA COM SUCESSO")
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
        """
        Processa e valida coordenadas
        Converte listas em tuplas
        """
        
        # Validar tipo
        if not isinstance(coords, list):
            raise ValueError(f"route_coords deve ser lista, recebido: {type(coords)}")
        
        # Validar quantidade mínima
        if len(coords) < 2:
            raise ValueError(f"Rota deve ter pelo menos 2 pontos, recebido: {len(coords)}")
        
        # Processar cada coordenada
        processed = []
        for i, coord in enumerate(coords):
            
            # Converter para lista se necessário
            if isinstance(coord, tuple):
                coord = list(coord)
            
            # Validar formato
            if not isinstance(coord, list) or len(coord) != 2:
                raise ValueError(
                    f"Coordenada {i} inválida: deve ser [lat, lon], "
                    f"recebido: {coord} (tipo: {type(coord)})"
                )
            
            lat, lon = coord
            
            # Validar tipos
            if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
                raise ValueError(
                    f"Coordenada {i}: lat e lon devem ser numéricos, "
                    f"recebido: lat={lat} (tipo: {type(lat)}), "
                    f"lon={lon} (tipo: {type(lon)})"
                )
            
            # Validar ranges
            if not (-90 <= lat <= 90):
                raise ValueError(f"Coordenada {i}: latitude {lat} fora do range [-90, 90]")
            
            if not (-180 <= lon <= 180):
                raise ValueError(f"Coordenada {i}: longitude {lon} fora do range [-180, 180]")
            
            # Adicionar como tupla
            processed.append((float(lat), float(lon)))
        
        return processed
    
    def _process_datetime(
        self, 
        dt: Union[str, datetime]
    ) -> datetime:
        """
        Processa e valida data/hora
        Converte string para datetime se necessário
        """
        
        # Se já é datetime, retornar
        if isinstance(dt, datetime):
            return dt
        
        # Se é string, tentar converter
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
            
            # Se nenhum formato funcionou
            raise ValueError(
                f"Formato de data/hora inválido: '{dt}'\n"
                f"Formatos aceitos:\n"
                f"  - YYYY-MM-DD HH:MM:SS\n"
                f"  - YYYY-MM-DD HH:MM\n"
                f"  - YYYY-MM-DDTHH:MM:SS (ISO)\n"
                f"  - DD/MM/YYYY HH:MM:SS\n"
                f"  - DD/MM/YYYY HH:MM"
            )
        
        raise ValueError(
            f"departure_datetime deve ser string ou datetime, "
            f"recebido: {type(dt)}"
        )
    
    def _validate_cargo_type(self, cargo: str) -> str:
        """
        Valida tipo de carga
        Remove espaços extras e valida contra lista disponível
        """
        
        # Validar tipo
        if not isinstance(cargo, str):
            raise ValueError(f"cargo_type deve ser string, recebido: {type(cargo)}")
        
        # Limpar string
        cargo_clean = cargo.strip()
        
        if not cargo_clean:
            raise ValueError("cargo_type não pode ser vazio")
        
        # Validar contra lista disponível
        available_cargos = list(self.predictor.cargo_risk_factors.keys())
        
        if cargo_clean not in available_cargos:
            # Sugerir carga mais próxima (case-insensitive)
            cargo_lower = cargo_clean.lower()
            suggestions = [
                c for c in available_cargos 
                if cargo_lower in c.lower() or c.lower() in cargo_lower
            ]
            
            error_msg = f"Tipo de carga '{cargo_clean}' não encontrado.\n"
            error_msg += f"\nTipos disponíveis:\n"
            for c in available_cargos:
                error_msg += f"  • {c}\n"
            
            if suggestions:
                error_msg += f"\nVocê quis dizer: {', '.join(suggestions)}?"
            
            raise ValueError(error_msg)
        
        return cargo_clean
    
    def get_available_cargo_types(self) -> List[Dict]:
        """Retorna tipos de carga disponíveis"""
        if self.predictor is None:
            raise RuntimeError("Modelo não carregado")
        
        return [
            {
                'name': cargo,
                'risk_factor_percent': float(factor),
                'risk_multiplier': round(1 + (factor / 100), 4)
            }
            for cargo, factor in sorted(
                self.predictor.cargo_risk_factors.items(),
                key=lambda x: x[1],
                reverse=True
            )
        ]
    
    def get_model_info(self) -> Dict:
        """Retorna informações do modelo"""
        if self.predictor is None:
            raise RuntimeError("Modelo não carregado")
        
        metadata = self.predictor.model_metadata
        
        return {
            'model_file': str(self.model_path),
            'model_size_mb': round(os.path.getsize(self.model_path) / (1024*1024), 2),
            'is_loaded': True,
            'trained_at': metadata.get('trained_at'),
            'total_records': metadata.get('total_records'),
            'date_range': metadata.get('date_range'),
            'spatial_bounds': metadata.get('spatial_bounds'),
            'cargo_types': self.get_available_cargo_types()
        }


# ============================================================================
# TESTE LOCAL (para debug)
# ============================================================================

if __name__ == "__main__":
    
    print("\n" + "="*70)
    print("TESTE DO RiskUseCase")
    print("="*70 + "\n")
    
    try:
        # Inicializar (ajuste o caminho se necessário)
        risk_uc = RiskUseCase(base_path=".")
        
        # Teste 1: Predição básica
        print("\n" + "="*70)
        print("TESTE 1: Predição Básica")
        print("="*70)
        
        result = risk_uc.predict_route_risk(
            route_coords=[
                [-23.5505, -46.6333],
                [-23.5489, -46.6388],
                [-23.5528, -46.6299]
            ],
            departure_datetime="2025-10-15 18:00:00",
            cargo_type="Cigarros"
        )
        
        print(f"\n✅ RESULTADO:")
        print(f"   Risco: {result['risk_category']}")
        print(f"   Score: {result['risk_score']:.4f}")
        print(f"   Distância: {result['route_length_km']:.2f} km")
        
        # Teste 2: Formatos diferentes
        print("\n" + "="*70)
        print("TESTE 2: Formatos Alternativos")
        print("="*70)
        
        # Com tuplas
        result2 = risk_uc.predict_route_risk(
            route_coords=[
                (-23.5505, -46.6333),
                (-23.5489, -46.6388)
            ],
            departure_datetime=datetime(2025, 10, 15, 18, 0),
            cargo_type="Alimentício"
        )
        print(f"\n✅ Com tuplas: {result2['risk_category']}")
        
        # Teste 3: Ver tipos de carga
        print("\n" + "="*70)
        print("TESTE 3: Tipos de Carga Disponíveis")
        print("="*70)
        
        cargos = risk_uc.get_available_cargo_types()
        print(f"\nTotal: {len(cargos)} tipos")
        for cargo in cargos[:5]:
            print(f"   • {cargo['name']:.<30} +{cargo['risk_factor_percent']:.1f}%")
        
        # Teste 4: Info do modelo
        print("\n" + "="*70)
        print("TESTE 4: Informações do Modelo")
        print("="*70)
        
        info = risk_uc.get_model_info()
        print(f"\nArquivo: {info['model_file']}")
        print(f"Tamanho: {info['model_size_mb']} MB")
        print(f"Treinado em: {info['trained_at']}")
        
        print("\n" + "="*70)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        print(traceback.format_exc())