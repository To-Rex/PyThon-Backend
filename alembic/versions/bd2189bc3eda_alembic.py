"""alembic

Revision ID: bd2189bc3eda
Revises: 
Create Date: 2023-12-09 02:46:02.792619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd2189bc3eda'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('display_name', sa.String(), nullable=True),
    sa.Column('given_name', sa.String(), nullable=True),
    sa.Column('middle_name', sa.String(), nullable=True),
    sa.Column('prefix', sa.String(), nullable=True),
    sa.Column('suffix', sa.String(), nullable=True),
    sa.Column('family_name', sa.String(), nullable=True),
    sa.Column('company', sa.String(), nullable=True),
    sa.Column('job_title', sa.String(), nullable=True),
    sa.Column('emails', sa.String(), nullable=True),
    sa.Column('phones', sa.String(), nullable=True),
    sa.Column('postal_addresses', sa.String(), nullable=True),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('birthday', sa.String(), nullable=True),
    sa.Column('android_account_type', sa.String(), nullable=True),
    sa.Column('android_account_type_raw', sa.String(), nullable=True),
    sa.Column('android_account_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contacts_display_name'), 'contacts', ['display_name'], unique=False)
    op.create_index(op.f('ix_contacts_id'), 'contacts', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('access_token', sa.String(), nullable=True),
    sa.Column('id_token', sa.String(), nullable=True),
    sa.Column('ids', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('photo_url', sa.String(), nullable=True),
    sa.Column('blocked', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('region', sa.String(), nullable=True),
    sa.Column('device', sa.String(), nullable=True),
    sa.Column('created_at', sa.String(), nullable=True),
    sa.Column('updated_at', sa.String(), nullable=True),
    sa.Column('token', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_contacts_id'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_display_name'), table_name='contacts')
    op.drop_table('contacts')
    # ### end Alembic commands ###
