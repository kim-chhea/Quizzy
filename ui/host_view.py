import streamlit as st
from quiz.session import initialize_quiz
from multiplayer.qr_generator import generate_qr_code, generate_join_url
from ui.leaderboard import render_leaderboard, render_mini_leaderboard
from ui.theme import inject_ui


def render_host_setup():
    """Render the host setup screen to create a multiplayer session"""
    inject_ui()
    
    st.markdown("<div class='app-title'>🎮 Host a Multiplayer Quiz 🎮</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='upload-card'>
    <h3>🎯 Create Your Game Session</h3>
    <p>Host a quiz game that others can join using a QR code or game PIN!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Game Settings")
        
        host_name = st.text_input("Your Name (Host)", value="Quiz Master", key="host_name")
        
        if st.session_state.get("df") is None:
            st.warning("⚠️ Please upload a dataset first!")
            if st.button("← Go Back to Upload"):
                st.session_state.page = "upload"
                st.rerun()
            return
        
        df = st.session_state.df
        max_questions = len(df)
        
        num_questions = st.slider(
            "Number of Questions",
            min_value=3,
            max_value=min(50, max_questions),
            value=min(10, max_questions),
            key="host_num_questions"
        )
        
        mode = st.selectbox(
            "Quiz Mode",
            ["📖 Chinese → English", "🔤 English → Chinese", "🗣️🎵 Pinyin → Chinese"],
            key="host_mode"
        )
        
        # Map display names to internal modes
        mode_map = {
            "📖 Chinese → English": "chinese_to_english",
            "🔤 English → Chinese": "english_to_chinese",
            "🗣️🎵 Pinyin → Chinese": "pinyin_to_chinese",
        }
        internal_mode = mode_map.get(mode, "chinese_to_english")
        
        time_limit = st.slider(
            "Time per Question (seconds)",
            min_value=5,
            max_value=60,
            value=20,
            step=5,
            key="host_time_limit"
        )
        
        st.markdown("---")
        
        if st.button("🚀 Create Game Session", type="primary", use_container_width=True):
            # Initialize session manager if not exists
            if "session_manager" not in st.session_state:
                from multiplayer.session_manager import SessionManager
                st.session_state.session_manager = SessionManager()
            
            # Generate questions
            quiz_settings = {
                "num_questions": num_questions,
                "mode": internal_mode,
                "time_limit": time_limit,
            }
            questions = initialize_quiz(df, quiz_settings)
            
            # Create game session
            session = st.session_state.session_manager.create_session(
                host_name=host_name,
                quiz_settings=quiz_settings,
                questions=questions
            )
            
            st.session_state.current_session_id = session.session_id
            st.session_state.page = "host_lobby"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class='upload-card'>
        <h4>🎮 How It Works</h4>
        <ol>
            <li>Create a game session</li>
            <li>Share QR code or PIN</li>
            <li>Players join and enter name</li>
            <li>Start when ready!</li>
            <li>Control game pace</li>
            <li>See live rankings</li>
        </ol>
        <br>
        <h4>⚡ Features</h4>
        <ul>
            <li>🏆 Real-time leaderboard</li>
            <li>⏱️ Timed questions</li>
            <li>📊 Speed bonus points</li>
            <li>📱 Mobile-friendly</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)


def render_host_lobby():
    """Render the host lobby where players can join"""
    inject_ui()
    
    if "session_manager" not in st.session_state or "current_session_id" not in st.session_state:
        st.error("Session not found!")
        if st.button("← Go Back"):
            st.session_state.page = "upload"
            st.rerun()
        return
    
    session = st.session_state.session_manager.get_session(st.session_state.current_session_id)
    if not session:
        st.error("Session expired!")
        if st.button("← Go Back"):
            st.session_state.page = "upload"
            st.rerun()
        return
    
    st.markdown("<div class='app-title'>🎮 Game Lobby 🎮</div>", unsafe_allow_html=True)
    
    # Display QR code and PIN
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div class='upload-card' style='text-align: center;'>
        <h2>📱 Scan to Join</h2>
        <p style='font-size: 48px; font-weight: bold; color: #667eea;'>{session.session_id}</p>
        <p>Game PIN</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate QR code
        join_url = generate_join_url(session.session_id)
        # For local development, use the full URL if available
        if "CODESPACE_NAME" in st.session_state:
            base_url = f"https://{st.session_state.CODESPACE_NAME}.github.dev"
            join_url = generate_join_url(session.session_id, base_url)
        
        qr_code_b64 = generate_qr_code(join_url)
        st.markdown(f"""
        <div style='text-align: center; padding: 20px;'>
        <img src='{qr_code_b64}' style='max-width: 300px; border-radius: 10px;'/>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='upload-card'>
        <h3>👥 Players ({len(session.players)})</h3>
        <p>Waiting for players to join...</p>
        </div>
        """, unsafe_allow_html=True)
        
        if session.players:
            for player_id, player_data in session.players.items():
                st.markdown(f"""
                <div style='background: #f0f2f6; padding: 10px; margin: 5px 0; border-radius: 8px;'>
                🎮 <strong>{player_data['name']}</strong>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No players yet. Share the QR code or PIN!")
        
        st.markdown("---")
        
        # Auto-refresh button
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        
        # Start game button
        if len(session.players) > 0:
            if st.button("🚀 Start Game", type="primary", use_container_width=True):
                session.start_game()
                st.session_state.page = "host_game"
                st.rerun()
        else:
            st.button("🚀 Start Game", type="primary", use_container_width=True, disabled=True)
            st.caption("Need at least 1 player to start")
        
        if st.button("❌ Cancel Game", use_container_width=True):
            st.session_state.session_manager.close_session(session.session_id)
            st.session_state.page = "upload"
            st.rerun()


def render_host_game():
    """Render the active game view for the host"""
    inject_ui()
    
    if "session_manager" not in st.session_state or "current_session_id" not in st.session_state:
        st.error("Session not found!")
        return
    
    session = st.session_state.session_manager.get_session(st.session_state.current_session_id)
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
    
    # Progress bar
    progress = (current_q + 1) / total_questions
    st.progress(progress)
    st.markdown(f"### Question {current_q + 1} of {total_questions}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display question
        st.markdown(f"""
        <div class='upload-card'>
        <h2 style='color: #667eea;'>{question['question_text']}</h2>
        <div style='margin-top: 20px;'>
        """, unsafe_allow_html=True)
        
        for i, option in enumerate(question['options']):
            st.markdown(f"""
            <div style='background: #f0f2f6; padding: 15px; margin: 10px 0; border-radius: 8px; font-size: 18px;'>
            <strong>{chr(65+i)}.</strong> {option}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Question stats
        stats = session.get_current_question_stats()
        st.markdown(f"""
        <div style='margin-top: 20px; padding: 15px; background: #e8f5e9; border-radius: 8px;'>
        <strong>📊 Response Stats:</strong><br>
        ✅ Answered: {stats['answered']}/{stats['total_players']} • 
        🎯 Correct: {stats['correct']}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Mini leaderboard
        leaderboard = session.get_leaderboard()
        render_mini_leaderboard(leaderboard, top_n=5)
        
        st.markdown("---")
        
        # Auto-refresh
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        
        # Next question button
        if current_q < total_questions - 1:
            if st.button("➡️ Next Question", type="primary", use_container_width=True):
                session.next_question()
                st.rerun()
        else:
            if st.button("🏁 Finish Game", type="primary", use_container_width=True):
                session.status = "finished"
                st.session_state.page = "host_results"
                st.rerun()


def render_host_results():
    """Render final results for host"""
    inject_ui()
    
    if "session_manager" not in st.session_state or "current_session_id" not in st.session_state:
        st.error("Session not found!")
        return
    
    session = st.session_state.session_manager.get_session(st.session_state.current_session_id)
    if not session:
        st.error("Session expired!")
        return
    
    st.markdown("<div class='app-title'>🎉 Game Over! 🎉</div>", unsafe_allow_html=True)
    
    st.balloons()
    
    # Full leaderboard
    leaderboard = session.get_leaderboard()
    render_leaderboard(leaderboard, show_details=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Play Again", type="primary", use_container_width=True):
            st.session_state.session_manager.close_session(session.session_id)
            st.session_state.page = "host_setup"
            st.rerun()
    
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.session_manager.close_session(session.session_id)
            st.session_state.page = "upload"
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
