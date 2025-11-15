"""
Alembic migration: Create auth tables (profiles, user_roles, customers, staff)
Support flexible role assignment: 1 user = multiple roles
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "001_create_auth_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create authentication and user profile tables."""

    # 1. Create profiles table
    op.create_table(
        "profiles",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            primary_key=True,
        ),
        sa.Column(
            "user_id", postgresql.UUID(as_uuid=True), nullable=False, unique=True
        ),
        sa.Column("full_name", sa.String(255)),
        sa.Column("avatar_url", sa.Text()),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
    )
    op.create_index("idx_profiles_user_id", "profiles", ["user_id"])

    # 2. Create user_roles table (Many-to-Many: 1 user = many roles)
    op.create_table(
        "user_roles",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            primary_key=True,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column(
            "assigned_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("assigned_by", postgresql.UUID(as_uuid=True)),
        sa.Column(
            "is_primary", sa.Boolean(), server_default=sa.text("false"), nullable=False
        ),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["assigned_by"], ["auth.users.id"], ondelete="SET NULL"
        ),
        sa.CheckConstraint(
            "role IN ('customer', 'receptionist', 'technician', 'admin')",
            name="valid_roles",
        ),
        sa.UniqueConstraint("user_id", "role", name="unique_user_role"),
    )
    op.create_index("idx_user_roles_user_id", "user_roles", ["user_id"])
    op.create_index("idx_user_roles_role", "user_roles", ["role"])
    op.create_index(
        "idx_user_roles_primary",
        "user_roles",
        ["user_id"],
        postgresql_where=sa.text("is_primary = true"),
    )

    # 3. Create customers table
    op.create_table(
        "customers",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            primary_key=True,
        ),
        sa.Column(
            "user_id", postgresql.UUID(as_uuid=True), nullable=False, unique=True
        ),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(20)),
        sa.Column("avatar_url", sa.String(500)),
        sa.Column("date_of_birth", sa.Date()),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
    )
    op.create_index("idx_customers_user_id", "customers", ["user_id"])

    # 4. Create audit_logs table (Security event tracking)
    op.create_table(
        "audit_logs",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            primary_key=True,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True)),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        sa.Column("ip_address", postgresql.INET()),
        sa.Column("user_agent", sa.Text()),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="SET NULL"),
    )
    op.create_index("idx_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("idx_audit_logs_event_type", "audit_logs", ["event_type"])
    op.create_index(
        "idx_audit_logs_created_at",
        "audit_logs",
        ["created_at"],
        postgresql_using="DESC",
    )

    # 5. Create staff table
    op.create_table(
        "staff",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            primary_key=True,
        ),
        sa.Column(
            "user_id", postgresql.UUID(as_uuid=True), nullable=False, unique=True
        ),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(20)),
        sa.Column("avatar_url", sa.String(500)),
        sa.Column("specialization", sa.String(100)),
        sa.Column("bio", sa.Text()),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
    )
    op.create_index("idx_staff_user_id", "staff", ["user_id"])

    # 6. Enable RLS on all tables
    op.execute("ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE user_roles ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE customers ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE staff ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;")

    # 6. Create RLS Policies for profiles
    op.execute(
        """
        CREATE POLICY "Users can view own profile"
          ON profiles FOR SELECT
          USING (auth.uid() = user_id);
    """
    )

    op.execute(
        """
        CREATE POLICY "Users can update own profile"
          ON profiles FOR UPDATE
          USING (auth.uid() = user_id);
    """
    )

    # 7. Create RLS Policies for user_roles
    op.execute(
        """
        CREATE POLICY "Users can view own roles"
          ON user_roles FOR SELECT
          USING (auth.uid() = user_id);
    """
    )

    # 8. Create RLS Policies for audit_logs
    op.execute(
        """
        CREATE POLICY "Users can view own audit logs"
          ON audit_logs FOR SELECT
          USING (auth.uid() = user_id);
    """
    )

    # 9. Create RLS Policies for customers
    op.execute(
        """
        CREATE POLICY "Customers view own customer profile"
          ON customers FOR SELECT
          USING (auth.uid() = user_id);
    """
    )

    op.execute(
        """
        CREATE POLICY "Customers update own customer profile"
          ON customers FOR UPDATE
          USING (auth.uid() = user_id);
    """
    )

    # 10. Create RLS Policies for staff
    op.execute(
        """
        CREATE POLICY "Staff can view own staff profile"
          ON staff FOR SELECT
          USING (auth.uid() = user_id);
    """
    )


def downgrade() -> None:
    """Drop authentication and user profile tables."""

    # Drop RLS policies (automatic with table drop)
    op.drop_table("audit_logs")
    op.drop_table("staff")
    op.drop_table("customers")
    op.drop_table("user_roles")
    op.drop_table("profiles")
