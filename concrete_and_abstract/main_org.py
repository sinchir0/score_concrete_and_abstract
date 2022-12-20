import pandas as pd
from calc_score import calc_score_by_word
from filter_mrcdb import filter_mrcdb
from text_prepare import text_prepare
from tokenizer import tokenize_by_vibrato

# データの用意
text_list = text_prepare(file_path="data001.txt")
translated_mrcdb = pd.read_csv("concrete_and_abstract_word_with_translated_word.csv")

# MRCDBを名詞に限定する
filtered_translated_mrcdb = filter_mrcdb(df=translated_mrcdb)

# 具体度の計算を行う
filtered_translated_mrcdb["concrete_score"] = (
    filtered_translated_mrcdb["CNC"] + filtered_translated_mrcdb["IMG"]
) / 2

# 分かち書き
split_text_list = [
    [token.surface() for token in tokenize_by_vibrato(text) if "名詞" in token.feature()]
    for text in text_list
]

# テキストごとにスコアリングを行う
text_score_list = calc_score_by_word(
    org_text_list=text_list,
    split_text_list=split_text_list,
    mrcdb=filtered_translated_mrcdb,
)

data = pd.DataFrame(text_score_list, columns=["org_text", "use_word", "concrete_score"])
data.to_csv("scored_text.csv", index=False)
