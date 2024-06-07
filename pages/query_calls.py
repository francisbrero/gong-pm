import streamlit as st
from utils.chroma_db import query_chromadb, init_chromadb, get_collection
import os

# Constants
CHROMA_PATH = './data/chroma'
COLLECTION_NAME = 'call_transcripts'
GONG_BASE_URL = os.getenv("GONG_BASE_URL")
# Replace API by APP in the Gong URL
GONG_BASE_APP_URL = GONG_BASE_URL.replace("api", "app")

# Initialize ChromaDB client and collection
client = init_chromadb(chroma_root_path=CHROMA_PATH)
collection = get_collection(client, collection_name=COLLECTION_NAME)

st.header("Gong Calls Query")

query_text = st.text_input("Enter your query:")
if query_text:
    results = query_chromadb(query_text, chroma_root_path=CHROMA_PATH, collection_name=COLLECTION_NAME)
    st.write("Query Results:")
    
    for i, metadata in enumerate(results['metadatas'][0]):
        call_id = metadata['call_id']
        start = metadata['start']
        # change start from milliseconds to seconds
        start = start // 1000
        speaker_name = metadata['speaker_name']
        sentence = results['documents'][0][i]
        call_link = f"{GONG_BASE_APP_URL}/call?id={call_id}&play={start}"
        
        st.write(f"**Speaker:** {speaker_name}")
        st.write(f"**Sentence:** {sentence}")
        st.write(f"[Listen to Call]({call_link})")
        st.write("---")

st.sidebar.write("""
This project allows you to search through Gong call transcripts. The transcripts are embedded and stored in a ChromaDB collection. You can query the database to find relevant segments from the calls.

To use the app, enter a search query in the text input below and view the results, which include a link to the relevant part of the call.
""")