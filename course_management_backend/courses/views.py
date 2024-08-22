from django.http import JsonResponse, HttpResponse
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
from .models import Course, CourseInstance
from .db_connection import db

@csrf_exempt
def course_management(request):
    if request.method == 'GET':
        # List all courses
        courses = list(db.courses.find())
        for course in courses:
            course['_id'] = str(course['_id'])
        return JsonResponse(courses, safe=False)

    elif request.method == 'POST':
        # Create a new course
        data = request.POST
        new_course = {
            "title": data.get('title'),
            "course_code": data.get('course_code'),
            "description": data.get('description')
        }
        result = db.courses.insert_one(new_course)
        return JsonResponse({"_id": str(result.inserted_id)}, status=201)

    return HttpResponse(status=405)


@csrf_exempt
def view_or_delete_course(request, course_id):
    if request.method == 'GET':
        # Fetch and return the course details
        course = db.courses.find_one({"_id": ObjectId(course_id)})
        if course:
            course['_id'] = str(course['_id'])
            return JsonResponse(course)
        return HttpResponse(status=404)
    
    elif request.method == 'DELETE':
        # Delete the course and return appropriate status
        result = db.courses.delete_one({"_id": ObjectId(course_id)})
        if result.deleted_count:
            return HttpResponse(status=204)
        return HttpResponse(status=404)
    
    return HttpResponse(status=405)

# POST /api/instances
def create_instance(request):
    if request.method == 'POST':
        data = request.POST
        try:
            # Convert year and semester to integers
            year = int(data.get('year'))
            semester = int(data.get('semester'))
            course_id = int(data.get('course_id'))

            new_instance = {
                "year": year,
                "semester": semester,
                "course_id": course_id
            }

            result = db.instances.insert_one(new_instance)
            return JsonResponse({"_id": str(result.inserted_id)}, status=201)
        except (ValueError, TypeError):
            # Handle the case where year or semester is not a valid integer
            return JsonResponse({"error": "Invalid year or semester format"}, status=400)

    return HttpResponse(status=405)

# GET /api/instances/<year>/<semester>
def list_instances(request, year, semester):
    if request.method == 'GET':
        print(f"Received year: {year}, semester: {semester}")
        

        instances = list(db.instances.find({"year": year, "semester": semester}))
        
        for instance in instances:
            instance['_id'] = str(instance['_id'])  # Convert ObjectId to string
            
        return JsonResponse(instances, safe=False)
    return HttpResponse(status=405)


@csrf_exempt
def view_or_delete_instance(request, year, semester, course_id):
    if request.method == 'GET':
        # Fetch and return the instance details
        instance = db.instances.find_one({
            "year": int(year),         
            "semester": int(semester),
            "course_id": int(course_id),
        })
        if instance:
            instance['_id'] = str(instance['_id'])  # Convert ObjectId to string
            return JsonResponse(instance)
        return HttpResponse(status=404)
    
    elif request.method == 'DELETE':
        # Delete the instance and return appropriate status
        result = db.instances.delete_one({
            "year": int(year),
            "semester": int(semester),
            "course_id": int(course_id)
        })
        if result.deleted_count:
            return HttpResponse(status=204)
        return HttpResponse(status=404)
    
    return HttpResponse(status=405)
