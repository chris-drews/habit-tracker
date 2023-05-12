import TrackerFunctions as tf

def test_habit_loading():
    habits = tf.load_habits()
    assert type(habits) == list