import streamlit as st
import psycopg2
import pandas as pd

# Function to establish a database connection
def get_database_connection():
    conn = psycopg2.connect(
        dbname="IPL_database",
        user="postgres",
        password="rohith2001",
        host="ipl.ctoewig06f50.us-east-2.rds.amazonaws.com",
        port="5432"
    )
    return conn

# Function to execute SQL query and display results
@st.cache(suppress_st_warning=True)
def execute_query(query):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        # Check if the query starts with a SELECT statement
        if not query.strip().lower().startswith('select'):
            raise ValueError("Only SELECT statements are allowed.")

        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
    finally:
        cursor.close()
        conn.close()

# Streamlit app
def main():
    st.title('IPL Database Viewer')

    # Input field for SQL query
    query = st.text_area("Enter your SQL query:")
    if st.button("Run Query"):
        df = execute_query(query)
        if df is not None:
            st.write(df)

    st.title('Examples of all relations')
    # Display sample data from all tables
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cursor.fetchall()
    for table in tables:
        st.subheader(table[0])
        cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5")
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        st.table(df)

    # Close connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
