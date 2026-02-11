import os

import pandas as pd
import streamlit as st
from core.validator import (
    ensure_optional_columns,
    get_missing_required_columns,
    validate_columns,
)

@st.cache_data
def _read_tabular(file):
    name = getattr(file, "name", "")
    _, ext = os.path.splitext(name.lower())
    if ext in {".csv"}:
        return pd.read_csv(file)
    if ext in {".xlsx", ".xls"}:
        return pd.read_excel(file)
    # Try Excel by default if extension is missing or unknown.
    return pd.read_excel(file)


def load_excel(file):
    df = _read_tabular(file)
    if validate_columns(df):
        return ensure_optional_columns(df)

    missing = get_missing_required_columns(df)
    missing_text = ", ".join(missing) if missing else "unknown"
    st.error(f"Invalid file: missing required columns: {missing_text}")
    return None
