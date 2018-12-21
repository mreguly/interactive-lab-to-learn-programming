from django.db import models

from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)

from course.models import Course


class CourseCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'author',
            'title',
            'description',
            'language',
        ]

course_detail_url = HyperlinkedIdentityField(
        view_name='course-api:detail',
        lookup_field='pk'
    )


class CourseDetialSerializer(ModelSerializer):
    url = course_detail_url
    user = SerializerMethodField()
    image = SerializerMethodField()
    html = SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'url',
            'user',
            'title',
            'description',
            'language',
            'html',
            'image',

        ]

    def get_html(self, obj):
        return obj.get_markdown()

    def get_user(self, obj):
        return str(obj.user.username)

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image


class CourseListSerializer(ModelSerializer):
    url = course_detail_url
    user = SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'url',
            'user',
            'title',
            'description',
            'language',
            'created',
        ]

    def get_user(self, obj):
        return str(obj.user.username)