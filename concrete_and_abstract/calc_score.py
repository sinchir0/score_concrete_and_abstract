import pandas as pd


def calc_score_by_word(
    org_text_list: list, split_text_list: list, mrcdb: pd.DataFrame
) -> list:
    text_score_list = []
    for org_text, split_text in zip(org_text_list, split_text_list):
        use_word = []
        for word in mrcdb["translated_word"]:
            if word in split_text:
                use_word.append(word)
        use_word_score = mrcdb[mrcdb["translated_word"].isin(use_word)]
        cnc_score = use_word_score["CNC"].mean()
        image_score = use_word_score["IMG"].mean()

        concrete_score = (cnc_score + image_score) / 2

        text_score_list.append((org_text, use_word, concrete_score))

    return text_score_list


def calc_score_by_word_only_concrete_score(
    org_text_list: list, split_text_list: list, mrcdb: pd.DataFrame
) -> list:
    text_score_list = []
    for org_text, split_text in zip(org_text_list, split_text_list):
        use_word = []
        for word in mrcdb["text"]:
            if word in split_text:
                use_word.append(word)
        use_word_score = mrcdb[mrcdb["text"].isin(use_word)]
        concrete_score = use_word_score["concrete_score"].mean()

        text_score_list.append((org_text, use_word, concrete_score))

    return text_score_list
