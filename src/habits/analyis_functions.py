from habits.habit import Habit
from habits.db_models import HabitEventDB
from typing import List, Dict
import logging

# return the longest run streak of all defined habits,
# and return the longest run streak for a given habit.

def get_all_habits_tracked(habit_list:List[Habit]) -> List[Dict]:
    result = [{habit.name: habit.uuid} for habit in habit_list]
    return result 

def get_all_habits_tracked_frequency(habit_list:List[Habit], frequency:str) -> List[Dict]:
    result = [{habit.name: habit.uuid} for habit in habit_list if habit.frequency == frequency]
    return result 

def get_longest_strike(habit:Habit, habit_events:List[HabitEventDB]) -> Dict:
    if len(habit_events) == 0:
        return None
    date_list = [habit_event.created_at.date() for habit_event in habit_events]
    sorted_dates = sorted(date_list)
    groups = []
    temp_group = []
    for i, date in enumerate(sorted_dates):
        if i == 0:
            temp_group.append(date)
            continue
        elif i == len(sorted_dates) - 1 and (date - sorted_dates[i-1]).days == 1:
            temp_group.append(date)
            groups.append(temp_group)
            continue
        elif i == len(sorted_dates) - 1:
            groups.append(temp_group)
            groups.append([date])
        
        if (date - sorted_dates[i-1]).days == 1:
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