# -*- coding: utf-8 -*-
 
from keywords.keyword import keywords
from category.categoryMain import category
from summarize.sumMain import BARTsummary

def analyze_text(text):
    summary = BARTsummary(text)
    res_keywords= keywords(text)
    res_category = category(text)

    return {
        "summary": summary,
        "keywords": res_keywords,
        "category": res_category
    }
