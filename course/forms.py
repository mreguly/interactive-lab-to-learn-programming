from django import forms
from django.contrib.auth.models import User
from course.models import Exercise, Lesson, Course, ExerciseTest


class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    # email = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class ExerciseTestForm(forms.ModelForm):
    class Meta:
        model = ExerciseTest
        fields = ['exercise', 'input', 'correct_answer', 'timeout']

        widgets = {
            'exercise': forms.Select(attrs={
                'id': 'post-test-exercise',
            }),

            'input': forms.TextInput(attrs={
                'id': 'post-test-input',
                'required': True,
                'placeholder': 'Name new exercise...'
            }),
            'correct_answer': forms.Textarea(attrs={
                'id': 'post-test-correct_answer',
                'required': True,
                'placeholder': 'Add description...'
            }),

            'timeout': forms.NumberInput(attrs={
                'id': 'post-test-timeout',
            })
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['teacher',  'language', 'title', 'description']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'title']

        widgets = {
            'title': forms.TextInput(attrs={
                'id': 'post-lesson-title',
                'required': True,
                'placeholder': 'Name new lesson...'
            }),
        }


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['course', 'lesson', 'title', 'description', 'test_method', 'code']

        widgets = {
            'lesson': forms.Select(attrs={
                'id': 'post-exercise-lesson',
            }),

            'title': forms.TextInput(attrs={
                'id': 'post-exercise-title',
                'required': True,
                'placeholder': 'Name new exercise...'
            }),
            'description': forms.Textarea(attrs={
                'id': 'post-exercise-description',
                'required': True,
                'placeholder': 'Add description...'
            }),

            'test_method': forms.TextInput(attrs={
                'id': 'post-exercise-test_method',
                'required': False,
                'placeholder': 'Add test_method name...'
            }),
            'code': forms.Textarea(attrs={
                'id': 'post-exercise-code',
                'required': False,
                'placeholder': 'Initialize code...'
            }),

        }
