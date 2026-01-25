import streamlit as st
import pandas as pd
from ui.theme import inject_ui


def render_results():
    inject_ui()
    st.markdown("<h1>📊 Quiz Results</h1>", unsafe_allow_html=True)
    quiz_data = st.session_state.get(
        "quiz_data", {"questions": [], "current_q": 0, "score": 0, "history": []}
    )
    total = len(quiz_data.get("questions", []))
    score = quiz_data.get("score", 0)
    
    # Score display with Chinese icons
    percentage = (score / total * 100) if total > 0 else 0
    if percentage >= 90:
        icon = "🏆"
        message = "Excellent! Keep up the great work!"
        color = "var(--chinese-gold)"
    elif percentage >= 70:
        icon = "🎉"
        message = "Great job! Room for improvement!"
        color = "var(--success)"
    elif percentage >= 50:
        icon = "💪"
        message = "Good effort! Keep practicing!"
        color = "var(--warning)"
    else:
        icon = "🌱"
        message = "Keep going! Start with the basics!"
        color = "var(--error)"
    
    st.markdown(f"""
    <div style="text-align: center; margin: 20px 0;">
        <div style="font-size: 48px; margin-bottom: 10px;">{icon}</div>
        <div style="font-size: 36px; font-weight: bold; color: {color};">{score} / {total}</div>
        <div style="font-size: 18px; color: var(--muted); margin-top: 10px;">{message}</div>
    </div>
    """, unsafe_allow_html=True)
    
    history = quiz_data.get("history", [])
    if history:
        st.markdown("### 📋 Detailed Results")
        df_hist = pd.DataFrame(history)
        st.dataframe(df_hist)
        
        # Download results removed
    
    # Use a form for the restart button to avoid accidental reruns / double-clicks
    with st.form(key="results_form"):
        restart = st.form_submit_button("🔄 Restart Quiz")

    if restart:
        st.session_state.page = "upload"
        st.session_state.df = None
        st.session_state.quiz_data = {
            "questions": [],
            "current_q": 0,
            "score": 0,
            "history": [],
        }
        st.rerun()
