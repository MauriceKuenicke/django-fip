import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class USER(models.Model):
    USERID = models.AutoField(primary_key=True)
    USERNAME = models.CharField(max_length=200, unique=True)
    USERPASSWORD = models.CharField(max_length=200)
    USERMAIL = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.USERNAME


class PLAN(models.Model):
    PLANID = models.AutoField(primary_key=True)
    PLANNAME = models.CharField(max_length=200, unique=True)
    USERID = models.ForeignKey(USER, on_delete=models.CASCADE)
    CREATED_AT = models.DateTimeField()

    def __str__(self):
        return self.PLANNAME

    def was_published_recently(self):
        now = timezone.now()
        return  now - datetime.timedelta(days=7) <= self.CREATED_AT <= now

class INCOMESOURCE(models.Model):
    SOURCEID = models.AutoField(primary_key=True)
    CATEGORY = models.CharField(max_length=200, default='No category')
    SOURCENAME = models.CharField(max_length=200, null=False)
    AMOUNT = models.FloatField(null=False)
    PLANID = models.ForeignKey(PLAN, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.SOURCEID}_{self.CATEGORY}_{self.SOURCENAME}"

