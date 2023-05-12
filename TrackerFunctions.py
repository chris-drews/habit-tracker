#functions of the app
from datetime import datetime, timedelta, date
import sqlite3

sql_connect = sqlite3.connect("habit-data.db")
cursor = sql_connect.cursor()

# functions outside the habit class
def get_timestamp():
    '''returns a current timestamp'''
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_time

def str_to_date(date):
    '''converts string dates from table to datetime format'''
    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return date

def load_habits():
    '''converts all habits from the habit table 
    to class instances of the habit class 
    and returns them as a list'''
    habits = []
    query = 'SELECT * FROM habits;'
    result = cursor.execute(query).fetchall()
    for habit in result:
        habits.append(Habit(name = habit[1], frequency = habit[2],
                           streak = habit[3], creation = habit[4],
                           last_completed = habit[5], last_check = habit[6]))
    return habits

def commit_changes(habits):
    '''Updates the habit table by first
    clearing it and then inserting each habit'''
    query = 'DELETE FROM habits;'
    cursor.execute(query)
    for habit in habits:
        query = ('INSERT INTO habits ' 
                '(name, frequency, streak, creation, last_completed, last_check) '
                f'VALUES ("{habit.name}", "{habit.frequency}", {habit.streak}, '
                f'"{habit.creation}", "{habit.last_completed}", "{habit.last_check}");')
        cursor.execute(query)
    sql_connect.commit()
    
def checked_today(habits):
    '''checks if app has already been opened today'''
    stamp = str_to_date(habits[0].last_check)
    if stamp.date()==date.today():
        return True
    else:
        return False
    
def get_habit(name, habits):
    '''returns the habit class instance with the given name'''
    for habit in habits:
        if habit.name == name:
            return habit
    
def longest_current_streak(habits):
    '''returns the current longest running habit and streak for weekly and daily habits'''
    max_streak_daily = max(habit.streak for habit in habits if habit.frequency=="daily")
    max_streak_weekly = max(habit.streak for habit in habits if habit.frequency=="weekly")
    result=[]
    for habit in habits:
        if habit.streak==max_streak_daily:
            result+=[f"{habit.name} with a streak of {max_streak_daily}"]
    for habit in habits:
        if habit.streak==max_streak_weekly:
            result+=[f"{habit.name} with a streak of {max_streak_weekly}"]
    return result
        
def longest_all_time_streak(habits):
    '''returns the longest running streak of all time for weekly and daily habits'''
    query = ("SELECT name,Max(streak) FROM "
             "(SELECT name,streak FROM habits "
             "UNION ALL " #checking both the current streaks and the database of old ones
             "SELECT name,streak FROM past_streaks);")
    result = cursor.execute(query).fetchall()[0]
    return [0,0] #temporary
    
def hardest_streak(habits):
    '''determines the hardest streak to maintain, by checking which streak has been lost the most often'''
    query = f"SELECT name FROM past_streaks;"
    result = cursor.execute(query).fetchall()
    cleaned_up_result = []
    #removing those lost streaks where the habit has since been deleted
    for name in result:
        name = name[0]
        if get_habit(name, habits) != None:
            cleaned_up_result.append(name)
    result = cleaned_up_result
    # count up the losses for each habit
    loss_count = {}
    for name in result:
        if name in loss_count:
            loss_count[name] += 1
        else:
            loss_count[name] = 1
    #sort dictionary by highest values
    loss_count = dict(sorted(loss_count.items(), reverse=True, key=lambda item: item[1]))

    hardest_habit = list(loss_count.keys())[0]
    losses = list(loss_count.items())[0]
    return hardest_habit, losses
    
def create_habit(name):
    '''creates and returns a new habit'''
    #input loop
    while True:
        frequency = "Should this be a daily (d) or a weekly (w) streak?"
        if frequency in ["d", "w"]:
            break
        else:
            print("Please use 'd' or 'w' as your input")
    new_habit = Habit(name, frequency = frequency)
    return new_habit

def delete_habit(name, habits):
    '''deletes an existing habit (optionally also from the statistics history)'''
    habit = get_habit(name, habits)
    if habit != None:
        # input loop
        while True:
            stats_delete = input("Would you like to remove this habit from past statistics? (y/n)")
            if stats_delete in ["y", "n"]:
                break
            else:
                print("invalid input")
        stats_delete = True if stats_delete == "y" else False
        habit.delete(stats_delete)
    else:
        print("Can't delete a habit that doesn't exist")
        
def view_all(frequency, habits):
    '''gives an overview of all the habits whose frequency matches the one specified'''
    if frequency in ["all", "daily", "weekly"]:
        for habit in habits:
            if frequency == "all" or habit.frequency == frequency:
                habit.info()
                print("\n")
    else:
        print("Invalid frequency input. Valid: 'all', 'daily', 'weekly'")

    
# habit class
class Habit:
    def __init__(self, name, frequency = "daily", streak = 0, creation=get_timestamp(),
                 last_completed="None", last_check="None", completed_today=False):
        self.name = name
        self.frequency = frequency
        self.streak = streak
        self.creation = creation
        self.last_completed = last_completed
        self.last_check = last_check
        self.completed_today = completed_today
        
    def complete(self):
        self.streak+=1
        self.last_completed=get_timestamp()
        self.completed_today=True
    
    def check_streak(self):
        today = date.today()
        yesterday = today - timedelta(days = 1)
        if self.last_completed == "None":
            self.completed_today = False
        else:
            last_completed = str_to_date(self.last_completed).date()
            if last_completed == today:
                self.completed_today = True
            else:
                self.completed_today = False
                
                if not ((self.frequency == "daily" and last_completed == yesterday) or 
                        (self.frequency == "weekly" and (today - last_completed).days <= 7)):
                    self.lose_streak()

        self.last_check = str(get_timestamp())
        
    def lose_streak(self):
        if self.streak != 0:
            self.streak = 0
            self.last_completed = None

            query = ('INSERT INTO past_streaks (name, end, streak)'
                     f'VALUES ("{self.name}","{date.today()}",{self.streak});')
            cursor.execute(query)

            timing = "yesterday" if self.frequency=="daily" else "last week"
            print(f"You didn't {self.name} {timing} and lost your streak :/")
        
    def info(self):
        print(f"""Habit: {self.name}
        Streak: {self.streak}
        Frequency: {self.frequency}
        Last Completed on: {self.last_completed}
        Created on: {self.creation}""")
        
    def delete(self, habits, stats_delete):
        query = f'DELETE FROM habits WHERE name="{self.name}"'
        cursor.execute(query)
        # delete stats if required
        query = f'DELETE FROM past_streaks WHERE name="{self.name}"'
        cursor.execute(query)
        habits.remove(self)
        del self
        return habits