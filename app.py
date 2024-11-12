import streamlit as st
from configsuper import insert_data_into_master_table, fetch_hscode_product_names


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to",["Insert into master table","Insert into HS code table","Chat"])
if page == "Insert into master table":
    #insert data into master table page section
    st.title("Product Management System")
    st.subheader("Add New Product to Master Table")
    hs_code = st.text_input("HS Code", key="hs_code_input")
    prod_name= st.text_input(" product name", key="prod_name_input")
    description = st.text_area("Product Description(keep it under 200 character)", key="description_input")
        
    if st.button("Add Product", key="add_product_button"):
        if hs_code and description:
            insert_data_into_master_table(hs_code,prod_name,description)
            
elif page =="Insert into HS code table":
    # insert data into table based on hs code selection 
    st.header("code for intert data into table which will be indexing")
    hscode_product_list = fetch_hscode_product_names()
    if hscode_product_list:
        # Dropdown for selecting HS code and product name
        selected_hscode_product = st.selectbox(
            "Select HS Code and Product Name",
            hscode_product_list,
            format_func=lambda x: f"{x[0]} - {x[1]}"
        )
        # After selecting the HS code and product, show file type options
        file_type = st.selectbox(
            "Select the type of file",
            ("Normal File", "File Containing Table")
        )
        # Show a message or perform actions based on file type selection
        if file_type == "Normal File":
            st.write("You selected a normal file.")
            # Add further actions for normal file handling here
        elif file_type == "File Containing Table":
            st.write("You selected a file containing a table.")
            # Add further actions for table file handling here
        
elif page =="Chat":
    st.header("Chat Interface")

    