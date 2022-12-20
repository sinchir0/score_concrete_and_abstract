import vibrato

# 分かち書きを行う
with open("ipadic-mecab-2_7_0/system.dic", "rb") as fp:
    dict_data = fp.read()
tokenizer = vibrato.Vibrato(dict_data)


def tokenize_by_vibrato(text: str):
    return tokenizer.tokenize(text)

