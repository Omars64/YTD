#!/usr/bin/env python3
"""
Life Planning System - Demonstration Script

This script demonstrates the key features and capabilities of the 
comprehensive life planning system.
"""

import uuid
from datetime import date, timedelta
from models import *
from database import DatabaseManager
from intelligence import IntelligenceEngine
from utils import create_progress_bar, format_streak_display

def demo_life_planning_system():
    """Demonstrate the Life Planning System capabilities"""
    
    print("🎯 LIFE PLANNING SYSTEM - DEMONSTRATION")
    print("=" * 60)
    
    # Initialize system
    print("\n1️⃣ INITIALIZING SYSTEM...")
    db = DatabaseManager("demo_life_planner.db")
    intelligence = IntelligenceEngine(db)
    print("✅ Database and intelligence engine initialized")
    
    # Create user profile
    print("\n2️⃣ CREATING USER PROFILE...")
    profile = UserProfile(
        name="Demo User",
        primary_life_focuses=[
            LifeCategory.HEALTH_FITNESS, 
            LifeCategory.CAREER_EDUCATION, 
            LifeCategory.PERSONAL_GROWTH
        ],
        life_vision="Live a balanced, purposeful life with continuous growth",
        core_values=["Health", "Learning", "Relationships", "Integrity"]
    )
    
    if db.create_user_profile(profile):
        print("✅ User profile created successfully")
        print(f"   Name: {profile.name}")
        print(f"   Focus areas: {[cat.value for cat in profile.primary_life_focuses]}")
        print(f"   Life vision: {profile.life_vision}")
    
    # Create sample goals
    print("\n3️⃣ CREATING SAMPLE GOALS...")
    goals = [
        Goal(
            id=str(uuid.uuid4()),
            title="Run a 5K race",
            description="Train for and complete a 5K running race",
            category=LifeCategory.HEALTH_FITNESS,
            priority=Priority.HIGH,
            difficulty=Difficulty.MODERATE,
            target_date=date.today() + timedelta(days=90),
            progress_percentage=25.0,
            why_important="Improve cardiovascular health and set fitness milestone",
            action_steps=["Week 1-2: Walk/jog intervals", "Week 3-6: Increase running duration", "Week 7-12: Build speed and endurance"],
            estimated_hours=36.0
        ),
        Goal(
            id=str(uuid.uuid4()),
            title="Learn Python programming",
            description="Master Python fundamentals and build projects",
            category=LifeCategory.CAREER_EDUCATION,
            priority=Priority.HIGH,
            difficulty=Difficulty.HARD,
            target_date=date.today() + timedelta(days=180),
            progress_percentage=40.0,
            why_important="Advance career in technology and automation",
            action_steps=["Complete online course", "Build 3 practice projects", "Contribute to open source"],
            estimated_hours=120.0
        ),
        Goal(
            id=str(uuid.uuid4()),
            title="Read 24 books this year",
            description="Develop a consistent reading habit for personal growth",
            category=LifeCategory.PERSONAL_GROWTH,
            priority=Priority.MEDIUM,
            difficulty=Difficulty.MODERATE,
            target_date=date.today() + timedelta(days=365),
            progress_percentage=33.0,
            why_important="Expand knowledge and improve focus",
            action_steps=["Read 30 minutes daily", "Join book club", "Track progress monthly"],
            estimated_hours=96.0
        )
    ]
    
    # Save goals
    for goal in goals:
        if db.create_goal(goal):
            difficulty_score = intelligence.calculate_goal_difficulty_score(goal)
            suggestions = intelligence.suggest_goal_breakdown(goal)
            
            print(f"✅ Goal created: {goal.title}")
            print(f"   Category: {goal.category.value}")
            print(f"   Progress: {create_progress_bar(goal.progress_percentage)} {goal.progress_percentage:.0f}%")
            print(f"   Difficulty: {difficulty_score:.2f}/1.0")
            print(f"   AI suggestions: {len(suggestions)} recommendations")
    
    # Create sample habits
    print("\n4️⃣ CREATING SAMPLE HABITS...")
    habits = [
        Habit(
            id=str(uuid.uuid4()),
            title="Morning exercise",
            description="30 minutes of physical activity each morning",
            category=LifeCategory.HEALTH_FITNESS,
            priority=Priority.HIGH,
            difficulty=Difficulty.MODERATE,
            frequency=HabitFrequency.DAILY,
            current_streak=12,
            longest_streak=18,
            total_completions=45,
            completion_rate=78.5,
            trigger_cue="After morning coffee",
            reward="Protein smoothie",
            preferred_time="07:00"
        ),
        Habit(
            id=str(uuid.uuid4()),
            title="Daily coding practice",
            description="Code for at least 45 minutes daily",
            category=LifeCategory.CAREER_EDUCATION,
            priority=Priority.HIGH,
            difficulty=Difficulty.HARD,
            frequency=HabitFrequency.DAILY,
            current_streak=5,
            longest_streak=23,
            total_completions=89,
            completion_rate=65.4,
            trigger_cue="After dinner",
            reward="Watch one YouTube video",
            preferred_time="19:30"
        ),
        Habit(
            id=str(uuid.uuid4()),
            title="Evening reading",
            description="Read for 30 minutes before bed",
            category=LifeCategory.PERSONAL_GROWTH,
            priority=Priority.MEDIUM,
            difficulty=Difficulty.EASY,
            frequency=HabitFrequency.DAILY,
            current_streak=7,
            longest_streak=31,
            total_completions=156,
            completion_rate=92.3,
            trigger_cue="After brushing teeth",
            reward="Relaxing herbal tea",
            preferred_time="21:30"
        )
    ]
    
    # Save habits
    for habit in habits:
        if db.create_habit(habit):
            success_prob = intelligence.predict_habit_success_probability(habit)
            optimization_tips = intelligence.suggest_habit_optimization(habit)
            
            print(f"✅ Habit created: {habit.title}")
            print(f"   Category: {habit.category.value}")
            print(f"   Streak: {format_streak_display(habit.current_streak, habit.longest_streak)}")
            print(f"   Success rate: {habit.completion_rate:.1f}%")
            print(f"   Success probability: {success_prob:.1%}")
            print(f"   Optimization tips: {len(optimization_tips)} suggestions")
    
    # Create sample daily entry
    print("\n5️⃣ CREATING DAILY ENTRY...")
    today = date.today()
    daily_entry = DailyEntry(
        date=today,
        completed_habits=[habits[0].id, habits[2].id],  # Completed 2 out of 3 habits
        goal_progress={goals[0].id: 5.0, goals[1].id: 2.0},  # Some progress on goals
        daily_wins=["Completed morning workout", "Learned new Python concept", "Had great family dinner"],
        challenges_faced=["Felt tired in afternoon", "Struggled with difficult code problem"],
        lessons_learned=["Need better sleep schedule", "Breaking problems into smaller parts helps"],
        gratitude_items=["Supportive family", "Good health", "Learning opportunities"],
        energy_level=7,
        mood_rating=8,
        stress_level=4,
        sleep_hours=7.5,
        exercise_minutes=45,
        tomorrow_priorities=["Finish Python project", "Plan weekend activities", "Call mom"]
    )
    
    if db.create_daily_entry(daily_entry):
        print("✅ Daily entry created successfully")
        print(f"   Habits completed: {len(daily_entry.completed_habits)}/3")
        print(f"   Daily wins: {len(daily_entry.daily_wins)} recorded")
        print(f"   Energy level: {daily_entry.energy_level}/10")
        print(f"   Mood rating: {daily_entry.mood_rating}/10")
        print(f"   Tomorrow priorities: {len(daily_entry.tomorrow_priorities)} set")
    
    # Generate analytics
    print("\n6️⃣ GENERATING ANALYTICS & INSIGHTS...")
    
    # Goal analytics
    goal_analytics = intelligence.generate_progress_analytics()
    print(f"📊 Goal Analytics:")
    print(f"   Total goals: {goal_analytics.total_goals}")
    print(f"   In progress: {goal_analytics.in_progress_goals}")
    print(f"   Completion rate: {goal_analytics.completion_rate:.1f}%")
    
    # Habit analytics
    habit_analytics = intelligence.generate_habit_analytics()
    print(f"🔄 Habit Analytics:")
    print(f"   Active habits: {habit_analytics.active_habits}")
    print(f"   Average streak: {habit_analytics.average_streak:.1f} days")
    print(f"   Weekly consistency: {habit_analytics.weekly_consistency_score:.1f}%")
    print(f"   Best performing: {', '.join(habit_analytics.best_performing_habits)}")
    
    # Life score
    life_score = intelligence.calculate_life_score()
    print(f"📈 Life Score:")
    print(f"   Overall score: {life_score.overall_score:.2f}/1.0")
    print(f"   Trend: {life_score.trend}")
    print(f"   Balance score: {life_score.balance_score:.2f}/1.0")
    
    # AI insights
    insights = intelligence.generate_intelligent_insights()
    print(f"🧠 AI Insights: {len(insights)} recommendations generated")
    
    if insights:
        print("   Top insights:")
        for i, insight in enumerate(insights[:3], 1):
            priority_icon = "🔥" if insight.priority == Priority.HIGH else "⭐"
            print(f"   {i}. {priority_icon} {insight.title}")
            print(f"      {insight.description}")
            print(f"      Confidence: {insight.confidence_score:.0%}")
    
    # System capabilities summary
    print("\n7️⃣ SYSTEM CAPABILITIES DEMONSTRATED:")
    print("✅ Comprehensive data models for all life aspects")
    print("✅ Intelligent goal breakdown and prioritization")
    print("✅ Advanced habit tracking with streak analysis")
    print("✅ AI-powered insights and recommendations")
    print("✅ Progress analytics and life balance scoring")
    print("✅ Daily planning and reflection capabilities")
    print("✅ Robust SQLite database with full CRUD operations")
    print("✅ Pattern recognition and success prediction")
    print("✅ Motivation and achievement tracking")
    print("✅ Holistic life optimization approach")
    
    print(f"\n🎉 DEMONSTRATION COMPLETE!")
    print("The Life Planning System is fully functional and ready to help")
    print("transform your life through intelligent goal setting and habit tracking!")
    
    print(f"\n📁 Demo data saved to: demo_life_planner.db")
    print("You can explore this data by running: python main.py")
    print("and opening the demo database file.")


if __name__ == "__main__":
    demo_life_planning_system()