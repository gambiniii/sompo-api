"""
Tipos de Carga Unificados - baseado na planilha consolidada
Inclui informações de risco para ROUBO e ACIDENTE
"""

from typing import Dict, List

# Estrutura completa de tipos de carga
UNIFIED_CARGO_TYPES = [
    {
        'id': 1,
        'nome': 'Cargas Fracionadas',
        'categoria': 'Geral',
        'risco_roubo_percentual': 32.3,
        'risco_acidente_percentual': 9,
        'descricao': 'Carga geral, múltiplos produtos pequenos',
        'exemplos': 'Diversos produtos misturados em um mesmo carregamento',
    },
    {
        'id': 2,
        'nome': 'Cigarros',
        'categoria': 'Geral',
        'risco_roubo_percentual': 21.4,
        'risco_acidente_percentual': 4,
        'descricao': 'Produtos de tabaco',
        'exemplos': 'Cigarros, charutos, fumo',
    },
    {
        'id': 3,
        'nome': 'Medicamentos',
        'categoria': 'Geral',
        'risco_roubo_percentual': 15.6,
        'risco_acidente_percentual': 3,
        'descricao': 'Produtos farmacêuticos',
        'exemplos': 'Remédios, antibióticos, medicamentos controlados',
    },
    {
        'id': 4,
        'nome': 'Alimentício',
        'categoria': 'Geral',
        'risco_roubo_percentual': 11.5,
        'risco_acidente_percentual': 8,
        'descricao': 'Produtos alimentícios',
        'exemplos': 'Alimentos em geral, produtos perecíveis, refrigerados',
    },
    {
        'id': 5,
        'nome': 'Eletroeletrônicos',
        'categoria': 'Geral',
        'risco_roubo_percentual': 10.6,
        'risco_acidente_percentual': 2,
        'descricao': 'Produtos eletrônicos',
        'exemplos': 'Celulares, computadores, TVs, eletrodomésticos',
    },
    {
        'id': 6,
        'nome': 'Peças/Autopeças',
        'categoria': 'Geral',
        'risco_roubo_percentual': 6.1,
        'risco_acidente_percentual': 7,
        'descricao': 'Peças automotivas e componentes',
        'exemplos': 'Pneus, peças de motor, componentes automotivos',
    },
    {
        'id': 7,
        'nome': 'Higiene/Cosmético',
        'categoria': 'Geral',
        'risco_roubo_percentual': 0.3,
        'risco_acidente_percentual': 5,
        'descricao': 'Produtos de higiene e cosméticos',
        'exemplos': 'Shampoo, sabonete, maquiagem, perfumes',
    },
    {
        'id': 8,
        'nome': 'Produto p/ Saúde',
        'categoria': 'Geral',
        'risco_roubo_percentual': 0.3,
        'risco_acidente_percentual': 5,
        'descricao': 'Produtos para saúde não-controlados',
        'exemplos': 'Suplementos, vitaminas, produtos ortopédicos',
    },
    {
        'id': 9,
        'nome': 'Minérios',
        'categoria': 'Geral',
        'risco_roubo_percentual': 0.5,
        'risco_acidente_percentual': 15,
        'descricao': 'Minérios e materiais pesados',
        'exemplos': 'Ferro, cobre, minério de ferro, materiais de construção',
    },
    {
        'id': 10,
        'nome': 'Agrícola',
        'categoria': 'Geral',
        'risco_roubo_percentual': 0.13,
        'risco_acidente_percentual': 12,
        'descricao': 'Produtos agrícolas',
        'exemplos': 'Grãos, sementes, soja, milho, café',
    },
    {
        'id': 11,
        'nome': 'Bebidas Alcoólicas',
        'categoria': 'Geral',
        'risco_roubo_percentual': 0.25,
        'risco_acidente_percentual': 10,
        'descricao': 'Bebidas alcoólicas',
        'exemplos': 'Cerveja, vinho, destilados, cachaça',
    },
    {
        'id': 12,
        'nome': 'Líquidos Inflamáveis',
        'categoria': 'Perigosa',
        'risco_roubo_percentual': 5,
        'risco_acidente_percentual': 37.5,
        'descricao': 'Combustíveis e líquidos inflamáveis',
        'exemplos': 'Gasolina, diesel, etanol, solventes',
        'riscos_principais': 'Incêndio, explosão',
        'impacto_ambiental': 'Muito Alto',
    },
    {
        'id': 13,
        'nome': 'Corrosivos',
        'categoria': 'Perigosa',
        'risco_roubo_percentual': 2,
        'risco_acidente_percentual': 17.5,
        'descricao': 'Substâncias corrosivas',
        'exemplos': 'Ácido sulfúrico, soda cáustica, ácido clorídrico',
        'riscos_principais': 'Queimaduras, corrosão',
        'impacto_ambiental': 'Alto',
    },
    {
        'id': 14,
        'nome': 'Gases (inflamáveis/tóxicos)',
        'categoria': 'Perigosa',
        'risco_roubo_percentual': 3,
        'risco_acidente_percentual': 11,
        'descricao': 'Gases sob pressão',
        'exemplos': 'GLP, GNV, amônia, oxigênio, acetileno',
        'riscos_principais': 'Explosão, sufocamento',
        'impacto_ambiental': 'Alto',
    },
    {
        'id': 15,
        'nome': 'Tóxicos/Infectantes',
        'categoria': 'Perigosa',
        'risco_roubo_percentual': 1.5,
        'risco_acidente_percentual': 9,
        'descricao': 'Substâncias tóxicas e infectantes',
        'exemplos': 'Cianeto, pesticidas, agrotóxicos',
        'riscos_principais': 'Nuvem tóxica, intoxicação',
        'impacto_ambiental': 'Muito Alto',
    },
    {
        'id': 16,
        'nome': 'Resíduos Perigosos',
        'categoria': 'Perigosa',
        'risco_roubo_percentual': 0.5,
        'risco_acidente_percentual': 9,
        'descricao': 'Resíduos industriais e hospitalares',
        'exemplos': 'Resíduos hospitalares, químicos industriais',
        'riscos_principais': 'Contaminação crônica',
        'impacto_ambiental': 'Alto',
    },
    {
        'id': 17,
        'nome': 'Explosivos',
        'categoria': 'Perigosa',
        'risco_roubo_percentual': 0.1,
        'risco_acidente_percentual': 6.5,
        'descricao': 'Materiais explosivos Classe 1',
        'exemplos': 'TNT, dinamite, munição, fogos de artifício',
        'riscos_principais': 'Detonação, fragmentos',
        'impacto_ambiental': 'Muito Alto',
    },
    {
        'id': 18,
        'nome': 'Baterias de Lítio',
        'categoria': 'Perigosa',
        'risco_roubo_percentual': 8,
        'risco_acidente_percentual': 6,
        'descricao': 'Baterias de íon-lítio',
        'exemplos': 'Baterias de veículos elétricos, celulares, notebooks',
        'riscos_principais': 'Incêndio, fumaça tóxica',
        'impacto_ambiental': 'Moderado',
    },
    {
        'id': 19,
        'nome': 'Radioativos',
        'categoria': 'Perigosa',
        'risco_roubo_percentual': 0.05,
        'risco_acidente_percentual': 4,
        'descricao': 'Materiais radioativos Classe 7',
        'exemplos': 'Isótopos médicos, material radioativo para radioterapia',
        'riscos_principais': 'Radiação ionizante',
        'impacto_ambiental': 'Muito Alto',
    },
]


def get_all_cargo_names() -> List[str]:
    """Retorna lista de todos os nomes de carga"""
    return [cargo['nome'] for cargo in UNIFIED_CARGO_TYPES]


def get_cargo_by_name(name: str) -> Dict:
    """Retorna informações completas de uma carga pelo nome"""
    for cargo in UNIFIED_CARGO_TYPES:
        if cargo['nome'] == name:
            return cargo
    return None


def get_general_cargos() -> List[Dict]:
    """Retorna apenas cargas da categoria Geral"""
    return [c for c in UNIFIED_CARGO_TYPES if c['categoria'] == 'Geral']


def get_dangerous_cargos() -> List[Dict]:
    """Retorna apenas cargas da categoria Perigosa"""
    return [c for c in UNIFIED_CARGO_TYPES if c['categoria'] == 'Perigosa']


def validate_cargo_name(name: str) -> bool:
    """Valida se o nome da carga existe"""
    return name in get_all_cargo_names()


# Para facilitar lookups
CARGO_NAMES = get_all_cargo_names()
