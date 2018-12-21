from django.contrib import admin
from django.urls import include, path

from pyexerciser import views
from graphene_django.views import GraphQLView

urlpatterns = [

    path('graphql', GraphQLView.as_view(graphiql=True)),

    path('', views.index, name="index"),
    path('courses/', include(('course.urls', 'course'), namespace='course')),
    path('registration/', views.UserFormView.as_view(), name="registration"),
    path('login/', views.LoginFormView.as_view(), name="login"),
    path('logout/', views.logout_user, name="logout"),

    path('admin/', admin.site.urls),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
