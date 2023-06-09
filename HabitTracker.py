# create database if necessary
import os
import database_setup

if not "habit_data.db" in os.listdir():
    database_setup.main("habit_data.db")
'''if not "habit_data.db" in os.listdir():
    with open("database_setup.py") as f:
        exec(f.read())'''

# Interface
import tracker as tf

page_help={"home":"""Commands:
            'stats' to open the statistics page
            'manage' to create or delete habits
            'check [number of habit]' to check of habit for today
            'to complete' to check all habits that haven't been completed today
            'exit' to end your session
            'help' to reprint instructions\n""",
          "stats":"""Commands:
            'home' to go back to the home page
            'lcs' to get the longest currently running streak
            'las' to get the longest streak of all time
            'hardest' to get hardest to maintain habit
            'ov [number of habit]' to get an overview of all stats of a particular streak
            'exit' to end your session
            'help' to reprint instructions\n""",
          "manage":"""Commands:
            'home' to go back to the home page
            'create [habit]' to create a new habit
            'delete [habit]' to delete a habit
            'view [all / daily / weekly]' to view all habits of specified period
            'exit' to end your session
            'help' to reprint instructions\n"""}

exit_message="Session completed. See you next time."

def input_loop(one_word_commands, two_word_commands, special_commands=[]):
    'runs in a loop until input is a recognized command'
    while True:
        command = input("What would you like to do? ")
        if command.split(" ")[0] in special_commands:
            command=[command.split(" ")[0], " ".join(command.split(" ")[1:])]
            break
        if command in one_word_commands:  
            break
        command = command.split(" ")
        if len(command) == 2:
            if command[0] in two_word_commands:
                break
        else:
            print("Command not recognized. Check spelling")
    return command

def validity_test(number, habit_list):
    'tests if input number for a command is a valid input'
    try:
        habit_number = int(number)
        invalid = False
        if habit_number > len(habit_list):
            print("Invalid input. Number out of range")
            invalid = True
    except:
        print("Invalid input. Not a number")
        invalid = True
        habit_number = None
    return habit_number, invalid

def main():
    'main loop that starts the program and opens the home page'
    # connect to database and load existing habits
    habits = tf.load_habits()

    print("Welcome to the Habit Tracking App")

    # check if streaks are lost and what streaks need to be completed
    if not tf.checked_today(habits):
        print("Checking your streaks...")
        for habit in habits:
            habit.check_streak()

    home_page(habits, list_commands = True)

    # Commit changes and end session
    tf.commit_changes(habits)
    tf.sql_connect.close()
    
def home_page(habits, list_commands = False):
    print("\n-----Home-----")
    if list_commands:
        print(page_help["home"])
    
    print("Habits to complete:")
    i = 1
    completable_habits=[]
    for habit in habits:
        if not habit.completed_today:
            print(f"{i}.) {habit.name}")
            completable_habits.append(habit)
            i += 1
    
    #input loop
    command = input_loop(one_word_commands = ["stats", "manage", "exit", "help"],
                         two_word_commands = ["check", "to complete"])

    # Command execution
    if command == "help":
        home_page(habits, list_commands = True)
    elif command == "exit":
        print(exit_message)
    elif command == "stats":
        stats_page(habits, list_commands = True)
    elif command == "manage":
        manage_page(habits, list_commands = True)
    elif command == "to complete":
        home_page(habits)
    elif "check" == command[0]:
        habit_number, invalid = validity_test(number = command[1],
                                               habit_list = completable_habits)
        if not invalid:
            habit_to_check = completable_habits[habit_number - 1]  #subtract one because counting began at 1
            habit_to_check.complete()
            print(f"{habit_to_check.name} completed")
        home_page(habits)
        
        
def stats_page(habits, list_commands = False):
    print("\n-----Habit Statistics-----")
    if list_commands:
        print(page_help["stats"])
    
    # Print all habits
    i = 1
    for habit in habits:
        print(f"{i}.) {habit.name}")
        i += 1

    #input loop
    command = input_loop(one_word_commands = ["home", "help", "exit", "lcs", "las", "hardest"],
                         two_word_commands = ["ov"])
            
    # Command execution
    if command == "help":
        stats_page(habits, list_commands = True)
    elif command == "home":
        home_page(habits, list_commands = True)
    elif command == "exit":
        print(exit_message)
    elif command == "lcs":
        longest_daily, longest_weekly = tf.longest_current_streak(habits)
        print(f"Your longest daily streak is {longest_daily[0]} with a streak of {longest_daily[1]}")
        print(f"Your longest weekly streak is {longest_weekly[0]} with a streak of {longest_weekly[1]}")
        stats_page(habits)
    elif command == "las":
        longest, streak = tf.longest_all_time_streak(habits)
        print(f"Your longest streak of all time is {longest} with a streak of {streak}")
        stats_page(habits)
    elif command == "hardest":
        hardest_to_maintain, losses = tf.hardest_streak(habits)
        print(f"The streak you struggle the most with is {hardest_to_maintain}. You lost this streak {losses} times.")
        stats_page(habits)
    elif command[0] == "ov":
        habit_number, invalid = validity_test(number = command[1],
                                               habit_list = habits)
        if not invalid:
            habit_to_check = habits[habit_number - 1]  #subtract one because counting began at 1
            print(habit_to_check.info())

        stats_page(habits)
            
def manage_page(habits, list_commands = False):
    print("\n-----Manage Habits-----")
    if list_commands:
        print(page_help["manage"])
    
    # Print all habits
    i = 1
    for habit in habits:
        print(f"{i}.) {habit.name}")
        i += 1
            
    # input loop
    command = input_loop(one_word_commands = ["home", "help", "exit"],
                         two_word_commands = ["view"],
                         special_commands=["create", "delete"])
        
    # command execution
    if command == "help":
        manage_page(habits, list_commands = True)
    elif command == "home":
        home_page(habits, list_commands = True)
    elif command == "exit":
        print(exit_message)
    elif command[0] == "create":
        new_habit = tf.create_habit(name = command[1])
        habits.append(new_habit)
        print("Your habit has been created")
        manage_page(habits)
    elif command[0] == "delete":
        tf.delete_habit(command[1], habits)
        print("Your habit has been deleted")
        manage_page(habits)
    elif command[0] == "view":
        habit_list=tf.view_all(command[1], habits)
        #print(habit_list)
        for habit in habit_list:
            print(habit.info(),"\n")
        manage_page(habits)

main()