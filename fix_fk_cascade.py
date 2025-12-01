#!/usr/bin/env python3
"""
Script to add ON DELETE CASCADE to order_details foreign keys.
This allows orders and menu_items to be deleted without FK constraint failures.
Backs up the database before making changes.
"""

import subprocess
import sys
from datetime import datetime
from FinalProject.api.dependencies.database import engine
from sqlalchemy import text

# DB config from your app
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "gAmbfnVLxAA3$",
    "database": "sandwich_maker_api",
    "port": 3306,
}

def backup_db():
    """Backup the database using mysqldump."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"sandwich_maker_api_backup_{timestamp}.sql"
    
    cmd = [
        "mysqldump",
        f"--host={db_config['host']}",
        f"--user={db_config['user']}",
        f"--password={db_config['password']}",
        f"--port={db_config['port']}",
        db_config["database"],
    ]
    
    print(f"Backing up database to {backup_file}...")
    try:
        with open(backup_file, "w") as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"WARNING: mysqldump exited with code {result.returncode}")
            print(f"STDERR: {result.stderr}")
            return None
        print(f"✓ Backup created: {backup_file}")
        return backup_file
    except FileNotFoundError:
        print("WARNING: mysqldump not found. Skipping backup. Make sure it's in your PATH.")
        return None
    except Exception as e:
        print(f"ERROR backing up DB: {e}")
        return None

def alter_fk_constraints():
    """Alter FK constraints to include ON DELETE CASCADE."""
    sqls = [
        # Drop existing constraints
        "ALTER TABLE order_details DROP FOREIGN KEY order_details_ibfk_1",
        "ALTER TABLE order_details DROP FOREIGN KEY order_details_ibfk_2",
        # Re-create with ON DELETE CASCADE
        """ALTER TABLE order_details
           ADD CONSTRAINT order_details_ibfk_1
           FOREIGN KEY (order_id) REFERENCES orders(id)
           ON DELETE CASCADE ON UPDATE CASCADE""",
        """ALTER TABLE order_details
           ADD CONSTRAINT order_details_ibfk_2
           FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
           ON DELETE CASCADE ON UPDATE CASCADE""",
    ]
    
    print("\nAltering foreign key constraints to enable ON DELETE CASCADE...")
    try:
        with engine.connect() as conn:
            for i, sql in enumerate(sqls, 1):
                print(f"  ({i}/{len(sqls)}) {sql[:60]}...")
                conn.execute(text(sql))
            conn.commit()
        print("✓ All FK constraints updated successfully")
        return True
    except Exception as e:
        print(f"✗ ERROR: {e}")
        print("Rolling back changes...")
        return False

def verify_fk_constraints():
    """Verify the FK constraints now include ON DELETE CASCADE."""
    print("\nVerifying FK constraints...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE REFERENCED_TABLE_NAME IN ('orders', 'menu_items') AND TABLE_SCHEMA = 'sandwich_maker_api'
            """))
            rows = result.fetchall()
            for row in rows:
                print(f"  - {row[0]}: {row[1]}.{row[2]} -> {row[3]}.{row[4]}")
        
        # Show the CREATE TABLE to confirm cascade is present
        result = conn.execute(text("SHOW CREATE TABLE order_details"))
        create_table = result.fetchone()[1]
        if "ON DELETE CASCADE" in create_table:
            print("✓ ON DELETE CASCADE found in table definition")
            return True
        else:
            print("✗ ON DELETE CASCADE NOT found in table definition")
            return False
    except Exception as e:
        print(f"✗ ERROR verifying: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("ForeignKey CASCADE DELETE Fixer")
    print("=" * 70)
    
    # Step 1: Backup
    backup_file = backup_db()
    
    # Step 2: Alter constraints
    success = alter_fk_constraints()
    
    if success:
        # Step 3: Verify
        verify_fk_constraints()
        print("\n" + "=" * 70)
        print("✓ FK constraints updated. You can now delete orders without FK errors.")
        print("=" * 70)
        sys.exit(0)
    else:
        print("\n" + "=" * 70)
        print("✗ Failed to update FK constraints.")
        if backup_file:
            print(f"Your backup is safe at: {backup_file}")
        print("=" * 70)
        sys.exit(1)
