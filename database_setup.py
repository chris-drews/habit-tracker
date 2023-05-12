#database set up
import sqlite3
import os
from datetime import timedelta, date

def create_table():
    sql_connect = sqlite3.connect("habit-data.db")
    cursor = sql_connect.cursor()
    main_table_query = ("CREATE TABLE habits("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "name TEXT, "
                    "frequency TEXT CHECK(frequency IN ('daily','weekly')), "
                    "streak INT, "
                    "creation DATETIME DEFAULT CURRENT_TIMESTAMP, "
                    "last_completed DATETIME, "
                    "last_check DATE);")
    cursor.execute(main_table_query)

    streak_table_query = ("CREATE TABLE past_streaks("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "name TEXT, "
                    "end DATE, "
                    "streak INT, "
                    "FOREIGN KEY (name) REFERENCES habits(name));")
    cursor.execute(streak_table_query)
    sql_connect.commit()
    sql_connect.close()

def insert_sample_data():
    today = date.today()
    yesterday = today - timedelta(1)
    null_value = None
    
    sql_connect = sqlite3.connect("habit-data.db")
    cursor = sql_connect.cursor()
    #insert example data for habit table
    insert_query = (
    "INSERT INTO habits "
        "(name, frequency, streak, creation, last_completed, last_check) "
    "VALUES "
        f"('Go for a walk', 'daily', 6, '2023-02-04 08:17:46', '{yesterday} 08:43:13', '{yesterday} 12:21:43'), "
        f"('Go to the gym', 'weekly', 3, '2023-02-04 08:16:46', '{yesterday} 09:43:13', '{yesterday} 12:21:43'), "
        f"('Take a shower', 'daily', 10, '2023-02-27 20:56:17', '{yesterday} 11:21:43', '{yesterday} 12:21:43'), "
        f"('Go swimming', 'weekly', 0, '2023-03-10 07:26:16', '{null_value}', '{yesterday} 12:21:43'), "
        f"('Study', 'daily', 0, '2023-02-04 08:43:13', '{null_value}', '{yesterday} 12:21:43');"
    )

    cursor.execute(insert_query)

    #insert example data for past streaks table
    insert_query = (
    "INSERT INTO past_streaks "
        "(name, end, streak) "
    "VALUES "
        "('Go for a walk', '2023-03-05', 4), "
        "('Go for a walk', '2023-03-13', 7), "
        "('Go for a walk', '2023-03-15', 1), "
        "('Go for a walk', '2023-03-19', 3), "
        "('Go for a walk', '2023-03-23', 2), "
        "('Go for a walk', '2023-03-29', 5), "
        "('Go swimming', '2023-03-16', 2), "
        "('Go swimming', '2023-03-24', 1), "
        "('Go to the gym', '2023-03-22', 3), " 
        "('Study', '2023-03-04', 3), "
        "('Study', '2023-03-11', 6), "
        "('Study', '2023-03-22', 10), "
        "('Study', '2023-03-24', 1), "
        "('Study', '2023-03-30', 5), "
        "('Take a shower', '2023-03-16', 15), "
        "('Take a shower', '2023-03-20', 3), "
        "('Take a shower', '2023-03-29', 8);"
    )

    cursor.execute(insert_query)
    sql_connect.commit()
    sql_connect.close()

if "habit-data.db" in os.listdir():
    os.remove("habit-data.db")
create_table()
insert_sample_data()