import chromadb
from chromadb.config import Settings
import logging
import os
import json
from utils.embedding_model import generate_embeddings

# Initialize ChromaDB client
def init_chromadb(chroma_root_path="./data/chroma"):
    chroma_client = chromadb.PersistentClient(path=chroma_root_path)
    return chroma_client

# Create or get collection
def get_collection(client, collection_name="call_transcripts"):
    return client.get_or_create_collection(name=collection_name)

# Add document to collection
def add_document(collection, document_id, text, metadata, embedding):
    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[document_id],
        embeddings=[embedding]
    )
    logging.info(f"Document {document_id} added to ChromaDB")

# Reset (delete and recreate) collection
def reset_collection(client, collection_name):
    try:
        client.delete_collection(name=collection_name)
        logging.info(f"Collection {collection_name} deleted.")
    except Exception as e:
        logging.error(f"Error deleting collection {collection_name}: {e}")

    client.create_collection(name=collection_name)
    logging.info(f"Collection {collection_name} recreated.")

# Function to chunk the transcript (adjusted for JSON)
def chunk_transcript(transcript, chunk_size=5):
    chunks = []
    current_chunk = []
    current_chunk_size = 0

    for sentence in transcript:
        current_chunk.append(sentence)
        current_chunk_size += 1

        if current_chunk_size >= chunk_size:
            chunks.append(current_chunk)
            current_chunk = []
            current_chunk_size = 0

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

# Function to embed and store transcripts in ChromaDB
def embed_and_store_transcripts(transcripts_path='data/transcripts', embeddings_path='data/embeddings'):
    os.makedirs(embeddings_path, exist_ok=True)
    client = init_chromadb()
    collection = get_collection(client)

    for filename in os.listdir(transcripts_path):
        if filename.endswith(".json"):
            file_path = os.path.join(transcripts_path, filename)
            with open(file_path, 'r') as f:
                for line in f:
                    record = json.loads(line)
                    sentence = record['sentence']
                    metadata = {
                        "call_id": filename.split('.')[0],
                        "start": record['start'],
                        "speaker_name": record['speaker_name']
                    }
                    embedding = generate_embeddings(sentence)
                    document_id = f"{metadata['call_id']}_{metadata['start']}"
                    add_document(collection, document_id, sentence, metadata, embedding)

            logging.info(f"Transcripts for {filename} embedded and stored in ChromaDB")

# Function to embed the first transcript and store in a test ChromaDB
def embed_first_transcript(transcripts_path='data/transcripts', test_chroma_path="./data/test_chroma"):
    client = init_chromadb(chroma_root_path=test_chroma_path)
    collection = get_collection(client, collection_name="test_call_transcripts")

    # Since we are using this for testing primarily, we will reset the collection
    reset_collection(client, collection)
    
    files = [f for f in os.listdir(transcripts_path) if f.endswith(".json")]
    
    if not files:
        logging.error(f"No transcript files found in {transcripts_path}")
        return
    
    filename = files[0]
    file_path = os.path.join(transcripts_path, filename)
    
    with open(file_path, 'r') as f:
        transcript = [json.loads(line) for line in f]

    chunks = chunk_transcript(transcript)
    for chunk in chunks:
        for record in chunk:
            sentence = record['sentence']
            metadata = {
                "call_id": filename.split('.')[0],
                "start": record['start'],
                "speaker_name": record['speaker_name']
            }
            embedding = generate_embeddings(sentence)
            document_id = f"{metadata['call_id']}_{metadata['start']}"
            add_document(collection, document_id, sentence, metadata, embedding)

    logging.info(f"Transcript for {filename} chunked, embedded, and stored in test ChromaDB")

# Function to query the ChromaDB collection
def query_chromadb(query_text, chroma_root_path="./data/chroma", collection_name="call_transcripts"):
    client = init_chromadb(chroma_root_path=chroma_root_path)
    collection = get_collection(client, collection_name=collection_name)
    
    query_embedding = generate_embeddings(query_text)
    results = collection.query(query_embeddings=[query_embedding], n_results=5)
    
    return results
