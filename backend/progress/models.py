from django.db import models

from django.db import models
from accounts.models import User
from courses.models import Course

class Progress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    attendance = models.IntegerField(default=0)   # %
    score = models.IntegerField(default=0)        # marks

    completed = models.BooleanField(default=False)
    certificate_issued = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

