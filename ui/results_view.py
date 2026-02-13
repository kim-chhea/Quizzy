import streamlit as st
import pandas as pd
from ui.theme import inject_ui


def render_results():
    inject_ui()
    
    st.markdown("""
    <style>
    .results-container {
        max-width: 700px;
        margin: 0 auto;
    }
    .score-card {
        background: linear-gradient(135deg, #b91c1c 0%, #dc2626 50%, #b91c1c 100%);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        border: 4px solid #fbbf24;
        box-shadow: 0 15px 45px rgba(185, 28, 28, 0.6);
        margin: 30px auto;
        position: relative;
        overflow: hidden;
    }
    .score-card::before {
        content: '福';
        position: absolute;
        top: -30px;
        right: -30px;
        font-size: 180px;
        opacity: 0.05;
        font-weight: bold;
        color: #fbbf24;
    }
    .score-icon {
        font-size: 80px;
        margin-bottom: 20px;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
        animation: bounce 2s infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    .score-text {
        font-size: 56px;
        font-weight: 900;
        color: #fef3c7;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        margin: 20px 0;
        letter-spacing: 3px;
    }
    .score-message {
        color: white;
        font-size: 20px;
        font-weight: 600;
        margin-top: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }
    .percentage-badge {
        display: inline-block;
        background: rgba(254, 243, 199, 0.2);
        border: 2px solid #fbbf24;
        border-radius: 30px;
        padding: 8px 20px;
        margin: 15px 0;
        font-size: 18px;
        font-weight: 700;
        color: #fef3c7;
    }
    .details-section {
        background: linear-gradient(135deg, rgba(185, 28, 28, 0.3) 0%, rgba(220, 38, 38, 0.3) 100%);
        border: 3px solid rgba(251, 191, 36, 0.4);
        border-radius: 16px;
        padding: 25px;
        margin: 25px auto;
        max-width: 700px;
    }
    .details-title {
        color: #fef3c7;
        font-size: 24px;
        font-weight: 900;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }
    .button-group {
        display: flex;
        gap: 15px;
        justify-content: center;
        margin: 30px auto;
        max-width: 600px;
        flex-wrap: wrap;
    }
    .nav-button {
        flex: 1;
        min-width: 200px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #fbbf24; font-size: 42px; font-weight: 900; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); margin-bottom: 30px;'>📊 QUIZ RESULTS 📊</h1>", unsafe_allow_html=True)
    
    quiz_data = st.session_state.get(
        "quiz_data", {"questions": [], "current_q": 0, "score": 0, "history": []}
    )
    total = len(quiz_data.get("questions", []))
    score = quiz_data.get("score", 0)
    
    # Score display with ang pao theme
    percentage = (score / total * 100) if total > 0 else 0
    if percentage >= 90:
        icon = "🏆"
        message = "EXCELLENT! PERFECT MASTERY!"
    elif percentage >= 70:
        icon = "🎉"
        message = "GREAT JOB! WELL DONE!"
    elif percentage >= 50:
        icon = "💪"
        message = "GOOD EFFORT! KEEP GOING!"
    else:
        icon = "🌱"
        message = "KEEP PRACTICING! YOU'LL IMPROVE!"
    
    st.markdown(f"""
    <div class='score-card'>
        <div class='score-icon'>{icon}</div>
        <div class='score-text'>{score} / {total}</div>
        <div class='percentage-badge'>{percentage:.1f}%</div>
        <div class='score-message'>{message}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed results in expander for better performance
    history = quiz_data.get("history", [])
    if history:
        with st.expander("📋 VIEW DETAILED RESULTS", expanded=False):
            st.markdown("<div class='details-title'>Question-by-Question Breakdown</div>", unsafe_allow_html=True)
            # Use pandas for efficient data display
            df_hist = pd.DataFrame(history)
            st.dataframe(df_hist, use_container_width=True, hide_index=True)
    
    # Navigation buttons
    st.markdown("<div class='button-group'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏠 BACK TO HOME", use_container_width=True, type="primary", key="home_btn"):
            # Reset all session state to go back to home
            st.session_state.page = "mode_select"
            st.session_state.game_mode = None
            st.session_state.df = None
            st.session_state.quiz_data = {
                "questions": [],
                "current_q": 0,
                "score": 0,
                "history": [],
            }
            st.rerun()
    
    with col2:
        if st.button("🔄 RESTART QUIZ", use_container_width=True, type="secondary", key="restart_btn"):
            # Keep mode but reset quiz
            st.session_state.page = "upload"
            st.session_state.df = None
            st.session_state.quiz_data = {
                "questions": [],
                "current_q": 0,
                "score": 0,
                "history": [],
            }
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

