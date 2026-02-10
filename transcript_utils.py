import re
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from deep_translator import LibreTranslator


def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def split_text_by_sentences(text, max_chars=5000):
    sentences = re.split(r'(?<=[।.?!])\s+', text)
    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) < max_chars:
            current += sentence + " "
        else:
            chunks.append(current.strip())
            current = sentence + " "
    if current:
        chunks.append(current.strip())
    return chunks

def translate_to_english(text: str) -> str:

    print("[INFO] Hindi transcript detected, translating to English...")

    try:
        max_chars = 5000
        translated_chunks = []

        # Split text into smaller chunks (≤ 5000 characters)
        chunks = split_text_by_sentences(text)
        for chunk in chunks:
            translated_chunk = LibreTranslator(
                source='hi',
                target='en',
                api_url='https://libretranslate.de/translate'
            ).translate(chunk)

            translated_chunks.append(translated_chunk)


        return " ".join(translated_chunks)

    except Exception as e:
        print(f"[Translation Failed]: {e}")
        return text  # fallback


def get_transcript_text(video_url: str, languages=['en', 'hi']) -> str:
    video_id = extract_video_id(video_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    for lang in languages:
        try:
            fetched = YouTubeTranscriptApi().fetch(video_id, languages=[lang])
            transcript = " ".join([snippet.text for snippet in fetched])

            # If it's a Hindi transcript, translate to English
            if lang == 'hi':
                transcript = translate_to_english(transcript)

            return transcript

        except NoTranscriptFound:
            continue

    raise RuntimeError(f"No transcript found for requested languages {languages}")
