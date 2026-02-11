import streamlit as st
import time
from ui.theme import inject_ui
from ui.leaderboard import render_leaderboard


def render_player_join():
    """Render the player join screen"""
    inject_ui()
    
    st.markdown("<div class='app-title'>🎮 Join a Quiz Game 🎮</div>", unsafe_allow_html=True)
    
    # Responsive styles
    st.markdown("""
    <style>
    .join-card {
        background: white;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    .pin-input {
        font-size: 24px;
        text-align: center;
        letter-spacing: 5px;
    }
    @media (max-width: 768px) {
        .join-card {
            padding: 20px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if session_id is in query params
    query_params = st.query_params
    session_id_from_url = query_params.get("session", None)
    
    # Back button
    if st.button("← Back to Mode Select"):
        st.session_state.page = "mode_select"
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class='join-card'>
        <h3 style='color: #667eea;'>📱 Enter Game PIN</h3>
        <p>Enter the 6-digit PIN shown by your host</p>
        </div>
        """, unsafe_allow_html=True)
        
        session_id = st.text_input(
            "Game PIN",
            value=session_id_from_url if session_id_from_url else "",
            max_chars=6,
            placeholder="123456",
            key="join_session_id",
            help="Ask your host for the 6-digit game PIN"
        )
        
        player_name = st.text_input(
            "Your Name",
            placeholder="Enter your name",
            max_chars=30,
            key="join_player_name",
            help="This name will be shown on the leaderboard"
        )
        
        st.markdown("---")
        
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
        <div class='join-card'>
        <h4>🎯 How to Play</h4>
        <ol>
            <li>Enter the 6-digit PIN</li>
            <li>Type your name</li>
            <li>Wait for host</li>
            <li>Answer fast!</li>
            <li>Win prizes!</li>
        </ol>
        <br>
        <h4>🏆 Scoring</h4>
        <ul>
            <li>✅ Correct: 1000 pts</li>
            <li>⚡ Speed bonus: +500 pts</li>
            <li>❌ Wrong: 0 pts</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)


def render_player_lobby():
    """Render the player lobby waiting screen"""
    inject_ui()
    
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
    <div class='upload-card' style='text-align: center;'>
    <h2>Welcome, {player_name}! 👋</h2>
    <p style='font-size: 18px;'>You've successfully joined the game!</p>
    <p style='font-size: 48px;'>🎮</p>
    <p>Waiting for the host to start the game...</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='upload-card'>
    <h3>👥 Players in Lobby ({len(session.players)})</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Show all players
    cols = st.columns(3)
    for idx, (player_id, player_data) in enumerate(session.players.items()):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style='background: #f0f2f6; padding: 15px; margin: 5px; border-radius: 8px; text-align: center;'>
            🎮<br><strong>{player_data['name']}</strong>
            </div>
            """, unsafe_allow_html=True)
    
    # Auto-refresh
    st.markdown("---")
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()
    
    # Leave button
    if st.button("🚪 Leave Game"):
        if "player_id" in st.session_state:
            player_id = st.session_state.player_id
            if player_id in session.players:
                del session.players[player_id]
        st.session_state.page = "player_join"
        st.rerun()


def render_player_game():
    """Render the active game view for players"""
    inject_ui()
    
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
        st.markdown(f"### Question {current_q + 1} of {total_questions}")
        
        # Check if player already answered
        already_answered = player_id in session.answers_submitted
        
        if already_answered:
            answer_data = session.answers_submitted[player_id]
            st.markdown(f"""
            <div class='upload-card' style='background: #e8f5e9;'>
            <h3>✅ Answer Submitted!</h3>
            <p>Your answer: <strong>{answer_data['answer']}</strong></p>
            <p>Time: <strong>{answer_data['time_taken']:.2f}s</strong></p>
            <p>Waiting for other players...</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Display question
            st.markdown(f"""
            <div class='upload-card'>
            <h2 style='color: #667eea;'>{question['question_text']}</h2>
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
        <div class='upload-card'>
        <h4>Your Stats</h4>
        <p><strong>Score:</strong> {player_data['score']:,} pts</p>
        <p><strong>Answered:</strong> {len(player_data['answers'])}/{total_questions}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show current rank
        leaderboard = session.get_leaderboard()
        for player in leaderboard:
            if player["player_id"] == player_id:
                rank = player["rank"]
                total_players = len(leaderboard)
                st.markdown(f"""
                <div style='background: #667eea; color: white; padding: 15px; border-radius: 8px; text-align: center;'>
                <h3 style='margin: 0; color: white;'>Rank</h3>
                <p style='font-size: 36px; margin: 10px 0; font-weight: bold;'>{rank}/{total_players}</p>
                </div>
                """, unsafe_allow_html=True)
                break
        
        # Auto-refresh if waiting
        if player_id in session.answers_submitted:
            st.markdown("---")
            if st.button("🔄 Refresh"):
                st.rerun()


def render_player_results():
    """Render final results for player"""
    inject_ui()
    
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
            <div class='upload-card' style='background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: white; text-align: center;'>
            <h1 style='color: white;'>🏆 WINNER! 🏆</h1>
            <p style='font-size: 24px;'>Congratulations, {player_rank['name']}!</p>
            <p style='font-size: 48px; font-weight: bold;'>{player_rank['score']:,} pts</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            emoji = "🥈" if rank == 2 else "🥉" if rank == 3 else "⭐"
            st.markdown(f"""
            <div class='upload-card' style='text-align: center;'>
            <h2>Great Job! {emoji}</h2>
            <p style='font-size: 24px;'>You ranked <strong>#{rank}</strong></p>
            <p style='font-size: 36px; font-weight: bold; color: #667eea;'>{player_rank['score']:,} pts</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Full leaderboard
    render_leaderboard(leaderboard, show_details=True)
    
    st.markdown("---")
    
    if st.button("🏠 Back to Home", use_container_width=True):
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
