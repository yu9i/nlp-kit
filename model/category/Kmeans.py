import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def OpenFile(dir):
    with open(dir, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data = data["data"]
    return data

def Preprocess(text):
    text = re.sub(r'\b\d+\S*\s*', '', text)
    text = re.sub(r'[a-zA-Z]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip()
    return text

data_path = "./ValidationData.json"

data = OpenFile(data_path)

texts = [Preprocess(item['original']) for item in data]

vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(texts)

num_clusters = 3
kmeans = KMeans(n_clusters=num_clusters, random_state=0)
kmeans.fit(X)

for i, label in enumerate(kmeans.labels_):
    print(f"Document {i+1}: Cluster {label}")

order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names_out()

for i in range(num_clusters):
    print(f"Cluster {i} keywords:", end='')
    for ind in order_centroids[i, :10]:
        print(f' {terms[ind]}', end=',')
    print()
