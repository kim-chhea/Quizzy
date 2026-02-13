import streamlit as st
import time
from ui.theme import inject_ui
from ui.leaderboard import render_leaderboard


def render_player_join():
    """Render the player join screen"""
    inject_ui()
    
    st.markdown("<div class='app-title'>🎮 Join a Quiz Game 🎮</div>", unsafe_allow_html=True)
    
    # Enhanced responsive styles
    st.markdown("""
    <style>
    .join-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 20px 0;
        border: 2px solid rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(10px);
    }
    .join-card h3 {
        color: #667eea;
        margin-bottom: 20px;
        font-size: 28px;
        font-weight: bold;
    }
    .join-card p {
        color: #a1a1aa;
        font-size: 16px;
        line-height: 1.6;
    }
    .pin-input {
        font-size: 24px;
        text-align: center;
        letter-spacing: 5px;
    }
    .how-to-play {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.15) 0%, rgba(220, 38, 38, 0.15) 100%);
        border-radius: 20px;
        padding: 30px;
        border: 2px solid rgba(251, 191, 36, 0.3);
    }
    .how-to-play h4 {
        color: #fbbf24;
        font-size: 22px;
        margin-bottom: 15px;
    }
    .how-to-play ol, .how-to-play ul {
        color: #fafafa;
        font-size: 15px;
        line-height: 2;
    }
    .how-to-play li {
        margin-bottom: 8px;
    }
    @media (max-width: 768px) {
        .join-card {
            padding: 20px;
        }
        .how-to-play {
            padding: 20px;
            margin-top: 20px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if session_id is in query params
    query_params = st.query_params
    session_id_from_url = query_params.get("session", None)
    
    # Back button
    col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
    with col_back1:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.page = "mode_select"
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class='join-card'>
        <h3>📱 Enter Game PIN</h3>
        <p>Enter the 6-digit PIN shown by your host to join the game</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        session_id = st.text_input(
            "🔢 Game PIN",
            value=session_id_from_url if session_id_from_url else "",
            max_chars=6,
            placeholder="123456",
            key="join_session_id",
            help="Ask your host for the 6-digit game PIN"
        )
        
        player_name = st.text_input(
            "👤 Your Name",
            placeholder="Enter your name",
            max_chars=30,
            key="join_player_name",
            help="This name will be shown on the leaderboard"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Join Game", type="primary", use_container_width=True, key="join_btn"):
            if not session_id or len(session_id) != 6:
                st.error("❌ Please enter a valid 6-digit game PIN")
                return
            
            if not player_name or len(player_name.strip()) == 0:
                st.error("❌ Please enter your name")
                return
            
            # Get the global session manager
            from multiplayer.session_manager import get_global_session_manager
            session_manager = get_global_session_manager("v2.0")
            
            session = session_manager.get_session(session_id)
            
            if not session:
                st.error("❌ Game not found! Please check the PIN")
                return
            
            if session.status != "waiting":
                st.error("❌ This game has already started or ended")
                return
            
            # Add player to session
            player_id = session.add_player(player_name.strip())
            st.session_state.player_id = player_id
            st.session_state.player_name = player_name.strip()
            st.session_state.current_session_id = session_id
            st.session_state.page = "player_lobby"
            st.success("✅ Joined successfully!")
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class='how-to-play'>
        <h4>🎯 How to Play</h4>
        <ol>
            <li>📝 Enter the 6-digit PIN</li>
            <li>👤 Type your name</li>
            <li>⏳ Wait for host to start</li>
            <li>⚡ Answer quickly!</li>
            <li>🏆 Climb the leaderboard!</li>
        </ol>
        <br>
        <h4>🏆 Scoring System</h4>
        <ul>
            <li>✅ Correct Answer: <strong>1000 pts</strong></li>
            <li>⚡ Speed Bonus: <strong>up to +500 pts</strong></li>
            <li>❌ Wrong Answer: <strong>0 pts</strong></li>
        </ul>
        <br>
        <p style='text-align: center; font-size: 14px; color: #fbbf24;'>💡 Answer fast to maximize your score!</p>
        </div>
        """, unsafe_allow_html=True)


def render_player_lobby():
    """Render the player lobby waiting screen"""
    inject_ui()
    
    st.markdown("""
    <style>
    .lobby-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 20px 0;
        border: 2px solid rgba(102, 126, 234, 0.3);
        text-align: center;
    }
    .player-badge {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(220, 38, 38, 0.2));
        padding: 20px;
        margin: 10px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid rgba(251, 191, 36, 0.4);
        transition: transform 0.3s ease;
    }
    .player-badge:hover {
        transform: translateY(-5px);
    }
    .player-badge strong {
        font-size: 18px;
        color: #fbbf24;
    }
    .waiting-animation {
        font-size: 48px;
        animation: bounce 1.5s infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    if "current_session_id" not in st.session_state:
        st.error("Session not found!")
        if st.button("← Go Back"):
            st.session_state.page = "player_join"
            st.rerun()
        return
    
    from multiplayer.session_manager import get_global_session_manager
    session_manager = get_global_session_manager("v2.0")
    session = session_manager.get_session(st.session_state.current_session_id)
    if not session:
        st.error("Session expired!")
        if st.button("← Go Back"):
            st.session_state.page = "player_join"
            st.rerun()
        return
    
    # Check if game started
    if session.status == "playing":
        st.session_state.page = "player_game"
        st.rerun()
        return
    
    st.markdown("<div class='app-title'>⏳ Waiting for Host... ⏳</div>", unsafe_allow_html=True)
    
    player_name = st.session_state.get("player_name", "Player")
    
    st.markdown(f"""
    <div class='lobby-card'>
    <h2>Welcome, {player_name}! 👋</h2>
    <p style='font-size: 20px; color: #a1a1aa;'>You've successfully joined the game!</p>
    <div class='waiting-animation'>🎮</div>
    <p style='font-size: 18px; color: #667eea; margin-top: 20px;'>Waiting for the host to start the game...</p>
    <p style='color: #fbbf24; margin-top: 10px;'>Get ready to compete!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='text-align: center; margin: 30px 0;'>
    <h3 style='color: #667eea;'>👥 Players in Lobby ({len(session.players)})</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Show all players in a more attractive grid
    cols = st.columns(3)
    for idx, (player_id, player_data) in enumerate(session.players.items()):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class='player-badge'>
            🎮<br><strong>{player_data['name']}</strong>
            </div>
            """, unsafe_allow_html=True)
    
    # Auto-refresh
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    with col2:
        auto_refresh = st.checkbox("Auto", value=False, help="Auto-refresh every 2s")
        if auto_refresh:
            time.sleep(2)
            st.rerun()
    
    st.markdown("---")
    
    # Leave button
    if st.button("🚪 Leave Game", use_container_width=True):
            if "player_id" in st.session_state:
                player_id = st.session_state.player_id
                if player_id in session.players:
                    del session.players[player_id]
            st.session_state.page = "player_join"
            st.rerun()


def render_player_game():
    """Render the active game view for players"""
    inject_ui()
    
    st.markdown("""
    <style>
    .game-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 20px 0;
        border: 2px solid rgba(102, 126, 234, 0.3);
    }
    .game-card h2 {
        color: #667eea;
        font-size: 28px;
        margin-bottom: 20px;
    }
    .stat-card {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(220, 38, 38, 0.2));
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid rgba(251, 191, 36, 0.4);
        margin-bottom: 15px;
    }
    .stat-card h4 {
        color: #fbbf24;
        margin-bottom: 10px;
    }
    .stat-card p {
        font-size: 18px;
        color: #fafafa;
        margin: 5px 0;
    }
    .rank-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    .rank-badge h3 {
        margin: 0;
        color: white !important;
        font-size: 20px;
    }
    .rank-badge p {
        font-size: 42px;
        margin: 10px 0;
        font-weight: bold;
        color: #fbbf24;
    }
    .answer-submitted {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.2));
        border: 2px solid rgba(16, 185, 129, 0.5);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
    }
    .answer-submitted h3 {
        color: #10b981;
        font-size: 28px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if "current_session_id" not in st.session_state:
        st.error("Session not found!")
        return
    
    from multiplayer.session_manager import get_global_session_manager
    session_manager = get_global_session_manager("v2.0")
    
    session = session_manager.get_session(st.session_state.current_session_id)
    if not session:
        st.error("Session expired!")
        st.write(f"Available sessions: {list(session_manager.sessions.keys())}")
        return
    
    player_id = st.session_state.get("player_id")
    if not player_id or player_id not in session.players:
        st.error("Player not found in session!")
        return
    
    player_data = session.players[player_id]
    
    # Check if player finished all questions
    if player_data.get("finished", False):
        st.session_state.page = "player_results"
        st.rerun()
        return
    
    # Get player's current question
    current_q = player_data.get("current_question", 0)
    question = session.questions[current_q]
    total_questions = len(session.questions)
    
    # Progress bar
    progress = (current_q + 1) / total_questions
    st.progress(progress)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"<h2 style='color: #667eea;'>❓ Question {current_q + 1} of {total_questions}</h2>", unsafe_allow_html=True)
        
        # Display question
        st.markdown(f"""
        <div class='game-card'>
        <h2>{question['question_text']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer options
        with st.form(key=f"answer_form_{current_q}_{player_id}"):
            selected_answer = st.radio(
                "Choose your answer:",
                question['options'],
                key=f"player_answer_{current_q}_{player_id}"
            )
            
            submit_button = st.form_submit_button("✅ Submit Answer", use_container_width=True, type="primary")
            
            if submit_button:
                # Validate inputs before submission
                if not selected_answer:
                    st.error("Please select an answer!")
                elif not player_id:
                    st.error("Player ID not found!")
                elif current_q is None:
                    st.error("Question number invalid!")
                elif not session:
                    st.error("Session not found!")
                elif not hasattr(session, 'submit_answer'):
                    st.error("Session object is invalid!")
                else:
                    try:
                        success = session.submit_answer(player_id, current_q, selected_answer)
                        if success:
                            # Show feedback
                            is_correct = selected_answer == question.get("correct_answer")
                            if is_correct:
                                st.success("🎉 Correct!")
                            else:
                                st.error(f"❌ Wrong! Correct answer: {question.get('correct_answer', 'N/A')}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Failed to submit answer! Please try again.")
                    except Exception as e:
                        st.error(f"Error submitting answer: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())
    
    with col2:
        # Player stats
        st.markdown(f"""
        <div class='stat-card'>
        <h4>📊 Your Stats</h4>
        <p><strong>Score:</strong></p>
        <p style='font-size: 28px; color: #fbbf24;'>{player_data['score']:,}</p>
        <p style='margin-top: 15px;'><strong>Progress:</strong></p>
        <p>{len(player_data['answers'])}/{total_questions}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show current rank
        leaderboard = session.get_leaderboard()
        for player in leaderboard:
            if player["player_id"] == player_id:
                rank = player["rank"]
                total_players = len(leaderboard)
                st.markdown(f"""
                <div class='rank-badge'>
                <h3>🏆 Your Rank</h3>
                <p>{rank}/{total_players}</p>
                </div>
                """, unsafe_allow_html=True)
                break


def render_player_results():
    """Render final results for player with detailed personal stats"""
    inject_ui()
    
    st.markdown("""
    <style>
    .red-envelope {
        background: linear-gradient(135deg, #b91c1c 0%, #dc2626 25%, #ef4444 50%, #dc2626 75%, #b91c1c 100%);
        border-radius: 20px;
        padding: 35px;
        box-shadow: 0 15px 45px rgba(185, 28, 28, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        text-align: center;
        max-width: 550px;
        margin: 20px auto;
        border: 4px solid #fbbf24;
        position: relative;
        overflow: hidden;
    }
    .red-envelope::before {
        content: '福';
        position: absolute;
        top: -30px;
        right: -30px;
        font-size: 180px;
        opacity: 0.05;
        font-weight: bold;
        color: #fbbf24;
    }
    .red-envelope::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: repeating-linear-gradient(
            45deg,
            transparent,
            transparent 10px,
            rgba(251, 191, 36, 0.03) 10px,
            rgba(251, 191, 36, 0.03) 20px
        );
        animation: shimmer 3s linear infinite;
        pointer-events: none;
    }
    @keyframes shimmer {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    .red-envelope-title {
        position: relative;
        z-index: 1;
        color: #fbbf24;
        font-size: 36px;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin: 15px 0;
        letter-spacing: 2px;
    }
    .red-envelope-character {
        position: relative;
        z-index: 1;
        font-size: 90px;
        margin: 10px 0;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
        animation: float-gentle 3s ease-in-out infinite;
    }
    @keyframes float-gentle {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-10px) scale(1.05); }
    }
    .red-envelope-name {
        position: relative;
        z-index: 1;
        color: white;
        font-size: 24px;
        font-weight: 700;
        margin: 15px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }
    .red-envelope-score {
        position: relative;
        z-index: 1;
        font-size: 52px;
        font-weight: 900;
        color: #fbbf24;
        text-shadow: 0 0 20px rgba(251, 191, 36, 0.5), 3px 3px 6px rgba(0,0,0,0.5);
        margin: 20px 0;
        letter-spacing: 3px;
    }
    .red-envelope-message {
        position: relative;
        z-index: 1;
        color: #fef3c7;
        font-size: 16px;
        font-weight: 600;
        margin-top: 15px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .results-card {
        background: linear-gradient(135deg, #b91c1c 0%, #dc2626 50%, #b91c1c 100%);
        border-radius: 18px;
        padding: 30px;
        box-shadow: 0 12px 35px rgba(185, 28, 28, 0.5);
        margin: 20px auto;
        border: 3px solid #fbbf24;
        text-align: center;
        max-width: 500px;
        position: relative;
        overflow: hidden;
    }
    .results-card::before {
        content: '★';
        position: absolute;
        top: 10px;
        left: 10px;
        font-size: 40px;
        opacity: 0.1;
        color: #fbbf24;
    }
    .results-card::after {
        content: '★';
        position: absolute;
        bottom: 10px;
        right: 10px;
        font-size: 40px;
        opacity: 0.1;
        color: #fbbf24;
    }
    .rank-display {
        font-size: 36px;
        font-weight: bold;
        color: #fbbf24;
        margin: 15px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }
    .character-banner {
        font-size: 80px;
        line-height: 1;
        margin: 10px 0;
        animation: bounce 2s infinite;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
        gap: 15px;
        margin: 25px auto;
        max-width: 650px;
    }
    .stat-card {
        background: linear-gradient(135deg, #b91c1c 0%, #dc2626 50%, #b91c1c 100%);
        padding: 18px 15px;
        border-radius: 14px;
        text-align: center;
        border: 3px solid #fbbf24;
        box-shadow: 0 8px 20px rgba(185, 28, 28, 0.4);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: repeating-linear-gradient(
            45deg,
            transparent,
            transparent 8px,
            rgba(251, 191, 36, 0.03) 8px,
            rgba(251, 191, 36, 0.03) 16px
        );
        pointer-events: none;
    }
    .stat-card:hover {
        transform: translateY(-5px);
        border-color: #fde68a;
        box-shadow: 0 12px 30px rgba(185, 28, 28, 0.6);
    }
    .stat-value {
        font-size: 32px;
        font-weight: 900;
        color: #fef3c7;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin: 10px 0;
        position: relative;
        z-index: 1;
    }
    .stat-label {
        color: #fef3c7;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
        position: relative;
        z-index: 1;
    }
    .advice-box {
        background: linear-gradient(135deg, #b91c1c 0%, #dc2626 50%, #b91c1c 100%);
        border: 3px solid #fbbf24;
        border-radius: 14px;
        padding: 25px;
        margin: 25px auto;
        text-align: left;
        max-width: 650px;
        box-shadow: 0 10px 30px rgba(185, 28, 28, 0.5);
    }
    .advice-title {
        color: #fef3c7;
        font-size: 22px;
        font-weight: 900;
        margin-bottom: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }
    .advice-text {
        color: white;
        font-size: 15px;
        line-height: 1.7;
        font-weight: 500;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .detail-item {
        background: linear-gradient(135deg, rgba(185, 28, 28, 0.3) 0%, rgba(220, 38, 38, 0.3) 100%);
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        border-left: 5px solid;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .detail-item:hover {
        background: linear-gradient(135deg, rgba(185, 28, 28, 0.4) 0%, rgba(220, 38, 38, 0.4) 100%);
        transform: translateX(8px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.3);
    }
    .item-correct { 
        border-left-color: #fbbf24;
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.15) 0%, rgba(185, 28, 28, 0.2) 100%);
    }
    .item-incorrect { 
        border-left-color: #7f1d1d;
        background: linear-gradient(135deg, rgba(127, 29, 29, 0.3) 0%, rgba(185, 28, 28, 0.2) 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    if "current_session_id" not in st.session_state:
        st.error("Session not found!")
        return
    
    from multiplayer.session_manager import get_global_session_manager
    session_manager = get_global_session_manager("v2.0")
    session = session_manager.get_session(st.session_state.current_session_id)
    if not session:
        st.error("Session expired!")
        return
    
    player_id = st.session_state.get("player_id")
    
    st.markdown("<div class='app-title'>🎉 Game Over! 🎉</div>", unsafe_allow_html=True)
    
    # Show player's rank
    leaderboard = session.get_leaderboard()
    player_rank = None
    for player in leaderboard:
        if player["player_id"] == player_id:
            player_rank = player
            break
    
    # Get player's detailed data
    player_data = session.players.get(player_id, {})
    player_answers = player_data.get('answers', [])
    total_questions = len(session.questions)
    
    # Calculate detailed statistics
    correct_count = sum(1 for ans in player_answers if ans.get('is_correct', False))
    incorrect_count = len(player_answers) - correct_count
    accuracy = (correct_count / len(player_answers) * 100) if len(player_answers) > 0 else 0
    avg_time = sum(ans.get('time_taken', 0) for ans in player_answers) / len(player_answers) if len(player_answers) > 0 else 0
    total_time = sum(ans.get('time_taken', 0) for ans in player_answers)
    
    # Character selection based on performance
    if player_rank:
        rank = player_rank["rank"]
        
        # Select character and message based on rank
        if rank == 1:
            character = "🐉"  # Dragon
            character_name = "Dragon Spirit"
            message = "You've achieved mastery!"
        elif rank == 2:
            character = "🦅"  # Phoenix
            character_name = "Phoenix Rising"
            message = "Outstanding performance!"
        elif rank == 3:
            character = "🐯"  # Tiger
            character_name = "Tiger Power"
            message = "Excellent work!"
        elif accuracy >= 80:
            character = "🐼"  # Panda
            character_name = "Wise Panda"
            message = "Great accuracy!"
        elif accuracy >= 60:
            character = "🦊"  # Fox
            character_name = "Clever Fox"
            message = "Good progress!"
        else:
            character = "🐇"  # Rabbit
            character_name = "Swift Rabbit"
            message = "Keep going!"
        
        if rank == 1:
            st.balloons()
            st.markdown(f"""
            <div class='red-envelope'>
            <div class='red-envelope-character'>🏆</div>
            <div class='red-envelope-title'>☆ CHAMPION ☆</div>
            <div style='font-size: 20px; font-weight: 600; color: #fef3c7; margin: 10px 0;'>{character_name}</div>
            <div class='red-envelope-name'>{player_rank['name']}</div>
            <div class='red-envelope-score'>{player_rank['score']:,}</div>
            <div class='red-envelope-message'>{message}</div>
            <div style='margin-top: 20px; font-size: 14px; color: #fbbf24; opacity: 0.8;'>✨ PERFECT VICTORY ✨</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            emoji = "🥈" if rank == 2 else "🥉" if rank == 3 else "⭐"
            st.markdown(f"""
            <div class='results-card'>
            <div class='character-banner'>{emoji}</div>
            <h2 style='font-size: 28px; color: #fbbf24; text-shadow: 2px 2px 4px rgba(0,0,0,0.4); margin: 15px 0;'>{character_name}</h2>
            <p style='font-size: 22px; color: white; margin: 15px 0; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{player_rank['name']}</p>
            <div class='rank-display'>Rank #{rank}</div>
            <p style='font-size: 40px; font-weight: bold; color: #fbbf24; margin: 15px 0; text-shadow: 0 0 15px rgba(251, 191, 36, 0.5);'>{player_rank['score']:,}</p>
            <p style='color: #fef3c7; font-size: 16px; margin-top: 15px; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>{message}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Personal Performance Statistics
    st.markdown("""
    <div style='text-align: center; margin: 30px 0 20px 0;'>
    <h2 style='color: #fef3c7; font-size: 30px; font-weight: 900; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); letter-spacing: 2px;'>📊 YOUR PERFORMANCE 📊</h2>
    <p style='color: #fbbf24; font-size: 15px; margin-top: 10px;'>Detailed breakdown of your results</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics Grid - Compact version
    st.markdown(f"""
    <div class='stats-grid'>
        <div class='stat-card'>
            <div style='font-size: 36px;'>✅</div>
            <div class='stat-value'>{correct_count}</div>
            <div class='stat-label'>Correct</div>
        </div>
        <div class='stat-card'>
            <div style='font-size: 36px;'>❌</div>
            <div class='stat-value'>{incorrect_count}</div>
            <div class='stat-label'>Incorrect</div>
        </div>
        <div class='stat-card'>
            <div style='font-size: 36px;'>🎯</div>
            <div class='stat-value'>{accuracy:.1f}%</div>
            <div class='stat-label'>Accuracy</div>
        </div>
        <div class='stat-card'>
            <div style='font-size: 36px;'>⏱️</div>
            <div class='stat-value'>{avg_time:.1f}s</div>
            <div class='stat-label'>Avg Time</div>
        </div>
        <div class='stat-card'>
            <div style='font-size: 36px;'>📈</div>
            <div class='stat-value'>{len(player_answers)}/{total_questions}</div>
            <div class='stat-label'>Done</div>
        </div>
        <div class='stat-card'>
            <div style='font-size: 36px;'>⏰</div>
            <div class='stat-value'>{total_time:.0f}s</div>
            <div class='stat-label'>Total</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Personalized Advice
    advice_parts = []
    
    if accuracy >= 90:
        advice_parts.append("✨ **Excellent!** You're mastering the material! Keep up this outstanding work.")
    elif accuracy >= 75:
        advice_parts.append("💪 **Very Good!** You have a strong understanding. Focus on the questions you missed.")
    elif accuracy >= 60:
        advice_parts.append("💡 **Good Progress!** You're on the right track. Review the incorrect answers to improve.")
    else:
        advice_parts.append("🌱 **Keep Going!** Learning takes practice. Don't give up! Review the material and try again.")
    
    if avg_time < 5:
        advice_parts.append("⚡ **Lightning Fast!** Great reflexes! Make sure to balance speed with accuracy.")
    elif avg_time < 10:
        advice_parts.append("🏃 **Quick Thinker!** Your response time is excellent!")
    elif avg_time > 20:
        advice_parts.append("🧘 **Thoughtful Approach:** You take time to think. Try to build confidence for faster responses.")
    
    if correct_count >= total_questions * 0.8:
        advice_parts.append("🎓 **Learning Master:** Challenge yourself with harder materials!")
    
    st.markdown(f"""
    <div class='advice-box'>
        <div class='advice-title'>💡 PERSONAL ADVICE</div>
        <div class='advice-text'>
        {'<br><br>'.join(advice_parts)}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed Answer Breakdown
    with st.expander("📝 VIEW ALL YOUR ANSWERS", expanded=False):
        st.markdown("<h3 style='color: #fef3c7; font-size: 24px; font-weight: 900; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>QUESTION ANALYSIS</h3>", unsafe_allow_html=True)
        
        for ans in player_answers:
            q_num = ans.get('question_num', 0)
            question = session.questions[q_num] if q_num < len(session.questions) else {}
            is_correct = ans.get('is_correct', False)
            time_taken = ans.get('time_taken', 0)
            points = ans.get('points', 0)
            
            q_text = question.get('question', 'N/A')
            correct_ans = question.get('correct_answer', 'N/A')
            user_ans = ans.get('answer', 'N/A')
            
            status_icon = "✅" if is_correct else "❌"
            status_class = "item-correct" if is_correct else "item-incorrect"
            
            st.markdown(f"""
            <div class='detail-item {status_class}'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                    <strong style='color: #fbbf24; font-size: 16px;'>{status_icon} Question {q_num + 1}</strong>
                    <div>
                        <span style='background: rgba(102, 126, 234, 0.3); padding: 3px 10px; border-radius: 10px; margin-right: 6px; font-size: 13px;'>
                            ⏱️ {time_taken:.1f}s
                        </span>
                        <span style='background: rgba(251, 191, 36, 0.3); padding: 3px 10px; border-radius: 10px; font-size: 13px;'>
                            💰 {points:,}
                        </span>
                    </div>
                </div>
                <div style='color: #e5e5e5; margin: 6px 0; font-size: 15px;'><strong>Q:</strong> {q_text}</div>
                <div style='color: {'#10b981' if is_correct else '#ef4444'}; margin: 4px 0; font-size: 14px;'>
                    <strong>Your Answer:</strong> {user_ans}
                </div>
                {f"<div style='color: #10b981; margin: 4px 0; font-size: 14px;'><strong>✅ Correct:</strong> {correct_ans}</div>" if not is_correct else "<div style='color: #10b981; margin: 4px 0; font-size: 14px;'>✨ Perfect!</div>"}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Full leaderboard
    render_leaderboard(leaderboard, show_details=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Back to Home", use_container_width=True, key="home_btn"):
            st.session_state.page = "mode_select"
            st.rerun()
    with col2:
        if st.button("🔄 Play Again", use_container_width=True, key="again_btn"):
            st.session_state.page = "player_join"
            st.rerun()


def render_player_view():
    """Main router for player views"""
    page = st.session_state.get("page", "player_join")
    
    if page == "player_join":
        render_player_join()
    elif page == "player_lobby":
        render_player_lobby()
    elif page == "player_game":
        render_player_game()
    elif page == "player_results":
        render_player_results()
    else:
        render_player_join()
