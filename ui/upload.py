import streamlit as st
import pandas as pd
from core.loader import load_excel
from ui.theme import inject_ui


def _sample_df():
    # minimal sample with required columns
    data = {
        "chinese": ["你好", "谢谢", "再见"],
        "pinyin": ["nǐ hǎo", "xiè xie", "zài jiàn"],
        "english": ["hello", "thanks", "goodbye"],
        "example_sentence": ["你好！", "谢谢你。", "再见！"],
        "pos": ["interjection", "verb", "interjection"],
        "semantic_type": ["greeting", "gratitude", "farewell"],
    }
    return pd.DataFrame(data)


def render_upload():
    inject_ui()
    # Chinese-themed catchy UI
    st.markdown("<div class='app-title'>🌟 Quizzy - Your Personal Quiz Generator 🎯</div>", unsafe_allow_html=True)
    st.markdown("<div class='step-progress'><div class='bar'></div></div>", unsafe_allow_html=True)

    st.markdown("<h3>🎯 Choose Your Learning Mode</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<div class='upload-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chinese-welcome'>🌟 Welcome to the World of Chinese Learning!<br/>Start your language adventure! 🚀</div>", unsafe_allow_html=True)
        
        # Default to sample dataset
        df_preview = _sample_df()
        max_rows = len(df_preview)
        
        st.success(f"📚 Using Sample Dataset ({max_rows} Vocabularies)")
        st.markdown("**✨ Start Learning Basic Chinese Vocabulary Now**")
        
        # Optional upload
        st.markdown("---")
        st.markdown("🔧 Advanced Option: Upload Your Own Dataset")
        uploaded = st.file_uploader("Choose File", type=["xlsx", "xls", "csv"], label_visibility="collapsed")

        if uploaded is not None:
            try:
                custom_df = load_excel(uploaded)
                if custom_df is not None:
                    df_preview = custom_df
                    max_rows = len(df_preview)
                    st.success(f"🎉 Custom dataset loaded! ({max_rows} rows)")
            except Exception:
                st.error("❌ File loading failed, please check the format")
        
        # Settings
        st.markdown("### ⚙️ Learning Settings")
        num_questions = st.slider("📝 Number of Questions", min_value=1, max_value=max_rows, value=min(10, max_rows), key="num_questions")
        st.write(f"🎯 Selected: {num_questions} questions")
        
        mode = st.selectbox("🎓 Quiz Mode", ["📖 Chinese → English", "🔤 English → Chinese", "🗣️🎵 Pinyin → Chinese"], index=0, key="mode")
        
        # Map display names to internal modes
        if mode == "📖 Chinese → English":
            internal_mode = "chinese_to_english"
        elif mode == "🔤 English → Chinese":
            internal_mode = "english_to_chinese"
        elif mode == "🗣️🎵 Pinyin → Chinese":
            internal_mode = "pinyin_to_chinese"
        else:
            internal_mode = "chinese_to_english"
        
        st.session_state["internal_mode"] = internal_mode
        
        # Start button
        if st.button("🚀 Start Quiz", type="primary"):
            # Use current df_preview (either sample or uploaded)
            st.session_state.df = df_preview
            st.session_state.quiz_settings["num_questions"] = num_questions
            st.session_state.quiz_settings["mode"] = internal_mode
            st.session_state.quiz_data = {
                "questions": [],
                "current_q": 0,
                "score": 0,
                "history": [],
            }
            st.session_state.page = "quiz"
            st.rerun()

        # Preview
        st.markdown("### 👀 Data Preview")
        st.dataframe(df_preview.head(6), height=220)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='upload-card'>", unsafe_allow_html=True)
        st.markdown("<h4>🎊 Learning Tips</h4>", unsafe_allow_html=True)
        st.markdown("""
        💡 **Study Tips:**
        - Start with basic vocabulary
        - Practice 10-15 minutes daily
        - Listen to standard pronunciation
        - Learn with example sentences
        
        🏆 **Goals:**
        - Build vocabulary
        - Improve reading comprehension
        - Enhance speaking skills
        """)
        st.markdown("</div>", unsafe_allow_html=True)
