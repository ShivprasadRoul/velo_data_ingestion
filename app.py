import streamlit as st
from embeddings import process_embedding
from configsuper import insert_data_into_master_table
from global2 import SUPABASE_KEY, SUPABASE_URL

# Page layout
st.title("Product Management System")

# Main UI
col1, col2 = st.columns(2)

with col1:
    st.subheader("Add New Product")
    hs_code = st.text_input("HS Code", key="hs_code_input")
    prod_name= st.text_input(" product name", key="prod_name_input")
    description = st.text_area("Product Description(keep it under 200 character)", key="description_input")
    
    if st.button("Add Product", key="add_product_button"):
        if hs_code and description:
            insert_data_into_master_table(hs_code,prod_name,description)

with col2:
    st.subheader("Search Products")
    search_hs_code = st.text_input("Search by HS Code", key="search_hs_code_input")
    search_description = st.text_area("Search by Description", key="search_description_input")
    
    if st.button("Search", key="search_button"):
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    if search_hs_code:
                        query = '''
                        SELECT hs_code, product_description 
                        FROM master_table 
                        WHERE hs_code = %s
                        '''
                        cursor.execute(query, (search_hs_code,))
                        result = cursor.fetchone()
                        if result:
                            st.write({
                                "HS Code": result[0],
                                "Description": result[1]
                            })
                        else:
                            st.info("No product found with that HS Code.")
                    elif search_description:
                        embedding = process_embedding(search_description)
                        if embedding is not None:
                            search_query = f'''
                            SELECT 
                                hs_code, 
                                product_description,
                                1 / (1 + (embedding::vector({EMBEDDING_DIM}) <-> ARRAY[%s]::vector({EMBEDDING_DIM}))) as similarity
                            FROM master_table
                            ORDER BY embedding::vector({EMBEDDING_DIM}) <-> ARRAY[%s]::vector({EMBEDDING_DIM})
                            LIMIT 5
                            '''
                            # Convert embedding to comma-separated string
                            embedding_str = ','.join(str(x) for x in embedding.tolist())
                            cursor.execute(search_query, (embedding_str, embedding_str))
                            results = cursor.fetchall()
                            
                            if results:
                                st.write("Search Results:")
                                for r in results:
                                    st.write({
                                        "HS Code": r[0],
                                        "Description": r[1],
                                        "Similarity": f"{r[2]:.2%}"
                                    })
                            else:
                                st.info("No similar products found.")
                    else:
                        st.warning("Please enter either HS Code or Description to search.")
        except Exception as e:
            st.error(f"Search error: {str(e)}")