from django.urls import include, path
from . import views


urlpatterns = [
    # preview courses
    path('', views.PreviewCourses.as_view(), name="listing"),

    # statistics
    path('stats/course/<course_id>)', views.statistics_view, name="statistics_view"),
    path('stats/', views.statistics, name="statistics"),

    # save, run, test and detail
    path('<course_id>/lesson/<lesson_id>/exercise/<exercise_id>/execute/', views.execute, name='execute'),
    path('<course_id>/lesson/<lesson_id>/exercise/<exercise_id>/test/', views.test, name='test'),
    path('<course_id>/lesson/<lesson_id>/exercise/<exercise_id>/save_code/', views.save_code, name='test'),
    path('<course_id>/lesson/<lesson_id>/exercise/<exercise_id>/', views.exercise_detail, name='exercise_detail'),


    # # course management
    path('manage/new/course/', views.course_create, name="new_course"),
    path('manage/edit/course/<pk>/', views.course_update, name="edit_course"),
    path('manage/delete/course/<pk>/', views.course_delete, name="delete_course"),

    # lesson management
    path('manage/new/lesson/<course_id>/', views.lesson_create, name="new_lesson"),
    path('manage/edit/lesson/<pk>/', views.lesson_update, name="edit_lesson"),
    path('manage/delete/lesson/<pk>/', views.lesson_delete, name="delete_lesson"),

    # exercise management
    path('manage/new/exercise/<lesson_id>/', views.exercise_create, name="new_exercise"),
    path('manage/edit/exercise/work/<pk>/', views.exercise_update_back, name="exercise_back"),
    path('manage/edit/exercise/<pk>/', views.exercise_update, name="edit_exercise"),
    path('manage/delete/exercise/<pk>/', views.exercise_delete, name="delete_exercise"),

    # test management
    path('manage/new/test/<exercise_id>/', views.test_create, name="new_test"),
    path('manage/edit/test/<pk>/<test_id>/', views.test_update_back, name="test_back"),
    path('manage/edit/test/<pk>/', views.test_update, name="edit_test"),
    path('manage/delete/test/<pk>/', views.test_delete, name="delete_test"),

    # teacher management
    path('manage/new/teacher/', views.teacher_create, name="new_teacher"),

    # management root
    path('manage/', views.manage, name="manage"),

]