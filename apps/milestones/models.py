from django.contrib.auth.models import User
from django.db import models
import datetime


class Milestone(models.Model):
    """
    A Milestone
    """
    
    title = models.CharField(max_length=255)
    
    due = models.DateField(default=datetime.datetime.today)
    
    responsible = models.ForeignKey(
        User,
        blank=True,
        help_text="Who's responsible?",
        null=True,
        related_name="todos_milestone_responsible")
    
    def __unicode__(self):
        return u'%s' % self.title
    
    def timed(self):
        return Timing.objects.filter(todo__todo_list__milestone=self).aggregate(Sum('duration')).items()[0][1]

    def guesstimated(self):
        try:
            return Guesstimate.objects.filter(todo__todo_list__milestone=self)[0].duration
        except:
            return None

    def remaining(self):
        return 0
        
    def overtime(self):
        return 0
