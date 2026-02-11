import random
import string
import time
from datetime import datetime
from typing import Dict, List, Optional


class GameSession:
    """Represents a multiplayer quiz game session"""
    
    def __init__(self, host_name: str, quiz_settings: dict, questions: list):
        self.session_id = self._generate_session_id()
        self.host_name = host_name
        self.quiz_settings = quiz_settings
        self.questions = questions
        self.players: Dict[str, dict] = {}  # player_id -> player_data
        self.current_question = 0
        self.status = "waiting"  # waiting, playing, finished
        self.created_at = datetime.now()
        self.question_start_time = None
        self.answers_submitted: Dict[str, dict] = {}  # player_id -> answer_data
        
    def _generate_session_id(self) -> str:
        """Generate a unique 6-character session ID"""
        return ''.join(random.choices(string.digits, k=6))
    
    def add_player(self, player_name: str) -> str:
        """Add a player to the session and return their player_id"""
        player_id = f"player_{len(self.players) + 1}_{int(time.time())}"
        self.players[player_id] = {
            "name": player_name,
            "score": 0,
            "answers": [],
            "joined_at": datetime.now(),
        }
        return player_id
    
    def start_game(self):
        """Start the game"""
        self.status = "playing"
        self.current_question = 0
        self.question_start_time = time.time()
        self.answers_submitted = {}
    
    def next_question(self):
        """Move to the next question"""
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.question_start_time = time.time()
            self.answers_submitted = {}
            return True
        else:
            self.status = "finished"
            return False
    
    def submit_answer(self, player_id: str, answer: str):
        """Submit an answer for a player"""
        if player_id not in self.players:
            return False
        
        if player_id in self.answers_submitted:
            return False  # Already answered
        
        question = self.questions[self.current_question]
        is_correct = answer == question["correct_answer"]
        time_taken = time.time() - self.question_start_time
        
        # Calculate score: correct = 1000 points, bonus for speed (max 500 points)
        points = 0
        if is_correct:
            base_points = 1000
            # Speed bonus: full bonus if answered within 2 seconds, decreasing linearly
            speed_bonus = max(0, 500 - (time_taken * 50))
            points = int(base_points + speed_bonus)
        
        self.answers_submitted[player_id] = {
            "answer": answer,
            "is_correct": is_correct,
            "time_taken": time_taken,
            "points": points,
        }
        
        self.players[player_id]["score"] += points
        self.players[player_id]["answers"].append({
            "question_num": self.current_question,
            "answer": answer,
            "is_correct": is_correct,
            "time_taken": time_taken,
            "points": points,
        })
        
        return True
    
    def get_leaderboard(self) -> List[dict]:
        """Get sorted leaderboard"""
        leaderboard = []
        for player_id, player_data in self.players.items():
            leaderboard.append({
                "player_id": player_id,
                "name": player_data["name"],
                "score": player_data["score"],
                "answers": player_data["answers"],
            })
        
        # Sort by score (descending), then by join time (ascending)
        leaderboard.sort(key=lambda x: (-x["score"], self.players[x["player_id"]]["joined_at"]))
        
        # Add ranks
        for i, player in enumerate(leaderboard):
            player["rank"] = i + 1
        
        return leaderboard
    
    def get_current_question_stats(self) -> dict:
        """Get statistics for current question"""
        total_players = len(self.players)
        answered = len(self.answers_submitted)
        correct = sum(1 for a in self.answers_submitted.values() if a["is_correct"])
        
        return {
            "total_players": total_players,
            "answered": answered,
            "correct": correct,
            "waiting": total_players - answered,
        }


class SessionManager:
    """Global manager for all game sessions"""
    
    def __init__(self):
        self.sessions: Dict[str, GameSession] = {}
    
    def create_session(self, host_name: str, quiz_settings: dict, questions: list) -> GameSession:
        """Create a new game session"""
        session = GameSession(host_name, quiz_settings, questions)
        self.sessions[session.session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[GameSession]:
        """Get a session by ID"""
        return self.sessions.get(session_id)
    
    def close_session(self, session_id: str):
        """Close and remove a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Remove sessions older than max_age_hours"""
        now = datetime.now()
        to_remove = []
        for session_id, session in self.sessions.items():
            age = (now - session.created_at).total_seconds() / 3600
            if age > max_age_hours:
                to_remove.append(session_id)
        
        for session_id in to_remove:
            del self.sessions[session_id]
