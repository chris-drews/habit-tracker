import tracker as tf
from unittest import mock, TestCase, main, TestLoader


#disable sorting
TestLoader.sortTestMethodsUsing = None


class TestHabits(TestCase):
    def test_habit_loading(self):
        habits = tf.load_habits()
        assert type(habits) == list

    #creation
    def test_habit_creation(self):
        with mock.patch("builtins.input", return_value="d"):
            new_habit = tf.create_habit("test_habit")
        assert new_habit.name == "test_habit"

        #save test habit in preparation for next tests
        habits = tf.load_habits()
        habits.append(new_habit)
        tf.commit_changes(habits)
        habits = tf.load_habits()
        for habit in habits:
            print(habit.name)

    #streak functionality        
    def test_streak_complete(self):
        habits = tf.load_habits()
        tf.get_habit("test_habit", habits).complete()

    #analytic tests
    def test_habit_overview(self):
        habits = tf.load_habits()
        tf.view_all(frequency="daily", habits=habits)

    def test_longest_streak(self):
        habits = tf.load_habits()
        result = tf.longest_current_streak(habits)
        assert result != None

    def test_longest_all_time_streak(self):
        habits = tf.load_habits()
        result = tf.longest_all_time_streak(habits)
        assert result != None

    def test_hardest_streak(self):
        habits = tf.load_habits()
        result = tf.hardest_streak(habits)
        assert result != None

    #deletion
    def test_habit_deletion(self):
        habits = tf.load_habits()
        assert tf.get_habit("test_habit", habits) != None
        with mock.patch("builtins.input", return_value="y"):
            tf.delete_habit(name = "test_habit", habits = habits)
        tf.commit_changes(habits)


if __name__ == "__main__":
    main()