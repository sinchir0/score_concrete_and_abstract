import nltk
import pandas as pd
import vibrato

nltk.download("averaged_perceptron_tagger")

with open("ipadic-mecab-2_7_0/system.dic", "rb") as fp:
    dict_data = fp.read()
tokenizer = vibrato.Vibrato(dict_data)


def filter_mrcdb(df: pd.DataFrame) -> pd.DataFrame:
    en_noun_bool = [
        True if nltk.pos_tag([word])[0][1] in ["NN", "NNS", "NNP", "NNPS"] else False
        for word in df["translated_word"]
    ]

    ja_noun_bool = [
        True if "名詞" in tokenizer.tokenize(word)[0].feature() else False
        for word in df["translated_word"]
    ]

    bool_list = [min(val) for val in zip(en_noun_bool, ja_noun_bool)]

    filtered_df = df[bool_list].reset_index(drop=True)
    return filtered_df
