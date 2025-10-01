from sqlalchemy import create_engine
import streamlit as st

# Initialize conn to None for safe access in case of connection failure
conn = None 

try:
    # 1. Read secure credentials from Streamlit secrets
    MYSQL_USER = st.secrets["mysql"]["user"]
    MYSQL_PASSWORD = st.secrets["mysql"]["password"]
    MYSQL_HOST = st.secrets["mysql"]["host"]
    MYSQL_PORT = st.secrets["mysql"]["port"]
    MYSQL_DB = "circle"

    # 2. Create the SQLAlchemy Engine using the mysql.connector dialect
    engine = create_engine(
        f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    
    # 3. Establish the connection object that main_app.py should use
    conn = engine.connect()

except Exception as e:
    # Displays the error on the Streamlit page if connection fails
    st.error(f"❌ Database connection failed: {e}")
