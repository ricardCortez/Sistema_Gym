"""Agrega columna codigo_unico a Socio y Entrenador

Revision ID: d9a41be5cbb4
Revises: 
Create Date: 2024-05-16 18:17:48.180006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9a41be5cbb4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('entrenador', schema=None) as batch_op:
        batch_op.add_column(sa.Column('codigo_unico', sa.String(length=36), nullable=True))
        batch_op.create_unique_constraint(None, ['codigo_unico'])

    with op.batch_alter_table('socio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('codigo_unico', sa.String(length=36), nullable=True))
        batch_op.create_unique_constraint(None, ['codigo_unico'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('socio', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('codigo_unico')

    with op.batch_alter_table('entrenador', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('codigo_unico')

    # ### end Alembic commands ###