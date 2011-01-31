from django.db import models


class Writeboard(models.Model):
    """
    A Collaborative Writeboard
    """
    
    title = models.CharField(max_length=200)
    
    content = models.TextField(
        blank=True)
    
    def __unicode__(self):
        return u"%s" % self.title