import streamlit as st
import pandas as pd
from quiz.session import initialize_quiz
from multiplayer.qr_generator import generate_qr_code, generate_join_url
from ui.leaderboard import render_leaderboard, render_mini_leaderboard
from ui.theme import inject_ui
from core.loader import load_excel


def _sample_df():
    """Generate sample dataset"""
    data = {
        "chinese": ["你好", "谢谢", "再见", "早上好", "晚安", "对不起", "没关系", "请", "是", "不是"],
        "pinyin": ["nǐ hǎo", "xiè xie", "zài jiàn", "zǎo shàng hǎo", "wǎn ān", "duì bu qǐ", "méi guān xi", "qǐng", "shì", "bú shì"],
        "english": ["hello", "thanks", "goodbye", "good morning", "good night", "sorry", "no problem", "please", "yes", "no"],
        "example_sentence": ["你好！", "谢谢你。", "再见！", "早上好！", "晚安！", "对不起。", "没关系。", "请坐。", "是的。", "不是。"],
        "pos": ["interjection", "verb", "interjection", "interjection", "interjection", "verb", "phrase", "verb", "verb", "verb"],
        "semantic_type": ["greeting", "gratitude", "farewell", "greeting", "farewell", "apology", "response", "courtesy", "affirmation", "negation"],
    }
    return pd.DataFrame(data)


def render_host_setup():
    """Render the host setup screen to create a multiplayer session"""
    inject_ui()
    
    st.markdown("<div class='app-title'>🎮 Host a Multiplayer Quiz 🎮</div>", unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Mode Select", key="back_from_host"):
        st.session_state.page = "mode_select"
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dataset Section
    st.markdown("""
    <style>
    .section-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    .section-title {
        font-size: 22px;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 15px;
    }
    @media (max-width: 768px) {
        .section-card {
            padding: 15px;
        }
        .section-title {
            font-size: 18px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📚 Step 1: Choose Your Dataset</div>', unsafe_allow_html=True)
    
    # Dataset selection tabs
    tab1, tab2 = st.tabs(["📖 Use Sample Dataset", "📁 Upload Custom Dataset"])
    
    with tab1:
        st.markdown("**Quick start with built-in vocabulary**")
        if st.button("✅ Load Sample Dataset", type="primary", use_container_width=True):
            st.session_state.df = _sample_df()
            st.success("✅ Sample dataset loaded!")
            st.rerun()
    
    with tab2:
        st.markdown("**Upload your own CSV or Excel file**")
        st.caption("Required columns: chinese, pinyin, english")
        uploaded = st.file_uploader("Choose File", type=["xlsx", "xls", "csv"], key="host_upload")
        
        if uploaded is not None:
            try:
                custom_df = load_excel(uploaded)
                if custom_df is not None:
                    st.session_state.df = custom_df
                    st.success(f"✅ Dataset loaded! ({len(custom_df)} rows)")
            except Exception as e:
                st.error(f"❌ File loading failed: {str(e)}")
    
    # Show dataset preview if loaded
    if st.session_state.get("df") is not None:
        df = st.session_state.df
        with st.expander("👀 Preview Dataset", expanded=False):
            st.dataframe(df.head(5), use_container_width=True)
            st.caption(f"Total: {len(df)} vocabulary items")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Only show game settings if dataset is loaded
    if st.session_state.get("df") is None:
        st.info("👆 Please load a dataset first to continue")
        return
    
    df = st.session_state.df
    max_questions = len(df)
    
    # Game Settings Section
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚙️ Step 2: Configure Game Settings</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        host_name = st.text_input("👤 Your Name (Host)", value="Quiz Master", key="host_name", max_chars=30)
        
        num_questions = st.slider(
            "📝 Number of Questions",
            min_value=3,
            max_value=min(50, max_questions),
            value=min(10, max_questions),
            key="host_num_questions",
            help="Select how many questions for the game"
        )
    
    with col2:
        mode = st.selectbox(
            "🎓 Quiz Mode",
            ["📖 Chinese → English", "🔤 English → Chinese", "🗣️🎵 Pinyin → Chinese"],
            key="host_mode",
            help="Choose the question format"
        )
        
        time_limit = st.slider(
            "⏱️ Time per Question (seconds)",
            min_value=5,
            max_value=60,
            value=20,
            step=5,
            key="host_time_limit",
            help="Time limit for each question"
        )
    
    # Map display names to internal modes
    mode_map = {
        "📖 Chinese → English": "chinese_to_english",
        "🔤 English → Chinese": "english_to_chinese",
        "🗣️🎵 Pinyin → Chinese": "pinyin_to_chinese",
    }
    internal_mode = mode_map.get(mode, "chinese_to_english")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Summary and Create Button
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🚀 Step 3: Launch Game</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        **Game Summary:**
        - 👤 Host: **{host_name}**
        - 📝 Questions: **{num_questions}**
        - 🎓 Mode: **{mode}**
        - ⏱️ Time Limit: **{time_limit}s per question**
        - 📊 Dataset: **{len(df)} items available**
        """)
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Create Game Session", type="primary", use_container_width=True, key="create_session_btn"):
            # Get the global session manager
            from multiplayer.session_manager import get_global_session_manager
            session_manager = get_global_session_manager()
            
            # Generate questions
            quiz_settings = {
                "num_questions": num_questions,
                "mode": internal_mode,
                "time_limit": time_limit,
            }
            
            with st.spinner("Generating questions..."):
                questions = initialize_quiz(df, quiz_settings)
            
            # Create game session
            session = session_manager.create_session(
                host_name=host_name,
                quiz_settings=quiz_settings,
                questions=questions
            )
            
            st.session_state.current_session_id = session.session_id
            st.session_state.page = "host_lobby"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Help Section
    with st.expander("💡 How to Host a Game"):
        st.markdown("""
        1. **Load Dataset**: Choose sample or upload your own
        2. **Configure Settings**: Set questions, mode, and time limit
        3. **Create Session**: Click the button to generate game PIN and QR code
        4. **Share**: Display QR code or share the 6-digit PIN with players
        5. **Wait**: Players join your lobby
        6. **Start**: Begin the game when everyone is ready
        7. **Control**: Advance questions at your own pace
        8. **Results**: View final leaderboard and winner
        """)
        
    # Tips Section  
    with st.expander("🎯 Hosting Tips"):
        st.markdown("""
        - **For Classrooms**: Use 15-20 questions with 20-30 second time limits
        - **For Quick Games**: Try 5-10 questions with 10-15 second limits
        - **For Practice**: Use 20+ questions with 30-60 second limits
        - **Dataset Quality**: Ensure your dataset has clear, unambiguous answers
        - **Network**: All players must be on same network or use public deployment
        - **Devices**: Players can join from phones, tablets, or computers
        """)


def render_host_lobby():
    """Render the host lobby where players can join"""
    inject_ui()
    
    if "current_session_id" not in st.session_state:
        st.error("Session not found!")
        if st.button("← Go Back"):
            st.session_state.page = "mode_select"
            st.rerun()
        return
    
    from multiplayer.session_manager import get_global_session_manager
    session_manager = get_global_session_manager()
    session = session_manager.get_session(st.session_state.current_session_id)
    if not session:
        st.error("Session expired!")
        if st.button("← Go Back"):
            st.session_state.page = "mode_select"
            st.rerun()
        return
    
    st.markdown("<div class='app-title'>🎮 Game Lobby 🎮</div>", unsafe_allow_html=True)
    
    # Responsive layout
    st.markdown("""
    <style>
    .qr-container {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
    .pin-display {
        font-size: 56px;
        font-weight: bold;
        letter-spacing: 8px;
        margin: 15px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .player-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 10px;
        margin: 15px 0;
    }
    .player-item {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
    }
    @media (max-width: 768px) {
        .pin-display {
            font-size: 42px;
            letter-spacing: 4px;
        }
        .player-grid {
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class='qr-container'>
        <h2 style='color: white; margin: 0;'>📱 Scan to Join</h2>
        <div class='pin-display'>{}</div>
        <p style='font-size: 18px; margin: 5px 0;'>Game PIN</p>
        </div>
        """.format(session.session_id), unsafe_allow_html=True)
        
        # Generate QR code
        join_url = generate_join_url(session.session_id)
        # Try to get base URL for better QR codes
        try:
            import os
            codespace_name = os.environ.get('CODESPACE_NAME')
            if codespace_name:
                join_url = generate_join_url(session.session_id, f"https://{codespace_name}-8501.app.github.dev")
        except:
            pass
        
        qr_code_b64 = generate_qr_code(join_url, size=350)
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: white; border-radius: 10px;'>
        <img src='{qr_code_b64}' style='max-width: 100%; height: auto; border-radius: 10px;'/>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("📱 Players can scan this QR code or enter PIN manually")
    
    with col2:
        st.markdown(f"""
        <div class='section-card'>
        <div class='section-title'>👥 Players ({len(session.players)})</div>
        </div>
        """, unsafe_allow_html=True)
        
        if session.players:
            # Display players in a grid
            player_html = '<div class="player-grid">'
            for player_id, player_data in session.players.items():
                player_html += f"""
                <div class='player-item'>
                🎮 {player_data['name']}
                </div>
                """
            player_html += '</div>'
            st.markdown(player_html, unsafe_allow_html=True)
        else:
            st.info("⏳ Waiting for players to join...")
            st.markdown("""
            **How players join:**
            1. Open Quizzy
            2. Click "Join Game"
            3. Enter PIN: **{}**
            4. Type their name
            """.format(session.session_id))
        
        st.markdown("---")
        
        # Control buttons
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        with col_b:
            # Auto-refresh toggle
            auto_refresh = st.checkbox("Auto-refresh", value=False)
            if auto_refresh:
                import time
                time.sleep(2)
                st.rerun()
        
        st.markdown("---")
        
        # Start game button
        if len(session.players) > 0:
            if st.button("🚀 Start Game", type="primary", use_container_width=True, key="start_game_btn"):
                session.start_game()
                st.session_state.page = "host_game"
                st.rerun()
            st.success(f"✅ Ready to start with {len(session.players)} player(s)")
        else:
            st.button("🚀 Start Game", type="primary", use_container_width=True, disabled=True)
            st.caption("⚠️ Need at least 1 player to start")
        
        if st.button("❌ Cancel Game", use_container_width=True):
            from multiplayer.session_manager import get_global_session_manager
            session_manager = get_global_session_manager()
            session_manager.close_session(session.session_id)
            st.session_state.page = "host_setup"
            st.rerun()


def render_host_game():
    """Render the active game view for the host"""
    inject_ui()
    
    if "current_session_id" not in st.session_state:
        st.error("Session not found!")
        return
    
    from multiplayer.session_manager import get_global_session_manager
    session_manager = get_global_session_manager()
    session = session_manager.get_session(st.session_state.current_session_id)
    if not session:
        st.error("Session expired!")
        return
    
    if session.status == "finished":
        st.session_state.page = "host_results"
        st.rerun()
        return
    
    current_q = session.current_question
    question = session.questions[current_q]
    total_questions = len(session.questions)
    
    st.markdown("<div class='app-title'>🎮 Game in Progress 🎮</div>", unsafe_allow_html=True)
    
    # Responsive styles
    st.markdown("""
    <style>
    .question-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    .option-box {
        background: #f0f2f6;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        font-size: 18px;
        transition: transform 0.2s;
    }
    .option-box:hover {
        transform: translateX(5px);
    }
    .stats-box {
        padding: 15px;
        background: #e8f5e9;
        border-radius: 8px;
        margin: 15px 0;
    }
    @media (max-width: 768px) {
        .question-card {
            padding: 15px;
        }
        .option-box {
            font-size: 16px;
            padding: 12px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Progress bar
    progress = (current_q + 1) / total_questions
    st.progress(progress)
    st.markdown(f"### Question {current_q + 1} of {total_questions}")
    
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        # Display question
        st.markdown(f"""
        <div class='question-card'>
        <h2 style='color: #667eea; margin-bottom: 20px;'>{question['question_text']}</h2>
        """, unsafe_allow_html=True)
        
        for i, option in enumerate(question['options']):
            st.markdown(f"""
            <div class='option-box'>
            <strong>{chr(65+i)}.</strong> {option}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Question stats
        stats = session.get_current_question_stats()
        st.markdown(f"""
        <div class='stats-box'>
        <strong>📊 Response Stats:</strong><br>
        ✅ Answered: <strong>{stats['answered']}/{stats['total_players']}</strong> • 
        🎯 Correct: <strong>{stats['correct']}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Mini leaderboard
        st.markdown("### 🏆 Current Rankings")
        leaderboard = session.get_leaderboard()
        render_mini_leaderboard(leaderboard, top_n=5)
        
        st.markdown("---")
        
        # Control buttons
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        with col_b:
            # Auto-refresh toggle
            if st.checkbox("Auto", value=False, help="Auto-refresh"):
                import time
                time.sleep(2)
                st.rerun()
        
        st.markdown("---")
        
        # Next question button
        if current_q < total_questions - 1:
            if st.button("➡️ Next Question", type="primary", use_container_width=True, key="next_q_btn"):
                session.next_question()
                st.rerun()
            st.caption(f"{total_questions - current_q - 1} questions remaining")
        else:
            if st.button("🏁 Finish Game", type="primary", use_container_width=True, key="finish_btn"):
                session.status = "finished"
                st.session_state.page = "host_results"
                st.rerun()
            st.caption("Last question!")


def render_host_results():
    """Render final results for host"""
    inject_ui()
    
    if "current_session_id" not in st.session_state:
        st.error("Session not found!")
        return
    
    from multiplayer.session_manager import get_global_session_manager
    session_manager = get_global_session_manager()
    session = session_manager.get_session(st.session_state.current_session_id)
    if not session:
        st.error("Session expired!")
        return
    
    st.markdown("<div class='app-title'>🎉 Game Over! 🎉</div>", unsafe_allow_html=True)
    
    st.balloons()
    
    # Game stats summary
    leaderboard = session.get_leaderboard()
    if leaderboard:
        winner = leaderboard[0]
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); 
                    color: white; padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0;'>
        <h1 style='color: white; margin: 0;'>👑 Winner: {winner['name']} 👑</h1>
        <p style='font-size: 36px; font-weight: bold; margin: 10px 0;'>{winner['score']:,} points</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Full leaderboard
    st.markdown("### 📊 Final Leaderboard")
    render_leaderboard(leaderboard, show_details=True)
    
    st.markdown("---")
    
    # Game statistics
    with st.expander("📈 Game Statistics"):
        total_players = len(session.players)
        total_questions = len(session.questions)
        st.markdown(f"""
        - **Total Players**: {total_players}
        - **Total Questions**: {total_questions}
        - **Quiz Mode**: {session.quiz_settings.get('mode', 'N/A')}
        - **Time per Question**: {session.quiz_settings.get('time_limit', 'N/A')}s
        - **Hosted by**: {session.host_name}
        """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 New Game", type="primary", use_container_width=True):
            st.session_state.session_manager.close_session(session.session_id)
            st.session_state.page = "host_setup"
            st.rerun()
    
    with col2:
        if st.button("📊 View Again", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.session_manager.close_session(session.session_id)
            st.session_state.page = "mode_select"
            st.rerun()


def render_host_view():
    """Main router for host views"""
    page = st.session_state.get("page", "host_setup")
    
    if page == "host_setup":
        render_host_setup()
    elif page == "host_lobby":
        render_host_lobby()
    elif page == "host_game":
        render_host_game()
    elif page == "host_results":
        render_host_results()
    else:
        render_host_setup()
