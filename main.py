#!/usr/bin/env python3
"""
Life Planning System - Main Application

A comprehensive daily goal planner and habit tracker that covers every aspect
of a person's life with intelligent algorithms and insights.
"""

import os
import sys
import uuid
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
import json

from models import *
from database import DatabaseManager
from intelligence import IntelligenceEngine
from utils import get_user_input, display_formatted_data, create_progress_bar


class LifePlannerApp:
    """Main application class for the Life Planning System"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.intelligence = IntelligenceEngine(self.db)
        self.current_user = self.db.get_user_profile()
        
        if not self.current_user:
            self._setup_first_time_user()
    
    def run(self):
        """Main application loop"""
        self._display_welcome()
        
        while True:
            try:
                choice = self._show_main_menu()
                
                if choice == '1':
                    self._goal_management_menu()
                elif choice == '2':
                    self._habit_management_menu()
                elif choice == '3':
                    self._daily_planning_menu()
                elif choice == '4':
                    self._analytics_and_insights_menu()
                elif choice == '5':
                    self._life_assessment_menu()
                elif choice == '6':
                    self._settings_menu()
                elif choice == '7':
                    self._data_management_menu()
                elif choice == '8':
                    print("\n👋 Thank you for using Life Planning System! Stay awesome!")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")
    
    def _display_welcome(self):
        """Display welcome message"""
        name = self.current_user.name if self.current_user else "User"
        print("\n" + "="*60)
        print("🎯 LIFE PLANNING SYSTEM")
        print("   Your Comprehensive Life Optimization Platform")
        print("="*60)
        print(f"Welcome back, {name}! Ready to make today amazing? ✨")
        
        # Show quick daily summary
        self._show_daily_summary()
    
    def _show_daily_summary(self):
        """Show quick daily summary"""
        today = date.today()
        daily_entry = self.db.get_daily_entry(today)
        active_habits = self.db.get_active_habits()
        
        print("\n📊 TODAY'S QUICK OVERVIEW:")
        print("-" * 40)
        
        # Habits completion
        if active_habits:
            completed_today = len(daily_entry.completed_habits) if daily_entry else 0
            completion_rate = (completed_today / len(active_habits)) * 100
            progress_bar = create_progress_bar(completion_rate, 20)
            print(f"Habits: {completed_today}/{len(active_habits)} {progress_bar} {completion_rate:.0f}%")
        
        # Goals progress
        active_goals = self.db.get_goals_by_status(GoalStatus.IN_PROGRESS)
        if active_goals:
            avg_progress = sum(g.progress_percentage for g in active_goals) / len(active_goals)
            progress_bar = create_progress_bar(avg_progress, 20)
            print(f"Goals:  {len(active_goals)} active {progress_bar} {avg_progress:.0f}% avg")
        
        # Insights count
        insights = self.intelligence.generate_intelligent_insights()
        high_priority_insights = [i for i in insights if i.priority in [Priority.HIGH, Priority.URGENT]]
        if high_priority_insights:
            print(f"💡 Insights: {len(high_priority_insights)} high-priority recommendations available")
    
    def _show_main_menu(self) -> str:
        """Display main menu and get user choice"""
        print("\n" + "="*60)
        print("🏠 MAIN MENU")
        print("="*60)
        print("1. 🎯 Goal Management")
        print("2. 🔄 Habit Tracking")
        print("3. 📅 Daily Planning")
        print("4. 📊 Analytics & Insights")
        print("5. 🔍 Life Assessment")
        print("6. ⚙️  Settings")
        print("7. 💾 Data Management")
        print("8. 🚪 Exit")
        print("-" * 60)
        
        return input("Choose an option (1-8): ").strip()
    
    # Goal Management
    def _goal_management_menu(self):
        """Goal management submenu"""
        while True:
            print("\n" + "="*50)
            print("🎯 GOAL MANAGEMENT")
            print("="*50)
            print("1. ➕ Create New Goal")
            print("2. 📋 View All Goals")
            print("3. ✏️  Edit Goal")
            print("4. 📈 Update Progress")
            print("5. ✅ Mark Complete")
            print("6. 🧠 Get AI Suggestions")
            print("7. 🔄 Prioritize Goals")
            print("8. 🏠 Back to Main Menu")
            
            choice = input("\nChoose an option (1-8): ").strip()
            
            if choice == '1':
                self._create_goal()
            elif choice == '2':
                self._view_goals()
            elif choice == '3':
                self._edit_goal()
            elif choice == '4':
                self._update_goal_progress()
            elif choice == '5':
                self._complete_goal()
            elif choice == '6':
                self._get_goal_suggestions()
            elif choice == '7':
                self._prioritize_goals()
            elif choice == '8':
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def _create_goal(self):
        """Create a new goal with intelligent assistance"""
        print("\n🎯 CREATE NEW GOAL")
        print("-" * 30)
        
        # Basic information
        title = get_user_input("Goal title", required=True)
        description = get_user_input("Description (optional)")
        
        # Category selection
        print("\nSelect a life category:")
        categories = list(LifeCategory)
        for i, cat in enumerate(categories, 1):
            print(f"{i:2d}. {cat.value}")
        
        while True:
            try:
                cat_choice = int(input("Category (1-12): "))
                if 1 <= cat_choice <= len(categories):
                    category = categories[cat_choice - 1]
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a number.")
        
        # Priority and difficulty
        priority = self._select_priority()
        difficulty = self._select_difficulty()
        
        # Target date
        target_date = self._get_target_date()
        
        # Advanced details
        print("\nLet's add some strategic details to make this goal more achievable:")
        why_important = get_user_input("Why is this goal important to you?")
        estimated_hours = self._get_optional_float("Estimated hours to complete")
        
        # Create goal
        goal = Goal(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            category=category,
            priority=priority,
            difficulty=difficulty,
            target_date=target_date,
            why_important=why_important,
            estimated_hours=estimated_hours
        )
        
        # Get AI suggestions for breakdown
        print("\n🧠 Getting AI suggestions for your goal...")
        suggestions = self.intelligence.suggest_goal_breakdown(goal)
        
        if suggestions:
            print("\n💡 AI SUGGESTIONS:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion}")
            
            if get_user_input("\nWould you like to add action steps now? (y/n)", default="y").lower() == 'y':
                self._add_action_steps(goal)
        
        # Save goal
        if self.db.create_goal(goal):
            print(f"\n✅ Goal '{title}' created successfully!")
            print(f"🎯 Difficulty Score: {self.intelligence.calculate_goal_difficulty_score(goal):.2f}/1.0")
        else:
            print("❌ Failed to create goal. Please try again.")
    
    def _view_goals(self):
        """View goals with filtering options"""
        print("\n📋 GOALS OVERVIEW")
        print("-" * 30)
        
        print("1. All Goals")
        print("2. By Status")
        print("3. By Category")
        print("4. By Priority")
        
        choice = input("Filter by (1-4): ").strip()
        
        if choice == '1':
            goals = self.db.get_all_goals()
        elif choice == '2':
            status = self._select_goal_status()
            goals = self.db.get_goals_by_status(status)
        elif choice == '3':
            category = self._select_category()
            goals = self.db.get_goals_by_category(category)
        elif choice == '4':
            goals = self.db.get_all_goals()
            goals = [g for g in goals if g.priority == self._select_priority()]
        else:
            print("❌ Invalid choice.")
            return
        
        if not goals:
            print("📭 No goals found.")
            return
        
        # Display goals
        self._display_goals_table(goals)
        
        # Option to view details
        if get_user_input("\nView goal details? (y/n)", default="n").lower() == 'y':
            self._view_goal_details(goals)
    
    def _display_goals_table(self, goals: List[Goal]):
        """Display goals in a formatted table"""
        print(f"\n📊 Found {len(goals)} goals:")
        print("-" * 100)
        print(f"{'#':<3} {'Title':<25} {'Category':<20} {'Priority':<8} {'Status':<12} {'Progress':<8}")
        print("-" * 100)
        
        for i, goal in enumerate(goals, 1):
            progress_bar = create_progress_bar(goal.progress_percentage, 8)
            print(f"{i:<3} {goal.title[:24]:<25} {goal.category.value[:19]:<20} "
                  f"{'🔥' if goal.priority == Priority.HIGH else '⭐' if goal.priority == Priority.MEDIUM else '📌':<8} "
                  f"{goal.status.value[:11]:<12} {progress_bar}")
    
    # Habit Management
    def _habit_management_menu(self):
        """Habit management submenu"""
        while True:
            print("\n" + "="*50)
            print("🔄 HABIT TRACKING")
            print("="*50)
            print("1. ➕ Create New Habit")
            print("2. 📋 View All Habits")
            print("3. ✅ Mark Habit Complete")
            print("4. 📊 Habit Analytics")
            print("5. 🧠 Get Habit Optimization")
            print("6. ⚙️  Edit Habit")
            print("7. 📈 View Habit History")
            print("8. 🏠 Back to Main Menu")
            
            choice = input("\nChoose an option (1-8): ").strip()
            
            if choice == '1':
                self._create_habit()
            elif choice == '2':
                self._view_habits()
            elif choice == '3':
                self._mark_habit_complete()
            elif choice == '4':
                self._show_habit_analytics()
            elif choice == '5':
                self._get_habit_optimization()
            elif choice == '6':
                self._edit_habit()
            elif choice == '7':
                self._view_habit_history()
            elif choice == '8':
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def _create_habit(self):
        """Create a new habit with intelligent guidance"""
        print("\n🔄 CREATE NEW HABIT")
        print("-" * 30)
        
        # Basic information
        title = get_user_input("Habit title", required=True)
        description = get_user_input("Description (optional)")
        
        # Category
        category = self._select_category()
        priority = self._select_priority()
        difficulty = self._select_difficulty()
        
        # Frequency and scheduling
        frequency = self._select_habit_frequency()
        target_days_per_week = 7
        
        if frequency == HabitFrequency.WEEKLY:
            target_days_per_week = self._get_optional_int("Days per week", default=3, min_val=1, max_val=7)
        elif frequency == HabitFrequency.CUSTOM:
            target_days_per_week = self._get_optional_int("Days per week", default=5, min_val=1, max_val=7)
        
        # Habit design (following best practices)
        print("\n🎯 Let's design this habit for success:")
        trigger_cue = get_user_input("Trigger/Cue (what will remind you?)")
        reward = get_user_input("Reward (how will you celebrate?)")
        environment_setup = get_user_input("Environment setup needed?")
        
        preferred_time = get_user_input("Preferred time (e.g., '07:00', 'morning')")
        duration_minutes = self._get_optional_int("Duration in minutes")
        
        # Create habit
        habit = Habit(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            category=category,
            priority=priority,
            difficulty=difficulty,
            frequency=frequency,
            target_days_per_week=target_days_per_week,
            preferred_time=preferred_time,
            duration_minutes=duration_minutes,
            trigger_cue=trigger_cue,
            reward=reward,
            environment_setup=environment_setup
        )
        
        # Save habit
        if self.db.create_habit(habit):
            print(f"\n✅ Habit '{title}' created successfully!")
            
            # Show success probability
            success_prob = self.intelligence.predict_habit_success_probability(habit)
            print(f"🎯 Success Probability: {success_prob:.1%}")
            
            # Show optimization tips
            tips = self.intelligence.suggest_habit_optimization(habit)
            if tips:
                print("\n💡 OPTIMIZATION TIPS:")
                for tip in tips:
                    print(f"• {tip}")
        else:
            print("❌ Failed to create habit. Please try again.")
    
    def _view_habits(self):
        """View habits with their current status"""
        print("\n📋 HABITS OVERVIEW")
        print("-" * 30)
        
        habits = self.db.get_all_habits()
        if not habits:
            print("📭 No habits found. Create your first habit!")
            return
        
        active_habits = [h for h in habits if h.is_active]
        inactive_habits = [h for h in habits if not h.is_active]
        
        print(f"\n🟢 ACTIVE HABITS ({len(active_habits)}):")
        self._display_habits_table(active_habits)
        
        if inactive_habits:
            print(f"\n⚪ INACTIVE HABITS ({len(inactive_habits)}):")
            self._display_habits_table(inactive_habits)
    
    def _display_habits_table(self, habits: List[Habit]):
        """Display habits in a formatted table"""
        if not habits:
            return
            
        print("-" * 110)
        print(f"{'#':<3} {'Title':<20} {'Category':<18} {'Streak':<8} {'Rate':<8} {'Difficulty':<10} {'Status':<8}")
        print("-" * 110)
        
        for i, habit in enumerate(habits, 1):
            status_icon = "🔥" if habit.current_streak > 7 else "✅" if habit.current_streak > 0 else "⭕"
            difficulty_stars = "⭐" * habit.difficulty.value
            
            rate_str = f"{habit.completion_rate:.1f}%"[:6]
            print(f"{i:<3} {habit.title[:19]:<20} {habit.category.value[:17]:<18} "
                  f"{habit.current_streak:<8} {rate_str:<7} "
                  f"{difficulty_stars:<10} {status_icon:<8}")
    
    def _mark_habit_complete(self):
        """Mark a habit as completed for today"""
        active_habits = self.db.get_active_habits()
        if not active_habits:
            print("📭 No active habits found.")
            return
        
        print("\n✅ MARK HABIT COMPLETE")
        print("-" * 30)
        
        # Show today's completion status
        today = date.today()
        daily_entry = self.db.get_daily_entry(today)
        completed_today = daily_entry.completed_habits if daily_entry else []
        
        print("Select a habit to mark complete:")
        for i, habit in enumerate(active_habits, 1):
            status = "✅" if habit.id in completed_today else "⭕"
            print(f"{i:2d}. {status} {habit.title}")
        
        try:
            choice = int(input("\nHabit number: ")) - 1
            if 0 <= choice < len(active_habits):
                habit = active_habits[choice]
                
                if habit.id in completed_today:
                    print("✅ This habit is already marked complete for today!")
                    return
                
                # Record completion
                completion_time = datetime.now().strftime("%H:%M")
                notes = get_user_input("Notes (optional)")
                
                if self.db.record_habit_completion(habit.id, today, completion_time, notes):
                    print(f"🎉 Great job! '{habit.title}' marked complete!")
                    
                    # Update daily entry
                    if not daily_entry:
                        daily_entry = DailyEntry(date=today)
                    
                    daily_entry.completed_habits.append(habit.id)
                    self.db.create_daily_entry(daily_entry)
                    
                    # Show updated streak
                    updated_habit = self.db.get_habit(habit.id)
                    if updated_habit:
                        print(f"🔥 Current streak: {updated_habit.current_streak} days!")
                        
                        if updated_habit.current_streak > updated_habit.longest_streak:
                            print("🏆 NEW PERSONAL RECORD! 🏆")
                else:
                    print("❌ Failed to record completion. Please try again.")
            else:
                print("❌ Invalid habit number.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    # Daily Planning
    def _daily_planning_menu(self):
        """Daily planning and reflection submenu"""
        while True:
            print("\n" + "="*50)
            print("📅 DAILY PLANNING")
            print("="*50)
            print("1. 🌅 Today's Focus")
            print("2. ✍️  Daily Reflection")
            print("3. 📊 Wellness Check-in")
            print("4. 🎯 Set Tomorrow's Priorities")
            print("5. 📈 Weekly Review")
            print("6. 📋 View Past Entries")
            print("7. 🏠 Back to Main Menu")
            
            choice = input("\nChoose an option (1-7): ").strip()
            
            if choice == '1':
                self._todays_focus()
            elif choice == '2':
                self._daily_reflection()
            elif choice == '3':
                self._wellness_checkin()
            elif choice == '4':
                self._set_tomorrow_priorities()
            elif choice == '5':
                self._weekly_review()
            elif choice == '6':
                self._view_past_entries()
            elif choice == '7':
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def _todays_focus(self):
        """Show today's focus and priorities"""
        today = date.today()
        print(f"\n🌅 TODAY'S FOCUS - {today.strftime('%A, %B %d, %Y')}")
        print("=" * 50)
        
        # Show prioritized goals
        active_goals = self.db.get_goals_by_status(GoalStatus.IN_PROGRESS)
        if active_goals:
            prioritized = self.intelligence.suggest_goal_prioritization(active_goals)
            print("🎯 TOP PRIORITY GOALS:")
            for i, goal in enumerate(prioritized[:3], 1):
                print(f"{i}. {goal.title} ({goal.progress_percentage:.0f}% complete)")
        
        # Show habits for today
        active_habits = self.db.get_active_habits()
        daily_entry = self.db.get_daily_entry(today)
        completed_today = daily_entry.completed_habits if daily_entry else []
        
        if active_habits:
            print("\n🔄 TODAY'S HABITS:")
            for habit in active_habits:
                status = "✅" if habit.id in completed_today else "⭕"
                print(f"{status} {habit.title}")
        
        # Show yesterday's priorities if set
        yesterday = today - timedelta(days=1)
        yesterday_entry = self.db.get_daily_entry(yesterday)
        if yesterday_entry and yesterday_entry.tomorrow_priorities:
            print("\n📋 PRIORITIES SET YESTERDAY:")
            for priority in yesterday_entry.tomorrow_priorities:
                print(f"• {priority}")
    
    # Analytics and Insights
    def _analytics_and_insights_menu(self):
        """Analytics and insights submenu"""
        while True:
            print("\n" + "="*50)
            print("📊 ANALYTICS & INSIGHTS")
            print("="*50)
            print("1. 🎯 Goal Analytics")
            print("2. 🔄 Habit Analytics")
            print("3. 🧠 AI Insights")
            print("4. 📈 Life Score")
            print("5. 📊 Progress Dashboard")
            print("6. 🔍 Deep Analysis")
            print("7. 🏠 Back to Main Menu")
            
            choice = input("\nChoose an option (1-7): ").strip()
            
            if choice == '1':
                self._show_goal_analytics()
            elif choice == '2':
                self._show_habit_analytics()
            elif choice == '3':
                self._show_ai_insights()
            elif choice == '4':
                self._show_life_score()
            elif choice == '5':
                self._show_progress_dashboard()
            elif choice == '6':
                self._deep_analysis()
            elif choice == '7':
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def _show_ai_insights(self):
        """Display AI-generated insights and recommendations"""
        print("\n🧠 AI INSIGHTS & RECOMMENDATIONS")
        print("=" * 50)
        
        insights = self.intelligence.generate_intelligent_insights()
        
        if not insights:
            print("✨ Great job! No urgent insights at the moment.")
            print("   Keep up the excellent work with your goals and habits!")
            return
        
        # Group insights by type
        insights_by_type = {}
        for insight in insights:
            if insight.insight_type not in insights_by_type:
                insights_by_type[insight.insight_type] = []
            insights_by_type[insight.insight_type].append(insight)
        
        # Display by priority
        type_icons = {
            "warning": "⚠️",
            "recommendation": "💡",
            "celebration": "🎉",
            "pattern": "📊"
        }
        
        for insight_type, type_insights in insights_by_type.items():
            icon = type_icons.get(insight_type, "📝")
            print(f"\n{icon} {insight_type.upper()} INSIGHTS:")
            print("-" * 40)
            
            for insight in type_insights:
                priority_icon = "🔥" if insight.priority == Priority.HIGH else "⭐" if insight.priority == Priority.MEDIUM else "📌"
                print(f"\n{priority_icon} {insight.title}")
                print(f"   {insight.description}")
                print(f"   Confidence: {insight.confidence_score:.0%}")
                
                if insight.action_items:
                    print("   💡 Action Items:")
                    for item in insight.action_items:
                        print(f"   • {item}")
                print()
    
    # Helper methods
    def _setup_first_time_user(self):
        """Setup for first-time users"""
        print("\n🎉 Welcome to the Life Planning System!")
        print("Let's set up your profile to get started.")
        print("-" * 50)
        
        name = get_user_input("Your name", required=True)
        
        print("\nSelect your primary life focus areas (up to 5):")
        categories = list(LifeCategory)
        for i, cat in enumerate(categories, 1):
            print(f"{i:2d}. {cat.value}")
        
        focus_areas = []
        while len(focus_areas) < 5:
            try:
                choices = input(f"\nEnter category numbers (comma-separated, {5-len(focus_areas)} remaining): ")
                if not choices.strip():
                    break
                    
                for choice in choices.split(','):
                    choice_num = int(choice.strip())
                    if 1 <= choice_num <= len(categories):
                        category = categories[choice_num - 1]
                        if category not in focus_areas:
                            focus_areas.append(category)
                break
            except ValueError:
                print("❌ Please enter valid numbers.")
        
        # Life vision
        life_vision = get_user_input("Your life vision (optional)")
        
        # Core values
        print("\nList your core values (comma-separated, optional):")
        values_input = get_user_input("Core values")
        core_values = [v.strip() for v in values_input.split(',')] if values_input else []
        
        # Create profile
        profile = UserProfile(
            name=name,
            primary_life_focuses=focus_areas,
            life_vision=life_vision,
            core_values=core_values
        )
        
        if self.db.create_user_profile(profile):
            self.current_user = profile
            print(f"\n✅ Welcome, {name}! Your profile has been created.")
            print("🚀 You're all set to start planning your amazing life!")
        else:
            print("❌ Failed to create profile. Please try again.")
    
    def _select_category(self) -> LifeCategory:
        """Helper to select a life category"""
        categories = list(LifeCategory)
        print("\nSelect category:")
        for i, cat in enumerate(categories, 1):
            print(f"{i:2d}. {cat.value}")
        
        while True:
            try:
                choice = int(input("Category: "))
                if 1 <= choice <= len(categories):
                    return categories[choice - 1]
                else:
                    print("❌ Invalid choice.")
            except ValueError:
                print("❌ Please enter a number.")
    
    def _select_priority(self) -> Priority:
        """Helper to select priority level"""
        priorities = list(Priority)
        print("\nSelect priority:")
        for i, priority in enumerate(priorities, 1):
            print(f"{i}. {priority.name.title()}")
        
        while True:
            try:
                choice = int(input("Priority: "))
                if 1 <= choice <= len(priorities):
                    return priorities[choice - 1]
                else:
                    print("❌ Invalid choice.")
            except ValueError:
                print("❌ Please enter a number.")
    
    def _select_difficulty(self) -> Difficulty:
        """Helper to select difficulty level"""
        difficulties = list(Difficulty)
        print("\nSelect difficulty:")
        for i, diff in enumerate(difficulties, 1):
            stars = "⭐" * diff.value
            print(f"{i}. {diff.name.replace('_', ' ').title()} {stars}")
        
        while True:
            try:
                choice = int(input("Difficulty: "))
                if 1 <= choice <= len(difficulties):
                    return difficulties[choice - 1]
                else:
                    print("❌ Invalid choice.")
            except ValueError:
                print("❌ Please enter a number.")
    
    def _get_target_date(self) -> Optional[date]:
        """Helper to get target date"""
        date_input = get_user_input("Target date (YYYY-MM-DD, optional)")
        if not date_input:
            return None
        
        try:
            return date.fromisoformat(date_input)
        except ValueError:
            print("❌ Invalid date format. Skipping target date.")
            return None
    
    def _get_optional_float(self, prompt: str) -> Optional[float]:
        """Helper to get optional float input"""
        value_input = get_user_input(f"{prompt} (optional)")
        if not value_input:
            return None
        
        try:
            return float(value_input)
        except ValueError:
            print("❌ Invalid number. Skipping.")
            return None
    
    def _get_optional_int(self, prompt: str, default: Optional[int] = None, 
                         min_val: Optional[int] = None, max_val: Optional[int] = None) -> Optional[int]:
        """Helper to get optional integer input"""
        default_text = f" (default: {default})" if default is not None else ""
        value_input = get_user_input(f"{prompt}{default_text}")
        
        if not value_input and default is not None:
            return default
        elif not value_input:
            return None
        
        try:
            value = int(value_input)
            if min_val is not None and value < min_val:
                print(f"❌ Value must be at least {min_val}.")
                return default
            if max_val is not None and value > max_val:
                print(f"❌ Value must be at most {max_val}.")
                return default
            return value
        except ValueError:
            print("❌ Invalid number.")
            return default
    
    # Placeholder methods for remaining functionality
    def _add_action_steps(self, goal: Goal):
        """Add action steps to a goal"""
        print("\n✏️ Add action steps (press Enter twice to finish):")
        steps = []
        while True:
            step = input(f"Step {len(steps) + 1}: ").strip()
            if not step:
                break
            steps.append(step)
        goal.action_steps = steps
    
    def _select_goal_status(self) -> GoalStatus:
        """Helper to select goal status"""
        statuses = list(GoalStatus)
        for i, status in enumerate(statuses, 1):
            print(f"{i}. {status.value}")
        
        while True:
            try:
                choice = int(input("Status: "))
                if 1 <= choice <= len(statuses):
                    return statuses[choice - 1]
                else:
                    print("❌ Invalid choice.")
            except ValueError:
                print("❌ Please enter a number.")
    
    def _select_habit_frequency(self) -> HabitFrequency:
        """Helper to select habit frequency"""
        frequencies = list(HabitFrequency)
        for i, freq in enumerate(frequencies, 1):
            print(f"{i}. {freq.value}")
        
        while True:
            try:
                choice = int(input("Frequency: "))
                if 1 <= choice <= len(frequencies):
                    return frequencies[choice - 1]
                else:
                    print("❌ Invalid choice.")
            except ValueError:
                print("❌ Please enter a number.")
    
    # Stub methods (to be implemented)
    def _edit_goal(self): pass
    def _update_goal_progress(self): pass
    def _complete_goal(self): pass
    def _get_goal_suggestions(self): pass
    def _prioritize_goals(self): pass
    def _view_goal_details(self, goals): pass
    def _edit_habit(self): pass
    def _view_habit_history(self): pass
    def _get_habit_optimization(self): pass
    def _show_habit_analytics(self): pass
    def _daily_reflection(self): pass
    def _wellness_checkin(self): pass
    def _set_tomorrow_priorities(self): pass
    def _weekly_review(self): pass
    def _view_past_entries(self): pass
    def _show_goal_analytics(self): pass
    def _show_life_score(self): pass
    def _show_progress_dashboard(self): pass
    def _deep_analysis(self): pass
    def _life_assessment_menu(self): pass
    def _settings_menu(self): pass
    def _data_management_menu(self): pass


def main():
    """Main entry point"""
    try:
        app = LifePlannerApp()
        app.run()
    except Exception as e:
        print(f"❌ Critical error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()