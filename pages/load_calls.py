import streamlit as st
from utils.utils import get_recent_calls, save_transcript_to_file
from utils.load_calls import read_loaded_call_ids
from utils.chroma_db import embed_and_store_transcripts, reset_collection, init_chromadb, get_collection
from datetime import datetime, timedelta
import os

# Constants
TRANSCRIPTS_PATH = 'data/transcripts'
CHROMA_PATH = './data/chroma'
COLLECTION_NAME = 'call_transcripts'
CHUNK_SIZE = 3

# Initialize ChromaDB client and collection
client = init_chromadb(chroma_root_path=CHROMA_PATH)
reset_collection(client, COLLECTION_NAME)
collection = get_collection(client, COLLECTION_NAME)

st.header("Load Gong Calls into ChromaDB")

# User input for number of days of calls to load
days_to_load = st.number_input("Enter the number of days of calls to load:", min_value=1, max_value=90, value=30)

if st.button("Load Calls"):
    with st.spinner("Loading calls..."):
        total_chunks = days_to_load // CHUNK_SIZE
        progress_bar = st.progress(0)
        
        # Read already loaded call IDs
        loaded_call_ids = read_loaded_call_ids(collection)

        for i in range(total_chunks):
            from_days_ago = (i + 1) * CHUNK_SIZE
            until_days_ago = i * CHUNK_SIZE
            calls = get_recent_calls(from_X_days_ago=from_days_ago, until_X_days_ago=until_days_ago)

            new_call_ids = []
            for call in calls:
                call_id = call['id']
                if call_id not in loaded_call_ids:
                    save_transcript_to_file(call_id)
                    new_call_ids.append(call_id)

            if new_call_ids:
                embed_and_store_transcripts(transcripts_path=TRANSCRIPTS_PATH, embeddings_path='data/embeddings')

            progress_bar.progress((i + 1) / total_chunks)
        
        st.success("Loading complete!")

st.sidebar.write("""
Pick a number of days to go back and load into our ChromaDB collection. The app will download the call transcripts from Gong and store them in the collection. 
We should be doing this incrementally so calls that have already been processed won't be re-processed.
""")
