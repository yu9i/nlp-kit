from rouge_score import rouge_scorer
import matplotlib.pyplot as plt
import json

def calculate_rouge(predictions, references):
    """
    ROUGE-1, ROUGE-2, ROUGE-L 점수를 계산하는 함수
    """
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    rouge1_scores = []
    rouge2_scores = []
    rougeL_scores = []

    for pred, ref in zip(predictions, references):
        scores = scorer.score(ref, pred)
        rouge1_scores.append(scores['rouge1'].fmeasure)
        rouge2_scores.append(scores['rouge2'].fmeasure)
        rougeL_scores.append(scores['rougeL'].fmeasure)
    
    return {
        'rouge1': sum(rouge1_scores) / len(rouge1_scores),
        'rouge2': sum(rouge2_scores) / len(rouge2_scores),
        'rougeL': sum(rougeL_scores) / len(rougeL_scores)
    }

def plot_rouge_scores(rouge_scores):
    """
    ROUGE 점수를 그래프로 시각화하는 함수
    """
    labels = list(rouge_scores.keys())
    scores = list(rouge_scores.values())
    
    plt.figure(figsize=(8, 5))
    plt.bar(labels, scores, color=['blue', 'orange', 'green'])
    plt.xlabel('ROUGE Score Type')
    plt.ylabel('Score')
    plt.ylim(0, 1)  # ROUGE 점수는 0과 1 사이
    plt.title('ROUGE Scores for Summarization Model')
    plt.show()

dir = "./BARTsummary.json"
try:
    with open(dir, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data = data["BART_epoch80"]
except IOError:
    print("파일을 읽는 중 오류 발생")

predicted_summaries = []
actual_summaries = []

for d in data:
    predicted_summaries.append(d["summary"])
    actual_summaries.append(d["BARTsummary"])

# ROUGE 점수 계산
rouge_results = calculate_rouge(predicted_summaries, actual_summaries)
print("ROUGE Scores:", rouge_results)

# ROUGE 점수 시각화
plot_rouge_scores(rouge_results)
