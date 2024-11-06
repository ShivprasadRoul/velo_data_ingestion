from langchain_cohere import CohereEmbeddings
embeddings_model = CohereEmbeddings(cohere_api_key="UvPEoXK1I9aWKwre0lYhqbySqSFhm1SKYL51fuwm", model='embed-english-v3.0')


def generate_embeddings(text):
    outputs = embeddings_model.embed_query(text)
    return outputs
