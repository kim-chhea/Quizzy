import streamlit as st
from quiz.session import initialize_quiz, submit_answer
from ui.theme import inject_ui


def render_quiz():
    inject_ui()

    # Navigation buttons
    st.markdown("""
    <style>
    .nav-buttons {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("🏠 HOME", use_container_width=True, key="home_quiz"):
            st.session_state.page = "mode_select"
            st.session_state.game_mode = None
            st.rerun()
    with col2:
        if st.button("⚙️ SETTINGS", use_container_width=True, key="settings_quiz"):
            st.session_state.page = "upload"
            st.rerun()

    # Larger, cleaner UI for showing all questions at once
    st.markdown(
        """
    <style>
      .quiz-container { max-width: 1000px; margin: 8px auto 24px; }
      .question-card { 
        padding: 24px; 
        border-radius: 16px; 
        background: linear-gradient(135deg, rgba(185, 28, 28, 0.15) 0%, rgba(220, 38, 38, 0.15) 100%);
        border: 2px solid rgba(251, 191, 36, 0.3);
        box-shadow: 0 6px 20px rgba(185, 28, 28, 0.2); 
        margin-bottom: 24px;
        transition: all 0.3s ease;
      }
      .question-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(185, 28, 28, 0.3);
        border-color: rgba(251, 191, 36, 0.5);
      }
      .question-title { 
        font-size: 32px; 
        font-weight: 700; 
        margin-bottom: 15px;
        color: #fbbf24;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
      }
      .options { margin-left: 6px; font-size: 18px; }
      .progress-area { 
        color: #fef3c7; 
        font-size: 18px;
        font-weight: 700;
        background: linear-gradient(135deg, rgba(185, 28, 28, 0.3) 0%, rgba(220, 38, 38, 0.3) 100%);
        border: 2px solid rgba(251, 191, 36, 0.4);
        border-radius: 12px;
        padding: 12px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
      }
      .finish-btn { margin-top: 20px; font-size: 18px; }
      .stRadio label { 
        font-size: 24px !important; 
        font-weight: 600 !important; 
        line-height: 1.5 !important; 
        padding: 8px 0 !important;
        transition: color 0.2s ease;
      }
      .stRadio label:hover {
        color: #fbbf24 !important;
      }

      /* Responsive design */
      @media (max-width: 768px) {
        .quiz-container { max-width: 95%; margin: 4px auto 16px; }
        .question-card { padding: 16px; margin-bottom: 16px; }
        .question-title { font-size: 24px; margin-bottom: 12px; }
        .stRadio label { font-size: 18px !important; padding: 6px 0 !important; }
        .progress-area { font-size: 16px; padding: 10px; }
        .finish-btn { font-size: 16px; margin-top: 16px; }
      }

      @media (max-width: 480px) {
        .question-title { font-size: 20px; }
        .stRadio label { font-size: 16px !important; padding: 4px 0 !important; }
        .question-card { padding: 12px; }
        .progress-area { font-size: 14px; padding: 8px; }
      }
    </style>
    """,
        unsafe_allow_html=True,
    )

    df = st.session_state.get("df")
    if df is None:
        st.error("No dataset loaded. Go back to upload.")
        if st.button("Go to upload"):
            st.session_state.page = "upload"
        return

    settings = st.session_state.get(
        "quiz_settings", {"num_questions": 10, "mode": "chinese_to_english"}
    )
    quiz_data = st.session_state.get(
        "quiz_data", {"questions": [], "current_q": 0, "score": 0, "history": []}
    )

    # Initialize full question set if not present
    if not quiz_data["questions"]:
        quiz_data["questions"] = initialize_quiz(df, settings)
        # reset any previous answers
        st.session_state.quiz_data = quiz_data
        st.session_state.answers = {}

    questions = quiz_data["questions"]
    total_q = len(questions)

    # Header: progress / score
    left, center, right = st.columns([2, 2, 2])
    with left:
        answered_count = sum(1 for i in range(total_q) if st.session_state.get(f"answer_{i}", None) is not None)
        st.markdown(f"<div class='progress-area'>📝 Answered: {answered_count} / {total_q}</div>", unsafe_allow_html=True)
    with center:
        mode_display = {
            "chinese_to_english": "📖 Chinese → English",
            "english_to_chinese": "🔤 English → Chinese", 
            "pinyin_to_chinese": "🗣️🎵 Pinyin → Chinese"
        }.get(settings.get("mode", "chinese_to_english"), "📖 Chinese → English")
        st.markdown(f"<div class='progress-area'>🎓 Mode: {mode_display}</div>", unsafe_allow_html=True)
    with right:
        st.markdown(f"<div class='progress-area'>🏆 Score: {quiz_data.get('score', 0)}</div>", unsafe_allow_html=True)

    st.markdown("<div class='quiz-container'>", unsafe_allow_html=True)

    # Render all questions - optimized with clear structure
    for i, q in enumerate(questions):
        st.markdown("<div class='question-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='question-title'>❓ {i+1}. {q['question_text']}</div>", unsafe_allow_html=True)
        # larger radio options for easier clicking
        st.radio("Select answer", q["options"], key=f"answer_{i}", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

    # Finish button - centered and prominent
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        finish = st.button("✅ FINISH AND GRADE", type="primary", use_container_width=True, key="finish_quiz")

    if finish:
        quiz_data["score"] = 0
        quiz_data["history"] = []
        for i, q in enumerate(questions):
            user_choice = st.session_state.get(f"answer_{i}", None)
            user_choice_val = user_choice if user_choice is not None else ""
            correct = submit_answer(quiz_data["history"], q, user_choice_val)
            if correct:
                quiz_data["score"] += 1
        st.session_state.quiz_data = quiz_data
        st.session_state.page = "results"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
