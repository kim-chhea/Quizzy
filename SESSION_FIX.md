# Session Manager Fix - Game PIN Not Found Issue

## Problem
Players were getting "❌ Game not found! Please check the PIN" error when trying to join games because:
- Each user had their own `SessionManager` instance stored in `st.session_state`
- `st.session_state` is **per-user**, not global
- Host's sessions were only visible to the host, not to players

## Solution
Implemented a **global session manager** using Streamlit's `@st.cache_resource` decorator:

### Changes Made:

#### 1. `/workspaces/Quizzy/multiplayer/session_manager.py`
- Added `@st.cache_resource` decorator to create a singleton SessionManager
- Added `get_global_session_manager()` function that returns the same instance for all users

```python
@st.cache_resource
def get_global_session_manager():
    """Get the global session manager singleton shared across all users"""
    return SessionManager()
```

#### 2. `/workspaces/Quizzy/ui/host_view.py`
- Replaced `st.session_state.session_manager` with `get_global_session_manager()`
- Updated in: `render_host_setup()`, `render_host_lobby()`, `render_host_game()`, `render_host_results()`

#### 3. `/workspaces/Quizzy/ui/player_view.py`
- Replaced `st.session_state.session_manager` with `get_global_session_manager()`
- Updated in: `render_player_join()`, `render_player_lobby()`, `render_player_game()`, `render_player_results()`

## How It Works Now

1. **Host creates a game**:
   - Calls `get_global_session_manager().create_session()`
   - Session is stored in the global manager
   - Gets a 6-digit PIN

2. **Player joins a game**:
   - Calls `get_global_session_manager().get_session(pin)`
   - Retrieves the session from the same global manager
   - Successfully joins the game

3. **Session sharing**:
   - All users (host and players) share the same SessionManager instance
   - Sessions created by the host are visible to all players
   - Real-time multiplayer works correctly

## Testing
To test the fix:
1. Start the app: `streamlit run app.py`
2. Open one browser tab as Host, create a game
3. Open another tab/browser as Player, use the PIN to join
4. Player should successfully join the lobby
5. Host can start the game and both see the questions

## Technical Details
- `@st.cache_resource` creates a singleton that persists across all user sessions
- Unlike `st.session_state` (per-user) or `@st.cache_data` (immutable), `@st.cache_resource` is perfect for stateful, shared objects
- The SessionManager's mutable state (sessions dict) is now properly shared
