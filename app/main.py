from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

app = FastAPI()

# Load CardiffNLP model for social media sentiment
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
label_map = ['negative', 'neutral', 'positive']

class TextIn(BaseModel):
    text: str

@app.post("/predict")
def predict_sentiment(data: TextIn):
    try:
        encoded_input = tokenizer(data.text, return_tensors='pt', truncation=True)
        with torch.no_grad():
            output = model(**encoded_input)
            scores = F.softmax(output.logits, dim=1)
            predicted = torch.argmax(scores, dim=1).item()
            return {
                "label": label_map[predicted],
                "score": round(float(scores[0][predicted]), 3)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
