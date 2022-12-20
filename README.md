# インストール

```bash
poetry install
```

# 英語を日本語を変換

```bash
poetry run python concrete_and_abstract/word_dataframe_en_to_ja.py 
```

# 推論

```bash
poetry run python concrete_and_abstract/add_mrcdb.py
```

# スコアリング
## 推論なし

```bash
poetry run python concrete_and_abstract/main_with_pred.py
```

## 推論あり

```bash
poetry run python concrete_and_abstract/main_with_pred.py
```