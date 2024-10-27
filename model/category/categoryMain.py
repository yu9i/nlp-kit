# -*- coding: utf-8 -*-

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json

# validation_path = "./ValidationData.json"

label = {
    "news_r": "뉴스",
    "briefing": "보도자료",
    "his_cul": "역사",
    "paper": "보고서",
    "minute": "회의록",
    "edit": "사설",
    "public": "간행물",
    "speech": "연설문",
    "literature": "문화",
    "narration": "나레이션"
}

def load_label_encoder(path):
    return torch.load(path)

def OpenFile(dir):
    with open(dir, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data = data["data"]
    return data

def predict_category(text, model, tokenizer, label_encoder):
    inputs = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=128,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )

    with torch.no_grad():
        outputs = model(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask']
        )
        probs = outputs.logits.softmax(dim=1)
        pred = torch.argmax(probs, dim=1).item()
    return list(label_encoder.keys())[list(label_encoder.values()).index(pred)]

def category(text):
    model_name = "./category/category_classification_kobert"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    label_encoder = load_label_encoder('./category/label_encoder.pth')

    predicted_category = predict_category(text, model, tokenizer, label_encoder)
    return label[predicted_category]