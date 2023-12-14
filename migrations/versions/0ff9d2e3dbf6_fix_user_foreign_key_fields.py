"""Fix user foreign key fields.

Revision ID: 0ff9d2e3dbf6
Revises: 4379e60c0dfd
Create Date: 2023-12-14 18:22:19.371452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0ff9d2e3dbf6"
down_revision = "4379e60c0dfd"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("ingredient", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=False))
        batch_op.drop_constraint("ingredient_user_fkey", type_="foreignkey")
        batch_op.create_foreign_key(None, "user", ["user_id"], ["id"])
        batch_op.drop_column("user")

    with op.batch_alter_table("recipe", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=False))
        batch_op.drop_constraint("recipe_user_fkey", type_="foreignkey")
        batch_op.create_foreign_key(None, "user", ["user_id"], ["id"])
        batch_op.drop_column("user")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("recipe", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("user", sa.INTEGER(), autoincrement=False, nullable=False)
        )
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.create_foreign_key("recipe_user_fkey", "user", ["user"], ["id"])
        batch_op.drop_column("user_id")

    with op.batch_alter_table("ingredient", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("user", sa.INTEGER(), autoincrement=False, nullable=False)
        )
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.create_foreign_key("ingredient_user_fkey", "user", ["user"], ["id"])
        batch_op.drop_column("user_id")

    # ### end Alembic commands ###
