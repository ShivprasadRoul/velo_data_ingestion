import streamlit as st
from utils.ui import master_table_input, display_search
from database import engine, master_table
from embeddings import generate_embedding
from sqlalchemy import insert, select
from llama_index import LlamaIndex

# Initialize Llama Index (or similar for vector search)
llama_index = LlamaIndex()

# Add new product
hs_code, description = master_table_input()

if st.sidebar.button("Add Product"):
    embedding = generate_embedding(description)
    # Insert data into PostgreSQL
    with engine.connect() as conn:
        conn.execute(insert(master_table).values(
            hs_code=hs_code,
            product_description=description,
            embedding=embedding
        ))
    st.sidebar.success("Product added successfully!")

# Search functionality
search_hs_code, search_desc = display_search()

if st.button("Search"):
    with engine.connect() as conn:
        if search_hs_code:
            query = select([master_table]).where(master_table.c.hs_code == search_hs_code)
        elif search_desc:
            embedding = generate_embedding(search_desc)
            # Use Llama Index to find the most similar embeddings
            results = llama_index.search(embedding)
            st.write(results)
