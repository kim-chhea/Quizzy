import streamlit as st
import pandas as pd
import time
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
            session_manager = get_global_session_manager("v2.0")
            
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
    session_manager = get_global_session_manager("v2.0")
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
            # Display players in a grid using st.columns
            cols = st.columns(3)
            for idx, (player_id, player_data) in enumerate(session.players.items()):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(220, 38, 38, 0.2)); 
                                padding: 20px; margin: 10px 0; border-radius: 15px; text-align: center;
                                border: 2px solid rgba(251, 191, 36, 0.4);'>
                    <div style='font-size: 32px;'>🎮</div>
                    <strong style='color: #fbbf24; font-size: 18px;'>{player_data['name']}</strong>
                    </div>
                    """, unsafe_allow_html=True)
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
            session_manager = get_global_session_manager("v2.0")
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
    session_manager = get_global_session_manager("v2.0")
    session = session_manager.get_session(st.session_state.current_session_id)
    if not session:
        st.error("Session expired!")
        return
    
    # Check if all players finished
    if session.status == "finished":
        st.session_state.page = "host_results"
        st.rerun()
        return
    
    total_questions = len(session.questions)
    
    st.markdown("<div class='app-title'>📊 Live Dashboard 📊</div>", unsafe_allow_html=True)
    
    # Enhanced dashboard styles
    st.markdown("""
    <style>
    .dashboard-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 20px 0;
        border: 2px solid rgba(102, 126, 234, 0.3);
    }
    .player-progress {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.15), rgba(220, 38, 38, 0.15));
        padding: 20px;
        margin: 15px 0;
        border-radius: 15px;
        border: 2px solid rgba(251, 191, 36, 0.3);
        transition: all 0.3s ease;
    }
    .player-progress:hover {
        transform: translateX(5px);
        border-color: rgba(251, 191, 36, 0.6);
    }
    .progress-bar-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 30px;
        overflow: hidden;
        margin: 10px 0;
    }
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    .stat-badge {
        display: inline-block;
        padding: 8px 16px;
        margin: 5px;
        border-radius: 20px;
        font-weight: bold;
    }
    .badge-score {
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        color: white;
    }
    .badge-question {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }
    .badge-finished {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
    }
    .summary-box {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.2));
        border-radius: 15px;
        border: 2px solid rgba(16, 185, 129, 0.4);
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    
    total_players = len(session.players)
    finished_players = sum(1 for p in session.players.values() if p.get("finished", False))
    avg_progress = sum(p.get("current_question", 0) for p in session.players.values()) / max(total_players, 1)
    avg_score = sum(p["score"] for p in session.players.values()) / max(total_players, 1)
    
    with col1:
        st.markdown(f"""
        <div class='summary-box'>
        <h3 style='color: #667eea; margin: 0;'>👥 Players</h3>
        <p style='font-size: 32px; font-weight: bold; color: #fbbf24; margin: 10px 0;'>{total_players}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='summary-box'>
        <h3 style='color: #667eea; margin: 0;'>✅ Finished</h3>
        <p style='font-size: 32px; font-weight: bold; color: #10b981; margin: 10px 0;'>{finished_players}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='summary-box'>
        <h3 style='color: #667eea; margin: 0;'>📊 Avg Progress</h3>
        <p style='font-size: 32px; font-weight: bold; color: #667eea; margin: 10px 0;'>{avg_progress:.1f}/{total_questions}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='summary-box'>
        <h3 style='color: #667eea; margin: 0;'>🏆 Avg Score</h3>
        <p style='font-size: 32px; font-weight: bold; color: #fbbf24; margin: 10px 0;'>{avg_score:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Player progress detail
    st.markdown("<h2 style='color: #667eea;'>👥 Player Progress</h2>", unsafe_allow_html=True)
    
    # Sort players by progress (furthest first)
    sorted_players = sorted(
        session.players.items(),
        key=lambda x: (x[1].get("current_question", 0), x[1]["score"]),
        reverse=True
    )
    
    for player_id, player_data in sorted_players:
        player_progress = player_data.get("current_question", 0)
        player_finished = player_data.get("finished", False)
        progress_pct = (player_progress / total_questions) * 100
        
        if player_finished:
            progress_display = f"Completed All {total_questions} Questions!"
            progress_pct = 100
            status_badge = "<span class='stat-badge badge-finished'>✅ FINISHED</span>"
        else:
            progress_display = f"On Question {player_progress + 1} of {total_questions}"
            status_badge = f"<span class='stat-badge badge-question'>📝 Q{player_progress + 1}</span>"
        
        st.markdown(f"""
        <div class='player-progress'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
            <h3 style='color: #fbbf24; margin: 0;'>🎮 {player_data['name']}</h3>
            <div>
                {status_badge}
                <span class='stat-badge badge-score'>💰 {player_data['score']:,} pts</span>
            </div>
        </div>
        <div class='progress-bar-container'>
            <div class='progress-bar-fill' style='width: {progress_pct}%;'>
                {progress_pct:.0f}%
            </div>
        </div>
        <p style='color: #a1a1aa; margin: 10px 0 0 0;'>{progress_display} • {len(player_data['answers'])} answered</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Leaderboard
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### 🏆 Current Leaderboard")
        leaderboard = session.get_leaderboard()
        render_mini_leaderboard(leaderboard, top_n=10)
    
    with col_right:
        st.markdown("### ⚙️ Controls")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Refresh", use_container_width=True, key="refresh_dashboard"):
                st.rerun()
        
        with col_b:
            auto_refresh = st.checkbox("Auto", value=False, help="Auto-refresh every 3s", key="auto_refresh")
        
        if auto_refresh:
            time.sleep(3)
            st.rerun()
        
        st.markdown("---")
        
        # End game button
        if finished_players == total_players and total_players > 0:
            st.success("🎉 All players finished!")
            if st.button("🏁 End Game & View Results", type="primary", use_container_width=True, key="end_game_btn"):
                session.status = "finished"
                st.session_state.page = "host_results"
                st.rerun()
        else:
            st.info(f"⏳ {total_players - finished_players} player(s) still playing...")
            if st.button("🏁 Force End Game", use_container_width=True, key="force_end_btn"):
                session.status = "finished"
                st.session_state.page = "host_results"
                st.rerun()


def render_host_results():
    """Render final results for host"""
    inject_ui()
    
    if "current_session_id" not in st.session_state:
        st.error("Session not found!")
        return
    
    from multiplayer.session_manager import get_global_session_manager
    session_manager = get_global_session_manager("v2.0")
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
            session_manager.close_session(session.session_id)
            st.session_state.page = "host_setup"
            st.rerun()
    
    with col2:
        if st.button("📊 View Again", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("🏠 Home", use_container_width=True):
            session_manager.close_session(session.session_id)
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
