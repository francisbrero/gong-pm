# gong-pm

Allow PMs to ask questions to your Gong library of calls

Gong is absolutely AWESOME and as a Product leader, I spend a lot of time in Gong listening to calls.  Gong is designed for sales teams and is therefore very sales-centric. I wanted to be able to ask questions about our product, our customers' needs across all accounts. This isn't natively possible in Gong. This is a simple tool that allows you to do that.

## instructions for local use

Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

install the dependencies

```bash
pip install -r requirements.txt
```

Create your .env file

```bash
touch .env
```

Add the following variables to your .env file

```bash
GONG_API_KEY=your_gong_api_key
GONG_BASE_URL=your_gong_base_url
GONG_SECRET=your_gong_secret
```

Set the PYTHONPATH

```bash
export PYTHONPATH=$(pwd)
```

### Load the calls into the database

```bash
python -m utils.load_calls
```

### run tests

1. Check you can connect to Gong

```bash
python -m test.test_gong_api
```

2. Get a transcript and test embedding it into a test chroma db

```bash
python -m test.test_transcripts
```

3. Test running a query against the chroma db

```bash
python -m test.test_query --query "What did the customer say about our pricing?"
```
4. Test against production data

```bash
python -m test.test_query --query "what did the customer say about pricing?" --chroma_path "./data/chroma" --collection_name "call_transcripts"
```

## Architecture

The system is designed as follows:

- Streamlit app to allow PMs to ask questions
- ChromaDB vector database to store all the call recordings and their embeddings
- Semantic search engine to find the most relevant calls using the embeddings. For now, we are using sentence-transformers

Stack:

- Streamlit
- ChromaDB
