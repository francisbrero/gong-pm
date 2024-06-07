from utils.utils import test_connection, get_recent_calls, get_call_transcript, get_speaker_details, get_speaker_name, write_to_file

# Test the connection
print("Testing connection to Gong API...")
connection_result = test_connection()
print(connection_result)

# Get recent calls
print("Fetching recent calls...")
recent_calls = get_recent_calls()
print(recent_calls)

# If there are any calls, fetch the transcript and speaker details for the first call
if recent_calls:
    first_call_id = recent_calls[0]['id']
    
    print(f"Fetching transcript for call ID: {first_call_id}...")
    transcript = get_call_transcript(first_call_id)
    print(transcript)
    
    print(f"Fetching speaker details for call ID: {first_call_id}...")
    speakers = get_speaker_details(first_call_id)
    print(speakers)

    # Assuming the first speaker in the list
    if speakers:
        first_speaker_id = speakers[0]['speakerId']
        speaker_name = get_speaker_name(first_speaker_id, speakers)
        print(f"Speaker Name: {speaker_name}")