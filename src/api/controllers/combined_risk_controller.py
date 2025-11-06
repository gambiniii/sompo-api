from src.api.controllers.risk_controller import RiskController
from src.api.controllers.accident_risk_controller import AccidentRiskController
from typing import List, Tuple, Optional


class CombinedRiskController:
    def __init__(self):
        self.theft_controller = RiskController()
        self.accident_controller = AccidentRiskController()

    def combined_risk_assessment(
        self,
        route: List[Tuple[float, float]],
        expected_hour: int,
        weekday: int,
        cargo_type: str,
        weather_condition: Optional[str] = None
    ):
        # Avaliar risco de roubo
        theft_risk = self.theft_controller.route_risk_assessment(
            route=route,
            expected_hour=expected_hour,
            weekday=weekday,
            cargo_type=cargo_type
        )

        # Avaliar risco de acidente
        accident_risk = self.accident_controller.route_risk_assessment(
            route=route,
            expected_hour=expected_hour,
            weekday=weekday,
            cargo_type=cargo_type,
            weather_condition=weather_condition
        )

        # Calcular risco combinado (média ponderada)
        # Roubo tem peso 0.6, Acidente tem peso 0.4
        overall_risk_score = (theft_risk['risk_score'] * 0.6) + (accident_risk['risk_score'] * 0.4)

        # Categorizar risco geral
        if overall_risk_score < 0.2:
            overall_category = "BAIXO"
        elif overall_risk_score < 0.5:
            overall_category = "MÉDIO"
        elif overall_risk_score < 0.8:
            overall_category = "ALTO"
        else:
            overall_category = "CRÍTICO"

        # Gerar recomendações
        recommendations = self._generate_recommendations(
            theft_risk, accident_risk, overall_risk_score
        )

        return {
            'theft_risk': theft_risk,
            'accident_risk': accident_risk,
            'overall_risk_score': overall_risk_score,
            'overall_risk_category': overall_category,
            'recommendations': recommendations
        }

    def _generate_recommendations(self, theft_risk, accident_risk, overall_score):
        recommendations = []

        # Recomendações baseadas em roubo
        if theft_risk['risk_category'] in ['ALTO', 'CRÍTICO']:
            recommendations.append(f"⚠️ Alto risco de roubo ({theft_risk['risk_category']}) - Considere rotas alternativas")
            if len(theft_risk['critical_segments']) > 0:
                recommendations.append(f"🔴 {len(theft_risk['critical_segments'])} pontos críticos de roubo identificados")

        # Recomendações baseadas em acidentes
        if accident_risk['risk_category'] in ['ALTO', 'CRÍTICO']:
            recommendations.append(f"⚠️ Alto risco de acidentes ({accident_risk['risk_category']}) - Dirija com cautela extra")

        if accident_risk.get('weather_multiplier', 1.0) > 1.3:
            recommendations.append(f"🌧️ Condições climáticas adversas aumentam o risco de acidentes")

        # Recomendações baseadas em temporal
        if theft_risk['temporal_multiplier'] > 1.5 or accident_risk['temporal_multiplier'] > 1.5:
            recommendations.append("🕐 Horário de alto risco - Considere alterar o horário da viagem")

        # Recomendações baseadas em carga
        if theft_risk['cargo_factor'] > 0.5:
            recommendations.append(f"📦 Tipo de carga '{theft_risk['cargo_type']}' tem alto fator de risco para roubos")

        # Recomendações gerais
        if overall_score < 0.3:
            recommendations.append("✅ Rota com baixo risco geral - Viagem segura")
        elif overall_score > 0.7:
            recommendations.append("🚨 Risco geral elevado - Avalie alternativas ou reforce segurança")

        if len(recommendations) == 0:
            recommendations.append("✅ Rota dentro dos parâmetros aceitáveis de risco")

        return recommendations
