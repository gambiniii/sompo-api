"""
Mapeamento unificado de tipos de carga baseado na planilha.
Os tipos agora vêm do banco de dados (tabela cargo_type).

Este arquivo mantém o mapeamento entre os nomes da planilha unificada
e os nomes usados nos modelos de ML (ambos os modelos foram atualizados com os 19 tipos).
"""

# Tipos disponíveis nos modelos (ambos têm os mesmos 19 tipos):
# Cargas Fracionadas, Cigarros, Medicamentos, Alimentício, Eletroeletrônicos,
# Peças/Autopeças, Higiene/Cosmético, Produto p/ Saúde, Minérios, Agrícola,
# Bebidas Alcoólicas, Líquidos Inflamáveis, Corrosivos, Gases (inflamáveis/tóxicos),
# Tóxicos/Infectantes, Resíduos Perigosos, Explosivos, Baterias de Lítio, Radioativos

# Mapeamento: Descrição da Planilha Unificada -> Nome no Modelo
UNIFIED_TO_MODEL = {
    # Categoria GERAL
    'Carga geral, múltiplos produtos pequenos': 'Cargas Fracionadas',
    'Produtos de tabaco': 'Cigarros',
    'Produtos farmacêuticos': 'Medicamentos',
    'Produtos alimentícios': 'Alimentício',
    'Produtos eletrônicos': 'Eletroeletrônicos',
    'Peças automotivas e componentes': 'Peças/Autopeças',
    'Produtos de higiene e cosméticos': 'Higiene/Cosmético',
    'Produtos para saúde não-controlados': 'Produto p/ Saúde',
    'Minérios e materiais pesados': 'Minérios',
    'Produtos agrícolas': 'Agrícola',
    'Bebidas alcoólicas': 'Bebidas Alcoólicas',

    # Categoria PERIGOSA
    'Combustíveis e líquidos inflamáveis': 'Líquidos Inflamáveis',
    'Substâncias corrosivas': 'Corrosivos',
    'Gases sob pressão': 'Gases (inflamáveis/tóxicos)',
    'Substâncias tóxicas e infectantes': 'Tóxicos/Infectantes',
    'Resíduos industriais e hospitalares': 'Resíduos Perigosos',
    'Materiais explosivos Classe 1': 'Explosivos',
    'Baterias de íon-lítio': 'Baterias de Lítio',
    'Materiais radioativos Classe 7': 'Radioativos',
}


def map_to_model(unified_cargo: str) -> str:
    """
    Mapeia tipo de carga da planilha unificada para o nome usado nos modelos de ML.

    Ambos os modelos (roubo e acidente) agora usam os mesmos 19 tipos.

    Args:
        unified_cargo: Descrição do tipo de carga da planilha unificada

    Returns:
        Tipo de carga correspondente nos modelos de ML
    """
    return UNIFIED_TO_MODEL.get(unified_cargo, 'Cargas Fracionadas')


def map_to_theft_model(unified_cargo: str) -> str:
    """
    Mapeia tipo de carga da planilha unificada para o modelo de roubo.
    (Wrapper para compatibilidade - ambos os modelos usam o mesmo mapeamento)
    """
    return map_to_model(unified_cargo)


def map_to_accident_model(unified_cargo: str) -> str:
    """
    Mapeia tipo de carga da planilha unificada para o modelo de acidentes.
    (Wrapper para compatibilidade - ambos os modelos usam o mesmo mapeamento)
    """
    return map_to_model(unified_cargo)


def validate_unified_cargo(cargo: str) -> bool:
    """
    Valida se a carga existe no mapeamento unificado.

    Args:
        cargo: Descrição do tipo de carga

    Returns:
        True se a carga é válida, False caso contrário
    """
    return cargo in UNIFIED_TO_MODEL
