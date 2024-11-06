# database.py
from config import get_connection

# Function to create the master table
def create_master_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS master_table (
        hs_code VARCHAR PRIMARY KEY,
        product_description VARCHAR,
        embedding FLOAT
    )
    '''
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(create_table_query)
        conn.commit()
        print("Master table created successfully.")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        cursor.close()
        conn.close()

# Example function to insert data
def insert_into_master_table(hs_code, product_description, embedding):
    insert_query = '''
    INSERT INTO master_table (hs_code, product_description, embedding)
    VALUES (%s, %s, %s)
    ON CONFLICT (hs_code) DO NOTHING
    '''
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(insert_query, (hs_code, product_description, embedding))
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        cursor.close()
        conn.close()


