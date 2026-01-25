import pandas as pd
import streamlit as st
from core.validator import validate_columns

@st.cache_data
def load_excel(file):
    df = pd.read_excel(file)
    if validate_columns(df):
        return df
    else:
        st.error("Invalid Excel file: Missing required columns.")
        return None
