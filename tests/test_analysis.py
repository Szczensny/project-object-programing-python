from habits.habit import Habit
from habits.analyis_functions import get_all_habits_tracked, get_all_habits_tracked_frequency, get_longest_strike
from habits.db_models import HabitEventDB
import datetime 

def test_get_all_habbits_tracked():
    h1 = Habit('test_uuid1', 'test_name1', 'daily', created_at=datetime.datetime.now())
    h2 = Habit('test_uuid2', 'test_name2', 'daily', created_at=datetime.datetime.now())
    h3 = Habit('test_uuid3', 'test_name3', 'weekly', created_at=datetime.datetime.now())
    h4 = Habit('test_uuid4', 'test_name4', 'weekly', created_at=datetime.datetime.now())
    h5 = Habit('test_uuid5', 'test_name5', 'daily', created_at=datetime.datetime.now())
    habit_list = [h1, h2, h3, h4, h5]
    expected = [
        {'test_name1': 'test_uuid1'},
        {'test_name2': 'test_uuid2'},
        {'test_name3': 'test_uuid3'},
        {'test_name4': 'test_uuid4'},
        {'test_name5': 'test_uuid5'},
    ]
    
    data = get_all_habits_tracked(habit_list)
    assert expected == data
    assert len(expected) == 5

def test_get_all_habbits_frequency():
    h1 = Habit('test_uuid1', 'test_name1', 'daily', created_at=datetime.datetime.now())
    h2 = Habit('test_uuid2', 'test_name2', 'daily', created_at=datetime.datetime.now())
    h3 = Habit('test_uuid3', 'test_name3', 'weekly', created_at=datetime.datetime.now())
    h4 = Habit('test_uuid4', 'test_name4', 'weekly', created_at=datetime.datetime.now())
    h5 = Habit('test_uuid5', 'test_name5', 'daily', created_at=datetime.datetime.now())
    habit_list = [h1, h2, h3, h4, h5]
    
    expected = [
        {'test_name1': 'test_uuid1'},
        {'test_name2': 'test_uuid2'},
        {'test_name5': 'test_uuid5'},
    ]

    expected2 = [
        {'test_name3': 'test_uuid3'},
        {'test_name4': 'test_uuid4'},
    ]
    
    data1 = get_all_habits_tracked_frequency(habit_list, 'daily')
    data2 = get_all_habits_tracked_frequency(habit_list, 'weekly')

    assert expected == data1
    assert len(data1) == 3
    assert expected2 == data2
    assert len(data2) == 2

def test_get_longest_strike_daily_all_chekced():
    h1 = Habit('test_uuid1', 'test_name1', 'daily', created_at=datetime.datetime.now())
    ts1 = datetime.datetime(2024,11,1)
    h1_event1 = HabitEventDB(uuid='uuid1', created_at=ts1, 
                             event_year=ts1.year, week_nb=ts1.strftime("%V"), habit_uuid=h1.uuid)
    ts2 = datetime.datetime(2024,11,2)
    h1_event2 = HabitEventDB(uuid='uuid1', created_at=ts2, 
                             event_year=ts2.year, week_nb=ts2.strftime("%V"), habit_uuid=h1.uuid)
    ts3 = datetime.datetime(2024,11,3)
    h1_event3 = HabitEventDB(uuid='uuid1', created_at=ts3, 
                             event_year=ts3.year, week_nb=ts3.strftime("%V"), habit_uuid=h1.uuid)
    ts4 = datetime.datetime(2024,11,4)
    h1_event4 = HabitEventDB(uuid='uuid1', created_at=ts4, 
                             event_year=ts4.year, week_nb=ts4.strftime("%V"), habit_uuid=h1.uuid)
    event_list = [h1_event1, h1_event2, h1_event4, h1_event3]
    expected = {"max_strike_times": 4 , "max_date": h1_event4.created_at.date(), "min_date": h1_event1.created_at.date()}
    data = get_longest_strike(h1, event_list)
    assert expected == data

def test_get_longest_strike_daily_non_chekced():
    h1 = Habit('test_uuid1', 'test_name1', 'daily', created_at=datetime.datetime.now())
    data = get_longest_strike(h1, [])
    assert data is None

def test_get_longst_strike_daily_1_group():
    h1 = Habit('test_uuid1', 'test_name1', 'daily', created_at=datetime.datetime.now())

    ts1 = datetime.datetime(2024,11,1)
    ts2 = datetime.datetime(2024,11,2)
    ts3 = datetime.datetime(2024,11,3)
    ts4 = datetime.datetime(2024,11,4)
    ts5 = datetime.datetime(2024,11,8)
    ts6 = datetime.datetime(2024,11,9)
    ts7 = datetime.datetime(2024,11,12)
    ts8 = datetime.datetime(2024,11,14)
    ts9 = datetime.datetime(2024,11,16)
    ts10 = datetime.datetime(2024,11,20)

    h1_event1 = HabitEventDB(uuid='uuid1', created_at=ts1, event_year=ts1.year, week_nb=ts1.strftime("%V"), habit_uuid=h1.uuid)
    h1_event2 = HabitEventDB(uuid='uuid1', created_at=ts2, event_year=ts2.year, week_nb=ts2.strftime("%V"), habit_uuid=h1.uuid)
    h1_event3 = HabitEventDB(uuid='uuid1', created_at=ts3, event_year=ts3.year, week_nb=ts3.strftime("%V"), habit_uuid=h1.uuid)
    h1_event4 = HabitEventDB(uuid='uuid1', created_at=ts4, event_year=ts4.year, week_nb=ts4.strftime("%V"), habit_uuid=h1.uuid)
    h1_event5 = HabitEventDB(uuid='uuid1', created_at=ts5, event_year=ts5.year, week_nb=ts5.strftime("%V"), habit_uuid=h1.uuid)
    h1_event6 = HabitEventDB(uuid='uuid1', created_at=ts6, event_year=ts6.year, week_nb=ts6.strftime("%V"), habit_uuid=h1.uuid)
    h1_event7 = HabitEventDB(uuid='uuid1', created_at=ts7, event_year=ts7.year, week_nb=ts7.strftime("%V"), habit_uuid=h1.uuid)
    h1_event8 = HabitEventDB(uuid='uuid1', created_at=ts8, event_year=ts8.year, week_nb=ts8.strftime("%V"), habit_uuid=h1.uuid)
    h1_event9 = HabitEventDB(uuid='uuid1', created_at=ts9, event_year=ts9.year, week_nb=ts9.strftime("%V"), habit_uuid=h1.uuid)
    h1_event10 = HabitEventDB(uuid='uuid1', created_at=ts10, event_year=ts10.year, week_nb=ts10.strftime("%V"), habit_uuid=h1.uuid)
    
    event_list = [h1_event10, h1_event9, h1_event8, h1_event7, h1_event6, h1_event5, h1_event4, h1_event3, h1_event2, h1_event1]
    expected = {"max_strike_times": 4 , "max_date": h1_event4.created_at.date(), "min_date": h1_event1.created_at.date()}
    data = get_longest_strike(h1, event_list)
    assert expected == data

def test_get_longst_strike_daily_2_group():
    h1 = Habit('test_uuid1', 'test_name1', 'daily', created_at=datetime.datetime.now())

    ts1 = datetime.datetime(2024,11,1)
    ts2 = datetime.datetime(2024,11,2)
    ts3 = datetime.datetime(2024,11,6)
    ts4 = datetime.datetime(2024,11,7)
    ts5 = datetime.datetime(2024,11,8)
    ts6 = datetime.datetime(2024,11,9)
    ts7 = datetime.datetime(2024,11,10)
    ts8 = datetime.datetime(2024,11,14)
    ts9 = datetime.datetime(2024,11,15)
    ts10 = datetime.datetime(2024,11,20)

    h1_event1 = HabitEventDB(uuid='uuid1', created_at=ts1, event_year=ts1.year, week_nb=ts1.strftime("%V"), habit_uuid=h1.uuid)
    h1_event2 = HabitEventDB(uuid='uuid1', created_at=ts2, event_year=ts2.year, week_nb=ts2.strftime("%V"), habit_uuid=h1.uuid)
    h1_event3 = HabitEventDB(uuid='uuid1', created_at=ts3, event_year=ts3.year, week_nb=ts3.strftime("%V"), habit_uuid=h1.uuid)
    h1_event4 = HabitEventDB(uuid='uuid1', created_at=ts4, event_year=ts4.year, week_nb=ts4.strftime("%V"), habit_uuid=h1.uuid)
    h1_event5 = HabitEventDB(uuid='uuid1', created_at=ts5, event_year=ts5.year, week_nb=ts5.strftime("%V"), habit_uuid=h1.uuid)
    h1_event6 = HabitEventDB(uuid='uuid1', created_at=ts6, event_year=ts6.year, week_nb=ts6.strftime("%V"), habit_uuid=h1.uuid)
    h1_event7 = HabitEventDB(uuid='uuid1', created_at=ts7, event_year=ts7.year, week_nb=ts7.strftime("%V"), habit_uuid=h1.uuid)
    h1_event8 = HabitEventDB(uuid='uuid1', created_at=ts8, event_year=ts8.year, week_nb=ts8.strftime("%V"), habit_uuid=h1.uuid)
    h1_event9 = HabitEventDB(uuid='uuid1', created_at=ts9, event_year=ts9.year, week_nb=ts9.strftime("%V"), habit_uuid=h1.uuid)
    h1_event10 = HabitEventDB(uuid='uuid1', created_at=ts10, event_year=ts10.year, week_nb=ts10.strftime("%V"), habit_uuid=h1.uuid)
    
    event_list = [h1_event10, h1_event9, h1_event8, h1_event7, h1_event6, h1_event5, h1_event4, h1_event3, h1_event2, h1_event1]
    expected = {"max_strike_times": 5 , "max_date": h1_event7.created_at.date(), "min_date": h1_event3.created_at.date()}
    data = get_longest_strike(h1, event_list)
    assert expected == data

def test_get_longst_strike_daily_3_group():
    h1 = Habit('test_uuid1', 'test_name1', 'daily', created_at=datetime.datetime.now())

    ts1 = datetime.datetime(2024,11,1)
    ts2 = datetime.datetime(2024,11,2)
    ts3 = datetime.datetime(2024,11,4)
    ts4 = datetime.datetime(2024,11,5)
    ts5 = datetime.datetime(2024,11,10)
    ts6 = datetime.datetime(2024,11,11)
    ts7 = datetime.datetime(2024,11,12)
    ts8 = datetime.datetime(2024,11,14)
    ts9 = datetime.datetime(2024,11,15)
    ts10 = datetime.datetime(2024,11,20)

    h1_event1 = HabitEventDB(uuid='uuid1', created_at=ts1, event_year=ts1.year, week_nb=ts1.strftime("%V"), habit_uuid=h1.uuid)
    h1_event2 = HabitEventDB(uuid='uuid1', created_at=ts2, event_year=ts2.year, week_nb=ts2.strftime("%V"), habit_uuid=h1.uuid)
    h1_event3 = HabitEventDB(uuid='uuid1', created_at=ts3, event_year=ts3.year, week_nb=ts3.strftime("%V"), habit_uuid=h1.uuid)
    h1_event4 = HabitEventDB(uuid='uuid1', created_at=ts4, event_year=ts4.year, week_nb=ts4.strftime("%V"), habit_uuid=h1.uuid)
    h1_event5 = HabitEventDB(uuid='uuid1', created_at=ts5, event_year=ts5.year, week_nb=ts5.strftime("%V"), habit_uuid=h1.uuid)
    h1_event6 = HabitEventDB(uuid='uuid1', created_at=ts6, event_year=ts6.year, week_nb=ts6.strftime("%V"), habit_uuid=h1.uuid)
    h1_event7 = HabitEventDB(uuid='uuid1', created_at=ts7, event_year=ts7.year, week_nb=ts7.strftime("%V"), habit_uuid=h1.uuid)
    h1_event8 = HabitEventDB(uuid='uuid1', created_at=ts8, event_year=ts8.year, week_nb=ts8.strftime("%V"), habit_uuid=h1.uuid)
    h1_event9 = HabitEventDB(uuid='uuid1', created_at=ts9, event_year=ts9.year, week_nb=ts9.strftime("%V"), habit_uuid=h1.uuid)
    h1_event10 = HabitEventDB(uuid='uuid1', created_at=ts10, event_year=ts10.year, week_nb=ts10.strftime("%V"), habit_uuid=h1.uuid)
    
    event_list = [h1_event10, h1_event9, h1_event8, h1_event7, h1_event6, h1_event5, h1_event4, h1_event3, h1_event2, h1_event1]
    expected = {"max_strike_times": 3 , "max_date": h1_event7.created_at.date(), "min_date": h1_event5.created_at.date()}
    data = get_longest_strike(h1, event_list)
    assert expected == data

def test_get_longst_strike_daily_4_group():
    h1 = Habit('test_uuid1', 'test_name1', 'daily', created_at=datetime.datetime.now())

    ts1 = datetime.datetime(2024,11,1)
    ts2 = datetime.datetime(2024,11,2)
    ts3 = datetime.datetime(2024,11,4)
    ts4 = datetime.datetime(2024,11,5)
    ts5 = datetime.datetime(2024,11,7)
    ts6 = datetime.datetime(2024,11,14)
    ts7 = datetime.datetime(2024,11,15)
    ts8 = datetime.datetime(2024,11,18)
    ts9 = datetime.datetime(2024,11,19)
    ts10 = datetime.datetime(2024,11,20)

    h1_event1 = HabitEventDB(uuid='uuid1', created_at=ts1, event_year=ts1.year, week_nb=ts1.strftime("%V"), habit_uuid=h1.uuid)
    h1_event2 = HabitEventDB(uuid='uuid1', created_at=ts2, event_year=ts2.year, week_nb=ts2.strftime("%V"), habit_uuid=h1.uuid)
    h1_event3 = HabitEventDB(uuid='uuid1', created_at=ts3, event_year=ts3.year, week_nb=ts3.strftime("%V"), habit_uuid=h1.uuid)
    h1_event4 = HabitEventDB(uuid='uuid1', created_at=ts4, event_year=ts4.year, week_nb=ts4.strftime("%V"), habit_uuid=h1.uuid)
    h1_event5 = HabitEventDB(uuid='uuid1', created_at=ts5, event_year=ts5.year, week_nb=ts5.strftime("%V"), habit_uuid=h1.uuid)
    h1_event6 = HabitEventDB(uuid='uuid1', created_at=ts6, event_year=ts6.year, week_nb=ts6.strftime("%V"), habit_uuid=h1.uuid)
    h1_event7 = HabitEventDB(uuid='uuid1', created_at=ts7, event_year=ts7.year, week_nb=ts7.strftime("%V"), habit_uuid=h1.uuid)
    h1_event8 = HabitEventDB(uuid='uuid1', created_at=ts8, event_year=ts8.year, week_nb=ts8.strftime("%V"), habit_uuid=h1.uuid)
    h1_event9 = HabitEventDB(uuid='uuid1', created_at=ts9, event_year=ts9.year, week_nb=ts9.strftime("%V"), habit_uuid=h1.uuid)
    h1_event10 = HabitEventDB(uuid='uuid1', created_at=ts10, event_year=ts10.year, week_nb=ts10.strftime("%V"), habit_uuid=h1.uuid)
    
    event_list = [h1_event10, h1_event9, h1_event8, h1_event7, h1_event6, h1_event5, h1_event4, h1_event3, h1_event2, h1_event1]
    expected = {"max_strike_times": 3 , "max_date": h1_event10.created_at.date(), "min_date": h1_event8.created_at.date()}
    data = get_longest_strike(h1, event_list)
    assert expected == data

def test_get_longst_strike_daily_3_and_4_group():
    h1 = Habit('test_uuid1', 'test_name1', 'daily', created_at=datetime.datetime.now())

    ts1 = datetime.datetime(2024,11,1)
    ts2 = datetime.datetime(2024,11,2)
    ts3 = datetime.datetime(2024,11,5)
    ts4 = datetime.datetime(2024,11,6)
    ts5 = datetime.datetime(2024,11,13)
    ts6 = datetime.datetime(2024,11,14)
    ts7 = datetime.datetime(2024,11,15)
    ts8 = datetime.datetime(2024,11,18)
    ts9 = datetime.datetime(2024,11,19)
    ts10 = datetime.datetime(2024,11,20)

    h1_event1 = HabitEventDB(uuid='uuid1', created_at=ts1, event_year=ts1.year, week_nb=ts1.strftime("%V"), habit_uuid=h1.uuid)
    h1_event2 = HabitEventDB(uuid='uuid1', created_at=ts2, event_year=ts2.year, week_nb=ts2.strftime("%V"), habit_uuid=h1.uuid)
    h1_event3 = HabitEventDB(uuid='uuid1', created_at=ts3, event_year=ts3.year, week_nb=ts3.strftime("%V"), habit_uuid=h1.uuid)
    h1_event4 = HabitEventDB(uuid='uuid1', created_at=ts4, event_year=ts4.year, week_nb=ts4.strftime("%V"), habit_uuid=h1.uuid)
    h1_event5 = HabitEventDB(uuid='uuid1', created_at=ts5, event_year=ts5.year, week_nb=ts5.strftime("%V"), habit_uuid=h1.uuid)
    h1_event6 = HabitEventDB(uuid='uuid1', created_at=ts6, event_year=ts6.year, week_nb=ts6.strftime("%V"), habit_uuid=h1.uuid)
    h1_event7 = HabitEventDB(uuid='uuid1', created_at=ts7, event_year=ts7.year, week_nb=ts7.strftime("%V"), habit_uuid=h1.uuid)
    h1_event8 = HabitEventDB(uuid='uuid1', created_at=ts8, event_year=ts8.year, week_nb=ts8.strftime("%V"), habit_uuid=h1.uuid)
    h1_event9 = HabitEventDB(uuid='uuid1', created_at=ts9, event_year=ts9.year, week_nb=ts9.strftime("%V"), habit_uuid=h1.uuid)
    h1_event10 = HabitEventDB(uuid='uuid1', created_at=ts10, event_year=ts10.year, week_nb=ts10.strftime("%V"), habit_uuid=h1.uuid)
    
    event_list = [h1_event10, h1_event9, h1_event8, h1_event7, h1_event6, h1_event5, h1_event4, h1_event3, h1_event2, h1_event1]
    expected = {"max_strike_times": 3 , "max_date": h1_event10.created_at.date(), "min_date": h1_event8.created_at.date()}
    data = get_longest_strike(h1, event_list)
    assert expected == data
