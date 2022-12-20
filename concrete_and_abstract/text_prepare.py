import re


def text_prepare(file_path: str):
    output_list = []
    with open(file_path) as f:
        for line in f:
            # ＠から始まる文章は評価対象に含めない
            if re.match(r"^＠", line):
                continue
            # F：の後ろ部分のみを利用する
            if match := re.search(r"：(.*)", line):
                line = match.group(1)
            # 改行は削除する
            line = line.replace("\n", "")
            # ＜笑い＞のような文字を削除する
            line = re.sub(r"＜.+＞", "", line)
            # 全角スペースを削除する
            line = line.replace("\u3000", "")
            # もし出力結果がNullの場合は出力に追加しない
            if not line:
                continue
            # 出力に追加する
            output_list.append(line)
    return output_list
