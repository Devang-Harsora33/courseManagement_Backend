import json
from django.http import JsonResponse, HttpResponse
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
from .db_connection import db

@csrf_exempt
def course_management(request):
    if request.method == 'GET':
        courses = list(db.courses.find())
        for course in courses:
            course['_id'] = str(course['_id'])
        return JsonResponse(courses, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_course = {
                "title": data.get('title'),
                "course_code": data.get('course_code'),
                "description": data.get('description')
            }
            result = db.courses.insert_one(new_course)
            return JsonResponse({"_id": str(result.inserted_id)}, status=201)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({"error": "Invalid input format"}, status=400)

    return HttpResponse(status=405)


@csrf_exempt
def view_or_delete_course(request, course_id):
    if request.method == 'GET':
        course = db.courses.find_one({"_id": ObjectId(course_id)})
        if course:
            course['_id'] = str(course['_id'])
            return JsonResponse(course)
        return HttpResponse(status=404)
    
    elif request.method == 'DELETE':
        result = db.courses.delete_one({"_id": ObjectId(course_id)})
        if result.deleted_count:
            return HttpResponse(status=204)
        return HttpResponse(status=404)
    
    return HttpResponse(status=405)


@csrf_exempt
def create_instance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            year = int(data.get('year'))
            semester = int(data.get('semester'))
            course_title = data.get('title')
            course_id = data.get('course_id')

            new_instance = {
                "year": year,
                "semester": semester,
                "course_title": course_title,
                "course_id": course_id  # Store course_id as ObjectId
            }

            result = db.instances.insert_one(new_instance)
            return JsonResponse({"_id": str(result.inserted_id)}, status=201)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({"error": "Invalid input format"}, status=400)

    return HttpResponse(status=405)


@csrf_exempt
def list_instances(request, year, semester):
    if request.method == 'GET':
        instances = list(db.instances.find({"year": int(year), "semester": int(semester)}))
        for instance in instances:
            instance['_id'] = str(instance['_id'])
        return JsonResponse(instances, safe=False)
    return HttpResponse(status=405)


@csrf_exempt
def view_or_delete_instance(request, year, semester, course_title):
    if request.method == 'GET':
        instance = db.instances.find_one({
            "year": int(year),
            "semester": int(semester),
            "course_title": course_title,
        })
        if instance:
            instance['_id'] = str(instance['_id'])
            return JsonResponse(instance)
        return HttpResponse(status=404)
    
    elif request.method == 'DELETE':
        result = db.instances.delete_one({
            "year": int(year),
            "semester": int(semester),
            "course_title": course_title
        })
        if result.deleted_count:
            return HttpResponse(status=204)
        return HttpResponse(status=404)
    
    return HttpResponse(status=405)