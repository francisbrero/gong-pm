import requests
import os
import json
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the environment variables
gong_base_url = os.getenv("GONG_BASE_URL")
gong_api_key = os.getenv("GONG_API_KEY")
gong_secret = os.getenv("GONG_SECRET")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Directories
TRANSCRIPTS_PATH = 'data/transcripts'

def test_connection():
    url = gong_base_url + "/v2/users"
    try:
        r = requests.get(url, auth=(gong_api_key, gong_secret))
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to Gong API: {e}")
        return None

def get_recent_calls(from_X_days_ago: int = 3, until_X_days_ago: int = 0):
    url = gong_base_url + "/v2/calls"
    
    start_date = datetime.now() - timedelta(days=from_X_days_ago)
    end_date = datetime.now() - timedelta(days=until_X_days_ago)
    from_date = start_date.strftime("%Y-%m-%dT%H:%M:%S")
    to_date = end_date.strftime("%Y-%m-%dT%H:%M:%S")

    query_string = f"?fromDateTime={from_date}Z&toDateTime={to_date}Z"

    try:
        r = requests.get(url + query_string, auth=(gong_api_key, gong_secret))
        r.raise_for_status()
        calls = r.json().get('calls', [])
        return calls
    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting recent calls: {e}")
        return []

def get_call_transcript(call_id):
    url = gong_base_url + f"/v2/calls/transcript"
    body = {
        "filter": {
            "callIds": [call_id]
        }
    }
    try:
        r = requests.post(url, json=body, auth=(gong_api_key, gong_secret))
        r.raise_for_status()
        call = r.json().get('callTranscripts', [])
        return call
    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting call transcript for {call_id}: {e}")
        return None

def get_speaker_details(call_id):
    url = gong_base_url + f"/v2/calls/extensive"
    body = {
        "filter": {
            "callIds": [call_id]
        },
        "contentSelector": {
            "exposedFields": {
                "parties": True
            }
        }
    }
    try:
        r = requests.post(url, json=body, auth=(gong_api_key, gong_secret))
        r.raise_for_status()
        speakers = r.json().get('calls', [])[0].get('parties', [])
        return speakers
    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting speaker details for {call_id}: {e}")
        return []

def get_speaker_name(speaker_id, speakers):
    for speaker in speakers:
        if speaker['speakerId'] == speaker_id:
            return speaker['name']
    return "Unknown Speaker"

def write_to_file(file_name, content):
    with open(f"data/{file_name}.txt", "w") as f:
        f.write(content)

def save_transcript_to_file(call_id):
    # Check if there is already a transcript saved for this call
    if os.path.exists(os.path.join(TRANSCRIPTS_PATH, f"{call_id}.json")):
        logging.info(f"Transcript for call {call_id} already exists.")
        return

    transcript_data = get_call_transcript(call_id)
    speakers = get_speaker_details(call_id)
    if transcript_data:
        transcripts = transcript_data
        transcript_json_lines = []

        for transcript in transcripts:
            for segment in transcript.get('transcript', []):
                speaker = segment['speakerId']
                speaker_name = get_speaker_name(speaker, speakers)
                for sentence in segment.get('sentences', []):
                    line_data = {
                        'start': sentence['start'],
                        'speaker_name': speaker_name,
                        'sentence': sentence['text']
                    }
                    transcript_json_lines.append(line_data)

        file_name = os.path.join(TRANSCRIPTS_PATH, f"{call_id}.json")
        with open(file_name, 'w') as f:
            for line in transcript_json_lines:
                json.dump(line, f)
                f.write('\n')
        logging.info(f"Transcript saved to {file_name}")
    else:
        logging.error(f"Failed to save transcript for call {call_id}")

def test_save_recent_transcripts():
    calls = get_recent_calls()
    # for the purpose of testing we will only keep the first call
    calls = calls[:1]
    os.makedirs(TRANSCRIPTS_PATH, exist_ok=True)
    for call in calls:
        call_id = call['id']
        save_transcript_to_file(call_id)
    logging.info("Recent transcripts saved successfully.")


def load_calls_for_last_n_days(n_days=30, chunk_size=3):
    total_chunks = n_days // chunk_size
    for i in range(total_chunks):
        from_days_ago = (i + 1) * chunk_size
        until_days_ago = i * chunk_size
        calls = get_recent_calls(from_X_days_ago=from_days_ago, until_X_days_ago=until_days_ago)
        for call in calls:
            save_transcript_to_file(call['id'])
