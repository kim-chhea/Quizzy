# Quizzy Multiplayer Mode - Kahoot-Style Features

## 🎮 New Features

Quizzy now supports real-time multiplayer quiz games similar to Kahoot! Host games, share QR codes, and compete with friends on a live leaderboard.

## 🌟 Key Features

### Host Mode
- **Create Game Sessions**: Set up custom quiz games with your dataset
- **QR Code Generation**: Share games easily with automatically generated QR codes
- **6-Digit PIN**: Simple game codes for quick joining
- **Live Player Management**: See who joins in real-time
- **Game Control**: Manage question progression at your own pace
- **Real-time Stats**: View response rates and correct answer percentages

### Player Mode
- **Quick Join**: Enter 6-digit PIN or scan QR code
- **Custom Names**: Players register with their own names
- **Competitive Scoring**: Points based on correctness and speed
- **Live Rankings**: See your rank update in real-time
- **Speed Bonus**: Answer faster to earn up to 500 bonus points per question

### Leaderboard
- **Animated Rankings**: Beautiful gradient design with rank badges
- **Gold/Silver/Bronze**: Special styling for top 3 players
- **Detailed Stats**: View accuracy, correct answers, and total points
- **Real-time Updates**: Rankings update as players answer

## 🎯 How to Use

### Starting a Multiplayer Game

1. **Launch Quizzy**
   ```bash
   streamlit run app.py
   ```

2. **Select Mode**
   - Choose between:
     - 📚 **Solo Practice**: Traditional single-player mode
     - 🎮 **Host Multiplayer**: Create and host a game
     - 👥 **Join Game**: Join an existing game

3. **Host Setup** (if hosting)
   - Upload or use sample dataset
   - Configure game settings:
     - Number of questions (3-50)
     - Quiz mode (Chinese→English, English→Chinese, Pinyin→Chinese)
     - Time per question (5-60 seconds)
   - Click "Create Game Session"

4. **Share Game**
   - Display the QR code for players to scan
   - Share the 6-digit PIN verbally or via chat
   - Wait for players to join

5. **Start Game**
   - See players join in the lobby
   - Click "Start Game" when ready
   - Control question progression with "Next Question"

6. **View Results**
   - See final leaderboard with detailed stats
   - Option to play again or return home

### Joining a Game

1. **Launch Quizzy**
   ```bash
   streamlit run app.py
   ```

2. **Select "Join Game"**
   - Enter the 6-digit game PIN
   - Type your player name
   - Click "Join Game"

3. **Wait in Lobby**
   - See other players joining
   - Wait for host to start

4. **Answer Questions**
   - Read each question carefully
   - Select your answer quickly for bonus points
   - Submit your answer
   - See your current rank

5. **Final Results**
   - View your final rank
   - See complete leaderboard
   - Celebrate if you won! 🎉

## 🏆 Scoring System

### Point Breakdown
- **Correct Answer**: 1,000 base points
- **Speed Bonus**: Up to 500 additional points
  - Full bonus for answers within 2 seconds
  - Decreases linearly based on time taken
  - Formula: `500 - (time_taken × 50)`
- **Wrong Answer**: 0 points

### Leaderboard Ranking
Players are ranked by:
1. **Total Score** (primary, descending)
2. **Join Time** (tiebreaker, ascending - earlier joins rank higher)

## 📱 Mobile-Friendly

All multiplayer features are fully responsive and work great on:
- Desktop computers
- Tablets
- Smartphones

Players can join from any device with a web browser!

## 🔧 Technical Details

### Architecture

```
multiplayer/
├── session_manager.py    # Game session and player management
├── qr_generator.py        # QR code generation utilities
ui/
├── host_view.py           # Host interface (setup, lobby, game, results)
├── player_view.py         # Player interface (join, lobby, game, results)
├── leaderboard.py         # Leaderboard rendering components
```

### Session Management
- Sessions stored in-memory using `SessionManager`
- Each session has a unique 6-digit PIN
- Automatic cleanup of old sessions (24 hours)
- Player data includes name, score, and answer history

### Real-time Updates
- Uses Streamlit's `st.rerun()` for pseudo-real-time updates
- Manual refresh buttons for mobile compatibility
- Auto-refresh on game state changes

### QR Code Generation
- Uses `qrcode` library with PIL backend
- Generates base64-encoded PNG images
- Embedded directly in HTML for instant display
- Includes full join URL with session ID

## 🚀 Advanced Usage

### Custom Datasets
Upload CSV or Excel files with these columns:
- `chinese`: Chinese characters
- `pinyin`: Pinyin pronunciation
- `english`: English translation
- `pos`: Part of speech (optional)
- `semantic_type`: Category (optional)

### Game Configuration
- **Questions**: 3-50 questions per game
- **Time Limit**: 5-60 seconds per question
- **Modes**: 3 quiz modes available
- **Dataset**: Use sample or upload custom

## 🐛 Troubleshooting

### Players Can't Join
- Verify the 6-digit PIN is correct
- Ensure game is still in "waiting" status
- Check network connectivity

### QR Code Not Working
- Use manual PIN entry as alternative
- Ensure camera has permission to scan
- Try refreshing the page

### Session Lost
- Sessions expire after 24 hours
- Browser refresh may clear session state
- Host should note the session ID

## 📊 Best Practices

### For Hosts
1. Test with sample data before live games
2. Start with fewer questions (10-15) for engagement
3. Keep time limits reasonable (15-20 seconds)
4. Wait for all players before starting
5. Use "Next Question" to control pace

### For Players
1. Join early to secure a good spot
2. Answer quickly for speed bonuses
3. Read questions carefully
4. Stay engaged throughout the game
5. Have fun and learn!

## 🎨 Customization

### Styling
- Modify `ui/leaderboard.py` for custom leaderboard designs
- Edit `ui/theme.py` for global styling changes
- Adjust colors in CSS gradients for your brand

### Scoring
- Update point values in `multiplayer/session_manager.py`
- Modify speed bonus formula for different difficulty
- Add penalties or multipliers as needed

## 🔒 Privacy & Security

- No user data is stored permanently
- Sessions are memory-only (no database)
- Session IDs are randomly generated
- No authentication required
- No personal information collected

## 📝 License

Same license as the main Quizzy project.

---

**Enjoy your multiplayer quiz games! 🎉**

For issues or feature requests, please open an issue on GitHub.
