import json
import torch
from torch.utils.data import Dataset
from transformers import AutoTokenizer, BertTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

train_path = "../TrainingData.json"
validation_path = "../ValidationData.json"


model_name = "monologg/kobert"
tokenizer = BertTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=10, trust_remote_code=True)


label_mapping = {
    "news_r": 0,
    "briefing": 1,
    "his_cul": 2,
    "paper": 3,
    "minute": 4,
    "edit": 5,
    "public": 6,
    "speech": 7,
    "literature": 8,
    "narration": 9
}
torch.save(label_mapping, './label_encoder.pth')

class CategoryDataset(Dataset):
    def __init__(self, data, tokenizer, max_length, label_mapping):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.label_mapping = label_mapping

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = str(self.data[idx]['original'])
        label = self.label_mapping[self.data[idx]['type']]

        inputs = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors="pt"
        )
        return {
            'input_ids': inputs['input_ids'].flatten(),
            'attention_mask': inputs['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

def load_data(file_path, tokenizer, max_length, label_mapping):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)["data"]
    return CategoryDataset(data, tokenizer, max_length, label_mapping)


train_dataset = load_data(train_path, tokenizer, 512, label_mapping)
val_dataset = load_data(validation_path, tokenizer, 512, label_mapping)


training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="steps",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    save_steps=10_000,
    save_total_limit=2,
    logging_dir='./logs',
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

trainer.train()

save_directory = "./category_classification_kobert"
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)
# tokenizer.save_vocabulary(save_directory)
