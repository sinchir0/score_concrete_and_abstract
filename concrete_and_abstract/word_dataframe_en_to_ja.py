import os

import deepl
import pandas as pd
from tqdm import tqdm

tqdm.pandas()

API_KEY = os.environ["DEEPL_API_KEY"]

data = pd.read_csv("concrete_and_abstract_word.csv")

source_languge = "EN"
target_language = "JA"

translator = deepl.Translator(API_KEY)


def en_to_ja(text: str, translator=translator):
    result = translator.translate_text(
        text, source_lang=source_languge, target_lang=target_language
    )
    translated_text = result.text
    return translated_text


# 文字を小文字に変換
data["lower_word"] = data["WORD"].str.lower()

data["translated_word"] = data["lower_word"].progress_apply(lambda x: en_to_ja(x))

# 同じ翻訳が行われた場合は重複を削除する
data = data.drop_duplicates("translated_word")

data.to_csv("concrete_and_abstract_word_with_translated_word.csv", index=False)
