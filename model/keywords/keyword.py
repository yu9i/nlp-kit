# -*- coding: utf-8 -*-

from .WRkeyword import keywords_with_wr
from .nlpKeyword import keywords_with_bert

def del_dup(words):
    ret = []
    for i, word in enumerate(words):
        contained = False
        for j, word2 in enumerate(words):
            if i != j:
                if word in word2:
                    if len(word) <= len(word2):
                        if word not in ret:
                            ret.append(word)
                    contained = True
                    break
                elif word2 in word:
                    if len(word2) < len(word):
                        if word2 not in ret:
                            ret.append(word2)
                    contained = True
                    break
        if not contained and word not in ret:
            ret.append(word)
    return ret

def add_keyword(ret, wr):
    for word in wr:
        if not any(existing in word for existing in ret):
            ret.append(word)
    return del_dup(ret)

def keywords(text):

    bert_keywords = keywords_with_bert(text)
    bert_keywords = [kw[0] for kw in bert_keywords]

    wr_keyword = keywords_with_wr(text)
    wr_keyword = list(wr_keyword.keys())

    ret = del_dup(bert_keywords)
    ret = add_keyword(ret, wr_keyword)
    
    return ret
