import database_setup
import os

#create database if necessary
if not "habit_data.db" in os.listdir():
    database_setup.main("habit_data.db")


from unittest import mock, TestCase, main
import tracker as tf


class TestHabits(TestCase):
    def test_habit_loading(self):
        habits = tf.load_habits()
        assert type(habits) == list

    #creation, deletion, streak function
    def test_new_habit(self):
        #creation
        with mock.patch("builtins.input", return_value="d"):
            new_habit = tf.create_habit("test_habit")
        assert new_habit.name == "test_habit"

        habits = tf.load_habits()
        habits.append(new_habit)

        #does saving habits work?
        tf.commit_changes(habits)
        habits = tf.load_habits()
        test_habit = tf.get_habit("test_habit", habits)
        assert test_habit != None

        #streak functionality
        assert test_habit.streak == 0
        test_habit.complete()
        assert test_habit.streak == 1

        #deletion
        assert tf.get_habit("test_habit", habits) != None
        with mock.patch("builtins.input", return_value="y"): #there is a user input here that needs to be simulated
            tf.delete_habit(name = "test_habit", habits = habits)
        tf.commit_changes(habits)

        #reload again to check
        habits = tf.load_habits()#
        names = [habit.name for habit in habits]
        assert "test_habit" not in names

    #analytic tests
    def test_habit_overview(self):
        habits = tf.load_habits()
        tf.view_all(frequency="daily", habits=habits)

    def test_longest_current_streak(self):
        habits = tf.load_habits()
        result = tf.longest_current_streak(habits)
        assert result == [['Take a shower', 10], ['Go to the gym', 3]]

    def test_longest_all_time_streak(self):
        habits = tf.load_habits()
        result = tf.longest_all_time_streak(habits)
        assert result == ("Take a shower", 15)

    def test_hardest_streak(self):
        habits = tf.load_habits()
        result = tf.hardest_streak(habits)
        assert result == ('Go for a walk', 6)

    

if __name__ == "__main__":
    main()