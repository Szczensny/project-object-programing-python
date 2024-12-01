from habits.habit import Habit
from habits.analyis_functions import get_all_habits_tracked, get_all_habits_tracked_frequency, get_longest_strike, max_min_date_for_week, get_longest_strike_for_all_habits
from habits.analyis_functions import get_longest_strike, max_min_date_for_week, get_longest_strike_for_all_habits, get_last_strike
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
    ts2 = datetime.datetime(2024,11,2)
    ts3 = datetime.datetime(2024,11,3)
    ts4 = datetime.datetime(2024,11,4)
    h1_event1 = HabitEventDB(uuid='uuid1', created_at=ts1, event_year=ts1.year, week_nb=ts1.strftime("%V"), habit_uuid=h1.uuid)
    h1_event2 = HabitEventDB(uuid='uuid1', created_at=ts2, event_year=ts2.year, week_nb=ts2.strftime("%V"), habit_uuid=h1.uuid)
    h1_event3 = HabitEventDB(uuid='uuid1', created_at=ts3, event_year=ts3.year, week_nb=ts3.strftime("%V"), habit_uuid=h1.uuid)
    h1_event4 = HabitEventDB(uuid='uuid1', created_at=ts4, event_year=ts4.year, week_nb=ts4.strftime("%V"), habit_uuid=h1.uuid)
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

#################################### weekly #########################################################################################


def test_get_longest_strike_weekly_all_chekced():
    h1 = Habit('test_uuid1', 'test_name1', 'weekly', created_at=datetime.datetime.now())
    ts1 = datetime.datetime(2024,11,1)
    ts2 = datetime.datetime(2024,11,7)
    ts3 = datetime.datetime(2024,11,13)
    ts4 = datetime.datetime(2024,11,21)
    h1_event1 = HabitEventDB(uuid='uuid1', created_at=ts1, event_year=ts1.year, week_nb=ts1.strftime("%V"), habit_uuid=h1.uuid)
    h1_event2 = HabitEventDB(uuid='uuid1', created_at=ts2, event_year=ts2.year, week_nb=ts2.strftime("%V"), habit_uuid=h1.uuid)
    h1_event3 = HabitEventDB(uuid='uuid1', created_at=ts3, event_year=ts3.year, week_nb=ts3.strftime("%V"), habit_uuid=h1.uuid)
    h1_event4 = HabitEventDB(uuid='uuid1', created_at=ts4, event_year=ts4.year, week_nb=ts4.strftime("%V"), habit_uuid=h1.uuid)
    event_list = [h1_event1, h1_event2, h1_event4, h1_event3]
    expected = {"max_strike_times": 4 , "max_date": h1_event4.created_at.date(), "min_date": h1_event1.created_at.date()}
    data = get_longest_strike(h1, event_list)
    assert expected == data

def test_get_longest_strike_weekly_non_chekced():
    h1 = Habit('test_uuid1', 'test_name1', 'weekly', created_at=datetime.datetime.now())
    data = get_longest_strike(h1, [])
    assert data is None

def test_get_longst_strike_weekly_1_group():
    h1 = Habit('test_uuid1', 'test_name1', 'weekly', created_at=datetime.datetime.now())

    ts1 = datetime.datetime(2024,11,1)
    ts2 = datetime.datetime(2024,11,9)
    ts3 = datetime.datetime(2024,11,14) # stike 3
    ts4 = datetime.datetime(2024,11,25)
    ts5 = datetime.datetime(2024,12,9)
    ts6 = datetime.datetime(2024,12,17)
    ts7 = datetime.datetime(2024,12,12)
    ts8 = datetime.datetime(2024,12,30)
    ts9 = datetime.datetime(2024,12,31)
    ts10 = datetime.datetime(2025,1,20)

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
    expected = {"max_strike_times": 3 , "max_date": h1_event3.created_at.date(), "min_date": h1_event1.created_at.date()}
    data = get_longest_strike(h1, event_list)
    assert expected == data

def test_get_longst_strike_weekly_2_group():
    h1 = Habit('test_uuid1', 'test_name1', 'weekly', created_at=datetime.datetime.now())

    ts1 = datetime.datetime(2024,10,1)
    ts2 = datetime.datetime(2024,10,15)
    ts3 = datetime.datetime(2024,10,29) #start strike
    ts4 = datetime.datetime(2024,11,29)
    ts5 = datetime.datetime(2024,11,5)
    ts6 = datetime.datetime(2024,11,14) #strike end
    ts7 = datetime.datetime(2024,11,26)
    ts8 = datetime.datetime(2024,12,3)
    ts9 = datetime.datetime(2024,12,20)
    ts10 = datetime.datetime(2024,12,31)

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
    expected = {"max_strike_times": 3, "max_date": h1_event6.created_at.date(), "min_date": h1_event3.created_at.date()}
    data = get_longest_strike(h1, event_list)
    assert expected == data

def test_get_longst_strike_weekly_3_group():
    h1 = Habit('test_uuid1', 'test_name1', 'weekly', created_at=datetime.datetime.now())

    ts1 = datetime.datetime(2024,9,1)
    ts2 = datetime.datetime(2024,9,12)
    ts3 = datetime.datetime(2024,9,16)
    ts4 = datetime.datetime(2024,9,30) # strike start
    ts5 = datetime.datetime(2024,10,10)
    ts6 = datetime.datetime(2024,10,19)
    ts7 = datetime.datetime(2024,10,22) # strike end
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
    expected = {"max_strike_times": 4 , "max_date": h1_event7.created_at.date(), "min_date": h1_event4.created_at.date()}
    data = get_longest_strike(h1, event_list)
    assert expected == data

def test_get_longst_strike_weekly_4_group():
    h1 = Habit('test_uuid1', 'test_name1', 'weekly', created_at=datetime.datetime.now())

    ts1 = datetime.datetime(2024,10,3)
    ts2 = datetime.datetime(2024,10,17)
    ts3 = datetime.datetime(2024,11,7)
    ts4 = datetime.datetime(2024,11,14)
    ts5 = datetime.datetime(2024,11,7)
    ts6 = datetime.datetime(2024,11,27)
    ts7 = datetime.datetime(2024,12,4)
    ts8 = datetime.datetime(2024,12,18) # strike start
    ts9 = datetime.datetime(2024,12,25)
    ts10 = datetime.datetime(2024,12,31) #strike end

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

def test_get_longst_strike_weekly_3_and_4_group():
    h1 = Habit('test_uuid1', 'test_name1', 'weekly', created_at=datetime.datetime.now())

    ts1 = datetime.datetime(2024,10,1)
    ts2 = datetime.datetime(2024,10,10)
    ts3 = datetime.datetime(2024,10,24)
    ts4 = datetime.datetime(2024,10,31)
    ts5 = datetime.datetime(2024,11,15) # strike 1 start
    ts6 = datetime.datetime(2024,11,20)
    ts7 = datetime.datetime(2024,11,30) # strike 1 end
    ts8 = datetime.datetime(2024,12,15) # strike2 start
    ts9 = datetime.datetime(2024,12,16)
    ts10 = datetime.datetime(2024,12,28) # strike2 ends

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

def test_max_min_week_dates():
    test_date = datetime.date(2024,11,27) 
    expected = {"max": datetime.date(2024,12,1), "min": datetime.date(2024,11,25)}
    data = max_min_date_for_week(test_date)
    
    test_date2 = datetime.date(2024,11,4)
    expected2 = {"max": datetime.date(2024,11,10), "min": datetime.date(2024,11,4)}
    data2 = max_min_date_for_week(test_date2)
    
    test_date3 = datetime.date(2024,10,6)
    expected3 = {"max": datetime.date(2024,10,6), "min": datetime.date(2024,9,30)}
    data3 = max_min_date_for_week(test_date3)
    
    assert expected == data
    assert expected2 == data2
    assert expected3 == data3

def test_longest_strike_habbits():
    h1 = Habit('test_uuid1', 'test_name1', 'weekly', created_at=datetime.datetime.now())
    ts4 = datetime.datetime(2024,9,30) # strike start
    ts5 = datetime.datetime(2024,10,10)
    ts6 = datetime.datetime(2024,10,19)
    ts7 = datetime.datetime(2024,10,22) # strike end
    h1_event4 = HabitEventDB(uuid='uuid1', created_at=ts4, event_year=ts4.year, week_nb=ts4.strftime("%V"), habit_uuid=h1.uuid)
    h1_event5 = HabitEventDB(uuid='uuid1', created_at=ts5, event_year=ts5.year, week_nb=ts5.strftime("%V"), habit_uuid=h1.uuid)
    h1_event6 = HabitEventDB(uuid='uuid1', created_at=ts6, event_year=ts6.year, week_nb=ts6.strftime("%V"), habit_uuid=h1.uuid)
    h1_event7 = HabitEventDB(uuid='uuid1', created_at=ts7, event_year=ts7.year, week_nb=ts7.strftime("%V"), habit_uuid=h1.uuid)
    habit1_tuple = (h1, [h1_event4, h1_event5, h1_event6, h1_event7])

    h2 = Habit('test_uuid2', 'test_name2', 'daily', created_at=datetime.datetime.now())
    ts1 = datetime.datetime(2024,11,1)
    ts2 = datetime.datetime(2024,11,2)
    ts3 = datetime.datetime(2024,11,3)
    ts4 = datetime.datetime(2024,11,4)
    ts5 = datetime.datetime(2024,11,5)
    h2_event1 = HabitEventDB(uuid='uuid2', created_at=ts1, event_year=ts1.year, week_nb=ts1.strftime("%V"), habit_uuid=h1.uuid)
    h2_event2 = HabitEventDB(uuid='uuid2', created_at=ts2, event_year=ts2.year, week_nb=ts2.strftime("%V"), habit_uuid=h1.uuid)
    h2_event3 = HabitEventDB(uuid='uuid2', created_at=ts3, event_year=ts3.year, week_nb=ts3.strftime("%V"), habit_uuid=h1.uuid)
    h2_event4 = HabitEventDB(uuid='uuid2', created_at=ts4, event_year=ts4.year, week_nb=ts4.strftime("%V"), habit_uuid=h1.uuid)
    h2_event5 = HabitEventDB(uuid='uuid2', created_at=ts5, event_year=ts5.year, week_nb=ts5.strftime("%V"), habit_uuid=h1.uuid)
    habit2_tuple = (h2, [h2_event1, h2_event3, h2_event2, h2_event4, h2_event5])
    
    h3 = Habit('test_uuid3', 'test_name3', 'daily', created_at=datetime.datetime.now())
    ts1 = datetime.datetime(2023,11,1)
    ts2 = datetime.datetime(2023,11,2)
    ts3 = datetime.datetime(2023,11,3)
    ts4 = datetime.datetime(2023,11,4)
    ts5 = datetime.datetime(2023,11,5)
    h3_event1 = HabitEventDB(uuid='uuid3', created_at=ts1, event_year=ts1.year, week_nb=ts1.strftime("%V"), habit_uuid=h1.uuid)
    h3_event2 = HabitEventDB(uuid='uuid3', created_at=ts2, event_year=ts2.year, week_nb=ts2.strftime("%V"), habit_uuid=h1.uuid)
    h3_event3 = HabitEventDB(uuid='uuid3', created_at=ts3, event_year=ts3.year, week_nb=ts3.strftime("%V"), habit_uuid=h1.uuid)
    h3_event4 = HabitEventDB(uuid='uuid3', created_at=ts4, event_year=ts4.year, week_nb=ts4.strftime("%V"), habit_uuid=h1.uuid)
    h3_event5 = HabitEventDB(uuid='uuid3', created_at=ts5, event_year=ts5.year, week_nb=ts5.strftime("%V"), habit_uuid=h1.uuid)
    habit3_tuple = (h3, [h3_event1, h3_event3, h3_event2, h3_event4, h3_event5])

    data = get_longest_strike_for_all_habits([habit1_tuple, habit2_tuple, habit3_tuple])
    expected = {"habit_name": 'test_name2', "strike": 5 , "max": h2_event5.created_at.date(), "min": h2_event1.created_at.date()}
    assert data == expected

def test_get_last_strike():
    h3 = Habit('test_uuid3', 'test_name3', 'daily', created_at=datetime.datetime.now())
    ts1 = datetime.datetime(2023,9,1)
    ts2 = datetime.datetime(2023,9,2)
    ts3 = datetime.datetime(2023,11,3)
    ts4 = datetime.datetime(2024,12,4)
    ts5 = datetime.datetime(2024,12,5)
    h3_event1 = HabitEventDB(uuid='uuid3', created_at=ts1, event_year=ts1.year, week_nb=ts1.strftime("%V"), habit_uuid=h3.uuid)
    h3_event2 = HabitEventDB(uuid='uuid3', created_at=ts2, event_year=ts2.year, week_nb=ts2.strftime("%V"), habit_uuid=h3.uuid)
    h3_event3 = HabitEventDB(uuid='uuid3', created_at=ts3, event_year=ts3.year, week_nb=ts3.strftime("%V"), habit_uuid=h3.uuid)
    h3_event4 = HabitEventDB(uuid='uuid3', created_at=ts4, event_year=ts4.year, week_nb=ts4.strftime("%V"), habit_uuid=h3.uuid)
    h3_event5 = HabitEventDB(uuid='uuid3', created_at=ts5, event_year=ts5.year, week_nb=ts5.strftime("%V"), habit_uuid=h3.uuid)
    habit3_list = [h3_event1, h3_event3, h3_event2, h3_event4, h3_event5]

    h1 = Habit('test_uuid1', 'test_name1', 'weekly', created_at=datetime.datetime.now())
    ts4 = datetime.datetime(2024,9,30)
    ts5 = datetime.datetime(2024,10,1)
    ts6 = datetime.datetime(2024,10,19)
    ts7 = datetime.datetime(2024,10,22)
    h1_event4 = HabitEventDB(uuid='uuid1', created_at=ts4, event_year=ts4.year, week_nb=ts4.strftime("%V"), habit_uuid=h1.uuid)
    h1_event5 = HabitEventDB(uuid='uuid1', created_at=ts5, event_year=ts5.year, week_nb=ts5.strftime("%V"), habit_uuid=h1.uuid)
    h1_event6 = HabitEventDB(uuid='uuid1', created_at=ts6, event_year=ts6.year, week_nb=ts6.strftime("%V"), habit_uuid=h1.uuid)
    h1_event7 = HabitEventDB(uuid='uuid1', created_at=ts7, event_year=ts7.year, week_nb=ts7.strftime("%V"), habit_uuid=h1.uuid)
    habit1_list = [h1_event4, h1_event5, h1_event6, h1_event7]

    h2 = Habit('test_uuid2', 'test_name2', 'weekly', created_at=datetime.datetime.now())
    habit2_list = []

    expected_habit2 = None
    expected_habit1 = {"strike": 2, "max": h1_event7.created_at.date() , "min": h1_event6.created_at.date()}
    expected_habit3 = {"strike": 2 , "max": h3_event5.created_at.date() , "min": h3_event4.created_at.date()}

    data_1 = get_last_strike(h1, habit1_list)
    import logging
    logging.warning(expected_habit1)
    data_2 = get_last_strike(h2, habit2_list)
    logging.warning(expected_habit2)
    data_3 = get_last_strike(h3, habit3_list)
    logging.warning(expected_habit3)

    assert data_1 == expected_habit1
    assert data_2 == expected_habit2
    assert data_3 == expected_habit3
