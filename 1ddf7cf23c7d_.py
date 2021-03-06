"""empty message

Revision ID: 1ddf7cf23c7d
Revises: c603d5b8a1c1
Create Date: 2022-06-12 23:54:09.721261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ddf7cf23c7d'
down_revision = 'c603d5b8a1c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles')
    op.drop_table('user_roles')
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('farmer_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('fk_products_user_id_users', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_products_farmer_id_farmers'), 'farmers', ['farmer_id'], ['id'])
        batch_op.drop_column('user_id')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('business_name')
        batch_op.drop_column('business_desc')
        batch_op.drop_column('contact')
        batch_op.drop_column('business_addr')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('business_addr', sa.VARCHAR(length=150), nullable=True))
        batch_op.add_column(sa.Column('contact', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('business_desc', sa.TEXT(), nullable=True))
        batch_op.add_column(sa.Column('business_name', sa.VARCHAR(length=200), nullable=True))

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_products_farmer_id_farmers'), type_='foreignkey')
        batch_op.create_foreign_key('fk_products_user_id_users', 'users', ['user_id'], ['id'])
        batch_op.drop_column('farmer_id')

    op.create_table('user_roles',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('role_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='fk_user_roles_role_id_roles', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_user_roles_user_id_users', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='pk_user_roles')
    )
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('description', sa.VARCHAR(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_roles')
    )
    # ### end Alembic commands ###
