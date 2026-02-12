import streamlit as st

# call set_page_config early (before other st.* calls)
st.set_page_config(
    page_title="Quizzy - Your Personal Quiz Generator",
    page_icon=":memo:",
    layout="wide",
)

try:
    from ui.upload import render_upload
    from ui.quiz_view import render_quiz
    from ui.results_view import render_results
    from ui.host_view import render_host_view
    from ui.player_view import render_player_view
except (ModuleNotFoundError, ImportError) as e:

    def _missing_ui(*args, _exc=e, **kwargs):
        st.error(
            "Missing UI modules. Create ui/upload.py, ui/quiz_view.py, ui/results_view.py (see README)."
        )
        st.exception(_exc)

    render_upload = render_quiz = render_results = render_host_view = render_player_view = _missing_ui
except Exception as e:

    def _import_error(*args, _exc=e, **kwargs):
        st.error("Error importing UI modules.")
        st.exception(_exc)

    render_upload = render_quiz = render_results = render_host_view = render_player_view = _import_error

# Initialize session state
if "page" not in st.session_state:
    # Check query params for multiplayer join
    query_params = st.query_params
    if "mode" in query_params and query_params.get("mode") == "join":
        st.session_state.page = "player_join"
    else:
        st.session_state.page = "mode_select"
if "df" not in st.session_state:
    st.session_state.df = None
if "quiz_settings" not in st.session_state:
    st.session_state.quiz_settings = {"num_questions": 10, "mode": "chinese_to_english"}
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = {
        "questions": [],
        "current_q": 0,
        "score": 0,
        "history": [],
    }
if "game_mode" not in st.session_state:
    st.session_state.game_mode = "single"  # single, host, player


def render_mode_select():
    """Render the mode selection screen"""
    from ui.theme import inject_ui
    inject_ui()
    
    st.markdown("<div class='app-title'>🌟 Quizzy - Your Personal Quiz Generator 🎯</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .mode-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        min-height: 380px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: all 0.4s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .mode-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        border-color: rgba(102, 126, 234, 0.6);
    }
    .mode-card h2 {
        font-size: 64px;
        margin: 20px 0;
    }
    .mode-card h3 {
        color: #667eea;
        font-size: 26px;
        margin-bottom: 15px;
    }
    .mode-card p {
        color: #a1a1aa;
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    .mode-card ul {
        text-align: left;
        color: #fafafa;
        font-size: 15px;
        line-height: 2;
        list-style-type: none;
        padding: 0;
    }
    .mode-card ul li:before {
        content: "✓ ";
        color: #fbbf24;
        font-weight: bold;
        margin-right: 8px;
    }
    </style>
    
    <div style='text-align: center; padding: 30px 20px;'>
    <p style='font-size: 24px; color: #fbbf24; font-weight: 600;'>Choose Your Game Mode</p>
    <p style='font-size: 16px; color: #a1a1aa;'>Select how you want to play and start learning!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div class='mode-card'>
        <div>
        <h2>📚</h2>
        <h3>Solo Practice</h3>
        <p>Practice at your own pace with customizable quizzes</p>
        <ul>
        <li>Self-paced learning</li>
        <li>Review mistakes</li>
        <li>Track progress</li>
        <li>No time pressure</li>
        </ul>
        </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎯 Start Solo", use_container_width=True, type="primary", key="solo_btn"):
            st.session_state.game_mode = "single"
            st.session_state.page = "upload"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class='mode-card'>
        <div>
        <h2>🎮</h2>
        <h3>Host Multiplayer</h3>
        <p>Create a game session and compete with friends!</p>
        <ul>
        <li>Real-time competition</li>
        <li>QR code joining</li>
        <li>Live leaderboard</li>
        <li>Control the game</li>
        </ul>
        </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Host Game", use_container_width=True, type="primary", key="host_btn"):
            st.session_state.game_mode = "host"
            st.session_state.page = "upload"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class='mode-card'>
        <div>
        <h2>👥</h2>
        <h3>Join Game</h3>
        <p>Join an existing game with a PIN and compete!</p>
        <ul>
        <li>Quick join with PIN</li>
        <li>Compete for top rank</li>
        <li>Earn bonus points</li>
        <li>Speed matters!</li>
        </ul>
        </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📱 Join Game", use_container_width=True, type="primary", key="join_btn"):
            st.session_state.game_mode = "player"
            st.session_state.page = "player_join"
            st.rerun()


def main():
    # Mode selection
    if st.session_state.page == "mode_select":
        render_mode_select()
        return
    
    # Multiplayer routes
    if st.session_state.page in ["player_join", "player_lobby", "player_game", "player_results"]:
        render_player_view()
        return
    
    if st.session_state.page in ["host_setup", "host_lobby", "host_game", "host_results"]:
        render_host_view()
        return
    
    # Single player routes
    st.title("Quizzy - Your Personal Quiz Generator")

    if st.session_state.page == "upload":
        # Show back button if in host mode
        if st.session_state.game_mode == "host":
            if st.button("← Back to Mode Select"):
                st.session_state.page = "mode_select"
                st.rerun()
            render_host_view()
        else:
            if st.button("← Back to Mode Select"):
                st.session_state.page = "mode_select"
                st.rerun()
            render_upload()
    elif st.session_state.page == "quiz":
        render_quiz()
    elif st.session_state.page == "results":
        render_results()


if __name__ == "__main__":
    main()
