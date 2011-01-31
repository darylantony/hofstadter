from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_save, post_save
from milestones.models import Milestone
import datetime


"""
    Notes
    
    Use Timings & Guesstimates to
    
        - make suppositions about the percentage completion of a task
        


"""

class Category(models.Model):
    """
    A ToDo Category
    """
    name = models.CharField(
        max_length=255)
        
    def __unicode__(self):
        return u'%s' % self.name
    
class ToDoList(models.Model):
    """
    A List of ToDo's
    """
    
    title = models.CharField(max_length=255)
    
    description = models.TextField(blank=True)
    
    milestone = models.ForeignKey(
        Milestone,
        blank=True,
        null=True)
    
    def __unicode__(self):
        return u'%s' % self.title
        
    def timed(self):
        """
        An aggregate of Timings
        """
        return Timing.objects.filter(todo__todo_list=self).aggregate(Sum('duration')).items()[0][1]
        
    def guesstimated(self):
        try:
            return Guesstimate.objects.filter(todo__todo_list=self)[0].duration
        except:
            return None
        
    def remaining(self):
        return 0
        
    def overtime(self):
        return 0

class ToDo(models.Model):
    """
    A ToDo
    """
    
    task = models.TextField()
    
    notes = models.TextField(
        blank=True,
        null=True)
    
    todo_list = models.ForeignKey(ToDoList)
    
    categories = models.ManyToManyField(Category)
    
    responsible = models.ForeignKey(
        User,
        blank=True,
        null=True)
        
    due = models.DateField(
        blank=True,
        null=True)
        
    done = models.BooleanField()
    
    def __unicode__(self):
        return u"%s" % self.task
        
    def timed(self):
        """
        An aggregate of Timings
        """
        return self.timing_set.aggregate(Sum('duration')).items()[0][1]
        
    def guesstimated(self):
        try:
            return self.guesstimate_set.all()[0].duration
        except:
            return None
        
    def remaining(self):
        return 0
        
    def overtime(self):
        return 0
        
class Timing(models.Model):
    """
    A period of time recorded against a ToDo
    
    After each timing there's an opportunity to
    enter in an estimate of the total time 'left'
    to complete the task.
    """
    
    todo = models.ForeignKey(ToDo)
    
    start = models.DateTimeField(
        default=datetime.datetime.now)
    stop = models.DateTimeField(
        blank=True,
        null=True)
        
    estimate = models.FloatField(
        blank=True,
        help_text="An estimate of the time remaining for a given To Do.  Estimates are calculated from the beginning of a Timing.",
        null=True)
        
    duration = models.FloatField(
        blank=False,
        editable=False,
        help_text="Makes aggregations easier. Calculates on save.",
        null=True)
          
    notes = models.TextField(blank=True)
    
    def __unicode__(self):
        return u'%s' % (self.todo)
        
    def save(self, *args, **kwargs):
        if self.start and self.stop:
            timedelta = self.stop - self.start
            self.duration = float(timedelta.seconds) / 60.00 / 60.00 # fix!
        super(Timing, self).save(*args, **kwargs)

class Guesstimate(models.Model):
    """
    A Guesstimate of time to do a ToDo
    
        For now.
            Only one estimate per todo.
            
        In the future.
            Revision estimates after each Timing.
            The latest estimate superseeds the previous.
    """
    
    timing = models.ForeignKey(
        Timing,
        blank=True,
        null=True)
        
    first = models.BooleanField()
    
    duration = models.FloatField(
        default=1.0,
        help_text="Guesstimate in decimal hours, e.g., 1.5(hrs) of the total task duration, or time left for the task")
    
    def __unicode__(self):
        return u'%s: %s' % (self.todo, self.duration)
        
    @property
    def timed(self):
        return Timing.objects.filter(todo__timing__todo__guesstimate=self).distinct().aggregate(Sum('duration')).items()[0][1] or 0.0
        
    def remaining(self):
        """
        The current duration estimate minus the aggregation of the Timings
        """
        return (self.duration - self.timed) if (self.duration - self.timed) >= 0 else None
        
    def overtime(self):
        """
        Time spent over the guesstimate
        """
        return (self.duration - self.timed) if (self.duration - self.timed) < 0 else None