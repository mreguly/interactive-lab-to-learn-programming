from django.contrib import admin

from .models import (Exercise, Lesson, Course, ExerciseTest, Assigned, StudentExercise,
                     StudentTestResult)


class StudentExerciseModelAdmin(admin.ModelAdmin):
    list_display = ['student', 'exercise', 'counter', 'updated', 'created']

class AssignedModelAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'student_id', 'updated', 'created']


class ExerciseTestModelAdmin(admin.ModelAdmin):
    list_display = ['exercise', 'input', 'correct_answer', 'updated', 'created']


class StudentTestResultModelAdmin(admin.ModelAdmin):
    list_display = ['test', 'student', 'result', 'updated', 'created']


class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'teacher', 'updated', 'created']

    list_field = ['updated', 'created']

    search_fields = ['title', 'description']


class LessonModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'updated', 'created']

    list_display_links = ['course']
    list_editable = ['title']


class ExerciseModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'course', 'updated', 'created']

    list_display_links = ['course']
    list_editable = ['title']


admin.site.register(ExerciseTest, ExerciseTestModelAdmin)
admin.site.register(StudentExercise, StudentExerciseModelAdmin)
admin.site.register(StudentTestResult, StudentTestResultModelAdmin)
admin.site.register(Assigned, AssignedModelAdmin)
admin.site.register(Course, CourseModelAdmin)
admin.site.register(Lesson, LessonModelAdmin)
admin.site.register(Exercise, ExerciseModelAdmin)
