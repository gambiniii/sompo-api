import os
import joblib
import numpy as np
import folium
from folium.plugins import HeatMap
from typing import List, Tuple, Dict, Any


class RiskUseCase:
    """Avalia risco de rota usando KDE + scaler.

    Esta versão usa os nomes das colunas exatamente como estão na planilha
    (ex.: 'LATITUDE', 'LONGITUDE', 'HORA_SIN', 'HORA_COS', 'FIM_DE_SEMANA').

    Arquivos esperados em base_path (padrão src/shared/machine_learning):
      - modelo_risco_kde.pkl
      - scaler_risco.pkl (opcional)
      - features_risco.pkl (opcional): lista com nomes exatamente como na planilha
      - train_log_scores.pkl (opcional): log-scores do treino para calibrar percentis
    """

    def __init__(self, base_path: str = "src/shared/machine_learning"):
        self.base_path = base_path

        # carregar KDE
        try:
            self.kde = joblib.load(os.path.join(base_path, "modelo_risco_kde.pkl"))
        except Exception as e:
            raise RuntimeError(
                f"Não foi possível carregar KDE (modelo_risco_kde.pkl): {e}"
            )

        # carregar scaler (opcional)
        try:
            self.scaler = joblib.load(os.path.join(base_path, "scaler_risco.pkl"))
        except Exception:
            self.scaler = None
            print(
                "[RiskUseCase] Atenção: scaler_risco.pkl não encontrado. Prosseguindo sem scaler."
            )

        # carregar features (opcional). Espera-se que os nomes sejam exatamente os da planilha.
        try:
            self.features = joblib.load(os.path.join(base_path, "features_risco.pkl"))
            print(
                "[RiskUseCase] features (usando nomes da planilha) carregadas:",
                self.features,
            )
        except Exception:
            self.features = None
            print(
                "[RiskUseCase] features_risco.pkl não encontrado. Usando ordem padrão [LATITUDE, LONGITUDE, HORA_SIN, HORA_COS, FIM_DE_SEMANA]."
            )

        # carregar train_log_scores (opcional) para calibrar percentis
        try:
            self.train_log_scores = joblib.load(
                os.path.join(base_path, "train_log_scores.pkl")
            )
            print(
                "[RiskUseCase] train_log_scores carregado para calibração de percentis."
            )
        except Exception:
            self.train_log_scores = None

    def _build_row_from_features(
        self, lat: float, lon: float, expected_hour: int, weekday: int
    ) -> List[float]:
        """Monta uma linha de features seguindo os nomes EXATOS da planilha.

        Se self.features estiver presente, usamos a ordem e os nomes tal qual aparecem nela.
        Exemplos de nomes esperados na planilha (caso você não tenha fornecido features_risco.pkl):
          - 'LATITUDE'
          - 'LONGITUDE'
          - 'HORA_SIN'
          - 'HORA_COS'
          - 'FIM_DE_SEMANA'

        Se algum nome da planilha não for reconhecido, preenchemos com 0.0 e emitimos aviso.
        """
        hora_sin = np.sin(2 * np.pi * expected_hour / 24)
        hora_cos = np.cos(2 * np.pi * expected_hour / 24)
        fim_de_semana = 1 if weekday >= 5 else 0

        # mapeamento para os nomes exatos da planilha (MAIÚSCULAS)
        mapping_exact = {
            "LATITUDE": lat,
            "LONGITUDE": lon,
            "LON": lon,
            "LONG": lon,
            "LAT": lat,
            "HORA_SIN": hora_sin,
            "HORA_COS": hora_cos,
            "FIM_DE_SEMANA": fim_de_semana,
            # algumas planilhas podem ter variações, adicionamos aliases comuns
            "latitude": lat,
            "longitude": lon,
            "hora_sin": hora_sin,
            "hora_cos": hora_cos,
            "fim_de_semana": fim_de_semana,
            "WEEKDAY": float(weekday),
            "HOUR": float(expected_hour),
        }

        if self.features:
            row = []
            for feat in self.features:
                # usar exatamente o nome que veio da planilha
                if feat in mapping_exact:
                    row.append(mapping_exact[feat])
                else:
                    # tentar versão maiúscula/minúscula como fallback
                    if feat.upper() in mapping_exact:
                        row.append(mapping_exact[feat.upper()])
                    elif feat.lower() in mapping_exact:
                        row.append(mapping_exact[feat.lower()])
                    else:
                        row.append(0.0)
                        print(
                            f"[RiskUseCase] Atenção: feature '{feat}' não mapeada; usando 0.0"
                        )
        else:
            # ordem padrão usando nomes da planilha (MAIÚSCULAS)
            row = [lat, lon, hora_sin, hora_cos, fim_de_semana]

        return row

    def route_risk_assessment(
        self, route: List[Tuple[float, float]], expected_hour: int, weekday: int
    ) -> Dict[str, Any]:
        """Avalia uma rota e retorna resultados por ponto + resumo."""
        if not route:
            return {
                "results": [],
                "average_log_density": None,
                "average_normalized": None,
                "points_analyzed": 0,
                "confidence": 0.0,
            }

        inputs = [
            self._build_row_from_features(lat, lon, expected_hour, weekday)
            for lat, lon in route
        ]
        X = np.asarray(inputs)

        # diagnóstico
        print("[RiskUseCase] X.shape:", X.shape)
        print("[RiskUseCase] X sample (first 5 rows): ", X[:5])
        if self.scaler is not None and hasattr(self.scaler, "n_features_in_"):
            print(
                "[RiskUseCase] scaler.n_features_in_:",
                getattr(self.scaler, "n_features_in_", None),
            )
        if self.features is not None:
            print("[RiskUseCase] features (planilha):", self.features)

        # aplicar scaler se existir
        if self.scaler is not None:
            try:
                X_scaled = self.scaler.transform(X)
            except Exception as e:
                raise RuntimeError(f"Erro ao aplicar scaler.transform: {e}")
        else:
            X_scaled = X

        print(
            "[RiskUseCase] X_scaled stats: min, max, mean, std ->",
            np.min(X_scaled),
            np.max(X_scaled),
            np.mean(X_scaled),
            np.std(X_scaled),
        )

        # obter log-density
        try:
            log_scores = self.kde.score_samples(X_scaled)
        except Exception as e:
            raise RuntimeError(f"Erro ao calcular score_samples no KDE: {e}")

        print(
            "[RiskUseCase] log_scores stats: min, max, mean, std ->",
            np.min(log_scores),
            np.max(log_scores),
            np.mean(log_scores),
            np.std(log_scores),
        )

        # normalizar log_scores diretamente para [0,1]
        min_ls, max_ls = float(np.min(log_scores)), float(np.max(log_scores))
        if max_ls - min_ls > 0:
            normalized_log = (log_scores - min_ls) / (max_ls - min_ls)
        else:
            normalized_log = np.zeros_like(log_scores)

        # usar percentis do treino (se existir) para calibrar classificação
        train_percentiles = None
        if self.train_log_scores is not None:
            try:
                p10 = np.percentile(self.train_log_scores, 10)
                p33 = np.percentile(self.train_log_scores, 33)
                p66 = np.percentile(self.train_log_scores, 66)
                p90 = np.percentile(self.train_log_scores, 90)
                train_percentiles = (p10, p33, p66, p90)
                print(
                    "[RiskUseCase] train percentiles (10,33,66,90):", train_percentiles
                )
            except Exception:
                train_percentiles = None

        results = []
        for (lat, lon), ls, nl in zip(route, log_scores, normalized_log):
            density_for_map = float(nl)  # peso para heatmap (0..1)
            risk_score_norm = float(1.0 - nl)  # 1 = maior risco (menor densidade)

            if train_percentiles is not None:
                p10, p33, p66, p90 = train_percentiles
                if ls <= p10:
                    risco = "ALTO"
                elif ls <= p33:
                    risco = "MÉDIO"
                elif ls <= p66:
                    risco = "BAIXO"
                else:
                    risco = "MUITO_BAIXO"
            else:
                if risk_score_norm >= 0.66:
                    risco = "ALTO"
                elif risk_score_norm >= 0.33:
                    risco = "MÉDIO"
                else:
                    risco = "BAIXO"

            results.append(
                {
                    "latitude": float(lat),
                    "longitude": float(lon),
                    "log_score": float(ls),
                    "normalized_log": density_for_map,
                    "risk_score_norm": risk_score_norm,
                    "risco": risco,
                }
            )

        summary = {
            "results": results,
            "average_log_density": float(np.mean(log_scores)),
            "average_normalized": float(np.mean(normalized_log)),
            "points_analyzed": len(results),
            "confidence": 0.95,
        }

        return summary

    def create_heatmap(
        self, resultados: List[Dict[str, Any]], out_file: str = "analise_rota.html"
    ) -> None:
        if not resultados:
            print("[RiskUseCase] Nenhum resultado para desenhar no mapa.")
            return

        avg_lat = np.mean([r["latitude"] for r in resultados])
        avg_lon = np.mean([r["longitude"] for r in resultados])

        mapa = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)
        heat_data = [
            [r["latitude"], r["longitude"], r.get("normalized_log", 0.0)]
            for r in resultados
        ]
        HeatMap(heat_data, radius=15, blur=10, max_zoom=13).add_to(mapa)

        for r in resultados:
            if r.get("risco") == "ALTO":
                folium.CircleMarker(
                    location=[r["latitude"], r["longitude"]],
                    radius=8,
                    color="red",
                    fill=True,
                    fillColor="red",
                    fillOpacity=0.8,
                    popup=(
                        f"Risco ALTO | log_score={r['log_score']:.3f} | "
                        f"normalized={r['normalized_log']:.3f} | risk_norm={r['risk_score_norm']:.3f}"
                    ),
                ).add_to(mapa)

        mapa.save(out_file)
        print(f"[RiskUseCase] Mapa salvo como '{out_file}'")


