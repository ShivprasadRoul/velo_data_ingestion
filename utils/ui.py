import streamlit as st

def master_table_input():
    st.sidebar.header("Add New Product")
    hs_code = st.sidebar.text_input("HS Code")
    description = st.sidebar.text_area("Product Description")
    return hs_code, description

def display_search():
    st.header("Search and Filter Data")
    search_hs_code = st.text_input("Search by HS Code")
    search_desc = st.text_input("Search by Product Description")
    return search_hs_code, search_desc