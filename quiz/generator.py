import random
from quiz.distractors import get_distractors


def generate_question(df, mode, used_words):
    available_words = df[~df['chinese'].isin(used_words)]
    if available_words.empty:
        available_words = df  # Reset if all used

    target_row = available_words.sample(1).iloc[0]

    # Build a clear, user-friendly question string depending on mode
    if mode == "chinese_to_english":
        prompt = target_row["chinese"]
        pinyin = target_row.get("pinyin", "")
        question_text = f"What is the word in English for: {prompt} ({pinyin})"
        correct_answer = target_row["english"]
    elif mode == "english_to_chinese":
        prompt = target_row["english"]
        question_text = f"What is the word in Chinese for: {prompt}"
        correct_answer = target_row["chinese"]
    elif mode == "pinyin_to_chinese":
        prompt = target_row.get("pinyin", "")
        question_text = f"What is the word in Chinese for the pinyin: {prompt}"
        correct_answer = target_row["chinese"]
    else:
        # fallback: mirror previous behaviour
        question_text = target_row.get("chinese", "")
        correct_answer = target_row.get("english", "")

    distractors = get_distractors(df, target_row, correct_answer, mode)
    options = [correct_answer] + distractors
    random.shuffle(options)

    return {
        "question_text": question_text,
        "options": options,
        "correct_answer": correct_answer,
        "target_row": target_row,
    }
