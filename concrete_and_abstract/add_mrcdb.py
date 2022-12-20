import itertools

import numpy as np
import pandas as pd
from filter_mrcdb import filter_mrcdb
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from text_prepare import text_prepare
from tokenizer import tokenize_by_vibrato
from word_vector import get_word_vector

# mrcdbの読み込み
translated_mrcdb = pd.read_csv("concrete_and_abstract_word_with_translated_word.csv")

# MRCDBを名詞に限定する
filtered_translated_mrcdb = filter_mrcdb(df=translated_mrcdb)

# 具体度の計算を行う
filtered_translated_mrcdb["concrete_score"] = (
    filtered_translated_mrcdb["CNC"] + filtered_translated_mrcdb["IMG"]
) / 2

# テストデータの用意
text_list = text_prepare(file_path="data001.txt")

# 分かち書きを行い名詞に限定する
split_text_list_only_noun = [
    [token.surface() for token in tokenize_by_vibrato(text) if "名詞" in token.feature()]
    for text in text_list
]

test_noun_list = list(set(itertools.chain.from_iterable(split_text_list_only_noun)))

# trainと重複する単語を除く
train_noun_list = list(set(filtered_translated_mrcdb["translated_word"]))
test_noun_list = list(
    set(test_noun_list) ^ (set(train_noun_list) & set(test_noun_list))
)

# SVRの学習のためのデータを、mrcdbから用意する
train_noun_list_with_vector = [
    (text, get_word_vector(text), concrete_score)
    for text, concrete_score in zip(
        filtered_translated_mrcdb["translated_word"],
        filtered_translated_mrcdb["concrete_score"],
    )
]

train = pd.DataFrame(
    train_noun_list_with_vector, columns=["text", "vector", "concrete_score"]
)

test_noun_list_with_vector = [(text, get_word_vector(text)) for text in test_noun_list]

test = pd.DataFrame(test_noun_list_with_vector, columns=["text", "vector"])

# vectorがNoneのデータは利用しない
train = train[train["vector"].notnull()].reset_index(drop=True)
test = test[test["vector"].notnull()].reset_index(drop=True)

# train, testのflgをつける
train["genre"] = "train"
test["genre"] = "test"

merge_data = pd.concat([train, test]).reset_index(drop=True)

# 標準化を行う
scaler = StandardScaler()
vector_norm = scaler.fit_transform(np.array(merge_data["vector"].tolist()))

vector_col_name = [f"vector_{idx}" for idx in list(range(200))]

# vector(200のlist)を展開する
vector = pd.DataFrame(
    vector_norm,
    columns=vector_col_name,
)

merge_data = pd.concat([merge_data, vector], axis=1).drop("vector", axis=1)

# train, testに分割する
train = merge_data[merge_data["genre"] == "train"].reset_index(drop=True)
test = merge_data[merge_data["genre"] == "test"].reset_index(drop=True)

# 学習
model = SVR()
model.fit(train[vector_col_name], train["concrete_score"])

# 推論
pred = model.predict(test[vector_col_name])

# 出力
test["concrete_score"] = pred

filtered_translated_mrcdb_with_pred = pd.concat(
    [
        filtered_translated_mrcdb[["translated_word", "concrete_score"]].rename(
            columns={"translated_word": "text"}
        ),
        test[["text", "concrete_score"]],
    ]
)

filtered_translated_mrcdb_with_pred.to_csv(
    "filtered_translated_mrcdb_with_pred.csv", index=False
)
