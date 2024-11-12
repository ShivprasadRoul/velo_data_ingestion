import os
from supabase import create_client, Client
from embeddings import process_embedding
from global2 import SUPABASE_KEY, SUPABASE_URL
import streamlit as st

url = "https://yonvhrgmeifiywrqycsw.supabase.co"
key ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlvbnZocmdtZWlmaXl3cnF5Y3N3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzEwNDY3MzQsImV4cCI6MjA0NjYyMjczNH0.TlLAtysOHDTJ7eHrhKK9gtxAMK8GhPlGNc5v4kgd0Zo"
supabase: Client = create_client(url,key)

#insert data into master table 
def insert_data_into_master_table(hscode,prod_name,prod_desc):
    try:
        # Process embedding
        prod_embedding = process_embedding(prod_desc).tolist()

        # Prepare data for insertion
        data = {
            "hs_code": hscode,
            "prod_name": prod_name,
            "prod_desc": prod_desc,
            "prod_embedding": prod_embedding
        }

        # Insert into master_table
        supabase.from_("master_table").insert(data).execute()
        create_hscode_section_content_table(hscode)
        create_market_trend_table(hscode)
        st.info("Record Added and two new tables created")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    
# Create hscode_section_content table
# Create hscode_section_content table using execute_sql stored procedure
def create_hscode_section_content_table(hscode):
    try:
        query = f"""
        CREATE TABLE IF NOT EXISTS {hscode} (
            id SERIAL PRIMARY KEY,
            hs_code VARCHAR NOT NULL REFERENCES master_table (hs_code) ON DELETE CASCADE,
            section_content TEXT NOT NULL,
            section_content_id SERIAL UNIQUE,
            embedding VECTOR(1024)
        );
        """
        # Execute the query using the stored procedure
        response = supabase.rpc('execute_sql', {'sql': query}).execute()
        
        if response.error:
            st.error(f"Error creating {hscode} table: {response.error}")
        else:
            st.info(f"Table {hscode} created successfully.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Create market_trend table using execute_sql stored procedure
def create_market_trend_table(hscode):
    try:
        query = f"""
        CREATE TABLE IF NOT EXISTS {hscode+"market_trend"} (
            id SERIAL PRIMARY KEY,
            hs_code VARCHAR NOT NULL REFERENCES master_table (hs_code) ON DELETE CASCADE,
            trend_content TEXT NOT NULL,
            trend_content_id SERIAL UNIQUE,
            embedding VECTOR(1024)
        );
        """
        # Execute the query using the stored procedure
        supabase.rpc('execute_sql', {'sql': query}).execute()
        st.info("market_trend table created successfully.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
        
def fetch_hscode_product_names():
    try:
        # Query to fetch hs_code and product name
        response = supabase.table("master_table").select("hs_code, prod_name").execute()
        
        # Extract hs_code and product name as a list of tuples
        hscode_product_list = [
            (item["hs_code"], item["prod_name"]) for item in response.data
        ]
        return hscode_product_list

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []