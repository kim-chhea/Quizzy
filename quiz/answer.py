import random
from typing import List, Dict, Optional
import pandas as pd


def generate_questions(
    df: pd.DataFrame,
    prompt_col: str,
    answer_col: str,
    num_questions: int,
    seed: Optional[int] = None,
) -> List[Dict]:
    """
    Build a list of question dicts from DataFrame.
    Each dict: {"prompt": str, "answer": str}
    """
    if seed is not None:
        random.seed(seed)

    if prompt_col not in df.columns or answer_col not in df.columns:
        raise ValueError("Selected columns not in DataFrame")

    # Drop rows with missing prompt/answer
    sub = df[[prompt_col, answer_col]].dropna()
    if sub.empty:
        return []

    # Determine sample size and sample without replacement when possible
    n = min(num_questions, len(sub))
    sampled = sub.sample(n=n, random_state=seed) if len(sub) >= n else sub.copy()

    questions = []
    for _, row in sampled.iterrows():
        prompt = str(row[prompt_col]).strip()
        answer = str(row[answer_col]).strip()
        questions.append({"prompt": prompt, "answer": answer})
    return questions
