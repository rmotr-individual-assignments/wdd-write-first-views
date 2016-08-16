from datetime import date

from django.http import Http404, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import (
    require_http_methods, require_GET)

STUDENTS = []


# HINT: use django views decorators to restrict this view to GET and POST methods
def students_list(request):
    """
    When GET method is received, this view must return the list of all active
    students found in the STUDENTS list.
    Optionally, a "?format=json" GET param might be sent. In that case the
    response content type must be JSON instead of HTML

    On the other hand, if a POST request is performed, a new student must be
    appended into the STUDENTS list.
    Make sure to validate that all required fields were POSTed and they all
    have the proper data type (int, bool, etc)
    """
    pass


# HINT: require only GET method
def students_detail(request, student_id):
    """
    Must return the student with id=:student_id in JSON format,
    or 404 if given id is not found in the STUDENTS list.
    """
    pass


# HINT: require authentication and GET method only
def students_me(request):
    """
    This view must redirect to the student detail of the currently authenticated
    student. To get the id of the authenticated student you can
    use `request.user.id`.
    Make sure to require authentication for this view.
    """
    pass


def students_search(request):
    """
    If a "query" GET param is given, this view will return the list of all
    students in the STUDENTS list that contains "query" value in their names.
    400 BAD REQUEST must be returned if "query" param is not given.
    Make sure to make the search case insensitive.
    """
    pass
