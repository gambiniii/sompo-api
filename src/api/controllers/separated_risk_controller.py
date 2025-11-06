from src.api.controllers.risk_controller import RiskController
from src.api.controllers.accident_risk_controller import AccidentRiskController
from src.shared.config.cargo_mapping import map_to_theft_model, map_to_accident_model, validate_unified_cargo
from typing import List, Tuple, Optional


class SeparatedRiskController:
    """
    Controller que chama os 2 modelos SEPARADAMENTE com mapeamento de cargas
    """

    def __init__(self):
        self.theft_controller = RiskController()
        self.accident_controller = AccidentRiskController()

    def separated_risk_assessment(
        self,
        route: List[Tuple[float, float]],
        expected_hour: int,
        weekday: int,
        cargo_type: str,  # Descrição do tipo de carga da planilha unificada
        weather_condition: Optional[str] = None
    ):
        """
        Avalia riscos separadamente:
        - Recebe tipo de carga da planilha unificada
        - Mapeia para modelos antigos de Roubo e Acidente
        """

        print("\n" + "="*80)
        print("🔍 DEBUG - SEPARATED RISK ASSESSMENT")
        print("="*80)
        print(f"📥 ENTRADA RECEBIDA:")
        print(f"   cargo_type = '{cargo_type}'")
        print(f"   tipo = {type(cargo_type)}")
        print(f"   expected_hour = {expected_hour}")
        print(f"   weekday = {weekday}")
        print(f"   weather_condition = {weather_condition}")
        print("="*80)

        # Validar se a carga existe no mapeamento unificado
        print(f"\n🔍 Validando cargo no mapeamento unificado...")
        is_valid = validate_unified_cargo(cargo_type)
        print(f"   Resultado: {is_valid}")

        if not is_valid:
            raise ValueError(
                f"Tipo de carga '{cargo_type}' não encontrado. "
                f"Verifique se o tipo existe na tabela cargo_type."
            )

        # 1. Mapear para o modelo de ROUBO
        theft_cargo = map_to_theft_model(cargo_type)
        print(f"\n🚨 MAPEAMENTO ROUBO:")
        print(f"   Entrada: '{cargo_type}'")
        print(f"   Saída para modelo: '{theft_cargo}'")

        theft_risk = self.theft_controller.route_risk_assessment(
            route=route,
            expected_hour=expected_hour,
            weekday=weekday,
            cargo_type=theft_cargo  # Usa o tipo mapeado para o modelo antigo
        )

        # 2. Mapear para o modelo de ACIDENTE
        accident_cargo = map_to_accident_model(cargo_type)
        print(f"\n🚗 MAPEAMENTO ACIDENTE:")
        print(f"   Entrada: '{cargo_type}'")
        print(f"   Saída para modelo: '{accident_cargo}'")

        # 3. Avaliar risco de ACIDENTE (usa a carga mapeada)
        accident_risk = self.accident_controller.route_risk_assessment(
            route=route,
            expected_hour=expected_hour,
            weekday=weekday,
            cargo_type=accident_cargo,  # Usa mapeada
            weather_condition=weather_condition
        )

        # 4. Calcular risco combinado
        overall_risk_score = (theft_risk['risk_score'] * 0.6) + (accident_risk['risk_score'] * 0.4)

        # Categorizar
        if overall_risk_score < 0.2:
            overall_category = "BAIXO"
        elif overall_risk_score < 0.5:
            overall_category = "MÉDIO"
        elif overall_risk_score < 0.8:
            overall_category = "ALTO"
        else:
            overall_category = "CRÍTICO"

        # 5. Gerar recomendações
        recommendations = self._generate_recommendations(
            theft_risk, accident_risk, overall_risk_score, cargo_type, accident_cargo
        )

        return {
            'theft_risk': theft_risk,
            'accident_risk': accident_risk,
            'overall_risk_score': overall_risk_score,
            'overall_risk_category': overall_category,
            'recommendations': recommendations,
            'cargo_mapping': {
                'unified_cargo': cargo_type,
                'theft_model_cargo': theft_cargo,
                'accident_model_cargo': accident_cargo,
                'note': f'Carga "{cargo_type}" foi mapeada para "{theft_cargo}" (roubo) e "{accident_cargo}" (acidente)'
            }
        }

    def _generate_recommendations(self, theft_risk, accident_risk, overall_score, unified_cargo, accident_cargo):
        recommendations = []

        # Info sobre mapeamento
        recommendations.append(f"📦 Análise para: '{unified_cargo}'")

        # Recomendações baseadas em roubo
        if theft_risk['risk_category'] in ['ALTO', 'CRÍTICO']:
            recommendations.append(f"⚠️ Alto risco de roubo ({theft_risk['risk_category']}) - Considere rotas alternativas")
            if len(theft_risk['critical_segments']) > 0:
                recommendations.append(f"🔴 {len(theft_risk['critical_segments'])} pontos críticos de roubo")

        # Recomendações baseadas em acidentes
        if accident_risk['risk_category'] in ['ALTO', 'CRÍTICO']:
            recommendations.append(f"⚠️ Alto risco de acidentes ({accident_risk['risk_category']}) - Dirija com cautela")

        if accident_risk.get('weather_multiplier', 1.0) > 1.3:
            recommendations.append(f"🌧️ Condições climáticas adversas aumentam risco de acidentes")

        # Recomendações temporais
        if theft_risk['temporal_multiplier'] > 1.5 or accident_risk['temporal_multiplier'] > 1.5:
            recommendations.append("🕐 Horário de alto risco - Considere alterar horário")

        # Recomendações de carga
        if theft_risk['cargo_factor'] > 0.5:
            recommendations.append(f"📦 Carga '{unified_cargo}' tem alto fator de risco para roubos")

        # Geral
        if overall_score < 0.3:
            recommendations.append("✅ Rota com baixo risco geral")
        elif overall_score > 0.7:
            recommendations.append("🚨 Risco geral elevado - Avalie alternativas")

        if len(recommendations) == 1:  # Só tem o mapeamento
            recommendations.append("✅ Rota dentro dos parâmetros aceitáveis")

        return recommendations
