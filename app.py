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
    <div style='text-align: center; padding: 20px;'>
    <p style='font-size: 20px;'>Choose your game mode</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='upload-card' style='text-align: center; min-height: 300px;'>
        <h2>📚</h2>
        <h3>Solo Practice</h3>
        <p>Practice at your own pace with customizable quizzes</p>
        <br>
        <ul style='text-align: left;'>
        <li>Self-paced learning</li>
        <li>Review mistakes</li>
        <li>Track progress</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎯 Start Solo", use_container_width=True, type="primary"):
            st.session_state.game_mode = "single"
            st.session_state.page = "upload"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class='upload-card' style='text-align: center; min-height: 300px;'>
        <h2>🎮</h2>
        <h3>Host Multiplayer</h3>
        <p>Create a game session and compete with friends!</p>
        <br>
        <ul style='text-align: left;'>
        <li>Real-time competition</li>
        <li>QR code joining</li>
        <li>Live leaderboard</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Host Game", use_container_width=True, type="primary"):
            st.session_state.game_mode = "host"
            st.session_state.page = "upload"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class='upload-card' style='text-align: center; min-height: 300px;'>
        <h2>👥</h2>
        <h3>Join Game</h3>
        <p>Join an existing game with a code or QR scan</p>
        <br>
        <ul style='text-align: left;'>
        <li>Quick join with PIN</li>
        <li>Compete for top rank</li>
        <li>Earn bonus points</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📱 Join Game", use_container_width=True, type="primary"):
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
