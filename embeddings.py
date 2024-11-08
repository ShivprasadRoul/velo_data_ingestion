from langchain_cohere import CohereEmbeddings
import numpy as np
from typing import Optional
import streamlit as st

# Initialize the embedding model
embeddings_model = CohereEmbeddings(
    cohere_api_key="UvPEoXK1I9aWKwre0lYhqbySqSFhm1SKYL51fuwm", 
    model='embed-english-v3.0'
)

# Constants
EMBEDDING_DIM = 1024

def generate_embeddings(text: str) -> Optional[np.ndarray]:
    """
    Generate embeddings for the given text using Cohere's API.
    """
    try:
        outputs = embeddings_model.embed_query(text)
        embedding = np.array(outputs, dtype=np.float64)  # Ensure float64 type
        return embedding
    except Exception as e:
        print(f"Error in generate_embeddings: {str(e)}")
        return None

def validate_embedding(embedding: np.ndarray) -> bool:
    """
    Validate the embedding dimensions and type.
    """
    if embedding is None:
        return False
    if not isinstance(embedding, np.ndarray):
        return False
    if embedding.size != 1024:
        return False
    return True

def process_embedding(text: str) -> Optional[np.ndarray]:
    """Process and validate the embedding"""
    try:
        embedding = generate_embeddings(text)
        if embedding is None:
            st.error("Failed to generate embedding")
            return None
            
        if not validate_embedding(embedding):
            st.error(f"Invalid embedding dimension. Expected {1024}")
            return None
            
        st.info(f"Generated embedding with dimension: {len(embedding)}")    
        return embedding
    except Exception as e:
        st.error(f"Error processing embedding: {str(e)}")
        return None
