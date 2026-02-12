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
            
            # Initialize session manager if not exists
            if "session_manager" not in st.session_state:
                from multiplayer.session_manager import SessionManager
                st.session_state.session_manager = SessionManager()
            
            session = st.session_state.session_manager.get_session(session_id)
            
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
    
    if "session_manager" not in st.session_state or "current_session_id" not in st.session_state:
        st.error("Session not found!")
        if st.button("← Go Back"):
            st.session_state.page = "player_join"
            st.rerun()
        return
    
    session = st.session_state.session_manager.get_session(st.session_state.current_session_id)
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
    
    # Leave button
    with col2:
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
    
    if "session_manager" not in st.session_state or "current_session_id" not in st.session_state:
        st.error("Session not found!")
        return
    
    session = st.session_state.session_manager.get_session(st.session_state.current_session_id)
    if not session:
        st.error("Session expired!")
        return
    
    player_id = st.session_state.get("player_id")
    if not player_id or player_id not in session.players:
        st.error("Player not found in session!")
        return
    
    # Check if game finished
    if session.status == "finished":
        st.session_state.page = "player_results"
        st.rerun()
        return
    
    player_data = session.players[player_id]
    current_q = session.current_question
    question = session.questions[current_q]
    total_questions = len(session.questions)
    
    # Progress bar
    progress = (current_q + 1) / total_questions
    st.progress(progress)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"<h2 style='color: #667eea;'>❓ Question {current_q + 1} of {total_questions}</h2>", unsafe_allow_html=True)
        
        # Check if player already answered
        already_answered = player_id in session.answers_submitted
        
        if already_answered:
            answer_data = session.answers_submitted[player_id]
            st.markdown(f"""
            <div class='answer-submitted'>
            <h3>✅ Answer Submitted!</h3>
            <p style='font-size: 20px; color: #fafafa; margin: 15px 0;'>Your answer: <strong style='color: #fbbf24;'>{answer_data['answer']}</strong></p>
            <p style='font-size: 18px; color: #a1a1aa;'>Time: <strong>{answer_data['time_taken']:.2f}s</strong></p>
            <p style='font-size: 16px; color: #667eea; margin-top: 20px;'>⏳ Waiting for other players...</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Display question
            st.markdown(f"""
            <div class='game-card'>
            <h2>{question['question_text']}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Answer options
            with st.form(key=f"answer_form_{current_q}"):
                selected_answer = st.radio(
                    "Choose your answer:",
                    question['options'],
                    key=f"player_answer_{current_q}"
                )
                
                submit_button = st.form_submit_button("✅ Submit Answer", use_container_width=True, type="primary")
                
                if submit_button:
                    session.submit_answer(player_id, selected_answer)
                    st.rerun()
    
    with col2:
        # Player stats
        st.markdown(f"""
        <div class='stat-card'>
        <h4>📊 Your Stats</h4>
        <p><strong>Score:</strong></p>
        <p style='font-size: 28px; color: #fbbf24;'>{player_data['score']:,}</p>
        <p style='margin-top: 15px;'><strong>Answered:</strong></p>
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
        
        # Auto-refresh if waiting
        if player_id in session.answers_submitted:
            st.markdown("---")
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()


def render_player_results():
    """Render final results for player"""
    inject_ui()
    
    st.markdown("""
    <style>
    .results-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 20px 0;
        border: 2px solid rgba(102, 126, 234, 0.3);
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
    </style>
    """, unsafe_allow_html=True)
    
    if "session_manager" not in st.session_state or "current_session_id" not in st.session_state:
        st.error("Session not found!")
        return
    
    session = st.session_state.session_manager.get_session(st.session_state.current_session_id)
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
    
    if player_rank:
        rank = player_rank["rank"]
        if rank == 1:
            st.balloons()
            st.markdown(f"""
            <div class='winner-card'>
            <h1>🏆 WINNER! 🏆</h1>
            <p>Congratulations, <strong>{player_rank['name']}</strong>!</p>
            <div class='score-display'>{player_rank['score']:,} pts</div>
            <p>You are the champion! 🎊</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            emoji = "🥈" if rank == 2 else "🥉" if rank == 3 else "⭐"
            st.markdown(f"""
            <div class='results-card'>
            <h2 style='font-size: 36px; color: #667eea;'>Great Job! {emoji}</h2>
            <p style='font-size: 22px; color: #fafafa; margin: 20px 0;'><strong>{player_rank['name']}</strong></p>
            <div class='rank-display'>Rank #{rank}</div>
            <p style='font-size: 42px; font-weight: bold; color: #fbbf24; margin: 20px 0;'>{player_rank['score']:,} pts</p>
            <p style='color: #a1a1aa; font-size: 16px;'>Keep practicing to reach the top!</p>
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
