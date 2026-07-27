from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema, exercises_schema,
    workout_schema, workouts_schema,
    workout_exercise_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    return {'message': 'Workout tracker API'}


@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    if request.method == 'GET':
        all_workouts = Workout.query.all()
        return jsonify(workouts_schema.dump(all_workouts)), 200

    data = request.get_json()
    try:
        workout = workout_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        db.session.add(workout)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return jsonify({'errors': [str(err)]}), 400

    return jsonify(workout_schema.dump(workout)), 201


@app.route('/workouts/<int:id>', methods=['GET', 'DELETE'])
def workout_by_id(id):
    workout = Workout.query.filter_by(id=id).first()
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404

    if request.method == 'GET':
        return jsonify(workout_schema.dump(workout)), 200

    for we in workout.workout_exercises:
        db.session.delete(we)
    db.session.delete(workout)
    db.session.commit()
    return {}, 204



@app.route('/exercises', methods=['GET', 'POST'])
def exercises():
    if request.method == 'GET':
        all_exercises = Exercise.query.all()
        return jsonify(exercises_schema.dump(all_exercises)), 200

    data = request.get_json()
    try:
        exercise = exercise_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        db.session.add(exercise)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return jsonify({'errors': [str(err)]}), 400

    return jsonify(exercise_schema.dump(exercise)), 201


@app.route('/exercises/<int:id>', methods=['GET', 'DELETE'])
def exercise_by_id(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    if request.method == 'GET':
        data = exercise_schema.dump(exercise)
        data['workouts'] = workouts_schema.dump(exercise.workouts)
        return jsonify(data), 200

    for we in exercise.workout_exercises:
        db.session.delete(we)
    db.session.delete(exercise)
    db.session.commit()
    return {}, 204


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.filter_by(id=workout_id).first()
    exercise = Exercise.query.filter_by(id=exercise_id).first()

    if not workout or not exercise:
        return jsonify({'error': 'Workout or exercise not found'}), 404

    data = request.get_json() or {}
    data['workout_id'] = workout_id
    data['exercise_id'] = exercise_id

    try:
        workout_exercise = workout_exercise_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        db.session.add(workout_exercise)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return jsonify({'errors': [str(err)]}), 400

    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
    