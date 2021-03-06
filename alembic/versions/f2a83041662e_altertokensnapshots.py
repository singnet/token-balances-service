"""AlterTokenSnapshots

Revision ID: f2a83041662e
Revises: bc1b1ea7e711
Create Date: 2021-05-25 10:15:59.315193

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "f2a83041662e"
down_revision = "db70140f9c2e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "token_snapshots", sa.Column("is_considered", mysql.BIT(), nullable=True)
    )
    op.add_column(
        "token_snapshots", sa.Column("comment", sa.VARCHAR(length=256), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("token_snapshots", "is_considered")
    op.drop_column("token_snapshots", "comment")
    # ### end Alembic commands ###
