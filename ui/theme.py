import streamlit as st
import streamlit.components.v1 as components


def inject_ui():
    # Modern UI CSS with Chinese Vibe
    css = """
    <style>
      :root{
        --bg: #0f0f0f;
        --card: #1a1a1a;
        --muted: #a1a1aa;
        --accent: #dc2626; /* Chinese red */
        --gold: #fbbf24; /* Gold */
        --text: #fafafa;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --chinese-red: #dc2626;
        --chinese-gold: #fbbf24;
        --chinese-black: #000000;
      }
      /* Global */
      body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: var(--text); background: var(--bg); }
      .stApp { background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 50%, #2a1810 100%); min-height: 100vh; }
      h1 { text-align: center; font-weight: 700; background: linear-gradient(135deg, var(--chinese-red), var(--chinese-gold)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }

      /* Containers */
      .app-header { margin: 10px 0 18px; }
      .quiz-container { max-width: 1000px; margin: 8px auto 24px; }
      .question-card { padding: 20px; border-radius: 16px; background: linear-gradient(135deg, var(--card) 0%, rgba(26,26,26,0.8) 100%); box-shadow: 0 8px 32px rgba(0,0,0,0.3); margin-bottom: 18px; border: 1px solid rgba(255,255,255,0.05); transition: transform 0.3s ease, box-shadow 0.3s ease; }
      .question-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(0,0,0,0.4); }
      .question-title { font-size: 20px; font-weight: 700; margin-bottom: 10px; color: var(--text); }
      .progress-area { color: var(--muted); font-size: 15px; }

      /* Header / steps */
      .app-title { font-size: 32px; font-weight: 800; color: var(--text); text-align:center; margin-bottom: 6px }
      .step-progress { width: 80%; height: 10px; background: rgba(255,255,255,0.04); border-radius: 8px; margin: 10px auto 18px; overflow: hidden }
      .step-progress > .bar { height: 100%; width: 30%; background: linear-gradient(90deg,var(--chinese-gold),var(--chinese-red)); border-radius: 8px }

      /* Upload card */
      .upload-card { 
        padding: 30px; 
        border-radius: 16px; 
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08)); 
        border: 2px solid rgba(102, 126, 234, 0.2);
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        margin: 20px 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
      }
      .upload-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.3);
      }
      .upload-drop { 
        border: 3px dashed rgba(102, 126, 234, 0.3); 
        padding: 30px; 
        border-radius: 12px; 
        text-align: center; 
        color: var(--muted);
        background: rgba(102, 126, 234, 0.05);
        transition: all 0.3s ease;
      }
      .upload-drop:hover {
        border-color: rgba(102, 126, 234, 0.6);
        background: rgba(102, 126, 234, 0.1);
      }
      .upload-drop .hint { margin-top: 10px; color: var(--muted); }
      .chinese-welcome { text-align: center; font-size: 20px; color: var(--chinese-gold); margin-bottom: 20px; font-weight: 600; }

      /* Preview table look */
      .stDataFrame table { border-collapse: collapse; }

      /* Input fields */
      .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: rgba(26, 26, 26, 0.8) !important;
        color: var(--text) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
      }
      .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: rgba(102, 126, 234, 0.8) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        outline: none !important;
      }
      .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: var(--text) !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        margin-bottom: 8px !important;
      }

      /* Large start button */
      .start-btn > button {
        background: linear-gradient(180deg,var(--chinese-red),var(--chinese-gold));
        padding: 14px 22px;
        font-size: 18px;
        border-radius: 12px;
      }

      /* Buttons (primary styled Chinese red/gold) */
      .stButton>button, button, .stFormSubmitButton button {
        background: linear-gradient(135deg, var(--chinese-red), var(--chinese-gold)) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 14px 24px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(220, 38, 38, 0.4) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
        font-size: 16px !important;
      }
      .stButton>button:hover, button:hover, .stFormSubmitButton button:hover { 
        transform: translateY(-3px) !important; 
        box-shadow: 0 10px 28px rgba(220, 38, 38, 0.5) !important;
        background: linear-gradient(135deg, var(--chinese-gold), var(--chinese-red)) !important;
      }
      .stButton>button:active, button:active { 
        transform: translateY(0px) !important; 
      }

      /* Processing state: show spinner and prevent further clicks */
      .stButton>button.processing, button.processing {
        cursor: wait;
        opacity: 0.9;
        pointer-events: none;
      }
      .stButton>button.processing::after, button.processing::after {
        content: '';
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 3px solid rgba(255,255,255,0.3);
        border-top-color: transparent;
        border-radius: 50%;
        margin-left: 10px;
        vertical-align: middle;
        animation: spin 0.8s linear infinite;
      }
      @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

      /* Radio/options spacing */
      .stRadio>div, .stRadio>label { 
        margin-bottom: 10px; 
      }
      .stRadio > div[role="radiogroup"] > label {
        background: rgba(102, 126, 234, 0.1);
        padding: 15px;
        border-radius: 10px;
        border: 2px solid rgba(102, 126, 234, 0.2);
        margin: 8px 0;
        cursor: pointer;
        transition: all 0.3s ease;
      }
      .stRadio > div[role="radiogroup"] > label:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.5);
        transform: translateX(5px);
      }

      /* Larger readable text */
      .stText, .stMarkdown { font-size: 16px; }

      /* Responsive design */
      @media (max-width: 1024px) {
        .app-title { font-size: 28px; }
        .quiz-container { max-width: 90%; }
        .question-card { padding: 18px; }
        .upload-card { padding: 24px; }
        .stButton>button, button, .stFormSubmitButton button { padding: 12px 20px; font-size: 16px; }
      }

      @media (max-width: 768px) {
        .app-title { font-size: 24px; }
        .quiz-container { max-width: 95%; margin: 4px auto 16px; }
        .question-card { padding: 16px; margin-bottom: 16px; }
        .question-title { font-size: 18px; margin-bottom: 8px; }
        .upload-card { padding: 20px; }
        .upload-drop { padding: 16px; }
        .step-progress { width: 90%; }
        .stButton>button, button, .stFormSubmitButton button { padding: 10px 16px; font-size: 14px; }
        .stTextInput input, .stNumberInput input, .stSelectbox select { padding: 10px; font-size: 14px; }
        .stRadio > div[role="radiogroup"] > label { padding: 12px; }
      }

      @media (max-width: 480px) {
        .app-title { font-size: 20px; }
        .question-card { padding: 12px; }
        .upload-card { padding: 16px; }
        .stButton>button, button, .stFormSubmitButton button { padding: 8px 12px; font-size: 13px; }
        .stTextInput input, .stNumberInput input, .stSelectbox select { padding: 8px; font-size: 13px; }
        .stText, .stMarkdown { font-size: 14px; }
        .stRadio > div[role="radiogroup"] > label { padding: 10px; font-size: 13px; }
      }

    </style>
    """

    # Robust JS: forward first pointerdown to a click and set a temporary "processing" state on the button
    js = """
    <script>
    (function(){
      try{
        function findButton(el){
          var wrapper = el.closest('.stButton');
          if(wrapper) return wrapper.querySelector('button');
          var b = el.closest('button');
          return b;
        }

        document.addEventListener('pointerdown', function(e){
          try{
            var native = findButton(e.target);
            if(!native) return;
            // If already processing, prevent extra clicks
            if(native.dataset.__processing) {
              e.preventDefault();
              return;
            }
            // Mark processing state and trigger a click (first click)
            native.dataset.__processing = '1';
            native.classList.add('processing');
            // For accessibility also set aria-disabled
            native.setAttribute('aria-disabled','true');

            // Fire the click (this triggers Streamlit form submit or button handler)
            native.click();

            // Ensure the UI re-enables after a delay in case Streamlit doesn't rerender quickly
            setTimeout(function(){
              try{
                delete native.dataset.__processing;
                native.classList.remove('processing');
                native.removeAttribute('aria-disabled');
              }catch(_){ }
            }, 2000);
          }catch(err){}
        }, true);

        // Also listen for keydown Enter to trigger same behavior
        document.addEventListener('keydown', function(e){
          if(e.key === 'Enter'){
            var native = findButton(document.activeElement || e.target);
            if(!native) return;
            if(native.dataset.__processing) { e.preventDefault(); return; }
            native.dataset.__processing = '1'; native.classList.add('processing'); native.setAttribute('aria-disabled','true'); native.click();
            setTimeout(function(){ try{ delete native.dataset.__processing; native.classList.remove('processing'); native.removeAttribute('aria-disabled'); }catch(_){ } }, 2000);
          }
        }, true);
      }catch(e){}
    })();
    </script>
    """

    st.markdown(css, unsafe_allow_html=True)
    components.html(js, height=0)
