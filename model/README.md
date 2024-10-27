# backend file and text analyze model
--------

## backend file
* app.py
--------

## text analyze model
### 텍스트 요약: summarize/*
- train.py: fine-tuning, 학습 파일
- main.py: 학습한 모델을 토대로 요약하는 파일

### 키워드 추출: keywords/*
- keyword.py: KRWordRank를 사용한 모델
- nlpKeyword.py: koBERT, KeyBERT를 사용한 모델

### 카테고리 분류: category/*
- Kmeans.py: 군집을 이용한 비지도 학습 Kmeans 카테고리 분류 모델
- categoryTrain.py: BERT를 이용한 카테고리 학습 파일
- categoryMain.py: 학습한 모델을 토대로 카테고리 분류하는 파일

##### performance.py: 성능 평가 파일