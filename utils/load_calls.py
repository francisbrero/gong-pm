import os
from datetime import datetime, timedelta
from tqdm import tqdm
import logging
from utils.utils import get_recent_calls, save_transcript_to_file
from utils.chroma_db import init_chromadb, reset_collection, embed_and_store_transcripts, get_collection

# Constants
TRANSCRIPTS_PATH = 'data/transcripts'
CHROMA_PATH = './data/chroma'
COLLECTION_NAME = 'call_transcripts'
DAYS_TO_LOAD = 30
CHUNK_SIZE = 3

# Set up logging
logging.basicConfig(level=logging.INFO)

def read_loaded_call_ids(collection):
    """
    Reads the loaded call IDs from the ChromaDB collection.
    """
    try:
        results = collection.query(query_embeddings=[], n_results=0, include=['metadatas'])
        loaded_call_ids = {metadata['call_id'] for result in results['results'] for metadata in result['metadatas']}
    except Exception as e:
        logging.error(f"Error reading loaded call IDs: {e}")
        loaded_call_ids = set()
    
    return loaded_call_ids

def load_calls_for_last_n_days_with_progress(n_days=30, chunk_size=3):
    total_chunks = n_days // chunk_size
    progress_bar = tqdm(total=total_chunks, desc="Loading calls", unit="chunk")
    
    # Initialize ChromaDB client and reset collection
    client = init_chromadb(chroma_root_path=CHROMA_PATH)
    reset_collection(client, COLLECTION_NAME)
    collection = get_collection(client, COLLECTION_NAME)
    
    # Read already loaded call IDs
    loaded_call_ids = read_loaded_call_ids(collection)

    for i in range(total_chunks):
        from_days_ago = (i + 1) * chunk_size
        until_days_ago = i * chunk_size
        calls = get_recent_calls(from_X_days_ago=from_days_ago, until_X_days_ago=until_days_ago)
        
        new_call_ids = []
        for call in calls:
            call_id = call['id']
            if call_id not in loaded_call_ids:
                save_transcript_to_file(call_id)
                new_call_ids.append(call_id)

        # Embed only new calls
        if new_call_ids:
            embed_and_store_transcripts(transcripts_path=TRANSCRIPTS_PATH, embeddings_path='data/embeddings')
        
        progress_bar.update(1)
    
    progress_bar.close()
    print("Loading complete!")

if __name__ == "__main__":
    load_calls_for_last_n_days_with_progress(n_days=DAYS_TO_LOAD, chunk_size=CHUNK_SIZE)
