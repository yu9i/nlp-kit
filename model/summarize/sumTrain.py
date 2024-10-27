from datasets import load_dataset
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration, Trainer, TrainingArguments
import json
import os
import glob

train_path = "../TrainingData.json"
validation_path = "../ValidationData.json"

model_name = "gogamza/kobart-summarization"
tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

def FindFile(dir): # 파일 찾기

    if os.path.isfile(dir): #전처리 파일 있을 때
        return True
    else: #전처리 파일 없을 때
        data_path = ""
        if dir == "../TrainingData.json":
            data_path = '../data1/Training/*.json'
        elif dir == "../ValidationData.json":
            data_path = '../data1/Validation/*.json'
        json_files = glob.glob(data_path)
        combined_data = []
        ret = {}

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    newData = {
                        "type": data["Meta(Acqusition)"]["doc_type"],
                        "original": data["Meta(Refine)"]["passage"],
                        "summary": data["Annotation"]["summary2"]
                    }
                    combined_data.append(newData)
            except IOError:
                print("파일을 읽는 중 오류 발생")
                return False
        try:
            ret["data"] = combined_data
            with open(dir, 'w', encoding='utf-8') as file:
                json.dump(ret, file, indent=4, ensure_ascii=False)
            print("파일 쓰기 완료")
            return True
        except IOError:
            print("파일 쓰는 중 오류 발생")
            return False

    return True

if(FindFile(train_path) and FindFile(validation_path)):
    datasets = load_dataset("json", data_files={"train": train_path, "validation": validation_path}, field="data")

def Preprocess(text):
    inputs = tokenizer(text["original"], max_length=1024, truncation=True, padding="max_length")
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(text["summary"], max_length=128, truncation=True, padding="max_length")
    inputs["labels"] = labels["input_ids"]
    return inputs

tokenized_datasets = datasets.map(Preprocess, batched=True)

training_args = TrainingArguments( # epoch 수 변경
    output_dir="./results",
    evaluation_strategy="steps",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=80,
    weight_decay=0.01,
    save_steps=10_000,
    save_total_limit=2,
    logging_dir='./logs',
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
)

trainer.train()

model.save_pretrained("./fine_tuned_kobart")
tokenizer.save_pretrained("./fine_tuned_kobart")