"""Refactor schema

Revision ID: 828137a176a6
Revises: f0e4886da080
Create Date: 2025-11-24 16:46:43.111672

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = "828137a176a6"
down_revision: Union[str, None] = "f0e4886da080"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create roles table
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_roles_name"), "roles", ["name"], unique=True)

    # 2. Seed roles
    op.execute(
        "INSERT INTO roles (name, description) VALUES ('customer', 'Khách hàng')"
    )
    op.execute(
        "INSERT INTO roles (name, description) VALUES ('receptionist', 'Lễ tân')"
    )
    op.execute(
        "INSERT INTO roles (name, description) VALUES ('technician', 'Kỹ thuật viên')"
    )
    op.execute(
        "INSERT INTO roles (name, description) VALUES ('admin', 'Quản trị viên')"
    )

    # 3. Drop email from profiles
    op.drop_column("profiles", "email")

    # 4. Migrate user_role_links
    # Add role_id as nullable first
    op.add_column("user_role_links", sa.Column("role_id", sa.Integer(), nullable=True))

    # Update role_id based on role_name
    # Cast role_name to text because it was an Enum
    op.execute(
        """
        UPDATE user_role_links
        SET role_id = roles.id
        FROM roles
        WHERE user_role_links.role_name::text = roles.name
    """
    )

    # Delete orphans if any
    op.execute("DELETE FROM user_role_links WHERE role_id IS NULL")

    # Alter column to not null
    op.alter_column("user_role_links", "role_id", nullable=False)

    # Create FK
    op.create_foreign_key(None, "user_role_links", "roles", ["role_id"], ["id"])

    # Drop old column
    op.drop_column("user_role_links", "role_name")

    # 5. Create Trigger for auth.users (Cascade Delete)
    # Note: This requires permissions on auth schema
    # We wrap in a block that might fail silently if permissions are missing,
    # but for Alembic it's better to let it fail or handle explicitly.
    # Here we just execute it. If it fails, user needs to run SQL manually.
    try:
        op.execute(
            """
            CREATE OR REPLACE FUNCTION public.handle_deleted_user()
            RETURNS TRIGGER AS $$
            BEGIN
              DELETE FROM public.profiles WHERE id = OLD.id;
              RETURN OLD;
            END;
            $$ LANGUAGE plpgsql SECURITY DEFINER;
        """
        )

        op.execute(
            """
            DROP TRIGGER IF EXISTS on_auth_user_deleted ON auth.users;
            CREATE TRIGGER on_auth_user_deleted
              AFTER DELETE ON auth.users
              FOR EACH ROW EXECUTE PROCEDURE public.handle_deleted_user();
        """
        )
    except Exception as e:
        print(f"WARNING: Could not create trigger on auth.users. Error: {e}")
        print("Please run the trigger creation SQL manually in Supabase SQL Editor.")


def downgrade() -> None:
    # Drop trigger
    try:
        op.execute("DROP TRIGGER IF EXISTS on_auth_user_deleted ON auth.users;")
        op.execute("DROP FUNCTION IF EXISTS public.handle_deleted_user();")
    except Exception:
        pass

    # Revert user_role_links
    # Create enum type again
    sa.Enum("CUSTOMER", "RECEPTIONIST", "TECHNICIAN", "ADMIN", name="role").create(
        op.get_bind()
    )

    op.add_column(
        "user_role_links",
        sa.Column(
            "role_name",
            postgresql.ENUM(
                "CUSTOMER", "RECEPTIONIST", "TECHNICIAN", "ADMIN", name="role"
            ),
            autoincrement=False,
            nullable=True,
        ),
    )

    # Restore data (reverse mapping)
    op.execute(
        """
        UPDATE user_role_links
        SET role_name = roles.name::role
        FROM roles
        WHERE user_role_links.role_id = roles.id
    """
    )

    op.alter_column("user_role_links", "role_name", nullable=False)

    op.drop_constraint(None, "user_role_links", type_="foreignkey")
    op.drop_column("user_role_links", "role_id")

    # Restore profiles.email (will be null initially)
    op.add_column(
        "profiles", sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True)
    )

    op.drop_index(op.f("ix_roles_name"), table_name="roles")
    op.drop_table("roles")
