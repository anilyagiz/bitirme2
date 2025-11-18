"""Initial schema with UUID primary keys

Revision ID: 001
Revises:
Create Date: 2025-11-17 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enum types
    op.execute("CREATE TYPE userrole AS ENUM ('admin', 'staff', 'supervisor')")
    op.execute("CREATE TYPE periodstatus AS ENUM ('planned', 'active', 'completed')")
    op.execute("CREATE TYPE locationtype AS ENUM ('derslik', 'ofis', 'tuvalet', 'koridor', 'diger')")
    op.execute("CREATE TYPE assignmentstatus AS ENUM ('pending', 'in_progress', 'completed', 'verified')")

    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('role', postgresql.ENUM('admin', 'staff', 'supervisor', name='userrole'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Create buildings table
    op.create_table('buildings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('ix_buildings_id', 'buildings', ['id'])
    op.create_index('ix_buildings_name', 'buildings', ['name'], unique=True)
    op.create_index('ix_buildings_code', 'buildings', ['code'], unique=True)

    # Create departments table
    op.create_table('departments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('ix_departments_id', 'departments', ['id'])
    op.create_index('ix_departments_name', 'departments', ['name'], unique=True)
    op.create_index('ix_departments_code', 'departments', ['code'], unique=True)

    # Create periods table
    op.create_table('periods',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('status', postgresql.ENUM('planned', 'active', 'completed', name='periodstatus'), nullable=False, server_default='planned'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('ix_periods_id', 'periods', ['id'])

    # Create locations table
    op.create_table('locations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('location_type', postgresql.ENUM('derslik', 'ofis', 'tuvalet', 'koridor', 'diger', name='locationtype'), nullable=False),
        sa.Column('location_subtype', sa.String(), nullable=True),
        sa.Column('building_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('department_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('parent_location_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_leaf', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('floor_label', sa.String(), nullable=True),
        sa.Column('area_sqm', sa.Integer(), nullable=True),
        sa.Column('special_instructions', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['building_id'], ['buildings.id']),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id']),
        sa.ForeignKeyConstraint(['parent_location_id'], ['locations.id'])
    )
    op.create_index('ix_locations_id', 'locations', ['id'])

    # Create assignments table
    op.create_table('assignments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('location_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('period_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('staff_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('supervisor_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('status', postgresql.ENUM('pending', 'in_progress', 'completed', 'verified', name='assignmentstatus'), nullable=False, server_default='pending'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id']),
        sa.ForeignKeyConstraint(['period_id'], ['periods.id']),
        sa.ForeignKeyConstraint(['staff_id'], ['users.id']),
        sa.ForeignKeyConstraint(['supervisor_id'], ['users.id'])
    )
    op.create_index('ix_assignments_id', 'assignments', ['id'])


def downgrade() -> None:
    op.drop_index('ix_assignments_id', table_name='assignments')
    op.drop_table('assignments')

    op.drop_index('ix_locations_id', table_name='locations')
    op.drop_table('locations')

    op.drop_index('ix_periods_id', table_name='periods')
    op.drop_table('periods')

    op.drop_index('ix_departments_code', table_name='departments')
    op.drop_index('ix_departments_name', table_name='departments')
    op.drop_index('ix_departments_id', table_name='departments')
    op.drop_table('departments')

    op.drop_index('ix_buildings_code', table_name='buildings')
    op.drop_index('ix_buildings_name', table_name='buildings')
    op.drop_index('ix_buildings_id', table_name='buildings')
    op.drop_table('buildings')

    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')

    op.execute('DROP TYPE assignmentstatus')
    op.execute('DROP TYPE locationtype')
    op.execute('DROP TYPE periodstatus')
    op.execute('DROP TYPE userrole')
