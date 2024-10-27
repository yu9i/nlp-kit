import json
import re
from krwordrank.word import KRWordRank

validation_path = "../ValidationData.json"

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
    return text_list

def keywords_with_wr(text):
    # val_data = OpenFile(validation_path)

    min_count = 4
    max_length = 8
    wordrank_extractor = KRWordRank(min_count=min_count, max_length=max_length)
    beta = 0.85
    max_iter = 10

    # data = val_dat0a[0]
    # texts = Preprocess(data["original"])
    texts = Preprocess(text)
    keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter)
    ret = {}

    for word, score in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:10]:
        ret[word] = score
    
    return ret