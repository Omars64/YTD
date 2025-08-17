"""
Intelligence Engine for Life Planning System

This module provides intelligent algorithms for goal optimization, habit formation,
analytics, insights, and personalized recommendations to help users achieve their life goals.
"""

import math
import statistics
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple, Any
from collections import defaultdict, Counter
from dataclasses import dataclass

from models import Goal, Habit, DailyEntry, LifeAssessment, LifeCategory, Priority, GoalStatus, Difficulty
from database import DatabaseManager


@dataclass
class Insight:
    """Represents an intelligent insight or recommendation"""
    title: str
    description: str
    category: LifeCategory
    priority: Priority
    action_items: List[str]
    confidence_score: float  # 0.0 to 1.0
    insight_type: str  # "pattern", "recommendation", "warning", "celebration"


@dataclass
class ProgressAnalytics:
    """Analytics data for progress tracking"""
    total_goals: int
    completed_goals: int
    in_progress_goals: int
    completion_rate: float
    average_completion_time: Optional[float]
    most_productive_category: Optional[LifeCategory]
    least_productive_category: Optional[LifeCategory]
    goal_difficulty_distribution: Dict[Difficulty, int]
    monthly_completion_trend: List[Tuple[str, int]]


@dataclass
class HabitAnalytics:
    """Analytics data for habit tracking"""
    total_habits: int
    active_habits: int
    average_streak: float
    best_performing_habits: List[str]
    struggling_habits: List[str]
    completion_rate_by_category: Dict[LifeCategory, float]
    weekly_consistency_score: float
    habit_difficulty_vs_success: Dict[Difficulty, float]


@dataclass
class LifeScore:
    """Comprehensive life satisfaction scoring"""
    overall_score: float
    category_scores: Dict[LifeCategory, float]
    trend: str  # "improving", "declining", "stable"
    strengths: List[LifeCategory]
    focus_areas: List[LifeCategory]
    balance_score: float  # How balanced life is across categories


class IntelligenceEngine:
    """Core intelligence engine for life planning optimization"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    # Goal Intelligence
    def suggest_goal_breakdown(self, goal: Goal) -> List[str]:
        """Suggest intelligent breakdown of a goal into actionable steps"""
        suggestions = []
        
        # Time-based breakdown
        if goal.target_date:
            days_remaining = (goal.target_date - date.today()).days
            if days_remaining > 90:
                suggestions.append("Break this long-term goal into quarterly milestones")
            elif days_remaining > 30:
                suggestions.append("Create weekly checkpoints to track progress")
            else:
                suggestions.append("Define daily actions to achieve this goal")
        
        # Difficulty-based suggestions
        if goal.difficulty == Difficulty.VERY_HARD:
            suggestions.extend([
                "Start with the smallest possible step to build momentum",
                "Identify potential obstacles and create contingency plans",
                "Consider finding an accountability partner or mentor"
            ])
        elif goal.difficulty == Difficulty.HARD:
            suggestions.extend([
                "Break into 3-5 major milestones",
                "Allocate buffer time for unexpected challenges"
            ])
        
        # Category-specific suggestions
        category_suggestions = {
            LifeCategory.HEALTH_FITNESS: [
                "Set specific, measurable targets (e.g., walk 10,000 steps daily)",
                "Plan your workout schedule in advance",
                "Track nutrition and sleep patterns"
            ],
            LifeCategory.CAREER_EDUCATION: [
                "Identify required skills and create learning plan",
                "Network with professionals in your target field",
                "Set up regular progress reviews with mentor/supervisor"
            ],
            LifeCategory.FINANCES: [
                "Create a detailed budget breakdown",
                "Set up automatic savings transfers",
                "Track expenses weekly"
            ],
            LifeCategory.RELATIONSHIPS: [
                "Schedule regular quality time",
                "Practice active listening techniques",
                "Express appreciation daily"
            ]
        }
        
        if goal.category in category_suggestions:
            suggestions.extend(category_suggestions[goal.category][:2])
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def calculate_goal_difficulty_score(self, goal: Goal) -> float:
        """Calculate intelligent difficulty score based on multiple factors"""
        base_score = goal.difficulty.value * 0.2  # 0.2 to 1.0
        
        # Time pressure factor
        if goal.target_date:
            days_remaining = (goal.target_date - date.today()).days
            if days_remaining < 7:
                base_score += 0.3
            elif days_remaining < 30:
                base_score += 0.2
            elif days_remaining < 90:
                base_score += 0.1
        
        # Complexity factor (based on action steps)
        action_steps_count = len(goal.action_steps)
        if action_steps_count > 10:
            base_score += 0.2
        elif action_steps_count > 5:
            base_score += 0.1
        
        # Resource requirement factor
        if len(goal.required_resources) > 3:
            base_score += 0.1
        
        return min(1.0, base_score)
    
    def suggest_goal_prioritization(self, goals: List[Goal]) -> List[Goal]:
        """Intelligently prioritize goals based on multiple factors"""
        def priority_score(goal: Goal) -> float:
            score = 0.0
            
            # Base priority
            score += goal.priority.value * 25
            
            # Urgency (time pressure)
            if goal.target_date:
                days_remaining = (goal.target_date - date.today()).days
                if days_remaining <= 7:
                    score += 50
                elif days_remaining <= 30:
                    score += 30
                elif days_remaining <= 90:
                    score += 15
            
            # Progress momentum
            if goal.progress_percentage > 50:
                score += 20  # Boost goals that are well underway
            elif goal.progress_percentage > 0:
                score += 10
            
            # Inverse difficulty bonus (easier goals get slight boost)
            score += (6 - goal.difficulty.value) * 5
            
            # Status penalty for stalled goals
            if goal.status == GoalStatus.ON_HOLD:
                score -= 30
            elif goal.status == GoalStatus.NOT_STARTED and goal.created_date < datetime.now() - timedelta(days=30):
                score -= 20
            
            return score
        
        return sorted(goals, key=priority_score, reverse=True)
    
    # Habit Intelligence
    def analyze_habit_success_factors(self, habit: Habit) -> Dict[str, Any]:
        """Analyze factors contributing to habit success/failure"""
        completions = self.db.get_habit_completions(habit.id)
        
        analysis = {
            "success_rate": habit.completion_rate,
            "streak_consistency": habit.current_streak / max(1, habit.longest_streak),
            "completion_pattern": self._analyze_completion_pattern(completions),
            "optimal_timing": self._find_optimal_habit_timing(completions),
            "success_factors": [],
            "improvement_suggestions": []
        }
        
        # Success factors analysis
        if habit.completion_rate > 80:
            analysis["success_factors"].extend([
                "Excellent consistency",
                "Well-established routine"
            ])
        elif habit.completion_rate > 60:
            analysis["success_factors"].append("Good habit foundation")
        
        if habit.current_streak > 7:
            analysis["success_factors"].append("Strong current momentum")
        
        # Improvement suggestions
        if habit.completion_rate < 50:
            analysis["improvement_suggestions"].extend([
                "Consider reducing difficulty or frequency",
                "Strengthen the habit trigger/cue",
                "Add a more immediate reward"
            ])
        
        if habit.current_streak == 0:
            analysis["improvement_suggestions"].extend([
                "Focus on consistency over intensity",
                "Start with the minimum viable habit"
            ])
        
        if not habit.trigger_cue:
            analysis["improvement_suggestions"].append("Define a clear trigger cue")
        
        if not habit.reward:
            analysis["improvement_suggestions"].append("Set up an immediate reward")
        
        return analysis
    
    def suggest_habit_optimization(self, habit: Habit) -> List[str]:
        """Suggest optimizations for habit formation"""
        suggestions = []
        
        # Based on completion rate
        if habit.completion_rate < 30:
            suggestions.extend([
                "Start smaller - reduce the habit to just 1-2 minutes",
                "Attach this habit to an existing strong habit (habit stacking)",
                "Remove all friction - make it as easy as possible"
            ])
        elif habit.completion_rate < 60:
            suggestions.extend([
                "Optimize your environment to make the habit obvious",
                "Set up a clear reward system",
                "Track your progress visually (calendar, chart)"
            ])
        
        # Based on streak performance
        if habit.longest_streak < 7:
            suggestions.append("Focus on building a 7-day streak before increasing intensity")
        elif habit.current_streak < habit.longest_streak * 0.5:
            suggestions.append("Review what made your longest streak successful and replicate it")
        
        # Based on difficulty vs success
        difficulty_vs_success = habit.completion_rate / (habit.difficulty.value * 20)
        if difficulty_vs_success < 0.8:
            suggestions.append("Consider reducing the difficulty level to build consistency first")
        
        # Time-based suggestions
        if habit.preferred_time:
            completions = self.db.get_habit_completions(habit.id)
            if completions:
                best_times = self._find_optimal_habit_timing(completions)
                if best_times and habit.preferred_time not in best_times[:2]:
                    suggestions.append(f"Consider shifting to {best_times[0]} - your most successful time")
        
        return suggestions[:4]  # Return top 4 suggestions
    
    def predict_habit_success_probability(self, habit: Habit) -> float:
        """Predict probability of habit success based on current patterns"""
        factors = []
        
        # Completion rate factor
        factors.append(habit.completion_rate / 100.0)
        
        # Streak momentum factor
        if habit.longest_streak > 0:
            streak_factor = min(1.0, habit.current_streak / habit.longest_streak)
            factors.append(streak_factor)
        
        # Difficulty alignment factor
        expected_success_rate = max(0.2, 1.0 - (habit.difficulty.value - 1) * 0.15)
        alignment_factor = min(1.0, habit.completion_rate / (expected_success_rate * 100))
        factors.append(alignment_factor)
        
        # Time since creation factor (habits get easier with time)
        days_since_creation = (date.today() - habit.created_date.date()).days
        time_factor = min(1.0, days_since_creation / 66)  # 66 days for habit formation
        factors.append(time_factor)
        
        # Environmental factors
        env_factor = 0.7  # Base environmental factor
        if habit.trigger_cue:
            env_factor += 0.1
        if habit.reward:
            env_factor += 0.1
        if habit.environment_setup:
            env_factor += 0.1
        factors.append(min(1.0, env_factor))
        
        return statistics.mean(factors)
    
    # Analytics and Insights
    def generate_progress_analytics(self) -> ProgressAnalytics:
        """Generate comprehensive progress analytics"""
        goals = self.db.get_all_goals()
        
        if not goals:
            return ProgressAnalytics(0, 0, 0, 0.0, None, None, None, {}, [])
        
        completed_goals = [g for g in goals if g.status == GoalStatus.COMPLETED]
        in_progress_goals = [g for g in goals if g.status == GoalStatus.IN_PROGRESS]
        
        # Basic stats
        total_goals = len(goals)
        completed_count = len(completed_goals)
        in_progress_count = len(in_progress_goals)
        completion_rate = (completed_count / total_goals) * 100
        
        # Average completion time
        completion_times = []
        for goal in completed_goals:
            if goal.completion_date:
                days = (goal.completion_date.date() - goal.created_date.date()).days
                completion_times.append(days)
        
        avg_completion_time = statistics.mean(completion_times) if completion_times else None
        
        # Category analysis
        category_completed = Counter(g.category for g in completed_goals)
        category_total = Counter(g.category for g in goals)
        
        category_rates = {}
        for category in LifeCategory:
            if category_total[category] > 0:
                rate = (category_completed[category] / category_total[category]) * 100
                category_rates[category] = rate
        
        most_productive = max(category_rates.items(), key=lambda x: x[1])[0] if category_rates else None
        least_productive = min(category_rates.items(), key=lambda x: x[1])[0] if category_rates else None
        
        # Difficulty distribution
        difficulty_dist = Counter(g.difficulty for g in goals)
        
        # Monthly trend (last 12 months)
        monthly_trend = []
        for i in range(12):
            month_start = date.today().replace(day=1) - timedelta(days=i*30)
            month_end = month_start + timedelta(days=30)
            month_completed = len([g for g in completed_goals 
                                 if g.completion_date and 
                                 month_start <= g.completion_date.date() <= month_end])
            monthly_trend.append((month_start.strftime("%Y-%m"), month_completed))
        
        return ProgressAnalytics(
            total_goals=total_goals,
            completed_goals=completed_count,
            in_progress_goals=in_progress_count,
            completion_rate=completion_rate,
            average_completion_time=avg_completion_time,
            most_productive_category=most_productive,
            least_productive_category=least_productive,
            goal_difficulty_distribution=dict(difficulty_dist),
            monthly_completion_trend=monthly_trend
        )
    
    def generate_habit_analytics(self) -> HabitAnalytics:
        """Generate comprehensive habit analytics"""
        habits = self.db.get_all_habits()
        active_habits = [h for h in habits if h.is_active]
        
        if not habits:
            return HabitAnalytics(0, 0, 0.0, [], [], {}, 0.0, {})
        
        # Basic stats
        total_habits = len(habits)
        active_count = len(active_habits)
        avg_streak = statistics.mean([h.current_streak for h in active_habits]) if active_habits else 0.0
        
        # Best and struggling habits
        sorted_habits = sorted(active_habits, key=lambda h: h.completion_rate, reverse=True)
        best_performing = [h.title for h in sorted_habits[:3]]
        struggling = [h.title for h in sorted_habits[-3:] if h.completion_rate < 60]
        
        # Completion rate by category
        category_rates = {}
        for category in LifeCategory:
            cat_habits = [h for h in active_habits if h.category == category]
            if cat_habits:
                avg_rate = statistics.mean([h.completion_rate for h in cat_habits])
                category_rates[category] = avg_rate
        
        # Weekly consistency score
        weekly_scores = []
        for habit in active_habits:
            if habit.completion_rate > 0:
                # Calculate consistency based on streak vs total days
                days_active = (date.today() - habit.created_date.date()).days
                consistency = min(1.0, habit.current_streak / max(1, days_active))
                weekly_scores.append(consistency)
        
        weekly_consistency = statistics.mean(weekly_scores) if weekly_scores else 0.0
        
        # Difficulty vs success analysis
        difficulty_success = {}
        for difficulty in Difficulty:
            diff_habits = [h for h in active_habits if h.difficulty == difficulty]
            if diff_habits:
                avg_success = statistics.mean([h.completion_rate for h in diff_habits])
                difficulty_success[difficulty] = avg_success
        
        return HabitAnalytics(
            total_habits=total_habits,
            active_habits=active_count,
            average_streak=avg_streak,
            best_performing_habits=best_performing,
            struggling_habits=struggling,
            completion_rate_by_category=category_rates,
            weekly_consistency_score=weekly_consistency * 100,
            habit_difficulty_vs_success=difficulty_success
        )
    
    def calculate_life_score(self) -> LifeScore:
        """Calculate comprehensive life satisfaction score"""
        # Get recent assessments
        assessments = self.db.get_life_assessments()
        recent_assessments = [a for a in assessments if a.date >= date.today() - timedelta(days=90)]
        
        if not recent_assessments:
            # Default scoring based on goals and habits performance
            return self._calculate_life_score_from_performance()
        
        # Use most recent assessment as base
        latest = recent_assessments[0]
        
        # Calculate category scores
        category_scores = {}
        overall_scores = []
        
        for category in LifeCategory:
            if category in latest.category_ratings:
                score = latest.category_ratings[category] / 10.0
                category_scores[category] = score
                overall_scores.append(score)
        
        overall_score = statistics.mean(overall_scores) if overall_scores else 0.5
        
        # Determine trend
        trend = "stable"
        if len(recent_assessments) >= 2:
            prev_score = statistics.mean([r / 10.0 for r in recent_assessments[1].category_ratings.values()])
            if overall_score > prev_score + 0.1:
                trend = "improving"
            elif overall_score < prev_score - 0.1:
                trend = "declining"
        
        # Identify strengths and focus areas
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        strengths = [cat for cat, score in sorted_categories[:3] if score > 0.7]
        focus_areas = [cat for cat, score in sorted_categories[-3:] if score < 0.6]
        
        # Calculate balance score (how evenly distributed across categories)
        if category_scores:
            scores = list(category_scores.values())
            balance_score = 1.0 - (statistics.stdev(scores) / statistics.mean(scores))
            balance_score = max(0.0, min(1.0, balance_score))
        else:
            balance_score = 0.0
        
        return LifeScore(
            overall_score=overall_score,
            category_scores=category_scores,
            trend=trend,
            strengths=strengths,
            focus_areas=focus_areas,
            balance_score=balance_score
        )
    
    def generate_intelligent_insights(self) -> List[Insight]:
        """Generate intelligent insights and recommendations"""
        insights = []
        
        # Goal insights
        goals = self.db.get_all_goals()
        if goals:
            insights.extend(self._generate_goal_insights(goals))
        
        # Habit insights
        habits = self.db.get_all_habits()
        if habits:
            insights.extend(self._generate_habit_insights(habits))
        
        # Life balance insights
        life_score = self.calculate_life_score()
        insights.extend(self._generate_life_balance_insights(life_score))
        
        # Productivity insights
        insights.extend(self._generate_productivity_insights())
        
        # Sort by confidence score and priority
        insights.sort(key=lambda x: (x.priority.value, x.confidence_score), reverse=True)
        
        return insights[:10]  # Return top 10 insights
    
    # Helper methods
    def _analyze_completion_pattern(self, completions: List[Dict]) -> Dict[str, Any]:
        """Analyze patterns in habit completions"""
        if not completions:
            return {"pattern": "insufficient_data"}
        
        # Analyze by day of week
        day_counts = defaultdict(int)
        for completion in completions:
            comp_date = date.fromisoformat(completion['completion_date'])
            day_counts[comp_date.weekday()] += 1
        
        best_days = sorted(day_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "pattern": "day_of_week",
            "best_days": [day for day, count in best_days[:3]],
            "consistency_score": len(day_counts) / 7.0  # How many different days of week
        }
    
    def _find_optimal_habit_timing(self, completions: List[Dict]) -> List[str]:
        """Find optimal timing for habit based on completion history"""
        if not completions:
            return []
        
        time_counts = defaultdict(int)
        for completion in completions:
            if completion.get('completion_time'):
                # Extract hour from time string
                try:
                    hour = int(completion['completion_time'].split(':')[0])
                    if 5 <= hour < 12:
                        time_counts['morning'] += 1
                    elif 12 <= hour < 17:
                        time_counts['afternoon'] += 1
                    elif 17 <= hour < 21:
                        time_counts['evening'] += 1
                    else:
                        time_counts['night'] += 1
                except:
                    pass
        
        return sorted(time_counts.keys(), key=lambda x: time_counts[x], reverse=True)
    
    def _calculate_life_score_from_performance(self) -> LifeScore:
        """Calculate life score based on goals and habits performance when no assessments exist"""
        # Get performance metrics
        goal_analytics = self.generate_progress_analytics()
        habit_analytics = self.generate_habit_analytics()
        
        # Calculate base score from performance
        goal_score = goal_analytics.completion_rate / 100.0 if goal_analytics.completion_rate else 0.5
        habit_score = habit_analytics.weekly_consistency_score / 100.0 if habit_analytics.weekly_consistency_score else 0.5
        
        overall_score = statistics.mean([goal_score, habit_score])
        
        # Estimate category scores based on goal/habit distribution
        category_scores = {}
        goals = self.db.get_all_goals()
        habits = self.db.get_all_habits()
        
        for category in LifeCategory:
            cat_goals = [g for g in goals if g.category == category]
            cat_habits = [h for h in habits if h.category == category]
            
            if cat_goals or cat_habits:
                cat_score = overall_score  # Use overall as base
                # Adjust based on category-specific performance
                if cat_goals:
                    completed = len([g for g in cat_goals if g.status == GoalStatus.COMPLETED])
                    cat_goal_rate = completed / len(cat_goals)
                    cat_score = statistics.mean([cat_score, cat_goal_rate])
                
                category_scores[category] = cat_score
        
        return LifeScore(
            overall_score=overall_score,
            category_scores=category_scores,
            trend="stable",
            strengths=[],
            focus_areas=[],
            balance_score=0.5
        )
    
    def _generate_goal_insights(self, goals: List[Goal]) -> List[Insight]:
        """Generate insights about goals"""
        insights = []
        
        # Stalled goals insight
        stalled_goals = [g for g in goals if g.status == GoalStatus.IN_PROGRESS and 
                        (date.today() - g.created_date.date()).days > 30 and 
                        g.progress_percentage < 20]
        
        if stalled_goals:
            insights.append(Insight(
                title="Stalled Goals Detected",
                description=f"You have {len(stalled_goals)} goals that haven't progressed much in 30+ days",
                category=LifeCategory.PERSONAL_GROWTH,
                priority=Priority.HIGH,
                action_items=[
                    "Review and break down stalled goals into smaller steps",
                    "Consider if these goals are still relevant",
                    "Set weekly progress checkpoints"
                ],
                confidence_score=0.9,
                insight_type="warning"
            ))
        
        # Overcommitment insight
        high_priority_goals = [g for g in goals if g.priority == Priority.HIGH and 
                              g.status in [GoalStatus.NOT_STARTED, GoalStatus.IN_PROGRESS]]
        
        if len(high_priority_goals) > 5:
            insights.append(Insight(
                title="Potential Overcommitment",
                description=f"You have {len(high_priority_goals)} high-priority goals active",
                category=LifeCategory.PERSONAL_GROWTH,
                priority=Priority.MEDIUM,
                action_items=[
                    "Consider reducing to 3-5 high-priority goals",
                    "Move some goals to medium priority",
                    "Focus on completing current goals before adding new ones"
                ],
                confidence_score=0.8,
                insight_type="recommendation"
            ))
        
        return insights
    
    def _generate_habit_insights(self, habits: List[Habit]) -> List[Insight]:
        """Generate insights about habits"""
        insights = []
        
        # Low completion rate habits
        struggling_habits = [h for h in habits if h.is_active and h.completion_rate < 40]
        
        if struggling_habits:
            insights.append(Insight(
                title="Struggling Habits Need Attention",
                description=f"{len(struggling_habits)} habits have completion rates below 40%",
                category=LifeCategory.PERSONAL_GROWTH,
                priority=Priority.HIGH,
                action_items=[
                    "Reduce difficulty of struggling habits",
                    "Strengthen habit cues and rewards",
                    "Consider habit stacking with existing routines"
                ],
                confidence_score=0.85,
                insight_type="recommendation"
            ))
        
        # Excellent habit performance
        excellent_habits = [h for h in habits if h.is_active and h.completion_rate > 85]
        
        if excellent_habits:
            insights.append(Insight(
                title="Excellent Habit Performance!",
                description=f"You're crushing it with {len(excellent_habits)} habits above 85% completion",
                category=LifeCategory.PERSONAL_GROWTH,
                priority=Priority.LOW,
                action_items=[
                    "Consider adding complementary habits to successful ones",
                    "Share your success strategies",
                    "Gradually increase difficulty if desired"
                ],
                confidence_score=0.9,
                insight_type="celebration"
            ))
        
        return insights
    
    def _generate_life_balance_insights(self, life_score: LifeScore) -> List[Insight]:
        """Generate insights about life balance"""
        insights = []
        
        if life_score.balance_score < 0.6:
            insights.append(Insight(
                title="Life Balance Opportunity",
                description="Your life satisfaction varies significantly across different areas",
                category=LifeCategory.PERSONAL_GROWTH,
                priority=Priority.MEDIUM,
                action_items=[
                    "Focus more attention on neglected life areas",
                    "Set goals in your lowest-scoring categories",
                    "Consider reducing time in over-developed areas"
                ],
                confidence_score=0.7,
                insight_type="recommendation"
            ))
        
        if life_score.focus_areas:
            insights.append(Insight(
                title="Areas Needing Focus",
                description=f"These life areas could use more attention: {', '.join([area.value for area in life_score.focus_areas])}",
                category=life_score.focus_areas[0] if life_score.focus_areas else LifeCategory.PERSONAL_GROWTH,
                priority=Priority.MEDIUM,
                action_items=[
                    "Set specific goals in these areas",
                    "Create habits to support these life domains",
                    "Schedule regular time for these areas"
                ],
                confidence_score=0.8,
                insight_type="recommendation"
            ))
        
        return insights
    
    def _generate_productivity_insights(self) -> List[Insight]:
        """Generate insights about productivity patterns"""
        insights = []
        
        # Analyze daily entries for patterns
        recent_entries = self.db.get_daily_entries_range(
            date.today() - timedelta(days=30), 
            date.today()
        )
        
        if len(recent_entries) >= 7:
            # Energy level patterns
            energy_levels = [e.energy_level for e in recent_entries if e.energy_level]
            if energy_levels and statistics.mean(energy_levels) < 6:
                insights.append(Insight(
                    title="Low Energy Levels Detected",
                    description=f"Your average energy level is {statistics.mean(energy_levels):.1f}/10 over the last 30 days",
                    category=LifeCategory.HEALTH_FITNESS,
                    priority=Priority.HIGH,
                    action_items=[
                        "Review sleep quality and duration",
                        "Assess nutrition and exercise habits",
                        "Consider stress management techniques",
                        "Schedule energy-boosting activities"
                    ],
                    confidence_score=0.8,
                    insight_type="warning"
                ))
        
        return insights