import random
import string
import time
from datetime import datetime
from typing import Dict, List, Optional
import streamlit as st


@st.cache_resource
def get_global_session_manager():
    """Get the global session manager singleton shared across all users"""
    return SessionManager()


class GameSession:
    """Represents a multiplayer quiz game session"""
    
    def __init__(self, host_name: str, quiz_settings: dict, questions: list):
        self.session_id = self._generate_session_id()
        self.host_name = host_name
        self.quiz_settings = quiz_settings
        self.questions = questions
        self.players: Dict[str, dict] = {}  # player_id -> player_data
        self.status = "waiting"  # waiting, playing, finished
        self.created_at = datetime.now()
        
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
            "current_question": 0,  # Each player tracks their own progress
            "finished": False,
            "start_time": time.time(),  # Initialize timer
        }
        return player_id
    
    def start_game(self):
        """Start the game"""
        self.status = "playing"
        # Initialize each player's progress
        for player_id in self.players:
            self.players[player_id]["current_question"] = 0
            self.players[player_id]["finished"] = False
            self.players[player_id]["start_time"] = time.time()
    
    def submit_answer(self, player_id: str, question_num: int, answer: str):
        """Submit an answer for a player at their current question"""
        if player_id not in self.players:
            return False
        
        player = self.players[player_id]
        
        # Ensure player has required fields
        if "current_question" not in player:
            player["current_question"] = 0
        if "finished" not in player:
            player["finished"] = False
        if "start_time" not in player:
            player["start_time"] = time.time()
        
        # Check if this is the player's current question
        if question_num != player["current_question"]:
            return False
        
        # Check if already answered this question
        answered_questions = [ans.get("question_num", -1) for ans in player.get("answers", [])]
        if question_num in answered_questions:
            return False
        
        # Validate question number
        if question_num < 0 or question_num >= len(self.questions):
            return False
        
        question = self.questions[question_num]
        is_correct = answer == question.get("correct_answer")
        time_taken = time.time() - player.get("start_time", time.time())
        
        # Calculate score: correct = 1000 points, bonus for speed (max 500 points)
        points = 0
        if is_correct:
            base_points = 1000
            # Speed bonus: full bonus if answered within 2 seconds, decreasing linearly
            speed_bonus = max(0, 500 - (time_taken * 50))
            points = int(base_points + speed_bonus)
        
        # Record the answer
        player["score"] = player.get("score", 0) + points
        if "answers" not in player:
            player["answers"] = []
        player["answers"].append({
            "question_num": question_num,
            "answer": answer,
            "is_correct": is_correct,
            "time_taken": time_taken,
            "points": points,
        })
        
        # Move to next question
        if player["current_question"] < len(self.questions) - 1:
            player["current_question"] += 1
            player["start_time"] = time.time()  # Reset timer for next question
        else:
            player["finished"] = True
            # Check if all players are finished
            if all(p.get("finished", False) for p in self.players.values()):
                self.status = "finished"
        
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
