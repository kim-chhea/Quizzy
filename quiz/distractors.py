import random


def get_distractors(df, target_row, correct_answer, mode):
    answer_col = "english" if mode == "chinese_to_english" else "chinese"
    if mode == "pinyin_to_chinese":
        answer_col = "chinese"

    # Strategy 1: Same pos and semantic_type
    candidates = df[
        (df["pos"] == target_row["pos"])
        & (df["semantic_type"] == target_row["semantic_type"])
        & (df[answer_col] != correct_answer)
    ]
    if len(candidates) >= 3:
        return random.sample(list(candidates[answer_col]), 3)

    # Strategy 2: Same pos
    candidates = df[
        (df["pos"] == target_row["pos"]) & (df[answer_col] != correct_answer)
    ]
    if len(candidates) >= 3:
        return random.sample(list(candidates[answer_col]), 3)

    # Strategy 3: Same semantic_type
    candidates = df[
        (df["semantic_type"] == target_row["semantic_type"])
        & (df[answer_col] != correct_answer)
    ]
    if len(candidates) >= 3:
        return random.sample(list(candidates[answer_col]), 3)

    # Fallback: build a robust list of unique values excluding the correct answer
    unique_candidates = list(df[df[answer_col] != correct_answer][answer_col].unique())
    if len(unique_candidates) >= 3:
        return random.sample(unique_candidates, 3)
    if len(unique_candidates) > 0:
        picked = random.sample(unique_candidates, min(3, len(unique_candidates)))
        # fill remaining slots by sampling with replacement from available uniques
        while len(picked) < 3:
            picked.append(random.choice(unique_candidates))
        return picked

    # Ultimate fallback: include any values (including the correct answer) if necessary
    fallback_all = list(df[answer_col].unique())
    if not fallback_all:
        # defensively return the correct_answer repeated if DataFrame lacks values
        return [correct_answer, correct_answer, correct_answer]
    picked = random.sample(fallback_all, min(3, len(fallback_all)))
    while len(picked) < 3:
        picked.append(random.choice(fallback_all))
    return picked
