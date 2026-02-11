import streamlit as st


def render_leaderboard(leaderboard: list, show_details: bool = True):
    """
    Render a leaderboard display
    
    Args:
        leaderboard: List of player data sorted by rank
        show_details: Whether to show detailed stats
    """
    if not leaderboard:
        st.info("No players yet!")
        return
    
    st.markdown("""
    <style>
    .leaderboard-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    .leaderboard-title {
        color: white;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .player-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        display: flex;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .player-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .rank-badge {
        font-size: 24px;
        font-weight: bold;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
    }
    .rank-1 {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white;
        animation: pulse 2s infinite;
    }
    .rank-2 {
        background: linear-gradient(135deg, #C0C0C0 0%, #808080 100%);
        color: white;
    }
    .rank-3 {
        background: linear-gradient(135deg, #CD7F32 0%, #8B4513 100%);
        color: white;
    }
    .rank-other {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .player-info {
        flex: 1;
    }
    .player-name {
        font-size: 20px;
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
    }
    .player-score {
        font-size: 24px;
        font-weight: bold;
        color: #667eea;
        margin-left: auto;
    }
    .stats-row {
        font-size: 14px;
        color: #666;
        margin-top: 5px;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="leaderboard-container">', unsafe_allow_html=True)
    st.markdown('<div class="leaderboard-title">🏆 Leaderboard 🏆</div>', unsafe_allow_html=True)
    
    for player in leaderboard:
        rank = player["rank"]
        name = player["name"]
        score = player["score"]
        
        # Determine rank badge class
        if rank == 1:
            rank_class = "rank-1"
            rank_emoji = "🥇"
        elif rank == 2:
            rank_class = "rank-2"
            rank_emoji = "🥈"
        elif rank == 3:
            rank_class = "rank-3"
            rank_emoji = "🥉"
        else:
            rank_class = "rank-other"
            rank_emoji = f"#{rank}"
        
        # Build stats if requested
        stats_html = ""
        if show_details and "answers" in player:
            total_questions = len(player["answers"])
            correct_answers = sum(1 for a in player["answers"] if a["is_correct"])
            accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
            stats_html = f'<div class="stats-row">✅ {correct_answers}/{total_questions} correct • 📊 {accuracy:.0f}% accuracy</div>'
        
        st.markdown(f'''
        <div class="player-card">
            <div class="rank-badge {rank_class}">{rank_emoji}</div>
            <div class="player-info">
                <div class="player-name">{name}</div>
                {stats_html}
            </div>
            <div class="player-score">{score:,} pts</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_mini_leaderboard(leaderboard: list, top_n: int = 5):
    """
    Render a compact leaderboard showing top N players
    
    Args:
        leaderboard: List of player data sorted by rank
        top_n: Number of top players to show
    """
    if not leaderboard:
        return
    
    st.markdown("### 🏆 Top Players")
    
    top_players = leaderboard[:top_n]
    
    for player in top_players:
        rank = player["rank"]
        name = player["name"]
        score = player["score"]
        
        if rank == 1:
            emoji = "🥇"
        elif rank == 2:
            emoji = "🥈"
        elif rank == 3:
            emoji = "🥉"
        else:
            emoji = "⭐"
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"{emoji} **{name}**")
        with col2:
            st.markdown(f"**{score:,}** pts")
