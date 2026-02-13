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
    
    st.markdown("<div class='app-title'>🐉 Quizzy - Quiz Generator 🏮</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .mode-card {
        background: linear-gradient(135deg, #b91c1c 0%, #dc2626 50%, #b91c1c 100%);
        border-radius: 18px;
        padding: 35px 25px;
        text-align: center;
        min-height: 400px;
        border: 4px solid #fbbf24;
        box-shadow: 0 15px 40px rgba(185, 28, 28, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
    }
    .mode-card::before {
        content: '福';
        position: absolute;
        top: -20px;
        right: -20px;
        font-size: 120px;
        opacity: 0.05;
        font-weight: bold;
        color: #fbbf24;
        transition: all 0.3s ease;
    }
    .mode-card:hover::before {
        opacity: 0.1;
        transform: rotate(10deg);
    }
    .mode-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(185, 28, 28, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: #fde68a;
    }
    .mode-card h2 {
        font-size: 75px;
        margin: 20px 0;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
        animation: gentle-bounce 2s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }
    @keyframes gentle-bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    .mode-card h3 {
        color: #fef3c7;
        font-size: 28px;
        margin-bottom: 10px;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        position: relative;
        z-index: 1;
        letter-spacing: 1px;
    }
    .mode-card p {
        color: #fef3c7;
        font-size: 15px;
        line-height: 1.5;
        margin-bottom: 20px;
        font-weight: 500;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    .mode-card ul {
        text-align: left;
        color: white;
        font-size: 14px;
        line-height: 1.9;
        list-style-type: none;
        padding: 0 10px;
        margin: 15px 0;
        position: relative;
        z-index: 1;
    }
    .mode-card ul li {
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .mode-card ul li:before {
        content: "⭐ ";
        font-size: 14px;
        margin-right: 8px;
    }
    </style>
    
    <div style='text-align: center; padding: 30px 20px;'>
    <p style='font-size: 30px; color: #fbbf24; font-weight: 900; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); letter-spacing: 2px;'>Choose Your Journey</p>
    <p style='font-size: 16px; color: #a1a1aa; font-weight: 500;'>Select your game mode and start learning!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div class='mode-card'>
        <div>
        <h2>�</h2>
        <div class='chinese-text'>独自练习 Solo Practice</div>
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
        <h2>🐉</h2>
        <div class='chinese-text'>主持多人 Host Multiplayer</div>
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
        <h2>🦊</h2>
        <div class='chinese-text'>加入游戏 Join Game</div>
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
