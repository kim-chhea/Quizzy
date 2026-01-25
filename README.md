# Quizzy - Your Personal Quiz Generator

## Overview
Quizzy is a modern, responsive web application built with Streamlit that generates personalized quizzes from your dataset. It supports multiple quiz modes (Chinese to English, English to Chinese, Pinyin to Chinese) and provides an interactive, professional interface for learning and testing.

## Features
- 📁 **Dataset Upload**: Support for CSV and Excel files
- 🎯 **Multiple Quiz Modes**: Chinese↔English, Pinyin→Chinese
- 📊 **Customizable Questions**: Choose number of questions from your dataset
- 📱 **Fully Responsive**: Optimized for desktop, tablet, and mobile
- 🎨 **Modern UI**: Clean, professional design with smooth animations
- 📈 **Progress Tracking**: Real-time score and progress display
- 🔄 **Sample Data**: Built-in sample dataset for quick testing

## Quick Start
1. **Setup Environment**:
   ```powershell
   .\setup.ps1 -InstallOnly   # Windows PowerShell
   ```
   Or manually:
   ```bash
   python -m venv .venv
   # Activate: .venv\Scripts\Activate.ps1 (Windows) or source .venv/bin/activate (macOS/Linux)
   pip install -r requirements.txt
   ```

2. **Run the App**:
   ```bash
   streamlit run app.py
   ```
   Or use: `.\setup.ps1 -Run`

3. **Use the App**:
   - Upload your CSV/Excel file with columns: `chinese`, `pinyin`, `english`
   - Select quiz mode and number of questions
   - Answer all questions in one go
   - View your results and score

## Workflow

### 1. Data Upload Phase
- User uploads CSV/Excel file or loads sample data
- App validates and previews the dataset
- User selects quiz mode and question count

### 2. Quiz Generation Phase
- App randomly selects words from dataset (avoiding repeats)
- For each question, generates 3 distractor options
- Questions are shuffled and stored in session

### 3. Quiz Taking Phase
- All questions displayed simultaneously
- User selects answers via radio buttons
- Real-time progress tracking

### 4. Results Phase
- Calculates score and shows correct/incorrect answers
- Option to restart with new quiz

## Algorithm Details

### Question Generation Algorithm
```python
def generate_question(df, mode, used_words):
    # 1. Filter unused words
    available_words = df[~df['chinese'].isin(used_words)]

    # 2. Randomly select target word
    target_row = available_words.sample(1).iloc[0]

    # 3. Build question based on mode
    if mode == "chinese_to_english":
        question = f"What is the word in English for: {target_row['chinese']} ({target_row['pinyin']})"
        correct_answer = target_row["english"]
    # ... other modes

    # 4. Generate distractors
    distractors = get_distractors(df, target_row, correct_answer, mode)

    # 5. Combine and shuffle options
    options = [correct_answer] + distractors
    random.shuffle(options)

    return question_data
```

### Distractor Generation
The `get_distractors` function creates plausible wrong answers by:
- Finding words with similar semantic meaning
- Using words from same POS (part of speech) category
- Ensuring distractors are different from correct answer
- Limiting to 3 distractors per question

### Quiz Initialization
```python
def initialize_quiz(df, settings):
    questions = []
    used_words = set()

    for _ in range(settings['num_questions']):
        question = generate_question(df, settings['mode'], used_words)
        questions.append(question)
        used_words.add(question['target_word'])

    return questions
```

## Code Structure

```
quizzy/
├── app.py                 # Main Streamlit app entry point
├── core/
│   └── loader.py          # Data loading utilities (CSV/Excel)
├── quiz/
│   ├── generator.py       # Question generation logic
│   ├── distractors.py     # Wrong answer generation
│   ├── session.py         # Quiz state management
│   └── answer.py          # Answer validation
├── ui/
│   ├── theme.py           # CSS styling and responsive design
│   ├── upload.py          # File upload interface
│   ├── quiz_view.py       # Quiz taking interface
│   └── results_view.py    # Results display
└── requirements.txt       # Python dependencies
```

## Dataset Format
Your CSV/Excel should contain these columns:
- `chinese`: Chinese characters (e.g., "你好")
- `pinyin`: Pinyin pronunciation (e.g., "nǐ hǎo")
- `english`: English translation (e.g., "hello")
- `pos`: Part of speech (optional, e.g., "interjection")
- `semantic_type`: Category (optional, e.g., "greeting")

## Performance Optimizations
- **Lazy Loading**: Questions generated only when needed
- **Session Caching**: Quiz state stored in Streamlit session
- **Efficient Filtering**: Pandas operations for data manipulation
- **Responsive CSS**: Media queries for smooth mobile experience
- **Minimal Re-renders**: Form-based submission prevents unnecessary updates

## Customization
- Modify `ui/theme.py` for custom styling
- Update `quiz/generator.py` for different question types
- Add new modes in `quiz/generator.py` and `ui/upload.py`

## Troubleshooting
- **Import Errors**: Ensure virtual environment is activated
- **File Upload Issues**: Check CSV/Excel format and column names
- **Performance**: Reduce dataset size or question count for better speed

---

Built with ❤️ using Streamlit. Contributions welcome!
