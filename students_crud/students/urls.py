from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.students_list, name='students_list'),
    url(r'(?P<student_id>[0-9]+)$', views.students_detail, name='students_detail'),
    url(r'me$', views.students_me, name='students_me'),
    url(r'search$', views.students_search, name='students_search'),

]


# /students/
# /students/:id
# /students/me (auth only)
# /students/search
