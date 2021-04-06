"""TransferInfo

Revision ID: f0bc2d58289f
Revises: 50417ee80aa2
Create Date: 2021-04-06 10:14:10.686393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0bc2d58289f'
down_revision = '50417ee80aa2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transfer_info',
    sa.Column('row_id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('row_created', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('row_updated', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('wallet_address', sa.VARCHAR(length=50), nullable=False),
    sa.Column('transfer_time', sa.DateTime(), nullable=False),
    sa.Column('transfer_fees', sa.DECIMAL(precision=19, scale=8), nullable=False),
    sa.Column('transfer_transaction', sa.VARCHAR(length=50), nullable=False),
    sa.Column('transfer_amount_in_cogs', sa.DECIMAL(precision=19, scale=8), nullable=False),
    sa.Column('transfer_status', sa.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('row_id')
    )
    op.create_index(op.f('ix_transfer_info_wallet_address'), 'transfer_info', ['wallet_address'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transfer_info_wallet_address'), table_name='transfer_info')
    op.drop_table('transfer_info')
    # ### end Alembic commands ###
