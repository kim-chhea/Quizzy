# 🎮 Quizzy Quick Reference Card

## 🚀 Quick Start
```bash
# Install and run
pip install -r requirements.txt
streamlit run app.py
```

## 📋 Three Modes

### 📚 Solo Practice
- Individual study at own pace
- Track personal progress
- Review mistakes

### 🎮 Host Multiplayer
- Create game sessions
- Share QR/PIN codes
- Control question flow
- View live rankings

### 👥 Join Game
- Enter 6-digit PIN
- Compete with others
- Earn speed bonuses
- See live rankings

## 📊 Dataset Format
**Required Columns:**
- `chinese` - Chinese characters
- `pinyin` - Pronunciation  
- `english` - Translation

**Optional Columns:**
- `example_sentence`
- `pos` (part of speech)
- `semantic_type` (category)

## 🏆 Scoring
- ✅ Correct: **1,000 points**
- ⚡ Speed bonus: **up to 500 points**
- ❌ Wrong: **0 points**
- 🎯 Max per question: **1,500 points**

## 🎯 Quiz Modes
1. 📖 Chinese → English
2. 🔤 English → Chinese
3. 🗣️ Pinyin → Chinese

## ⚙️ Host Settings
- **Questions**: 3-50
- **Time limit**: 5-60 seconds
- **Mode**: 3 options
- **Dataset**: Sample or custom

## 📱 Joining Games

### Method 1: QR Code
1. Open Quizzy
2. Click "Join Game"
3. Scan QR code

### Method 2: Manual PIN
1. Open Quizzy
2. Click "Join Game"
3. Enter 6-digit PIN
4. Type your name

## 🎮 Game Flow

### Host
1. Setup → 2. Lobby → 3. Game → 4. Results

### Player
1. Join → 2. Lobby → 3. Game → 4. Results

## 💡 Pro Tips

### For Hosts
- ✅ Test with sample data first
- ✅ Use 10-15 questions for quick games
- ✅ Set 20-30 sec time limits
- ✅ Share PIN clearly multiple times
- ✅ Wait for all players before starting

### For Players
- ✅ Join early
- ✅ Answer quickly for bonuses
- ✅ Read questions carefully
- ✅ Stay focused throughout
- ✅ Have fun!

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't join game | Verify PIN is correct |
| QR not working | Use manual PIN entry |
| Session expired | Host creates new game |
| Slow loading | Reduce question count |
| No sample data | Check requirements.txt |

## 📞 Support

- 📖 Full docs: `MULTIPLAYER_README.md`
- 🔧 Issues: Check file validation
- 💾 Dataset: Verify column names
- 🌐 Network: Same network for best results

## 🎨 Responsive Design
- 💻 **Desktop**: Full features
- 📱 **Tablet**: Optimized layout
- 📱 **Mobile**: Touch-friendly

## ⌨️ Keyboard Shortcuts
- `Ctrl+R` / `Cmd+R`: Refresh page
- `Tab`: Navigate between inputs
- `Enter`: Submit forms
- `Esc`: Close modals

## 🔒 Privacy
- ❌ No data stored permanently
- ❌ No registration required
- ❌ No personal info collected
- ✅ Memory-only sessions

## 📈 Recommended Setup

### Classroom (20 students)
- Questions: 15-20
- Time: 20 seconds
- Mode: Chinese → English

### Study Group (3-5 people)
- Questions: 20-30
- Time: 30 seconds
- Mode: All modes

### Quick Game (2-10 people)
- Questions: 5-10
- Time: 15 seconds
- Mode: Any

---

**Version**: 2.0 with Multiplayer
**Last Updated**: February 2026
**License**: Same as main project

Happy Quizzing! 🎉
