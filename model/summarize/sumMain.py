# -*- coding: utf-8 -*-

import os
import glob
import json
import torch
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

# tokenizer = PreTrainedTokenizerFast.from_pretrained("./fine_tuned_kobart")
# model = BartForConditionalGeneration.from_pretrained("./fine_tuned_kobart")

tokenizer = PreTrainedTokenizerFast.from_pretrained("./summarize/fine_tuned_kobart")
model = BartForConditionalGeneration.from_pretrained("./summarize/fine_tuned_kobart")


def summarize(text, max_length=200, min_length=30):
    inputs = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)     
    summary_ids = model.generate(inputs, max_length=max_length, min_length=min_length, length_penalty=1.0, num_beams=3, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


def BARTsummary(text):
    summary = summarize(text)
    return summary
