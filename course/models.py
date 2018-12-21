from enum import Enum, unique

from django.contrib.auth.models import Group, User
from django.db import models

EXERCISES = [
    ("Exercise 1", "Exercise 1"),
    ("Exercise 2", "Exercise 2"),
    ("Exercise 3", "Exercise 3"),
    ("Exercise 4", "Exercise 4"),
    ("Exercise 5", "Exercise 5"),
]


def upload_location(instance, filename):
    return "{}/{}".format(instance, filename)


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(BaseModel):

    LANGUAGE_MAP = {
        0: 'python',
        1: 'text/x-csrc',
        2: 'text/x-c++src',
        3: 'text/x-java',
    }

    LANGUAGE_CHOICES = (
        (0, 'Python'),
        (1, 'C'),
        (2, 'C++'),
        (3, 'Java'),
    )


    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_superuser': True})

    title = models.CharField(max_length=100)
    language = models.PositiveIntegerField(max_length=6, choices=LANGUAGE_CHOICES)
    description = models.TextField()

    def __str__(self):
        return '{}'.format(self.title)

    def __unicode__(self):
        return '{}'.format(self.title)

    class Meta:
        db_table = 'course'


class Assigned(BaseModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.title)

    def __unicode__(self):
        return '{}'.format(self.title)

    class Meta:
        db_table = 'lesson'


class Exercise(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    # lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    title = models.CharField(max_length=100) #, choices=EXERCISES)
    description = models.TextField()
    code = models.TextField(blank=True)
    test_method = models.CharField(max_length=50, blank=True)
    timeout = models.IntegerField(default=5)

    def __str__(self):
        return '{}'.format(self.title)

    def __unicode__(self):
        return '{}'.format(self.title)

    class Meta:
        db_table = 'exercise'


class StudentExercise(BaseModel):
    @unique
    class State(Enum):
        complete = 'complete'
        open = 'open'
        initial = 'initial'

    STATE_CHOICES = (
        (State.open.value, 'open'),
        (State.complete.value, 'complete'),
        (State.initial.value, 'initial'),
    )

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    code = models.TextField()
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default=State.initial.value)
    counter = models.IntegerField(default=0)
    test_method = models.CharField(max_length=50)

    def __str__(self):
        return '{} {} {}'.format(self.student, self.exercise.course, self.exercise.title)

    def __unicode__(self):
        return '{} {} {}'.format(self.student, self.exercise.course, self.exercise.title)

    class Meta:
        db_table = 'student_exercise'


class ExerciseTest(BaseModel):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    input = models.CharField(max_length=50)
    correct_answer = models.TextField(max_length=100)
    timeout = models.IntegerField(default=5)

    def __str__(self):
        return '{}'.format(self.exercise.title)

    def __unicode__(self):
        return '{}'.format(self.exercise.title)

    class Meta:
        db_table = 'exercise_test'


class StudentTestResult(BaseModel):
    @unique
    class Result(Enum):
        error = 'ERROR'
        syntax_error = 'SYNTAX_ERROR'
        timeout = 'TIMEOUT'
        correct = 'CORRECT'
        wrong = 'WRONG'
        initial = 'INITIAL'

    RESULT_CHOICES = (
        (Result.error.value, 'ERROR'),
        (Result.syntax_error.value, 'SYNTAX_ERROR'),
        (Result.timeout.value, 'TIMEOUT'),
        (Result.correct.value, 'CORRECT'),
        (Result.wrong.value, 'WRONG'),
        (Result.initial.value, 'INITIAL'),
    )

    test = models.ForeignKey(ExerciseTest, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default=Result.initial.value)
    counter = models.IntegerField(default=0)

    def __str__(self):
        return '{} {} {}'.format(self.student, self.test, self.result)

    def __unicode__(self):
        return '{} {} {}'.format(self.student, self.test, self.result)

    class Meta:
        db_table = 'student_test_result'
