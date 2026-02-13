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
    
    st.success(f"✅ Session found! Type: {type(session)}")
    
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
    .results-card {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.15) 0%, rgba(251, 191, 36, 0.15) 100%);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 20px 0;
        border: 3px solid rgba(251, 191, 36, 0.4);
        text-align: center;
    }
    .winner-card {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white;
        border-radius: 20px;
        padding: 50px;
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.5);
        text-align: center;
        animation: glow 2s infinite;
        border: 3px solid #FFD700;
    }
    @keyframes glow {
        0%, 100% { box-shadow: 0 15px 40px rgba(255, 215, 0, 0.5); }
        50% { box-shadow: 0 20px 50px rgba(255, 215, 0, 0.8); }
    }
    .winner-card h1 {
        color: white !important;
        font-size: 48px;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .winner-card p {
        font-size: 24px;
        color: white;
        margin: 15px 0;
    }
    .score-display {
        font-size: 56px;
        font-weight: bold;
        color: white;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
        margin: 20px 0;
    }
    .rank-display {
        font-size: 48px;
        font-weight: bold;
        color: #fbbf24;
        margin: 20px 0;
    }
    .character-banner {
        font-size: 120px;
        line-height: 1;
        margin: 20px 0;
        animation: bounce 2s infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 15px;
        margin: 25px 0;
    }
    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid rgba(251, 191, 36, 0.3);
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-5px);
        border-color: rgba(251, 191, 36, 0.6);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    .stat-value {
        font-size: 36px;
        font-weight: bold;
        color: #fbbf24;
        margin: 10px 0;
    }
    .stat-label {
        color: #a1a1aa;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .advice-box {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.2), rgba(251, 191, 36, 0.2));
        border: 2px solid rgba(251, 191, 36, 0.5);
        border-radius: 15px;
        padding: 25px;
        margin: 25px 0;
        text-align: left;
    }
    .advice-title {
        color: #fbbf24;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .advice-text {
        color: #fafafa;
        font-size: 16px;
        line-height: 1.8;
    }
    .detail-item {
        background: rgba(255, 255, 255, 0.03);
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        border-left: 4px solid;
        transition: all 0.3s ease;
    }
    .detail-item:hover {
        background: rgba(255, 255, 255, 0.06);
        transform: translateX(5px);
    }
    .item-correct { border-left-color: #10b981; }
    .item-incorrect { border-left-color: #ef4444; }
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
        
        # Select character based on rank and performance
        if rank == 1:
            character = "🐉"  # Dragon - ultimate champion
            character_name = "龙 (Lóng) - Dragon Spirit"
            message = "You've achieved mastery! The dragon's wisdom flows through you!"
        elif rank == 2:
            character = "🦅"  # Phoenix
            character_name = "凤凰 (Fènghuáng) - Phoenix Rising"
            message = "Outstanding! Like the phoenix, you're destined for greatness!"
        elif rank == 3:
            character = "🐯"  # Tiger
            character_name = "虎 (Hǔ) - Tiger Power"
            message = "Excellent work! The tiger's strength is with you!"
        elif accuracy >= 80:
            character = "🐼"  # Panda
            character_name = "熊猫 (Xióngmāo) - Wise Panda"
            message = "Great accuracy! The panda's wisdom guides your path!"
        elif accuracy >= 60:
            character = "🦊"  # Fox
            character_name = "狐狸 (Húlí) - Clever Fox"
            message = "Good progress! The fox's cleverness shines in you!"
        else:
            character = "🐇"  # Rabbit
            character_name = "兔 (Tù) - Swift Rabbit"
            message = "Keep going! The rabbit's speed and determination will lead you forward!"
        
        if rank == 1:
            st.balloons()
            st.markdown(f"""
            <div class='winner-card'>
            <div class='character-banner'>{character}</div>
            <h1>🏆 冒险者之冠 🏆</h1>
            <p style='font-size: 20px; opacity: 0.9;'>{character_name}</p>
            <p style='font-size: 26px; font-weight: bold; margin: 20px 0;'>{player_rank['name']}</p>
            <div class='score-display'>{player_rank['score']:,} 分</div>
            <p style='font-size: 18px; margin-top: 20px;'>{message}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            emoji = "🥈" if rank == 2 else "🥉" if rank == 3 else "⭐"
            st.markdown(f"""
            <div class='results-card'>
            <div class='character-banner'>{character}</div>
            <h2 style='font-size: 36px; color: #fbbf24;'>{emoji} {character_name} {emoji}</h2>
            <p style='font-size: 24px; color: #fafafa; margin: 20px 0; font-weight: bold;'>{player_rank['name']}</p>
            <div class='rank-display'># {rank}</div>
            <p style='font-size: 42px; font-weight: bold; color: #fbbf24; margin: 20px 0;'>{player_rank['score']:,} 点</p>
            <p style='color: #e5e5e5; font-size: 18px; margin-top: 20px;'>{message}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Personal Performance Statistics
    st.markdown("""
    <div style='text-align: center; margin: 30px 0;'>
    <h2 style='color: #fbbf24; font-size: 32px;'>📊 你的成绩分析 Your Performance</h2>
    <p style='color: #a1a1aa; font-size: 16px;'>Detailed breakdown of your quiz results</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics Grid
    st.markdown(f"""
    <div class='stats-grid'>
        <div class='stat-card'>
            <div style='font-size: 48px;'>✅</div>
            <div class='stat-value'>{correct_count}</div>
            <div class='stat-label'>Correct</div>
        </div>
        <div class='stat-card'>
            <div style='font-size: 48px;'>❌</div>
            <div class='stat-value'>{incorrect_count}</div>
            <div class='stat-label'>Incorrect</div>
        </div>
        <div class='stat-card'>
            <div style='font-size: 48px;'>🎯</div>
            <div class='stat-value'>{accuracy:.1f}%</div>
            <div class='stat-label'>Accuracy</div>
        </div>
        <div class='stat-card'>
            <div style='font-size: 48px;'>⏱️</div>
            <div class='stat-value'>{avg_time:.1f}s</div>
            <div class='stat-label'>Avg Time</div>
        </div>
        <div class='stat-card'>
            <div style='font-size: 48px;'>📈</div>
            <div class='stat-value'>{len(player_answers)}/{total_questions}</div>
            <div class='stat-label'>Completed</div>
        </div>
        <div class='stat-card'>
            <div style='font-size: 48px;'>⏰</div>
            <div class='stat-value'>{total_time:.0f}s</div>
            <div class='stat-label'>Total Time</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Personalized Advice
    advice_parts = []
    
    if accuracy >= 90:
        advice_parts.append("✨ **卓越表现 Excellent!** You're mastering the material! Keep up this outstanding work.")
    elif accuracy >= 75:
        advice_parts.append("💪 **很好 Very Good!** You have a strong understanding. Focus on the questions you missed.")
    elif accuracy >= 60:
        advice_parts.append("💡 **不错 Good Progress!** You're on the right track. Review the incorrect answers to improve.")
    else:
        advice_parts.append("🌱 **努力 Keep Going!** Learning takes practice. Don't give up! Review the material and try again.")
    
    if avg_time < 5:
        advice_parts.append("⚡ **闪电速度 Lightning Fast!** Great reflexes! Make sure to balance speed with accuracy.")
    elif avg_time < 10:
        advice_parts.append("🏃 **速度好 Quick Thinker!** Your response time is excellent!")
    elif avg_time > 20:
        advice_parts.append("🧘 **仔细思考 Thoughtful Approach:** You take time to think. Try to build confidence for faster responses.")
    
    if correct_count >= total_questions * 0.8:
        advice_parts.append("🎓 **学习能手 Learning Master:** Challenge yourself with harder materials!")
    
    st.markdown(f"""
    <div class='advice-box'>
        <div class='advice-title'>🦉 个性化建议 Personal Advice for You</div>
        <div class='advice-text'>
        {'<br><br>'.join(advice_parts)}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed Answer Breakdown
    with st.expander("📝 查看所有答案 View All Your Answers", expanded=False):
        st.markdown("<h3 style='color: #fbbf24;'>Question by Question Analysis</h3>", unsafe_allow_html=True)
        
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
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
                    <strong style='color: #fbbf24; font-size: 18px;'>{status_icon} Question {q_num + 1}</strong>
                    <div>
                        <span style='background: rgba(102, 126, 234, 0.3); padding: 4px 12px; border-radius: 12px; margin-right: 8px;'>
                            ⏱️ {time_taken:.1f}s
                        </span>
                        <span style='background: rgba(251, 191, 36, 0.3); padding: 4px 12px; border-radius: 12px;'>
                            💰 {points:,} pts
                        </span>
                    </div>
                </div>
                <div style='color: #e5e5e5; margin: 8px 0; font-size: 16px;'><strong>Q:</strong> {q_text}</div>
                <div style='color: {'#10b981' if is_correct else '#ef4444'}; margin: 4px 0; font-size: 15px;'>
                    <strong>你的答案 Your Answer:</strong> {user_ans}
                </div>
                {f"<div style='color: #10b981; margin: 4px 0; font-size: 15px;'><strong>✅ 正确答案 Correct Answer:</strong> {correct_ans}</div>" if not is_correct else "<div style='color: #10b981; margin: 4px 0; font-size: 15px;'>✨ Perfect! 完美!</div>"}
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
