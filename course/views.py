import os
from subprocess import Popen, PIPE, TimeoutExpired, run, STDOUT

from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.template.response import TemplateResponse
from django.views.generic import View

from course.models import (
    Course, Lesson, Exercise, ExerciseTest, Assigned, StudentExercise, StudentTestResult
)
from course import engine
from .forms import CourseForm, ExerciseForm, LessonForm, ExerciseTestForm, TeacherForm

import logging
logr = logging.getLogger('custom')


###########################
##
# ________COURSES__________
##
###########################
def course_create(request, template_name='course/new_course.html'):
    if request.user.is_superuser:
        form = CourseForm(request.POST or None)
        if form.is_valid():
            with transaction.atomic():
                course = form.save()

                lesson = Lesson(title="Dummy lesson title", course_id=course.id)
                lesson.save()
                course.lesson = lesson

                exercise = Exercise(
                    course=course,
                    lesson=lesson,
                    title="Dummy exercise title",
                    description="",
                    test_method="",
                    code=""
                )
                exercise.save()

                course.main_exercise = exercise
                return HttpResponseRedirect(reverse('course:exercise_detail', kwargs={"course_id": exercise.course_id,
                                                                                      "lesson_id": exercise.lesson_id,
                                                                                      "exercise_id": exercise.pk}))
        return render(request, template_name, {'form': form})
    return TemplateResponse(request, '404.html', {})


def course_update(request, pk, template_name='course/edit_course.html'):
    if request.user.is_superuser:
        course = get_object_or_404(Course, pk=pk)
        form = CourseForm(request.POST or None, instance=course)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                return HttpResponseRedirect(reverse('course:manage'))
        return render(request, template_name, {'form': form})
    return TemplateResponse(request, '404.html', {})


def course_delete(request, pk, template_name='confirm_delete.html'):
    if request.user.is_superuser:
        course = get_object_or_404(Course, pk=pk)
        if request.method == 'POST':
            with transaction.atomic():
                course.delete()
                return HttpResponseRedirect(reverse('course:manage'))
        return render(request, template_name, {'object': course})
    return TemplateResponse(request, '404.html', {})


###########################
##
# ________LESSONS__________
##
###########################
def lesson_create(request, course_id, template_name='course/new_lesson.html'):
    if request.user.is_superuser:


        # request.POST['course'] = Course.objects.get(course_id=request.POST['course'])
        form = LessonForm(request.POST or None, initial={'course': course_id})

        print(request.POST)
        print(form.is_valid())

        if form.is_valid():
            with transaction.atomic():
                lesson = form.save()
                print("AAA", lesson)
                return HttpResponseRedirect(reverse('course:manage'))

        print(form.errors)
        return render(request, template_name, {'form': form})
    return TemplateResponse(request, '404.html', {})


def lesson_update(request, pk, template_name='course/new_lesson.html'):
    if request.user.is_superuser:
        lesson = get_object_or_404(Lesson, pk=pk)

        form = LessonForm(request.POST or None, instance=lesson)
        if form.is_valid():
            with transaction.atomic():
                exercises = Exercise.objects.filter(lesson=lesson)
                new_lesson = form.save()

                # change also lesson's exercises
                for exercise in exercises:
                    exercise.course = new_lesson.course
                    exercise.save()

                return HttpResponseRedirect(reverse('course:manage'))
        return render(request, template_name, {'form': form})
    return TemplateResponse(request, '404.html', {})


def lesson_delete(request, pk, template_name='confirm_delete.html'):
    if request.user.is_superuser:
        lesson = get_object_or_404(Lesson, pk=pk)
        if request.method == 'POST':
            with transaction.atomic():
                lesson.delete()
                return HttpResponseRedirect(reverse('course:manage'))
        return render(request, template_name, {'object': lesson})
    return TemplateResponse(request, '404.html', {})


###########################
##
# ________EXERCISES________
##
###########################
def exercise_create(request, lesson_id, template_name='course/new_exercise.html'):
    if request.user.is_superuser:
        lesson = Lesson.objects.get(pk=lesson_id)

        print("ASASFASSSSSSSSSSSSSSSSSSSSSSSSsss")
        print(request.POST)


        form = ExerciseForm(request.POST or None, initial={'course': lesson.course, 'lesson': lesson})
        print(form.is_valid())
        if form.is_valid():
            with transaction.atomic():
                exercise = form.save()
                print(exercise)
                course_id = Course.objects.get(id=exercise.course_id).id

                # update also to student
                assigned = Assigned.objects.filter(course_id=course_id)
                for assigned in assigned:
                    student_exercise = StudentExercise(exercise=exercise, lesson=lesson, student=assigned.student,
                                                       code=exercise.code, test_method=exercise.test_method)
                    student_exercise.save()

                return HttpResponseRedirect(reverse('course:manage'))
        return render(request, template_name, {'form': form})
    return TemplateResponse(request, '404.html', {})


def exercise_update(request, pk, template_name='course/new_exercise.html'):
    if request.user.is_superuser:
        exercise = get_object_or_404(Exercise, pk=pk)

        form = ExerciseForm(request.POST or None, instance=exercise)
        print("UPDATE", exercise)
        print("UPDATE", request.POST)
        print("UPDATE", form.is_valid())

        if form.is_valid():
            with transaction.atomic():
                form.save()
                return HttpResponseRedirect(reverse('course:manage'))

        return render(request, template_name, {'form': form})
    return TemplateResponse(request, '404.html', {})


# def exercise_update_back(request, pk, template_name='course/new_exercise.html'):
#     if request.user.is_superuser:
#         exercise = get_object_or_404(Exercise, pk=pk)
#         form = ExerciseForm(request.POST or None, instance=exercise)
#         if form.is_valid():
#             with transaction.atomic():
#                 form.save()
#
#                 return HttpResponseRedirect(reverse('course:exercise_detail', kwargs={"course_id": exercise.course_id,
#                                                                                       "lesson_id": exercise.lesson_id,
#                                                                                       "exercise_id": exercise.pk}))
#         return render(request, template_name, {'form': form})
#     return TemplateResponse(request, '404.html', {})
from django.core import serializers

def exercise_update_back(request, pk, template_name='course/new_exercise.html'):
    if request.user.is_superuser:
        if request.method == "GET":
            exercise = get_object_or_404(Exercise, pk=pk)
            form = ExerciseForm(request.POST or None, instance=exercise)
            if form.is_valid():
                with transaction.atomic():
                    form.save()

                    return HttpResponseRedirect(reverse('course:exercise_detail', kwargs={"course_id": exercise.course_id,
                                                                                          "lesson_id": exercise.lesson_id,
                                                                                          "exercise_id": exercise.pk}))
            return render(request, template_name, {'form': form})
        else:
            # POST
            print(request.POST)
            exercise = get_object_or_404(Exercise, pk=pk)
            print(exercise)
            print(exercise.__dict__)
            # print("ASASF", exercise.values())
            # form = ExerciseForm(exercise.__dict__)
            serialized_exercise = serializers.serialize('json', [exercise, ])
            # print(serialized_exercise.get('fields'))
            print(serialized_exercise)
            return JsonResponse(serialized_exercise, safe=False)
    return TemplateResponse(request, '404.html', {})


def exercise_delete(request, pk, template_name='confirm_delete.html'):
    if request.user.is_superuser:
        exercise = get_object_or_404(Exercise, pk=pk)
        if request.method == 'POST':
            with transaction.atomic():
                exercise.delete()
                return HttpResponseRedirect(reverse('course:manage'))
        return render(request, template_name, {'object': exercise})
    return TemplateResponse(request, '404.html', {})


###########################
##
# ________TESTS________
##
###########################
def test_create(request, exercise_id, template_name='course/new_test.html'):
    if request.user.is_superuser:


        form = ExerciseTestForm(request.POST or None, initial={'exercise': exercise_id})

        print("TEST", request.POST)
        print(form.is_valid())

        if form.is_valid():
            with transaction.atomic():
                new_test = form.save()

                # update also to student
                students_exercises = StudentExercise.objects.filter(exercise=new_test.exercise)
                for exercise in students_exercises:
                    test_result = StudentTestResult(test=new_test, student=exercise.student)
                    test_result.save()

                return HttpResponseRedirect(reverse('course:manage'))
        print(form.errors)
        return render(request, template_name, {'form': form})
    return TemplateResponse(request, '404.html', {})


def test_update(request, pk, template_name='course/new_test.html'):
    if request.user.is_superuser:
        test = get_object_or_404(ExerciseTest, pk=pk)
        form = ExerciseTestForm(request.POST or None, instance=test)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                return HttpResponseRedirect(reverse('course:manage'))
        return render(request, template_name, {'form': form})
    return TemplateResponse(request, '404.html', {})



def test_update_back(request, pk, test_id, template_name='course/new_test.html'):
    if request.user.is_superuser:
        exercise = get_object_or_404(Exercise, pk=pk)
        test = get_object_or_404(ExerciseTest, id=test_id)
        form = ExerciseTestForm(request.POST or None, instance=test)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                return HttpResponseRedirect(reverse('course:exercise_detail', kwargs={"course_id": exercise.course_id,
                                                                                      "lesson_id": exercise.lesson_id,
                                                                                      "exercise_id": exercise.pk}))
        return render(request, template_name, {'form': form})
    return TemplateResponse(request, '404.html', {})


def test_delete(request, pk, template_name='confirm_delete.html'):
    if request.user.is_superuser:
        test = get_object_or_404(Exercise, pk=pk)
        if request.method == 'POST':
            with transaction.atomic():
                test.delete()
                return HttpResponseRedirect(reverse('course:manage'))
        return render(request, template_name, {'object': test})
    return TemplateResponse(request, '404.html', {})

###########################
##
# ________TEACHERS_________
##
###########################
def teacher_create(request, template_name='course/new_teacher.html'):
    if request.user.is_superuser:
        form = TeacherForm(request.POST or None)
        if form.is_valid():
            with transaction.atomic():
                teacher = form.save()
                # clean data
                password = form.cleaned_data['password']

                teacher.is_superuser = True
                teacher.set_password(password)
                teacher.save()

                return HttpResponseRedirect(reverse('course:new_course'))
        return render(request, template_name, {'form': form})
    return TemplateResponse(request, '404.html', {})


class PreviewCourses(View):
    template_name = 'course/courses.html'

    def get(self, request):
        courses = Course.objects.all()
        authenticated = request.user.is_authenticated

        # check student's assigned courses to show Enter or Assign buttons
        if authenticated:
            user = User.objects.get(id=request.user.id)
            for course in courses:
                course.main_exercise = Exercise.objects.filter(course=course).first()
                try:
                    Assigned.objects.get(course=course, student=user)
                    course.already_assigned = True
                except Assigned.DoesNotExist:
                    course.already_assigned = False
        else:
            for course in courses:
                course.main_exercise = Exercise.objects.filter(course=course).first()
                course.already_assigned = True


        context = {
            "courses": courses,
        }
        return TemplateResponse(request, self.template_name, context)

    def post(self, request):
        course_id = request.POST.get('course_id')
        course = Course.objects.get(id=course_id)
        course.main_exercise = Exercise.objects.filter(course=course).first()
        lesson = Lesson.objects.filter(course=course).first()
        exercises = Exercise.objects.filter(course=course)
        student = User.objects.get(id=request.user.id)

        # run in transaction
        with transaction.atomic():
            # new Assigned student
            assign = Assigned(course=course, student=student)
            assign.save()

            for exercise in exercises:
                # copy Exercises
                student_exercise = StudentExercise(exercise=exercise, lesson=exercise.lesson, student=student,
                                                   code=exercise.code,
                                                   test_method=exercise.test_method)
                student_exercise.save()

                # copy ExerciseTests
                tests = ExerciseTest.objects.filter(exercise=exercise)
                for test in tests:
                    student_result = StudentTestResult(test=test, student=student)
                    student_result.save()

        # return redirect('/courses/' + course_id + '/exercise/' + str(course.main_exercise.id))
        return redirect(reverse('exercise_detail', kwargs={"course_id": course_id,
                                                           "lesson_id": lesson.id,
                                                           "exercise_id": course.main_exercise.id}))


def manage(request):
    if request.user.is_superuser:
        courses = Course.objects.all()
        lessons = Lesson.objects.all()
        exercises = Exercise.objects.all()
        tests = ExerciseTest.objects.all()

        context = {
            "courses": courses,
            "lessons": lessons,
            "exercises": exercises,
            "tests": tests
        }
        return TemplateResponse(request, 'course/manage.html', context)
    return TemplateResponse(request, '404.html', {})


def statistics(request):
    if request.user.is_superuser:
        courses = Course.objects.all()

        for course in courses:
            course.student_count = Assigned.objects.filter(course=course).count()
            course.lesson_count = Lesson.objects.filter(course=course).count()
            course.exercise_count = Exercise.objects.filter(course=course).count()

        context = {
            "courses": courses,
        }
        return TemplateResponse(request, 'course/statistics.html', context)
    return TemplateResponse(request, '404.html', {})


def statistics_view(request, course_id):
    if request.user.is_superuser:
        data = []
        students = Assigned.objects.filter(course_id=course_id).select_related('student')
        exercises = Exercise.objects.filter(course_id=course_id)

        headers = ["Name"]
        for exercise in exercises:
            headers.append(exercise.title[0:3])
        headers.append("Total")

        for assigned in students:
            exer_data = [assigned.student]
            counter = 0
            for exercise in exercises:
                s_exercise = StudentExercise.objects.get(exercise=exercise, student=assigned.student)
                if s_exercise.state == 'open':
                    exer_data.append("ER({})".format(s_exercise.counter))
                elif s_exercise.state == 'complete':
                    exer_data.append("OK({})".format(s_exercise.counter))
                    counter += 1
                elif s_exercise.state == 'initial':
                    if s_exercise.counter > 0:
                        exer_data.append("R({})".format(s_exercise.counter))
                    else:
                        exer_data.append("—")
            exer_data.append("{}/{}".format(counter, len(exercises)))
            data.append(exer_data)

        context = {
            "data": data,
            "headers": headers,
        }
        return TemplateResponse(request, 'course/statistics_detail.html', context)
    return TemplateResponse(request, '404.html', {})


def exercise_detail(request, course_id, lesson_id, exercise_id):
    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(course_id=course_id)
    exercise_tests = ExerciseTest.objects.filter(exercise_id=exercise_id)

    lesson_map = dict()
    authenticated = request.user.is_authenticated

    # if logged in student use student's exercise
    if authenticated:
        student = User.objects.get(id=request.user.id)

        # check change in exercise state
        student_exercises = StudentExercise.objects.filter(student=student)
        for s_exercise in student_exercises:
            is_correct = True

            # check if all test results are correct
            s_tests = ExerciseTest.objects.filter(exercise=s_exercise.exercise)
            for s_test in s_tests:
                test = StudentTestResult.objects.get(test=s_test, student=student)
                if test.result == "WRONG" or test.result == "ERROR" or test.result == "SYNTAX_ERROR" or test.result == "TIMEOUT":
                    is_correct = False
                    break
                elif test.result == "INITIAL":
                    is_correct = None
                    break

            # change state of exercise
            if len(s_tests) > 0:
                if is_correct:
                    s_exercise.state = 'complete'
                    s_exercise.save()
                elif is_correct == False:
                    s_exercise.state = 'open'
                    s_exercise.save()
            else:
                if s_exercise.counter > 0:
                    s_exercise.state = 'complete'
                    s_exercise.save()

        student_exercise = StudentExercise.objects.get(exercise_id=exercise_id, student=student)

        # set students test results for each test
        for s_test in exercise_tests:
            s_test.result = StudentTestResult.objects.get(student=student, test=s_test).result

    # create dict of lessons and it's exercises
    for lesson in lessons:
        exercises = Exercise.objects.filter(lesson=lesson, course_id=course_id)
        if authenticated:
            lesson.exercises_done = StudentExercise.objects.filter(lesson=lesson, student=student,
                                                               state='complete').count()
            for exercise in exercises:
                exercise.state = StudentExercise.objects.get(exercise=exercise, student=student).state
        lesson_map[lesson] = exercises

    # not authenticated
    exercise = Exercise.objects.get(id=exercise_id, course_id=course_id)

    if not authenticated:
        # not authenticated - show empty exercise
        student_exercise = exercise

    course.language = Course.LANGUAGE_MAP.get(course.language)

    # print(ExerciseForm(initial={'course': course_id, 'lesson': exercise.lesson}))

    context = {
        'lesson_map': sorted(lesson_map.items(), key=lambda x: x[0].id),
        'exercise_id': exercise.id,
        'exercise_title': exercise.title,
        'exercise_description': exercise.description,
        'exercise_code': student_exercise.code,
        'exercise_tests': exercise_tests,

        'course': course,
        'lesson_form': LessonForm(initial={'course': course_id}),
        'exercise_form': ExerciseForm(initial={'course': course_id, 'lesson': exercise.lesson}),
        'test_form': ExerciseTestForm(initial={'exercise': exercise})
    }

    return render(request, 'course/detail.html', context)


def execute(request, course_id, lesson_id, exercise_id):
    authenticated = request.user.is_authenticated

    if authenticated:
        code = request.POST.get('content').strip()
        stop_endless_run_sh = settings.DOCKER_STOP_SH_PATH


        timeout = Exercise.objects.get(id=exercise_id).timeout

        save_path = settings.DATA_RUNS_PATH

        # save student's code to db and increase counter
        exercise = StudentExercise.objects.get(exercise_id=exercise_id, student=request.user)

        exercise.counter += 1
        exercise.code = code
        exercise.save()

        course = Course.objects.get(id=course_id)

        print(course)
        print(course.language)

        language = course.language

        if language == 0:
            # run in docker --> python
            shell_script = settings.RUN_PYTHON_CODE_SH_PATH
            file_name = "USR{}_python.py".format(request.user.id)
            result = engine.run_python_in_docker(save_path, code, shell_script, stop_endless_run_sh, file_name, timeout)
        elif language == 1:
            # run in docker --> C
            shell_script = settings.RUN_C_CODE_SH_PATH
            file_name = "USR{}_csrc.c".format(request.user.id)
            result = engine.run_c_in_docker(save_path, code, shell_script, stop_endless_run_sh, file_name, timeout)
        elif language == 2:
            # run in docker --> C++
            shell_script = settings.RUN_CPP_CODE_SH_PATH
            file_name = "USR{}_cppsrc.cpp".format(request.user.id)
            result = engine.run_in_docker(save_path, code, shell_script, stop_endless_run_sh, file_name, timeout)
        elif language == 3:
            # run in docker --> Java
            shell_script = settings.RUN_JAVA_CODE_SH_PATH
            file_name = "USR{}_javasrc.java".format(request.user.id)
            result = engine.run_java_in_docker(save_path, code, shell_script, stop_endless_run_sh, file_name, timeout)


        # print(exercise)
        # print(code)
        # print()
        # print(exercise.code)



        return JsonResponse({'result': result})
    else:
        return JsonResponse({})


def save_code(request, course_id, lesson_id, exercise_id):
    authenticated = request.user.is_authenticated

    code = request.POST.get('content').strip()

    test_template = """import sys, os
sys.stdout = open(os.devnull, 'w')
{}
sys.stdout = sys.__stdout__"""

    if authenticated:
        # student save code when testing
        student_exercise = StudentExercise.objects.get(exercise_id=exercise_id, student=request.user)
        test_fname = "EX{}USR{}.py".format(student_exercise.id, request.user.id)
        student_exercise.code = code
        student_exercise.save()

        with open(os.path.join(settings.DATA_TESTS_PATH, test_fname), 'w') as test_file:
            test_file.write(test_template.format(code))

    return JsonResponse({})


def test(request, course_id, lesson_id, exercise_id):
    authenticated = request.user.is_authenticated

    if authenticated:
        # DB calls
        test_id = request.POST.get('test_id')
        exercise = Exercise.objects.get(id=exercise_id)
        student_exercise = StudentExercise.objects.get(exercise_id=exercise_id, student=request.user)
        test = ExerciseTest.objects.get(id=test_id)

        # paths, scripts and file names preparation
        run_test_sh = settings.RUN_TESTS_SH_PATH
        docker_stop_sh = settings.DOCKER_STOP_SH_PATH

        data_tests_path = settings.DATA_TESTS_PATH

        testing_file = "EX{}USR{}.py".format(student_exercise.id, request.user.id)
        container_name = "{}_{}".format(testing_file, test_id)

        testing_file_path = os.path.join(data_tests_path, testing_file)

        template_assert = "assert({}({}) == {})".format(exercise.test_method, test.input, test.correct_answer)

        with open(testing_file_path, 'a') as file:
            file.write("\n{}".format(template_assert))

        # docker call
        try:

            p = Popen([run_test_sh, container_name, testing_file_path, testing_file],
                      stdin=PIPE,
                      stdout=PIPE, stderr=PIPE)
            output, err = p.communicate(timeout=5)
            # print(output, err)

            err = err.decode('utf-8').strip()
            if err:
                if "AssertionError" in err:
                    result = 'WRONG'
                    logr.debug("USER: {}. Wrong: {}".format(request.user.username, err))
                else:
                    result = 'SYNTAX_ERROR'
                    logr.debug("USER: {}. Syntax Error: {}".format(request.user.username, err))
            else:
                result = "CORRECT"

        except TimeoutExpired as e:
            run([docker_stop_sh, container_name], stderr=STDOUT)
            result = 'TIMEOUT'
            logr.debug("USER: {}. Timeout: {}".format(request.user.username, e))
        except Exception as e:
            result = 'ERROR'
            # logr.info("USER: {}. Syntax Error: {}".format(request.user.username, err))
            logr.error("USER: {}. Syntax Error: {}".format(request.user.username, e))

        # remove added line with assert
        os.system('sed -i "$ d" {0}'.format(testing_file_path))

        student = User.objects.get(id=request.user.id)
        student_result = StudentTestResult.objects.get(test_id=test_id, student=student)
        student_result.counter += 1
        if student_result.result != result:
            student_result.result = result
            student_result.save()

        return JsonResponse({'result': result})
    else:
        return JsonResponse({})
