import streamlit as st
import pandas as pd
# Import the established SQLAlchemy connection object
from auth_db import conn

def view_users():
    """
    Displays all registered users from the 'users' table using a Streamlit interface.
    """
    st.title("👤 Registered Users")
    st.subheader("List of all users in the 'users' table (excluding password hash)")

    # Check if the connection object from auth_db.py is successfully established
    if conn is not None:
        try:
            # SQL query to select ID, Name, and Email from the users table
            # We exclude the 'password' column for security.
            query = "SELECT id, name, email FROM users"

            # Use pandas to read the SQL query result directly into a DataFrame
            df = pd.read_sql(query, conn)

            # Display the DataFrame in Streamlit
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                st.success(f"Successfully retrieved {len(df)} users.")
            else:
                st.info("No users found in the 'users' table.")

        except Exception as e:
            st.error(f"Error fetching data from the database: {e}")
            st.warning("Ensure the 'users' table exists and the connection is active.")
    else:
        st.warning("Database connection failed. Please ensure your MySQL server is running and your Streamlit secrets are configured correctly.")

if __name__ == "__main__":
    # The script must be run via Streamlit (streamlit run viewusers.py)
    # for st.secrets to be available to auth_db.py
    view_users()