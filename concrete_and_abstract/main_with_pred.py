import pandas as pd
from calc_score import calc_score_by_word, calc_score_by_word_only_concrete_score
from filter_mrcdb import filter_mrcdb
from text_prepare import text_prepare
from tokenizer import tokenize_by_vibrato

# データの用意
text_list = text_prepare(file_path="data001.txt")
filtered_translated_mrcdb_with_pred = pd.read_csv(
    "filtered_translated_mrcdb_with_pred.csv"
)

# 分かち書き
split_text_list = [
    [token.surface() for token in tokenize_by_vibrato(text) if "名詞" in token.feature()]
    for text in text_list
]

# テキストごとにスコアリングを行う
text_score_list = calc_score_by_word_only_concrete_score(
    org_text_list=text_list,
    split_text_list=split_text_list,
    mrcdb=filtered_translated_mrcdb_with_pred,
)

data = pd.DataFrame(text_score_list, columns=["org_text", "use_word", "concrete_score"])
data.to_csv("scored_text_with_pred.csv", index=False)
