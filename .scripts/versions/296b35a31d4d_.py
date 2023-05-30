"""empty message

Revision ID: 296b35a31d4d
Revises: 99ad6a918e64
Create Date: 2023-05-30 15:50:06.896927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '296b35a31d4d'
down_revision = '99ad6a918e64'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(op.f('uq_collected_questions_id'), 'collected_questions', ['id'])
    op.create_unique_constraint(op.f('uq_collected_questions_question_id'), 'collected_questions', ['question_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_collected_questions_question_id'), 'collected_questions', type_='unique')
    op.drop_constraint(op.f('uq_collected_questions_id'), 'collected_questions', type_='unique')
    # ### end Alembic commands ###
