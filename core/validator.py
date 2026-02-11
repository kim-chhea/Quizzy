REQUIRED_COLUMNS = ["chinese", "pinyin", "english"]
OPTIONAL_COLUMNS = ["example_sentence", "pos", "semantic_type"]


def validate_columns(df):
    return all(col in df.columns for col in REQUIRED_COLUMNS)


def ensure_optional_columns(df):
    for col in OPTIONAL_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df


def get_missing_required_columns(df):
    return [col for col in REQUIRED_COLUMNS if col not in df.columns]
