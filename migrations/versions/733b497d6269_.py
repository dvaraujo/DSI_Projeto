"""empty message

Revision ID: 733b497d6269
Revises: 47b6c146859c
Create Date: 2020-09-22 23:08:27.265523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '733b497d6269'
down_revision = '47b6c146859c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('escritorio',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('razao_social', sa.String(length=250), nullable=False),
    sa.Column('cnpj', sa.String(length=14), nullable=False),
    sa.Column('n_oab', sa.String(length=8), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('senha', sa.String(length=200), nullable=False),
    sa.Column('criado_em', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cnpj'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('n_oab'),
    sa.UniqueConstraint('razao_social')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('escritorio')
    # ### end Alembic commands ###