from keybert import KeyBERT
from transcript_utils import get_transcript_text

def extract_video_topics(url: str, num_topics: int = 5) -> list[str]:
    # Get the transcript
    transcript = get_transcript_text(url)
    # print("Transcipt:",transcript)
    # Initialize KeyBERT model
    model = KeyBERT(model='all-MiniLM-L6-v2')  # lightweight model

    # Extract keywords as topics
    keywords = model.extract_keywords(transcript, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=num_topics)
    
    # Just return the keywords as list of strings
    return [kw for kw, score in keywords]
