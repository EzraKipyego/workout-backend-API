# Workout tracker API

A backend API for a workout tracking application built with Flask, SQLAlchemy, and Marshmallow. The application provides a platform for personal trainers to manage workouts.

## Features

### Workouts

* Create a workout
* View all workouts
* View a single workout with its exercises.
* Delete a workout

### Exercises

* Create a reusable exercise
* View all exercises
* View a single exercise with the workouts it belongs to
* Delete an exercise

### Workout exercises

* Add an exercise to a workout.

## Tech Stack

### Backend

* Flask
* Flask-SQLAlchemy
* Flask-Migrate
* Marshmallow
* SQLite3

## Run the project

### Clone the repository

```bash
git clone https://github.com/EzraKipyego/workout-backend-API
cd workout-backend-API
```

### Backend

```bash
pipenv install
pipenv shell
pipenv install flask

cd server

flask db init
flask db migrate -m "initial migration"
flask db upgrade head

python seed.py
flask run
```

## License


This project is available for learning purposes.

## Author

Ezra Kipyego