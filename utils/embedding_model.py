from sentence_transformers import SentenceTransformer

# Load the Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(text):
    # Generate embeddings
    embeddings = model.encode(text)
    return embeddings.tolist()