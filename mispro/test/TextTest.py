# -*- coding"utf-8 -*-
# @Auther : zhangxiaoer
# @Time : 2023-04-11 21:25 
# @File : kmeansTest.py

# https://scikit-learn.org/stable/install.html
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MiniBatchKMeans

# 严格限制标点符号
strict_punctuation = '。，、＇：∶；?‘’“”〝〞ˆˇ﹕︰﹔﹖﹑·¨….¸;！´？！～—ˉ｜‖＂〃｀@﹫¡¿﹏﹋﹌︴々﹟#﹩$﹠&﹪%*﹡﹢﹦﹤‐￣¯―﹨ˆ˜﹍﹎+=＿_-\ˇ~﹉﹊（）〈〉‹›﹛﹜『』〖〗［］《》〔〕{}「」【】︵︷︿︹︽_﹁﹃︻︶︸﹀︺︾ˉ﹂﹄︼'
# 简单限制标点符号
simple_punctuation = '’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
# 去除标点符号
punctuation = simple_punctuation + strict_punctuation

"""
tokenizer

"""


def tokenizer(content):
    """
    :desc : Replace symbols in text
    :param content:origin text
    :return:
    """
    text_symbol_flag = []
    line_feed_flag = ['\t', '\n', '\r']
    filters = [f"{symbol_flag}" for symbol_flag in punctuation]
    text_symbol_flag.extend(line_feed_flag)
    text_symbol_flag.extend(filters)
    text_symbol_flag = list(set(text_symbol_flag))
    content = re.sub("|".join(text_symbol_flag), " ", content)
    tokens = [i.strip().lower() for i in content.split()]

    return tokens


def loadDataset():
    '''导入文本数据集'''
    corpus_folder = r"E:\webpro\text_analysis\data_source\kmeansCorpus"
    corpus_files = os.listdir(corpus_folder)
    dataset = []
    for file in corpus_files:
        file_path = os.path.join(corpus_folder, file)
        file_content = open(file_path, 'r', encoding='utf-8').read()
        dataset.append(file_content)

    return dataset


def transform(dataset, n_features=1000):
    vectorizer = TfidfVectorizer(max_df=0.5, max_features=n_features, min_df=2, use_idf=True)
    X = vectorizer.fit_transform(dataset)
    return X, vectorizer


def train(X, vectorizer, true_k=10, minibatch=False, showLable=False):
    # 使用采样数据还是原始数据训练k-means，
    if minibatch:
        km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,
                             init_size=1000, batch_size=1000, verbose=False)
    else:
        km = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=1,
                    verbose=False)
    km.fit(X)
    if showLable:
        print("Top terms per cluster:")
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]
        # terms = vectorizer.get_feature_names()
        terms = vectorizer.get_feature_names_out()
        print(vectorizer.get_stop_words())
        for i in range(true_k):
            print("Cluster %d:" % i, end='')
            for ind in order_centroids[i, :10]:
                print(' %s' % terms[ind], end='')
            print()
    result = list(km.predict(X))
    print('Cluster distribution:')
    print(dict([(i, result.count(i)) for i in result]))
    return -km.score(X)


def test():
    '''测试选择最优参数'''
    dataset = loadDataset()
    print("%d documents" % len(dataset))
    n_features = 100  # 500
    X, vectorizer = transform(dataset, n_features=n_features)
    true_ks = []
    scores = []
    for i in range(3, 80, 1):
        score = train(X, vectorizer, true_k=i) / len(dataset)
        print(i, score)
        true_ks.append(i)
        scores.append(score)
    plt.figure(figsize=(8, 4))
    plt.plot(true_ks, scores, label="error", color="red", linewidth=1)
    plt.xlabel("n_features")
    plt.ylabel("error")
    plt.legend()
    plt.show()


def out():
    '''在最优参数下输出聚类结果'''
    dataset = loadDataset()
    X, vectorizer = transform(dataset, n_features=500)
    score = train(X, vectorizer, true_k=10, showLable=True) / len(dataset)
    print(score)


if __name__ == "__main__":
    test()
    # out()
