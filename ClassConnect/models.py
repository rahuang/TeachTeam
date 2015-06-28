from django.db import models
from django.contrib.auth.models import User


class Assignment(models.Model):
    name = models.TextField()
    term = models.IntegerField()
    category = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    studentScore = models.IntegerField()
    totalScore = models.IntegerField()
    
    def __unicode__(self):
        return "Assignments: " + self.name + " score: " + str(self.studentScore)
        
        