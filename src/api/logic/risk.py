import pickle
import os
from pathlib import Path
import numpy as np


class RiskUseCase:
    def __init__(self):
        self.model = self._load_model()
        self.scaler = self._load_scaler()
        self.features = self._load_features()

    def _load_model(self):
        """Carrega o modelo KDE treinado"""
        try:
            # Caminho absoluto para o arquivo do modelo
            current_dir = Path(__file__).parent
            model_path = (
                current_dir
                / ".."
                / ".."
                / "shared"
                / "machine_learning"
                / "modelo_risco_kde.pkl"
            )

            with open(model_path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            raise Exception("Arquivo do modelo não encontrado")
        except Exception as e:
            raise Exception(f"Erro ao carregar modelo: {str(e)}")

    def _load_scaler(self):
        """Carrega o scaler utilizado no treinamento"""
        try:
            current_dir = Path(__file__).parent
            scaler_path = (
                current_dir
                / ".."
                / ".."
                / "shared"
                / "machine_learning"
                / "scaler_risco.pkl"
            )

            with open(scaler_path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            print("Scaler não encontrado, continuando sem scaler")
            return None

    def _load_features(self):
        """Carrega as features esperadas pelo modelo"""
        try:
            current_dir = Path(__file__).parent
            features_path = (
                current_dir
                / ".."
                / ".."
                / "shared"
                / "machine_learning"
                / "features_risco.pkl"
            )

            with open(features_path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            print("Features não encontradas")
            return None

    def route_risk_assessment(self, route: list):
        """Avalia o risco para uma rota completa"""
        print("Rota recebida:", route)

        # Pré-processamento da rota
        processed_data = self._preprocess_route(route)

        # Aplicar scaler se disponível
        if self.scaler:
            processed_data = self.scaler.transform(processed_data)

        # Fazer predição com o modelo KDE
        try:
            # KDE geralmente usa score_samples para probabilidade
            risk_scores = self.model.score_samples(processed_data)
            average_risk = np.mean(risk_scores)

            return {
                "risk_score": float(average_risk),
                "risk_level": self._classify_risk(average_risk),
                "points_analyzed": len(risk_scores),
                "confidence": 0.95,
            }
        except Exception as e:
            raise Exception(f"Erro na predição: {str(e)}")

    def _preprocess_route(self, route):
        """
        Pré-processa a rota para o formato esperado pelo modelo
        Aqui você precisa adaptar para o formato que seu modelo espera
        """
        # Exemplo: converter coordenadas em features
        # Isso depende completamente de como seu modelo foi treinado
        processed_data = []

        for i, (lat, lng) in enumerate(route):
            # Exemplo de features básicas de uma rota
            features = [
                lat,  # latitude
                lng,  # longitude
                i / len(route),  # posição normalizada na rota
            ]
            processed_data.append(features)

        return np.array(processed_data)

    def _classify_risk(self, score):
        """Classifica o score de risco em categorias"""
        if score < -1:  # Ajuste esses valores conforme seu modelo
            return "very_low"
        elif score < 0:
            return "low"
        elif score < 1:
            return "medium"
        else:
            return "high"
