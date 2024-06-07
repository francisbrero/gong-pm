from utils.utils import test_save_recent_transcripts
from utils.chroma_db import embed_first_transcript

def main():
    # Test saving recent transcripts
    print("Testing saving recent transcripts...")
    test_save_recent_transcripts()

    # Test embedding the first transcript into a test ChromaDB
    print("Testing embedding the first transcript into a test ChromaDB...")
    embed_first_transcript()

if __name__ == "__main__":
    main()