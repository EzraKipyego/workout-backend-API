from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts = db.relationship(
        'Workout', secondary='workout_exercises', back_populates='exercises', viewonly=True)

    VALID_CATEGORIES = ['cardio', 'strength', 'flexibility', 'balance']

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError('Exercise name cannot be empty')
        return name

    @validates('category')
    def validate_category(self, key, category):
        if category not in self.VALID_CATEGORIES:
            raise ValueError(f'Category must be one of {self.VALID_CATEGORIES}')
        return category

    def __repr__(self):
        return f'<Exercise {self.id}, {self.name}, {self.category}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    # Constraint defined at the Column level
    duration_minutes = db.Column(db.Integer,
                                  db.CheckConstraint('duration_minutes > 0'),
                                  nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    exercises = db.relationship(
        'Exercise', secondary='workout_exercises', back_populates='workouts', viewonly=True)

    @validates('duration_minutes')
    def validate_duration(self, key, duration_minutes):
        if duration_minutes <= 0:
            raise ValueError('Duration must be greater than 0')
        return duration_minutes

    def __repr__(self):
        return f'<Workout {self.id}, {self.date}, {self.duration_minutes}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, db.CheckConstraint('reps IS NULL OR reps > 0'))
    sets = db.Column(db.Integer, db.CheckConstraint('sets IS NULL OR sets > 0'))
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps')
    def validate_reps(self, key, reps):
        if reps is not None and reps <= 0:
            raise ValueError('Reps must be greater than 0')
        return reps

    @validates('sets')
    def validate_sets(self, key, sets):
        if sets is not None and sets <= 0:
            raise ValueError('Sets must be greater than 0')
        return sets

    def __repr__(self):
        return f'<WorkoutExercise {self.id}, workout_id={self.workout_id}, exercise_id={self.exercise_id}>'