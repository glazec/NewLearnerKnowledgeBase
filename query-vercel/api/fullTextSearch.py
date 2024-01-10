import numpy as np
import jieba
import chinese_converter
from os.path import join


def single_word_search(texts, query):
    index = np.char.count(texts, query)
    filtered_arr = texts[index != 0]
    if len(filtered_arr) < 5:
        return filtered_arr
    sorted_indices = np.argsort(index)
    # take the top 5 results
    # top_five_counts = index[sorted_indices[-5:]]
    top_five_texts = texts[sorted_indices[-5:]]

    return top_five_texts


def full_text_search(query):
    with open(join("data", "texts.txt"), "r") as file:
        data = file.read()
    texts = np.array([text.strip() for text in data.split("===")])
    query = query.lower()
    query = chinese_converter.to_simplified(query)
    tokens = jieba.cut(query)
    stopwords = [
        line.strip()
        for line in open(
            join("data", "stop_words.txt"), "r", encoding="utf-8"
        ).readlines()
    ]
    filtered_words = [word for word in tokens if word not in stopwords]
    response = np.array([])
    for word in filtered_words:
        response = np.concatenate((response, single_word_search(texts, word)), axis=0)
    response = np.unique(response)
    print(len(response))
    return response


if __name__ == "__main__":
    print(full_text_search("我们Macos的快捷键是什么"))
