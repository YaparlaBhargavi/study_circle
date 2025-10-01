import mysql.connector
import os

# --- Configuration (Hardcoded for Setup) ---
# NOTE: Replace 'cseds@32' with your actual root password if it's different.
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "cseds@32" 
DB_SCRIPT_FILE = "mysql.sql"

def setup_database():
    """
    Reads the full SQL script and executes it against the MySQL server.
    """
    print(f"Attempting to connect to MySQL at {MYSQL_HOST}...")

    try:
        # 1. Connect to MySQL server without specifying a database (to allow CREATE DATABASE)
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        cursor = conn.cursor()

        if not os.path.exists(DB_SCRIPT_FILE):
            print(f"❌ Error: SQL file '{DB_SCRIPT_FILE}' not found in the current directory.")
            return

        # 2. Read SQL script content
        with open(DB_SCRIPT_FILE, 'r') as f:
            sql_script = f.read()

        # 3. Split script into individual commands and execute
        # This handles all commands: CREATE DATABASE, USE, CREATE TABLE, INSERT
        sql_commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]

        print(f"Found {len(sql_commands)} SQL commands to execute from {DB_SCRIPT_FILE}.")

        for command in sql_commands:
            try:
                cursor.execute(command)
                # Commit any changes (like CREATE TABLE and INSERT)
                conn.commit()
            except mysql.connector.Error as err:
                # Ignore common, non-critical errors during setup
                if "already exists" in str(err) or "Unknown database" in str(err):
                    continue
                # Report any other critical errors
                print(f"⚠️ SQL Error during execution: {err} | Command: {command[:80]}...")
            except Exception as e:
                print(f"❌ General Error during execution: {e}")

        print("\n✅ Database 'circle' and all tables/data successfully set up!")

    except mysql.connector.Error as err:
        print(f"❌ Critical Connection/Authentication Error: {err}")
        print("Please ensure your MySQL server is running and the credentials in setup_db.py are correct.")

    finally:
        # Close the connection if it was opened
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")


if __name__ == '__main__':
    setup_database()