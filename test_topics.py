from topic_extractor import extract_video_topics

url = input("Paste YouTube URL: ").strip()
topics = extract_video_topics(url)
print("Extracted Topics:")
for i, topic in enumerate(topics, start=1):
    print(f"{i}. {topic}")
