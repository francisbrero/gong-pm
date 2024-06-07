import argparse
from utils.chroma_db import query_chromadb

def main():
    parser = argparse.ArgumentParser(description='Query the ChromaDB collection.')
    parser.add_argument('--query', type=str, required=True, help='The query text to search in the ChromaDB collection')
    parser.add_argument('--chroma_path', type=str, default='./data/test_chroma', help='The path to the ChromaDB')
    parser.add_argument('--collection_name', type=str, default='test_call_transcripts', help='The name of the ChromaDB collection to query')
    
    args = parser.parse_args()

    print("Querying the ChromaDB collection...")
    results = query_chromadb(args.query, chroma_root_path=args.chroma_path, collection_name=args.collection_name)
    print("Query Results:", results)

    documents = results["documents"][0]
    for doc in documents:
        print("Query results: ", doc)

if __name__ == "__main__":
    main()
