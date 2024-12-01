from habits.habit import Habit
from habits.db_models import HabitEventDB
from typing import List, Dict, Set, Tuple
import logging
import datetime

def max_min_date_for_week(date:datetime.date) -> Dict:
    monday = date - datetime.timedelta(days=date.weekday())
    sunday = date + datetime.timedelta(days=(6 - date.weekday()))
    return {"max": sunday, "min": monday}

def get_all_habits_tracked(habit_list:List[Habit]) -> List[Dict]:
    result = [{habit.name: habit.uuid} for habit in habit_list]
    return result 

def get_all_habits_tracked_frequency(habit_list:List[Habit], frequency:str) -> List[Dict]:
    result = [{habit.name: habit.uuid} for habit in habit_list if habit.frequency == frequency]
    return result 

def get_longest_strike(habit:Habit, habit_events:List[HabitEventDB]) -> Dict:
    if habit.frequency == 'daily':
        max_diff_days = 1
    elif habit.frequency == 'weekly':
        max_diff_days = 6
    if len(habit_events) == 0:
        return None
    date_list = [habit_event.created_at.date() for habit_event in habit_events]
    sorted_dates = sorted(date_list)
    groups = []
    temp_group = []
    for i, date in enumerate(sorted_dates):
        if i > 0 and habit.frequency == 'daily':
            date_to_check = sorted_dates[i-1]
        elif i > 0 and habit.frequency == 'weekly':
            date_to_check = max_min_date_for_week(sorted_dates[i-1])['max']
            if date.isocalendar()[:2] == date_to_check.isocalendar()[:2]:
                continue

        if i == 0:
            temp_group.append(date)
            continue
        elif i == len(sorted_dates) - 1 and (date - date_to_check).days <= max_diff_days:
            temp_group.append(date)
            groups.append(temp_group)
            continue
        elif i == len(sorted_dates) - 1:
            groups.append(temp_group)
            groups.append([date])
        
        if (date - date_to_check).days <= max_diff_days:
            temp_group.append(date)
        else:
            groups.append(temp_group)
            temp_group = []
            temp_group.append(date)
    strike_conter = [len(group) for group in groups]
    max_strike = max(strike_conter)
    max_strike_pos = 0
    for i, value in enumerate(strike_conter):
        if value == max_strike and i > max_strike_pos:
            max_strike_pos = i
    min_date, max_date = groups[max_strike_pos][0], groups[max_strike_pos][-1]
    return {"max_strike_times": max_strike , "max_date": max_date, "min_date": min_date}


def get_longest_strike_for_all_habits(habits:List[Tuple[Habit, List[HabitEventDB]]]) -> dict:
    strike_list = []
    for habit in habits:
        longest_strike = get_longest_strike(habit[0], habit[1])
        strike_list.append({"habit_name": habit[0].name,
                             "strike": longest_strike['max_strike_times'],
                             "max": longest_strike['max_date'],
                             "min": longest_strike["min_date"]})
    biggest_strike = max(strike_list, key=lambda row: (row['strike'], row['max']) )
    return biggest_strike
