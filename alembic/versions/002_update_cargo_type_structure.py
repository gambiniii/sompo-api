"""update cargo_type structure

Revision ID: 002
Revises: 001
Create Date: 2024-10-14 17:20:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    # Drop old cargo_type table if exists
    op.execute("DROP TABLE IF EXISTS cargo_type CASCADE")

    # Create new cargo_type table with updated structure
    op.create_table(
        "cargo_type",
        sa.Column("id", sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column("categoria", sa.String(50), nullable=False),
        sa.Column("risco_roubo_percentual", sa.Float(), nullable=False),
        sa.Column("risco_acidente_percentual", sa.Float(), nullable=False),
        sa.Column("descricao", sa.String(500), nullable=False),
        sa.Column("exemplos", sa.Text(), nullable=True),
        sa.Column("riscos_principais", sa.String(500), nullable=True),
        sa.Column("impacto_ambiental", sa.String(100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Insert initial data from the spreadsheet
    op.execute("""
        INSERT INTO cargo_type (categoria, risco_roubo_percentual, risco_acidente_percentual, descricao, exemplos, riscos_principais, impacto_ambiental)
        VALUES
        ('Geral', 32.3, 9, 'Carga geral, múltiplos produtos pequenos', 'Diversos produtos misturados em um mesmo carregamento', NULL, NULL),
        ('Geral', 21.4, 4, 'Produtos de tabaco', 'Cigarros, charutos, fumo', NULL, NULL),
        ('Geral', 15.6, 3, 'Produtos farmacêuticos', 'Remédios, antibióticos, medicamentos controlados', NULL, NULL),
        ('Geral', 11.5, 8, 'Produtos alimentícios', 'Alimentos em geral, produtos perecíveis, refrigerados', NULL, NULL),
        ('Geral', 10.6, 2, 'Produtos eletrônicos', 'Celulares, computadores, TVs, eletrodomésticos', NULL, NULL),
        ('Geral', 6.1, 7, 'Peças automotivas e componentes', 'Pneus, peças de motor, componentes automotivos', NULL, NULL),
        ('Geral', 0.3, 5, 'Produtos de higiene e cosméticos', 'Shampoo, sabonete, maquiagem, perfumes', NULL, NULL),
        ('Geral', 0.3, 5, 'Produtos para saúde não-controlados', 'Suplementos, vitaminas, produtos ortopédicos', NULL, NULL),
        ('Geral', 0.5, 15, 'Minérios e materiais pesados', 'Ferro, cobre, minério de ferro, materiais de construção', NULL, NULL),
        ('Geral', 0.13, 12, 'Produtos agrícolas', 'Grãos, sementes, soja, milho, café', NULL, NULL),
        ('Geral', 0.25, 10, 'Bebidas alcoólicas', 'Cerveja, vinho, destilados, cachaça', NULL, NULL),
        ('Perigosa', 5, 37.5, 'Combustíveis e líquidos inflamáveis', 'Gasolina, diesel, etanol, solventes', 'Incêndio, explosão', 'Muito Alto'),
        ('Perigosa', 2, 17.5, 'Substâncias corrosivas', 'Ácido sulfúrico, soda cáustica, ácido clorídrico', 'Queimaduras, corrosão', 'Alto'),
        ('Perigosa', 3, 11, 'Gases sob pressão', 'GLP, GNV, amônia, oxigênio, acetileno', 'Explosão, sufocamento', 'Alto'),
        ('Perigosa', 1.5, 9, 'Substâncias tóxicas e infectantes', 'Cianeto, pesticidas, agrotóxicos', 'Nuvem tóxica, intoxicação', 'Muito Alto'),
        ('Perigosa', 0.5, 9, 'Resíduos industriais e hospitalares', 'Resíduos hospitalares, químicos industriais', 'Contaminação crônica', 'Alto'),
        ('Perigosa', 0.1, 6.5, 'Materiais explosivos Classe 1', 'TNT, dinamite, munição, fogos de artifício', 'Detonação, fragmentos', 'Muito Alto'),
        ('Perigosa', 8, 6, 'Baterias de íon-lítio', 'Baterias de veículos elétricos, celulares, notebooks', 'Incêndio, fumaça tóxica', 'Moderado'),
        ('Perigosa', 0.05, 4, 'Materiais radioativos Classe 7', 'Isótopos médicos, material radioativo para radioterapia', 'Radiação ionizante', 'Muito Alto')
    """)


def downgrade():
    op.drop_table("cargo_type")
