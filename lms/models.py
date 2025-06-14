from django.db import models

from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    lank = True
    null = True
    preview = models.ImageField(upload_to='course_previews/')
    description = models.TextField()

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/')
    video_link = models.URLField()

    def __str__(self):
        return self.name
