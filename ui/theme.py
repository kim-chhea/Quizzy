import streamlit as st
import streamlit.components.v1 as components


def inject_ui():
    # Modern UI CSS with Chinese Vibe - Enhanced for teens and adults
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
        --dragon-purple: #8b5cf6;
        --phoenix-orange: #f97316;
      }
      
      /* Global with Chinese patterns */
      body { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans SC', sans-serif; 
        color: var(--text); 
        background: var(--bg);
      }
      
      .stApp { 
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 50%, #2a1810 100%);
        min-height: 100vh;
        position: relative;
      }
      
      /* Add subtle Chinese pattern overlay */
      .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
          repeating-linear-gradient(0deg, transparent, transparent 50px, rgba(220, 38, 38, 0.03) 50px, rgba(220, 38, 38, 0.03) 51px),
          repeating-linear-gradient(90deg, transparent, transparent 50px, rgba(251, 191, 36, 0.03) 50px, rgba(251, 191, 36, 0.03) 51px);
        pointer-events: none;
        z-index: 0;
      }
      
      /* Elegant Chinese gradient text */
      h1 { 
        text-align: center; 
        font-weight: 700; 
        background: linear-gradient(135deg, var(--chinese-red), var(--chinese-gold), var(--phoenix-orange)); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        background-clip: text;
        position: relative;
        z-index: 1;
      }

      /* Containers with Chinese lantern inspired design */
      .app-header { margin: 10px 0 18px; }
      .quiz-container { max-width: 1000px; margin: 8px auto 24px; position: relative; z-index: 1; }
      
      .question-card { 
        padding: 20px; 
        border-radius: 16px; 
        background: linear-gradient(135deg, var(--card) 0%, rgba(26,26,26,0.8) 100%); 
        box-shadow: 0 8px 32px rgba(220, 38, 38, 0.2), 0 0 20px rgba(251, 191, 36, 0.1); 
        margin-bottom: 18px; 
        border: 2px solid rgba(251, 191, 36, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
      }
      
      .question-card::before {
        content: '龙';
        position: absolute;
        top: -20px;
        right: -20px;
        font-size: 120px;
        opacity: 0.03;
        font-weight: bold;
        color: var(--chinese-gold);
        pointer-events: none;
      }
      
      .question-card:hover { 
        transform: translateY(-4px); 
        box-shadow: 0 12px 40px rgba(220, 38, 38, 0.3), 0 0 30px rgba(251, 191, 36, 0.2); 
        border-color: rgba(251, 191, 36, 0.4);
      }
      
      .question-title { font-size: 20px; font-weight: 700; margin-bottom: 10px; color: var(--text); }
      .progress-area { color: var(--muted); font-size: 15px; }

      /* Header / steps with dragon motif */
      .app-title { 
        font-size: 32px; 
        font-weight: 800; 
        color: var(--text); 
        text-align:center; 
        margin-bottom: 6px;
        text-shadow: 0 0 20px rgba(251, 191, 36, 0.3);
      }
      
      .step-progress { 
        width: 80%; 
        height: 10px; 
        background: rgba(255,255,255,0.04); 
        border-radius: 8px; 
        margin: 10px auto 18px; 
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
      }
      
      .step-progress > .bar { 
        height: 100%; 
        width: 30%; 
        background: linear-gradient(90deg, var(--chinese-red), var(--chinese-gold), var(--phoenix-orange)); 
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(251, 191, 36, 0.5);
        animation: shimmer 2s infinite;
      }
      
      @keyframes shimmer {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
      }

      /* Upload card with Chinese paper texture */
      .upload-card { 
        padding: 30px; 
        border-radius: 16px; 
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.12), rgba(251, 191, 36, 0.12)); 
        border: 2px solid rgba(251, 191, 36, 0.3);
        box-shadow: 0 8px 24px rgba(220, 38, 38, 0.2);
        margin: 20px 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
      }
      
      .upload-card::after {
        content: '学';
        position: absolute;
        bottom: 10px;
        right: 20px;
        font-size: 80px;
        opacity: 0.05;
        font-weight: bold;
        color: var(--chinese-gold);
      }
      
      .upload-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(220, 38, 38, 0.3);
        border-color: rgba(251, 191, 36, 0.5);
      }
      
      .upload-drop { 
        border: 3px dashed rgba(251, 191, 36, 0.4); 
        padding: 30px; 
        border-radius: 12px; 
        text-align: center; 
        color: var(--muted);
        background: rgba(220, 38, 38, 0.05);
        transition: all 0.3s ease;
      }
      
      .upload-drop:hover {
        border-color: rgba(251, 191, 36, 0.7);
        background: rgba(251, 191, 36, 0.1);
      }
      
      .upload-drop .hint { margin-top: 10px; color: var(--muted); }
      .chinese-welcome { 
        text-align: center; 
        font-size: 20px; 
        color: var(--chinese-gold); 
        margin-bottom: 20px; 
        font-weight: 600;
        text-shadow: 0 0 10px rgba(251, 191, 36, 0.3);
      }

      /* Preview table look */
      .stDataFrame table { border-collapse: collapse; }

      /* Input fields with Chinese flair */
      .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: rgba(26, 26, 26, 0.8) !important;
        color: var(--text) !important;
        border: 2px solid rgba(251, 191, 36, 0.3) !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
      }
      
      .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: rgba(251, 191, 36, 0.8) !important;
        box-shadow: 0 0 0 3px rgba(251, 191, 36, 0.2), 0 0 15px rgba(251, 191, 36, 0.3) !important;
        outline: none !important;
      }
      
      .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: var(--text) !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        margin-bottom: 8px !important;
      }

      /* Large start button with dragon energy */
      .start-btn > button {
        background: linear-gradient(135deg, var(--chinese-red), var(--chinese-gold), var(--phoenix-orange));
        padding: 14px 22px;
        font-size: 18px;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(220, 38, 38, 0.4);
      }

      /* Buttons with Chinese imperial style */
      .stButton>button, button, .stFormSubmitButton button {
        background: linear-gradient(135deg, var(--chinese-red), var(--chinese-gold)) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 14px 24px !important;
        font-weight: 600 !important;
        border: 2px solid rgba(251, 191, 36, 0.3) !important;
        box-shadow: 0 6px 20px rgba(220, 38, 38, 0.4), 0 0 15px rgba(251, 191, 36, 0.2) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
        font-size: 16px !important;
      }
      
      .stButton>button::before, button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
      }
      
      .stButton>button:hover::before, button:hover::before {
        left: 100%;
      }
      
      .stButton>button:hover, button:hover, .stFormSubmitButton button:hover { 
        transform: translateY(-3px) !important; 
        box-shadow: 0 10px 28px rgba(220, 38, 38, 0.5), 0 0 25px rgba(251, 191, 36, 0.3) !important;
        background: linear-gradient(135deg, var(--chinese-gold), var(--phoenix-orange), var(--chinese-red)) !important;
      }
      
      .stButton>button:active, button:active { 
        transform: translateY(0px) !important; 
      }

      /* Processing state */
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
        border-top-color: white;
        border-radius: 50%;
        margin-left: 10px;
        vertical-align: middle;
        animation: spin 0.8s linear infinite;
      }
      
      @keyframes spin { 
        from { transform: rotate(0deg); } 
        to { transform: rotate(360deg); } 
      }

      /* Radio/options with lantern style */
      .stRadio>div, .stRadio>label { 
        margin-bottom: 10px; 
      }
      .stRadio > div[role="radiogroup"] > label {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.1), rgba(251, 191, 36, 0.1));
        padding: 15px;
        border-radius: 10px;
        border: 2px solid rgba(251, 191, 36, 0.3);
        margin: 8px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
      }
      
      .stRadio > div[role="radiogroup"] > label::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(251, 191, 36, 0.2), transparent);
        transition: left 0.5s;
      }
      
      .stRadio > div[role="radiogroup"] > label:hover::before {
        left: 100%;
      }
      
      .stRadio > div[role="radiogroup"] > label:hover {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.2), rgba(251, 191, 36, 0.2));
        border-color: rgba(251, 191, 36, 0.6);
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(251, 191, 36, 0.2);
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
