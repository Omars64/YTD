"""
Database Layer for Life Planning System

Handles all data persistence using SQLite with comprehensive operations
for goals, habits, daily entries, assessments, and user profiles.
"""

import sqlite3
import json
from datetime import datetime, date
from typing import List, Dict, Optional, Any
from pathlib import Path

from models import (
    Goal, Habit, DailyEntry, LifeAssessment, UserProfile,
    LifeCategory, Priority, GoalStatus, HabitFrequency, Difficulty
)


class DatabaseManager:
    """Comprehensive database manager for the life planning system"""
    
    def __init__(self, db_path: str = "life_planner.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with proper configuration"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with all required tables"""
        with self.get_connection() as conn:
            # Goals table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS goals (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    category TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    difficulty INTEGER NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Not Started',
                    created_date TEXT NOT NULL,
                    target_date TEXT,
                    completion_date TEXT,
                    progress_percentage REAL DEFAULT 0.0,
                    milestones TEXT,
                    action_steps TEXT,
                    required_resources TEXT,
                    potential_obstacles TEXT,
                    why_important TEXT,
                    success_metrics TEXT,
                    rewards TEXT,
                    estimated_hours REAL,
                    tags TEXT,
                    notes TEXT
                )
            """)
            
            # Habits table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    category TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    difficulty INTEGER NOT NULL,
                    frequency TEXT NOT NULL,
                    target_days_per_week INTEGER DEFAULT 7,
                    target_times_per_day INTEGER DEFAULT 1,
                    preferred_time TEXT,
                    duration_minutes INTEGER,
                    created_date TEXT NOT NULL,
                    current_streak INTEGER DEFAULT 0,
                    longest_streak INTEGER DEFAULT 0,
                    total_completions INTEGER DEFAULT 0,
                    completion_rate REAL DEFAULT 0.0,
                    why_important TEXT,
                    trigger_cue TEXT,
                    reward TEXT,
                    environment_setup TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    reminder_enabled BOOLEAN DEFAULT TRUE,
                    tags TEXT,
                    notes TEXT
                )
            """)
            
            # Daily entries table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS daily_entries (
                    date TEXT PRIMARY KEY,
                    completed_habits TEXT,
                    goal_progress TEXT,
                    daily_wins TEXT,
                    challenges_faced TEXT,
                    lessons_learned TEXT,
                    gratitude_items TEXT,
                    energy_level INTEGER,
                    mood_rating INTEGER,
                    stress_level INTEGER,
                    sleep_hours REAL,
                    exercise_minutes INTEGER,
                    tomorrow_priorities TEXT,
                    notes TEXT,
                    created_time TEXT NOT NULL
                )
            """)
            
            # Life assessments table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS life_assessments (
                    id TEXT PRIMARY KEY,
                    date TEXT NOT NULL,
                    assessment_type TEXT NOT NULL,
                    category_ratings TEXT,
                    overall_satisfaction INTEGER,
                    biggest_wins TEXT,
                    main_challenges TEXT,
                    key_learnings TEXT,
                    focus_areas TEXT,
                    new_goals_ideas TEXT,
                    habits_to_start TEXT,
                    habits_to_stop TEXT,
                    goals_completed TEXT,
                    goals_abandoned TEXT,
                    notes TEXT,
                    created_time TEXT NOT NULL
                )
            """)
            
            # User profile table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_profile (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    timezone TEXT DEFAULT 'UTC',
                    preferred_reminder_times TEXT,
                    notification_preferences TEXT,
                    primary_life_focuses TEXT,
                    life_vision TEXT,
                    core_values TEXT,
                    weekly_review_day TEXT DEFAULT 'Sunday',
                    monthly_review_date INTEGER DEFAULT 1,
                    created_date TEXT NOT NULL
                )
            """)
            
            # Habit completions tracking table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS habit_completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id TEXT NOT NULL,
                    completion_date TEXT NOT NULL,
                    completion_time TEXT,
                    notes TEXT,
                    FOREIGN KEY (habit_id) REFERENCES habits (id),
                    UNIQUE(habit_id, completion_date, completion_time)
                )
            """)
            
            conn.commit()
    
    # Goal operations
    def create_goal(self, goal: Goal) -> bool:
        """Create a new goal"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO goals VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    goal.id, goal.title, goal.description, goal.category.value,
                    goal.priority.value, goal.difficulty.value, goal.status.value,
                    goal.created_date.isoformat(),
                    goal.target_date.isoformat() if goal.target_date else None,
                    goal.completion_date.isoformat() if goal.completion_date else None,
                    goal.progress_percentage,
                    json.dumps(goal.milestones),
                    json.dumps(goal.action_steps),
                    json.dumps(goal.required_resources),
                    json.dumps(goal.potential_obstacles),
                    goal.why_important,
                    json.dumps(goal.success_metrics),
                    json.dumps(goal.rewards),
                    goal.estimated_hours,
                    json.dumps(goal.tags),
                    goal.notes
                ))
                return True
        except Exception as e:
            print(f"Error creating goal: {e}")
            return False
    
    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """Get a goal by ID"""
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM goals WHERE id = ?", (goal_id,)).fetchone()
            if row:
                return self._row_to_goal(row)
            return None
    
    def get_all_goals(self) -> List[Goal]:
        """Get all goals"""
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM goals ORDER BY created_date DESC").fetchall()
            return [self._row_to_goal(row) for row in rows]
    
    def get_goals_by_category(self, category: LifeCategory) -> List[Goal]:
        """Get goals by category"""
        with self.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM goals WHERE category = ? ORDER BY priority DESC, created_date DESC",
                (category.value,)
            ).fetchall()
            return [self._row_to_goal(row) for row in rows]
    
    def get_goals_by_status(self, status: GoalStatus) -> List[Goal]:
        """Get goals by status"""
        with self.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM goals WHERE status = ? ORDER BY priority DESC, created_date DESC",
                (status.value,)
            ).fetchall()
            return [self._row_to_goal(row) for row in rows]
    
    def update_goal(self, goal: Goal) -> bool:
        """Update an existing goal"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    UPDATE goals SET title=?, description=?, category=?, priority=?, difficulty=?,
                    status=?, target_date=?, completion_date=?, progress_percentage=?,
                    milestones=?, action_steps=?, required_resources=?, potential_obstacles=?,
                    why_important=?, success_metrics=?, rewards=?, estimated_hours=?,
                    tags=?, notes=? WHERE id=?
                """, (
                    goal.title, goal.description, goal.category.value,
                    goal.priority.value, goal.difficulty.value, goal.status.value,
                    goal.target_date.isoformat() if goal.target_date else None,
                    goal.completion_date.isoformat() if goal.completion_date else None,
                    goal.progress_percentage,
                    json.dumps(goal.milestones),
                    json.dumps(goal.action_steps),
                    json.dumps(goal.required_resources),
                    json.dumps(goal.potential_obstacles),
                    goal.why_important,
                    json.dumps(goal.success_metrics),
                    json.dumps(goal.rewards),
                    goal.estimated_hours,
                    json.dumps(goal.tags),
                    goal.notes,
                    goal.id
                ))
                return True
        except Exception as e:
            print(f"Error updating goal: {e}")
            return False
    
    def delete_goal(self, goal_id: str) -> bool:
        """Delete a goal"""
        try:
            with self.get_connection() as conn:
                conn.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
                return True
        except Exception as e:
            print(f"Error deleting goal: {e}")
            return False
    
    # Habit operations
    def create_habit(self, habit: Habit) -> bool:
        """Create a new habit"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    habit.id, habit.title, habit.description, habit.category.value,
                    habit.priority.value, habit.difficulty.value, habit.frequency.value,
                    habit.target_days_per_week, habit.target_times_per_day,
                    habit.preferred_time, habit.duration_minutes,
                    habit.created_date.isoformat(),
                    habit.current_streak, habit.longest_streak,
                    habit.total_completions, habit.completion_rate,
                    habit.why_important, habit.trigger_cue, habit.reward,
                    habit.environment_setup, habit.is_active, habit.reminder_enabled,
                    json.dumps(habit.tags), habit.notes
                ))
                return True
        except Exception as e:
            print(f"Error creating habit: {e}")
            return False
    
    def get_habit(self, habit_id: str) -> Optional[Habit]:
        """Get a habit by ID"""
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM habits WHERE id = ?", (habit_id,)).fetchone()
            if row:
                return self._row_to_habit(row)
            return None
    
    def get_all_habits(self) -> List[Habit]:
        """Get all habits"""
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM habits ORDER BY is_active DESC, priority DESC, created_date DESC").fetchall()
            return [self._row_to_habit(row) for row in rows]
    
    def get_active_habits(self) -> List[Habit]:
        """Get all active habits"""
        with self.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM habits WHERE is_active = TRUE ORDER BY priority DESC, created_date DESC"
            ).fetchall()
            return [self._row_to_habit(row) for row in rows]
    
    def update_habit(self, habit: Habit) -> bool:
        """Update an existing habit"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    UPDATE habits SET title=?, description=?, category=?, priority=?, difficulty=?,
                    frequency=?, target_days_per_week=?, target_times_per_day=?, preferred_time=?,
                    duration_minutes=?, current_streak=?, longest_streak=?, total_completions=?,
                    completion_rate=?, why_important=?, trigger_cue=?, reward=?, environment_setup=?,
                    is_active=?, reminder_enabled=?, tags=?, notes=? WHERE id=?
                """, (
                    habit.title, habit.description, habit.category.value,
                    habit.priority.value, habit.difficulty.value, habit.frequency.value,
                    habit.target_days_per_week, habit.target_times_per_day,
                    habit.preferred_time, habit.duration_minutes,
                    habit.current_streak, habit.longest_streak,
                    habit.total_completions, habit.completion_rate,
                    habit.why_important, habit.trigger_cue, habit.reward,
                    habit.environment_setup, habit.is_active, habit.reminder_enabled,
                    json.dumps(habit.tags), habit.notes, habit.id
                ))
                return True
        except Exception as e:
            print(f"Error updating habit: {e}")
            return False
    
    def record_habit_completion(self, habit_id: str, completion_date: date, 
                               completion_time: Optional[str] = None, notes: str = "") -> bool:
        """Record a habit completion"""
        try:
            with self.get_connection() as conn:
                # Insert completion record
                conn.execute("""
                    INSERT OR IGNORE INTO habit_completions (habit_id, completion_date, completion_time, notes)
                    VALUES (?, ?, ?, ?)
                """, (habit_id, completion_date.isoformat(), completion_time, notes))
                
                # Update habit statistics
                habit = self.get_habit(habit_id)
                if habit:
                    # Calculate new streak and completion rate
                    completions = self.get_habit_completions(habit_id)
                    habit.total_completions = len(completions)
                    
                    # Calculate current streak
                    habit.current_streak = self._calculate_current_streak(completions, completion_date)
                    habit.longest_streak = max(habit.longest_streak, habit.current_streak)
                    
                    # Calculate completion rate
                    days_since_creation = (completion_date - habit.created_date.date()).days + 1
                    expected_completions = days_since_creation * (habit.target_days_per_week / 7)
                    habit.completion_rate = min(100.0, (habit.total_completions / expected_completions) * 100)
                    
                    self.update_habit(habit)
                
                return True
        except Exception as e:
            print(f"Error recording habit completion: {e}")
            return False
    
    def get_habit_completions(self, habit_id: str, start_date: Optional[date] = None, 
                             end_date: Optional[date] = None) -> List[Dict[str, Any]]:
        """Get habit completion records"""
        with self.get_connection() as conn:
            query = "SELECT * FROM habit_completions WHERE habit_id = ?"
            params = [habit_id]
            
            if start_date:
                query += " AND completion_date >= ?"
                params.append(start_date.isoformat())
            
            if end_date:
                query += " AND completion_date <= ?"
                params.append(end_date.isoformat())
                
            query += " ORDER BY completion_date DESC"
            
            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]
    
    # Daily entry operations
    def create_daily_entry(self, entry: DailyEntry) -> bool:
        """Create or update a daily entry"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO daily_entries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    entry.date.isoformat(),
                    json.dumps(entry.completed_habits),
                    json.dumps(entry.goal_progress),
                    json.dumps(entry.daily_wins),
                    json.dumps(entry.challenges_faced),
                    json.dumps(entry.lessons_learned),
                    json.dumps(entry.gratitude_items),
                    entry.energy_level,
                    entry.mood_rating,
                    entry.stress_level,
                    entry.sleep_hours,
                    entry.exercise_minutes,
                    json.dumps(entry.tomorrow_priorities),
                    entry.notes,
                    entry.created_time.isoformat()
                ))
                return True
        except Exception as e:
            print(f"Error creating daily entry: {e}")
            return False
    
    def get_daily_entry(self, date: date) -> Optional[DailyEntry]:
        """Get daily entry for a specific date"""
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM daily_entries WHERE date = ?",
                (date.isoformat(),)
            ).fetchone()
            if row:
                return self._row_to_daily_entry(row)
            return None
    
    def get_daily_entries_range(self, start_date: date, end_date: date) -> List[DailyEntry]:
        """Get daily entries for a date range"""
        with self.get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM daily_entries 
                WHERE date >= ? AND date <= ? 
                ORDER BY date DESC
            """, (start_date.isoformat(), end_date.isoformat())).fetchall()
            return [self._row_to_daily_entry(row) for row in rows]
    
    # Life assessment operations
    def create_life_assessment(self, assessment: LifeAssessment) -> bool:
        """Create a life assessment"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO life_assessments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    assessment.id,
                    assessment.date.isoformat(),
                    assessment.assessment_type,
                    json.dumps({cat.value: rating for cat, rating in assessment.category_ratings.items()}),
                    assessment.overall_satisfaction,
                    json.dumps(assessment.biggest_wins),
                    json.dumps(assessment.main_challenges),
                    json.dumps(assessment.key_learnings),
                    json.dumps([cat.value for cat in assessment.focus_areas]),
                    json.dumps(assessment.new_goals_ideas),
                    json.dumps(assessment.habits_to_start),
                    json.dumps(assessment.habits_to_stop),
                    json.dumps(assessment.goals_completed),
                    json.dumps(assessment.goals_abandoned),
                    assessment.notes,
                    assessment.created_time.isoformat()
                ))
                return True
        except Exception as e:
            print(f"Error creating life assessment: {e}")
            return False
    
    def get_life_assessments(self, assessment_type: Optional[str] = None) -> List[LifeAssessment]:
        """Get life assessments, optionally filtered by type"""
        with self.get_connection() as conn:
            if assessment_type:
                rows = conn.execute(
                    "SELECT * FROM life_assessments WHERE assessment_type = ? ORDER BY date DESC",
                    (assessment_type,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM life_assessments ORDER BY date DESC"
                ).fetchall()
            return [self._row_to_life_assessment(row) for row in rows]
    
    # User profile operations
    def create_user_profile(self, profile: UserProfile) -> bool:
        """Create or update user profile"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO user_profile (id, name, timezone, preferred_reminder_times,
                    notification_preferences, primary_life_focuses, life_vision, core_values,
                    weekly_review_day, monthly_review_date, created_date)
                    VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    profile.name,
                    profile.timezone,
                    json.dumps(profile.preferred_reminder_times),
                    json.dumps(profile.notification_preferences),
                    json.dumps([cat.value for cat in profile.primary_life_focuses]),
                    profile.life_vision,
                    json.dumps(profile.core_values),
                    profile.weekly_review_day,
                    profile.monthly_review_date,
                    profile.created_date.isoformat()
                ))
                return True
        except Exception as e:
            print(f"Error creating user profile: {e}")
            return False
    
    def get_user_profile(self) -> Optional[UserProfile]:
        """Get user profile"""
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM user_profile WHERE id = 1").fetchone()
            if row:
                return self._row_to_user_profile(row)
            return None
    
    # Helper methods for converting database rows to objects
    def _row_to_goal(self, row) -> Goal:
        """Convert database row to Goal object"""
        return Goal(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            category=LifeCategory(row['category']),
            priority=Priority(row['priority']),
            difficulty=Difficulty(row['difficulty']),
            status=GoalStatus(row['status']),
            created_date=datetime.fromisoformat(row['created_date']),
            target_date=date.fromisoformat(row['target_date']) if row['target_date'] else None,
            completion_date=datetime.fromisoformat(row['completion_date']) if row['completion_date'] else None,
            progress_percentage=row['progress_percentage'],
            milestones=json.loads(row['milestones']) if row['milestones'] else [],
            action_steps=json.loads(row['action_steps']) if row['action_steps'] else [],
            required_resources=json.loads(row['required_resources']) if row['required_resources'] else [],
            potential_obstacles=json.loads(row['potential_obstacles']) if row['potential_obstacles'] else [],
            why_important=row['why_important'] or "",
            success_metrics=json.loads(row['success_metrics']) if row['success_metrics'] else [],
            rewards=json.loads(row['rewards']) if row['rewards'] else [],
            estimated_hours=row['estimated_hours'],
            tags=json.loads(row['tags']) if row['tags'] else [],
            notes=row['notes'] or ""
        )
    
    def _row_to_habit(self, row) -> Habit:
        """Convert database row to Habit object"""
        return Habit(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            category=LifeCategory(row['category']),
            priority=Priority(row['priority']),
            difficulty=Difficulty(row['difficulty']),
            frequency=HabitFrequency(row['frequency']),
            target_days_per_week=row['target_days_per_week'],
            target_times_per_day=row['target_times_per_day'],
            preferred_time=row['preferred_time'],
            duration_minutes=row['duration_minutes'],
            created_date=datetime.fromisoformat(row['created_date']),
            current_streak=row['current_streak'],
            longest_streak=row['longest_streak'],
            total_completions=row['total_completions'],
            completion_rate=row['completion_rate'],
            why_important=row['why_important'] or "",
            trigger_cue=row['trigger_cue'] or "",
            reward=row['reward'] or "",
            environment_setup=row['environment_setup'] or "",
            is_active=bool(row['is_active']),
            reminder_enabled=bool(row['reminder_enabled']),
            tags=json.loads(row['tags']) if row['tags'] else [],
            notes=row['notes'] or ""
        )
    
    def _row_to_daily_entry(self, row) -> DailyEntry:
        """Convert database row to DailyEntry object"""
        return DailyEntry(
            date=date.fromisoformat(row['date']),
            completed_habits=json.loads(row['completed_habits']) if row['completed_habits'] else [],
            goal_progress=json.loads(row['goal_progress']) if row['goal_progress'] else {},
            daily_wins=json.loads(row['daily_wins']) if row['daily_wins'] else [],
            challenges_faced=json.loads(row['challenges_faced']) if row['challenges_faced'] else [],
            lessons_learned=json.loads(row['lessons_learned']) if row['lessons_learned'] else [],
            gratitude_items=json.loads(row['gratitude_items']) if row['gratitude_items'] else [],
            energy_level=row['energy_level'],
            mood_rating=row['mood_rating'],
            stress_level=row['stress_level'],
            sleep_hours=row['sleep_hours'],
            exercise_minutes=row['exercise_minutes'],
            tomorrow_priorities=json.loads(row['tomorrow_priorities']) if row['tomorrow_priorities'] else [],
            notes=row['notes'] or "",
            created_time=datetime.fromisoformat(row['created_time'])
        )
    
    def _row_to_life_assessment(self, row) -> LifeAssessment:
        """Convert database row to LifeAssessment object"""
        category_ratings = {}
        if row['category_ratings']:
            ratings_dict = json.loads(row['category_ratings'])
            category_ratings = {LifeCategory(cat): rating for cat, rating in ratings_dict.items()}
        
        focus_areas = []
        if row['focus_areas']:
            focus_areas = [LifeCategory(cat) for cat in json.loads(row['focus_areas'])]
        
        return LifeAssessment(
            id=row['id'],
            date=date.fromisoformat(row['date']),
            assessment_type=row['assessment_type'],
            category_ratings=category_ratings,
            overall_satisfaction=row['overall_satisfaction'],
            biggest_wins=json.loads(row['biggest_wins']) if row['biggest_wins'] else [],
            main_challenges=json.loads(row['main_challenges']) if row['main_challenges'] else [],
            key_learnings=json.loads(row['key_learnings']) if row['key_learnings'] else [],
            focus_areas=focus_areas,
            new_goals_ideas=json.loads(row['new_goals_ideas']) if row['new_goals_ideas'] else [],
            habits_to_start=json.loads(row['habits_to_start']) if row['habits_to_start'] else [],
            habits_to_stop=json.loads(row['habits_to_stop']) if row['habits_to_stop'] else [],
            goals_completed=json.loads(row['goals_completed']) if row['goals_completed'] else [],
            goals_abandoned=json.loads(row['goals_abandoned']) if row['goals_abandoned'] else [],
            notes=row['notes'] or "",
            created_time=datetime.fromisoformat(row['created_time'])
        )
    
    def _row_to_user_profile(self, row) -> UserProfile:
        """Convert database row to UserProfile object"""
        primary_life_focuses = []
        if row['primary_life_focuses']:
            primary_life_focuses = [LifeCategory(cat) for cat in json.loads(row['primary_life_focuses'])]
        
        return UserProfile(
            name=row['name'],
            timezone=row['timezone'],
            preferred_reminder_times=json.loads(row['preferred_reminder_times']) if row['preferred_reminder_times'] else [],
            notification_preferences=json.loads(row['notification_preferences']) if row['notification_preferences'] else {},
            primary_life_focuses=primary_life_focuses,
            life_vision=row['life_vision'] or "",
            core_values=json.loads(row['core_values']) if row['core_values'] else [],
            weekly_review_day=row['weekly_review_day'],
            monthly_review_date=row['monthly_review_date'],
            created_date=datetime.fromisoformat(row['created_date'])
        )
    
    def _calculate_current_streak(self, completions: List[Dict], current_date: date) -> int:
        """Calculate current streak for a habit"""
        if not completions:
            return 1 if current_date == date.today() else 0
        
        # Sort completions by date
        completion_dates = sorted([date.fromisoformat(c['completion_date']) for c in completions], reverse=True)
        
        # Start from today and count backwards
        streak = 0
        check_date = current_date
        
        for completion_date in completion_dates:
            if completion_date == check_date:
                streak += 1
                check_date = date.fromordinal(check_date.toordinal() - 1)
            elif completion_date < check_date:
                break
        
        return streak