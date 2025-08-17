"""
Comprehensive Life Planning System - Data Models

This module defines the core data models for a robust daily goal planner
and habit tracker that covers every aspect of a person's life.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Optional, Any
from enum import Enum
import json


class LifeCategory(Enum):
    """Categories covering all aspects of life"""
    HEALTH_FITNESS = "Health & Fitness"
    CAREER_EDUCATION = "Career & Education" 
    RELATIONSHIPS = "Relationships & Social"
    FINANCES = "Finances & Money"
    PERSONAL_GROWTH = "Personal Growth & Learning"
    HOBBIES_RECREATION = "Hobbies & Recreation"
    SPIRITUALITY = "Spirituality & Mindfulness"
    HOME_ENVIRONMENT = "Home & Environment"
    FAMILY = "Family & Parenting"
    CREATIVITY = "Creativity & Arts"
    COMMUNITY = "Community & Service"
    TRAVEL_ADVENTURE = "Travel & Adventure"


class Priority(Enum):
    """Priority levels for goals and habits"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class GoalStatus(Enum):
    """Status of goals"""
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"
    CANCELLED = "Cancelled"


class HabitFrequency(Enum):
    """Frequency options for habits"""
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    CUSTOM = "Custom"


class Difficulty(Enum):
    """Difficulty levels"""
    VERY_EASY = 1
    EASY = 2
    MODERATE = 3
    HARD = 4
    VERY_HARD = 5


@dataclass
class Goal:
    """Comprehensive goal model"""
    id: str
    title: str
    description: str
    category: LifeCategory
    priority: Priority
    difficulty: Difficulty
    status: GoalStatus = GoalStatus.NOT_STARTED
    created_date: datetime = field(default_factory=datetime.now)
    target_date: Optional[date] = None
    completion_date: Optional[datetime] = None
    progress_percentage: float = 0.0
    
    # Breakdown and planning
    milestones: List[str] = field(default_factory=list)
    action_steps: List[str] = field(default_factory=list)
    required_resources: List[str] = field(default_factory=list)
    potential_obstacles: List[str] = field(default_factory=list)
    
    # Motivation and tracking
    why_important: str = ""
    success_metrics: List[str] = field(default_factory=list)
    rewards: List[str] = field(default_factory=list)
    
    # Smart features
    estimated_hours: Optional[float] = None
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category.value,
            'priority': self.priority.value,
            'difficulty': self.difficulty.value,
            'status': self.status.value,
            'created_date': self.created_date.isoformat(),
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'progress_percentage': self.progress_percentage,
            'milestones': self.milestones,
            'action_steps': self.action_steps,
            'required_resources': self.required_resources,
            'potential_obstacles': self.potential_obstacles,
            'why_important': self.why_important,
            'success_metrics': self.success_metrics,
            'rewards': self.rewards,
            'estimated_hours': self.estimated_hours,
            'tags': self.tags,
            'notes': self.notes
        }


@dataclass
class Habit:
    """Comprehensive habit model"""
    id: str
    title: str
    description: str
    category: LifeCategory
    priority: Priority
    difficulty: Difficulty
    frequency: HabitFrequency
    
    # Scheduling
    target_days_per_week: int = 7
    target_times_per_day: int = 1
    preferred_time: Optional[str] = None
    duration_minutes: Optional[int] = None
    
    # Tracking
    created_date: datetime = field(default_factory=datetime.now)
    current_streak: int = 0
    longest_streak: int = 0
    total_completions: int = 0
    completion_rate: float = 0.0
    
    # Motivation and context
    why_important: str = ""
    trigger_cue: str = ""
    reward: str = ""
    environment_setup: str = ""
    
    # Smart features
    is_active: bool = True
    reminder_enabled: bool = True
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category.value,
            'priority': self.priority.value,
            'difficulty': self.difficulty.value,
            'frequency': self.frequency.value,
            'target_days_per_week': self.target_days_per_week,
            'target_times_per_day': self.target_times_per_day,
            'preferred_time': self.preferred_time,
            'duration_minutes': self.duration_minutes,
            'created_date': self.created_date.isoformat(),
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'total_completions': self.total_completions,
            'completion_rate': self.completion_rate,
            'why_important': self.why_important,
            'trigger_cue': self.trigger_cue,
            'reward': self.reward,
            'environment_setup': self.environment_setup,
            'is_active': self.is_active,
            'reminder_enabled': self.reminder_enabled,
            'tags': self.tags,
            'notes': self.notes
        }


@dataclass
class DailyEntry:
    """Daily journal and tracking entry"""
    date: date
    
    # Daily goals and habits
    completed_habits: List[str] = field(default_factory=list)
    goal_progress: Dict[str, float] = field(default_factory=dict)
    
    # Reflection and planning
    daily_wins: List[str] = field(default_factory=list)
    challenges_faced: List[str] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)
    gratitude_items: List[str] = field(default_factory=list)
    
    # Wellness tracking
    energy_level: Optional[int] = None  # 1-10 scale
    mood_rating: Optional[int] = None   # 1-10 scale
    stress_level: Optional[int] = None  # 1-10 scale
    sleep_hours: Optional[float] = None
    exercise_minutes: Optional[int] = None
    
    # Planning
    tomorrow_priorities: List[str] = field(default_factory=list)
    notes: str = ""
    
    created_time: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'date': self.date.isoformat(),
            'completed_habits': self.completed_habits,
            'goal_progress': self.goal_progress,
            'daily_wins': self.daily_wins,
            'challenges_faced': self.challenges_faced,
            'lessons_learned': self.lessons_learned,
            'gratitude_items': self.gratitude_items,
            'energy_level': self.energy_level,
            'mood_rating': self.mood_rating,
            'stress_level': self.stress_level,
            'sleep_hours': self.sleep_hours,
            'exercise_minutes': self.exercise_minutes,
            'tomorrow_priorities': self.tomorrow_priorities,
            'notes': self.notes,
            'created_time': self.created_time.isoformat()
        }


@dataclass
class LifeAssessment:
    """Periodic life assessment and review"""
    id: str
    date: date
    assessment_type: str  # "weekly", "monthly", "quarterly", "yearly"
    
    # Life satisfaction ratings (1-10 scale)
    category_ratings: Dict[LifeCategory, int] = field(default_factory=dict)
    overall_satisfaction: Optional[int] = None
    
    # Reflection
    biggest_wins: List[str] = field(default_factory=list)
    main_challenges: List[str] = field(default_factory=list)
    key_learnings: List[str] = field(default_factory=list)
    
    # Planning
    focus_areas: List[LifeCategory] = field(default_factory=list)
    new_goals_ideas: List[str] = field(default_factory=list)
    habits_to_start: List[str] = field(default_factory=list)
    habits_to_stop: List[str] = field(default_factory=list)
    
    # Goals
    goals_completed: List[str] = field(default_factory=list)
    goals_abandoned: List[str] = field(default_factory=list)
    
    notes: str = ""
    created_time: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'assessment_type': self.assessment_type,
            'category_ratings': {cat.value: rating for cat, rating in self.category_ratings.items()},
            'overall_satisfaction': self.overall_satisfaction,
            'biggest_wins': self.biggest_wins,
            'main_challenges': self.main_challenges,
            'key_learnings': self.key_learnings,
            'focus_areas': [cat.value for cat in self.focus_areas],
            'new_goals_ideas': self.new_goals_ideas,
            'habits_to_start': self.habits_to_start,
            'habits_to_stop': self.habits_to_stop,
            'goals_completed': self.goals_completed,
            'goals_abandoned': self.goals_abandoned,
            'notes': self.notes,
            'created_time': self.created_time.isoformat()
        }


@dataclass
class UserProfile:
    """User profile and preferences"""
    name: str
    timezone: str = "UTC"
    
    # Preferences
    preferred_reminder_times: List[str] = field(default_factory=list)
    notification_preferences: Dict[str, bool] = field(default_factory=dict)
    
    # Life focus areas
    primary_life_focuses: List[LifeCategory] = field(default_factory=list)
    life_vision: str = ""
    core_values: List[str] = field(default_factory=list)
    
    # Settings
    weekly_review_day: str = "Sunday"
    monthly_review_date: int = 1
    
    created_date: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'timezone': self.timezone,
            'preferred_reminder_times': self.preferred_reminder_times,
            'notification_preferences': self.notification_preferences,
            'primary_life_focuses': [cat.value for cat in self.primary_life_focuses],
            'life_vision': self.life_vision,
            'core_values': self.core_values,
            'weekly_review_day': self.weekly_review_day,
            'monthly_review_date': self.monthly_review_date,
            'created_date': self.created_date.isoformat()
        }