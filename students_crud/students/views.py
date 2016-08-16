from datetime import date

from django.http import Http404, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import (
    require_http_methods, require_GET)

STUDENTS = []


@require_http_methods(["GET", "POST"])
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
    if request.method == 'GET':
        if request.GET.get('format') == 'json':
            return JsonResponse(data={"students": STUDENTS})
        return render(request, 'students_list.html',
                      context={'students': STUDENTS})
    else:
        student_data = request.POST.dict()
        try:
            student_data = dict(
                id=int(student_data['id']),
                name=student_data['name'],
                birth_date=student_data['birth_date'],
                age=int(student_data['age']),
                active=bool(student_data['active']),
            )
        except (KeyError, ValueError):
            return HttpResponseBadRequest(
                'POSTed student data is incomplete or invalid')
        STUDENTS.append(student_data)
        return HttpResponse(status=201)


@require_GET
def students_detail(request, student_id):
    """
    Must return the student with id=:student_id in JSON format,
    or 404 if given id is not found in the STUDENTS list.
    """
    for student_dict in STUDENTS:
        if student_dict['id'] == int(student_id):
            return JsonResponse(data=student_dict)
    raise Http404


@login_required
@require_GET
def students_me(request):
    """
    This view must redirect to the student detail of the currently authenticated
    student. To get the id of the authenticated student you can
    use `request.user.id`.
    Make sure to require authentication for this view.
    """
    return redirect('students:students_detail', student_id=request.user.id)


def students_search(request):
    """
    If a "query" GET param is given, this view will return the list of all
    students in the STUDENTS list that contains "query" value in their names.
    400 BAD REQUEST must be returned if "query" param is not given.
    Make sure to make the search case insensitive.
    """
    query = request.GET.get('query')
    if not query:
        return HttpResponseBadRequest('"query" param must be provided')
    return JsonResponse(data={
        'results': [doc for doc in STUDENTS
                    if query.lower() in doc['name'].lower()]})
