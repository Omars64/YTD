"""
Utility Functions for Life Planning System

Common utilities for user interaction, data formatting, and display operations.
"""

import os
import json
import csv
from datetime import datetime, date
from typing import Any, List, Dict, Optional
import re


def get_user_input(prompt: str, required: bool = False, default: Optional[str] = None) -> str:
    """
    Get user input with validation and default values
    
    Args:
        prompt: The input prompt
        required: Whether input is required
        default: Default value if none provided
        
    Returns:
        User input string
    """
    default_text = f" [{default}]" if default else ""
    full_prompt = f"{prompt}{default_text}: "
    
    while True:
        user_input = input(full_prompt).strip()
        
        if user_input:
            return user_input
        elif default is not None:
            return default
        elif not required:
            return ""
        else:
            print("❌ This field is required. Please enter a value.")


def get_yes_no_input(prompt: str, default: bool = True) -> bool:
    """
    Get yes/no input from user
    
    Args:
        prompt: The question prompt
        default: Default value (True for yes, False for no)
        
    Returns:
        Boolean response
    """
    default_text = "Y/n" if default else "y/N"
    response = get_user_input(f"{prompt} ({default_text})", default="y" if default else "n")
    return response.lower() in ['y', 'yes', '1', 'true']


def get_numeric_input(prompt: str, min_val: Optional[float] = None, 
                     max_val: Optional[float] = None, input_type: type = int) -> Optional[float]:
    """
    Get numeric input with validation
    
    Args:
        prompt: The input prompt
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        input_type: int or float
        
    Returns:
        Numeric value or None if invalid
    """
    while True:
        user_input = get_user_input(prompt)
        if not user_input:
            return None
            
        try:
            value = input_type(user_input)
            
            if min_val is not None and value < min_val:
                print(f"❌ Value must be at least {min_val}")
                continue
                
            if max_val is not None and value > max_val:
                print(f"❌ Value must be at most {max_val}")
                continue
                
            return value
            
        except ValueError:
            print(f"❌ Please enter a valid {input_type.__name__}")


def get_rating_input(prompt: str, scale: int = 10) -> Optional[int]:
    """
    Get rating input on a scale (e.g., 1-10)
    
    Args:
        prompt: The input prompt
        scale: Maximum value on scale (minimum is always 1)
        
    Returns:
        Rating value or None
    """
    return get_numeric_input(f"{prompt} (1-{scale})", min_val=1, max_val=scale, input_type=int)


def create_progress_bar(percentage: float, width: int = 20, filled_char: str = "█", 
                       empty_char: str = "░") -> str:
    """
    Create a visual progress bar
    
    Args:
        percentage: Progress percentage (0-100)
        width: Width of the progress bar in characters
        filled_char: Character for filled portion
        empty_char: Character for empty portion
        
    Returns:
        Progress bar string
    """
    if percentage < 0:
        percentage = 0
    elif percentage > 100:
        percentage = 100
        
    filled_length = int(width * percentage / 100)
    empty_length = width - filled_length
    
    return f"{filled_char * filled_length}{empty_char * empty_length}"


def format_duration(minutes: int) -> str:
    """
    Format duration in minutes to human-readable format
    
    Args:
        minutes: Duration in minutes
        
    Returns:
        Formatted duration string
    """
    if minutes < 60:
        return f"{minutes}m"
    elif minutes < 1440:  # Less than 24 hours
        hours = minutes // 60
        remaining_minutes = minutes % 60
        if remaining_minutes == 0:
            return f"{hours}h"
        else:
            return f"{hours}h {remaining_minutes}m"
    else:  # 24 hours or more
        days = minutes // 1440
        remaining_hours = (minutes % 1440) // 60
        if remaining_hours == 0:
            return f"{days}d"
        else:
            return f"{days}d {remaining_hours}h"


def format_date_relative(target_date: date) -> str:
    """
    Format date relative to today
    
    Args:
        target_date: The date to format
        
    Returns:
        Relative date string
    """
    today = date.today()
    delta = (target_date - today).days
    
    if delta == 0:
        return "Today"
    elif delta == 1:
        return "Tomorrow"
    elif delta == -1:
        return "Yesterday"
    elif delta > 0:
        if delta <= 7:
            return f"In {delta} days"
        elif delta <= 30:
            weeks = delta // 7
            return f"In {weeks} week{'s' if weeks > 1 else ''}"
        elif delta <= 365:
            months = delta // 30
            return f"In {months} month{'s' if months > 1 else ''}"
        else:
            years = delta // 365
            return f"In {years} year{'s' if years > 1 else ''}"
    else:  # Past date
        delta = abs(delta)
        if delta <= 7:
            return f"{delta} days ago"
        elif delta <= 30:
            weeks = delta // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        elif delta <= 365:
            months = delta // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        else:
            years = delta // 365
            return f"{years} year{'s' if years > 1 else ''} ago"


def display_formatted_data(data: Dict[str, Any], title: str = "", indent: int = 0) -> None:
    """
    Display data in a formatted, readable way
    
    Args:
        data: Dictionary of data to display
        title: Optional title for the data section
        indent: Indentation level
    """
    indent_str = "  " * indent
    
    if title:
        print(f"{indent_str}{title}:")
        print(f"{indent_str}{'-' * len(title)}")
    
    for key, value in data.items():
        formatted_key = key.replace('_', ' ').title()
        
        if isinstance(value, dict):
            print(f"{indent_str}{formatted_key}:")
            display_formatted_data(value, indent=indent + 1)
        elif isinstance(value, list):
            if value:  # Non-empty list
                print(f"{indent_str}{formatted_key}:")
                for item in value:
                    if isinstance(item, dict):
                        display_formatted_data(item, indent=indent + 1)
                    else:
                        print(f"{indent_str}  • {item}")
            else:
                print(f"{indent_str}{formatted_key}: None")
        elif isinstance(value, (datetime, date)):
            print(f"{indent_str}{formatted_key}: {value.strftime('%Y-%m-%d %H:%M' if isinstance(value, datetime) else '%Y-%m-%d')}")
        elif isinstance(value, float):
            if key.endswith('_percentage') or key.endswith('_rate'):
                print(f"{indent_str}{formatted_key}: {value:.1f}%")
            else:
                print(f"{indent_str}{formatted_key}: {value:.2f}")
        elif value is None or value == "":
            print(f"{indent_str}{formatted_key}: Not set")
        else:
            print(f"{indent_str}{formatted_key}: {value}")


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to maximum length with suffix
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_list_display(items: List[str], max_items: int = 5, 
                       show_count: bool = True) -> str:
    """
    Format a list for display with optional truncation
    
    Args:
        items: List of items to display
        max_items: Maximum number of items to show
        show_count: Whether to show total count if truncated
        
    Returns:
        Formatted list string
    """
    if not items:
        return "None"
    
    if len(items) <= max_items:
        return ", ".join(items)
    else:
        displayed = ", ".join(items[:max_items])
        remaining = len(items) - max_items
        
        if show_count:
            return f"{displayed} (+{remaining} more)"
        else:
            return f"{displayed}..."


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause(message: str = "Press Enter to continue..."):
    """Pause execution and wait for user input"""
    input(f"\n{message}")


def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def export_to_csv(data: List[Dict[str, Any]], filename: str, 
                  fieldnames: Optional[List[str]] = None) -> bool:
    """
    Export data to CSV file
    
    Args:
        data: List of dictionaries to export
        filename: Output filename
        fieldnames: Optional list of fieldnames (uses first dict keys if None)
        
    Returns:
        True if successful
    """
    if not data:
        return False
    
    try:
        if fieldnames is None:
            fieldnames = list(data[0].keys())
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        return True
    except Exception as e:
        print(f"❌ Error exporting to CSV: {e}")
        return False


def export_to_json(data: Any, filename: str, indent: int = 2) -> bool:
    """
    Export data to JSON file
    
    Args:
        data: Data to export (must be JSON serializable)
        filename: Output filename
        indent: JSON indentation
        
    Returns:
        True if successful
    """
    try:
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=indent, default=str)
        
        return True
    except Exception as e:
        print(f"❌ Error exporting to JSON: {e}")
        return False


def import_from_json(filename: str) -> Optional[Any]:
    """
    Import data from JSON file
    
    Args:
        filename: Input filename
        
    Returns:
        Imported data or None if failed
    """
    try:
        with open(filename, 'r', encoding='utf-8') as jsonfile:
            return json.load(jsonfile)
    except Exception as e:
        print(f"❌ Error importing from JSON: {e}")
        return None


def create_backup_filename(base_name: str, extension: str = ".bak") -> str:
    """
    Create a backup filename with timestamp
    
    Args:
        base_name: Base filename
        extension: Backup extension
        
    Returns:
        Backup filename with timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name_without_ext = os.path.splitext(base_name)[0]
    return f"{name_without_ext}_{timestamp}{extension}"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division by zero
        
    Returns:
        Division result or default
    """
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ValueError):
        return default


def generate_color_indicator(value: float, thresholds: Dict[str, float]) -> str:
    """
    Generate color indicator emoji based on value and thresholds
    
    Args:
        value: Value to evaluate
        thresholds: Dictionary with 'excellent', 'good', 'fair', 'poor' thresholds
        
    Returns:
        Color indicator emoji
    """
    if value >= thresholds.get('excellent', 90):
        return "🟢"  # Green
    elif value >= thresholds.get('good', 70):
        return "🟡"  # Yellow
    elif value >= thresholds.get('fair', 50):
        return "🟠"  # Orange
    else:
        return "🔴"  # Red


def calculate_percentage(part: float, total: float) -> float:
    """
    Calculate percentage safely
    
    Args:
        part: Part value
        total: Total value
        
    Returns:
        Percentage (0-100)
    """
    return safe_divide(part * 100, total, 0.0)


def format_streak_display(current: int, longest: int) -> str:
    """
    Format streak display with appropriate emoji
    
    Args:
        current: Current streak
        longest: Longest streak
        
    Returns:
        Formatted streak string
    """
    if current == 0:
        return f"⭕ {current} (best: {longest})"
    elif current >= 30:
        return f"🔥 {current} (best: {longest})"
    elif current >= 7:
        return f"✨ {current} (best: {longest})"
    else:
        return f"✅ {current} (best: {longest})"


def get_motivation_message(category: str, achievement_level: str = "good") -> str:
    """
    Get a motivational message based on category and achievement level
    
    Args:
        category: Category of achievement (habit, goal, etc.)
        achievement_level: Level of achievement (excellent, good, needs_work)
        
    Returns:
        Motivational message
    """
    messages = {
        "habit": {
            "excellent": [
                "🎉 You're absolutely crushing it! Keep this amazing momentum going!",
                "🔥 Your consistency is inspiring! You're building an incredible habit!",
                "⭐ This is what success looks like! You're a habit-building machine!"
            ],
            "good": [
                "✅ Great progress! You're building something meaningful here!",
                "💪 Nice work! Small consistent steps lead to big wins!",
                "🌟 You're on the right track! Keep pushing forward!"
            ],
            "needs_work": [
                "💡 Every expert was once a beginner. You've got this!",
                "🔄 Progress isn't always linear. Focus on the next small step!",
                "🌱 Growth takes time. Be patient with yourself!"
            ]
        },
        "goal": {
            "excellent": [
                "🏆 Outstanding progress! You're turning dreams into reality!",
                "🎯 Bullseye! Your focus and dedication are paying off!",
                "🚀 You're unstoppable! This goal is within your reach!"
            ],
            "good": [
                "📈 Solid progress! Every step forward counts!",
                "🎪 You're making it happen! Stay focused on your vision!",
                "💫 Keep going! Success is built one day at a time!"
            ],
            "needs_work": [
                "🧭 Every journey has challenging parts. Recalibrate and continue!",
                "💭 Remember why this goal matters to you. You can do this!",
                "🛠️ Time to adjust the approach. You're learning and growing!"
            ]
        }
    }
    
    category_messages = messages.get(category, messages["goal"])
    level_messages = category_messages.get(achievement_level, category_messages["good"])
    
    import random
    return random.choice(level_messages)