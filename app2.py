import streamlit as st
from utils.ui import master_table_input, display_search
from config import get_connection
from embeddings import generate_embeddings
import numpy as np 

#from llama_index import LlamaIndex  

#llama_index = LlamaIndex()

# Function to create the master_table if it doesn't exist
def create_master_table():
    create_extension_query = 'CREATE EXTENSION IF NOT EXISTS vector;'
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS master_table (
        hs_code VARCHAR PRIMARY KEY,
        product_description VARCHAR,
        embedding VECTOR(540)  -- Ensure the dimension matches your embeddings
    )
    '''
    with get_connection() as conn:
        with conn.cursor() as cursor:
            # Create the pgvector extension
            cursor.execute(create_extension_query)
            # Create the master_table with a vector column
            cursor.execute(create_table_query)
            conn.commit()

# Call the function to ensure the table exists
create_master_table()

# Add new product
hs_code, description = master_table_input()

if st.sidebar.button("Add Product"):
    embedding = generate_embeddings(description)  # Should be a list of floats

    insert_query = '''
    INSERT INTO master_table (hs_code, product_description, embedding)
    VALUES (%s, %s, %s)
    ON CONFLICT (hs_code) DO NOTHING
    '''
    
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(insert_query, (hs_code, description, embedding.tolist()))
                conn.commit()
                st.sidebar.success("Product added successfully!")
            except Exception as e:
                st.sidebar.error(f"An error occurred: {e}")

# Search functionality
search_hs_code, search_desc = display_search()

if st.button("Search"):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            if search_hs_code:
                # Query for product by hs_code
                query = '''
                SELECT hs_code, product_description, embedding 
                FROM master_table 
                WHERE hs_code = %s
                '''
                
                try:
                    cursor.execute(query, (search_hs_code,))
                    result = cursor.fetchone()
                    if result:
                        st.write({
                            "HS Code": result[0],
                            "Description": result[1],
                            "Embedding": result[2]
                        })
                    else:
                        st.write("No product found with that HS Code.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            elif search_desc:
                # Search based on description using embeddings
                embedding = generate_embeddings(search_desc)
                results = llama_index.search(embedding)
                st.write(results)
