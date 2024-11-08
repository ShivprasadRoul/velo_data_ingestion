import os
from supabase import create_client, Client
from embeddings import process_embedding
from global2 import SUPABASE_KEY, SUPABASE_URL

url = "https://yonvhrgmeifiywrqycsw.supabase.co"
key ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlvbnZocmdtZWlmaXl3cnF5Y3N3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzEwNDY3MzQsImV4cCI6MjA0NjYyMjczNH0.TlLAtysOHDTJ7eHrhKK9gtxAMK8GhPlGNc5v4kgd0Zo"
supabase: Client = create_client(url,key)

#insert data into master table 
def insert_data_into_master_table(hscode,prod_name,prod_desc):
    data = {
        "hs_code": hscode,
        "prod_name": prod_name,
        "prod_desc": prod_desc,
        "prod_embedding": process_embedding(prod_desc).tolist()
        }
    supabase.from_("master_table").insert(data).execute()
    #create_hscode_table(hscode)
    
#to make hs code table, actually two table is created one is hs code one and ohter is hscode section 
def create_hscode_table(hscode):
    table_name = f"{hscode}_table"
    hscodesection_table = f"{hscode}section"

    # Check if the HS code-specific table exists, and if not, create it
    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        hs_id SERIAL PRIMARY KEY,
        meta_data TEXT NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS {hscodesection_table} (
        id SERIAL PRIMARY KEY,
        hsid INT NOT NULL REFERENCES {table_name}(hs_id) ON DELETE CASCADE,
        section_content TEXT NOT NULL,
        embedding VECTOR(1024)
    );
    """
    
    # Execute the query
    supabase.rpc("execute_sql", {"sql": query}).execute()
    