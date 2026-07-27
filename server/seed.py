from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print('Clearing tables...')
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print('Seeding exercises...')
    push_ups = Exercise(name='Push Ups', category='strength', equipment_needed=False)
    squats = Exercise(name='Squats', category='strength', equipment_needed=False)
    running = Exercise(name='Running', category='cardio', equipment_needed=False)
    plank = Exercise(name='Plank', category='balance', equipment_needed=False)
    bench_press = Exercise(name='Bench Press', category='strength', equipment_needed=True)

    db.session.add_all([push_ups, squats, running, plank, bench_press])
    db.session.commit()

    print('Seeding workouts...')
    workout_1 = Workout(date=date(2026, 7, 1), duration_minutes=45, notes='Upper body day')
    workout_2 = Workout(date=date(2026, 7, 3), duration_minutes=30, notes='Cardio session')

    db.session.add_all([workout_1, workout_2])
    db.session.commit()

    print('Seeding workout_exercises...')
    we_1 = WorkoutExercise(workout_id=workout_1.id, exercise_id=push_ups.id, reps=15, sets=3)
    we_2 = WorkoutExercise(workout_id=workout_1.id, exercise_id=bench_press.id, reps=10, sets=4)
    we_3 = WorkoutExercise(workout_id=workout_2.id, exercise_id=running.id, duration_seconds=1200)
    we_4 = WorkoutExercise(workout_id=workout_2.id, exercise_id=plank.id, duration_seconds=60, sets=3)

    db.session.add_all([we_1, we_2, we_3, we_4])
    db.session.commit()

    print('Done seeding!')