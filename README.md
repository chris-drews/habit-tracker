# HabitTracker

HabitTracker is a small app that can be used to keep track of a number of habits over time by using the concept of streaks.

## Installation

Download all the files of the app and make sure to have them in the same folder.

When using the app for the first time, the database for habits to be stored in will be created automatically.

This database comes with pre-existing sample data.

## Usage

To start the app, run HabitTracker.py by either:
  1. Starting the file from within the folder.
  2. Starting the file via the command-line
```shell
$ python HabitTracker.py
```
This will start up the home page of the app.

Here, the various commands you can input, will be listed and briefly explained.

The program runs as a loop, so after typing in a command, you will get the answer for that command and then be able to input the next one.

For some commands, you will need to clarify the specific habit you are referring to. To simplify this, the habits are listed at the beginning of the page with numbers next to them. This way you can type in the numbers instead of writing out the full habit name.

You enter the command right after the question that you are being asked by the program.

## Testing
To test if the functions of the app are running correctly, navigate to the folder the app files are placed in and use the commandline to run the following:
```shell
$ python -m unittest test_habit_app.py
```

## Usage Examples

#### Remember that your input is everything that comes after the question.
### 1. Exiting the app
To exit the app you type in "exit".
```terminal
What would you like to do? exit
```

### 2. Creating a new habit
*Scenario*: You want to create a new daily habit called "Drink 2 liters of water".
First go to the management page.
```terminal
What would you like to do? manage
```
Then use the command "create [your habit]"
```terminal
What would you like to do? create Drink 2 liters of water
```
You will then be asked if this should be a daily or a weekly streak (d for daily in this case).
```terminal
Should this be a daily (d) or a weekly (w) streak? d
```
Your new habit is now added to the floating habits and will be commited to the database upon exiting the app.

### 3. Getting statistics on a particular habit
*Scenario*:ou want to get a statistical overview of the habit "Go for a walk".
First you go to the statistics page.
```terminal
What would you like to do? stats
```
Then you check the number next to your habit and input the following command (in this case 1).
```terminal
1.) Go for a walk
2.) Take a shower
3.) Drink 2 liters of water
What would you like to do? ov 1
```

