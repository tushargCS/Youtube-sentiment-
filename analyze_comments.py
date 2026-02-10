# analyze_comments.py

from youtube_comment_downloader import YoutubeCommentDownloader
import requests

def get_comments(video_url, max_comments=50):
    downloader = YoutubeCommentDownloader()
    comments = []
    try:
        for comment in downloader.get_comments_from_url(video_url, sort_by=1):
            if len(comments) >= max_comments:
                break
            comments.append(comment["text"])
    except Exception as e:
        print(f"Error downloading comments: {e}")
    return comments

def get_sentiment(comment):
    try:
        res = requests.post("http://127.0.0.1:9000/predict", json={"text": comment})
        if res.status_code == 200:
            return res.json()
        else:
            return {"label": "error", "score": 0.0}
    except Exception as e:
        return {"label": "error", "score": 0.0}

def analyze_video(video_url):
    comments = get_comments(video_url)
    print(f"Fetched {len(comments)} comments from YouTube\n")
    for i, comment in enumerate(comments):
        result = get_sentiment(comment)
        print(f"{i+1}. Comment: {comment}")
        print(f"   ➤ Sentiment: {result['label']} | Score: {result['score']}\n")

if __name__ == "__main__":
    url = input("Paste YouTube Video URL: ")
    analyze_video(url)
