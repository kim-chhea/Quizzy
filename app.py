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
except (ModuleNotFoundError, ImportError) as e:

    def _missing_ui(*args, _exc=e, **kwargs):
        st.error(
            "Missing UI modules. Create ui/upload.py, ui/quiz_view.py, ui/results_view.py (see README)."
        )
        st.exception(_exc)

    render_upload = render_quiz = render_results = _missing_ui
except Exception as e:

    def _import_error(*args, _exc=e, **kwargs):
        st.error("Error importing UI modules.")
        st.exception(_exc)

    render_upload = render_quiz = render_results = _import_error

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "upload"
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


def main():
    st.title("Quizzy - Your Personal Quiz Generator")

    if st.session_state.page == "upload":
        render_upload()
    elif st.session_state.page == "quiz":
        render_quiz()
    elif st.session_state.page == "results":
        render_results()


if __name__ == "__main__":
    main()
