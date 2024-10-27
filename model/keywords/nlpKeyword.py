import json
import re
from keybert import KeyBERT
from transformers import BertModel, BertTokenizer

validation_path = "../ValidationData.json"

model_name = "monologg/kobert"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

def OpenFile(dir):
    with open(dir, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data = data["data"]
    return data

def Preprocess(texts):
    texts_list = texts.split('.')
    text_list = []
    for text in texts_list:
        text = re.sub(r'\b\d+\S*\s*', '', text)
        text = re.sub(r'[a-zA-Z]', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        text = text.strip()

        if text:
            text_list.append(text)
    return ' '.join(text_list)

def keywords_with_bert(text):
    # val_data = OpenFile(validation_path)
    # data = val_data[0]
    # original_text = data["original"]
    # processed_text = Preprocess(original_text)

    kw_model = KeyBERT(model)
    data = text
    processed_text = Preprocess(data)

    keywords = kw_model.extract_keywords(processed_text, keyphrase_ngram_range=(1, 1), stop_words=None, top_n=5)
    
    return keywords
