from marshmallow import Schema, fields, validate, post_load

from models import db, Exercise, Workout, WorkoutExercise


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(
        required=True,
        validate=validate.OneOf(['cardio', 'strength', 'flexibility', 'balance'])
    )
    equipment_needed = fields.Bool(load_default=False)

    @post_load
    def make_exercise(self, data, **kwargs):
        return Exercise(**data)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1))
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @post_load
    def make_workout_exercise(self, data, **kwargs):
        return WorkoutExercise(**data)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True)
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)

    @post_load
    def make_workout(self, data, **kwargs):
        return Workout(**data)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=('workout_exercises',))

workout_exercise_schema = WorkoutExerciseSchema()