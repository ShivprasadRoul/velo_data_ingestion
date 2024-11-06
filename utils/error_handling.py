import logging
import streamlit as st

def handle_error(e):
    logging.error(e)
    st.error("An error occurred: {}".format(e))
