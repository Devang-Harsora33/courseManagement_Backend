from django.db import models

class Course:
    def __init__(self, title, course_code, description):
        self.title = title
        self.course_code = course_code
        self.description = description

class CourseInstance:
    def __init__(self, year, semester, course_id):
        self.year = year
        self.semester = semester
        self.course_id = course_id
