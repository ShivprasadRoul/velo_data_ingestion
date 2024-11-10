import streamlit as st
from embeddings import process_embedding
from configsuper import insert_data_into_master_table
from global2 import SUPABASE_KEY, SUPABASE_URL


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to",["Insert into master table","Insert into HS code table","Chat"])
if page == "Insert into master table":
    # Page layout
    st.title("Product Management System")

    st.subheader("Add New Product to Master Table")
    hs_code = st.text_input("HS Code", key="hs_code_input")
    prod_name= st.text_input(" product name", key="prod_name_input")
    description = st.text_area("Product Description(keep it under 200 character)", key="description_input")
        
    if st.button("Add Product", key="add_product_button"):
        if hs_code and description:
            insert_data_into_master_table(hs_code,prod_name,description)
            
elif page =="Insert into HS code table":
    st.header("code for intert data into table which will be indexing")
    
elif page =="Chat":
    st.header("Chat Interface")

    