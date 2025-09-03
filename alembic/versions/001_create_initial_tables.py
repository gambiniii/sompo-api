# filepath: c:\Users\lucas\OneDrive\Área de Trabalho\FIAP\__SOMPO\Implementação\sompo-api\alembic\versions\001_create_initial_tables.py
"""create initial tables

Revision ID: 001
Revises:
Create Date: 2023-09-03 10:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create police_occurrence_types table
    op.create_table(
        "police_occurrence_types",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create hexagons table
    op.create_table(
        "hexagons",
        sa.Column("id", sa.String(20), nullable=False),
        sa.Column("resolution", sa.BigInteger(), nullable=False),
        sa.Column("danger_percentage", sa.Float(53), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create traffic_occurrence_types table
    op.create_table(
        "traffic_occurrence_types",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create police_occurrences table
    op.create_table(
        "police_occurrences",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("police_occurrence_type_id", sa.BigInteger(), nullable=False),
        sa.Column("description", sa.String(255), nullable=False),
        sa.Column("lat", sa.Float(53), nullable=False),
        sa.Column("lng", sa.Float(53), nullable=False),
        sa.Column("occurred_at", sa.Date(), nullable=False),
        sa.Column("h3_id", sa.String(20), nullable=False),
        sa.ForeignKeyConstraint(
            ["police_occurrence_type_id"], ["police_occurrence_types.id"]
        ),
        sa.ForeignKeyConstraint(["h3_id"], ["hexagons.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create traffic_occurrences table
    op.create_table(
        "traffic_occurrences",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("traffic_occurrence_type_id", sa.BigInteger(), nullable=False),
        sa.Column("description", sa.String(255), nullable=False),
        sa.Column("lat", sa.Float(53), nullable=False),
        sa.Column("lng", sa.Float(53), nullable=False),
        sa.Column("occurred_at", sa.Date(), nullable=False),
        sa.Column("h3_id", sa.String(20), nullable=False),
        sa.ForeignKeyConstraint(
            ["traffic_occurrence_type_id"], ["traffic_occurrence_types.id"]
        ),
        sa.ForeignKeyConstraint(["h3_id"], ["hexagons.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create hexagon_occurrence_stats table
    op.create_table(
        "hexagon_occurrence_stats",
        sa.Column("h3_id", sa.String(20), nullable=False),
        sa.Column("occurrence_type", sa.String(50), nullable=False),
        sa.Column("type_id", sa.BigInteger(), nullable=False),
        sa.Column("count", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(["h3_id"], ["hexagons.id"]),
        sa.PrimaryKeyConstraint("h3_id", "occurrence_type", "type_id"),
    )


def downgrade():
    op.drop_table("hexagon_occurrence_stats")
    op.drop_table("traffic_occurrences")
    op.drop_table("police_occurrences")
    op.drop_table("traffic_occurrence_types")
    op.drop_table("police_occurrence_types")
    op.drop_table("hexagons")
