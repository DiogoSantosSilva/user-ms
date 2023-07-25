"""empty message

Revision ID: 120c64379418
Revises: b1f97b071f64
Create Date: 2023-07-23 17:55:31.884661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '120c64379418'
down_revision = 'b1f97b071f64'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('responsible_for',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entity_name', sa.String(), nullable=True),
    sa.Column('responsible_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['responsible_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_responsible_for_id'), 'responsible_for', ['id'], unique=False)
    op.drop_constraint('users_responsible_for_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'responsible_for_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('responsible_for_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_responsible_for_id_fkey', 'users', 'users', ['responsible_for_id'], ['id'])
    op.drop_index(op.f('ix_responsible_for_id'), table_name='responsible_for')
    op.drop_table('responsible_for')
    # ### end Alembic commands ###
