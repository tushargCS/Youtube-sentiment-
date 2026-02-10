# test_transcript.py

from transcript_utils import get_transcript_text

url = input("Paste YouTube URL: ").strip()
transcript = get_transcript_text(url)
print("Transcript (first 500 characters):")
print(transcript[:50])
