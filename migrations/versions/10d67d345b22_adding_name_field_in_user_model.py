"""Adding Name Field in User Model

Revision ID: 10d67d345b22
Revises: 3b431ba16a14
Create Date: 2020-02-02 17:11:31.206464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10d67d345b22'
down_revision = '3b431ba16a14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_MST_USER_email', table_name='MST_USER')
    op.drop_index('ix_MST_USER_username', table_name='MST_USER')
    op.drop_table('MST_USER')
    op.drop_table('MST_TODO')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('MST_TODO',
    sa.Column('item_id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), nullable=False),
    sa.Column('description', sa.VARCHAR(length=200), nullable=False),
    sa.Column('date_created', sa.DATETIME(), nullable=True),
    sa.Column('is_completed', sa.BOOLEAN(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.CheckConstraint('is_completed IN (0, 1)'),
    sa.ForeignKeyConstraint(['user_id'], ['MST_USER.id'], ),
    sa.PrimaryKeyConstraint('item_id')
    )
    op.create_table('MST_USER',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_MST_USER_username', 'MST_USER', ['username'], unique=1)
    op.create_index('ix_MST_USER_email', 'MST_USER', ['email'], unique=1)
    # ### end Alembic commands ###