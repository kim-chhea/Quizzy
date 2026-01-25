REQUIRED_COLUMNS = ["chinese", "pinyin", "english", "example_sentence", "pos", "semantic_type"]

def validate_columns(df):
    return all(col in df.columns for col in REQUIRED_COLUMNS)
