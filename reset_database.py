"""
EduLift AI - Database Reset Utility
WARNING: Running this script will completely ERASE the current local SQLite
database and re-create all tables with fresh demonstration seed data.
"""

import sys
from database import drop_all_tables, init_db
from seed_data import seed_database


def reset_database(confirm: bool = False):
    """Drop all tables, recreate them, and seed fresh demonstration records."""
    print("=" * 60)
    print("WARNING: This will delete all local database tables and contents!")
    print("=" * 60)

    drop_all_tables()
    print("-> All existing database tables have been dropped.")

    init_db()
    print("-> Database schema re-initialized.")

    seed_database()
    print("-> Fresh demonstration data seeded successfully.")
    print("=" * 60)
    print("Database reset complete. You can now log in with demo accounts.")


if __name__ == "__main__":
    reset_database(confirm=True)
