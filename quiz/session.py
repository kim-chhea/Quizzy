from quiz.generator import generate_question

def initialize_quiz(df, settings):
    questions = []
    used_words = []
    for _ in range(settings['num_questions']):
        q = generate_question(df, settings['mode'], used_words)
        questions.append(q)
        used_words.append(q['target_row']['chinese'])
    return questions

def submit_answer(history, question, user_choice):
    is_correct = user_choice == question['correct_answer']
    history.append({
        "question_text": question['question_text'],
        "options": question['options'],
        "user_choice": user_choice,
        "correct_choice": question['correct_answer'],
        "is_correct": is_correct,
        **question['target_row'].to_dict()
    })
    return is_correct
