from habits.habit import Habit
from habits.db_models import HabitEventDB
from typing import List, Dict, Tuple
import datetime

def max_min_date_for_week(date:datetime.date) -> Dict:
    """Function generates dates of monday and sunday of the same week as input date

    Args:
        date (datetime.date): date of intrest

    Returns:
        Dict:{"max": <sunday date>, "min": <monday date>}
    """
    monday = date - datetime.timedelta(days=date.weekday())
    sunday = date + datetime.timedelta(days=(6 - date.weekday()))
    return {"max": sunday, "min": monday}

def get_all_habits_tracked(habit_list:List[Habit]) -> List[Dict]:
    """generates list of dictionaris containing habits uuids with objects

    Args:
        habit_list (List[Habit]): List of habit objects

    Returns:
        List[Dict]: [{"uuuid": <UUID>, "obj": <habit object>}]
    """
    result = [{habit.name: habit.uuid, "obj": habit} for habit in habit_list]
    return result 

def get_all_habits_counter(habit_list:List[Habit]) -> Dict:
    """ Counts amount of daily and weekly habits and retruns values as dictionary

    Args:
        habit_list (List[Habit]): List of Habits objects in intrest

    Returns:
        Dict:{"daily": <daily habits count>, "weekly": <weekly habits count>}
    """
    counter_daily = 0
    counter_weekly = 0
    for habit in habit_list:
        if habit.frequency == 'daily':
            counter_daily +=1
        elif habit.frequency == 'weekly':
            counter_weekly +=1
    
    return {"daily": counter_daily, "weekly":counter_weekly}

def get_all_habits_tracked_frequency(habit_list:List[Habit], frequency:str) -> List[Habit]:
    """Returns the list of habits with choosen frequency

    Args:
        habit_list (List[Habit]): List of habits in intrest
        frequency (str): name of the frequency 

    Returns:
        List[Habit]: list of habits object after filtration. If no match fund return empty list
    """
    result = [habit for habit in habit_list if habit.frequency == frequency]
    return result 

def get_all_strikes(habit:Habit, habit_events:List[HabitEventDB]) -> List[List[HabitEventDB]] | None:
    """Counts the amount of strikes (count of situation when events happend in succesive order)


    Args:
        habit (Habit): Habit object
        habit_events (List[HabitEventDB]): list of habits events to coresponding habit

    Returns:
        List[List[HabitEventDB]]: list containg groups of events that happend one after another. If no habit event is provided returns None
    """
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
    return groups

def get_longest_strike(habit:Habit, habit_events:List[HabitEventDB]) -> Dict | None:
    """Generates the count of the longest strike for given habbit and its habits events

    Args:
        habit (Habit): Habit object in intrest
        habit_events (List[HabitEventDB]): List of habits events that belong to habit

    Returns:
        Dict | None: {"max_strike_times": max_strike , "max_date": max_date, "min_date": min_date}
        if event list is empty returns None
    """
    all_strikes = get_all_strikes(habit, habit_events)
    if all_strikes is None or len(all_strikes)==0:
        return None
    strike_conter = [len(group) for group in all_strikes]
    max_strike = max(strike_conter)
    max_strike_pos = 0
    for i, value in enumerate(strike_conter):
        if value == max_strike and i > max_strike_pos:
            max_strike_pos = i
    min_date, max_date = all_strikes[max_strike_pos][0], all_strikes[max_strike_pos][-1]
    return {"max_strike_times": max_strike , "max_date": max_date, "min_date": min_date}


def get_longest_strike_for_all_habits(habits:List[Tuple[Habit, List[HabitEventDB]]]) -> dict | None:
    """Restruns a longest strike for all given habits

    Args:
        habits (List[Tuple[Habit, List[HabitEventDB]]]): List of touples where each contain Habit object and list of coresponding habit events.

    Returns:
        dict | None: Returns dictionary wit information on the biggest strike. 
                            {"habit_name": <value>,
                             "strike": <value>,
                             "max":<value>,
                             "min": <value>}
    """
    strike_list = []
    for habit in habits:
        longest_strike = get_longest_strike(habit[0], habit[1])
        if longest_strike is None:
            continue
        strike_list.append({"habit_name": habit[0].name,
                             "strike": longest_strike['max_strike_times'],
                             "max": longest_strike['max_date'],
                             "min": longest_strike["min_date"]})
    biggest_strike = max(strike_list, key=lambda row: (row['strike'], row['max']) )
    return biggest_strike

def get_last_strike(habit:Habit, habit_events:List[HabitEventDB]) -> Dict | None:
    """Returns the last strike of given habit

    Args:
        habit (Habit): Habit object in intrest
        habit_events (List[HabitEventDB]): List of coresponding habit events

    Returns:
        Dict | None: returns dictionary with data as example below. If list of habits is empty returns None
        {"strike": <value>, "max":<value> , "min": <value>}
    """
    all_strikes = get_all_strikes(habit, habit_events)
    if all_strikes is None or len(all_strikes)==0:
        return None
    result = {"strike": len(all_strikes[-1]), "max": all_strikes[-1][-1] , "min": all_strikes[-1][0]}
    return result
