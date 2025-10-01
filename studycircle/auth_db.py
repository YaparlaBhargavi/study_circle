import streamlit as st
from sqlalchemy import create_engine
import os # Import the os module for robust environment variable checks

# Initialize engine to None for safe access in case of connection failure
engine = None

# --- Database Connection Logic ---

# Check for the presence of the necessary flat secrets in st.secrets
if (
    "DB_USER" in st.secrets and 
    "DB_PASSWORD" in st.secrets and
    "DB_HOST" in st.secrets and 
    "DB_PORT" in st.secrets and 
    "DB_DB" in st.secrets # Use DB_DB to match the variable in your screenshot
):
    try:
        # Read credentials from Streamlit secrets (using the flat keys you entered)
        MYSQL_USER = st.secrets["DB_USER"]
        MYSQL_PASSWORD = st.secrets["DB_PASSWORD"]
        MYSQL_HOST = st.secrets["DB_HOST"]
        MYSQL_PORT = st.secrets["DB_PORT"]
        MYSQL_DB = st.secrets["DB_DB"] # Using DB_DB to match your variable name

        # Create the SQLAlchemy engine using the MySQL connector dialect
        engine = create_engine(
            f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
        )
        
    except Exception as e:
        # Displays the error on the Streamlit page if connection fails
        st.error(f"❌ Database connection failed during engine creation: {e}")
        engine = None
        
else:
    # This block executes if any of the required secrets are missing, 
    # which is the cause of your "No secrets found" error.
    st.error("❌ Database connection failed: Missing environment variables.")
    st.info("Please ensure you have set DB_HOST, DB_USER, DB_PASSWORD, DB_PORT, and DB_DB in Render.")
    engine = None


def get_db_connection():
    """Returns the database engine object."""
    if engine is None:
        # This handles the 'NoneType object has no attribute 'execute'' error 
        # that occurs if the engine creation failed.
        return None 
    
    # Establish the connection object that main_app.py should use
    try:
        conn = engine.connect()
        return conn
    except Exception as e:
        st.error(f"❌ Database connection failed when opening connection: {e}")
        return None

# The rest of your authentication functions (authenticate_user, etc.)
# would use get_db_connection() and conn.execute() 
# but are omitted here for brevity.
